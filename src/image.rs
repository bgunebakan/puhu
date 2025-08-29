use pyo3::prelude::*;
use pyo3::types::{PyBytes, PyType};
use image::{DynamicImage, ImageFormat, ColorType, Rgba, Rgb};
use std::io::Cursor;
use std::path::PathBuf;
use crate::blending::{self, BlendMode, GradientDirection};
use crate::css_filters;
use crate::drawing;
use crate::errors::PuhuError;
use crate::filters;
use crate::formats;
use crate::operations;
use crate::pixels;
use crate::shadows;
use numpy::{PyArray2, PyArray3, PyArrayMethods, PyUntypedArrayMethods};

/// Convert ColorType to PIL-compatible mode string
fn color_type_to_mode_string(color_type: ColorType) -> String {
    match color_type {
        ColorType::L8 => "L".to_string(),
        ColorType::La8 => "LA".to_string(),
        ColorType::Rgb8 => "RGB".to_string(),
        ColorType::Rgba8 => "RGBA".to_string(),
        ColorType::L16 => "I".to_string(),
        ColorType::La16 => "LA".to_string(),
        ColorType::Rgb16 => "RGB".to_string(),
        ColorType::Rgba16 => "RGBA".to_string(),
        ColorType::Rgb32F => "RGB".to_string(),
        ColorType::Rgba32F => "RGBA".to_string(),
        _ => "RGB".to_string(), // Default fallback
    }
}

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
                let reader = image::ImageReader::new(cursor).with_guessed_format()
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

