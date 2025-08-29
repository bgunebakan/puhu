# Pixel Manipulation

Direct pixel access, analysis, and manipulation operations in Puhu.

## 🎯 Overview

Puhu provides comprehensive pixel-level operations for fine-grained image manipulation, color analysis, and custom effects. These operations allow you to work directly with individual pixels or analyze image characteristics at the pixel level.

## 🔍 Direct Pixel Access

### Getting Pixel Values

#### `Image.getpixel(x, y)`

Get the color value of a pixel at specific coordinates.

**Parameters:**
- `x` (int): X coordinate (0 to width-1)
- `y` (int): Y coordinate (0 to height-1)

**Returns:** Pixel color as tuple (depends on image mode)
- RGB mode: `(r, g, b)`
- RGBA mode: `(r, g, b, a)`
- Grayscale mode: `(gray,)` or single value

**Examples:**

```python
import puhu

img = puhu.open("photo.jpg")

# Get pixel at specific coordinates
pixel = img.getpixel(100, 100)
print(f"Pixel at (100, 100): {pixel}")

# Get pixels from different image modes
rgb_img = img.convert("RGB")
rgba_img = img.convert("RGBA")
gray_img = img.convert("L")

rgb_pixel = rgb_img.getpixel(50, 50)    # (r, g, b)
rgba_pixel = rgba_img.getpixel(50, 50)  # (r, g, b, a)
gray_pixel = gray_img.getpixel(50, 50)  # (gray,) or single value

# Sample pixels from different regions
def sample_pixels(img, num_samples=10):
    """Sample random pixels from the image."""
    import random
    
    width, height = img.size
    samples = []
    
    for _ in range(num_samples):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        pixel = img.getpixel(x, y)
        samples.append(((x, y), pixel))
    
    return samples

samples = sample_pixels(img, 5)
for (x, y), pixel in samples:
    print(f"Pixel at ({x}, {y}): {pixel}")

# Get pixels along a line
def get_line_pixels(img, start, end):
    """Get pixel values along a line."""
    x1, y1 = start
    x2, y2 = end
    
    # Simple line sampling (Bresenham's algorithm would be more accurate)
    steps = max(abs(x2 - x1), abs(y2 - y1))
    pixels = []
    
    for i in range(steps + 1):
        t = i / steps if steps > 0 else 0
        x = int(x1 + t * (x2 - x1))
        y = int(y1 + t * (y2 - y1))
        
        if 0 <= x < img.width and 0 <= y < img.height:
            pixel = img.getpixel(x, y)
            pixels.append(((x, y), pixel))
    
    return pixels

line_pixels = get_line_pixels(img, (0, 0), (100, 100))
```

### Setting Pixel Values

#### `Image.putpixel(x, y, color)`

Set the color value of a pixel at specific coordinates.

**Parameters:**
- `x` (int): X coordinate
- `y` (int): Y coordinate  
- `color` (tuple): Color value (must match image mode)

**Returns:** New `Image` instance with modified pixel

**Examples:**

```python
img = puhu.open("photo.jpg")

# Set a single pixel to red
red_dot = img.putpixel(100, 100, (255, 0, 0, 255))

# Draw a simple pattern
def draw_cross(img, center_x, center_y, size, color):
    """Draw a cross pattern using putpixel."""
    result = img
    
    # Horizontal line
    for i in range(-size, size + 1):
        x = center_x + i
        if 0 <= x < img.width:
            result = result.putpixel(x, center_y, color)
    
    # Vertical line
    for i in range(-size, size + 1):
        y = center_y + i
        if 0 <= y < img.height:
            result = result.putpixel(center_x, y, color)
    
    return result

marked = draw_cross(img, 200, 150, 10, (255, 0, 0, 255))

# Create a gradient using putpixel
def create_gradient_putpixel(width, height, start_color, end_color):
    """Create a gradient using individual pixel operations."""
    img = puhu.new("RGB", (width, height))
    
    for x in range(width):
        # Calculate interpolation factor
        t = x / (width - 1) if width > 1 else 0
        
        # Interpolate colors
        r = int(start_color[0] + t * (end_color[0] - start_color[0]))
        g = int(start_color[1] + t * (end_color[1] - start_color[1]))
        b = int(start_color[2] + t * (end_color[2] - start_color[2]))
        
        # Set entire column to this color
        for y in range(height):
            img = img.putpixel(x, y, (r, g, b, 255))
    
    return img

gradient = create_gradient_putpixel(200, 100, (255, 0, 0), (0, 0, 255))

# Pixel art creation
def create_pixel_art(size, pattern):
    """Create pixel art from a pattern."""
    img = puhu.new("RGB", size, "white")
    
    for y, row in enumerate(pattern):
        for x, color_key in enumerate(row):
            if x < size[0] and y < size[1]:
                colors = {
                    'R': (255, 0, 0, 255),
                    'G': (0, 255, 0, 255),
                    'B': (0, 0, 255, 255),
                    'K': (0, 0, 0, 255),
                    'W': (255, 255, 255, 255),
                }
                if color_key in colors:
                    img = img.putpixel(x, y, colors[color_key])
    
    return img

# Simple smiley face pattern
smiley_pattern = [
    "WWWKKKWWW",
    "WKWWWWWKW",
    "KWWWWWWWK",
    "KWKWWWKWK",
    "KWWWWWWWK",
    "KWKWWWKWK",
    "KWWKKKWWK",
    "WKWWWWWKW",
    "WWWKKKWWW",
]

smiley = create_pixel_art((9, 9), smiley_pattern)
```

