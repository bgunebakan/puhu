# API Reference

Complete reference for all Puhu classes, methods, and functions.

## 📚 Module Overview

```python
import puhu

# Core functions
puhu.open()          # Open image from file or bytes
puhu.new()           # Create new image
puhu.fromarray()     # Create image from NumPy array

# Functional API
puhu.blur()          # Apply blur filter
puhu.sharpen()       # Apply sharpen filter
puhu.brightness()    # Adjust brightness
# ... and more

# Classes
puhu.Image           # Main image class
puhu.ImageMode       # Image mode constants
puhu.ImageFormat     # Image format constants
puhu.Resampling      # Resampling method constants
puhu.Transpose       # Transpose operation constants
```

## 🖼️ Image Class

### Constructor

#### `Image(rust_image=None)`

Initialize an Image instance.

**Parameters:**
- `rust_image`: Internal Rust image object (typically not used directly)

**Note:** Use `puhu.open()`, `puhu.new()`, or `puhu.fromarray()` instead of direct construction.

### Class Methods

#### `Image.open(fp, mode=None, formats=None)`

Open an image file.

**Parameters:**
- `fp` (str | Path | bytes): File path, Path object, or image bytes
- `mode` (str, optional): Mode hint (reserved for future use)
- `formats` (list, optional): List of formats to try (reserved for future use)

**Returns:** `Image` instance

**Raises:**
- `FileNotFoundError`: If file doesn't exist
- `IOError`: If file cannot be read or is corrupted
- `UnsupportedFormatError`: If image format is not supported

**Examples:**

```python
# From file path
img = Image.open("photo.jpg")

# From Path object
from pathlib import Path
img = Image.open(Path("images/photo.png"))

# From bytes
with open("photo.jpg", "rb") as f:
    img = Image.open(f.read())
```

#### `Image.new(mode, size, color=0)`

Create a new image.

**Parameters:**
- `mode` (str): Image mode ("RGB", "RGBA", "L", "LA")
- `size` (tuple): Image size as (width, height)
- `color` (int | tuple | str): Fill color

**Returns:** New `Image` instance

**Examples:**

```python
# Solid color images
red_img = Image.new("RGB", (400, 300), "red")
blue_img = Image.new("RGB", (400, 300), (0, 0, 255))
transparent = Image.new("RGBA", (400, 300), (255, 0, 0, 128))

# Grayscale
gray_img = Image.new("L", (300, 300), 128)
```

#### `Image.fromarray(obj, mode=None)`

Create image from NumPy array.

**Parameters:**
- `obj` (numpy.ndarray): Input array
- `mode` (str, optional): Mode hint (auto-detected)

**Returns:** New `Image` instance

**Requires:** NumPy

**Examples:**

```python
import numpy as np

# RGB array
rgb_array = np.random.randint(0, 256, (200, 300, 3), dtype=np.uint8)
img = Image.fromarray(rgb_array)

# Grayscale array
gray_array = np.random.randint(0, 256, (200, 300), dtype=np.uint8)
gray_img = Image.fromarray(gray_array)
```

### Instance Methods

#### File Operations

##### `save(fp, format=None, **options)`

Save image to file.

**Parameters:**
- `fp` (str | Path): Output file path
- `format` (str, optional): Image format
- `**options`: Additional save options (reserved)

**Examples:**

```python
img.save("output.png")
img.save("output.jpg", format="JPEG")
```

##### `to_bytes()`

Get raw pixel data as bytes.

**Returns:** `bytes` object containing pixel data

#### Geometric Transformations

##### `resize(size, resample=Resampling.BILINEAR)`

Resize image to specified dimensions.

**Parameters:**
- `size` (tuple): Target size as (width, height)
- `resample` (str): Resampling algorithm

**Returns:** New resized `Image` instance

**Examples:**

```python
from puhu import Resampling

small = img.resize((400, 300))
quality = img.resize((800, 600), Resampling.LANCZOS)
```

##### `crop(box)`

