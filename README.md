# Puhu 🦉

[![CI](https://github.com/bgunebakan/puhu/workflows/CI/badge.svg)](https://github.com/bgunebakan/puhu/actions)
[![PyPI](https://img.shields.io/pypi/v/puhu.svg)](https://pypi.org/project/puhu/)
[![Documentation](https://readthedocs.org/projects/puhu/badge/?version=latest)](https://puhu.readthedocs.io/en/latest/)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Rust](https://img.shields.io/badge/rust-1.70+-orange.svg)](https://www.rust-lang.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A modern, high-performance image processing library for Python, powered by Rust. Puhu provides a Pillow-compatible API while delivering significantly better performance for common image operations.

## Features

- **High Performance** - Rust-powered for significantly faster operations
- **Pillow Compatible** - Drop-in replacement for most Pillow operations
- **Memory Safe** - Built with Rust's memory safety guarantees
- **Easy to Install** - Pre-built wheels for all major platforms
- **Rich Format Support** - PNG, JPEG, BMP, TIFF, GIF, WEBP

## Installation

```bash
pip install puhu
```

Pre-built wheels are available for:

- **Linux** (x86_64, ARM64)
- **macOS** (Intel, Apple Silicon)
- **Windows** (x64)
- **Python** 3.8+

## Quick Start

```python
import puhu

# Open and process an image
img = puhu.open("photo.jpg")
img = img.resize((800, 600))
img = img.crop((100, 100, 500, 400))
img.save("output.png")

# Drop-in Pillow replacement
from puhu import Image
img = Image.open("photo.jpg")
img = img.resize((400, 300))
img.save("resized.jpg")
```

## Documentation

Full documentation is available at **[puhu.readthedocs.io](https://puhu.readthedocs.io)**

- [Installation Guide](https://puhu.readthedocs.io/en/latest/installation.html)
- [Quick Start Tutorial](https://puhu.readthedocs.io/en/latest/quickstart.html)
- [API Reference](https://puhu.readthedocs.io/en/latest/api.html)
- [Pillow Compatibility](https://puhu.readthedocs.io/en/latest/pillow_compatibility.html)

## Development

### Building from Source

```bash
# Clone repository
git clone https://github.com/bgunebakan/puhu.git
cd puhu

# Install dependencies
pip install -r requirements.txt

# Build and install
maturin develop --release

# Run tests
pytest python/puhu/tests/
```

**Requirements**: Python 3.8+, Rust 1.70+, Maturin

## Contributing

Contributions are welcome! See our [Contributing Guide](https://puhu.readthedocs.io/en/latest/contributing.html) for details.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Links

- **Documentation**: https://puhu.readthedocs.io
- **PyPI**: https://pypi.org/project/puhu/
- **Source Code**: https://github.com/bgunebakan/puhu
- **Issue Tracker**: https://github.com/bgunebakan/puhu/issues

Built with [PyO3](https://pyo3.rs/) and [image-rs](https://github.com/image-rs/image)
