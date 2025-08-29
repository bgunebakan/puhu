# Installation Guide

This guide covers all the ways to install Puhu on your system.

## 📦 Quick Installation

### From PyPI (Recommended)

```bash
pip install puhu
```

This installs the pre-compiled binary wheels for most platforms.

### With Optional Dependencies

```bash
# For NumPy integration
pip install puhu[numpy]

# For development and testing
pip install puhu[dev]
```

## 🛠️ System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **Operating System**: Linux, macOS, or Windows
- **Architecture**: x86_64, ARM64 (Apple Silicon supported)

### Recommended
- **Python**: 3.10 or higher
- **NumPy**: 1.20+ (for array operations)
- **Memory**: 512MB+ available RAM

## 🔧 Platform-Specific Installation

### Linux

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3-pip
pip install puhu

# CentOS/RHEL/Fedora
sudo yum install python3-pip  # or dnf
pip install puhu

# Arch Linux
sudo pacman -S python-pip
pip install puhu
```

### macOS

```bash
# Using Homebrew
brew install python
pip install puhu

# Using MacPorts
sudo port install python310
pip install puhu
```

### Windows

```bash
# Using pip (in Command Prompt or PowerShell)
pip install puhu

# Using conda
conda install -c conda-forge puhu
```

## 🏗️ Building from Source

If pre-compiled wheels aren't available for your platform, you can build from source.

### Prerequisites

```bash
# Install Rust (required for building)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env

# Install Python build tools
pip install maturin
```

### Build and Install

```bash
# Clone the repository
git clone https://github.com/bgunebakan/puhu.git
cd puhu

# Install Python dependencies
pip install -r requirements.txt

# Build and install in development mode
maturin develop --release

# Or build wheel for distribution
maturin build --release
pip install target/wheels/puhu-*.whl
```

### Development Installation

```bash
# Clone and enter directory
git clone https://github.com/bgunebakan/puhu.git
cd puhu

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -r requirements.txt
maturin develop

# Run tests to verify installation
pytest python/puhu/tests/
```

## ✅ Verifying Installation

### Basic Verification

```python
import puhu
print(f"Puhu version: {puhu.__version__}")

# Test basic functionality
img = puhu.new("RGB", (100, 100), "red")
print(f"Created image: {img.size} {img.mode}")
```

### Comprehensive Test

```python
import puhu

# Test image creation
img = puhu.new("RGB", (200, 200), (255, 128, 0))

# Test basic operations
resized = img.resize((100, 100))
cropped = img.crop((50, 50, 150, 150))
rotated = img.rotate(90)

# Test filters
blurred = img.blur(2.0)
sharpened = img.sharpen(1.5)

print("✅ All basic operations working!")
```

### NumPy Integration Test

```python
try:
    import numpy as np
    import puhu
    
    # Create from NumPy array
    array = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
    img = puhu.fromarray(array)
    print("✅ NumPy integration working!")
    
except ImportError:
    print("⚠️  NumPy not available - install with: pip install numpy")
```

## 🚨 Troubleshooting

### Common Issues

#### Import Error: "No module named '_core'"

```bash
# Rebuild the Rust extension
maturin develop --release
```

#### "Rust compiler not found"

```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env
```

#### Permission Errors on Linux/macOS

```bash
# Use user installation
pip install --user puhu

# Or use virtual environment
python -m venv puhu_env
source puhu_env/bin/activate
pip install puhu
```

#### Windows Build Issues

```powershell
# Install Visual Studio Build Tools
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Install Rust
# Download from: https://rustup.rs/

# Then install Puhu
pip install puhu
```

### Performance Issues

#### Slow Import Times

```python
# This is normal on first import due to lazy loading
import puhu  # May take 1-2 seconds on first import
```

#### Memory Usage

```python
# Puhu is memory-efficient, but for very large images:
import puhu

# Process images in chunks or use streaming operations
# Large images (>100MP) may require significant RAM
```

### Getting Help

If you encounter issues:

1. **Check the [GitHub Issues](https://github.com/bgunebakan/puhu/issues)**
2. **Update to the latest version**: `pip install --upgrade puhu`
3. **Verify your Python version**: `python --version`
4. **Check platform compatibility**: Puhu supports x86_64 and ARM64

#### Reporting Issues

When reporting installation issues, please include:

```bash
# System information
python --version
pip --version
rustc --version  # If building from source

# Platform information
uname -a  # Linux/macOS
systeminfo  # Windows

# Installation command used
pip install puhu --verbose
```

## 🔄 Updating Puhu

### Regular Updates

```bash
# Update to latest version
pip install --upgrade puhu

# Check current version
python -c "import puhu; print(puhu.__version__)"
```

### Development Updates

```bash
# If installed from source
cd puhu
git pull origin main
maturin develop --release
```

## 🗑️ Uninstalling

```bash
# Remove Puhu
pip uninstall puhu

# Remove all dependencies (if not used by other packages)
pip uninstall maturin numpy pillow pytest
```

---

## Next Steps

Once Puhu is installed, check out:
- [Quick Start Guide](quickstart.md) - Get started with basic operations
- [Basic Usage](basic-usage.md) - Learn core concepts
- [Examples](examples.md) - See real-world usage examples