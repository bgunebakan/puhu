use pyo3::prelude::*;
use pyo3::types::{PyBytes, PyType};
use image::{DynamicImage, ImageFormat};
use std::io::Cursor;
use std::path::PathBuf;
use crate::errors::PuhuError;
use crate::formats;
use crate::operations;
use crate::utils::color_type_to_mode_string;
use crate::conversions;
use crate::palette;

#[derive(Clone)]
enum LazyImage {
    Loaded(DynamicImage),
    /// Image data stored as file path
    Path { path: PathBuf },
    /// Image data stored as bytes
    Bytes { data: Vec<u8> },
}

impl LazyImage {
    /// Ensure the image is loaded
    fn ensure_loaded(&mut self) -> Result<&DynamicImage, PuhuError> {
        match self {
            LazyImage::Loaded(img) => Ok(img),
            LazyImage::Path { path } => {
                let img = image::open(path)
                    .map_err(|e| PuhuError::ImageError(e))?;
                *self = LazyImage::Loaded(img);
                match self {
                    LazyImage::Loaded(img) => Ok(img),
                    _ => unreachable!("Just set to Loaded variant")
                }
            }
            LazyImage::Bytes { data } => {
                let cursor = Cursor::new(data);
                let reader = image::io::Reader::new(cursor).with_guessed_format()
                    .map_err(|e| PuhuError::Io(e))?;
                let img = reader.decode()
                    .map_err(|e| PuhuError::ImageError(e))?;
                *self = LazyImage::Loaded(img);
                match self {
                    LazyImage::Loaded(img) => Ok(img),
                    _ => unreachable!("Just set to Loaded variant")
                }
            }
        }
    }
}

#[pyclass(name = "Image")]
pub struct PyImage {
    lazy_image: LazyImage,
    format: Option<ImageFormat>,
}

impl PyImage {
    fn get_image(&mut self) -> Result<&DynamicImage, PuhuError> {
        self.lazy_image.ensure_loaded()
    }
}

#[pymethods]
impl PyImage {
    #[new]
    fn __new__() -> Self {
        // Create a default 1x1 RGB image for compatibility
        let image = DynamicImage::new_rgb8(1, 1);
        PyImage { 
            lazy_image: LazyImage::Loaded(image), 
            format: None 
        }
    }

    #[classmethod]
    #[pyo3(signature = (mode, size, color=None))]
    fn new(_cls: &Bound<'_, PyType>, mode: &str, size: (u32, u32), color: Option<(u8, u8, u8, u8)>) -> PyResult<Self> {
        let (width, height) = size;
        
        if width == 0 || height == 0 {
            return Err(PuhuError::InvalidOperation(
                "Image dimensions must be greater than 0".to_string()
            ).into());
        }
        
        let image = match mode {
            "RGB" => {
                let (r, g, b, _) = color.unwrap_or((0, 0, 0, 255));
                DynamicImage::ImageRgb8(
                    image::RgbImage::from_pixel(width, height, image::Rgb([r, g, b]))
                )
            }
            "RGBA" => {
                let (r, g, b, a) = color.unwrap_or((0, 0, 0, 0));
                DynamicImage::ImageRgba8(
                    image::RgbaImage::from_pixel(width, height, image::Rgba([r, g, b, a]))
                )
            }
            "L" => {
                let (gray, _, _, _) = color.unwrap_or((0, 0, 0, 255));
                DynamicImage::ImageLuma8(
                    image::GrayImage::from_pixel(width, height, image::Luma([gray]))
                )
            }
            "LA" => {
                let (gray, _, _, a) = color.unwrap_or((0, 0, 0, 255));
                DynamicImage::ImageLumaA8(
                    image::GrayAlphaImage::from_pixel(width, height, image::LumaA([gray, a]))
                )
            }
            _ => {
                return Err(PuhuError::InvalidOperation(
                    format!("Unsupported image mode: {}", mode)
                ).into());
            }
        };
        
        Ok(PyImage {
            lazy_image: LazyImage::Loaded(image),
            format: None,
        })
    }

    #[classmethod]
    fn open(_cls: &Bound<'_, PyType>, path_or_bytes: &Bound<'_, PyAny>) -> PyResult<Self> {
        if let Ok(path) = path_or_bytes.extract::<String>() {
            // Store path for lazy loading
            let path_buf = PathBuf::from(&path);
            let format = ImageFormat::from_path(&path).ok();
            Ok(PyImage { 
                lazy_image: LazyImage::Path { path: path_buf },
                format 
            })
        } else if let Ok(bytes) = path_or_bytes.downcast::<PyBytes>() {
            // Store bytes for lazy loading
            let data = bytes.as_bytes().to_vec();
            // Try to guess format from bytes header
            let format = {
                let cursor = Cursor::new(&data);
                image::io::Reader::new(cursor).with_guessed_format()
                    .ok()
                    .and_then(|r| r.format())
            };
            Ok(PyImage { 
                lazy_image: LazyImage::Bytes { data },
                format 
            })
        } else {
            Err(PuhuError::InvalidOperation(
                "Expected file path (str) or bytes".to_string()
            ).into())
        }
    }

