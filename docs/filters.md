# Image Filters

Complete reference for all image filters and effects available in Puhu.

## 🎨 Basic Filters

### Blur

#### `Image.blur(radius)` / `puhu.blur(image, radius)`

Apply Gaussian blur to the image.

**Parameters:**
- `radius` (float): Blur radius (0.0 = no blur, higher values = more blur)

**Returns:** New blurred `Image` instance

**Examples:**

```python
import puhu

img = puhu.open("photo.jpg")

# Light blur
light_blur = img.blur(1.0)

# Medium blur
medium_blur = img.blur(3.0)

# Heavy blur
heavy_blur = img.blur(8.0)

# Functional API
blurred_func = puhu.blur(img, 2.5)

# Progressive blur levels
blur_levels = [0.5, 1.0, 2.0, 5.0, 10.0]
for i, radius in enumerate(blur_levels):
    blurred = img.blur(radius)
    blurred.save(f"blur_radius_{radius}.png")

# Selective blur (blur background, keep foreground sharp)
def selective_blur(img, mask_threshold=128):
    """Apply blur selectively based on brightness."""
    gray = img.convert("L")
    
    # Create mask based on brightness
    bright_areas = gray.threshold(mask_threshold)
    
    # Apply different blur levels
    light_blur = img.blur(0.5)
    heavy_blur = img.blur(3.0)
    
    # Note: Advanced masking would require additional compositing
    return heavy_blur  # Simplified example
```

**Use Cases:**
- Background blur effects
- Noise reduction
- Soft focus photography
- Motion blur simulation
- Preparing images for edge detection

### Sharpen

#### `Image.sharpen(strength)` / `puhu.sharpen(image, strength)`

Apply sharpening filter to enhance image details.

**Parameters:**
- `strength` (float): Sharpening strength (1.0 = normal, higher = more sharpening)

**Returns:** New sharpened `Image` instance

**Examples:**

```python
img = puhu.open("photo.jpg")

# Light sharpening
light_sharp = img.sharpen(1.2)

# Medium sharpening
medium_sharp = img.sharpen(1.5)

# Heavy sharpening
heavy_sharp = img.sharpen(2.5)

# Functional API
sharpened_func = puhu.sharpen(img, 1.8)

# Progressive sharpening
sharpen_levels = [0.5, 1.0, 1.5, 2.0, 3.0]
for strength in sharpen_levels:
    sharpened = img.sharpen(strength)
    sharpened.save(f"sharpen_strength_{strength}.png")

# Unsharp mask effect (blur then sharpen)
def unsharp_mask(img, blur_radius=1.0, sharpen_strength=2.0):
    """Apply unsharp mask sharpening technique."""
    return img.blur(blur_radius).sharpen(sharpen_strength)

enhanced = unsharp_mask(img, 0.8, 1.8)
```

**Use Cases:**
- Enhancing photo details
- Correcting soft focus
- Preparing images for printing
- Enhancing text readability
- Post-processing after resizing

### Edge Detection

#### `Image.edge_detect()` / `puhu.edge_detect(image)`

Detect edges in the image using Sobel operator.

**Returns:** New `Image` instance with edges highlighted

**Examples:**

```python
img = puhu.open("photo.jpg")

# Basic edge detection
edges = img.edge_detect()

# Functional API
edges_func = puhu.edge_detect(img)

# Edge detection on different image types
test_images = ["geometric.png", "text_sample.png", "colorful_squares.png"]
for image_path in test_images:
    img = puhu.open(image_path)
    edges = img.edge_detect()
    edges.save(f"edges_{Path(image_path).stem}.png")

# Combine with other filters for artistic effects
artistic_edges = (img.blur(0.5)
                     .edge_detect()
                     .contrast(1.5)
                     .brightness(20))

# Edge-enhanced image (blend original with edges)
def edge_enhance(img, edge_strength=0.3):
    """Enhance image by blending with edge detection."""
    edges = img.edge_detect()
    # Note: This is a simplified version
    # Full implementation would require proper blending
    return img.sharpen(1.0 + edge_strength)

enhanced = edge_enhance(img, 0.5)
```

