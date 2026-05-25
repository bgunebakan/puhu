use crate::errors::PuhuError;
use image::imageops::colorops::{dither, grayscale, BiLevel};
use image::{DynamicImage, GrayImage};
use rayon::prelude::*;

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
            let pixels: Vec<u8> = luma_img
                .par_iter()
                .flat_map(|&l| {
                    let l_f64 = l as f64;
                    [
                        (matrix[0] * l_f64).clamp(0.0, 255.0) as u8,
                        (matrix[1] * l_f64).clamp(0.0, 255.0) as u8,
                        (matrix[2] * l_f64).clamp(0.0, 255.0) as u8,
                    ]
                })
                .collect();

            let rgb_img = image::RgbImage::from_raw(width, height, pixels).ok_or_else(|| {
                PuhuError::InvalidOperation(
                    "Failed to create RGB image from converted pixels".to_string(),
                )
            })?;
            Ok(DynamicImage::ImageRgb8(rgb_img))
        }
        (12, "RGB") => {
            let rgb_img = image.to_rgb8();
            let (width, height) = rgb_img.dimensions();

            // Parallel processing of pixels
            let pixels: Vec<u8> = rgb_img
                .par_chunks(3)
                .flat_map(|pixel| {
                    let r = pixel[0] as f64;
                    let g = pixel[1] as f64;
                    let b = pixel[2] as f64;
                    [
                        (matrix[0] * r + matrix[1] * g + matrix[2] * b + matrix[3])
                            .clamp(0.0, 255.0) as u8,
                        (matrix[4] * r + matrix[5] * g + matrix[6] * b + matrix[7])
                            .clamp(0.0, 255.0) as u8,
                        (matrix[8] * r + matrix[9] * g + matrix[10] * b + matrix[11])
                            .clamp(0.0, 255.0) as u8,
                    ]
                })
                .collect();

            let result_img = image::RgbImage::from_raw(width, height, pixels).ok_or_else(|| {
                PuhuError::InvalidOperation(
                    "Failed to create RGB image from converted pixels".to_string(),
                )
            })?;
            Ok(DynamicImage::ImageRgb8(result_img))
        }
        (4, mode) => Err(PuhuError::InvalidOperation(format!(
            "4-tuple matrix conversion to mode '{}' not supported",
            mode
        ))),
        (12, mode) => Err(PuhuError::InvalidOperation(format!(
            "12-tuple matrix conversion to mode '{}' not supported",
            mode
        ))),
        (len, _) => Err(PuhuError::InvalidOperation(format!(
            "Matrix must be 4-tuple or 12-tuple, got {}-tuple",
            len
        ))),
    }
}