## 📊 Color Analysis

### Histogram Analysis

#### `Image.histogram()`

Generate color histograms for image analysis.

**Returns:** Tuple of histograms `(r_hist, g_hist, b_hist, a_hist)`
- Each histogram is a list of 256 values (pixel counts for each intensity level)
- Alpha histogram is None for RGB images

**Examples:**

```python
img = puhu.open("photo.jpg")

# Get color histograms
r_hist, g_hist, b_hist, a_hist = img.histogram()

print(f"Red histogram length: {len(r_hist)}")
print(f"Green histogram length: {len(g_hist)}")
print(f"Blue histogram length: {len(b_hist)}")
print(f"Alpha histogram: {a_hist}")  # None for RGB images

# Analyze histogram data
def analyze_histogram(histogram, channel_name):
    """Analyze a single color channel histogram."""
    total_pixels = sum(histogram)
    
    # Find peak intensity
    peak_intensity = histogram.index(max(histogram))
    peak_count = max(histogram)
    
    # Calculate mean intensity
    weighted_sum = sum(i * count for i, count in enumerate(histogram))
    mean_intensity = weighted_sum / total_pixels if total_pixels > 0 else 0
    
    # Find intensity range
    min_intensity = next(i for i, count in enumerate(histogram) if count > 0)
    max_intensity = next(i for i in range(255, -1, -1) if histogram[i] > 0)
    
    return {
        "channel": channel_name,
        "total_pixels": total_pixels,
        "peak_intensity": peak_intensity,
        "peak_count": peak_count,
        "mean_intensity": mean_intensity,
        "min_intensity": min_intensity,
        "max_intensity": max_intensity,
        "range": max_intensity - min_intensity,
    }

# Analyze each channel
r_analysis = analyze_histogram(r_hist, "Red")
g_analysis = analyze_histogram(g_hist, "Green")
b_analysis = analyze_histogram(b_hist, "Blue")

print(f"Red channel - Mean: {r_analysis['mean_intensity']:.1f}, Peak: {r_analysis['peak_intensity']}")
print(f"Green channel - Mean: {g_analysis['mean_intensity']:.1f}, Peak: {g_analysis['peak_intensity']}")
print(f"Blue channel - Mean: {b_analysis['mean_intensity']:.1f}, Peak: {b_analysis['peak_intensity']}")

# Detect image characteristics from histogram
def detect_image_characteristics(img):
    """Detect image characteristics from histogram analysis."""
    r_hist, g_hist, b_hist, a_hist = img.histogram()
    
    r_analysis = analyze_histogram(r_hist, "Red")
    g_analysis = analyze_histogram(g_hist, "Green")
    b_analysis = analyze_histogram(b_hist, "Blue")
    
    characteristics = []
    
    # Check if image is dark
    avg_mean = (r_analysis['mean_intensity'] + g_analysis['mean_intensity'] + b_analysis['mean_intensity']) / 3
    if avg_mean < 85:
        characteristics.append("dark")
    elif avg_mean > 170:
        characteristics.append("bright")
    
    # Check if image is low contrast
    avg_range = (r_analysis['range'] + g_analysis['range'] + b_analysis['range']) / 3
    if avg_range < 128:
        characteristics.append("low_contrast")
    elif avg_range > 200:
        characteristics.append("high_contrast")
    
    # Check color dominance
    if r_analysis['mean_intensity'] > g_analysis['mean_intensity'] + 20 and r_analysis['mean_intensity'] > b_analysis['mean_intensity'] + 20:
        characteristics.append("red_dominant")
    elif g_analysis['mean_intensity'] > r_analysis['mean_intensity'] + 20 and g_analysis['mean_intensity'] > b_analysis['mean_intensity'] + 20:
        characteristics.append("green_dominant")
    elif b_analysis['mean_intensity'] > r_analysis['mean_intensity'] + 20 and b_analysis['mean_intensity'] > g_analysis['mean_intensity'] + 20:
        characteristics.append("blue_dominant")
    
    return characteristics

characteristics = detect_image_characteristics(img)
print(f"Image characteristics: {characteristics}")
```