**Use Cases:**
- Object boundary detection
- Artistic line art effects
- Image analysis and computer vision
- Preparing images for further processing
- Creating coloring book style images

### Emboss

#### `Image.emboss()` / `puhu.emboss(image)`

Apply emboss effect to create a raised, 3D appearance.

**Returns:** New `Image` instance with emboss effect

**Examples:**

```python
img = puhu.open("photo.jpg")

# Basic emboss
embossed = img.emboss()

# Functional API
embossed_func = puhu.emboss(img)

# Emboss different image types
test_images = ["geometric.png", "text_sample.png", "colorful_squares.png"]
for image_path in test_images:
    img = puhu.open(image_path)
    embossed = img.emboss()
    embossed.save(f"emboss_{Path(image_path).stem}.png")

# Combine emboss with color adjustments
artistic_emboss = (img.emboss()
                      .brightness(30)
                      .contrast(1.3)
                      .sepia(0.3))

# Subtle emboss effect
def subtle_emboss(img, blend_factor=0.5):
    """Apply subtle emboss by blending with original."""
    embossed = img.emboss()
    # Note: This is conceptual - full blending would require additional methods
    return embossed.brightness(int(50 * blend_factor))

subtle = subtle_emboss(img, 0.3)
```

**Use Cases:**
- Creating 3D text effects
- Artistic photo effects
- Texture enhancement
- Vintage photo styling
- Preparing images for engraving simulation

## 🌈 Color Adjustment Filters

### Brightness

#### `Image.brightness(adjustment)` / `puhu.brightness(image, adjustment)`

Adjust image brightness.

**Parameters:**
- `adjustment` (int): Brightness adjustment (-255 to +255, 0 = no change)

**Returns:** New `Image` instance with adjusted brightness

**Examples:**

```python
img = puhu.open("photo.jpg")

# Brighten image
brighter = img.brightness(50)
much_brighter = img.brightness(100)

# Darken image
darker = img.brightness(-30)
much_darker = img.brightness(-80)

# Functional API
bright_func = puhu.brightness(img, 40)

# Progressive brightness adjustment
brightness_levels = [-100, -50, 0, 50, 100]
for level in brightness_levels:
    adjusted = img.brightness(level)
    sign = "+" if level >= 0 else ""
    adjusted.save(f"brightness_{sign}{level}.png")

# Auto-brightness adjustment based on image analysis
def auto_brightness(img):
    """Automatically adjust brightness based on average color."""
    avg_color = img.average_color()
    if len(avg_color) >= 3:
        avg_luminance = sum(avg_color[:3]) / 3
        if avg_luminance < 100:
            return img.brightness(50)  # Brighten dark images
        elif avg_luminance > 180:
            return img.brightness(-30)  # Darken bright images
    return img

auto_adjusted = auto_brightness(img)
```

**Use Cases:**
- Correcting underexposed photos
- Creating mood effects
- Preparing images for different display conditions
- Artistic effects
- Batch photo correction

### Contrast

#### `Image.contrast(factor)` / `puhu.contrast(image, factor)`

Adjust image contrast.

**Parameters:**
- `factor` (float): Contrast factor (1.0 = no change, >1.0 = more contrast, <1.0 = less contrast)

**Returns:** New `Image` instance with adjusted contrast

**Examples:**

