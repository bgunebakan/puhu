# Migration Guide

Complete guide for migrating from PIL/Pillow to Puhu with minimal code changes.

## 🔄 Overview

Puhu is designed as a drop-in replacement for Pillow, maintaining API compatibility while providing enhanced performance and additional features. Most existing Pillow code will work with minimal or no changes.

## 🚀 Quick Migration

### Simple Drop-in Replacement

```python
# Before (Pillow)
from PIL import Image
img = Image.open("photo.jpg")
img = img.resize((800, 600))
img.save("resized.jpg")

# After (Puhu)
from puhu import Image
img = Image.open("photo.jpg")
img = img.resize((800, 600))
img.save("resized.jpg")
```

### Import Statement Changes

```python
# Pillow imports
from PIL import Image, ImageFilter, ImageEnhance
from PIL.Image import Resampling, Transpose

# Puhu equivalents
from puhu import Image
from puhu import Resampling, Transpose
# Note: ImageFilter and ImageEnhance functionality is built into Image class
```

## 📋 Compatibility Matrix

### ✅ Fully Compatible Features

| Feature | Pillow | Puhu | Notes |
|---------|--------|------|-------|
| `Image.open()` | ✅ | ✅ | Identical API |
| `Image.new()` | ✅ | ✅ | Identical API |
| `Image.save()` | ✅ | ✅ | Identical API |
| `resize()` | ✅ | ✅ | Same parameters |
| `crop()` | ✅ | ✅ | Same parameters |
| `rotate()` | ✅ | ✅ | 90° increments only |
| `transpose()` | ✅ | ✅ | Same methods |
| `copy()` | ✅ | ✅ | Identical behavior |
| `convert()` | ✅ | ✅ | Same modes supported |
| `split()` | ✅ | ✅ | Same return format |
| `paste()` | ✅ | ✅ | Same parameters |
| Properties | ✅ | ✅ | `size`, `width`, `height`, `mode`, `format` |

### 🆕 Puhu Enhancements

| Feature | Pillow | Puhu | Enhancement |
|---------|--------|------|-------------|
| `blur()` | `ImageFilter.GaussianBlur` | Built-in method | Simpler API |
| `sharpen()` | `ImageFilter.SHARPEN` | Built-in method | Adjustable strength |
| `brightness()` | `ImageEnhance.Brightness` | Built-in method | Direct adjustment |
| `contrast()` | `ImageEnhance.Contrast` | Built-in method | Direct adjustment |
| `fromarray()` | ✅ | ✅ | Better NumPy integration |
| Pixel operations | Limited | Extended | `getpixel()`, `putpixel()`, `histogram()` |
| Drawing | `ImageDraw` module | Built-in methods | Integrated API |
| CSS filters | ❌ | ✅ | `sepia()`, `invert()`, `hue_rotate()` |
| Shadow effects | ❌ | ✅ | `drop_shadow()`, `glow()`, `inner_shadow()` |

### ⚠️ Partial Compatibility

| Feature | Pillow | Puhu | Migration Notes |
|---------|--------|------|-----------------|
| `rotate()` arbitrary angles | ✅ | ❌ | Only 90°, 180°, 270° supported |
| `frombytes()` | ✅ | ❌ | Use `fromarray()` instead |
| `tobytes()` | ✅ | `to_bytes()` | Method name changed |
| Advanced text rendering | ✅ | Limited | Basic bitmap fonts only |
| Some image modes | ✅ | Limited | CMYK, YCbCr not fully supported |

## 🔧 Step-by-Step Migration

### Step 1: Update Imports

```python
# Old Pillow imports
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
from PIL.Image import Resampling

# New Puhu imports
import puhu
from puhu import Resampling
# Note: Filter and enhance functionality is built into Image class
```

### Step 2: Replace Filter Operations

```python
# Pillow filter operations
from PIL import Image, ImageFilter, ImageEnhance

img = Image.open("photo.jpg")

# Old way
blurred = img.filter(ImageFilter.GaussianBlur(radius=2))
sharpened = img.filter(ImageFilter.SHARPEN)
enhancer = ImageEnhance.Brightness(img)
brightened = enhancer.enhance(1.2)

# Puhu way
import puhu

img = puhu.open("photo.jpg")
blurred = img.blur(2.0)
sharpened = img.sharpen(1.5)
brightened = img.brightness(20)  # Direct adjustment
```

### Step 3: Update Drawing Operations

