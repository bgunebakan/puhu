use crate::conversions;
use crate::errors::PuhuError;
use crate::formats;
use crate::operations;
use crate::palette;
use crate::utils::{
    color_type_to_mode_string, convert_mode, fill_region, parse_color, paste_with_mask,
};
use image::{DynamicImage, ImageFormat};
use pyo3::prelude::*;
use pyo3::types::{PyBytes, PyType};
use std::io::Cursor;
use std::path::PathBuf;

#[derive(Clone)]
enum LazyImage {
    Loaded(DynamicImage),
    /// Image data stored as file path
    Path {
        path: PathBuf,
    },
    /// Image data stored as bytes
    Bytes {
        data: Vec<u8>,
    },
}

impl LazyImage {
    /// Ensure the image is loaded
    fn ensure_loaded(&mut self) -> Result<&DynamicImage, PuhuError> {
        match self {
            LazyImage::Loaded(img) => Ok(img),
            LazyImage::Path { path } => {
                let img = image::open(path).map_err(|e| PuhuError::ImageError(e))?;
                *self = LazyImage::Loaded(img);
                match self {
                    LazyImage::Loaded(img) => Ok(img),
                    _ => unreachable!("Just set to Loaded variant"),
                }
            }
            LazyImage::Bytes { data } => {
                let cursor = Cursor::new(data);
                let reader = image::io::Reader::new(cursor)
                    .with_guessed_format()
                    .map_err(|e| PuhuError::Io(e))?;
                let img = reader.decode().map_err(|e| PuhuError::ImageError(e))?;
                *self = LazyImage::Loaded(img);
                match self {
                    LazyImage::Loaded(img) => Ok(img),
                    _ => unreachable!("Just set to Loaded variant"),
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
            format: None,
        }
    }

    #[classmethod]
    #[pyo3(signature = (mode, size, color=None))]
    fn new(
        _cls: &Bound<'_, PyType>,
        mode: &str,
        size: (u32, u32),
        color: Option<&Bound<'_, PyAny>>,
    ) -> PyResult<Self> {
        let (width, height) = size;

        if width == 0 || height == 0 {
            return Err(PuhuError::InvalidOperation(
                "Image dimensions must be greater than 0".to_string(),
            )
            .into());
        }

        let parsed_color = if let Some(c) = color {
            parse_color(c)?
        } else {
            (0, 0, 0, 0)
        };
        let (r, g, b, a) = parsed_color;

        let image = match mode {
            "RGB" => DynamicImage::ImageRgb8(image::RgbImage::from_pixel(
                width,
                height,
                image::Rgb([r, g, b]),
            )),
            "RGBA" => DynamicImage::ImageRgba8(image::RgbaImage::from_pixel(
                width,
                height,
                image::Rgba([r, g, b, a]),
            )),
            "L" => {
                // If parsing returns full color but mode is L, we should probably just use one channel
                // But parse_color returns RGBA. For int/float it puts val in R,G,B.
                // So using R channel is safe for grayscale inputs.
                DynamicImage::ImageLuma8(image::GrayImage::from_pixel(
                    width,
                    height,
                    image::Luma([r]),
                ))
            }
            "LA" => DynamicImage::ImageLumaA8(image::GrayAlphaImage::from_pixel(
                width,
                height,
                image::LumaA([r, a]),
            )),
            _ => {
                return Err(PuhuError::InvalidOperation(format!(
                    "Unsupported image mode: {}",
                    mode
                ))
                .into());
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
                format,
            })
        } else if let Ok(bytes) = path_or_bytes.downcast::<PyBytes>() {
            // Store bytes for lazy loading
            let data = bytes.as_bytes().to_vec();
            // Try to guess format from bytes header
            let format = {
                let cursor = Cursor::new(&data);
                image::io::Reader::new(cursor)
                    .with_guessed_format()
                    .ok()
                    .and_then(|r| r.format())
            };
            Ok(PyImage {
                lazy_image: LazyImage::Bytes { data },
                format,
            })
        } else {
            Err(PuhuError::InvalidOperation("Expected file path (str) or bytes".to_string()).into())
        }
    }

    #[pyo3(signature = (path_or_buffer, format=None))]
    fn save(&mut self, path_or_buffer: &Bound<'_, PyAny>, format: Option<String>) -> PyResult<()> {
        if let Ok(path) = path_or_buffer.extract::<String>() {
            // Save to file path
            let save_format = if let Some(fmt) = format {
                formats::parse_format(&fmt)?
            } else {
                ImageFormat::from_path(&path).map_err(|_| {
                    PuhuError::UnsupportedFormat("Cannot determine format from path".to_string())
                })?
            };

            // Ensure image is loaded before saving
            let image = self.get_image()?;

            Python::with_gil(|py| {
                py.allow_threads(|| {
                    image
                        .save_with_format(&path, save_format)
                        .map_err(|e| PuhuError::ImageError(e))
                        .map_err(|e| e.into())
                })
            })
        } else {
            Err(PuhuError::InvalidOperation("Buffer saving not yet implemented".to_string()).into())
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
            return Err(PuhuError::InvalidOperation(format!(
                "Crop coordinates ({}+{}, {}+{}) exceed image bounds ({}x{})",
                x,
                width,
                y,
                height,
                image.width(),
                image.height()
            ))
            .into());
        }

        if width == 0 || height == 0 {
            return Err(PuhuError::InvalidOperation(
                "Crop dimensions must be greater than 0".to_string(),
            )
            .into());
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
                        "Only 90, 180, 270 degree rotations supported".to_string(),
                    )
                    .into());
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
                    _ => {
                        return Err(PuhuError::InvalidOperation(format!(
                            "Unsupported transpose method: {}",
                            method
                        ))
                        .into())
                    }
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
            let bytes = py.allow_threads(|| image.as_bytes().to_vec());
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
                    "Matrix must be a 4-tuple or 12-tuple of floats".to_string(),
                )
                .into());
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

    #[pyo3(signature = (im, box_coords=None, mask=None))]
    fn paste(
        &mut self,
        im: &Bound<'_, PyAny>,
        box_coords: Option<&Bound<'_, PyAny>>,
        mask: Option<&Bound<'_, PyAny>>,
    ) -> PyResult<()> {
        // Step 1: Handle abbreviated syntax - paste(im, mask) where box is actually mask
        let (actual_box, actual_mask): (Option<&Bound<'_, PyAny>>, Option<&Bound<'_, PyAny>>) =
            if let Some(box_val) = box_coords {
                if box_val.downcast::<PyImage>().is_ok() {
                    // Abbreviated syntax: paste(im, mask)
                    (None, Some(box_val))
                } else {
                    (Some(box_val), mask)
                }
            } else {
                (None, mask)
            };

        // Step 2: Parse source - can be Image or color tuple
        enum PasteSource {
            Image(DynamicImage),
            Color((u8, u8, u8, u8)),
        }

        let source = if let Ok(img_ref) = im.downcast::<PyImage>() {
            let mut img = img_ref.borrow_mut();
            PasteSource::Image(img.get_image()?.clone())
        } else if let Ok(color) = parse_color(im) {
            PasteSource::Color(color)
        } else {
            return Err(PuhuError::InvalidOperation(
                "im must be Image or valid color (tuple, string, int)".to_string(),
            )
            .into());
        };

        // Step 3: Get source dimensions
        let (src_width, src_height) = match &source {
            PasteSource::Image(img) => (img.width(), img.height()),
            PasteSource::Color(_) => {
                // Get dimensions from box or mask for color fill
                if let Some(mask_bound) = actual_mask {
                    let mask_ref = mask_bound.downcast::<PyImage>()?;
                    let mut mask_img = mask_ref.borrow_mut();
                    let mask_image = mask_img.get_image()?;
                    (mask_image.width(), mask_image.height())
                } else if let Some(box_val) = actual_box {
                    // Try to extract 4-tuple to get dimensions
                    if let Ok((left, top, right, bottom)) =
                        box_val.extract::<(i32, i32, i32, i32)>()
                    {
                        ((right - left) as u32, (bottom - top) as u32)
                    } else {
                        return Err(PuhuError::InvalidOperation(
                            "Cannot determine region size for color fill; use 4-item box"
                                .to_string(),
                        )
                        .into());
                    }
                } else {
                    return Err(PuhuError::InvalidOperation(
                        "Cannot determine region size for color fill; use 4-item box".to_string(),
                    )
                    .into());
                }
            }
        };

        // Step 4: Parse and expand box coordinates (supports negative for clipping)
        let box_4tuple: (i32, i32, i32, i32) = if let Some(box_val) = actual_box {
            if let Ok((x, y)) = box_val.extract::<(i32, i32)>() {
                // 2-tuple: expand to 4-tuple
                (x, y, x + src_width as i32, y + src_height as i32)
            } else if let Ok(coords) = box_val.extract::<(i32, i32, i32, i32)>() {
                coords
            } else {
                return Err(PuhuError::InvalidOperation(
                    "box must be 2-tuple (x, y) or 4-tuple (left, upper, right, lower)".to_string(),
                )
                .into());
            }
        } else {
            // None: default to (0, 0)
            (0, 0, src_width as i32, src_height as i32)
        };

        let (paste_x, paste_y, paste_right, paste_bottom) = box_4tuple;
        let paste_width = (paste_right - paste_x) as u32;
        let paste_height = (paste_bottom - paste_y) as u32;

        // Step 5: Get and prepare destination image
        let mut dest = self.get_image()?.clone();
        let dest_mode = color_type_to_mode_string(dest.color());

        // Step 6: Handle source based on type
        match source {
            PasteSource::Image(src_img) => {
                // Mode conversion if needed
                let src_mode = color_type_to_mode_string(src_img.color());
                let source_converted = if dest_mode != src_mode
                    && !(dest_mode == "RGB" && matches!(src_mode.as_str(), "RGBA" | "LA" | "RGBa"))
                {
                    // Convert source to destination mode
                    convert_mode(&src_img, &dest_mode)?
                } else {
                    src_img
                };

                // Paste with or without mask
                if let Some(mask_bound) = actual_mask {
                    let mask_ref = mask_bound.downcast::<PyImage>()?;
                    let mut mask_img_borrowed = mask_ref.borrow_mut();
                    let mask_img = mask_img_borrowed.get_image()?;

                    // Validate mask size
                    if mask_img.width() != source_converted.width()
                        || mask_img.height() != source_converted.height()
                    {
                        return Err(PuhuError::InvalidOperation(format!(
                            "Mask size ({}x{}) must match source size ({}x{})",
                            mask_img.width(),
                            mask_img.height(),
                            source_converted.width(),
                            source_converted.height()
                        ))
                        .into());
                    }

                    // Perform masked paste
                    paste_with_mask(&mut dest, &source_converted, paste_x, paste_y, mask_img)?;
                } else {
                    // Direct overlay using imageops
                    image::imageops::overlay(
                        &mut dest,
                        &source_converted,
                        paste_x as i64,
                        paste_y as i64,
                    );
                }
            }
            PasteSource::Color(color) => {
                // Fill region with solid color
                fill_region(
                    &mut dest,
                    paste_x,
                    paste_y,
                    paste_width,
                    paste_height,
                    color,
                )?;
            }
        }

        // Update the image
        self.lazy_image = LazyImage::Loaded(dest);
        Ok(())
    }

    fn __repr__(&mut self) -> String {
        match self.get_image() {
            Ok(img) => {
                let (width, height) = (img.width(), img.height());
                let mode = color_type_to_mode_string(img.color());
                let format = self.format().unwrap_or_else(|| "Unknown".to_string());
                format!(
                    "<Image size={}x{} mode={} format={}>",
                    width, height, mode, format
                )
            }
            Err(_) => "<Image [Error loading image]>".to_string(),
        }
    }
}