### Color Statistics

#### `Image.dominant_color()`

Find the most frequently occurring color in the image.

**Returns:** Color tuple representing the dominant color

**Examples:**

```python
img = puhu.open("photo.jpg")

# Get dominant color
dominant = img.dominant_color()
print(f"Dominant color: {dominant}")

# Create a swatch showing the dominant color
def create_color_swatch(color, size=(100, 100)):
    """Create a color swatch image."""
    return puhu.new("RGB", size, color[:3])  # Use only RGB components

dominant_swatch = create_color_swatch(dominant)
dominant_swatch.save("dominant_color_swatch.png")

# Find multiple dominant colors (conceptual implementation)
def find_top_colors(img, num_colors=5):
    """Find the top N most common colors."""
    # This is a simplified approach - a real implementation would use clustering
    r_hist, g_hist, b_hist, a_hist = img.histogram()
    
    # For demonstration, we'll just return the dominant color multiple times
    # A real implementation would analyze the histogram more thoroughly
    dominant = img.dominant_color()
    
    # Generate variations of the dominant color for demonstration
    colors = [dominant]
    if len(dominant) >= 3:
        r, g, b = dominant[:3]
        variations = [
            (min(255, r + 30), g, b),
            (r, min(255, g + 30), b),
            (r, g, min(255, b + 30)),
            (max(0, r - 30), max(0, g - 30), max(0, b - 30)),
        ]
        colors.extend(variations[:num_colors-1])
    
    return colors[:num_colors]

top_colors = find_top_colors(img, 5)
print(f"Top colors: {top_colors}")

# Create a palette from top colors
def create_color_palette(colors, swatch_size=(50, 50)):
    """Create a color palette image."""
    palette_width = len(colors) * swatch_size[0]
    palette_height = swatch_size[1]
    
    palette = puhu.new("RGB", (palette_width, palette_height), "white")
    
    for i, color in enumerate(colors):
        swatch = puhu.new("RGB", swatch_size, color[:3])
        x_pos = i * swatch_size[0]
        palette = palette.paste(swatch, (x_pos, 0))
    
    return palette

color_palette = create_color_palette(top_colors)
```

#### `Image.average_color()`

Calculate the average color of the entire image.

**Returns:** Color tuple representing the average color

**Examples:**

```python
img = puhu.open("photo.jpg")

# Get average color
average = img.average_color()
print(f"Average color: {average}")

# Create average color swatch
average_swatch = create_color_swatch(average)
average_swatch.save("average_color_swatch.png")

# Compare dominant vs average color
def compare_colors(img):
    """Compare dominant and average colors."""
    dominant = img.dominant_color()
    average = img.average_color()
    
    # Create comparison image
    comparison = puhu.new("RGB", (200, 100), "white")
    
    # Left half: dominant color
    dominant_half = puhu.new("RGB", (100, 100), dominant[:3])
    comparison = comparison.paste(dominant_half, (0, 0))
    
    # Right half: average color
    average_half = puhu.new("RGB", (100, 100), average[:3])
    comparison = comparison.paste(average_half, (100, 0))
    
    return comparison, dominant, average

comparison_img, dom_color, avg_color = compare_colors(img)
comparison_img.save("color_comparison.png")
print(f"Dominant: {dom_color}, Average: {avg_color}")

# Use average color for background
def create_themed_border(img, border_width=20):
    """Create a border using the image's average color."""
    avg_color = img.average_color()
    
    # Create larger canvas with average color background
    new_width = img.width + 2 * border_width
    new_height = img.height + 2 * border_width
    
    bordered = puhu.new("RGB", (new_width, new_height), avg_color[:3])
    bordered = bordered.paste(img, (border_width, border_width))
    
    return bordered

themed_border = create_themed_border(img, 30)
```

