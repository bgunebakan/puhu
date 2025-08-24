use image::{DynamicImage, Rgb, Rgba, Luma, LumaA, GenericImageView};
use crate::errors::PuhuError;

/// Get pixel value at specified coordinates
pub fn get_pixel(image: &DynamicImage, x: u32, y: u32) -> Result<(u8, u8, u8, u8), PuhuError> {
    let (width, height) = image.dimensions();
    
    if x >= width || y >= height {
        return Err(PuhuError::InvalidOperation(
            format!("Pixel coordinates ({}, {}) out of bounds for image size {}x{}", x, y, width, height)
        ));
    }
    
    match image {
        DynamicImage::ImageRgb8(rgb_img) => {
            let pixel = rgb_img.get_pixel(x, y);
            Ok((pixel[0], pixel[1], pixel[2], 255))
        }
        DynamicImage::ImageRgba8(rgba_img) => {
            let pixel = rgba_img.get_pixel(x, y);
            Ok((pixel[0], pixel[1], pixel[2], pixel[3]))
        }
        DynamicImage::ImageLuma8(gray_img) => {
            let pixel = gray_img.get_pixel(x, y);
            Ok((pixel[0], pixel[0], pixel[0], 255))
        }
        DynamicImage::ImageLumaA8(gray_alpha_img) => {
            let pixel = gray_alpha_img.get_pixel(x, y);
            Ok((pixel[0], pixel[0], pixel[0], pixel[1]))
        }
        _ => {
            let rgb_img = image.to_rgb8();
            let pixel = rgb_img.get_pixel(x, y);
            Ok((pixel[0], pixel[1], pixel[2], 255))
        }
    }
}

/// Set pixel value at specified coordinates
pub fn put_pixel(image: &DynamicImage, x: u32, y: u32, color: (u8, u8, u8, u8)) -> Result<DynamicImage, PuhuError> {
    let (width, height) = image.dimensions();
    
    if x >= width || y >= height {
        return Err(PuhuError::InvalidOperation(
            format!("Pixel coordinates ({}, {}) out of bounds for image size {}x{}", x, y, width, height)
        ));
    }
    
    let mut result = image.clone();
    
    match &mut result {
        DynamicImage::ImageRgb8(rgb_img) => {
            rgb_img.put_pixel(x, y, Rgb([color.0, color.1, color.2]));
        }
        DynamicImage::ImageRgba8(rgba_img) => {
            rgba_img.put_pixel(x, y, Rgba([color.0, color.1, color.2, color.3]));
        }
        DynamicImage::ImageLuma8(gray_img) => {
            // Convert RGB to grayscale using luminance formula
            let gray = (color.0 as f32 * 0.2126 + color.1 as f32 * 0.7152 + color.2 as f32 * 0.0722) as u8;
            gray_img.put_pixel(x, y, Luma([gray]));
        }
        DynamicImage::ImageLumaA8(gray_alpha_img) => {
            let gray = (color.0 as f32 * 0.2126 + color.1 as f32 * 0.7152 + color.2 as f32 * 0.0722) as u8;
            gray_alpha_img.put_pixel(x, y, LumaA([gray, color.3]));
        }
        _ => {
            return Err(PuhuError::InvalidOperation(
                "Unsupported image format for pixel manipulation".to_string()
            ));
        }
    }
    
    Ok(result)
}

/// Get a region of pixels as a 2D array
pub fn get_region(
    image: &DynamicImage,
    x: u32,
    y: u32,
    width: u32,
    height: u32,
) -> Result<Vec<Vec<(u8, u8, u8, u8)>>, PuhuError> {
    let (img_width, img_height) = image.dimensions();
    
    if x + width > img_width || y + height > img_height {
        return Err(PuhuError::InvalidOperation(
            format!("Region ({}, {}, {}, {}) out of bounds for image size {}x{}", 
                   x, y, width, height, img_width, img_height)
        ));
    }
    
    let mut region = Vec::with_capacity(height as usize);
    
    for row in 0..height {
        let mut row_pixels = Vec::with_capacity(width as usize);
        for col in 0..width {
            let pixel = get_pixel(image, x + col, y + row)?;
            row_pixels.push(pixel);
        }
        region.push(row_pixels);
    }
    
    Ok(region)
}

/// Set a region of pixels from a 2D array
pub fn put_region(
    image: &DynamicImage,
    x: u32,
    y: u32,
    pixels: &[Vec<(u8, u8, u8, u8)>],
) -> Result<DynamicImage, PuhuError> {
    let (img_width, img_height) = image.dimensions();
    let height = pixels.len() as u32;
    
    if height == 0 {
        return Ok(image.clone());
    }
    
    let width = pixels[0].len() as u32;
    
    if x + width > img_width || y + height > img_height {
        return Err(PuhuError::InvalidOperation(
            format!("Region ({}, {}, {}, {}) out of bounds for image size {}x{}", 
                   x, y, width, height, img_width, img_height)
        ));
    }
    
    let mut result = image.clone();
    
    for (row, pixel_row) in pixels.iter().enumerate() {
        for (col, &pixel) in pixel_row.iter().enumerate() {
            result = put_pixel(&result, x + col as u32, y + row as u32, pixel)?;
        }
    }
    
    Ok(result)
}