pub(crate) fn split_bands(
    image: &DynamicImage,
    width: u32,
    height: u32,
) -> Result<Vec<DynamicImage>, PuhuError> {
    let mismatch = || PuhuError::InvalidOperation("split: buffer size mismatch".to_string());
    let n = (width * height) as usize;

    match image {
        DynamicImage::ImageLuma8(img) => Ok(vec![DynamicImage::ImageLuma8(img.clone())]),
        DynamicImage::ImageLuma16(img) => Ok(vec![DynamicImage::ImageLuma16(img.clone())]),
        DynamicImage::ImageLumaA8(img) => {
            let raw = img.as_raw();
            // Single-pass: pre-allocated buffers + iter_mut proves non-aliasing to LLVM,
            // enabling paired SIMD loads and sequential stores.
            let (mut luma, mut alpha) = unsafe {
                let mut l = Vec::<u8>::with_capacity(n);
                let mut a = Vec::<u8>::with_capacity(n);
                l.set_len(n);
                a.set_len(n);
                (l, a)
            };
            raw.chunks_exact(2)
                .zip(luma.iter_mut().zip(alpha.iter_mut()))
                .for_each(|(p, (l, a))| {
                    *l = p[0];
                    *a = p[1];
                });
            Ok(vec![
                DynamicImage::ImageLuma8(
                    GrayImage::from_raw(width, height, luma).ok_or_else(mismatch)?,
                ),
                DynamicImage::ImageLuma8(
                    GrayImage::from_raw(width, height, alpha).ok_or_else(mismatch)?,
                ),
            ])
        }
        DynamicImage::ImageRgb8(img) => {
            let raw = img.as_raw();
            let (mut r, mut g, mut b) = unsafe {
                let mut r = Vec::<u8>::with_capacity(n);
                let mut g = Vec::<u8>::with_capacity(n);
                let mut b = Vec::<u8>::with_capacity(n);
                r.set_len(n);
                g.set_len(n);
                b.set_len(n);
                (r, g, b)
            };
            raw.chunks_exact(3)
                .zip(r.iter_mut().zip(g.iter_mut().zip(b.iter_mut())))
                .for_each(|(p, (rr, (gg, bb)))| {
                    *rr = p[0];
                    *gg = p[1];
                    *bb = p[2];
                });
            Ok(vec![
                DynamicImage::ImageLuma8(
                    GrayImage::from_raw(width, height, r).ok_or_else(mismatch)?,
                ),
                DynamicImage::ImageLuma8(
                    GrayImage::from_raw(width, height, g).ok_or_else(mismatch)?,
                ),
                DynamicImage::ImageLuma8(
                    GrayImage::from_raw(width, height, b).ok_or_else(mismatch)?,
                ),
            ])
        }
        DynamicImage::ImageRgba8(img) => {
            let raw = img.as_raw();
            let (mut r, mut g, mut b, mut a) = unsafe {
                let mut r = Vec::<u8>::with_capacity(n);
                let mut g = Vec::<u8>::with_capacity(n);
                let mut b = Vec::<u8>::with_capacity(n);
                let mut a = Vec::<u8>::with_capacity(n);
                r.set_len(n);
                g.set_len(n);
                b.set_len(n);
                a.set_len(n);
                (r, g, b, a)
            };
            raw.chunks_exact(4)
                .zip(
                    r.iter_mut()
                        .zip(g.iter_mut().zip(b.iter_mut().zip(a.iter_mut()))),
                )
                .for_each(|(p, (rr, (gg, (bb, aa))))| {
                    *rr = p[0];
                    *gg = p[1];
                    *bb = p[2];
                    *aa = p[3];
                });
            Ok(vec![
                DynamicImage::ImageLuma8(
                    GrayImage::from_raw(width, height, r).ok_or_else(mismatch)?,
                ),
                DynamicImage::ImageLuma8(
                    GrayImage::from_raw(width, height, g).ok_or_else(mismatch)?,
                ),
                DynamicImage::ImageLuma8(
                    GrayImage::from_raw(width, height, b).ok_or_else(mismatch)?,
                ),
                DynamicImage::ImageLuma8(
                    GrayImage::from_raw(width, height, a).ok_or_else(mismatch)?,
                ),
            ])
        }
        _ => {
            // Fallback: normalise to RGBA8 first (handles 16-bit multi-channel, float variants)
            let rgba = image.to_rgba8();
            let raw = rgba.as_raw();
            let (mut r, mut g, mut b, mut a) = unsafe {
                let mut r = Vec::<u8>::with_capacity(n);
                let mut g = Vec::<u8>::with_capacity(n);
                let mut b = Vec::<u8>::with_capacity(n);
                let mut a = Vec::<u8>::with_capacity(n);
                r.set_len(n);
                g.set_len(n);
                b.set_len(n);
                a.set_len(n);
                (r, g, b, a)
            };
            raw.chunks_exact(4)
                .zip(
                    r.iter_mut()
                        .zip(g.iter_mut().zip(b.iter_mut().zip(a.iter_mut()))),
                )
                .for_each(|(p, (rr, (gg, (bb, aa))))| {
                    *rr = p[0];
                    *gg = p[1];
                    *bb = p[2];
                    *aa = p[3];
                });
            Ok(vec![
                DynamicImage::ImageLuma8(
                    GrayImage::from_raw(width, height, r).ok_or_else(mismatch)?,
                ),
                DynamicImage::ImageLuma8(
                    GrayImage::from_raw(width, height, g).ok_or_else(mismatch)?,
                ),
                DynamicImage::ImageLuma8(
                    GrayImage::from_raw(width, height, b).ok_or_else(mismatch)?,
                ),
                DynamicImage::ImageLuma8(
                    GrayImage::from_raw(width, height, a).ok_or_else(mismatch)?,
                ),
            ])
        }
    }
}

pub fn convert_to_bilevel(
    image: &DynamicImage,
    apply_dither: bool,
) -> Result<DynamicImage, PuhuError> {
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