Extract rectangular region from image.

**Parameters:**
- `box` (tuple): Crop box as (left, top, right, bottom)

**Returns:** New cropped `Image` instance

**Examples:**

```python
cropped = img.crop((100, 100, 500, 400))
```

##### `rotate(angle, expand=False, fillcolor=None)`

Rotate image by specified angle.

**Parameters:**
- `angle` (float): Rotation angle in degrees (90°, 180°, 270° supported)
- `expand` (bool): Whether to expand image (not implemented)
- `fillcolor`: Fill color for empty areas (not implemented)

**Returns:** New rotated `Image` instance

**Examples:**

```python
rotated_90 = img.rotate(90)
rotated_180 = img.rotate(180)
```

##### `transpose(method)`

Flip or rotate image using transpose operations.

**Parameters:**
- `method` (str | int): Transpose method

**Returns:** New transposed `Image` instance

**Examples:**

```python
from puhu import Transpose

flipped_h = img.transpose(Transpose.FLIP_LEFT_RIGHT)
flipped_v = img.transpose(Transpose.FLIP_TOP_BOTTOM)
```

##### `thumbnail(size, resample=Resampling.BICUBIC)`

Create thumbnail in-place.

**Parameters:**
- `size` (tuple): Maximum size as (width, height)
- `resample` (str): Resampling algorithm

**Note:** Modifies image in-place

**Examples:**

```python
img.thumbnail((200, 200))
```

##### `copy()`

Create copy of the image.

**Returns:** New `Image` instance (identical copy)

#### Mode and Channel Operations

##### `convert(mode)`

Convert image to different color mode.

**Parameters:**
- `mode` (str): Target mode ("RGB", "RGBA", "L", "LA")

**Returns:** New converted `Image` instance

**Examples:**

```python
gray = img.convert("L")
rgba = img.convert("RGBA")
```

##### `split()`

Split image into individual channel images.

**Returns:** List of `Image` instances (one per channel)

**Examples:**

```python
r, g, b = img.split()  # RGB image
r, g, b, a = rgba_img.split()  # RGBA image
```

##### `paste(im, box=None, mask=None)`

Paste another image onto this image.

**Parameters:**
- `im` (Image): Image to paste
- `box` (tuple, optional): Position as (x, y) or (x, y, x2, y2)
- `mask` (Image, optional): Mask image for alpha blending

**Returns:** New `Image` instance with pasted content

**Examples:**

```python
result = base.paste(overlay, (50, 50))
blended = base.paste(overlay, (50, 50), mask)
```

#### Basic Filters

##### `blur(radius)`

Apply Gaussian blur.

**Parameters:**
- `radius` (float): Blur radius

**Returns:** New blurred `Image` instance

##### `sharpen(strength)`

Apply sharpening filter.

**Parameters:**
- `strength` (float): Sharpening strength

**Returns:** New sharpened `Image` instance

##### `edge_detect()`

Detect edges using Sobel operator.

**Returns:** New `Image` instance with edges highlighted

##### `emboss()`

Apply emboss effect.

**Returns:** New `Image` instance with emboss effect

##### `brightness(adjustment)`

Adjust image brightness.

**Parameters:**
- `adjustment` (int): Brightness adjustment (-255 to +255)

**Returns:** New `Image` instance with adjusted brightness

##### `contrast(factor)`

Adjust image contrast.

**Parameters:**
- `factor` (float): Contrast factor (1.0 = no change)

**Returns:** New `Image` instance with adjusted contrast

#### CSS-Style Filters

##### `sepia(amount)`

Apply sepia tone effect.

**Parameters:**
- `amount` (float): Sepia intensity (0.0 to 1.0)

**Returns:** New `Image` instance with sepia effect

##### `grayscale_filter(amount)`

Convert to grayscale with amount control.

**Parameters:**
- `amount` (float): Grayscale intensity (0.0 to 1.0)

**Returns:** New `Image` instance with grayscale effect

##### `invert(amount)`

Invert image colors.

