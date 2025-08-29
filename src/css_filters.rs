use image::{DynamicImage, ImageBuffer, Rgb, Rgba};
use crate::errors::PuhuError;

/// Apply sepia filter (CSS-like sepia effect)
pub fn sepia(image: &DynamicImage, amount: f32) -> Result<DynamicImage, PuhuError> {
    let amount = amount.max(0.0).min(1.0); // Clamp between 0 and 1
    
    match image {
        DynamicImage::ImageRgb8(rgb_img) => {
            let (width, height) = rgb_img.dimensions();
            let mut result = ImageBuffer::new(width, height);

            for y in 0..height {
                for x in 0..width {
                    let pixel = rgb_img.get_pixel(x, y);
                    let r = pixel[0] as f32;
                    let g = pixel[1] as f32;
                    let b = pixel[2] as f32;

                    // Sepia transformation matrix
                    let sepia_r = (r * 0.393 + g * 0.769 + b * 0.189).min(255.0);
                    let sepia_g = (r * 0.349 + g * 0.686 + b * 0.168).min(255.0);
                    let sepia_b = (r * 0.272 + g * 0.534 + b * 0.131).min(255.0);

                    // Blend with original based on amount
                    let final_r = (r * (1.0 - amount) + sepia_r * amount) as u8;
                    let final_g = (g * (1.0 - amount) + sepia_g * amount) as u8;
                    let final_b = (b * (1.0 - amount) + sepia_b * amount) as u8;

                    result.put_pixel(x, y, Rgb([final_r, final_g, final_b]));
                }
            }

            Ok(DynamicImage::ImageRgb8(result))
        }
        DynamicImage::ImageRgba8(rgba_img) => {
            let (width, height) = rgba_img.dimensions();
            let mut result = ImageBuffer::new(width, height);

            for y in 0..height {
                for x in 0..width {
                    let pixel = rgba_img.get_pixel(x, y);
                    let r = pixel[0] as f32;
                    let g = pixel[1] as f32;
                    let b = pixel[2] as f32;
                    let a = pixel[3];

                    let sepia_r = (r * 0.393 + g * 0.769 + b * 0.189).min(255.0);
                    let sepia_g = (r * 0.349 + g * 0.686 + b * 0.168).min(255.0);
                    let sepia_b = (r * 0.272 + g * 0.534 + b * 0.131).min(255.0);

                    let final_r = (r * (1.0 - amount) + sepia_r * amount) as u8;
                    let final_g = (g * (1.0 - amount) + sepia_g * amount) as u8;
                    let final_b = (b * (1.0 - amount) + sepia_b * amount) as u8;

                    result.put_pixel(x, y, Rgba([final_r, final_g, final_b, a]));
                }
            }

            Ok(DynamicImage::ImageRgba8(result))
        }
        _ => {
            let rgb_img = image.to_rgb8();
            let rgb_dynamic = DynamicImage::ImageRgb8(rgb_img);
            sepia(&rgb_dynamic, amount)
        }
    }
}

/// Apply grayscale filter (CSS-like grayscale effect)
pub fn grayscale(image: &DynamicImage, amount: f32) -> Result<DynamicImage, PuhuError> {
    let amount = amount.max(0.0).min(1.0);
    
    match image {
        DynamicImage::ImageRgb8(rgb_img) => {
            let (width, height) = rgb_img.dimensions();
            let mut result = ImageBuffer::new(width, height);

            for y in 0..height {
                for x in 0..width {
                    let pixel = rgb_img.get_pixel(x, y);
                    let r = pixel[0] as f32;
                    let g = pixel[1] as f32;
                    let b = pixel[2] as f32;

                    // Luminance calculation (ITU-R BT.709)
                    let gray = r * 0.2126 + g * 0.7152 + b * 0.0722;

                    let final_r = (r * (1.0 - amount) + gray * amount) as u8;
                    let final_g = (g * (1.0 - amount) + gray * amount) as u8;
                    let final_b = (b * (1.0 - amount) + gray * amount) as u8;

                    result.put_pixel(x, y, Rgb([final_r, final_g, final_b]));
                }
            }

            Ok(DynamicImage::ImageRgb8(result))
        }
        DynamicImage::ImageRgba8(rgba_img) => {
            let (width, height) = rgba_img.dimensions();
            let mut result = ImageBuffer::new(width, height);

            for y in 0..height {
                for x in 0..width {
                    let pixel = rgba_img.get_pixel(x, y);
                    let r = pixel[0] as f32;
                    let g = pixel[1] as f32;
                    let b = pixel[2] as f32;
                    let a = pixel[3];

                    let gray = r * 0.2126 + g * 0.7152 + b * 0.0722;

                    let final_r = (r * (1.0 - amount) + gray * amount) as u8;
                    let final_g = (g * (1.0 - amount) + gray * amount) as u8;
                    let final_b = (b * (1.0 - amount) + gray * amount) as u8;

                    result.put_pixel(x, y, Rgba([final_r, final_g, final_b, a]));
                }
            }

            Ok(DynamicImage::ImageRgba8(result))
        }
        _ => {
            let rgb_img = image.to_rgb8();
            let rgb_dynamic = DynamicImage::ImageRgb8(rgb_img);
            grayscale(&rgb_dynamic, amount)
        }
    }
}

