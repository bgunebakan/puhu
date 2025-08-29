use image::{DynamicImage, ImageBuffer, Rgba, GenericImageView};
use crate::errors::PuhuError;

/// Blend modes for compositing operations
#[derive(Debug, Clone, Copy)]
pub enum BlendMode {
    Normal,
    Multiply,
    Screen,
    Overlay,
    SoftLight,
    HardLight,
    ColorDodge,
    ColorBurn,
    Darken,
    Lighten,
    Difference,
    Exclusion,
}

/// Composite two images using the specified blend mode
pub fn composite(
    base: &DynamicImage,
    overlay: &DynamicImage,
    blend_mode: BlendMode,
    opacity: f32,
) -> Result<DynamicImage, PuhuError> {
    let (base_width, base_height) = base.dimensions();
    let (overlay_width, overlay_height) = overlay.dimensions();
    
    // Use the smaller dimensions
    let width = base_width.min(overlay_width);
    let height = base_height.min(overlay_height);
    
    let base_rgba = base.to_rgba8();
    let overlay_rgba = overlay.to_rgba8();
    let mut result = ImageBuffer::new(width, height);
    
    let opacity = opacity.max(0.0).min(1.0);
    
    for y in 0..height {
        for x in 0..width {
            let base_pixel = base_rgba.get_pixel(x, y);
            let overlay_pixel = overlay_rgba.get_pixel(x, y);
            
            let blended = blend_pixels(
                (base_pixel[0], base_pixel[1], base_pixel[2], base_pixel[3]),
                (overlay_pixel[0], overlay_pixel[1], overlay_pixel[2], overlay_pixel[3]),
                blend_mode,
                opacity,
            );
            
            result.put_pixel(x, y, Rgba([blended.0, blended.1, blended.2, blended.3]));
        }
    }
    
    Ok(DynamicImage::ImageRgba8(result))
}

/// Blend two pixels using the specified blend mode
fn blend_pixels(
    base: (u8, u8, u8, u8),
    overlay: (u8, u8, u8, u8),
    blend_mode: BlendMode,
    opacity: f32,
) -> (u8, u8, u8, u8) {
    let base_r = base.0 as f32 / 255.0;
    let base_g = base.1 as f32 / 255.0;
    let base_b = base.2 as f32 / 255.0;
    let base_a = base.3 as f32 / 255.0;
    
    let overlay_r = overlay.0 as f32 / 255.0;
    let overlay_g = overlay.1 as f32 / 255.0;
    let overlay_b = overlay.2 as f32 / 255.0;
    let overlay_a = overlay.3 as f32 / 255.0;
    
    let (blended_r, blended_g, blended_b) = match blend_mode {
        BlendMode::Normal => (overlay_r, overlay_g, overlay_b),
        BlendMode::Multiply => (
            base_r * overlay_r,
            base_g * overlay_g,
            base_b * overlay_b,
        ),
        BlendMode::Screen => (
            1.0 - (1.0 - base_r) * (1.0 - overlay_r),
            1.0 - (1.0 - base_g) * (1.0 - overlay_g),
            1.0 - (1.0 - base_b) * (1.0 - overlay_b),
        ),
        BlendMode::Overlay => (
            overlay_blend(base_r, overlay_r),
            overlay_blend(base_g, overlay_g),
            overlay_blend(base_b, overlay_b),
        ),
        BlendMode::SoftLight => (
            soft_light_blend(base_r, overlay_r),
            soft_light_blend(base_g, overlay_g),
            soft_light_blend(base_b, overlay_b),
        ),
        BlendMode::HardLight => (
            hard_light_blend(base_r, overlay_r),
            hard_light_blend(base_g, overlay_g),
            hard_light_blend(base_b, overlay_b),
        ),
        BlendMode::ColorDodge => (
            color_dodge_blend(base_r, overlay_r),
            color_dodge_blend(base_g, overlay_g),
            color_dodge_blend(base_b, overlay_b),
        ),
        BlendMode::ColorBurn => (
            color_burn_blend(base_r, overlay_r),
            color_burn_blend(base_g, overlay_g),
            color_burn_blend(base_b, overlay_b),
        ),
        BlendMode::Darken => (
            base_r.min(overlay_r),
            base_g.min(overlay_g),
            base_b.min(overlay_b),
        ),
        BlendMode::Lighten => (
            base_r.max(overlay_r),
            base_g.max(overlay_g),
            base_b.max(overlay_b),
        ),
        BlendMode::Difference => (
            (base_r - overlay_r).abs(),
            (base_g - overlay_g).abs(),
            (base_b - overlay_b).abs(),
        ),
        BlendMode::Exclusion => (
            base_r + overlay_r - 2.0 * base_r * overlay_r,
            base_g + overlay_g - 2.0 * base_g * overlay_g,
            base_b + overlay_b - 2.0 * base_b * overlay_b,
        ),
    };
    
    // Apply opacity
    let final_r = base_r * (1.0 - opacity) + blended_r * opacity;
    let final_g = base_g * (1.0 - opacity) + blended_g * opacity;
    let final_b = base_b * (1.0 - opacity) + blended_b * opacity;
    
    // Combine alpha channels
    let final_a = base_a + overlay_a * (1.0 - base_a);
    
    (
        (final_r * 255.0) as u8,
        (final_g * 255.0) as u8,
        (final_b * 255.0) as u8,
        (final_a * 255.0) as u8,
    )
}