```python
img = puhu.open("photo.jpg")

# Increase contrast
high_contrast = img.contrast(1.5)
very_high_contrast = img.contrast(2.0)

# Decrease contrast
low_contrast = img.contrast(0.7)
very_low_contrast = img.contrast(0.5)

# Functional API
contrast_func = puhu.contrast(img, 1.3)

# Progressive contrast adjustment
contrast_levels = [0.5, 0.8, 1.0, 1.5, 2.0]
for level in contrast_levels:
    adjusted = img.contrast(level)
    adjusted.save(f"contrast_{level}.png")

# Combine brightness and contrast
def enhance_photo(img, brightness_adj=10, contrast_factor=1.1):
    """Apply standard photo enhancement."""
    return img.brightness(brightness_adj).contrast(contrast_factor)

enhanced = enhance_photo(img, 20, 1.2)

# Adaptive contrast enhancement
def adaptive_contrast(img):
    """Apply contrast based on image characteristics."""
    # Analyze image histogram (conceptual)
    avg_color = img.average_color()
    if len(avg_color) >= 3:
        color_range = max(avg_color[:3]) - min(avg_color[:3])
        if color_range < 100:  # Low contrast image
            return img.contrast(1.5)
        elif color_range > 200:  # High contrast image
            return img.contrast(0.9)
    return img.contrast(1.1)  # Default enhancement

adaptive = adaptive_contrast(img)
```

**Use Cases:**
- Enhancing flat, dull images
- Creating dramatic effects
- Correcting overexposed photos
- Artistic styling
- Preparing images for printing

## 🎭 CSS-Style Filters

### Sepia

#### `Image.sepia(amount)` / `puhu.sepia(image, amount)`

Apply sepia tone effect for vintage appearance.

**Parameters:**
- `amount` (float): Sepia intensity (0.0 = no effect, 1.0 = full sepia)

**Returns:** New `Image` instance with sepia effect

**Examples:**

```python
img = puhu.open("photo.jpg")

# Light sepia
light_sepia = img.sepia(0.3)

# Medium sepia
medium_sepia = img.sepia(0.6)

# Full sepia
full_sepia = img.sepia(1.0)

# Functional API
sepia_func = puhu.sepia(img, 0.8)

# Progressive sepia levels
sepia_levels = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
for level in sepia_levels:
    sepia_img = img.sepia(level)
    sepia_img.save(f"sepia_{level}.png")

# Vintage photo effect
def vintage_effect(img):
    """Create vintage photo effect."""
    return (img.sepia(0.8)
              .contrast(0.9)
              .brightness(-10)
              .blur(0.3))

vintage = vintage_effect(img)
```

**Use Cases:**
- Vintage photo effects
- Artistic styling
- Wedding photography
- Historical document styling
- Nostalgic mood creation

### Grayscale Filter

#### `Image.grayscale_filter(amount)` / `puhu.grayscale_filter(image, amount)`

Convert to grayscale with amount control.

**Parameters:**
- `amount` (float): Grayscale intensity (0.0 = no effect, 1.0 = full grayscale)

**Returns:** New `Image` instance with grayscale effect

**Examples:**

```python
img = puhu.open("photo.jpg")

# Partial grayscale
partial_gray = img.grayscale_filter(0.5)

# Full grayscale
full_gray = img.grayscale_filter(1.0)

# Functional API
gray_func = puhu.grayscale_filter(img, 0.7)

# Note: This is different from convert("L") which completely converts the mode
# grayscale_filter() maintains RGB mode but desaturates colors

# Progressive desaturation
gray_levels = [0.0, 0.25, 0.5, 0.75, 1.0]
for level in gray_levels:
    gray_img = img.grayscale_filter(level)
    gray_img.save(f"grayscale_{level}.png")

# Selective color effect (keep one color, desaturate others)
def selective_color_effect(img, preserve_amount=0.3):
    """Create selective color effect."""
    return img.grayscale_filter(0.8).saturate(1.0 + preserve_amount)

selective = selective_color_effect(img)
```

### Color Inversion

#### `Image.invert(amount)` / `puhu.invert(image, amount)`

Invert image colors for negative effect.

**Parameters:**
- `amount` (float): Inversion intensity (0.0 = no effect, 1.0 = full inversion)

**Returns:** New `Image` instance with inverted colors

**Examples:**

