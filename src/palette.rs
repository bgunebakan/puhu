use image::DynamicImage;
use color_quant::NeuQuant;
use crate::errors::PuhuError;

pub fn generate_web_palette() -> Vec<u8> {
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

pub fn generate_adaptive_palette(image: &DynamicImage, num_colors: u32) -> Vec<u8> {
    let rgb_img = image.to_rgb8();
    let colors = num_colors.clamp(2, 256) as usize;
    
    // Convert to RGBA for NeuQuant
    let rgba_data: Vec<u8> = rgb_img.pixels()
        .flat_map(|p| [p[0], p[1], p[2], 255])
        .collect();
    
    let nq = NeuQuant::new(10, colors, &rgba_data);
    nq.color_map_rgb()
}

pub fn convert_to_palette(
    image: &DynamicImage,
    palette_type: &str,
    num_colors: u32,
    apply_dither: bool,
) -> Result<DynamicImage, PuhuError> {
    let rgb_img = image.to_rgb8();
    let (width, height) = rgb_img.dimensions();
    
    let palette = match palette_type {
        "WEB" => generate_web_palette(),
        "ADAPTIVE" => generate_adaptive_palette(image, num_colors),
        _ => {
            return Err(PuhuError::InvalidOperation(
                format!("Unsupported palette type: '{}'. Use 'WEB' or 'ADAPTIVE'", palette_type)
            ));
        }
    };

    let mut palette_indices = Vec::with_capacity((width * height) as usize);
    
    if apply_dither {
        palette_indices = apply_floyd_steinberg_dithering(&rgb_img, &palette, width, height);
    } else {
        // No dithering
        for pixel in rgb_img.pixels() {
            let (idx, _) = find_nearest_palette_color(&palette, pixel[0], pixel[1], pixel[2]);
            palette_indices.push(idx);
        }
    }

    // Convert palette indices back to RGB
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

fn apply_floyd_steinberg_dithering(
    rgb_img: &image::RgbImage,
    palette: &[u8],
    width: u32,
    height: u32,
) -> Vec<u8> {
    let mut palette_indices = Vec::with_capacity((width * height) as usize);
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
            
            let (idx, nearest) = find_nearest_palette_color(palette, r, g, b);
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
    
    palette_indices
}

pub fn find_nearest_palette_color(palette: &[u8], r: u8, g: u8, b: u8) -> (u8, (u8, u8, u8)) {
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