/// Apply invert filter (CSS-like invert effect)
pub fn invert(image: &DynamicImage, amount: f32) -> Result<DynamicImage, PuhuError> {
    let amount = amount.max(0.0).min(1.0);
    
    match image {
        DynamicImage::ImageRgb8(rgb_img) => {
            let (width, height) = rgb_img.dimensions();
            let mut result = ImageBuffer::new(width, height);

            for y in 0..height {
                for x in 0..width {
                    let pixel = rgb_img.get_pixel(x, y);
                    let r = pixel[0] as f32;
                    let g = pixel[1] as f32;
                    let b = pixel[2] as f32;

                    let inv_r = 255.0 - r;
                    let inv_g = 255.0 - g;
                    let inv_b = 255.0 - b;

                    let final_r = (r * (1.0 - amount) + inv_r * amount) as u8;
                    let final_g = (g * (1.0 - amount) + inv_g * amount) as u8;
                    let final_b = (b * (1.0 - amount) + inv_b * amount) as u8;

                    result.put_pixel(x, y, Rgb([final_r, final_g, final_b]));
                }
            }

            Ok(DynamicImage::ImageRgb8(result))
        }
        DynamicImage::ImageRgba8(rgba_img) => {
            let (width, height) = rgba_img.dimensions();
            let mut result = ImageBuffer::new(width, height);

            for y in 0..height {
                for x in 0..width {
                    let pixel = rgba_img.get_pixel(x, y);
                    let r = pixel[0] as f32;
                    let g = pixel[1] as f32;
                    let b = pixel[2] as f32;
                    let a = pixel[3];

                    let inv_r = 255.0 - r;
                    let inv_g = 255.0 - g;
                    let inv_b = 255.0 - b;

                    let final_r = (r * (1.0 - amount) + inv_r * amount) as u8;
                    let final_g = (g * (1.0 - amount) + inv_g * amount) as u8;
                    let final_b = (b * (1.0 - amount) + inv_b * amount) as u8;

                    result.put_pixel(x, y, Rgba([final_r, final_g, final_b, a]));
                }
            }

            Ok(DynamicImage::ImageRgba8(result))
        }
        _ => {
            let rgb_img = image.to_rgb8();
            let rgb_dynamic = DynamicImage::ImageRgb8(rgb_img);
            invert(&rgb_dynamic, amount)
        }
    }
}