/// Overlay blend function
fn overlay_blend(base: f32, overlay: f32) -> f32 {
    if base < 0.5 {
        2.0 * base * overlay
    } else {
        1.0 - 2.0 * (1.0 - base) * (1.0 - overlay)
    }
}

/// Soft light blend function
fn soft_light_blend(base: f32, overlay: f32) -> f32 {
    if overlay < 0.5 {
        2.0 * base * overlay + base * base * (1.0 - 2.0 * overlay)
    } else {
        2.0 * base * (1.0 - overlay) + base.sqrt() * (2.0 * overlay - 1.0)
    }
}

/// Hard light blend function
fn hard_light_blend(base: f32, overlay: f32) -> f32 {
    if overlay < 0.5 {
        2.0 * base * overlay
    } else {
        1.0 - 2.0 * (1.0 - base) * (1.0 - overlay)
    }
}

/// Color dodge blend function
fn color_dodge_blend(base: f32, overlay: f32) -> f32 {
    if overlay >= 1.0 {
        1.0
    } else {
        (base / (1.0 - overlay)).min(1.0)
    }
}

/// Color burn blend function
fn color_burn_blend(base: f32, overlay: f32) -> f32 {
    if overlay <= 0.0 {
        0.0
    } else {
        1.0 - ((1.0 - base) / overlay).min(1.0)
    }
}

/// Alpha composite two images (standard alpha blending)
pub fn alpha_composite(base: &DynamicImage, overlay: &DynamicImage) -> Result<DynamicImage, PuhuError> {
    composite(base, overlay, BlendMode::Normal, 1.0)
}

/// Create a gradient overlay
pub fn gradient_overlay(
    image: &DynamicImage,
    start_color: (u8, u8, u8, u8),
    end_color: (u8, u8, u8, u8),
    direction: GradientDirection,
    blend_mode: BlendMode,
    opacity: f32,
) -> Result<DynamicImage, PuhuError> {
    let (width, height) = image.dimensions();
    let gradient = create_gradient(width, height, start_color, end_color, direction)?;
    composite(image, &gradient, blend_mode, opacity)
}

/// Gradient direction
#[derive(Debug, Clone, Copy)]
pub enum GradientDirection {
    Horizontal,
    Vertical,
    Diagonal,
    Radial,
}

/// Create a gradient image
fn create_gradient(
    width: u32,
    height: u32,
    start_color: (u8, u8, u8, u8),
    end_color: (u8, u8, u8, u8),
    direction: GradientDirection,
) -> Result<DynamicImage, PuhuError> {
    let mut gradient = ImageBuffer::new(width, height);
    
    let start_r = start_color.0 as f32;
    let start_g = start_color.1 as f32;
    let start_b = start_color.2 as f32;
    let start_a = start_color.3 as f32;
    
    let end_r = end_color.0 as f32;
    let end_g = end_color.1 as f32;
    let end_b = end_color.2 as f32;
    let end_a = end_color.3 as f32;
    
    for y in 0..height {
        for x in 0..width {
            let t = match direction {
                GradientDirection::Horizontal => x as f32 / (width - 1) as f32,
                GradientDirection::Vertical => y as f32 / (height - 1) as f32,
                GradientDirection::Diagonal => {
                    ((x + y) as f32) / ((width + height - 2) as f32)
                }
                GradientDirection::Radial => {
                    let center_x = width as f32 / 2.0;
                    let center_y = height as f32 / 2.0;
                    let max_distance = (center_x * center_x + center_y * center_y).sqrt();
                    let distance = ((x as f32 - center_x).powi(2) + (y as f32 - center_y).powi(2)).sqrt();
                    (distance / max_distance).min(1.0)
                }
            };
            
            let r = (start_r * (1.0 - t) + end_r * t) as u8;
            let g = (start_g * (1.0 - t) + end_g * t) as u8;
            let b = (start_b * (1.0 - t) + end_b * t) as u8;
            let a = (start_a * (1.0 - t) + end_a * t) as u8;
            
            gradient.put_pixel(x, y, Rgba([r, g, b, a]));
        }
    }
    
    Ok(DynamicImage::ImageRgba8(gradient))
}

/// Apply a color overlay to an image
pub fn color_overlay(
    image: &DynamicImage,
    color: (u8, u8, u8, u8),
    blend_mode: BlendMode,
    opacity: f32,
) -> Result<DynamicImage, PuhuError> {
    let (width, height) = image.dimensions();
    let color_layer = create_solid_color(width, height, color)?;
    composite(image, &color_layer, blend_mode, opacity)
}

/// Create a solid color image
fn create_solid_color(
    width: u32,
    height: u32,
    color: (u8, u8, u8, u8),
) -> Result<DynamicImage, PuhuError> {
    let mut solid = ImageBuffer::new(width, height);
    
    for y in 0..height {
        for x in 0..width {
            solid.put_pixel(x, y, Rgba([color.0, color.1, color.2, color.3]));
        }
    }
    
    Ok(DynamicImage::ImageRgba8(solid))
}
