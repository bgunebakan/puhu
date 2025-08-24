# Image Operations

Complete reference for all image manipulation operations in Puhu.

## 📂 File Operations

### Opening Images

#### `puhu.open(fp, mode=None, formats=None)`

Open an image file from various sources.

**Parameters:**
- `fp` (str | Path | bytes): File path, Path object, or image bytes
- `mode` (str, optional): Mode hint (not currently used)
- `formats` (list, optional): List of formats to try (not currently used)

**Returns:** `Image` instance

**Examples:**

```python
import puhu
from pathlib import Path

# From file path
img = puhu.open("photo.jpg")

# From Path object
img = puhu.open(Path("images/photo.png"))

# From bytes
with open("photo.jpg", "rb") as f:
    img = puhu.open(f.read())

# Error handling
try:
    img = puhu.open("nonexistent.jpg")
except FileNotFoundError:
    print("File not found")
except Exception as e:
    print(f"Error opening image: {e}")
```

**Supported Formats:**
- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- BMP (.bmp)
- TIFF (.tiff, .tif)
- WEBP (.webp)

### Saving Images

#### `Image.save(fp, format=None, **options)`

Save the image to a file.

**Parameters:**
- `fp` (str | Path): Output file path
- `format` (str, optional): Image format ("JPEG", "PNG", etc.)
- `**options`: Additional save options (reserved for future use)

**Examples:**

```python
img = puhu.open("input.jpg")

# Auto-detect format from extension
img.save("output.png")
img.save("output.jpg")

# Explicit format
img.save("output.webp", format="WEBP")

# Save to different directory
from pathlib import Path
output_dir = Path("processed")
output_dir.mkdir(exist_ok=True)
img.save(output_dir / "result.png")
```

## 🎨 Image Creation

### Creating New Images

#### `puhu.new(mode, size, color=0)`

Create a new image with specified mode, size, and color.

**Parameters:**
- `mode` (str): Image mode ("RGB", "RGBA", "L", "LA")
- `size` (tuple): Image size as (width, height)
- `color` (int | tuple | str): Fill color

**Returns:** New `Image` instance

**Examples:**

```python
# Solid color images
red_img = puhu.new("RGB", (400, 300), "red")
blue_img = puhu.new("RGB", (400, 300), (0, 0, 255))
transparent = puhu.new("RGBA", (400, 300), (255, 0, 0, 128))

# Grayscale
gray_img = puhu.new("L", (300, 300), 128)

# Black image (default)
black_img = puhu.new("RGB", (400, 300))

# Named colors
colors = ["red", "green", "blue", "yellow", "cyan", "magenta", "white", "black"]
for color in colors:
    img = puhu.new("RGB", (100, 100), color)
    img.save(f"{color}.png")
```

**Supported Modes:**
- `"RGB"`: 8-bit RGB color
- `"RGBA"`: 8-bit RGB with alpha
- `"L"`: 8-bit grayscale
- `"LA"`: 8-bit grayscale with alpha

### Creating from Arrays

#### `puhu.fromarray(obj, mode=None)`

Create an image from a NumPy array.

**Parameters:**
- `obj` (numpy.ndarray): Input array
- `mode` (str, optional): Mode hint (auto-detected from array shape)

**Returns:** New `Image` instance

**Requirements:** NumPy must be installed

**Examples:**