## 🎨 Color Manipulation

### Color Replacement

#### `Image.replace_color(target_color, replacement_color, tolerance=0)`

Replace specific colors in the image with new colors.

**Parameters:**
- `target_color` (tuple): Color to replace
- `replacement_color` (tuple): New color
- `tolerance` (int): Color matching tolerance (0-255)

**Returns:** New `Image` instance with replaced colors

**Examples:**

```python
img = puhu.open("photo.jpg")

# Replace exact color match
exact_replace = img.replace_color((255, 0, 0), (0, 255, 0), tolerance=0)

# Replace with tolerance for similar colors
tolerant_replace = img.replace_color((255, 0, 0), (0, 255, 0), tolerance=30)

# Replace multiple colors
def replace_multiple_colors(img, color_map, tolerance=10):
    """Replace multiple colors in sequence."""
    result = img
    for target, replacement in color_map.items():
        result = result.replace_color(target, replacement, tolerance)
    return result

color_replacements = {
    (255, 0, 0): (0, 255, 0),    # Red to Green
    (0, 0, 255): (255, 255, 0),  # Blue to Yellow
    (0, 255, 0): (255, 0, 255),  # Green to Magenta
}

multi_replaced = replace_multiple_colors(img, color_replacements, 20)

# Create color swap effect
def create_color_swap(img, color1, color2, tolerance=15):
    """Swap two colors in the image."""
    # Use a temporary color to avoid conflicts
    temp_color = (128, 128, 128)
    
    # Replace color1 with temp
    temp_img = img.replace_color(color1, temp_color, tolerance)
    
    # Replace color2 with color1
    temp_img = temp_img.replace_color(color2, color1, tolerance)
    
    # Replace temp with color2
    result = temp_img.replace_color(temp_color, color2, tolerance)
    
    return result

swapped = create_color_swap(img, (255, 0, 0), (0, 0, 255), 25)

# Selective color enhancement
def enhance_specific_color(img, target_color, enhancement_factor=1.5, tolerance=20):
    """Enhance (saturate) a specific color range."""
    # This is a conceptual implementation
    # Real implementation would require more sophisticated color space operations
    
    # For demonstration, we'll replace the color with a more saturated version
    if len(target_color) >= 3:
        r, g, b = target_color[:3]
        
        # Increase saturation (simplified)
        enhanced_r = min(255, int(r * enhancement_factor))
        enhanced_g = min(255, int(g * enhancement_factor))
        enhanced_b = min(255, int(b * enhancement_factor))
        
        enhanced_color = (enhanced_r, enhanced_g, enhanced_b)
        return img.replace_color(target_color, enhanced_color, tolerance)
    
    return img

enhanced_reds = enhance_specific_color(img, (200, 50, 50), 1.3, 30)
```

### Thresholding

#### `Image.threshold(threshold_value)`

Convert image to binary (black and white) based on threshold.

**Parameters:**
- `threshold_value` (int): Threshold value (0-255)

**Returns:** New binary `Image` instance

**Examples:**