```python
img = puhu.open("photo.jpg")

# Partial inversion
partial_invert = img.invert(0.5)

# Full inversion (negative effect)
full_invert = img.invert(1.0)

# Functional API
invert_func = puhu.invert(img, 0.8)

# Progressive inversion
invert_levels = [0.0, 0.3, 0.6, 1.0]
for level in invert_levels:
    inverted = img.invert(level)
    inverted.save(f"invert_{level}.png")

# Artistic negative effect
def artistic_negative(img):
    """Create artistic negative effect."""
    return (img.invert(1.0)
              .contrast(1.2)
              .brightness(20))

negative_art = artistic_negative(img)

# High contrast negative
def high_contrast_negative(img):
    """Create high contrast negative effect."""
    return (img.contrast(1.8)
              .invert(1.0)
              .sharpen(1.2))

hc_negative = high_contrast_negative(img)
```

**Use Cases:**
- Artistic effects
- Film negative simulation
- High contrast designs
- X-ray style effects
- Creative photography

### Hue Rotation

#### `Image.hue_rotate(degrees)` / `puhu.hue_rotate(image, degrees)`

Rotate the hue of all colors in the image.

**Parameters:**
- `degrees` (float): Hue rotation in degrees (0-360)

**Returns:** New `Image` instance with rotated hues

**Examples:**

```python
img = puhu.open("photo.jpg")

# Rotate hue by 90 degrees
hue_90 = img.hue_rotate(90)

# Rotate hue by 180 degrees (complementary colors)
hue_180 = img.hue_rotate(180)

# Rotate hue by 270 degrees
hue_270 = img.hue_rotate(270)

# Functional API
hue_func = puhu.hue_rotate(img, 120)

# Progressive hue rotation
hue_angles = [0, 60, 120, 180, 240, 300]
for angle in hue_angles:
    hue_rotated = img.hue_rotate(angle)
    hue_rotated.save(f"hue_rotate_{angle}.png")

# Color theme variations
def create_color_themes(img):
    """Create different color theme variations."""
    themes = {
        "original": img,
        "warm": img.hue_rotate(30),
        "cool": img.hue_rotate(210),
        "complementary": img.hue_rotate(180),
        "triadic_1": img.hue_rotate(120),
        "triadic_2": img.hue_rotate(240),
    }
    return themes

themes = create_color_themes(img)
for name, themed_img in themes.items():
    themed_img.save(f"theme_{name}.png")
```

**Use Cases:**
- Color theme variations
- Artistic color effects
- Mood adjustment
- Brand color adaptation
- Creative photography

### Saturation

#### `Image.saturate(factor)` / `puhu.saturate(image, factor)`

Adjust color saturation.

**Parameters:**
- `factor` (float): Saturation factor (1.0 = no change, >1.0 = more saturated, <1.0 = less saturated)

**Returns:** New `Image` instance with adjusted saturation

**Examples:**

```python
img = puhu.open("photo.jpg")

# Increase saturation
vibrant = img.saturate(1.5)
very_vibrant = img.saturate(2.0)

# Decrease saturation
muted = img.saturate(0.7)
very_muted = img.saturate(0.3)

# Functional API
saturated_func = puhu.saturate(img, 1.3)

# Progressive saturation
saturation_levels = [0.0, 0.5, 1.0, 1.5, 2.0]
for level in saturation_levels:
    saturated = img.saturate(level)
    saturated.save(f"saturate_{level}.png")

# Instagram-style filters using saturation
def instagram_vibrant(img):
    """Create vibrant Instagram-style effect."""
    return (img.saturate(1.4)
              .contrast(1.1)
              .brightness(10))

def instagram_muted(img):
    """Create muted Instagram-style effect."""
    return (img.saturate(0.8)
              .brightness(15)
              .contrast(0.95))

vibrant_style = instagram_vibrant(img)
muted_style = instagram_muted(img)
```

**Use Cases:**
- Enhancing color photos
- Creating mood effects
- Social media filters
- Artistic styling
- Brand-consistent imagery

## 🎨 Filter Combinations and Chains

### Chaining Filters