```python
import numpy as np
import puhu

# RGB array (height, width, 3)
rgb_array = np.random.randint(0, 256, (200, 300, 3), dtype=np.uint8)
rgb_img = puhu.fromarray(rgb_array)

# RGBA array (height, width, 4)
rgba_array = np.random.randint(0, 256, (200, 300, 4), dtype=np.uint8)
rgba_img = puhu.fromarray(rgba_array)

# Grayscale array (height, width)
gray_array = np.random.randint(0, 256, (200, 300), dtype=np.uint8)
gray_img = puhu.fromarray(gray_array)

# Float arrays (automatically converted to uint8)
float_array = np.random.random((100, 100, 3)).astype(np.float32)
img = puhu.fromarray(float_array)  # Values scaled from [0,1] to [0,255]

# Create gradient
def create_gradient(width, height, direction="horizontal"):
    if direction == "horizontal":
        gradient = np.linspace(0, 255, width, dtype=np.uint8)
        array = np.tile(gradient, (height, 1))
    else:
        gradient = np.linspace(0, 255, height, dtype=np.uint8)
        array = np.tile(gradient.reshape(-1, 1), (1, width))
    return puhu.fromarray(array)

gradient_img = create_gradient(400, 300, "horizontal")
```

## 🔄 Geometric Transformations

### Resizing

#### `Image.resize(size, resample=Resampling.BILINEAR)`

Resize the image to specified dimensions.

**Parameters:**
- `size` (tuple): Target size as (width, height)
- `resample` (str | int): Resampling algorithm

**Returns:** New resized `Image` instance

**Examples:**

```python
from puhu import Resampling

img = puhu.open("photo.jpg")

# Basic resize
small = img.resize((400, 300))
large = img.resize((1920, 1080))

# Different resampling methods
nearest = img.resize((400, 300), Resampling.NEAREST)    # Fastest
bilinear = img.resize((400, 300), Resampling.BILINEAR)  # Default
bicubic = img.resize((400, 300), Resampling.BICUBIC)    # Higher quality
lanczos = img.resize((400, 300), Resampling.LANCZOS)    # Best quality

# Maintain aspect ratio
def resize_with_aspect(img, max_width, max_height):
    width, height = img.size
    aspect = width / height
    
    if width > height:
        new_width = min(max_width, width)
        new_height = int(new_width / aspect)
    else:
        new_height = min(max_height, height)
        new_width = int(new_height * aspect)
    
    return img.resize((new_width, new_height))

# Scale by factor
def scale_image(img, factor):
    width, height = img.size
    return img.resize((int(width * factor), int(height * factor)))

scaled = scale_image(img, 0.5)  # 50% size
```

**Resampling Methods:**
- `NEAREST`: Fastest, lowest quality (good for pixel art)
- `BILINEAR`: Good balance of speed and quality (default)
- `BICUBIC`: Higher quality, slower
- `LANCZOS`: Best quality, slowest

### Cropping

#### `Image.crop(box)`

Extract a rectangular region from the image.

**Parameters:**
- `box` (tuple): Crop box as (left, top, right, bottom)

**Returns:** New cropped `Image` instance

**Examples:**

```python
img = puhu.open("photo.jpg")

# Basic crop
cropped = img.crop((100, 100, 500, 400))

# Center crop
def center_crop(img, crop_width, crop_height):
    width, height = img.size
    left = (width - crop_width) // 2
    top = (height - crop_height) // 2
    right = left + crop_width
    bottom = top + crop_height
    return img.crop((left, top, right, bottom))

square = center_crop(img, 400, 400)

# Smart crop with position
def crop_from_position(img, crop_size, position="center"):
    width, height = img.size
    crop_width, crop_height = crop_size
    
    positions = {
        "center": ((width - crop_width) // 2, (height - crop_height) // 2),
        "top_left": (0, 0),
        "top_right": (width - crop_width, 0),
        "bottom_left": (0, height - crop_height),
        "bottom_right": (width - crop_width, height - crop_height),
    }
    
    if position not in positions:
        raise ValueError(f"Invalid position: {position}")
    
    left, top = positions[position]
    return img.crop((left, top, left + crop_width, top + crop_height))

# Usage
top_left_crop = crop_from_position(img, (300, 200), "top_left")
```

### Rotation

#### `Image.rotate(angle, expand=False, fillcolor=None)`

Rotate the image by specified angle.

