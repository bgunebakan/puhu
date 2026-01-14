use crate::errors::PuhuError;
use image::ColorType;
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
