use pyo3::prelude::*;
use pyo3::types::{PyBytes, PyType};
use image::{DynamicImage, ImageFormat, ColorType};
use image::imageops::colorops::{grayscale, dither, BiLevel};
use rayon::prelude::*;
use color_quant::NeuQuant;
use std::io::Cursor;
use std::path::PathBuf;
use crate::errors::PuhuError;
use crate::formats;
use crate::operations;

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

    fn convert_with_matrix(image: &DynamicImage, target_mode: &str, matrix: &[f64]) -> Result<DynamicImage, PuhuError> {
        // 4-tuple: single channel transform (e.g., L -> RGB)
        // 12-tuple: RGB -> RGB color space transform
        match (matrix.len(), target_mode) {
            (4, "RGB") => {
                let luma_img = image.to_luma8();
                let (width, height) = luma_img.dimensions();
                
                // Parallel processing of pixels
                let pixels: Vec<u8> = luma_img.par_iter()
                    .flat_map(|&l| {
                        let l_f64 = l as f64;
                        [
                            (matrix[0] * l_f64).clamp(0.0, 255.0) as u8,
                            (matrix[1] * l_f64).clamp(0.0, 255.0) as u8,
                            (matrix[2] * l_f64).clamp(0.0, 255.0) as u8,
                        ]
                    })
                    .collect();
                
                let rgb_img = image::RgbImage::from_raw(width, height, pixels)
                    .ok_or_else(|| PuhuError::InvalidOperation(
                        "Failed to create RGB image from converted pixels".to_string()
                    ))?;
                Ok(DynamicImage::ImageRgb8(rgb_img))
            }
            (12, "RGB") => {
                let rgb_img = image.to_rgb8();
                let (width, height) = rgb_img.dimensions();
                
                // Parallel processing of pixels
                let pixels: Vec<u8> = rgb_img.par_chunks(3)
                    .flat_map(|pixel| {
                        let r = pixel[0] as f64;
                        let g = pixel[1] as f64;
                        let b = pixel[2] as f64;
                        [
                            (matrix[0] * r + matrix[1] * g + matrix[2] * b + matrix[3]).clamp(0.0, 255.0) as u8,
                            (matrix[4] * r + matrix[5] * g + matrix[6] * b + matrix[7]).clamp(0.0, 255.0) as u8,
                            (matrix[8] * r + matrix[9] * g + matrix[10] * b + matrix[11]).clamp(0.0, 255.0) as u8,
                        ]
                    })
                    .collect();
                
                let result_img = image::RgbImage::from_raw(width, height, pixels)
                    .ok_or_else(|| PuhuError::InvalidOperation(
                        "Failed to create RGB image from converted pixels".to_string()
                    ))?;
                Ok(DynamicImage::ImageRgb8(result_img))
            }
            (4, mode) => Err(PuhuError::InvalidOperation(
                format!("4-tuple matrix conversion to mode '{}' not supported", mode)
            )),
            (12, mode) => Err(PuhuError::InvalidOperation(
                format!("12-tuple matrix conversion to mode '{}' not supported", mode)
            )),
            (len, _) => Err(PuhuError::InvalidOperation(
                format!("Matrix must be 4-tuple or 12-tuple, got {}-tuple", len)
            )),
        }
    }

    fn convert_to_bilevel(image: &DynamicImage, apply_dither: bool) -> Result<DynamicImage, PuhuError> {
        let mut luma = grayscale(image);
        if apply_dither {
            dither(&mut luma, &BiLevel);
        } else {
            for pixel in luma.pixels_mut() {
                pixel[0] = if pixel[0] > 127 { 255 } else { 0 };
            }
        }
        Ok(DynamicImage::ImageLuma8(luma))
    }

    fn generate_web_palette() -> Vec<u8> {
        let mut palette = Vec::with_capacity(216 * 3);
        // Web-safe colors: 6x6x6 cube (0, 51, 102, 153, 204, 255 for each channel)
        for r in 0..6 {
            for g in 0..6 {
                for b in 0..6 {
                    palette.push((r * 51) as u8);
                    palette.push((g * 51) as u8);
                    palette.push((b * 51) as u8);
                }
            }
        }
        palette
    }

    fn convert_to_palette(
        image: &DynamicImage,
        palette_type: &str,
        num_colors: u32,
        apply_dither: bool,
    ) -> Result<DynamicImage, PuhuError> {
        let rgb_img = image.to_rgb8();
        let (width, height) = rgb_img.dimensions();
        
        let palette = match palette_type {
            "WEB" => {
                Self::generate_web_palette()
            }
            "ADAPTIVE" => {
                // Use NeuQuant
                let colors = num_colors.clamp(2, 256) as usize;
                let rgba_data: Vec<u8> = rgb_img.pixels()
                    .flat_map(|p| [p[0], p[1], p[2], 255])
                    .collect();
                
                let nq = NeuQuant::new(10, colors, &rgba_data);
                nq.color_map_rgb()
            }
            _ => {
                return Err(PuhuError::InvalidOperation(
                    format!("Unsupported palette type: '{}'. Use 'WEB' or 'ADAPTIVE'", palette_type)
                ));
            }
        };

        let mut palette_indices = Vec::with_capacity((width * height) as usize);
        
        if apply_dither {
            let mut error_buffer = vec![vec![(0i16, 0i16, 0i16); width as usize]; 2];
            
            for y in 0..height {
                let curr_row = (y % 2) as usize;
                let next_row = ((y + 1) % 2) as usize;
                
                for x in 0..width as usize {
                    error_buffer[next_row][x] = (0, 0, 0);
                }
                
                for x in 0..width {
                    let pixel = rgb_img.get_pixel(x, y);
                    let (err_r, err_g, err_b) = error_buffer[curr_row][x as usize];
                    
                    let r = (pixel[0] as i16 + err_r).clamp(0, 255) as u8;
                    let g = (pixel[1] as i16 + err_g).clamp(0, 255) as u8;
                    let b = (pixel[2] as i16 + err_b).clamp(0, 255) as u8;
                    
                    let (idx, nearest) = Self::find_nearest_palette_color(&palette, r, g, b);
                    palette_indices.push(idx);
                    
                    let quant_err_r = r as i16 - nearest.0 as i16;
                    let quant_err_g = g as i16 - nearest.1 as i16;
                    let quant_err_b = b as i16 - nearest.2 as i16;
                    
                    // Distribute error to neighboring pixels (Floyd-Steinberg)
                    if x + 1 < width {
                        let e = &mut error_buffer[curr_row][(x + 1) as usize];
                        e.0 += quant_err_r * 7 / 16;
                        e.1 += quant_err_g * 7 / 16;
                        e.2 += quant_err_b * 7 / 16;
                    }
                    if y + 1 < height {
                        if x > 0 {
                            let e = &mut error_buffer[next_row][(x - 1) as usize];
                            e.0 += quant_err_r * 3 / 16;
                            e.1 += quant_err_g * 3 / 16;
                            e.2 += quant_err_b * 3 / 16;
                        }
                        let e = &mut error_buffer[next_row][x as usize];
                        e.0 += quant_err_r * 5 / 16;
                        e.1 += quant_err_g * 5 / 16;
                        e.2 += quant_err_b * 5 / 16;
                        
                        if x + 1 < width {
                            let e = &mut error_buffer[next_row][(x + 1) as usize];
                            e.0 += quant_err_r * 1 / 16;
                            e.1 += quant_err_g * 1 / 16;
                            e.2 += quant_err_b * 1 / 16;
                        }
                    }
                }
            }
        } else {
            // No dithering
            for pixel in rgb_img.pixels() {
                let (idx, _) = Self::find_nearest_palette_color(&palette, pixel[0], pixel[1], pixel[2]);
                palette_indices.push(idx);
            }
        }

        // Convert palette indices back to RGB for now
        let rgb_data: Vec<u8> = palette_indices.iter()
            .flat_map(|&idx| {
                let base = (idx as usize) * 3;
                [palette[base], palette[base + 1], palette[base + 2]]
            })
            .collect();

        let result_img = image::RgbImage::from_raw(width, height, rgb_data)
            .ok_or_else(|| PuhuError::InvalidOperation(
                "Failed to create palette image".to_string()
            ))?;

        Ok(DynamicImage::ImageRgb8(result_img))
    }

    fn find_nearest_palette_color(palette: &[u8], r: u8, g: u8, b: u8) -> (u8, (u8, u8, u8)) {
        let mut min_dist = u32::MAX;
        let mut best_idx = 0;
        let mut best_color = (0u8, 0u8, 0u8);

        for (i, chunk) in palette.chunks(3).enumerate() {
            let pr = chunk[0];
            let pg = chunk[1];
            let pb = chunk[2];
            
            // Euclidean distance in RGB space
            let dr = (r as i32 - pr as i32).abs() as u32;
            let dg = (g as i32 - pg as i32).abs() as u32;
            let db = (b as i32 - pb as i32).abs() as u32;
            let dist = dr * dr + dg * dg + db * db;

            if dist < min_dist {
                min_dist = dist;
                best_idx = i;
                best_color = (pr, pg, pb);
            }
        }

        (best_idx as u8, best_color)
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
                    Self::convert_with_matrix(image, mode, &mat)?
                } else {
                    match mode {
                        "L" => {
                            // grayscale
                            DynamicImage::ImageLuma8(image.to_luma8())
                        }
                        "LA" => {
                            // grayscale with alpha
                            DynamicImage::ImageLumaA8(image.to_luma_alpha8())
                        }
                        "RGB" => {
                            DynamicImage::ImageRgb8(image.to_rgb8())
                        }
                        "RGBA" => {
                            DynamicImage::ImageRgba8(image.to_rgba8())
                        }
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
                            
                            Self::convert_to_bilevel(image, apply_dither)?
                        }
                        "P" => {
                            // Palette mode with color quantization
                            let palette_type = palette.as_deref().unwrap_or("WEB");
                            let num_colors = colors.unwrap_or(256);
                            
                            // Determine if dithering should be applied
                            let apply_dither = match dither.as_deref() {
                                Some("NONE") | Some("none") => false,
                                Some("FLOYDSTEINBERG") | Some("floydsteinberg") => true,
                                None => true, // Default to Floyd-Steinberg for palette conversion
                                Some(other) => {
                                    return Err(PuhuError::InvalidOperation(
                                        format!("Unsupported dither method: '{}'. Use 'NONE' or 'FLOYDSTEINBERG'", other)
                                    ).into());
                                }
                            };
                            
                            Self::convert_to_palette(image, palette_type, num_colors, apply_dither)?
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
