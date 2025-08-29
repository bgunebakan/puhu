# Quick Start Guide

Get up and running with Puhu in just a few minutes! This guide covers the essential operations you'll use most often.

## 🚀 Your First Puhu Program

```python
import puhu

# Open an image
img = puhu.open("photo.jpg")

# Resize it
resized = img.resize((800, 600))

# Save the result
resized.save("resized_photo.jpg")

print(f"Resized image from {img.size} to {resized.size}")
```

## 📖 Basic Concepts

### Images are Immutable
Puhu follows an immutable design - operations return new images rather than modifying the original:

```python
img = puhu.open("photo.jpg")
blurred = img.blur(2.0)  # img is unchanged, blurred is a new image
```

### Method Chaining
You can chain operations together for concise code:

```python
result = (puhu.open("photo.jpg")
          .resize((800, 600))
          .blur(1.0)
          .brightness(20)
          .save("processed.jpg"))
```

### Pillow Compatibility
Puhu is designed as a drop-in replacement for Pillow:

```python
# Replace this:
# from PIL import Image

# With this:
from puhu import Image

# Your existing Pillow code works!
img = Image.open("photo.jpg")
```

## 🎯 Essential Operations

### 1. Opening and Saving Images

```python
import puhu

# Open from file path
img = puhu.open("image.jpg")

# Open from bytes
with open("image.jpg", "rb") as f:
    img = puhu.open(f.read())

# Save with format detection
img.save("output.png")  # PNG format detected from extension

# Save with explicit format
img.save("output.jpg", format="JPEG")
```

### 2. Creating New Images

```python
# Create solid color images
red_img = puhu.new("RGB", (400, 300), "red")
blue_img = puhu.new("RGB", (400, 300), (0, 0, 255))
transparent = puhu.new("RGBA", (400, 300), (255, 0, 0, 128))

# Create grayscale
gray_img = puhu.new("L", (400, 300), 128)
```

### 3. Basic Transformations

```python
img = puhu.open("photo.jpg")

# Resize (width, height)
small = img.resize((400, 300))
large = img.resize((1920, 1080))

# Crop (left, top, right, bottom)
cropped = img.crop((100, 100, 500, 400))

# Rotate (90°, 180°, 270° supported)
rotated = img.rotate(90)

# Flip and transpose
from puhu import Transpose
flipped_h = img.transpose(Transpose.FLIP_LEFT_RIGHT)
flipped_v = img.transpose(Transpose.FLIP_TOP_BOTTOM)
```

### 4. Image Properties

```python
img = puhu.open("photo.jpg")

print(f"Size: {img.size}")           # (width, height)
print(f"Width: {img.width}")         # Width in pixels
print(f"Height: {img.height}")       # Height in pixels
print(f"Mode: {img.mode}")           # "RGB", "RGBA", "L", etc.
print(f"Format: {img.format}")       # "JPEG", "PNG", etc.
```

## 🎨 Image Filters

### Basic Filters

```python
img = puhu.open("photo.jpg")

# Blur with radius
blurred = img.blur(2.0)

# Sharpen with strength
sharp = img.sharpen(1.5)

# Edge detection
edges = img.edge_detect()

# Emboss effect
embossed = img.emboss()

# Brightness adjustment (-255 to +255)
brighter = img.brightness(50)
darker = img.brightness(-30)

# Contrast adjustment (0.0 to 3.0+)
high_contrast = img.contrast(1.5)
low_contrast = img.contrast(0.7)
```

### CSS-Style Filters

```python
# Sepia tone (0.0 to 1.0)
sepia = img.sepia(0.8)

# Grayscale with amount control
gray = img.grayscale_filter(1.0)

# Color inversion
inverted = img.invert(1.0)

# Hue rotation in degrees
hue_shifted = img.hue_rotate(90)

# Saturation adjustment
desaturated = img.saturate(0.5)
oversaturated = img.saturate(2.0)
```

### Filter Chaining

```python
# Combine multiple filters
artistic = (img.blur(1.0)
           .sharpen(2.0)
           .brightness(20)
           .contrast(1.3)
           .sepia(0.3))

# Create different styles
vintage = img.sepia(0.8).contrast(0.9).brightness(-10)
dramatic = img.contrast(1.8).saturate(1.5).sharpen(1.2)
soft_focus = img.blur(0.8).brightness(10).contrast(0.8)
```

## 🔄 Mode Conversion and Channels

### Converting Between Modes

```python
img = puhu.open("color_photo.jpg")  # RGB image

# Convert to grayscale
gray = img.convert("L")

# Add alpha channel
rgba = img.convert("RGBA")

# Remove alpha channel
rgb = rgba.convert("RGB")
```

### Channel Operations

```python
# Split into individual channels
r, g, b = img.split()  # RGB image -> 3 grayscale images

# For RGBA images
r, g, b, a = rgba_img.split()  # 4 grayscale images
```

## 🎯 Pixel Operations

### Direct Pixel Access

```python
# Get pixel value at (x, y)
pixel = img.getpixel(100, 100)
print(f"Pixel at (100, 100): {pixel}")

# Set pixel value
modified = img.putpixel(100, 100, (255, 0, 0, 255))  # Red pixel
```

### Color Analysis