```python
img = puhu.open("photo.jpg")

# Simple chain
result = img.blur(1.0).sharpen(1.5).brightness(20)

# Complex artistic effect
artistic = (img.blur(0.8)
              .sharpen(2.0)
              .brightness(15)
              .contrast(1.3)
              .sepia(0.3)
              .saturate(1.1))

# Vintage effect chain
vintage = (img.sepia(0.8)
             .contrast(0.9)
             .brightness(-10)
             .blur(0.5)
             .saturate(0.8))

# High contrast dramatic effect
dramatic = (img.contrast(1.8)
              .saturate(1.5)
              .sharpen(1.2)
              .brightness(10))

# Soft focus portrait effect
soft_portrait = (img.blur(0.8)
                   .brightness(10)
                   .contrast(0.9)
                   .saturate(1.1))
```

### Predefined Filter Styles

```python
def apply_filter_style(img, style_name):
    """Apply predefined filter styles."""
    styles = {
        "vintage": lambda x: x.sepia(0.8).contrast(0.9).brightness(-10),
        "dramatic": lambda x: x.contrast(1.8).saturate(1.5).sharpen(1.2),
        "soft_focus": lambda x: x.blur(0.8).brightness(10).contrast(0.8),
        "high_detail": lambda x: x.sharpen(1.5).contrast(1.2).saturate(1.1),
        "artistic": lambda x: x.blur(1.0).sharpen(2.0).brightness(20).contrast(1.3),
        "black_white": lambda x: x.grayscale_filter(1.0).contrast(1.2),
        "warm_tone": lambda x: x.hue_rotate(15).saturate(1.2).brightness(5),
        "cool_tone": lambda x: x.hue_rotate(200).saturate(1.1).brightness(-5),
    }
    
    if style_name not in styles:
        raise ValueError(f"Unknown style: {style_name}")
    
    return styles[style_name](img)

# Apply different styles
styles = ["vintage", "dramatic", "soft_focus", "high_detail", "artistic"]
for style in styles:
    styled = apply_filter_style(img, style)
    styled.save(f"filter_chain_{style}.png")
```

### Custom Filter Combinations

```python
def create_custom_filter(blur_radius=1.0, sharpen_strength=1.5, 
                        brightness_adj=20, contrast_factor=1.3,
                        sepia_amount=0.0, saturation_factor=1.0):
    """Create custom filter function."""
    def apply_filter(img):
        result = img
        if blur_radius > 0:
            result = result.blur(blur_radius)
        if sharpen_strength != 1.0:
            result = result.sharpen(sharpen_strength)
        if brightness_adj != 0:
            result = result.brightness(brightness_adj)
        if contrast_factor != 1.0:
            result = result.contrast(contrast_factor)
        if sepia_amount > 0:
            result = result.sepia(sepia_amount)
        if saturation_factor != 1.0:
            result = result.saturate(saturation_factor)
        return result
    
    return apply_filter

# Create custom filters
portrait_filter = create_custom_filter(
    blur_radius=0.5, brightness_adj=10, contrast_factor=1.1, saturation_factor=1.2
)

landscape_filter = create_custom_filter(
    sharpen_strength=1.3, contrast_factor=1.2, saturation_factor=1.4
)

vintage_filter = create_custom_filter(
    sepia_amount=0.7, contrast_factor=0.9, brightness_adj=-5
)

# Apply custom filters
portrait_result = portrait_filter(img)
landscape_result = landscape_filter(img)
vintage_result = vintage_filter(img)
```

## 🔧 Functional API

All filters are available as both methods and functions:

```python
import puhu

img = puhu.open("photo.jpg")

# Method chaining (object-oriented)
result1 = img.blur(2.0).sharpen(1.5).brightness(20)

# Functional API
blurred = puhu.blur(img, 2.0)
sharpened = puhu.sharpen(blurred, 1.5)
result2 = puhu.brightness(sharpened, 20)

# Functional composition
from functools import reduce

filters = [
    lambda x: puhu.blur(x, 1.0),
    lambda x: puhu.sharpen(x, 1.5),
    lambda x: puhu.brightness(x, 20),
    lambda x: puhu.contrast(x, 1.3),
]

result3 = reduce(lambda img, f: f(img), filters, img)

# Pipeline function
def create_filter_pipeline(*filter_funcs):
    """Create a filter pipeline from functions."""
    def apply_pipeline(img):
        return reduce(lambda result, func: func(result), filter_funcs, img)
    return apply_pipeline

# Usage
pipeline = create_filter_pipeline(
    lambda x: puhu.blur(x, 1.0),
    lambda x: puhu.sharpen(x, 1.5),
    lambda x: puhu.brightness(x, 20),
)

result4 = pipeline(img)
```