/// Apply hue rotation filter (CSS-like hue-rotate effect)
pub fn hue_rotate(image: &DynamicImage, degrees: f32) -> Result<DynamicImage, PuhuError> {
    let radians = degrees.to_radians();
    let cos_val = radians.cos();
    let sin_val = radians.sin();
    
    // Hue rotation matrix coefficients
    let a = cos_val + (1.0 - cos_val) / 3.0;
    let _b = (1.0 - cos_val) / 3.0 - (3.0_f32).sqrt() * sin_val / 3.0;
    let c = (1.0 - cos_val) / 3.0 + (3.0_f32).sqrt() * sin_val / 3.0;
    
    match image {
        DynamicImage::ImageRgb8(rgb_img) => {
            let (width, height) = rgb_img.dimensions();
            let mut result = ImageBuffer::new(width, height);

            for y in 0..height {
                for x in 0..width {
                    let pixel = rgb_img.get_pixel(x, y);
                    let r = pixel[0] as f32;
                    let g = pixel[1] as f32;
                    let b = pixel[2] as f32;

                    let new_r = (a * r + _b * g + c * b).max(0.0).min(255.0) as u8;
                    let new_g = (c * r + a * g + _b * b).max(0.0).min(255.0) as u8;
                    let new_b = (_b * r + c * g + a * b).max(0.0).min(255.0) as u8;

                    result.put_pixel(x, y, Rgb([new_r, new_g, new_b]));
                }
            }

            Ok(DynamicImage::ImageRgb8(result))
        }
        DynamicImage::ImageRgba8(rgba_img) => {
            let (width, height) = rgba_img.dimensions();
            let mut result = ImageBuffer::new(width, height);

            for y in 0..height {
                for x in 0..width {
                    let pixel = rgba_img.get_pixel(x, y);
                    let r = pixel[0] as f32;
                    let g = pixel[1] as f32;
                    let b = pixel[2] as f32;
                    let alpha = pixel[3];

                    let new_r = (a * r + _b * g + c * b).max(0.0).min(255.0) as u8;
                    let new_g = (c * r + a * g + _b * b).max(0.0).min(255.0) as u8;
                    let new_b = (_b * r + c * g + a * b).max(0.0).min(255.0) as u8;

                    result.put_pixel(x, y, Rgba([new_r, new_g, new_b, alpha]));
                }
            }

            Ok(DynamicImage::ImageRgba8(result))
        }
        _ => {
            let rgb_img = image.to_rgb8();
            let rgb_dynamic = DynamicImage::ImageRgb8(rgb_img);
            hue_rotate(&rgb_dynamic, degrees)
        }
    }
}

/// Apply saturate filter (CSS-like saturate effect)
pub fn saturate(image: &DynamicImage, amount: f32) -> Result<DynamicImage, PuhuError> {
    let amount = amount.max(0.0); // No upper limit for saturation
    
    match image {
        DynamicImage::ImageRgb8(rgb_img) => {
            let (width, height) = rgb_img.dimensions();
            let mut result = ImageBuffer::new(width, height);

            for y in 0..height {
                for x in 0..width {
                    let pixel = rgb_img.get_pixel(x, y);
                    let r = pixel[0] as f32;
                    let g = pixel[1] as f32;
                    let b = pixel[2] as f32;

                    // Calculate luminance
                    let luminance = r * 0.2126 + g * 0.7152 + b * 0.0722;

                    // Apply saturation
                    let new_r = (luminance + (r - luminance) * amount).max(0.0).min(255.0) as u8;
                    let new_g = (luminance + (g - luminance) * amount).max(0.0).min(255.0) as u8;
                    let new_b = (luminance + (b - luminance) * amount).max(0.0).min(255.0) as u8;

                    result.put_pixel(x, y, Rgb([new_r, new_g, new_b]));
                }
            }

            Ok(DynamicImage::ImageRgb8(result))
        }
        DynamicImage::ImageRgba8(rgba_img) => {
            let (width, height) = rgba_img.dimensions();
            let mut result = ImageBuffer::new(width, height);

            for y in 0..height {
                for x in 0..width {
                    let pixel = rgba_img.get_pixel(x, y);
                    let r = pixel[0] as f32;
                    let g = pixel[1] as f32;
                    let b = pixel[2] as f32;
                    let a = pixel[3];

                    let luminance = r * 0.2126 + g * 0.7152 + b * 0.0722;

                    let new_r = (luminance + (r - luminance) * amount).max(0.0).min(255.0) as u8;
                    let new_g = (luminance + (g - luminance) * amount).max(0.0).min(255.0) as u8;
                    let new_b = (luminance + (b - luminance) * amount).max(0.0).min(255.0) as u8;

                    result.put_pixel(x, y, Rgba([new_r, new_g, new_b, a]));
                }
            }

            Ok(DynamicImage::ImageRgba8(result))
        }
        _ => {
            let rgb_img = image.to_rgb8();
            let rgb_dynamic = DynamicImage::ImageRgb8(rgb_img);
            saturate(&rgb_dynamic, amount)
        }
    }
}
