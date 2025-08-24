# Contributing to Puhu

Thank you for your interest in contributing to Puhu! This guide will help you get started with contributing to the project.

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+**
- **Rust 1.70+**
- **Git**
- **Maturin** for building Python extensions

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/yourusername/puhu.git
   cd puhu
   ```

2. **Set up Python Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install maturin pytest
   ```

3. **Build Development Version**
   ```bash
   maturin develop --release
   ```

4. **Run Tests**
   ```bash
   pytest python/puhu/tests/
   ```

## 🎯 Areas for Contribution

### 🔥 High Priority

1. **Performance Optimization**
   - Benchmark existing operations
   - Optimize memory usage
   - Implement SIMD optimizations
   - Parallel processing improvements

2. **Core Features**
   - `frombytes()` and `tobytes()` methods
   - Advanced text rendering with font support
   - Additional image formats (AVIF, HEIF)
   - Metadata preservation

### 🚧 Medium Priority

3. **Image Processing Features**
   - More CSS-style filters
   - Advanced compositing modes
   - Path operations and vector graphics
   - Morphological operations

4. **API Enhancements**
   - Better error handling and messages
   - Type hints improvements
   - Async/await support for I/O operations
   - Streaming image processing

### 📚 Documentation & Testing

5. **Documentation**
   - More real-world examples
   - Performance comparisons
   - Video tutorials
   - API documentation improvements

6. **Testing**
   - Edge case testing
   - Performance benchmarks
   - Compatibility tests with different Python versions
   - Memory leak testing

## 🛠️ Development Workflow

### Code Organization

```
puhu/
├── src/                    # Rust source code
│   ├── lib.rs             # Main Rust library
│   ├── image.rs           # Image struct and methods
│   ├── filters.rs         # Image filters
│   └── drawing.rs         # Drawing operations
├── python/puhu/           # Python package
│   ├── __init__.py        # Python API
│   ├── constants.py       # Constants and enums
│   └── tests/             # Python tests
├── docs/                  # Documentation
└── examples/              # Example scripts
```

### Making Changes

1. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Follow the coding standards below
   - Add tests for new functionality
   - Update documentation as needed

3. **Test Your Changes**
   ```bash
   # Run Python tests
   pytest python/puhu/tests/
   
   # Run Rust tests
   cargo test
   
   # Test examples
   python examples/basic_usage.py
   ```

4. **Commit and Push**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   git push origin feature/your-feature-name
   ```

5. **Create Pull Request**
   - Describe your changes clearly
   - Include examples if applicable
   - Reference any related issues

## 📝 Coding Standards

### Rust Code

- Follow standard Rust formatting (`cargo fmt`)
- Use `cargo clippy` for linting
- Add documentation comments for public functions
- Include error handling with proper error types

```rust
/// Apply Gaussian blur to the image.
/// 
/// # Arguments
/// * `radius` - Blur radius in pixels
/// 
/// # Returns
/// New blurred image
/// 
/// # Example
/// ```rust
/// let blurred = image.blur(2.0)?;
/// ```
pub fn blur(&self, radius: f32) -> PyResult<Self> {
    // Implementation
}
```

### Python Code

- Follow PEP 8 style guide
- Use type hints where possible
- Add docstrings for all public functions
- Include examples in docstrings

```python
def blur(self, radius: float) -> 'Image':
    """Apply Gaussian blur to the image.
    
    Args:
        radius: Blur radius in pixels
        
    Returns:
        New blurred Image instance
        
    Example:
        >>> img = puhu.open("photo.jpg")
        >>> blurred = img.blur(2.0)
        >>> blurred.save("blurred.jpg")
    """
    return self._rust_image.blur(radius)
```

### Documentation

- Use clear, concise language
- Include practical examples
- Add performance notes where relevant
- Keep documentation up to date with code changes

## 🧪 Testing Guidelines

### Writing Tests

1. **Unit Tests** - Test individual functions
2. **Integration Tests** - Test feature combinations
3. **Performance Tests** - Benchmark critical operations
4. **Compatibility Tests** - Ensure Pillow compatibility

### Test Structure

```python
import pytest
import puhu
import numpy as np