```python
img = puhu.open("photo.jpg")

# Convert to grayscale first for better thresholding
gray_img = img.convert("L")

# Apply different threshold values
thresholds = [64, 128, 192]
for thresh in thresholds:
    binary = gray_img.threshold(thresh)
    binary.save(f"threshold_{thresh}.png")

# Adaptive thresholding based on image characteristics
def adaptive_threshold(img):
    """Apply adaptive thresholding based on image content."""
    gray_img = img.convert("L")
    
    # Get average brightness
    avg_color = gray_img.average_color()
    avg_brightness = avg_color[0] if isinstance(avg_color, tuple) else avg_color
    
    # Adjust threshold based on average brightness
    if avg_brightness < 85:  # Dark image
        threshold_val = 64
    elif avg_brightness > 170:  # Bright image
        threshold_val = 192
    else:  # Normal image
        threshold_val = 128
    
    return gray_img.threshold(threshold_val)

adaptive_binary = adaptive_threshold(img)

# Create high contrast effect
def high_contrast_threshold(img, threshold=128):
    """Create high contrast black and white effect."""
    gray = img.convert("L")
    binary = gray.threshold(threshold)
    
    # Convert back to RGB for further processing
    return binary.convert("RGB")

high_contrast = high_contrast_threshold(img, 140)

# Text extraction preparation
def prepare_for_ocr(img):
    """Prepare image for OCR by applying optimal thresholding."""
    # Convert to grayscale
    gray = img.convert("L")
    
    # Apply slight blur to reduce noise
    blurred = gray.blur(0.5)
    
    # Apply threshold
    binary = blurred.threshold(128)
    
    # Convert back to RGB
    return binary.convert("RGB")

ocr_ready = prepare_for_ocr(img)
```

### Posterization

#### `Image.posterize(levels)`

Reduce the number of color levels in the image.

**Parameters:**
- `levels` (int): Number of levels per channel (2-8 typically)

**Returns:** New posterized `Image` instance

**Examples:**

```python
img = puhu.open("photo.jpg")

# Apply different posterization levels
levels = [2, 3, 4, 6, 8]
for level in levels:
    posterized = img.posterize(level)
    posterized.save(f"posterize_{level}_levels.png")

# Create pop art effect
def pop_art_effect(img, levels=4):
    """Create pop art style effect using posterization."""
    return (img.posterize(levels)
              .saturate(1.5)
              .contrast(1.3))

pop_art = pop_art_effect(img, 3)

# Combine posterization with color effects
def stylized_poster(img, levels=4, hue_shift=0):
    """Create stylized poster effect."""
    return (img.posterize(levels)
              .hue_rotate(hue_shift)
              .saturate(1.4)
              .contrast(1.2))

# Create multiple poster variations
hue_shifts = [0, 60, 120, 180, 240, 300]
for i, hue in enumerate(hue_shifts):
    poster = stylized_poster(img, 4, hue)
    poster.save(f"stylized_poster_{i}.png")

# Vintage poster effect
def vintage_poster(img, levels=5):
    """Create vintage poster effect."""
    return (img.posterize(levels)
              .sepia(0.3)
              .contrast(1.1)
              .brightness(-10))

vintage = vintage_poster(img, 5)
```

## 🔧 Advanced Pixel Operations

### Custom Pixel Processing

```python
def apply_custom_pixel_function(img, pixel_func):
    """Apply a custom function to each pixel (conceptual)."""
    # Note: This is a conceptual example
    # Real implementation would require iterating through all pixels
    # which would be slow in Python - better done in Rust core
    
    width, height = img.size
    result = img.copy()
    
    # Sample processing on a small area for demonstration
    for x in range(min(50, width)):
        for y in range(min(50, height)):
            pixel = img.getpixel(x, y)
            new_pixel = pixel_func(pixel, x, y)
            result = result.putpixel(x, y, new_pixel)
    
    return result

# Example pixel functions
def invert_pixel(pixel, x, y):
    """Invert a single pixel."""
    if len(pixel) >= 3:
        return (255 - pixel[0], 255 - pixel[1], 255 - pixel[2], pixel[3] if len(pixel) > 3 else 255)
    return pixel

def brighten_pixel(pixel, x, y, amount=50):
    """Brighten a single pixel."""
    if len(pixel) >= 3:
        return (
            min(255, pixel[0] + amount),
            min(255, pixel[1] + amount),
            min(255, pixel[2] + amount),
            pixel[3] if len(pixel) > 3 else 255
        )
    return pixel

def position_based_tint(pixel, x, y):
    """Apply tint based on pixel position."""
    if len(pixel) >= 3:
        # Add red tint based on x position
        red_boost = int((x / 50) * 50) if x < 50 else 50
        return (
            min(255, pixel[0] + red_boost),
            pixel[1],
            pixel[2],
            pixel[3] if len(pixel) > 3 else 255
        )
    return pixel

# Apply custom functions (on small area for demonstration)
inverted_area = apply_custom_pixel_function(img, invert_pixel)
brightened_area = apply_custom_pixel_function(img, lambda p, x, y: brighten_pixel(p, x, y, 30))
tinted_area = apply_custom_pixel_function(img, position_based_tint)
```

