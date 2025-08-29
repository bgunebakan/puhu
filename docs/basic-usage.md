# Basic Usage Guide

This guide covers the fundamental concepts and patterns you'll use when working with Puhu.

## 🎯 Core Concepts

### Immutable Design

Puhu follows an immutable design pattern - operations return new images rather than modifying the original:

```python
import puhu

original = puhu.open("photo.jpg")
blurred = original.blur(2.0)

# original is unchanged
# blurred is a new image with the blur effect applied
print(f"Original size: {original.size}")
print(f"Blurred size: {blurred.size}")  # Same size, different content
```

### Method Chaining

Since operations return new images, you can chain them together:

```python
result = (puhu.open("photo.jpg")
          .resize((800, 600))
          .blur(1.0)
          .brightness(20)
          .contrast(1.2))

# Equivalent to:
img = puhu.open("photo.jpg")
img = img.resize((800, 600))
img = img.blur(1.0)
img = img.brightness(20)
result = img.contrast(1.2)
```

### Dual API Design

Puhu provides both object-oriented and functional APIs:

```python
# Object-oriented (method chaining)
result = img.blur(2.0).sharpen(1.5)

# Functional (module functions)
blurred = puhu.blur(img, 2.0)
result = puhu.sharpen(blurred, 1.5)
```

## 📂 Working with Images

### Opening Images

```python
import puhu
from pathlib import Path

# From file path (string)
img1 = puhu.open("photo.jpg")

# From Path object
img2 = puhu.open(Path("images/photo.png"))

# From bytes
with open("photo.jpg", "rb") as f:
    data = f.read()
    img3 = puhu.open(data)

# Check if file exists before opening
import os
if os.path.exists("photo.jpg"):
    img = puhu.open("photo.jpg")
else:
    print("File not found!")
```

### Image Properties

```python
img = puhu.open("photo.jpg")

# Basic properties
print(f"Size: {img.size}")           # (width, height) tuple
print(f"Width: {img.width}")         # Width in pixels
print(f"Height: {img.height}")       # Height in pixels
print(f"Mode: {img.mode}")           # Color mode: "RGB", "RGBA", "L", etc.
print(f"Format: {img.format}")       # Original format: "JPEG", "PNG", etc.

# Aspect ratio calculation
aspect_ratio = img.width / img.height
print(f"Aspect ratio: {aspect_ratio:.2f}")
```

### Creating New Images

```python
# Solid color images
red_square = puhu.new("RGB", (200, 200), "red")
blue_rect = puhu.new("RGB", (400, 300), (0, 0, 255))

# With transparency
transparent_red = puhu.new("RGBA", (200, 200), (255, 0, 0, 128))

# Grayscale
gray_img = puhu.new("L", (300, 300), 128)  # 50% gray

# Black image (default)
black_img = puhu.new("RGB", (400, 300))  # Default color is black
```

### Saving Images

```python
img = puhu.open("input.jpg")

# Save with format auto-detection
img.save("output.png")  # PNG format from extension
img.save("output.jpg")  # JPEG format from extension

# Save with explicit format
img.save("output.webp", format="WEBP")

# Save to different directory
from pathlib import Path
output_dir = Path("processed_images")
output_dir.mkdir(exist_ok=True)
img.save(output_dir / "result.png")
```

## 🔄 Image Transformations

### Resizing

```python
img = puhu.open("large_photo.jpg")

# Basic resize
small = img.resize((400, 300))

# Maintain aspect ratio
def resize_with_aspect_ratio(img, max_width, max_height):
    width, height = img.size
    aspect = width / height
    
    if width > height:
        new_width = min(max_width, width)
        new_height = int(new_width / aspect)
    else:
        new_height = min(max_height, height)
        new_width = int(new_height * aspect)
    
    return img.resize((new_width, new_height))

# Usage
resized = resize_with_aspect_ratio(img, 800, 600)

# Using thumbnail (modifies in-place)
thumb_img = img.copy()
thumb_img.thumbnail((200, 200))  # Maintains aspect ratio
```

### Resampling Methods

