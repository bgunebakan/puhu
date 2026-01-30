use crate::errors::PuhuError;
use image::{ColorType, DynamicImage, GenericImage, GenericImageView};
use pyo3::prelude::*;

pub fn color_type_to_mode_string(color_type: ColorType) -> String {
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

pub fn parse_color(input: &Bound<'_, PyAny>) -> PyResult<(u8, u8, u8, u8)> {
    if let Ok(s) = input.extract::<String>() {
        let c = csscolorparser::parse(&s)
            .map_err(|e| PuhuError::InvalidOperation(format!("Invalid color string: {}", e)))?;
        let rgba = c.to_rgba8();
        Ok((rgba[0], rgba[1], rgba[2], rgba[3]))
    } else if let Ok(val) = input.extract::<u8>() {
        // Single integer -> grayscale (opaque)
        Ok((val, val, val, 255))
    } else if let Ok(tuple) = input.extract::<(u8, u8, u8)>() {
        // RGB tuple -> opaque
        Ok((tuple.0, tuple.1, tuple.2, 255))
    } else if let Ok(tuple) = input.extract::<(u8, u8, u8, u8)>() {
        // RGBA tuple
        Ok(tuple)
    } else {
        Err(PuhuError::InvalidOperation(
            "Color must be a string, integer, or tuple (RGB/RGBA)".to_string(),
        )
        .into())
    }
}

/// Paste source image onto destination with mask-based alpha blending
pub fn paste_with_mask(
    dest: &mut DynamicImage,
    src: &DynamicImage,
    x: u32,
    y: u32,
    mask: &DynamicImage,
) -> Result<(), PuhuError> {
    // Convert mask to grayscale if needed
    let mask_gray = mask.to_luma8();

    for src_y in 0..src.height() {
        for src_x in 0..src.width() {
            let dest_x = x + src_x;
            let dest_y = y + src_y;

            // Skip if out of bounds
            if dest_x >= dest.width() || dest_y >= dest.height() {
                continue;
            }

            let mask_val = mask_gray.get_pixel(src_x, src_y)[0];
            let alpha = mask_val as f32 / 255.0;

            // Get source and destination pixels
            let src_pixel = src.get_pixel(src_x, src_y);
            let dest_pixel = dest.get_pixel(dest_x, dest_y);

            // Blend: out = src * alpha + dest * (1 - alpha)
            let blended = image::Rgba([
                (src_pixel[0] as f32 * alpha + dest_pixel[0] as f32 * (1.0 - alpha)) as u8,
                (src_pixel[1] as f32 * alpha + dest_pixel[1] as f32 * (1.0 - alpha)) as u8,
                (src_pixel[2] as f32 * alpha + dest_pixel[2] as f32 * (1.0 - alpha)) as u8,
                if src_pixel.0.len() > 3 && dest_pixel.0.len() > 3 {
                    (src_pixel[3] as f32 * alpha + dest_pixel[3] as f32 * (1.0 - alpha)) as u8
                } else {
                    255
                },
            ]);

            dest.put_pixel(dest_x, dest_y, blended);
        }
    }

    Ok(())
}

/// Fill a region with a solid color
pub fn fill_region(
    dest: &mut DynamicImage,
    x: u32,
    y: u32,
    width: u32,
    height: u32,
    color: (u8, u8, u8, u8),
) -> Result<(), PuhuError> {
    let (r, g, b, a) = color;
    let pixel = image::Rgba([r, g, b, a]);

    for dy in 0..height {
        for dx in 0..width {
            let dest_x = x + dx;
            let dest_y = y + dy;

            // Skip if out of bounds
            if dest_x >= dest.width() || dest_y >= dest.height() {
                continue;
            }

            dest.put_pixel(dest_x, dest_y, pixel);
        }
    }

    Ok(())
}

/// Convert image to a different mode
pub fn convert_mode(image: &DynamicImage, target_mode: &str) -> Result<DynamicImage, PuhuError> {
    match target_mode {
        "L" => Ok(DynamicImage::ImageLuma8(image.to_luma8())),
        "LA" => Ok(DynamicImage::ImageLumaA8(image.to_luma_alpha8())),
        "RGB" => Ok(DynamicImage::ImageRgb8(image.to_rgb8())),
        "RGBA" => Ok(DynamicImage::ImageRgba8(image.to_rgba8())),
        _ => Err(PuhuError::InvalidOperation(format!(
            "Unsupported conversion mode: '{}'. Supported modes: L, LA, RGB, RGBA",
            target_mode
        ))),
    }
}