```python
# Pillow drawing
from PIL import Image, ImageDraw

img = Image.new("RGB", (400, 300), "white")
draw = ImageDraw.Draw(img)
draw.rectangle([50, 50, 150, 150], fill="red")
draw.ellipse([200, 100, 300, 200], fill="blue")

# Puhu drawing
import puhu

img = puhu.new("RGB", (400, 300), "white")
img = img.draw_rectangle(50, 50, 100, 100, (255, 0, 0, 255))
img = img.draw_circle(250, 150, 50, (0, 0, 255, 255))
```

### Step 4: Handle NumPy Integration

```python
# Pillow NumPy integration
from PIL import Image
import numpy as np

array = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
img = Image.fromarray(array)
back_to_array = np.array(img)

# Puhu NumPy integration (same API)
import puhu
import numpy as np

array = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
img = puhu.fromarray(array)
# Note: to_array() not yet implemented, use alternative methods
```

## 🛠️ Common Migration Patterns

### Pattern 1: Basic Image Processing Pipeline

```python
# Pillow version
def process_image_pillow(input_path, output_path):
    from PIL import Image, ImageFilter, ImageEnhance
    
    img = Image.open(input_path)
    
    # Resize
    img = img.resize((800, 600), Image.Resampling.LANCZOS)
    
    # Enhance
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.1)
    
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.2)
    
    # Filter
    img = img.filter(ImageFilter.SHARPEN)
    
    img.save(output_path)

# Puhu version
def process_image_puhu(input_path, output_path):
    import puhu
    
    img = puhu.open(input_path)
    
    # Chain operations efficiently
    processed = (img
                 .resize((800, 600), puhu.Resampling.LANCZOS)
                 .brightness(10)    # Equivalent to enhance(1.1)
                 .contrast(1.2)
                 .sharpen(1.5))
    
    processed.save(output_path)
```

### Pattern 2: Batch Processing

```python
# Pillow version
def batch_process_pillow(image_paths):
    from PIL import Image, ImageEnhance
    
    results = []
    for path in image_paths:
        img = Image.open(path)
        
        # Apply enhancements
        brightness = ImageEnhance.Brightness(img)
        img = brightness.enhance(1.1)
        
        contrast = ImageEnhance.Contrast(img)
        img = contrast.enhance(1.2)
        
        # Resize
        img = img.resize((400, 300))
        
        output_path = f"processed_{Path(path).name}"
        img.save(output_path)
        results.append(output_path)
    
    return results

# Puhu version
def batch_process_puhu(image_paths):
    import puhu
    
    results = []
    for path in image_paths:
        # More efficient chaining
        processed = (puhu.open(path)
                     .brightness(10)
                     .contrast(1.2)
                     .resize((400, 300)))
        
        output_path = f"processed_{Path(path).name}"
        processed.save(output_path)
        results.append(output_path)
    
    return results
```

### Pattern 3: Image Analysis

```python
# Pillow version
def analyze_image_pillow(image_path):
    from PIL import Image
    import numpy as np
    
    img = Image.open(image_path)
    
    # Basic properties
    info = {
        "size": img.size,
        "mode": img.mode,
        "format": img.format,
    }
    
    # Convert to array for analysis
    array = np.array(img)
    info["mean_color"] = tuple(array.mean(axis=(0, 1)).astype(int))
    
    return info

# Puhu version
def analyze_image_puhu(image_path):
    import puhu
    
    img = puhu.open(image_path)
    
    # Enhanced analysis capabilities
    info = {
        "size": img.size,
        "mode": img.mode,
        "format": img.format,
        "dominant_color": img.dominant_color(),
        "average_color": img.average_color(),
    }
    
    # Get histogram data
    r_hist, g_hist, b_hist, a_hist = img.histogram()
    info["histogram_peaks"] = [
        r_hist.index(max(r_hist)),
        g_hist.index(max(g_hist)),
        b_hist.index(max(b_hist)),
    ]
    
    return info
```

## 🔄 Automated Migration Tools

### Migration Script

