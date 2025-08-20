# Puhu 🦉

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Rust](https://img.shields.io/badge/rust-1.70+-orange.svg)](https://www.rust-lang.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A **blazingly fast**, modern image processing library for Python, powered by Rust. Puhu provides a Pillow-compatible API while delivering significantly performance for common image operations.

## ✨ Key Features

- **🔥 High Performance**: Significantly fast for common image operations
- **🔄 Pillow Compatible**: Drop-in replacement for most Pillow operations
- **🦀 Rust Powered**: Memory-safe and efficient core written in Rust
- **📦 Easy to Use**: Simple, intuitive API that feels familiar
- **🎯 Format Support**: PNG, JPEG, BMP, TIFF, GIF, WEBP

## 🚀 Quick Start

### Installation

```bash
pip install puhu
```

### Basic Usage

```python
import puhu

# Open an image
img = puhu.open("photo.jpg")

# Resize image
resized = img.resize((800, 600))

# Crop image
cropped = img.crop((100, 100, 500, 400))

# Rotate image
rotated = img.rotate(90)

# Save image
img.save("output.png")

# Create new image
new_img = puhu.new("RGB", (800, 600), "red")
```

### Drop-in Pillow Replacement

```python
# Replace this:
# from PIL import Image

# With this:
from puhu import Image

# Your existing Pillow code works unchanged!
img = Image.open("photo.jpg")
img = img.resize((400, 300))
img.save("resized.jpg")
```

## 🔄 Pillow Compatibility

### ✅ Fully Compatible Operations

- `open()`, `new()`, `save()`
- `resize()`, `crop()`, `rotate()`, `transpose()`
- `copy()`, `thumbnail()`
- Properties: `size`, `width`, `height`, `mode`, `format`
- All major image formats (PNG, JPEG, BMP, TIFF, GIF, WEBP)

### 🚧 Planned Features

- `convert()`, `paste()`, `split()` - _High Priority_
- `filter()`, `getpixel()`, `putpixel()` - _Medium Priority_
- `fromarray()`, `frombytes()` - _NumPy Integration_

## 📖 API Reference

### Core Functions

```python
# Open image from file or bytes
img = puhu.open("path/to/image.jpg")
img = puhu.open(image_bytes)

# Create new image
img = puhu.new(mode, size, color=None)
# Examples:
img = puhu.new("RGB", (800, 600))  # Black image
img = puhu.new("RGB", (800, 600), "red")  # Red image
img = puhu.new("RGB", (800, 600), (255, 0, 0))  # Red image with RGB tuple
```

### Image Operations

```python
# Resize image
resized = img.resize((width, height), resample=puhu.Resampling.BILINEAR)

# Crop image (left, top, right, bottom)
cropped = img.crop((x1, y1, x2, y2))

# Rotate image (90°, 180°, 270° supported)
rotated = img.rotate(90)

# Transpose/flip image
flipped = img.transpose(puhu.Transpose.FLIP_LEFT_RIGHT)
flipped = img.transpose(puhu.Transpose.FLIP_TOP_BOTTOM)

# Copy image
copy = img.copy()

# Create thumbnail (modifies image in-place)
img.thumbnail((200, 200))

# Save image
img.save("output.jpg", format="JPEG")
img.save("output.png")  # Format auto-detected from extension
```

### Properties

```python
# Image dimensions
width = img.width
height = img.height
size = img.size  # (width, height) tuple

# Image mode and format
mode = img.mode  # "RGB", "RGBA", "L", etc.
format = img.format  # "JPEG", "PNG", etc.

# Raw pixel data
bytes_data = img.to_bytes()
```

## 🔧 Development

### Building from Source

```bash
# Clone repository
git clone https://github.com/your-username/puhu.git
cd puhu

# Install dependencies
pip install -r requirements.txt

# Build Rust extension
maturin develop --release

# Run tests
pytest python/puhu/tests/

```

### Requirements

- Python 3.8+
- Rust 1.70+
- Maturin for building

## 🤝 Contributing

Contributions are welcome! Areas where help is needed:

1. **High Priority Features**: `convert()`, `paste()`, `fromarray()`, `split()`
2. **Performance Optimization**: Further speed improvements
3. **Format Support**: Additional image formats
4. **Documentation**: Examples and tutorials
5. **Testing**: Edge cases and compatibility tests

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [PyO3](https://pyo3.rs/) for Python-Rust integration
- Uses [image-rs](https://github.com/image-rs/image) for core image processing
- Inspired by [Pillow](https://pillow.readthedocs.io/) for API design
