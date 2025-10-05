use pyo3::prelude::*;
use pyo3::types::PyModule;

mod errors;
mod image;
mod formats;
mod operations;
mod utils;
mod conversions;
mod palette;

pub use errors::PuhuError;
pub use image::PyImage;

#[pymodule]
fn _core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PyImage>()?;
    m.add("PuhuProcessingError", m.py().get_type_bound::<errors::PuhuProcessingError>())?;
    m.add("InvalidImageError", m.py().get_type_bound::<errors::InvalidImageError>())?;
    m.add("UnsupportedFormatError", m.py().get_type_bound::<errors::UnsupportedFormatError>())?;
    m.add("PuhuIOError", m.py().get_type_bound::<errors::PuhuIOError>())?;
    Ok(())
}