```python
from puhu import Resampling

img = puhu.open("photo.jpg")

# Different resampling algorithms
nearest = img.resize((400, 300), Resampling.NEAREST)    # Fastest, lowest quality
bilinear = img.resize((400, 300), Resampling.BILINEAR)  # Good balance (default)
bicubic = img.resize((400, 300), Resampling.BICUBIC)    # Better quality
lanczos = img.resize((400, 300), Resampling.LANCZOS)    # Best quality, slower

# When to use each:
# NEAREST: Pixel art, very fast preview
# BILINEAR: General purpose, good performance
# BICUBIC: High quality photos
# LANCZOS: Maximum quality, detailed images
```

### Cropping

```python
img = puhu.open("photo.jpg")

# Basic crop (left, top, right, bottom)
cropped = img.crop((100, 100, 500, 400))

# Center crop
def center_crop(img, crop_width, crop_height):
    width, height = img.size
    left = (width - crop_width) // 2
    top = (height - crop_height) // 2
    right = left + crop_width
    bottom = top + crop_height
    return img.crop((left, top, right, bottom))

# Usage
square = center_crop(img, 400, 400)

# Smart crop (crop from specific position)
def crop_from_position(img, crop_size, position="center"):
    width, height = img.size
    crop_width, crop_height = crop_size
    
    if position == "center":
        left = (width - crop_width) // 2
        top = (height - crop_height) // 2
    elif position == "top_left":
        left, top = 0, 0
    elif position == "top_right":
        left = width - crop_width
        top = 0
    elif position == "bottom_left":
        left = 0
        top = height - crop_height
    elif position == "bottom_right":
        left = width - crop_width
        top = height - crop_height
    else:
        raise ValueError("Invalid position")
    
    return img.crop((left, top, left + crop_width, top + crop_height))
```

### Rotation and Flipping

```python
from puhu import Transpose

img = puhu.open("photo.jpg")

# Rotation (90° increments only)
rotated_90 = img.rotate(90)
rotated_180 = img.rotate(180)
rotated_270 = img.rotate(270)

# Flipping
flipped_h = img.transpose(Transpose.FLIP_LEFT_RIGHT)
flipped_v = img.transpose(Transpose.FLIP_TOP_BOTTOM)

# Rotation using transpose (alternative)
rot_90_alt = img.transpose(Transpose.ROTATE_90)
rot_180_alt = img.transpose(Transpose.ROTATE_180)
rot_270_alt = img.transpose(Transpose.ROTATE_270)
```

## 🎨 Color and Mode Operations

### Mode Conversion

```python
img = puhu.open("color_photo.jpg")  # Usually RGB

# Convert to grayscale
gray = img.convert("L")

# Add alpha channel
rgba = img.convert("RGBA")

# Remove alpha channel
rgb_from_rgba = rgba.convert("RGB")

# Grayscale with alpha
gray_alpha = img.convert("LA")

# Mode compatibility check
def ensure_mode(img, target_mode):
    if img.mode != target_mode:
        return img.convert(target_mode)
    return img

# Usage
rgba_img = ensure_mode(img, "RGBA")
```

### Channel Operations

```python
# Split RGB image into channels
r, g, b = img.split()

# Split RGBA image
rgba_img = img.convert("RGBA")
r, g, b, a = rgba_img.split()

# Work with individual channels
# Each channel is a grayscale image
enhanced_red = r.brightness(20).contrast(1.2)
enhanced_green = g.blur(0.5)
enhanced_blue = b.sharpen(1.1)

# Note: Puhu doesn't have merge() yet, but you can work with channels individually
```

### Color Analysis

```python
# Get image statistics
r_hist, g_hist, b_hist, a_hist = img.histogram()

# Find dominant color
dominant = img.dominant_color()
print(f"Most common color: {dominant}")

# Calculate average color
average = img.average_color()
print(f"Average color: {average}")

# Color replacement
# Replace red pixels with blue (with tolerance)
modified = img.replace_color((255, 0, 0), (0, 0, 255), tolerance=30)
```

## 🔢 Working with NumPy

### Creating Images from Arrays

```python
import numpy as np
import puhu

# RGB array (height, width, channels)
rgb_array = np.random.randint(0, 256, (200, 300, 3), dtype=np.uint8)
rgb_img = puhu.fromarray(rgb_array)

# Grayscale array (height, width)
gray_array = np.random.randint(0, 256, (200, 300), dtype=np.uint8)
gray_img = puhu.fromarray(gray_array)

# RGBA array
rgba_array = np.random.randint(0, 256, (200, 300, 4), dtype=np.uint8)
rgba_img = puhu.fromarray(rgba_array)

# Float arrays (automatically converted)
float_array = np.random.random((100, 100, 3)).astype(np.float32)
img_from_float = puhu.fromarray(float_array)  # Scaled to 0-255
```

