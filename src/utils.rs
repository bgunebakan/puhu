use crate::errors::PuhuError;
use image::{ColorType, DynamicImage, GenericImage, GenericImageView, GrayImage};
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
    } else if let Ok((val,)) = input.extract::<(u8,)>() {
        // Single-element tuple -> grayscale (opaque)
        Ok((val, val, val, 255))
    } else if let Ok(tuple) = input.extract::<(u8, u8, u8)>() {
        // RGB tuple -> opaque
        Ok((tuple.0, tuple.1, tuple.2, 255))
    } else if let Ok(tuple) = input.extract::<(u8, u8, u8, u8)>() {
        // RGBA tuple
        Ok(tuple)
    } else {
        Err(PuhuError::InvalidOperation(
            "Color must be a string, integer, or tuple (1-item/RGB/RGBA)".to_string(),
        )
        .into())
    }
}

/// Region information for paste operations with clipping support
#[derive(Debug)]
pub struct PasteRegion {
    /// Source start x (offset into source image)
    pub sx: u32,
    /// Source start y (offset into source image)
    pub sy: u32,
    /// Destination start x
    pub dx: u32,
    /// Destination start y
    pub dy: u32,
    /// Copy width after clipping
    pub cw: u32,
    /// Copy height after clipping
    pub ch: u32,
}

/// Calculate clipped paste region for negative or out-of-bounds coordinates
pub fn calculate_paste_region(
    src_w: u32,
    src_h: u32,
    dest_w: u32,
    dest_h: u32,
    x: i32,
    y: i32,
) -> Option<PasteRegion> {
    // Source offsets (for negative dest coords, skip part of source)
    let sx = (-x).max(0) as u32;
    let sy = (-y).max(0) as u32;

    // Dest offsets (clamp to 0 for negative coords)
    let dx = x.max(0) as u32;
    let dy = y.max(0) as u32;

    // Calculate available source and dest dimensions
    let src_remaining_w = src_w.saturating_sub(sx);
    let src_remaining_h = src_h.saturating_sub(sy);
    let dest_remaining_w = dest_w.saturating_sub(dx);
    let dest_remaining_h = dest_h.saturating_sub(dy);

    // Copy dimensions are minimum of remaining source and dest space
    let cw = src_remaining_w.min(dest_remaining_w);
    let ch = src_remaining_h.min(dest_remaining_h);

    // Return None if nothing to copy
    if cw == 0 || ch == 0 {
        return None;
    }

    Some(PasteRegion {
        sx,
        sy,
        dx,
        dy,
        cw,
        ch,
    })
}