**Parameters:**
- `amount` (float): Inversion intensity (0.0 to 1.0)

**Returns:** New `Image` instance with inverted colors

##### `hue_rotate(degrees)`

Rotate hue of all colors.

**Parameters:**
- `degrees` (float): Hue rotation angle (0-360)

**Returns:** New `Image` instance with rotated hues

##### `saturate(factor)`

Adjust color saturation.

**Parameters:**
- `factor` (float): Saturation factor (1.0 = no change)

**Returns:** New `Image` instance with adjusted saturation

#### Pixel Operations

##### `getpixel(x, y)`

Get pixel color at coordinates.

**Parameters:**
- `x, y` (int): Pixel coordinates

**Returns:** Color tuple (depends on image mode)

##### `putpixel(x, y, color)`

Set pixel color at coordinates.

**Parameters:**
- `x, y` (int): Pixel coordinates
- `color` (tuple): Color value

**Returns:** New `Image` instance with modified pixel

##### `histogram()`

Generate color histograms.

**Returns:** Tuple of histograms `(r_hist, g_hist, b_hist, a_hist)`

##### `dominant_color()`

Find most frequently occurring color.

**Returns:** Color tuple representing dominant color

##### `average_color()`

Calculate average color of entire image.

**Returns:** Color tuple representing average color

##### `replace_color(target_color, replacement_color, tolerance=0)`

Replace specific colors.

**Parameters:**
- `target_color` (tuple): Color to replace
- `replacement_color` (tuple): New color
- `tolerance` (int): Color matching tolerance (0-255)

**Returns:** New `Image` instance with replaced colors

##### `threshold(threshold_value)`

Convert to binary based on threshold.

**Parameters:**
- `threshold_value` (int): Threshold value (0-255)

**Returns:** New binary `Image` instance

##### `posterize(levels)`

Reduce number of color levels.

**Parameters:**
- `levels` (int): Number of levels per channel

**Returns:** New posterized `Image` instance

#### Drawing Operations

##### `draw_rectangle(x, y, width, height, color)`

Draw filled rectangle.

**Parameters:**
- `x, y` (int): Top-left corner coordinates
- `width, height` (int): Rectangle dimensions
- `color` (tuple): RGBA color tuple

**Returns:** New `Image` instance with rectangle drawn

##### `draw_circle(center_x, center_y, radius, color)`

Draw filled circle.

**Parameters:**
- `center_x, center_y` (int): Circle center coordinates
- `radius` (int): Circle radius
- `color` (tuple): RGBA color tuple

**Returns:** New `Image` instance with circle drawn

##### `draw_line(x1, y1, x2, y2, color)`

Draw line between two points.

**Parameters:**
- `x1, y1, x2, y2` (int): Line endpoints
- `color` (tuple): RGBA color tuple

**Returns:** New `Image` instance with line drawn

##### `draw_text(text, x, y, color, scale=1)`

Draw text using bitmap font.

**Parameters:**
- `text` (str): Text to draw
- `x, y` (int): Text position
- `color` (tuple): RGBA color tuple
- `scale` (int): Text scale factor

**Returns:** New `Image` instance with text drawn

#### Shadow Effects

##### `drop_shadow(offset_x, offset_y, blur_radius, color)`

Add drop shadow behind image content.

**Parameters:**
- `offset_x, offset_y` (int): Shadow offset
- `blur_radius` (float): Shadow blur amount
- `color` (tuple): Shadow color as RGBA tuple

**Returns:** New `Image` instance with drop shadow

##### `glow(blur_radius, color, intensity=1.0)`

Add glow effect around image content.

**Parameters:**
- `blur_radius` (float): Glow blur radius
- `color` (tuple): Glow color as RGBA tuple
- `intensity` (float): Glow intensity multiplier

**Returns:** New `Image` instance with glow effect

##### `inner_shadow(offset_x, offset_y, blur_radius, color)`

Add inner shadow for depth and inset appearance.