/// Apply a function to each pixel in the image
pub fn map_pixels<F>(image: &DynamicImage, mut func: F) -> Result<DynamicImage, PuhuError>
where
    F: FnMut(u32, u32, (u8, u8, u8, u8)) -> (u8, u8, u8, u8),
{
    let (width, height) = image.dimensions();
    let mut result = image.clone();
    
    for y in 0..height {
        for x in 0..width {
            let current_pixel = get_pixel(image, x, y)?;
            let new_pixel = func(x, y, current_pixel);
            result = put_pixel(&result, x, y, new_pixel)?;
        }
    }
    
    Ok(result)
}

/// Create a histogram of pixel values
pub fn histogram(image: &DynamicImage) -> Result<([u32; 256], [u32; 256], [u32; 256], [u32; 256]), PuhuError> {
    let (width, height) = image.dimensions();
    let mut r_hist = [0u32; 256];
    let mut g_hist = [0u32; 256];
    let mut b_hist = [0u32; 256];
    let mut a_hist = [0u32; 256];
    
    for y in 0..height {
        for x in 0..width {
            let (r, g, b, a) = get_pixel(image, x, y)?;
            r_hist[r as usize] += 1;
            g_hist[g as usize] += 1;
            b_hist[b as usize] += 1;
            a_hist[a as usize] += 1;
        }
    }
    
    Ok((r_hist, g_hist, b_hist, a_hist))
}

/// Find the dominant color in the image
pub fn dominant_color(image: &DynamicImage) -> Result<(u8, u8, u8, u8), PuhuError> {
    let (width, height) = image.dimensions();
    let mut color_counts = std::collections::HashMap::new();
    
    for y in 0..height {
        for x in 0..width {
            let pixel = get_pixel(image, x, y)?;
            *color_counts.entry(pixel).or_insert(0) += 1;
        }
    }
    
    color_counts
        .into_iter()
        .max_by_key(|(_, count)| *count)
        .map(|(color, _)| color)
        .ok_or_else(|| PuhuError::InvalidOperation("No pixels found in image".to_string()))
}

/// Calculate average color of the image
pub fn average_color(image: &DynamicImage) -> Result<(u8, u8, u8, u8), PuhuError> {
    let (width, height) = image.dimensions();
    let total_pixels = (width * height) as u64;
    
    if total_pixels == 0 {
        return Err(PuhuError::InvalidOperation("Image has no pixels".to_string()));
    }
    
    let mut r_sum = 0u64;
    let mut g_sum = 0u64;
    let mut b_sum = 0u64;
    let mut a_sum = 0u64;
    
    for y in 0..height {
        for x in 0..width {
            let (r, g, b, a) = get_pixel(image, x, y)?;
            r_sum += r as u64;
            g_sum += g as u64;
            b_sum += b as u64;
            a_sum += a as u64;
        }
    }
    
    Ok((
        (r_sum / total_pixels) as u8,
        (g_sum / total_pixels) as u8,
        (b_sum / total_pixels) as u8,
        (a_sum / total_pixels) as u8,
    ))
}

/// Replace all pixels of one color with another color
pub fn replace_color(
    image: &DynamicImage,
    target_color: (u8, u8, u8, u8),
    replacement_color: (u8, u8, u8, u8),
    tolerance: u8,
) -> Result<DynamicImage, PuhuError> {
    map_pixels(image, |_x, _y, pixel| {
        let distance = color_distance(pixel, target_color);
        if distance <= tolerance as f32 {
            replacement_color
        } else {
            pixel
        }
    })
}

/// Calculate color distance between two pixels
fn color_distance(color1: (u8, u8, u8, u8), color2: (u8, u8, u8, u8)) -> f32 {
    let dr = color1.0 as f32 - color2.0 as f32;
    let dg = color1.1 as f32 - color2.1 as f32;
    let db = color1.2 as f32 - color2.2 as f32;
    let da = color1.3 as f32 - color2.3 as f32;
    
    (dr * dr + dg * dg + db * db + da * da).sqrt()
}

/// Apply threshold to create a binary image
pub fn threshold(image: &DynamicImage, threshold_value: u8) -> Result<DynamicImage, PuhuError> {
    map_pixels(image, |_x, _y, pixel| {
        // Convert to grayscale first
        let gray = (pixel.0 as f32 * 0.2126 + pixel.1 as f32 * 0.7152 + pixel.2 as f32 * 0.0722) as u8;
        
        if gray >= threshold_value {
            (255, 255, 255, pixel.3) // White
        } else {
            (0, 0, 0, pixel.3) // Black
        }
    })
}

/// Apply posterization effect (reduce number of colors)
pub fn posterize(image: &DynamicImage, levels: u8) -> Result<DynamicImage, PuhuError> {
    if levels == 0 {
        return Err(PuhuError::InvalidOperation("Levels must be greater than 0".to_string()));
    }
    
    let step = 255.0 / (levels - 1) as f32;
    
    map_pixels(image, |_x, _y, pixel| {
        let r = ((pixel.0 as f32 / step).round() * step) as u8;
        let g = ((pixel.1 as f32 / step).round() * step) as u8;
        let b = ((pixel.2 as f32 / step).round() * step) as u8;
        
        (r, g, b, pixel.3)
    })
}
