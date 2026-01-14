# Tech Stack: Puhu

## Backend & Core (Rust)
- **Rust (2021 Edition):** The primary engine for all image processing logic, chosen for its memory safety, performance, and concurrency primitives.
- **PyO3:** The bridge between Rust and Python, allowing us to expose high-performance Rust functions as native Python modules.
- **Image Crate (`image`):** Provides the foundational types and codecs for a wide variety of image formats (PNG, JPEG, GIF, BMP, TIFF, WEBP).
- **Rayon:** Used for data-parallelism, allowing computationally intensive image operations (like resizing or filtering) to automatically scale across all available CPU cores.
- **Support Libraries:** 
  - `thiserror` for idiomatic Rust error management.
  - `color_quant` for efficient color quantization.
  - `csscolorparser` for modern, flexible color input support.

## Frontend & API (Python)
- **Python (3.8+):** The user-facing interface, providing a clean, Pillow-compatible API that is familiar to the majority of Python developers.
- **Maturin:** The build system used to compile the Rust core into a Python extension module and package it for distribution.

## Development & Infrastructure
- **Testing:** 
  - `pytest` for comprehensive integration testing of the Python API.
  - Standard Rust `#[test]` suites for verifying core logic in the `src/` directory.
- **Documentation:** Sphinx-based documentation hosted on Read the Docs, ensuring users have clear, accessible, and versioned guides.
- **CI/CD:** GitHub Actions for automated building of cross-platform wheels (Linux, macOS, Windows) and running the test suite on every push.