**Parameters:**
- `offset_x, offset_y` (int): Shadow offset
- `blur_radius` (float): Shadow blur amount
- `color` (tuple): Shadow color as RGBA tuple

**Returns:** New `Image` instance with inner shadow

#### Properties

##### `size`

Image dimensions as (width, height) tuple.

**Type:** `tuple[int, int]`

##### `width`

Image width in pixels.

**Type:** `int`

##### `height`

Image height in pixels.

**Type:** `int`

##### `mode`

Image color mode.

**Type:** `str`

**Values:** "RGB", "RGBA", "L", "LA"

##### `format`

Original image format.

**Type:** `str | None`

**Values:** "JPEG", "PNG", "GIF", "BMP", "TIFF", "WEBP", etc.

## 🔧 Module Functions

### Core Functions

#### `open(fp, mode=None, formats=None)`

Open image file. Equivalent to `Image.open()`.

#### `new(mode, size, color=0)`

Create new image. Equivalent to `Image.new()`.

#### `fromarray(obj, mode=None)`

Create image from NumPy array. Equivalent to `Image.fromarray()`.

### Functional API

All image methods are also available as module functions:

#### `blur(image, radius)`

Apply blur filter functionally.

#### `sharpen(image, strength)`

Apply sharpen filter functionally.

#### `brightness(image, adjustment)`

Adjust brightness functionally.

#### `contrast(image, factor)`

Adjust contrast functionally.

#### `sepia(image, amount)`

Apply sepia effect functionally.

#### `grayscale_filter(image, amount)`

Apply grayscale filter functionally.

#### `invert(image, amount)`

Invert colors functionally.

#### `hue_rotate(image, degrees)`

Rotate hue functionally.

#### `saturate(image, factor)`

Adjust saturation functionally.

#### `edge_detect(image)`

Detect edges functionally.

#### `emboss(image)`

Apply emboss effect functionally.

#### `resize(image, size, resample=Resampling.BILINEAR)`

Resize image functionally.

#### `crop(image, box)`

Crop image functionally.

#### `rotate(image, angle)`

Rotate image functionally.

#### `convert(image, mode)`

Convert image mode functionally.

#### `split(image)`

Split image channels functionally.

#### `paste(base_image, overlay_image, position, mask=None)`

Paste images functionally.

## 📊 Constants and Enums

### ImageMode

Image mode constants.

```python
class ImageMode:
    L = "L"          # 8-bit grayscale
    LA = "LA"        # 8-bit grayscale + alpha
    RGB = "RGB"      # 8-bit RGB
    RGBA = "RGBA"    # 8-bit RGB + alpha
    I = "I"          # 32-bit integer grayscale
    CMYK = "CMYK"    # 8-bit CMYK (not fully supported)
    YCbCr = "YCbCr"  # 8-bit YCbCr (not fully supported)
    HSV = "HSV"      # 8-bit HSV (not fully supported)
    BINARY = "1"     # 1-bit binary (not fully supported)
```

### ImageFormat

Image format constants.

```python
class ImageFormat:
    JPEG = "JPEG"
    PNG = "PNG"
    GIF = "GIF"
    BMP = "BMP"
    TIFF = "TIFF"
    WEBP = "WEBP"
    ICO = "ICO"
    PNM = "PNM"
    DDS = "DDS"
    TGA = "TGA"
    FARBFELD = "FARBFELD"
    AVIF = "AVIF"
```

### Resampling

Resampling filter constants.

```python
class Resampling:
    NEAREST = "NEAREST"    # Fastest, lowest quality
    BILINEAR = "BILINEAR"  # Good balance (default)
    BICUBIC = "BICUBIC"    # Better quality
    LANCZOS = "LANCZOS"    # Best quality, slower
    
    # Pillow compatibility
    NEAREST_INT = 0
    BILINEAR_INT = 1
    BICUBIC_INT = 2
    LANCZOS_INT = 3
    
    @classmethod
    def from_int(cls, value: int) -> str:
        """Convert integer constant to string."""
```

### Transpose