### Pixel Pattern Detection

```python
def detect_pixel_patterns(img, pattern_size=(3, 3)):
    """Detect specific pixel patterns in the image."""
    width, height = img.size
    pattern_width, pattern_height = pattern_size
    
    patterns_found = []
    
    # Sample a small area for demonstration
    for x in range(0, min(100, width - pattern_width)):
        for y in range(0, min(100, height - pattern_height)):
            # Extract pattern
            pattern = []
            for py in range(pattern_height):
                row = []
                for px in range(pattern_width):
                    pixel = img.getpixel(x + px, y + py)
                    row.append(pixel)
                pattern.append(row)
            
            # Check for specific patterns (e.g., all same color)
            first_pixel = pattern[0][0]
            if all(pixel == first_pixel for row in pattern for pixel in row):
                patterns_found.append(((x, y), "solid_block", first_pixel))
    
    return patterns_found

patterns = detect_pixel_patterns(img, (2, 2))
print(f"Found {len(patterns)} solid 2x2 blocks")

def find_edge_pixels(img, threshold=30):
    """Find pixels that are likely on edges."""
    width, height = img.size
    edge_pixels = []
    
    # Sample a small area
    for x in range(1, min(99, width - 1)):
        for y in range(1, min(99, height - 1)):
            center_pixel = img.getpixel(x, y)
            
            # Check neighboring pixels
            neighbors = [
                img.getpixel(x-1, y),
                img.getpixel(x+1, y),
                img.getpixel(x, y-1),
                img.getpixel(x, y+1),
            ]
            
            # Calculate color difference
            if len(center_pixel) >= 3:
                for neighbor in neighbors:
                    if len(neighbor) >= 3:
                        diff = sum(abs(center_pixel[i] - neighbor[i]) for i in range(3))
                        if diff > threshold:
                            edge_pixels.append((x, y, center_pixel))
                            break
    
    return edge_pixels

edge_pixels = find_edge_pixels(img, 50)
print(f"Found {len(edge_pixels)} edge pixels")
```

### Color Space Analysis

```python
def analyze_color_distribution(img):
    """Analyze the distribution of colors in the image."""
    r_hist, g_hist, b_hist, a_hist = img.histogram()
    
    analysis = {
        "total_pixels": sum(r_hist),
        "color_channels": {
            "red": {
                "mean": sum(i * count for i, count in enumerate(r_hist)) / sum(r_hist),
                "std": 0,  # Simplified - would need proper calculation
                "min": next(i for i, count in enumerate(r_hist) if count > 0),
                "max": next(i for i in range(255, -1, -1) if r_hist[i] > 0),
            },
            "green": {
                "mean": sum(i * count for i, count in enumerate(g_hist)) / sum(g_hist),
                "std": 0,
                "min": next(i for i, count in enumerate(g_hist) if count > 0),
                "max": next(i for i in range(255, -1, -1) if g_hist[i] > 0),
            },
            "blue": {
                "mean": sum(i * count for i, count in enumerate(b_hist)) / sum(b_hist),
                "std": 0,
                "min": next(i for i, count in enumerate(b_hist) if count > 0),
                "max": next(i for i in range(255, -1, -1) if b_hist[i] > 0),
            },
        }
    }
    
    # Calculate overall statistics
    analysis["overall"] = {
        "brightness": (analysis["color_channels"]["red"]["mean"] + 
                      analysis["color_channels"]["green"]["mean"] + 
                      analysis["color_channels"]["blue"]["mean"]) / 3,
        "contrast": (analysis["color_channels"]["red"]["max"] - analysis["color_channels"]["red"]["min"] +
                    analysis["color_channels"]["green"]["max"] - analysis["color_channels"]["green"]["min"] +
                    analysis["color_channels"]["blue"]["max"] - analysis["color_channels"]["blue"]["min"]) / 3,
    }
    
    return analysis

color_analysis = analyze_color_distribution(img)
print(f"Overall brightness: {color_analysis['overall']['brightness']:.1f}")
print(f"Overall contrast: {color_analysis['overall']['contrast']:.1f}")

def suggest_adjustments(analysis):
    """Suggest image adjustments based on color analysis."""
    suggestions = []
    
    brightness = analysis["overall"]["brightness"]
    contrast = analysis["overall"]["contrast"]
    
    if brightness < 85:
        suggestions.append(("brightness", 30, "Image appears dark, consider brightening"))
    elif brightness > 170:
        suggestions.append(("brightness", -20, "Image appears bright, consider darkening"))
    
    if contrast < 100:
        suggestions.append(("contrast", 1.3, "Image appears low contrast, consider increasing contrast"))
    elif contrast > 200:
        suggestions.append(("contrast", 0.8, "Image appears high contrast, consider reducing contrast"))
    
    # Check color balance
    red_mean = analysis["color_channels"]["red"]["mean"]
    green_mean = analysis["color_channels"]["green"]["mean"]
    blue_mean = analysis["color_channels"]["blue"]["mean"]
    
    if red_mean > green_mean + 30 and red_mean > blue_mean + 30:
        suggestions.append(("hue_rotate", 180, "Image has red color cast, consider adjusting hue"))
    elif blue_mean > red_mean + 30 and blue_mean > green_mean + 30:
        suggestions.append(("hue_rotate", 60, "Image has blue color cast, consider adjusting hue"))
    
    return suggestions

suggestions = suggest_adjustments(color_analysis)
for adjustment_type, value, description in suggestions:
    print(f"Suggestion: {description} (apply {adjustment_type} with value {value})")
```

