use image::imageops::FilterType;
use crate::errors::PuhuError;

/// Parse a resample filter string into a FilterType
pub fn parse_resample_filter(filter_str: Option<&str>) -> Result<FilterType, PuhuError> {
    match filter_str {
        Some("NEAREST") | Some("nearest") => Ok(FilterType::Nearest),
        Some("BILINEAR") | Some("bilinear") => Ok(FilterType::Triangle),
        Some("BICUBIC") | Some("bicubic") => Ok(FilterType::CatmullRom),
        Some("LANCZOS") | Some("lanczos") => Ok(FilterType::Lanczos3),
        None => Ok(FilterType::Triangle), // Default to bilinear
        Some(other) => Err(PuhuError::InvalidOperation(format!(
            "Unsupported resample filter: {}", other
        ))),
    }
}