```python
# Get color histogram
r_hist, g_hist, b_hist, a_hist = img.histogram()

# Find dominant color
dominant = img.dominant_color()
print(f"Dominant color: {dominant}")

# Calculate average color
average = img.average_color()
print(f"Average color: {average}")
```

## 🖼️ Compositing Images

### Pasting Images

```python
# Create base image
base = puhu.new("RGB", (400, 300), "white")

# Create overlay
overlay = puhu.new("RGB", (100, 100), "red")

# Paste at position (x, y)
result = base.paste(overlay, (50, 50))

# Paste with alpha blending
mask = puhu.new("L", (100, 100), 128)  # 50% opacity
blended = base.paste(overlay, (50, 50), mask)
```

## 🔢 NumPy Integration

```python
import numpy as np
import puhu

# Create image from NumPy array
array = np.random.randint(0, 256, (200, 300, 3), dtype=np.uint8)
img = puhu.fromarray(array)

# Grayscale array
gray_array = np.random.randint(0, 256, (200, 300), dtype=np.uint8)
gray_img = puhu.fromarray(gray_array)

# Float arrays (automatically scaled)
float_array = np.random.random((100, 100, 3)).astype(np.float32)
img_from_float = puhu.fromarray(float_array)
```

## 🎨 Drawing Operations

```python
# Create canvas
canvas = puhu.new("RGB", (400, 300), "white")

# Draw shapes with RGBA colors
canvas = canvas.draw_rectangle(50, 50, 100, 80, (255, 0, 0, 255))  # Red rectangle
canvas = canvas.draw_circle(200, 150, 40, (0, 255, 0, 255))        # Green circle
canvas = canvas.draw_line(10, 10, 390, 290, (0, 0, 255, 255))      # Blue line

# Draw text
canvas = canvas.draw_text("Hello Puhu!", 150, 200, (0, 0, 0, 255), 2)

canvas.save("drawing.png")
```

## ✨ Shadow Effects

```python
# Convert to RGBA for best shadow results
rgba_img = img.convert("RGBA")

# Drop shadow (offset_x, offset_y, blur_radius, color)
with_shadow = rgba_img.drop_shadow(5, 5, 3.0, (0, 0, 0, 128))

# Glow effect (blur_radius, color, intensity)
glowing = rgba_img.glow(8.0, (255, 255, 0, 150), 1.5)

# Inner shadow
inner_shadow = rgba_img.inner_shadow(3, 3, 2.0, (0, 0, 0, 100))
```

## 🔧 Functional API

For functional programming style, use the module-level functions:

```python
import puhu

# Instead of method chaining
img = puhu.open("photo.jpg")
blurred = puhu.blur(img, 3.0)
edges = puhu.edge_detect(blurred)

# Functional composition
from functools import reduce

filters = [
    lambda x: puhu.blur(x, 1.0),
    lambda x: puhu.sharpen(x, 1.5),
    lambda x: puhu.brightness(x, 20),
]

result = reduce(lambda img, f: f(img), filters, puhu.open("photo.jpg"))
```

## 📊 Performance Tips

### Efficient Processing

```python
# Chain operations to minimize memory allocation
result = (img.resize((800, 600))
             .blur(1.0)
             .sharpen(1.2)
             .save("output.jpg"))

# Use appropriate resampling for your use case
from puhu import Resampling

# Fast but lower quality
quick = img.resize((400, 300), Resampling.NEAREST)

# High quality but slower
quality = img.resize((400, 300), Resampling.LANCZOS)
```

### Memory Management

```python
# For large images, process in smaller chunks when possible
# Puhu automatically manages memory efficiently

# Create thumbnails to reduce memory usage
img.thumbnail((200, 200))  # Modifies image in-place
```

## 🚨 Common Pitfalls

### 1. Coordinate Systems

```python
# Crop uses (left, top, right, bottom)
cropped = img.crop((100, 100, 300, 200))  # ✅ Correct

# Not (x, y, width, height)
# cropped = img.crop((100, 100, 200, 100))  # ❌ Wrong
```

### 2. Image Modes

```python
# Some operations require specific modes
rgba_img = img.convert("RGBA")  # Convert before shadow effects
shadow = rgba_img.drop_shadow(5, 5, 3.0, (0, 0, 0, 128))
```

### 3. Color Values

```python
# RGBA colors need 4 values
red_opaque = (255, 0, 0, 255)      # ✅ Correct
red_transparent = (255, 0, 0, 128)  # ✅ Correct
# red_wrong = (255, 0, 0)          # ❌ Missing alpha for RGBA operations
```

## 🎯 Next Steps

Now that you know the basics, explore:

- **[Image Operations](image-operations.md)** - Detailed operation documentation
- **[Filters](filters.md)** - Complete filter reference
- **[Examples](examples.md)** - Real-world usage examples
- **[API Reference](api-reference.md)** - Complete method documentation

## 💡 Quick Reference

```python
import puhu
from puhu import Resampling, Transpose

# Essential operations
img = puhu.open("input.jpg")
img.resize((800, 600))
img.crop((0, 0, 400, 300))
img.rotate(90)
img.transpose(Transpose.FLIP_LEFT_RIGHT)

# Filters
img.blur(2.0).sharpen(1.5).brightness(20).contrast(1.3)

# Creation
puhu.new("RGB", (400, 300), "red")
puhu.fromarray(numpy_array)

# Properties
img.size, img.width, img.height, img.mode, img.format
```

Happy image processing with Puhu! 🦉