class TestImageFilters:
    """Test image filter operations."""
    
    def test_blur_basic(self):
        """Test basic blur functionality."""
        img = puhu.new("RGB", (100, 100), "red")
        blurred = img.blur(2.0)
        
        assert blurred.size == img.size
        assert blurred.mode == img.mode
    
    def test_blur_radius_validation(self):
        """Test blur radius validation."""
        img = puhu.new("RGB", (100, 100), "red")
        
        with pytest.raises(ValueError):
            img.blur(-1.0)  # Negative radius should fail
    
    @pytest.mark.performance
    def test_blur_performance(self):
        """Test blur performance."""
        img = puhu.new("RGB", (1000, 1000), "red")
        
        import time
        start = time.time()
        blurred = img.blur(3.0)
        duration = time.time() - start
        
        assert duration < 1.0  # Should complete in under 1 second
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest python/puhu/tests/test_filters.py

# Run with coverage
pytest --cov=puhu

# Run performance tests
pytest -m performance

# Run tests in parallel
pytest -n auto
```

## 🚀 Performance Guidelines

### Benchmarking

Always benchmark performance changes:

```python
import time
import puhu

def benchmark_operation(operation, iterations=10):
    """Benchmark an image operation."""
    img = puhu.open("test_image.jpg")
    
    times = []
    for _ in range(iterations):
        start = time.time()
        result = operation(img)
        end = time.time()
        times.append(end - start)
    
    avg_time = sum(times) / len(times)
    print(f"Average time: {avg_time:.4f}s")
    return avg_time

# Benchmark blur operation
benchmark_operation(lambda img: img.blur(2.0))
```

### Memory Usage

Monitor memory usage for large images:

```python
import psutil
import os

def monitor_memory(func):
    """Monitor memory usage during function execution."""
    process = psutil.Process(os.getpid())
    
    mem_before = process.memory_info().rss / 1024 / 1024  # MB
    result = func()
    mem_after = process.memory_info().rss / 1024 / 1024   # MB
    
    print(f"Memory usage: {mem_after - mem_before:.1f} MB")
    return result
```

## 📋 Pull Request Guidelines

### Before Submitting

- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation is updated
- [ ] Performance impact is considered
- [ ] Breaking changes are documented

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Performance improvement
- [ ] Documentation update
- [ ] Breaking change

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Performance benchmarks run

## Documentation
- [ ] Code comments added
- [ ] API documentation updated
- [ ] Examples updated

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Tests pass locally
- [ ] No breaking changes (or documented)
```

## 🐛 Bug Reports

### Before Reporting

1. Check existing issues
2. Test with latest version
3. Create minimal reproduction case

### Bug Report Template

```markdown
## Bug Description
Clear description of the bug

## To Reproduce
Steps to reproduce:
1. Load image with `puhu.open("image.jpg")`
2. Apply operation `img.blur(2.0)`
3. See error

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- Puhu version: 
- Python version:
- Operating system:
- Image format/size:

## Additional Context
Any other relevant information
```

## 💡 Feature Requests

### Before Requesting

1. Check if feature already exists
2. Consider if it fits Puhu's scope
3. Think about API design

### Feature Request Template

```markdown
## Feature Description
Clear description of the proposed feature

## Use Case
Why is this feature needed?

## Proposed API
```python
# Example of how the feature would be used
result = img.new_feature(parameters)
```

## Implementation Ideas
Any thoughts on implementation

## Alternatives
Other ways to achieve the same goal
```

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- Documentation credits

## 📞 Getting Help

- **GitHub Issues** - For bugs and feature requests
- **GitHub Discussions** - For questions and general discussion
- **Code Review** - All PRs receive thorough review and feedback

## 🔗 Resources

- **[Rust Book](https://doc.rust-lang.org/book/)** - Learn Rust
- **[PyO3 Guide](https://pyo3.rs/)** - Python-Rust integration
- **[image-rs Documentation](https://docs.rs/image/)** - Core image library
- **[Pillow Documentation](https://pillow.readthedocs.io/)** - API compatibility reference

Thank you for contributing to Puhu! 🦉