## 🎯 Practical Applications

### Image Quality Assessment

```python
def assess_image_quality(img):
    """Assess various aspects of image quality."""
    analysis = analyze_color_distribution(img)
    characteristics = detect_image_characteristics(img)
    
    quality_score = 100  # Start with perfect score
    issues = []
    
    # Check brightness
    brightness = analysis["overall"]["brightness"]
    if brightness < 50:
        quality_score -= 20
        issues.append("Very dark image")
    elif brightness < 85:
        quality_score -= 10
        issues.append("Dark image")
    elif brightness > 200:
        quality_score -= 15
        issues.append("Overexposed image")
    
    # Check contrast
    contrast = analysis["overall"]["contrast"]
    if contrast < 80:
        quality_score -= 25
        issues.append("Very low contrast")
    elif contrast < 120:
        quality_score -= 10
        issues.append("Low contrast")
    
    # Check for color casts
    if "red_dominant" in characteristics:
        quality_score -= 5
        issues.append("Red color cast")
    elif "blue_dominant" in characteristics:
        quality_score -= 5
        issues.append("Blue color cast")
    
    return {
        "quality_score": max(0, quality_score),
        "issues": issues,
        "characteristics": characteristics,
        "analysis": analysis,
    }

quality_report = assess_image_quality(img)
print(f"Image quality score: {quality_report['quality_score']}/100")
print(f"Issues found: {quality_report['issues']}")
```

### Batch Pixel Analysis

```python
def batch_analyze_images(image_paths):
    """Analyze multiple images for pixel-level characteristics."""
    results = {}
    
    for path in image_paths:
        try:
            img = puhu.open(path)
            
            # Get basic statistics
            dominant = img.dominant_color()
            average = img.average_color()
            quality = assess_image_quality(img)
            
            results[path] = {
                "size": img.size,
                "mode": img.mode,
                "dominant_color": dominant,
                "average_color": average,
                "quality_score": quality["quality_score"],
                "issues": quality["issues"],
            }
            
        except Exception as e:
            results[path] = {"error": str(e)}
    
    return results

# Example usage
image_files = ["photo1.jpg", "photo2.jpg", "photo3.jpg"]
batch_results = batch_analyze_images(image_files)

for path, result in batch_results.items():
    if "error" not in result:
        print(f"{path}: Quality {result['quality_score']}/100, Dominant color: {result['dominant_color']}")
    else:
        print(f"{path}: Error - {result['error']}")
```

## 🔗 Next Steps

- **[Drawing Operations](drawing.md)** - Shape and text drawing
- **[Shadow Effects](shadows.md)** - Drop shadows and glow effects
- **[Compositing & Blending](compositing.md)** - Advanced image compositing
- **[Performance Guide](performance.md)** - Optimization techniques
- **[Examples](examples.md)** - Real-world pixel manipulation examples