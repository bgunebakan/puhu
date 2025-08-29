# Puhu Documentation

Welcome to the Puhu documentation! This guide will help you get the most out of Puhu, the blazingly fast image processing library for Python.

## 📚 Documentation Index

### 🚀 Getting Started
- **[Quick Start Guide](quickstart.md)** - Get up and running in minutes
- **[Basic Usage](basic-usage.md)** - Core concepts and common patterns
- **[Migration Guide](migration.md)** - Moving from Pillow to Puhu

### 📖 Reference & Examples
- **[API Reference](api-reference.md)** - Complete method documentation
- **[Examples](examples.md)** - Real-world usage examples and tutorials
- **[Performance Guide](performance.md)** - Optimization techniques and best practices

### 🤝 Contributing
- **[Contributing Guide](contributing.md)** - How to contribute to Puhu

## 🎯 Quick Navigation

### New to Puhu?
Start with the **[Quick Start Guide](quickstart.md)** to install Puhu and run your first image processing operations.

### Coming from Pillow?
Check out the **[Migration Guide](migration.md)** for a smooth transition from Pillow to Puhu.

### Looking for Examples?
Browse the **[Examples](examples.md)** section for real-world usage patterns and creative applications.

### Need Performance?
Read the **[Performance Guide](performance.md)** to optimize your image processing workflows.

### Want to Contribute?
See the **[Contributing Guide](contributing.md)** to learn how you can help improve Puhu.

## 🔍 What You'll Learn

### Core Concepts
- Image loading, saving, and format conversion
- Basic transformations (resize, crop, rotate)
- Color mode conversions and channel operations
- Method chaining for efficient processing

### Advanced Features
- Built-in filters and effects
- CSS-style image filters
- Pixel manipulation and analysis
- Drawing operations and compositing
- Shadow effects and artistic filters

### Performance Optimization
- Batch processing techniques
- Memory management strategies
- Parallel processing approaches
- Performance monitoring and profiling

### Real-World Applications
- Photography enhancement workflows
- Web development image optimization
- Creative projects and artistic effects
- Data visualization and infographics
- E-commerce product image processing

## 🚀 Quick Example

```python
import puhu

# Load and enhance a photo
img = puhu.open("photo.jpg")

# Apply enhancements with method chaining
enhanced = (img
            .resize((800, 600))
            .brightness(15)
            .contrast(1.1)
            .saturate(1.05)
            .sharpen(1.2))

# Save the result
enhanced.save("enhanced_photo.jpg")
```

## 🔗 External Resources

- **[GitHub Repository](https://github.com/bgunebakan/puhu)** - Source code and issues
- **[PyPI Package](https://pypi.org/project/puhu/)** - Installation and releases
- **[Pillow Documentation](https://pillow.readthedocs.io/)** - API compatibility reference

## 📝 Documentation Feedback

Found an error or have suggestions for improving the documentation? Please:

1. **[Open an issue](https://github.com/bgunebakan/puhu/issues)** on GitHub
2. **[Submit a pull request](https://github.com/bgunebakan/puhu/pulls)** with improvements
3. **[Start a discussion](https://github.com/bgunebakan/puhu/discussions)** for questions

Your feedback helps make Puhu better for everyone! 🦉