**Parameters:**
- `angle` (float): Rotation angle in degrees (90°, 180°, 270° supported)
- `expand` (bool): Whether to expand image to fit rotated content (not implemented)
- `fillcolor`: Fill color for empty areas (not implemented)

**Returns:** New rotated `Image` instance

**Examples:**

```python
img = puhu.open("photo.jpg")

# Standard rotations
rotated_90 = img.rotate(90)    # 90° clockwise
rotated_180 = img.rotate(180)  # 180°
rotated_270 = img.rotate(270)  # 270° clockwise (90° counter-clockwise)

# Multiple rotations
def rotate_multiple(img, angles):
    results = {}
    for angle in angles:
        results[f"{angle}°"] = img.rotate(angle)
    return results

rotations = rotate_multiple(img, [90, 180, 270])

# Note: Arbitrary angle rotation not yet implemented
# rotated_45 = img.rotate(45)  # Will raise NotImplementedError
```

### Transpose Operations

#### `Image.transpose(method)`

Flip or rotate the image using transpose operations.

**Parameters:**
- `method` (str | int): Transpose method

**Returns:** New transposed `Image` instance

**Examples:**

```python
from puhu import Transpose

img = puhu.open("photo.jpg")

# Flipping
flipped_h = img.transpose(Transpose.FLIP_LEFT_RIGHT)
flipped_v = img.transpose(Transpose.FLIP_TOP_BOTTOM)

# Rotation (alternative to rotate())
rotated_90 = img.transpose(Transpose.ROTATE_90)
rotated_180 = img.transpose(Transpose.ROTATE_180)
rotated_270 = img.transpose(Transpose.ROTATE_270)

# Using integer constants (Pillow compatibility)
flipped_h_int = img.transpose(0)  # FLIP_LEFT_RIGHT
flipped_v_int = img.transpose(1)  # FLIP_TOP_BOTTOM
```

**Transpose Methods:**
- `FLIP_LEFT_RIGHT`: Horizontal flip (mirror)
- `FLIP_TOP_BOTTOM`: Vertical flip
- `ROTATE_90`: 90° clockwise rotation
- `ROTATE_180`: 180° rotation
- `ROTATE_270`: 270° clockwise rotation

### Thumbnails

#### `Image.thumbnail(size, resample=Resampling.BICUBIC)`

Create a thumbnail version of the image in-place.

**Parameters:**
- `size` (tuple): Maximum size as (width, height)
- `resample` (str): Resampling algorithm

**Note:** This method modifies the image in-place (unlike other operations)

**Examples:**

```python
img = puhu.open("large_photo.jpg")
print(f"Original size: {img.size}")

# Create thumbnail (modifies original)
img.thumbnail((200, 200))
print(f"Thumbnail size: {img.size}")

# To keep original, make a copy first
original = puhu.open("large_photo.jpg")
thumbnail = original.copy()
thumbnail.thumbnail((200, 200))

# Create multiple thumbnail sizes
def create_thumbnails(img, sizes):
    thumbnails = {}
    for size in sizes:
        thumb = img.copy()
        thumb.thumbnail(size)
        thumbnails[f"{size[0]}x{size[1]}"] = thumb
    return thumbnails

sizes = [(64, 64), (128, 128), (256, 256)]
thumbs = create_thumbnails(img, sizes)
```

## 🎨 Mode and Channel Operations

### Mode Conversion

#### `Image.convert(mode)`

Convert the image to a different color mode.

**Parameters:**
- `mode` (str): Target mode ("RGB", "RGBA", "L", "LA")

**Returns:** New converted `Image` instance

**Examples:**

```python
img = puhu.open("color_photo.jpg")  # RGB

# Convert to grayscale
gray = img.convert("L")

# Add alpha channel
rgba = img.convert("RGBA")

# Remove alpha channel
rgb_from_rgba = rgba.convert("RGB")

# Grayscale with alpha
gray_alpha = img.convert("LA")

# Batch conversion
def convert_to_formats(img, modes):
    results = {}
    for mode in modes:
        results[mode] = img.convert(mode)
    return results

formats = convert_to_formats(img, ["L", "RGBA", "LA"])
```