    #[pyo3(signature = (path_or_buffer, format=None))]
    fn save(&mut self, path_or_buffer: &Bound<'_, PyAny>, format: Option<String>) -> PyResult<()> {
        if let Ok(path) = path_or_buffer.extract::<String>() {
            // Save to file path
            let save_format = if let Some(fmt) = format {
                formats::parse_format(&fmt)?
            } else {
                ImageFormat::from_path(&path)
                    .map_err(|_| PuhuError::UnsupportedFormat(
                        "Cannot determine format from path".to_string()
                    ))?
            };
            
            // Ensure image is loaded before saving
            let image = self.get_image()?;
            
            Python::with_gil(|py| {
                py.allow_threads(|| {
                    image.save_with_format(&path, save_format)
                        .map_err(|e| PuhuError::ImageError(e))
                        .map_err(|e| e.into())
                })
            })
        } else {
            Err(PuhuError::InvalidOperation(
                "Buffer saving not yet implemented".to_string()
            ).into())
        }
    }

    #[pyo3(signature = (size, resample=None))]
    fn resize(&mut self, size: (u32, u32), resample: Option<String>) -> PyResult<Self> {
        let (width, height) = size;
        let format = self.format;
        
        // Load image to check dimensions
        let image = self.get_image()?;
        
        // Early return if size is the same
        if image.width() == width && image.height() == height {
            return Ok(PyImage {
                lazy_image: LazyImage::Loaded(image.clone()),
                format,
            });
        }
        
        let filter = operations::parse_resample_filter(resample.as_deref())?;
        
        Ok(Python::with_gil(|py| {
            py.allow_threads(|| {
                let resized = image.resize(width, height, filter);
                PyImage {
                    lazy_image: LazyImage::Loaded(resized),
                    format,
                }
            })
        }))
    }

    fn crop(&mut self, box_coords: (u32, u32, u32, u32)) -> PyResult<Self> {
        let (x, y, width, height) = box_coords;
        let format = self.format;
        
        let image = self.get_image()?;
        
        // Validate crop bounds
        if x + width > image.width() || y + height > image.height() {
            return Err(PuhuError::InvalidOperation(
                format!("Crop coordinates ({}+{}, {}+{}) exceed image bounds ({}x{})", 
                       x, width, y, height, image.width(), image.height())
            ).into());
        }
        
        if width == 0 || height == 0 {
            return Err(PuhuError::InvalidOperation(
                "Crop dimensions must be greater than 0".to_string()
            ).into());
        }
        
        Ok(Python::with_gil(|py| {
            py.allow_threads(|| {
                let cropped = image.crop_imm(x, y, width, height);
                PyImage {
                    lazy_image: LazyImage::Loaded(cropped),
                    format,
                }
            })
        }))
    }

    fn rotate(&mut self, angle: f64) -> PyResult<Self> {
        let format = self.format;
        let image = self.get_image()?;
        
        Python::with_gil(|py| {
            py.allow_threads(|| {
                let rotated = if (angle - 90.0).abs() < f64::EPSILON {
                    image.rotate90()
                } else if (angle - 180.0).abs() < f64::EPSILON {
                    image.rotate180()
                } else if (angle - 270.0).abs() < f64::EPSILON {
                    image.rotate270()
                } else {
                    return Err(PuhuError::InvalidOperation(
                        "Only 90, 180, 270 degree rotations supported".to_string()
                    ).into());
                };
                Ok(PyImage {
                    lazy_image: LazyImage::Loaded(rotated),
                    format,
                })
            })
        })
    }

    fn transpose(&mut self, method: String) -> PyResult<Self> {
        let format = self.format;
        let image = self.get_image()?;
        
        Python::with_gil(|py| {
            py.allow_threads(|| {
                let transposed = match method.as_str() {
                    "FLIP_LEFT_RIGHT" => image.fliph(),
                    "FLIP_TOP_BOTTOM" => image.flipv(),
                    "ROTATE_90" => image.rotate90(),
                    "ROTATE_180" => image.rotate180(),
                    "ROTATE_270" => image.rotate270(),
                    _ => return Err(PuhuError::InvalidOperation(
                        format!("Unsupported transpose method: {}", method)
                    ).into()),
                };
                Ok(PyImage {
                    lazy_image: LazyImage::Loaded(transposed),
                    format,
                })
            })
        })
    }