### Array Processing Patterns

```python
# Create gradient
def create_gradient(width, height, direction="horizontal"):
    if direction == "horizontal":
        gradient = np.linspace(0, 255, width, dtype=np.uint8)
        array = np.tile(gradient, (height, 1))
    else:  # vertical
        gradient = np.linspace(0, 255, height, dtype=np.uint8)
        array = np.tile(gradient.reshape(-1, 1), (1, width))
    
    return puhu.fromarray(array)

# Create noise pattern
def create_noise(width, height, intensity=50):
    base = np.full((height, width, 3), 128, dtype=np.uint8)
    noise = np.random.randint(-intensity, intensity, (height, width, 3))
    noisy = np.clip(base + noise, 0, 255).astype(np.uint8)
    return puhu.fromarray(noisy)

# Usage
gradient_img = create_gradient(400, 300, "horizontal")
noise_img = create_noise(400, 300, 30)
```

## 🎯 Pixel-Level Operations

### Direct Pixel Access

```python
img = puhu.open("photo.jpg")

# Get pixel value at specific coordinates
pixel = img.getpixel(100, 100)
print(f"Pixel at (100, 100): {pixel}")

# Set pixel value (returns new image)
red_dot = img.putpixel(100, 100, (255, 0, 0, 255))

# Batch pixel operations
def draw_cross(img, center_x, center_y, size, color):
    result = img
    for i in range(-size, size + 1):
        # Horizontal line
        if 0 <= center_x + i < img.width:
            result = result.putpixel(center_x + i, center_y, color)
        # Vertical line
        if 0 <= center_y + i < img.height:
            result = result.putpixel(center_x, center_y + i, color)
    return result

# Usage
marked = draw_cross(img, 200, 150, 10, (255, 0, 0, 255))
```

### Thresholding and Quantization

```python
# Binary threshold
binary = img.threshold(128)  # Pixels > 128 become white, others black

# Posterize (reduce color levels)
posterized = img.posterize(4)  # Reduce to 4 levels per channel
```

## 🖼️ Image Composition

### Pasting Images

```python
# Create base canvas
canvas = puhu.new("RGB", (800, 600), "white")

# Create elements to paste
red_square = puhu.new("RGB", (100, 100), "red")
blue_circle = puhu.new("RGBA", (80, 80), (0, 0, 255, 128))

# Simple paste
canvas_with_square = canvas.paste(red_square, (50, 50))

# Paste with alpha blending
mask = puhu.new("L", (100, 100), 128)  # 50% opacity
blended = canvas.paste(red_square, (200, 50), mask)

# Multiple pastes
result = (canvas
          .paste(red_square, (50, 50))
          .paste(blue_circle, (200, 100))
          .paste(red_square, (350, 150)))
```

### Creating Collages

```python
def create_grid_collage(images, grid_size, cell_size):
    """Create a grid collage from a list of images."""
    cols, rows = grid_size
    cell_width, cell_height = cell_size
    
    canvas_width = cols * cell_width
    canvas_height = rows * cell_height
    canvas = puhu.new("RGB", (canvas_width, canvas_height), "white")
    
    for i, img in enumerate(images[:cols * rows]):
        row = i // cols
        col = i % cols
        
        # Resize image to fit cell
        resized = img.resize(cell_size)
        
        # Calculate position
        x = col * cell_width
        y = row * cell_height
        
        # Paste onto canvas
        canvas = canvas.paste(resized, (x, y))
    
    return canvas

# Usage
images = [puhu.open(f"photo_{i}.jpg") for i in range(1, 7)]
collage = create_grid_collage(images, (3, 2), (200, 150))
```

## 🔧 Error Handling

### Common Error Patterns