### Channel Splitting

#### `Image.split()`

Split the image into individual channel images.

**Returns:** List of `Image` instances (one per channel)

**Examples:**

```python
# RGB image
rgb_img = puhu.open("color_photo.jpg")
r, g, b = rgb_img.split()  # 3 grayscale images

# RGBA image
rgba_img = rgb_img.convert("RGBA")
r, g, b, a = rgba_img.split()  # 4 grayscale images

# Grayscale image
gray_img = rgb_img.convert("L")
l, = gray_img.split()  # 1 grayscale image (note the comma)

# Process individual channels
enhanced_red = r.brightness(20).contrast(1.2)
blurred_green = g.blur(0.5)
sharpened_blue = b.sharpen(1.1)

# Save channels
channels = rgb_img.split()
channel_names = ["red", "green", "blue"]
for channel, name in zip(channels, channel_names):
    channel.save(f"channel_{name}.png")
```

## 🖼️ Compositing Operations

### Pasting Images

#### `Image.paste(im, box=None, mask=None)`

Paste another image onto this image.

**Parameters:**
- `im` (Image): Image to paste
- `box` (tuple, optional): Position as (x, y) or (x, y, x2, y2)
- `mask` (Image, optional): Mask image for alpha blending

**Returns:** New `Image` instance with pasted content

**Examples:**

```python
# Create base canvas
canvas = puhu.new("RGB", (800, 600), "white")

# Create elements
red_square = puhu.new("RGB", (100, 100), "red")
blue_circle = puhu.new("RGBA", (80, 80), (0, 0, 255, 128))

# Simple paste at position
result = canvas.paste(red_square, (50, 50))

# Paste with mask for alpha blending
mask = puhu.new("L", (100, 100), 128)  # 50% opacity
blended = canvas.paste(red_square, (200, 50), mask)

# Multiple pastes (chaining)
collage = (canvas
           .paste(red_square, (50, 50))
           .paste(blue_circle, (200, 100))
           .paste(red_square, (350, 150)))

# Create a grid layout
def create_grid(images, cols, cell_size):
    cell_width, cell_height = cell_size
    rows = (len(images) + cols - 1) // cols
    
    canvas_width = cols * cell_width
    canvas_height = rows * cell_height
    canvas = puhu.new("RGB", (canvas_width, canvas_height), "white")
    
    for i, img in enumerate(images):
        row = i // cols
        col = i % cols
        x = col * cell_width
        y = row * cell_height
        
        resized = img.resize(cell_size)
        canvas = canvas.paste(resized, (x, y))
    
    return canvas
```

## 🔍 Image Properties and Information

### Basic Properties

```python
img = puhu.open("photo.jpg")

# Dimensions
print(f"Size: {img.size}")           # (width, height) tuple
print(f"Width: {img.width}")         # Width in pixels
print(f"Height: {img.height}")       # Height in pixels

# Color information
print(f"Mode: {img.mode}")           # "RGB", "RGBA", "L", etc.
print(f"Format: {img.format}")       # "JPEG", "PNG", etc.

# Calculated properties
aspect_ratio = img.width / img.height
megapixels = (img.width * img.height) / 1_000_000
print(f"Aspect ratio: {aspect_ratio:.2f}")
print(f"Megapixels: {megapixels:.1f}MP")
```

### Data Access

#### `Image.to_bytes()`

Get the raw pixel data as bytes.

**Returns:** `bytes` object containing pixel data

**Examples:**

```python
img = puhu.open("photo.jpg")

# Get raw pixel data
pixel_data = img.to_bytes()
print(f"Data size: {len(pixel_data)} bytes")

# Calculate expected size
expected_size = img.width * img.height * len(img.mode)
print(f"Expected size: {expected_size} bytes")
```

