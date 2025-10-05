use image::DynamicImage;
use image::imageops::colorops::{grayscale, dither, BiLevel};
use rayon::prelude::*;
use crate::errors::PuhuError;

pub fn convert_with_matrix(
    image: &DynamicImage,
    target_mode: &str,
    matrix: &[f64],
) -> Result<DynamicImage, PuhuError> {
    // 4-tuple: single channel transform (e.g., L → RGB)
    // 12-tuple: RGB → RGB color space transform
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

pub fn convert_to_bilevel(image: &DynamicImage, apply_dither: bool) -> Result<DynamicImage, PuhuError> {
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