#[derive(Clone)]
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

    #[staticmethod]
    #[pyo3(signature = (mode, size, color=None))]
    fn new(mode: &str, size: (u32, u32), color: Option<(u8, u8, u8, u8)>) -> PyResult<Self> {
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

    #[staticmethod]
    fn open(path_or_bytes: &Bound<'_, PyAny>) -> PyResult<Self> {
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
                image::ImageReader::new(cursor).with_guessed_format()
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

    #[staticmethod]
    #[pyo3(signature = (array, _mode=None))]
    fn fromarray(array: &Bound<'_, PyAny>, _mode: Option<&str>) -> PyResult<Self> {
        // Try to handle 2D array (grayscale)
        if let Ok(array_2d) = array.downcast::<PyArray2<u8>>() {
            let readonly = array_2d.readonly();
            let shape = readonly.shape();
            let height = shape[0] as u32;
            let width = shape[1] as u32;

            let data: Vec<u8> = readonly.as_slice()?.to_vec();

            let image = image::GrayImage::from_raw(width, height, data)
                .ok_or_else(|| PuhuError::InvalidOperation(
                    "Failed to create image from array data".to_string()
                ))?;

            return Ok(PyImage {
                lazy_image: LazyImage::Loaded(DynamicImage::ImageLuma8(image)),
                format: None,
            });
        }

        // Try to handle 3D array (RGB/RGBA)
        if let Ok(array_3d) = array.downcast::<PyArray3<u8>>() {
            let readonly = array_3d.readonly();
            let shape = readonly.shape();
            let height = shape[0] as u32;
            let width = shape[1] as u32;
            let channels = shape[2];

            let data = readonly.as_slice()?;

            match channels {
                3 => {
                    // RGB image
                    let mut rgb_data = Vec::with_capacity((width * height * 3) as usize);
                    for i in 0..(width * height) as usize {
                        rgb_data.push(data[i * 3]);     // R
                        rgb_data.push(data[i * 3 + 1]); // G
                        rgb_data.push(data[i * 3 + 2]); // B
                    }

                    let image = image::RgbImage::from_raw(width, height, rgb_data)
                        .ok_or_else(|| PuhuError::InvalidOperation(
                            "Failed to create RGB image from array data".to_string()
                        ))?;

                    Ok(PyImage {
                        lazy_image: LazyImage::Loaded(DynamicImage::ImageRgb8(image)),
                        format: None,
                    })
                }
                4 => {
                    // RGBA image
                    let mut rgba_data = Vec::with_capacity((width * height * 4) as usize);
                    for i in 0..(width * height) as usize {
                        rgba_data.push(data[i * 4]);     // R
                        rgba_data.push(data[i * 4 + 1]); // G
                        rgba_data.push(data[i * 4 + 2]); // B
                        rgba_data.push(data[i * 4 + 3]); // A
                    }

                    let image = image::RgbaImage::from_raw(width, height, rgba_data)
                        .ok_or_else(|| PuhuError::InvalidOperation(
                            "Failed to create RGBA image from array data".to_string()
                        ))?;

                    Ok(PyImage {
                        lazy_image: LazyImage::Loaded(DynamicImage::ImageRgba8(image)),
                        format: None,
                    })
                }
                _ => Err(PuhuError::InvalidOperation(
                    format!("Unsupported number of channels: {}. Expected 3 (RGB) or 4 (RGBA)", channels)
                ).into())
            }
        } else {
            Err(PuhuError::InvalidOperation(
                "Expected numpy array with shape (H, W) for grayscale or (H, W, C) for RGB/RGBA".to_string()
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

    fn convert(&mut self, mode: &str) -> PyResult<Self> {
        let format = self.format;
        let image = self.get_image()?;

        // If already in target mode, return a copy
        let current_mode = color_type_to_mode_string(image.color());
        if current_mode == mode {
            return Ok(PyImage {
                lazy_image: LazyImage::Loaded(image.clone()),
                format,
            });
        }

        let converted = Python::with_gil(|py| {
            py.allow_threads(|| {
                match mode {
                    "L" => {
                        // Convert to grayscale
                        Ok(DynamicImage::ImageLuma8(image.to_luma8()))
                    }
                    "LA" => {
                        // Convert to grayscale with alpha
                        Ok(DynamicImage::ImageLumaA8(image.to_luma_alpha8()))
                    }
                    "RGB" => {
                        // Convert to RGB
                        Ok(DynamicImage::ImageRgb8(image.to_rgb8()))
                    }
                    "RGBA" => {
                        // Convert to RGBA
                        Ok(DynamicImage::ImageRgba8(image.to_rgba8()))
                    }
                    _ => Err(PuhuError::InvalidOperation(
                        format!("Unsupported conversion mode: {}", mode)
                    )),
                }
            })
        })?;

        Ok(PyImage {
            lazy_image: LazyImage::Loaded(converted),
            format,
        })
    }

    fn split(&mut self) -> PyResult<Vec<Self>> {
        let format = self.format;
        let image = self.get_image()?;

        let result = Python::with_gil(|py| {
            py.allow_threads(|| {
                match image {
                    DynamicImage::ImageRgb8(rgb_img) => {
                        let (width, height) = rgb_img.dimensions();
                        let mut channels = Vec::new();

                        // Extract R, G, B channels
                        for channel_idx in 0..3 {
                            let mut channel_data = Vec::with_capacity((width * height) as usize);
                            for pixel in rgb_img.pixels() {
                                channel_data.push(pixel.0[channel_idx]);
                            }

                            let channel_img = image::GrayImage::from_raw(width, height, channel_data)
                                .ok_or_else(|| PuhuError::InvalidOperation(
                                    "Failed to create channel image".to_string()
                                ))?;

                            channels.push(PyImage {
                                lazy_image: LazyImage::Loaded(DynamicImage::ImageLuma8(channel_img)),
                                format,
                            });
                        }

                        Ok(channels)
                    }
                    DynamicImage::ImageRgba8(rgba_img) => {
                        let (width, height) = rgba_img.dimensions();
                        let mut channels = Vec::new();

                        // Extract R, G, B, A channels
                        for channel_idx in 0..4 {
                            let mut channel_data = Vec::with_capacity((width * height) as usize);
                            for pixel in rgba_img.pixels() {
                                channel_data.push(pixel.0[channel_idx]);
                            }

                            let channel_img = image::GrayImage::from_raw(width, height, channel_data)
                                .ok_or_else(|| PuhuError::InvalidOperation(
                                    "Failed to create channel image".to_string()
                                ))?;

                            channels.push(PyImage {
                                lazy_image: LazyImage::Loaded(DynamicImage::ImageLuma8(channel_img)),
                                format,
                            });
                        }

                        Ok(channels)
                    }
                    DynamicImage::ImageLuma8(_) => {
                        // Grayscale image - return single channel
                        Ok(vec![PyImage {
                            lazy_image: LazyImage::Loaded(image.clone()),
                            format,
                        }])
                    }
                    DynamicImage::ImageLumaA8(la_img) => {
                        let (width, height) = la_img.dimensions();
                        let mut channels = Vec::new();

                        // Extract L, A channels
                        for channel_idx in 0..2 {
                            let mut channel_data = Vec::with_capacity((width * height) as usize);
                            for pixel in la_img.pixels() {
                                channel_data.push(pixel.0[channel_idx]);
                            }

                            let channel_img = image::GrayImage::from_raw(width, height, channel_data)
                                .ok_or_else(|| PuhuError::InvalidOperation(
                                    "Failed to create channel image".to_string()
                                ))?;

                            channels.push(PyImage {
                                lazy_image: LazyImage::Loaded(DynamicImage::ImageLuma8(channel_img)),
                                format,
                            });
                        }

                        Ok(channels)
                    }
                    _ => Err(PuhuError::InvalidOperation(
                        "Unsupported image format for channel splitting".to_string()
                    )),
                }
            })
        });
        result.map_err(|e| e.into())
    }

    #[pyo3(signature = (other, position=None, mask=None))]
    fn paste(&mut self, other: &mut Self, position: Option<(i32, i32)>, mask: Option<Self>) -> PyResult<Self> {
        let format = self.format;
        let base_image = self.get_image()?;
        let paste_image = other.get_image()?;

        let (paste_x, paste_y) = position.unwrap_or((0, 0));

        // Get mask image if provided
        let mask_image = if let Some(mut mask_img) = mask {
            Some(mask_img.get_image()?.clone())
        } else {
            None
        };

        Python::with_gil(|py| {
            py.allow_threads(|| {
                // Create a mutable copy of the base image
                let mut result = base_image.clone();

                match (&mut result, paste_image) {
                    (DynamicImage::ImageRgb8(base), DynamicImage::ImageRgb8(paste)) => {
                        let (base_width, base_height) = base.dimensions();
                        let (paste_width, paste_height) = paste.dimensions();

                        for y in 0..paste_height {
                            for x in 0..paste_width {
                                let target_x = paste_x + x as i32;
                                let target_y = paste_y + y as i32;

                                // Check bounds
                                if target_x >= 0 && target_y >= 0
                                    && (target_x as u32) < base_width
                                    && (target_y as u32) < base_height {

                                    let pixel = paste.get_pixel(x, y);

                                    // Apply mask if provided
                                    if let Some(ref mask) = mask_image {
                                        if let DynamicImage::ImageLuma8(mask_gray) = mask {
                                            let mask_pixel = mask_gray.get_pixel(x, y);
                                            let alpha = mask_pixel.0[0] as f32 / 255.0;

                                            if alpha > 0.0 {
                                                let base_pixel = base.get_pixel(target_x as u32, target_y as u32);
                                                let blended = Rgb([
                                                    ((1.0 - alpha) * base_pixel.0[0] as f32 + alpha * pixel.0[0] as f32) as u8,
                                                    ((1.0 - alpha) * base_pixel.0[1] as f32 + alpha * pixel.0[1] as f32) as u8,
                                                    ((1.0 - alpha) * base_pixel.0[2] as f32 + alpha * pixel.0[2] as f32) as u8,
                                                ]);
                                                base.put_pixel(target_x as u32, target_y as u32, blended);
                                            }
                                        }
                                    } else {
                                        base.put_pixel(target_x as u32, target_y as u32, *pixel);
                                    }
                                }
                            }
                        }
                    }
                    (DynamicImage::ImageRgba8(base), DynamicImage::ImageRgba8(paste)) => {
                        let (base_width, base_height) = base.dimensions();
                        let (paste_width, paste_height) = paste.dimensions();

                        for y in 0..paste_height {
                            for x in 0..paste_width {
                                let target_x = paste_x + x as i32;
                                let target_y = paste_y + y as i32;

                                // Check bounds
                                if target_x >= 0 && target_y >= 0
                                    && (target_x as u32) < base_width
                                    && (target_y as u32) < base_height {

                                    let pixel = paste.get_pixel(x, y);
                                    let alpha = pixel.0[3] as f32 / 255.0;

                                    if alpha > 0.0 {
                                        let base_pixel = base.get_pixel(target_x as u32, target_y as u32);
                                        let blended = Rgba([
                                            ((1.0 - alpha) * base_pixel.0[0] as f32 + alpha * pixel.0[0] as f32) as u8,
                                            ((1.0 - alpha) * base_pixel.0[1] as f32 + alpha * pixel.0[1] as f32) as u8,
                                            ((1.0 - alpha) * base_pixel.0[2] as f32 + alpha * pixel.0[2] as f32) as u8,
                                            255, // Keep base alpha
                                        ]);
                                        base.put_pixel(target_x as u32, target_y as u32, blended);
                                    }
                                }
                            }
                        }
                    }
                    // Convert images to compatible formats if needed
                    _ => {
                        let base_rgba = result.to_rgba8();
                        let paste_rgba = paste_image.to_rgba8();
                        let mut result_rgba = base_rgba;

                        let (base_width, base_height) = result_rgba.dimensions();
                        let (paste_width, paste_height) = paste_rgba.dimensions();

                        for y in 0..paste_height {
                            for x in 0..paste_width {
                                let target_x = paste_x + x as i32;
                                let target_y = paste_y + y as i32;

                                // Check bounds
                                if target_x >= 0 && target_y >= 0
                                    && (target_x as u32) < base_width
                                    && (target_y as u32) < base_height {

                                    let pixel = paste_rgba.get_pixel(x, y);
                                    let alpha = pixel.0[3] as f32 / 255.0;

                                    if alpha > 0.0 {
                                        let base_pixel = result_rgba.get_pixel(target_x as u32, target_y as u32);
                                        let blended = Rgba([
                                            ((1.0 - alpha) * base_pixel.0[0] as f32 + alpha * pixel.0[0] as f32) as u8,
                                            ((1.0 - alpha) * base_pixel.0[1] as f32 + alpha * pixel.0[1] as f32) as u8,
                                            ((1.0 - alpha) * base_pixel.0[2] as f32 + alpha * pixel.0[2] as f32) as u8,
                                            base_pixel.0[3], // Keep base alpha
                                        ]);
                                        result_rgba.put_pixel(target_x as u32, target_y as u32, blended);
                                    }
                                }
                            }
                        }

                        result = DynamicImage::ImageRgba8(result_rgba);
                    }
                }

                Ok(PyImage {
                    lazy_image: LazyImage::Loaded(result),
                    format,
                })
            })
        })
    }

    fn blur(&mut self, radius: f32) -> PyResult<Self> {
        let format = self.format;
        let image = self.get_image()?;

        Python::with_gil(|py| {
            py.allow_threads(|| {
                filters::blur(image, radius)
            })
        }).map(|filtered| PyImage {
            lazy_image: LazyImage::Loaded(filtered),
            format,
        }).map_err(|e| e.into())
    }

    fn sharpen(&mut self, strength: f32) -> PyResult<Self> {
        let format = self.format;
        let image = self.get_image()?;

        Python::with_gil(|py| {
            py.allow_threads(|| {
                filters::sharpen(image, strength)
            })
        }).map(|filtered| PyImage {
            lazy_image: LazyImage::Loaded(filtered),
            format,
        }).map_err(|e| e.into())
    }

    fn edge_detect(&mut self) -> PyResult<Self> {
        let format = self.format;
        let image = self.get_image()?;

        Python::with_gil(|py| {
            py.allow_threads(|| {
                filters::edge_detect(image)
            })
        }).map(|filtered| PyImage {
            lazy_image: LazyImage::Loaded(filtered),
            format,
        }).map_err(|e| e.into())
    }

    fn emboss(&mut self) -> PyResult<Self> {
        let format = self.format;
        let image = self.get_image()?;

        Python::with_gil(|py| {
            py.allow_threads(|| {
                filters::emboss(image)
            })
        }).map(|filtered| PyImage {
            lazy_image: LazyImage::Loaded(filtered),
            format,
        }).map_err(|e| e.into())
    }

    fn brightness(&mut self, adjustment: i16) -> PyResult<Self> {
        let format = self.format;
        let image = self.get_image()?;

        Python::with_gil(|py| {
            py.allow_threads(|| {
                filters::brightness(image, adjustment)
            })
        }).map(|filtered| PyImage {
            lazy_image: LazyImage::Loaded(filtered),
            format,
        }).map_err(|e| e.into())
    }

    fn contrast(&mut self, factor: f32) -> PyResult<Self> {
        let format = self.format;
        let image = self.get_image()?;

        Python::with_gil(|py| {
            py.allow_threads(|| {
                filters::contrast(image, factor)
            })
        }).map(|filtered| PyImage {
            lazy_image: LazyImage::Loaded(filtered),
            format,
        }).map_err(|e| e.into())
    }

    // CSS-like filters
    fn sepia(&mut self, amount: f32) -> PyResult<Self> {
        let format = self.format;
        let image = self.get_image()?;

        Python::with_gil(|py| {
            py.allow_threads(|| {
                css_filters::sepia(image, amount)
            })
        }).map(|filtered| PyImage {
            lazy_image: LazyImage::Loaded(filtered),
            format,
        }).map_err(|e| e.into())
    }

    fn grayscale_filter(&mut self, amount: f32) -> PyResult<Self> {
        let format = self.format;
        let image = self.get_image()?;

        Python::with_gil(|py| {
            py.allow_threads(|| {
                css_filters::grayscale(image, amount)
            })
        }).map(|filtered| PyImage {
            lazy_image: LazyImage::Loaded(filtered),
            format,
        }).map_err(|e| e.into())
    }

    fn invert(&mut self, amount: f32) -> PyResult<Self> {
        let format = self.format;
        let image = self.get_image()?;

        Python::with_gil(|py| {
            py.allow_threads(|| {
                css_filters::invert(image, amount)
            })
        }).map(|filtered| PyImage {
            lazy_image: LazyImage::Loaded(filtered),
            format,
        }).map_err(|e| e.into())
    }

    fn hue_rotate(&mut self, degrees: f32) -> PyResult<Self> {
        let format = self.format;
        let image = self.get_image()?;

        Python::with_gil(|py| {
            py.allow_threads(|| {
                css_filters::hue_rotate(image, degrees)
            })
        }).map(|filtered| PyImage {
            lazy_image: LazyImage::Loaded(filtered),
            format,
        }).map_err(|e| e.into())
    }

    fn saturate(&mut self, amount: f32) -> PyResult<Self> {
        let format = self.format;
        let image = self.get_image()?;

        Python::with_gil(|py| {
            py.allow_threads(|| {
                css_filters::saturate(image, amount)
            })
        }).map(|filtered| PyImage {
            lazy_image: LazyImage::Loaded(filtered),
            format,
        }).map_err(|e| e.into())
    }

    // Pixel manipulation methods
    fn getpixel(&mut self, x: u32, y: u32) -> PyResult<(u8, u8, u8, u8)> {
        let image = self.get_image()?;

        Python::with_gil(|py| {
            py.allow_threads(|| {
                pixels::get_pixel(image, x, y)
            })
        }).map_err(|e| e.into())
    }

    fn putpixel(&mut self, x: u32, y: u32, color: (u8, u8, u8, u8)) -> PyResult<Self> {
        let format = self.format;
        let image = self.get_image()?;

        Python::with_gil(|py| {
            py.allow_threads(|| {
                pixels::put_pixel(image, x, y, color)
            })
        }).map(|result| PyImage {
            lazy_image: LazyImage::Loaded(result),
            format,
        }).map_err(|e| e.into())
    }

    fn histogram(&mut self) -> PyResult<(Vec<u32>, Vec<u32>, Vec<u32>, Vec<u32>)> {
        let image = self.get_image()?;

        Python::with_gil(|py| {
            py.allow_threads(|| {
                pixels::histogram(image)
            })
        }).map(|(r, g, b, a)| (r.to_vec(), g.to_vec(), b.to_vec(), a.to_vec()))
        .map_err(|e| e.into())
    }

    fn dominant_color(&mut self) -> PyResult<(u8, u8, u8, u8)> {
        let image = self.get_image()?;

        Python::with_gil(|py| {
            py.allow_threads(|| {
                pixels::dominant_color(image)
            })
        }).map_err(|e| e.into())
    }

    fn average_color(&mut self) -> PyResult<(u8, u8, u8, u8)> {
        let image = self.get_image()?;

        Python::with_gil(|py| {
            py.allow_threads(|| {
                pixels::average_color(image)
            })
        }).map_err(|e| e.into())
    }

    fn replace_color(&mut self, target_color: (u8, u8, u8, u8), replacement_color: (u8, u8, u8, u8), tolerance: u8) -> PyResult<Self> {
        let format = self.format;
        let image = self.get_image()?;

        Python::with_gil(|py| {
            py.allow_threads(|| {
                pixels::replace_color(image, target_color, replacement_color, tolerance)
            })
        }).map(|result| PyImage {
            lazy_image: LazyImage::Loaded(result),
            format,
        }).map_err(|e| e.into())
    }

    fn threshold(&mut self, threshold_value: u8) -> PyResult<Self> {
        let format = self.format;
        let image = self.get_image()?;

        Python::with_gil(|py| {
            py.allow_threads(|| {
                pixels::threshold(image, threshold_value)
            })
        }).map(|result| PyImage {
            lazy_image: LazyImage::Loaded(result),
            format,
        }).map_err(|e| e.into())
    }

    fn posterize(&mut self, levels: u8) -> PyResult<Self> {
        let format = self.format;
        let image = self.get_image()?;

        Python::with_gil(|py| {
            py.allow_threads(|| {
                pixels::posterize(image, levels)
            })
        }).map(|result| PyImage {
            lazy_image: LazyImage::Loaded(result),
            format,
        }).map_err(|e| e.into())
    }

    // Drawing methods
    fn draw_rectangle(&mut self, x: i32, y: i32, width: u32, height: u32, color: (u8, u8, u8, u8)) -> PyResult<Self> {
        let format = self.format;
        let image = self.get_image()?;

        Python::with_gil(|py| {
            py.allow_threads(|| {
                drawing::draw_rectangle(image, x, y, width, height, color)
            })
        }).map(|result| PyImage {
            lazy_image: LazyImage::Loaded(result),
            format,
        }).map_err(|e| e.into())
    }

    fn draw_circle(&mut self, center_x: i32, center_y: i32, radius: u32, color: (u8, u8, u8, u8)) -> PyResult<Self> {
        let format = self.format;
        let image = self.get_image()?;

        Python::with_gil(|py| {
            py.allow_threads(|| {
                drawing::draw_circle(image, center_x, center_y, radius, color)
            })
        }).map(|result| PyImage {
            lazy_image: LazyImage::Loaded(result),
            format,
        }).map_err(|e| e.into())
    }

    fn draw_line(&mut self, x0: i32, y0: i32, x1: i32, y1: i32, color: (u8, u8, u8, u8)) -> PyResult<Self> {
        let format = self.format;
        let image = self.get_image()?;

        Python::with_gil(|py| {
            py.allow_threads(|| {
                drawing::draw_line(image, x0, y0, x1, y1, color)
            })
        }).map(|result| PyImage {
            lazy_image: LazyImage::Loaded(result),
            format,
        }).map_err(|e| e.into())
    }

    fn draw_text(&mut self, text: &str, x: i32, y: i32, color: (u8, u8, u8, u8), scale: u32) -> PyResult<Self> {
        let format = self.format;
        let image = self.get_image()?;

        Python::with_gil(|py| {
            py.allow_threads(|| {
                drawing::draw_text(image, text, x, y, color, scale)
            })
        }).map(|result| PyImage {
            lazy_image: LazyImage::Loaded(result),
            format,
        }).map_err(|e| e.into())
    }

    // Shadow effects
    fn drop_shadow(&mut self, offset_x: i32, offset_y: i32, blur_radius: f32, shadow_color: (u8, u8, u8, u8)) -> PyResult<Self> {
        let format = self.format;
        let image = self.get_image()?;

        Python::with_gil(|py| {
            py.allow_threads(|| {
                shadows::drop_shadow(image, offset_x, offset_y, blur_radius, shadow_color)
            })
        }).map(|result| PyImage {
            lazy_image: LazyImage::Loaded(result),
            format,
        }).map_err(|e| e.into())
    }

    fn inner_shadow(&mut self, offset_x: i32, offset_y: i32, blur_radius: f32, shadow_color: (u8, u8, u8, u8)) -> PyResult<Self> {
        let format = self.format;
        let image = self.get_image()?;

        Python::with_gil(|py| {
            py.allow_threads(|| {
                shadows::inner_shadow(image, offset_x, offset_y, blur_radius, shadow_color)
            })
        }).map(|result| PyImage {
            lazy_image: LazyImage::Loaded(result),
            format,
        }).map_err(|e| e.into())
    }

    fn glow(&mut self, blur_radius: f32, glow_color: (u8, u8, u8, u8), intensity: f32) -> PyResult<Self> {
        let format = self.format;
        let image = self.get_image()?;

        Python::with_gil(|py| {
            py.allow_threads(|| {
                shadows::glow(image, blur_radius, glow_color, intensity)
            })
        }).map(|result| PyImage {
            lazy_image: LazyImage::Loaded(result),
            format,
        }).map_err(|e| e.into())
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
