use crate::errors::PuhuError;
use image::ImageFormat;

/// Parse a format string into an ImageFormat
pub fn parse_format(format_str: &str) -> Result<ImageFormat, PuhuError> {
    match format_str.to_uppercase().as_str() {
        "JPEG" | "JPG" => Ok(ImageFormat::Jpeg),
        "PNG" => Ok(ImageFormat::Png),
        "GIF" => Ok(ImageFormat::Gif),
        "BMP" => Ok(ImageFormat::Bmp),
        "TIFF" | "TIF" => Ok(ImageFormat::Tiff),
        "WEBP" => Ok(ImageFormat::WebP),
        "ICO" => Ok(ImageFormat::Ico),
        "PNM" => Ok(ImageFormat::Pnm),
        "DDS" => Ok(ImageFormat::Dds),
        "TGA" => Ok(ImageFormat::Tga),
        "FARBFELD" | "FF" => Ok(ImageFormat::Farbfeld),
        "AVIF" => Ok(ImageFormat::Avif),
        _ => Err(PuhuError::UnsupportedFormat(format!(
            "Unsupported format: {}",
            format_str
        ))),
    }
}