```python
#!/usr/bin/env python3
"""
Automated migration script to convert Pillow code to Puhu.
"""

import re
import sys
from pathlib import Path

class PillowToPuhuMigrator:
    """Automated code migration from Pillow to Puhu."""
    
    def __init__(self):
        self.replacements = [
            # Import replacements
            (r'from PIL import Image', 'import puhu'),
            (r'from PIL\.Image import', 'from puhu import'),
            (r'from PIL import ImageFilter', '# ImageFilter functionality is built into puhu.Image'),
            (r'from PIL import ImageEnhance', '# ImageEnhance functionality is built into puhu.Image'),
            (r'from PIL import ImageDraw', '# ImageDraw functionality is built into puhu.Image'),
            
            # Basic operations
            (r'Image\.open\(', 'puhu.open('),
            (r'Image\.new\(', 'puhu.new('),
            (r'Image\.fromarray\(', 'puhu.fromarray('),
            
            # Filter operations
            (r'\.filter\(ImageFilter\.GaussianBlur\(radius=(\d+(?:\.\d+)?)\)\)', r'.blur(\1)'),
            (r'\.filter\(ImageFilter\.SHARPEN\)', '.sharpen(1.5)'),
            (r'\.filter\(ImageFilter\.BLUR\)', '.blur(1.0)'),
            
            # Enhancement operations
            (r'ImageEnhance\.Brightness\([^)]+\)\.enhance\(([^)]+)\)', r'.brightness(int((\1 - 1) * 100))'),
            (r'ImageEnhance\.Contrast\([^)]+\)\.enhance\(([^)]+)\)', r'.contrast(\1)'),
            
            # Resampling constants
            (r'Image\.Resampling\.', 'puhu.Resampling.'),
            (r'Image\.LANCZOS', 'puhu.Resampling.LANCZOS'),
            (r'Image\.BICUBIC', 'puhu.Resampling.BICUBIC'),
            (r'Image\.BILINEAR', 'puhu.Resampling.BILINEAR'),
            (r'Image\.NEAREST', 'puhu.Resampling.NEAREST'),
            
            # Transpose constants
            (r'Image\.FLIP_LEFT_RIGHT', 'puhu.Transpose.FLIP_LEFT_RIGHT'),
            (r'Image\.FLIP_TOP_BOTTOM', 'puhu.Transpose.FLIP_TOP_BOTTOM'),
            
            # Method name changes
            (r'\.tobytes\(\)', '.to_bytes()'),
        ]
    
    def migrate_file(self, file_path):
        """Migrate a single Python file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Apply replacements
            for pattern, replacement in self.replacements:
                content = re.sub(pattern, replacement, content)
            
            # Check if changes were made
            if content != original_content:
                # Create backup
                backup_path = file_path.with_suffix(file_path.suffix + '.pillow_backup')
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                
                # Write migrated content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                return True, f"Migrated {file_path} (backup: {backup_path})"
            else:
                return False, f"No changes needed for {file_path}"
                
        except Exception as e:
            return False, f"Error migrating {file_path}: {e}"
    
    def migrate_directory(self, directory_path):
        """Migrate all Python files in a directory."""
        directory = Path(directory_path)
        results = []
        
        for py_file in directory.rglob("*.py"):
            changed, message = self.migrate_file(py_file)
            results.append((changed, message))
            print(message)
        
        # Summary
        changed_count = sum(1 for changed, _ in results if changed)
        total_count = len(results)
        
        print(f"\nMigration Summary:")
        print(f"Files processed: {total_count}")
        print(f"Files changed: {changed_count}")
        print(f"Files unchanged: {total_count - changed_count}")
        
        return results

def main():
    """Main migration function."""
    if len(sys.argv) != 2:
        print("Usage: python migrate_to_puhu.py <directory_or_file>")
        sys.exit(1)
    
    path = Path(sys.argv[1])
    migrator = PillowToPuhuMigrator()
    
    if path.is_file():
        changed, message = migrator.migrate_file(path)
        print(message)
    elif path.is_dir():
        migrator.migrate_directory(path)
    else:
        print(f"Error: {path} is not a valid file or directory")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### Usage

```bash
# Migrate a single file
python migrate_to_puhu.py my_image_script.py

# Migrate entire project
python migrate_to_puhu.py ./my_project/

# The script creates .pillow_backup files for safety
```

## 🧪 Testing Migration

### Validation Script

```python
"""
Validation script to test Pillow to Puhu migration.
"""

import puhu
from pathlib import Path

def test_basic_operations():
    """Test basic operations work correctly."""
    print("Testing basic operations...")
    
    # Create test image
    img = puhu.new("RGB", (100, 100), "red")
    assert img.size == (100, 100)
    assert img.mode == "RGB"
    
    # Test resize
    resized = img.resize((50, 50))
    assert resized.size == (50, 50)
    
    # Test crop
    cropped = img.crop((10, 10, 60, 60))
    assert cropped.size == (50, 50)
    
    # Test rotate
    rotated = img.rotate(90)
    assert rotated.size == (100, 100)
    
    print("✓ Basic operations working")

def test_filter_operations():
    """Test filter operations work correctly."""
    print("Testing filter operations...")
    
    img = puhu.new("RGB", (100, 100), "blue")
    
    # Test filters
    blurred = img.blur(2.0)
    assert blurred.size == img.size
    
    sharpened = img.sharpen(1.5)
    assert sharpened.size == img.size
    
    brightened = img.brightness(20)
    assert brightened.size == img.size
    
    contrasted = img.contrast(1.2)
    assert contrasted.size == img.size
    
    print("✓ Filter operations working")