### Copying Images

#### `Image.copy()`

Create a copy of the image.

**Returns:** New `Image` instance (identical copy)

**Examples:**

```python
original = puhu.open("photo.jpg")

# Create independent copy
copy = original.copy()

# Modify copy without affecting original
modified = copy.brightness(50).blur(1.0)

# Original remains unchanged
print(f"Original size: {original.size}")
print(f"Copy size: {copy.size}")
print(f"Modified size: {modified.size}")

# Use copy for in-place operations like thumbnail
thumb = original.copy()
thumb.thumbnail((200, 200))
```

## 🔧 Utility Functions

### Image Validation

```python
def validate_image_dimensions(size):
    """Validate image size tuple."""
    if not isinstance(size, (tuple, list)) or len(size) != 2:
        raise ValueError("Size must be a 2-tuple (width, height)")
    
    width, height = size
    if not all(isinstance(dim, int) for dim in [width, height]):
        raise ValueError("Dimensions must be integers")
    
    if width <= 0 or height <= 0:
        raise ValueError("Dimensions must be positive")
    
    return True

def validate_crop_box(box, img_size):
    """Validate crop box coordinates."""
    if len(box) != 4:
        raise ValueError("Crop box must have 4 coordinates")
    
    left, top, right, bottom = box
    img_width, img_height = img_size
    
    if any(coord < 0 for coord in [left, top]):
        raise ValueError("Crop coordinates cannot be negative")
    
    if right > img_width or bottom > img_height:
        raise ValueError("Crop box exceeds image boundaries")
    
    if left >= right or top >= bottom:
        raise ValueError("Invalid crop box dimensions")
    
    return True
```

### Batch Operations

```python
def batch_resize(image_paths, output_dir, size):
    """Resize multiple images."""
    from pathlib import Path
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    results = []
    for path in image_paths:
        try:
            img = puhu.open(path)
            resized = img.resize(size)
            
            output_file = output_path / f"resized_{Path(path).name}"
            resized.save(output_file)
            results.append(output_file)
            
        except Exception as e:
            print(f"Error processing {path}: {e}")
    
    return results

def batch_convert_format(image_paths, output_format="PNG"):
    """Convert multiple images to specified format."""
    results = []
    for path in image_paths:
        try:
            img = puhu.open(path)
            output_path = Path(path).with_suffix(f".{output_format.lower()}")
            img.save(output_path, format=output_format)
            results.append(output_path)
        except Exception as e:
            print(f"Error converting {path}: {e}")
    
    return results
```

## 🚨 Error Handling

### Common Exceptions

```python
import puhu

# File operations
try:
    img = puhu.open("nonexistent.jpg")
except FileNotFoundError:
    print("Image file not found")
except Exception as e:
    print(f"Error opening image: {e}")

# Invalid operations
try:
    img = puhu.new("RGB", (400, 300))
    # Invalid crop coordinates
    cropped = img.crop((100, 100, 50, 50))  # right < left
except ValueError as e:
    print(f"Invalid operation: {e}")

# Unsupported features
try:
    img = puhu.open("photo.jpg")
    rotated = img.rotate(45)  # Arbitrary angles not supported
except NotImplementedError as e:
    print(f"Feature not implemented: {e}")
```

### Safe Operation Wrappers

```python
def safe_operation(func, *args, **kwargs):
    """Safely execute an image operation."""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print(f"Operation failed: {e}")
        return None

# Usage
img = puhu.open("photo.jpg")
resized = safe_operation(img.resize, (800, 600))
if resized:
    resized.save("output.jpg")
```

## 🔗 Next Steps

- **[Filters](filters.md)** - Image filtering and effects
- **[Pixel Manipulation](pixel-manipulation.md)** - Direct pixel operations
- **[Drawing Operations](drawing.md)** - Shape and text drawing
- **[Performance Guide](performance.md)** - Optimization techniques