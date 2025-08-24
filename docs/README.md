# Puhu Documentation

Welcome to the comprehensive documentation for Puhu, a high-performance image processing library for Python with a Rust backend.

## 📚 Documentation Structure

### Getting Started
- [Installation Guide](installation.md) - How to install and set up Puhu
- [Quick Start](quickstart.md) - Get up and running in minutes
- [Basic Usage](basic-usage.md) - Core concepts and basic operations

### Feature Documentation
- [Image Operations](image-operations.md) - Core image manipulation functions
- [Filters](filters.md) - All available image filters and effects
- [CSS Filters](css-filters.md) - CSS-like filter effects
- [Pixel Manipulation](pixel-manipulation.md) - Direct pixel access and analysis
- [Drawing Operations](drawing.md) - Shape and text drawing capabilities
- [Shadow Effects](shadows.md) - Drop shadows, inner shadows, and glow effects
- [Compositing & Blending](compositing.md) - Advanced image compositing

### Advanced Topics
- [Performance Guide](performance.md) - Optimization tips and benchmarks
- [API Reference](api-reference.md) - Complete API documentation
- [Examples](examples.md) - Comprehensive examples and tutorials
- [Migration Guide](migration.md) - Migrating from PIL/Pillow

### Development
- [Contributing](contributing.md) - How to contribute to Puhu
- [Architecture](architecture.md) - Internal architecture and design
- [Building from Source](building.md) - Development setup and building
- [Testing](testing.md) - Running tests and adding new tests

## 🚀 Quick Links

- **[Installation](installation.md)** - Get Puhu installed
- **[Quick Start](quickstart.md)** - Your first Puhu program
- **[API Reference](api-reference.md)** - Complete method documentation
- **[Examples](examples.md)** - Real-world usage examples

## 🎯 Feature Overview

Puhu provides a comprehensive set of image processing capabilities:

### Core Operations
- Load, save, resize, crop, rotate images
- Format conversion and channel manipulation
- NumPy array integration

### Filters & Effects
- Basic filters (blur, sharpen, edge detection, emboss)
- CSS-like filters (sepia, grayscale, invert, hue rotation)
- Brightness, contrast, and saturation adjustments
- Shadow effects (drop shadow, inner shadow, glow)

### Advanced Features
- Pixel-level manipulation and analysis
- Drawing operations (shapes, lines, text)
- Color analysis and replacement
- Histogram generation and analysis
- Compositing and blending operations

### Performance
- High-performance Rust backend
- Memory-efficient processing
- Thread-safe operations
- Both method chaining and functional APIs

## 📖 Documentation Conventions

### Code Examples
All code examples in this documentation are tested and working. They assume you have Puhu installed and imported:

```python
import puhu

# Load an image
img = puhu.open("example.jpg")
```

### Method Signatures
Methods are documented with their full signatures and parameter types:

```python
def resize(self, size: Tuple[int, int], resample: Optional[str] = None) -> Image:
    """Resize image to specified dimensions."""
```

### Return Values
All methods that return new images follow the immutable pattern - the original image is not modified.

## 🔗 External Resources

- [GitHub Repository](https://github.com/bgunebakan/puhu)
- [PyPI Package](https://pypi.org/project/puhu/)
- [Issue Tracker](https://github.com/bgunebakan/puhu/issues)

## 📝 License

Puhu is licensed under the MIT License. See the [LICENSE](../LICENSE) file for details.

## 👥 Contributors

- **[Bilal Tonga](https://github.com/bgunebakan)** - Original author and maintainer
- **[GrandpaEJ](https://github.com/GrandpaEJ)** - Feature requests and guidance

---

*This documentation is continuously updated. If you find any issues or have suggestions, please [open an issue](https://github.com/bgunebakan/puhu/issues).*