## 📊 Performance Considerations

### Filter Optimization

```python
# Efficient: Chain operations to minimize memory allocation
efficient = img.blur(1.0).sharpen(1.5).brightness(20).contrast(1.3)

# Less efficient: Multiple intermediate variables
# temp1 = img.blur(1.0)
# temp2 = temp1.sharpen(1.5)
# temp3 = temp2.brightness(20)
# result = temp3.contrast(1.3)

# Batch processing
def batch_apply_filter(image_paths, filter_func, output_dir):
    """Apply filter to multiple images efficiently."""
    from pathlib import Path
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    for path in image_paths:
        img = puhu.open(path)
        filtered = filter_func(img)
        output_file = output_path / f"filtered_{Path(path).name}"
        filtered.save(output_file)

# Usage
vintage_filter = lambda x: x.sepia(0.8).contrast(0.9).brightness(-10)
batch_apply_filter(["photo1.jpg", "photo2.jpg"], vintage_filter, "output")
```

## 🎯 Filter Use Cases

### Photography Enhancement

```python
def enhance_portrait(img):
    """Enhance portrait photos."""
    return (img.blur(0.3)          # Slight skin smoothing
              .brightness(5)        # Slight brightening
              .contrast(1.05)       # Subtle contrast boost
              .saturate(1.1))       # Enhance skin tones

def enhance_landscape(img):
    """Enhance landscape photos."""
    return (img.sharpen(1.2)       # Enhance details
              .contrast(1.15)       # Increase contrast
              .saturate(1.3)        # Vibrant colors
              .brightness(-5))      # Slight darkening for drama

def enhance_macro(img):
    """Enhance macro photography."""
    return (img.sharpen(1.5)       # Sharp details
              .contrast(1.2)        # High contrast
              .saturate(1.2)        # Rich colors
              .brightness(10))      # Bright and clear
```

### Artistic Effects

```python
def create_oil_painting_effect(img):
    """Simulate oil painting effect."""
    return (img.blur(1.5)
              .sharpen(0.8)
              .contrast(1.3)
              .saturate(1.4))

def create_pencil_sketch_effect(img):
    """Create pencil sketch effect."""
    return (img.edge_detect()
              .invert(1.0)
              .grayscale_filter(1.0)
              .contrast(1.5))

def create_dream_effect(img):
    """Create dreamy, ethereal effect."""
    return (img.blur(2.0)
              .brightness(20)
              .contrast(0.8)
              .saturate(1.2)
              .sepia(0.2))
```

### Social Media Filters

```python
def instagram_valencia(img):
    """Valencia-style Instagram filter."""
    return (img.contrast(1.1)
              .brightness(10)
              .saturate(1.2)
              .sepia(0.1))

def instagram_nashville(img):
    """Nashville-style Instagram filter."""
    return (img.sepia(0.2)
              .contrast(1.2)
              .brightness(5)
              .saturate(1.3))

def instagram_kelvin(img):
    """Kelvin-style Instagram filter."""
    return (img.hue_rotate(15)
              .saturate(1.5)
              .contrast(1.1)
              .brightness(10))
```

## 🔗 Next Steps

- **[CSS Filters](css-filters.md)** - Advanced CSS-style filter effects
- **[Pixel Manipulation](pixel-manipulation.md)** - Direct pixel operations
- **[Drawing Operations](drawing.md)** - Shape and text drawing
- **[Shadow Effects](shadows.md)** - Drop shadows and glow effects
- **[Examples](examples.md)** - Real-world filter usage examples