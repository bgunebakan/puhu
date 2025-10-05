use pyo3::exceptions::PyException;
use pyo3::prelude::*;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum PuhuError {
    #[error("Invalid image data: {0}")]
    InvalidImage(String),
    #[error("Unsupported format: {0}")]
    UnsupportedFormat(String),
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),
    #[error("Image processing error: {0}")]
    ImageError(#[from] image::ImageError),
    #[error("Invalid operation: {0}")]
    InvalidOperation(String),
}

impl From<PuhuError> for PyErr {
    fn from(err: PuhuError) -> PyErr {
        match err {
            PuhuError::InvalidImage(msg) => InvalidImageError::new_err(msg),
            PuhuError::UnsupportedFormat(msg) => UnsupportedFormatError::new_err(msg),
            PuhuError::Io(err) => PuhuIOError::new_err(err.to_string()),
            PuhuError::ImageError(err) => PuhuProcessingError::new_err(err.to_string()),
            PuhuError::InvalidOperation(msg) => PuhuProcessingError::new_err(msg),
        }
    }
}

// Python exception types
pyo3::create_exception!(puhu_core, PuhuProcessingError, PyException);
pyo3::create_exception!(puhu_core, InvalidImageError, PuhuProcessingError);
pyo3::create_exception!(puhu_core, UnsupportedFormatError, PuhuProcessingError);
pyo3::create_exception!(puhu_core, PuhuIOError, PuhuProcessingError);