Transpose operation constants.

```python
class Transpose:
    FLIP_LEFT_RIGHT = "FLIP_LEFT_RIGHT"
    FLIP_TOP_BOTTOM = "FLIP_TOP_BOTTOM"
    ROTATE_90 = "ROTATE_90"
    ROTATE_180 = "ROTATE_180"
    ROTATE_270 = "ROTATE_270"
    TRANSPOSE = "TRANSPOSE"      # Not implemented
    TRANSVERSE = "TRANSVERSE"    # Not implemented
    
    # Pillow compatibility
    FLIP_LEFT_RIGHT_INT = 0
    FLIP_TOP_BOTTOM_INT = 1
    ROTATE_90_INT = 2
    ROTATE_180_INT = 3
    ROTATE_270_INT = 4
    TRANSPOSE_INT = 5
    TRANSVERSE_INT = 6
    
    @classmethod
    def from_int(cls, value: int) -> str:
        """Convert integer constant to string."""
```

## ⚠️ Exceptions

### PuhuError

Base exception class for all Puhu errors.

### PuhuProcessingError

Raised when image processing operations fail.

### InvalidImageError

Raised when image data is invalid or corrupted.

### UnsupportedFormatError

Raised when image format is not supported.

### PuhuIOError

Raised when file I/O operations fail.

## 🔄 Pillow Compatibility

Puhu is designed as a drop-in replacement for Pillow. Most Pillow code should work with minimal changes:

```python
# Pillow code
from PIL import Image
img = Image.open("photo.jpg")
img = img.resize((800, 600))
img.save("resized.jpg")

# Puhu equivalent
from puhu import Image
img = Image.open("photo.jpg")
img = img.resize((800, 600))
img.save("resized.jpg")
```

### Compatibility Notes

**Fully Compatible:**
- Basic operations: `open()`, `new()`, `save()`, `resize()`, `crop()`, `rotate()`, `transpose()`
- Properties: `size`, `width`, `height`, `mode`, `format`
- Mode conversion: `convert()`
- Channel operations: `split()`
- Compositing: `paste()`
- NumPy integration: `fromarray()`

**Puhu Extensions:**
- Advanced filters: `blur()`, `sharpen()`, `edge_detect()`, `emboss()`
- CSS-style filters: `sepia()`, `grayscale_filter()`, `invert()`, `hue_rotate()`, `saturate()`
- Pixel operations: `getpixel()`, `putpixel()`, `histogram()`, `dominant_color()`, `average_color()`
- Drawing operations: `draw_rectangle()`, `draw_circle()`, `draw_line()`, `draw_text()`
- Shadow effects: `drop_shadow()`, `glow()`, `inner_shadow()`
- Color manipulation: `replace_color()`, `threshold()`, `posterize()`

**Not Yet Implemented:**
- `frombytes()`, `tobytes()` (use `to_bytes()` instead)
- Advanced text rendering with font support
- Some specialized image modes (CMYK, YCbCr, HSV)
- Arbitrary angle rotation (only 90° increments)
- Some advanced Pillow features

## 📝 Type Hints

Puhu includes comprehensive type hints for better IDE support:

```python
from typing import Tuple, Union, Optional, List
from pathlib import Path
import numpy as np

def open(fp: Union[str, Path, bytes], 
         mode: Optional[str] = None, 
         formats: Optional[List[str]] = None) -> Image: ...

def new(mode: str, 
        size: Tuple[int, int], 
        color: Union[int, Tuple[int, ...], str] = 0) -> Image: ...

def fromarray(obj: np.ndarray, 
              mode: Optional[str] = None) -> Image: ...
```

## 🔗 See Also

- **[Quick Start](quickstart.md)** - Get started quickly
- **[Basic Usage](basic-usage.md)** - Core concepts and patterns
- **[Examples](examples.md)** - Real-world usage examples
- **[Performance Guide](performance.md)** - Optimization techniques
- **[Migration Guide](migration.md)** - Migrating from Pillow