```python
import puhu

def safe_open(filepath):
    """Safely open an image with error handling."""
    try:
        return puhu.open(filepath)
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return None
    except Exception as e:
        print(f"Error opening {filepath}: {e}")
        return None

def safe_resize(img, size):
    """Safely resize with validation."""
    if img is None:
        return None
    
    width, height = size
    if width <= 0 or height <= 0:
        print("Invalid size: dimensions must be positive")
        return None
    
    try:
        return img.resize(size)
    except Exception as e:
        print(f"Error resizing: {e}")
        return None

# Usage
img = safe_open("photo.jpg")
if img:
    resized = safe_resize(img, (800, 600))
    if resized:
        resized.save("output.jpg")
```

### Validation Helpers

```python
def validate_image_size(size):
    """Validate image size tuple."""
    if not isinstance(size, (tuple, list)) or len(size) != 2:
        raise ValueError("Size must be a 2-tuple (width, height)")
    
    width, height = size
    if not isinstance(width, int) or not isinstance(height, int):
        raise ValueError("Width and height must be integers")
    
    if width <= 0 or height <= 0:
        raise ValueError("Width and height must be positive")
    
    return True

def validate_crop_box(box, img_size):
    """Validate crop box coordinates."""
    if len(box) != 4:
        raise ValueError("Crop box must have 4 coordinates")
    
    left, top, right, bottom = box
    img_width, img_height = img_size
    
    if left < 0 or top < 0:
        raise ValueError("Crop coordinates cannot be negative")
    
    if right > img_width or bottom > img_height:
        raise ValueError("Crop box exceeds image boundaries")
    
    if left >= right or top >= bottom:
        raise ValueError("Invalid crop box: right > left and bottom > top required")
    
    return True
```

## 📊 Performance Considerations

### Efficient Processing

```python
# Chain operations to minimize intermediate images
efficient = (img.resize((800, 600))
            .blur(1.0)
            .brightness(20)
            .save("output.jpg"))

# Instead of creating many intermediate variables
# less_efficient = img.resize((800, 600))
# less_efficient = less_efficient.blur(1.0)
# less_efficient = less_efficient.brightness(20)
# less_efficient.save("output.jpg")
```

### Memory Management

```python
# For large images, consider processing in chunks
def process_large_image(filepath):
    img = puhu.open(filepath)
    
    # Check image size
    if img.width * img.height > 10_000_000:  # > 10MP
        print("Large image detected, using thumbnail for preview")
        preview = img.copy()
        preview.thumbnail((1000, 1000))
        return preview
    
    return img

# Use thumbnail for previews
def create_preview(img, max_size=400):
    preview = img.copy()
    preview.thumbnail((max_size, max_size))
    return preview
```

## 🎯 Best Practices

### Code Organization

```python
# Group related operations
def enhance_photo(img):
    """Apply standard photo enhancements."""
    return (img.brightness(10)
           .contrast(1.1)
           .sharpen(1.2)
           .saturate(1.05))

def create_thumbnail_set(img):
    """Create multiple thumbnail sizes."""
    sizes = [(64, 64), (128, 128), (256, 256)]
    thumbnails = {}
    
    for size in sizes:
        thumb = img.copy()
        thumb.thumbnail(size)
        thumbnails[f"{size[0]}x{size[1]}"] = thumb
    
    return thumbnails

# Usage
enhanced = enhance_photo(img)
thumbs = create_thumbnail_set(enhanced)
```

### Configuration Management

```python
# Use configuration dictionaries
PHOTO_SETTINGS = {
    "thumbnail_size": (200, 200),
    "web_size": (800, 600),
    "print_size": (3000, 2000),
    "quality_settings": {
        "preview": {"blur": 0.5, "brightness": 5},
        "web": {"sharpen": 1.1, "contrast": 1.05},
        "print": {"sharpen": 1.3, "contrast": 1.1}
    }
}

def process_for_web(img):
    settings = PHOTO_SETTINGS["quality_settings"]["web"]
    return (img.resize(PHOTO_SETTINGS["web_size"])
           .sharpen(settings["sharpen"])
           .contrast(settings["contrast"]))
```

## 🔗 Next Steps

Now that you understand the basics, explore:

- **[Image Operations](image-operations.md)** - Detailed operation reference
- **[Filters](filters.md)** - Complete filter documentation
- **[Drawing Operations](drawing.md)** - Shape and text drawing
- **[Performance Guide](performance.md)** - Optimization techniques
- **[Examples](examples.md)** - Real-world usage examples