def test_chaining():
    """Test method chaining works correctly."""
    print("Testing method chaining...")
    
    img = puhu.new("RGB", (200, 200), "green")
    
    # Chain multiple operations
    result = (img
              .resize((100, 100))
              .blur(1.0)
              .brightness(10)
              .contrast(1.1)
              .sharpen(1.2))
    
    assert result.size == (100, 100)
    print("✓ Method chaining working")

def test_file_operations():
    """Test file I/O operations."""
    print("Testing file operations...")
    
    # Create and save test image
    img = puhu.new("RGB", (50, 50), "yellow")
    test_path = "test_migration.png"
    
    try:
        img.save(test_path)
        
        # Load and verify
        loaded = puhu.open(test_path)
        assert loaded.size == (50, 50)
        assert loaded.mode == "RGB"
        
        print("✓ File operations working")
        
    finally:
        # Clean up
        if Path(test_path).exists():
            Path(test_path).unlink()

def run_migration_tests():
    """Run all migration validation tests."""
    print("Running Puhu migration validation tests...")
    print("=" * 50)
    
    try:
        test_basic_operations()
        test_filter_operations()
        test_chaining()
        test_file_operations()
        
        print("=" * 50)
        print("🎉 All migration tests passed!")
        print("Your Puhu migration is working correctly.")
        
    except Exception as e:
        print(f"❌ Migration test failed: {e}")
        print("Please check your Puhu installation and migration.")
        raise

if __name__ == "__main__":
    run_migration_tests()
```

## 📝 Migration Checklist

### Pre-Migration

- [ ] **Backup your code** - Create a full backup before starting
- [ ] **Identify Pillow usage** - Find all files using PIL/Pillow
- [ ] **Check dependencies** - Ensure Puhu is installed and working
- [ ] **Review compatibility** - Check for unsupported features

### During Migration

- [ ] **Update imports** - Change PIL imports to Puhu
- [ ] **Replace filter operations** - Convert ImageFilter usage
- [ ] **Update enhancement operations** - Convert ImageEnhance usage
- [ ] **Modify drawing operations** - Convert ImageDraw usage
- [ ] **Test incrementally** - Test each file after migration

### Post-Migration

- [ ] **Run validation tests** - Ensure everything works
- [ ] **Performance testing** - Verify performance improvements
- [ ] **Update documentation** - Document any API changes
- [ ] **Clean up backups** - Remove backup files when confident

## 🚨 Common Migration Issues

### Issue 1: Arbitrary Angle Rotation

```python
# Pillow (works)
rotated = img.rotate(45)

# Puhu (not supported yet)
# rotated = img.rotate(45)  # Will raise NotImplementedError

# Workaround: Use 90-degree increments
rotated_90 = img.rotate(90)
```

### Issue 2: Complex Text Rendering

```python
# Pillow (full font support)
from PIL import ImageDraw, ImageFont
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("arial.ttf", 24)
draw.text((10, 10), "Hello", font=font, fill="black")

# Puhu (basic bitmap fonts only)
img = img.draw_text("Hello", 10, 10, (0, 0, 0, 255), 2)
```

### Issue 3: Bytes Operations

```python
# Pillow
img_bytes = img.tobytes()
img_from_bytes = Image.frombytes("RGB", (100, 100), img_bytes)

# Puhu
img_bytes = img.to_bytes()  # Method name changed
# frombytes not yet implemented - use fromarray instead
```

## 🔗 Migration Resources

### Helpful Tools

1. **Migration Script** - Use the automated migration script above
2. **Validation Tests** - Run tests to verify migration success
3. **Performance Comparison** - Benchmark before and after migration
4. **Documentation** - Refer to API reference for detailed compatibility

### Getting Help

- **GitHub Issues** - Report migration problems
- **Documentation** - Check API reference for alternatives
- **Examples** - Look at migration examples in this guide
- **Community** - Ask questions in project discussions

## 🎯 Migration Benefits

After successful migration to Puhu, you'll gain:

- **Better Performance** - Rust-powered speed improvements
- **Enhanced API** - Built-in filters and effects
- **Method Chaining** - More elegant code patterns
- **Memory Safety** - Rust's memory management
- **Extended Features** - CSS filters, shadows, advanced drawing
- **Future-Proof** - Active development and improvements

## 🔗 Next Steps

- **[Performance Guide](performance.md)** - Optimize your migrated code
- **[Examples](examples.md)** - See real-world migration examples
- **[API Reference](api-reference.md)** - Complete method documentation
- **[Contributing](contributing.md)** - Help improve Puhu