    #[getter]
    fn size(&mut self) -> PyResult<(u32, u32)> {
        let img = self.get_image()?;
        Ok((img.width(), img.height()))
    }

    #[getter]
    fn width(&mut self) -> PyResult<u32> {
        let img = self.get_image()?;
        Ok(img.width())
    }

    #[getter]
    fn height(&mut self) -> PyResult<u32> {
        let img = self.get_image()?;
        Ok(img.height())
    }

    #[getter]
    fn mode(&mut self) -> PyResult<String> {
        let img = self.get_image()?;
        Ok(color_type_to_mode_string(img.color()))
    }

    #[getter]
    fn format(&self) -> Option<String> {
        self.format.map(|f| format!("{:?}", f).to_uppercase())
    }

    fn to_bytes(&mut self) -> PyResult<Py<PyBytes>> {
        let image = self.get_image()?;
        Python::with_gil(|py| {
            let bytes = py.allow_threads(|| {
                image.as_bytes().to_vec()
            });
            Ok(PyBytes::new_bound(py, &bytes).into())
        })
    }

    fn copy(&self) -> Self {
        PyImage {
            lazy_image: self.lazy_image.clone(),
            format: self.format,
        }
    }

    #[pyo3(signature = (mode, matrix=None, dither=None, palette=None, colors=None))]
    fn convert(
        &mut self,
        mode: &str,
        matrix: Option<Vec<f64>>,
        dither: Option<String>,
        palette: Option<String>,
        colors: Option<u32>,
    ) -> PyResult<Self> {
        let format = self.format;
        let image = self.get_image()?;
        
        // Validate matrix if provided
        if let Some(ref mat) = matrix {
            if mat.len() != 4 && mat.len() != 12 {
                return Err(PuhuError::InvalidOperation(
                    "Matrix must be a 4-tuple or 12-tuple of floats".to_string()
                ).into());
            }
        }
        
        let current_mode = color_type_to_mode_string(image.color());
        
        // Early return if converting to the same mode (and no matrix)
        if current_mode == mode && matrix.is_none() {
            return Ok(PyImage {
                lazy_image: LazyImage::Loaded(image.clone()),
                format,
            });
        }
        
        Python::with_gil(|py| {
            py.allow_threads(|| {
                let converted = if let Some(mat) = matrix {
                    conversions::convert_with_matrix(image, mode, &mat)?
                } else {
                    match mode {
                        "L" => DynamicImage::ImageLuma8(image.to_luma8()),
                        "LA" => DynamicImage::ImageLumaA8(image.to_luma_alpha8()),
                        "RGB" => DynamicImage::ImageRgb8(image.to_rgb8()),
                        "RGBA" => DynamicImage::ImageRgba8(image.to_rgba8()),
                        "1" => {
                            // bilevel
                            let apply_dither = match dither.as_deref() {
                                Some("NONE") | Some("none") => false,
                                Some("FLOYDSTEINBERG") | Some("floydsteinberg") => true,
                                None => true,
                                Some(other) => {
                                    return Err(PuhuError::InvalidOperation(
                                        format!("Unsupported dither method: '{}'. Use 'NONE' or 'FLOYDSTEINBERG'", other)
                                    ).into());
                                }
                            };
                            conversions::convert_to_bilevel(image, apply_dither)?
                        }
                        "P" => {
                            let palette_type = palette.as_deref().unwrap_or("WEB");
                            let num_colors = colors.unwrap_or(256);
                            let apply_dither = match dither.as_deref() {
                                Some("NONE") | Some("none") => false,
                                Some("FLOYDSTEINBERG") | Some("floydsteinberg") => true,
                                None => true,
                                Some(other) => {
                                    return Err(PuhuError::InvalidOperation(
                                        format!("Unsupported dither method: '{}'. Use 'NONE' or 'FLOYDSTEINBERG'", other)
                                    ).into());
                                }
                            };
                            palette::convert_to_palette(image, palette_type, num_colors, apply_dither)?
                        }
                        _ => {
                            return Err(PuhuError::InvalidOperation(
                                format!("Unsupported conversion mode: '{}'. Supported modes: L, LA, RGB, RGBA, 1, P", mode)
                            ).into());
                        }
                    }
                };
                
                Ok(PyImage {
                    lazy_image: LazyImage::Loaded(converted),
                    format,
                })
            })
        })
    }

    fn __repr__(&mut self) -> String {
        match self.get_image() {
            Ok(img) => {
                let (width, height) = (img.width(), img.height());
                let mode = color_type_to_mode_string(img.color());
                let format = self.format().unwrap_or_else(|| "Unknown".to_string());
                format!("<Image size={}x{} mode={} format={}>", width, height, mode, format)
            },
            Err(_) => "<Image [Error loading image]>".to_string(),
        }
    }
}