/// Paste source image onto destination with mask-based alpha blending
/// Supports negative coordinates through clipping
pub fn paste_with_mask(
    dest: &mut DynamicImage,
    src: &DynamicImage,
    x: i32,
    y: i32,
    mask: &DynamicImage,
) -> Result<(), PuhuError> {
    let region = match calculate_paste_region(
        src.width(),
        src.height(),
        dest.width(),
        dest.height(),
        x,
        y,
    ) {
        Some(r) => r,
        None => return Ok(()), // Nothing to paste
    };

    // Reuse grayscale masks without reallocation when possible.
    let mask_gray = mask.as_luma8().cloned().unwrap_or_else(|| mask.to_luma8());

    // Fast paths for common modes using typed image buffers.
    if let (Some(dest_rgb), Some(src_rgb)) = (dest.as_mut_rgb8(), src.as_rgb8()) {
        paste_with_mask_rgb8(dest_rgb, src_rgb, &mask_gray, &region);
        return Ok(());
    }
    if let (Some(dest_rgba), Some(src_rgba)) = (dest.as_mut_rgba8(), src.as_rgba8()) {
        paste_with_mask_rgba8(dest_rgba, src_rgba, &mask_gray, &region);
        return Ok(());
    }

    // Generic fallback for less common mode combinations.
    for py in 0..region.ch {
        for px in 0..region.cw {
            let src_x = region.sx + px;
            let src_y = region.sy + py;
            let dest_x = region.dx + px;
            let dest_y = region.dy + py;

            let mask_val = mask_gray.get_pixel(src_x, src_y)[0];
            let inv_alpha = 255u16.saturating_sub(mask_val as u16);

            // Get source and destination pixels
            let src_pixel = src.get_pixel(src_x, src_y);
            let dest_pixel = dest.get_pixel(dest_x, dest_y);

            // Blend: out = (src * alpha + dest * (255 - alpha)) / 255
            let blended = image::Rgba([
                blend_u8(src_pixel[0], dest_pixel[0], mask_val, inv_alpha),
                blend_u8(src_pixel[1], dest_pixel[1], mask_val, inv_alpha),
                blend_u8(src_pixel[2], dest_pixel[2], mask_val, inv_alpha),
                if src_pixel.0.len() > 3 && dest_pixel.0.len() > 3 {
                    blend_u8(src_pixel[3], dest_pixel[3], mask_val, inv_alpha)
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
/// Supports negative coordinates through clipping
pub fn fill_region(
    dest: &mut DynamicImage,
    x: i32,
    y: i32,
    width: u32,
    height: u32,
    color: (u8, u8, u8, u8),
) -> Result<(), PuhuError> {
    let region = match calculate_paste_region(width, height, dest.width(), dest.height(), x, y) {
        Some(r) => r,
        None => return Ok(()), // Nothing to fill
    };

    let (r, g, b, a) = color;

    if let Some(dest_rgb) = dest.as_mut_rgb8() {
        for py in 0..region.ch {
            let y = region.dy + py;
            for px in 0..region.cw {
                let x = region.dx + px;
                dest_rgb.put_pixel(x, y, image::Rgb([r, g, b]));
            }
        }
        return Ok(());
    }

    if let Some(dest_rgba) = dest.as_mut_rgba8() {
        for py in 0..region.ch {
            let y = region.dy + py;
            for px in 0..region.cw {
                let x = region.dx + px;
                dest_rgba.put_pixel(x, y, image::Rgba([r, g, b, a]));
            }
        }
        return Ok(());
    }

    if let Some(dest_luma) = dest.as_mut_luma8() {
        let l = rgb_to_luma_u8(r, g, b);
        for py in 0..region.ch {
            let y = region.dy + py;
            for px in 0..region.cw {
                let x = region.dx + px;
                dest_luma.put_pixel(x, y, image::Luma([l]));
            }
        }
        return Ok(());
    }

    // Generic fallback.
    let pixel = image::Rgba([r, g, b, a]);
    for py in 0..region.ch {
        let y = region.dy + py;
        for px in 0..region.cw {
            let x = region.dx + px;
            dest.put_pixel(x, y, pixel);
        }
    }

    Ok(())
}

#[inline]
fn blend_u8(src: u8, dst: u8, alpha: u8, inv_alpha: u16) -> u8 {
    let a = alpha as u16;
    (((src as u16 * a) + (dst as u16 * inv_alpha) + 127) / 255) as u8
}

#[inline]
fn rgb_to_luma_u8(r: u8, g: u8, b: u8) -> u8 {
    // Match Pillow-style luma conversion (ITU-R BT.601): 0.299 R + 0.587 G + 0.114 B
    ((299u32 * r as u32 + 587u32 * g as u32 + 114u32 * b as u32 + 500) / 1000) as u8
}

fn paste_with_mask_rgb8(
    dest: &mut image::RgbImage,
    src: &image::RgbImage,
    mask: &GrayImage,
    region: &PasteRegion,
) {
    for py in 0..region.ch {
        let sy = region.sy + py;
        let dy = region.dy + py;
        for px in 0..region.cw {
            let sx = region.sx + px;
            let dx = region.dx + px;
            let alpha = mask.get_pixel(sx, sy)[0];
            if alpha == 0 {
                continue;
            }
            if alpha == 255 {
                *dest.get_pixel_mut(dx, dy) = *src.get_pixel(sx, sy);
                continue;
            }
            let inv_alpha = 255u16 - alpha as u16;
            let s = src.get_pixel(sx, sy).0;
            let d = dest.get_pixel(dx, dy).0;
            *dest.get_pixel_mut(dx, dy) = image::Rgb([
                blend_u8(s[0], d[0], alpha, inv_alpha),
                blend_u8(s[1], d[1], alpha, inv_alpha),
                blend_u8(s[2], d[2], alpha, inv_alpha),
            ]);
        }
    }
}

fn paste_with_mask_rgba8(
    dest: &mut image::RgbaImage,
    src: &image::RgbaImage,
    mask: &GrayImage,
    region: &PasteRegion,
) {
    for py in 0..region.ch {
        let sy = region.sy + py;
        let dy = region.dy + py;
        for px in 0..region.cw {
            let sx = region.sx + px;
            let dx = region.dx + px;
            let alpha = mask.get_pixel(sx, sy)[0];
            if alpha == 0 {
                continue;
            }
            if alpha == 255 {
                *dest.get_pixel_mut(dx, dy) = *src.get_pixel(sx, sy);
                continue;
            }
            let inv_alpha = 255u16 - alpha as u16;
            let s = src.get_pixel(sx, sy).0;
            let d = dest.get_pixel(dx, dy).0;
            *dest.get_pixel_mut(dx, dy) = image::Rgba([
                blend_u8(s[0], d[0], alpha, inv_alpha),
                blend_u8(s[1], d[1], alpha, inv_alpha),
                blend_u8(s[2], d[2], alpha, inv_alpha),
                blend_u8(s[3], d[3], alpha, inv_alpha),
            ]);
        }
    }
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
