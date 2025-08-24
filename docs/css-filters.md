# CSS-Style Filters

Advanced CSS-like filter effects that provide web-standard image processing capabilities.

## 🎨 Overview

Puhu's CSS-style filters are designed to match the behavior of CSS filter functions, making it easy to apply web-standard effects to images programmatically. These filters can be chained together and provide precise control over visual effects.

## 🌈 Color Filters

### Grayscale

#### `Image.grayscale_filter(amount)`

Convert image to grayscale with controllable intensity.

**Parameters:**
- `amount` (float): Grayscale intensity (0.0 = no effect, 1.0 = full grayscale)

**CSS Equivalent:** `filter: grayscale(amount)`

**Examples:**

```python
import puhu

img = puhu.open("colorful_photo.jpg")

# No grayscale (original colors)
original = img.grayscale_filter(0.0)

# Partial grayscale (desaturated)
partial = img.grayscale_filter(0.5)

# Full grayscale (black and white)
bw = img.grayscale_filter(1.0)

# Progressive grayscale levels
levels = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
for level in levels:
    result = img.grayscale_filter(level)
    result.save(f"css_grayscale_{level}.png")

# Selective grayscale effect
def selective_grayscale(img, preserve_factor=0.3):
    """Apply grayscale while preserving some color."""
    return (img.grayscale_filter(0.8)
              .saturate(1.0 + preserve_factor))

selective = selective_grayscale(img, 0.4)
```

**Use Cases:**
- Creating black and white photos
- Reducing color distraction
- Vintage effects
- Accessibility improvements
- Artistic styling

### Sepia

#### `Image.sepia(amount)`

Apply sepia tone effect for vintage, warm appearance.

**Parameters:**
- `amount` (float): Sepia intensity (0.0 = no effect, 1.0 = full sepia)

**CSS Equivalent:** `filter: sepia(amount)`

**Examples:**

```python
img = puhu.open("photo.jpg")

# Light sepia tone
light = img.sepia(0.3)

# Medium sepia tone
medium = img.sepia(0.6)

# Full sepia tone
vintage = img.sepia(1.0)

# Progressive sepia levels
levels = [0.0, 0.25, 0.5, 0.75, 1.0]
for level in levels:
    result = img.sepia(level)
    result.save(f"css_sepia_{level}.png")

# Vintage photo effect
def vintage_photo(img):
    """Create authentic vintage photo effect."""
    return (img.sepia(0.8)
              .contrast(0.9)
              .brightness(-10)
              .blur(0.3))

vintage_effect = vintage_photo(img)

# Warm sepia tone
def warm_sepia(img, warmth=0.7):
    """Create warm sepia effect."""
    return (img.sepia(warmth)
              .brightness(5)
              .saturate(1.1))

warm = warm_sepia(img, 0.6)
```

**Use Cases:**
- Vintage photography effects
- Wedding photography
- Historical document styling
- Nostalgic mood creation
- Artistic photo treatments

### Invert

#### `Image.invert(amount)`

Invert image colors to create negative effects.

**Parameters:**
- `amount` (float): Inversion intensity (0.0 = no effect, 1.0 = full inversion)

**CSS Equivalent:** `filter: invert(amount)`

**Examples:**

```python
img = puhu.open("photo.jpg")

# Partial inversion
partial = img.invert(0.5)

# Full inversion (negative)
negative = img.invert(1.0)

# Progressive inversion
levels = [0.0, 0.3, 0.6, 1.0]
for level in levels:
    result = img.invert(level)
    result.save(f"css_invert_{level}.png")

# High contrast negative
def high_contrast_negative(img):
    """Create dramatic negative effect."""
    return (img.invert(1.0)
              .contrast(1.5)
              .brightness(20))

dramatic = high_contrast_negative(img)

# Partial invert for artistic effect
def artistic_invert(img, invert_amount=0.7):
    """Create artistic partial inversion."""
    return (img.invert(invert_amount)
              .contrast(1.2)
              .saturate(1.3))

artistic = artistic_invert(img, 0.6)

# X-ray effect
def xray_effect(img):
    """Create X-ray style effect."""
    return (img.grayscale_filter(1.0)
              .invert(1.0)
              .contrast(1.8)
              .brightness(30))

xray = xray_effect(img)
```

**Use Cases:**
- Artistic negative effects
- High contrast designs
- X-ray style imagery
- Creative photography
- UI dark mode effects

### Hue Rotate

#### `Image.hue_rotate(degrees)`

Rotate the hue of all colors in the image.

**Parameters:**
- `degrees` (float): Hue rotation angle (0-360 degrees)

**CSS Equivalent:** `filter: hue-rotate(degrees)`

**Examples:**

```python
img = puhu.open("colorful_photo.jpg")

# Quarter rotation (90°)
quarter = img.hue_rotate(90)

# Half rotation (180° - complementary colors)
complementary = img.hue_rotate(180)

# Three-quarter rotation (270°)
three_quarter = img.hue_rotate(270)

# Progressive hue rotation
angles = [0, 45, 90, 135, 180, 225, 270, 315]
for angle in angles:
    result = img.hue_rotate(angle)
    result.save(f"css_hue_rotate_{angle}.png")

# Color theme variations
def create_color_themes(img):
    """Generate different color themes."""
    themes = {
        "original": img,
        "warm": img.hue_rotate(30),      # Warmer tones
        "cool": img.hue_rotate(210),     # Cooler tones
        "complementary": img.hue_rotate(180),  # Opposite colors
        "analogous_1": img.hue_rotate(60),     # Adjacent colors
        "analogous_2": img.hue_rotate(300),    # Adjacent colors (other side)
        "triadic_1": img.hue_rotate(120),      # Triadic harmony
        "triadic_2": img.hue_rotate(240),      # Triadic harmony
    }
    return themes

themes = create_color_themes(img)

# Seasonal color adjustments
def seasonal_adjustment(img, season):
    """Adjust colors for seasonal themes."""
    adjustments = {
        "spring": 60,    # Fresh, green tones
        "summer": 30,    # Warm, bright tones
        "autumn": 15,    # Warm, orange tones
        "winter": 240,   # Cool, blue tones
    }
    
    if season not in adjustments:
        return img
    
    return img.hue_rotate(adjustments[season])

spring_img = seasonal_adjustment(img, "spring")
```

**Use Cases:**
- Color theme variations
- Brand color adaptation
- Seasonal adjustments
- Artistic color effects
- Mood enhancement

### Saturate

#### `Image.saturate(factor)`

Adjust color saturation intensity.

**Parameters:**
- `factor` (float): Saturation multiplier (1.0 = no change, >1.0 = more saturated, <1.0 = less saturated)

**CSS Equivalent:** `filter: saturate(factor)`

**Examples:**

```python
img = puhu.open("photo.jpg")

# Desaturated (muted colors)
muted = img.saturate(0.5)

# Normal saturation
normal = img.saturate(1.0)

# Enhanced saturation
vibrant = img.saturate(1.5)

# Highly saturated
very_vibrant = img.saturate(2.0)

# Progressive saturation levels
levels = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5]
for level in levels:
    result = img.saturate(level)
    result.save(f"css_saturate_{level}.png")

# Instagram-style filters
def instagram_vibrant(img):
    """Create vibrant Instagram-style filter."""
    return (img.saturate(1.4)
              .contrast(1.1)
              .brightness(10)
              .sharpen(1.1))

def instagram_muted(img):
    """Create muted Instagram-style filter."""
    return (img.saturate(0.7)
              .brightness(15)
              .contrast(0.95)
              .sepia(0.1))

vibrant_style = instagram_vibrant(img)
muted_style = instagram_muted(img)

# Adaptive saturation based on image content
def adaptive_saturation(img):
    """Adjust saturation based on image characteristics."""
    # Analyze average color to determine current saturation level
    avg_color = img.average_color()
    if len(avg_color) >= 3:
        # Calculate color variance as saturation indicator
        color_variance = max(avg_color[:3]) - min(avg_color[:3])
        
        if color_variance < 50:  # Low saturation image
            return img.saturate(1.5)
        elif color_variance > 150:  # High saturation image
            return img.saturate(0.8)
    
    return img.saturate(1.2)  # Default enhancement

adaptive = adaptive_saturation(img)
```

**Use Cases:**
- Enhancing dull photos
- Creating vibrant social media content
- Mood adjustment
- Brand-consistent imagery
- Artistic color effects

## 🔧 Advanced CSS Filter Combinations

### Multi-Filter Effects

```python
def css_filter_combinations(img):
    """Demonstrate various CSS filter combinations."""
    
    effects = {}
    
    # Vintage effect
    effects["vintage"] = (img.sepia(0.8)
                            .saturate(0.8)
                            .contrast(0.9))
    
    # High contrast B&W
    effects["dramatic_bw"] = (img.grayscale_filter(1.0)
                                .contrast(1.5)
                                .invert(0.1))
    
    # Warm sunset
    effects["warm_sunset"] = (img.hue_rotate(15)
                                .saturate(1.3)
                                .sepia(0.2))
    
    # Cool morning
    effects["cool_morning"] = (img.hue_rotate(200)
                                 .saturate(1.1)
                                 .brightness(5))
    
    # Psychedelic
    effects["psychedelic"] = (img.hue_rotate(180)
                                .saturate(2.0)
                                .contrast(1.3))
    
    # Faded film
    effects["faded_film"] = (img.saturate(0.6)
                               .contrast(0.8)
                               .sepia(0.3)
                               .brightness(10))
    
    return effects

# Apply all combinations
effects = css_filter_combinations(img)
for name, effect_img in effects.items():
    effect_img.save(f"css_combo_{name}.png")
```

### Web-Style Filter Presets

```python
class CSSFilterPresets:
    """Collection of web-inspired filter presets."""
    
    @staticmethod
    def polaroid(img):
        """Polaroid instant photo effect."""
        return (img.sepia(0.3)
                  .saturate(1.2)
                  .contrast(1.1)
                  .brightness(5))
    
    @staticmethod
    def kodachrome(img):
        """Kodachrome film emulation."""
        return (img.saturate(1.4)
                  .contrast(1.2)
                  .hue_rotate(5)
                  .brightness(-5))
    
    @staticmethod
    def cross_process(img):
        """Cross-processing film effect."""
        return (img.hue_rotate(10)
                  .saturate(1.6)
                  .contrast(1.4)
                  .brightness(10))
    
    @staticmethod
    def bleach_bypass(img):
        """Bleach bypass cinema effect."""
        return (img.saturate(0.3)
                  .contrast(1.8)
                  .brightness(15))
    
    @staticmethod
    def cyberpunk(img):
        """Cyberpunk aesthetic."""
        return (img.hue_rotate(280)
                  .saturate(1.8)
                  .contrast(1.5)
                  .invert(0.1))
    
    @staticmethod
    def vaporwave(img):
        """Vaporwave aesthetic."""
        return (img.hue_rotate(300)
                  .saturate(1.5)
                  .sepia(0.2)
                  .brightness(10))

# Apply presets
presets = CSSFilterPresets()
polaroid_img = presets.polaroid(img)
kodachrome_img = presets.kodachrome(img)
cyberpunk_img = presets.cyberpunk(img)
```

### Dynamic Filter Application

```python
def apply_css_filter_sequence(img, filter_sequence):
    """Apply a sequence of CSS filters dynamically."""
    result = img
    
    for filter_name, value in filter_sequence:
        if filter_name == "grayscale":
            result = result.grayscale_filter(value)
        elif filter_name == "sepia":
            result = result.sepia(value)
        elif filter_name == "invert":
            result = result.invert(value)
        elif filter_name == "hue-rotate":
            result = result.hue_rotate(value)
        elif filter_name == "saturate":
            result = result.saturate(value)
        elif filter_name == "brightness":
            result = result.brightness(value)
        elif filter_name == "contrast":
            result = result.contrast(value)
        elif filter_name == "blur":
            result = result.blur(value)
        elif filter_name == "sharpen":
            result = result.sharpen(value)
    
    return result

# Define filter sequences
vintage_sequence = [
    ("sepia", 0.8),
    ("saturate", 0.8),
    ("contrast", 0.9),
    ("brightness", -10),
]

dramatic_sequence = [
    ("contrast", 1.5),
    ("saturate", 1.3),
    ("hue-rotate", 15),
    ("sharpen", 1.2),
]

# Apply sequences
vintage_result = apply_css_filter_sequence(img, vintage_sequence)
dramatic_result = apply_css_filter_sequence(img, dramatic_sequence)
```

## 🎨 Creative CSS Filter Techniques

### Color Grading

```python
def color_grade_cinematic(img, style="warm"):
    """Apply cinematic color grading."""
    
    styles = {
        "warm": {
            "hue_shift": 15,
            "saturation": 1.2,
            "sepia": 0.1,
        },
        "cool": {
            "hue_shift": 200,
            "saturation": 1.1,
            "sepia": 0.0,
        },
        "teal_orange": {
            "hue_shift": 30,
            "saturation": 1.4,
            "sepia": 0.0,
        },
        "desaturated": {
            "hue_shift": 0,
            "saturation": 0.6,
            "sepia": 0.2,
        }
    }
    
    if style not in styles:
        style = "warm"
    
    settings = styles[style]
    
    return (img.hue_rotate(settings["hue_shift"])
              .saturate(settings["saturation"])
              .sepia(settings["sepia"])
              .contrast(1.1))

# Apply different color grades
warm_grade = color_grade_cinematic(img, "warm")
cool_grade = color_grade_cinematic(img, "cool")
teal_orange = color_grade_cinematic(img, "teal_orange")
```

### Mood-Based Filters

```python
def apply_mood_filter(img, mood):
    """Apply filters based on desired mood."""
    
    mood_filters = {
        "happy": lambda x: x.saturate(1.3).brightness(15).hue_rotate(30),
        "sad": lambda x: x.saturate(0.6).grayscale_filter(0.3).brightness(-10),
        "energetic": lambda x: x.saturate(1.8).contrast(1.3).hue_rotate(45),
        "calm": lambda x: x.saturate(0.8).brightness(5).hue_rotate(200),
        "mysterious": lambda x: x.saturate(0.7).contrast(1.4).brightness(-20),
        "romantic": lambda x: x.sepia(0.3).saturate(1.2).brightness(10),
        "nostalgic": lambda x: x.sepia(0.6).saturate(0.9).contrast(0.9),
        "futuristic": lambda x: x.hue_rotate(270).saturate(1.5).contrast(1.2),
    }
    
    if mood not in mood_filters:
        return img
    
    return mood_filters[mood](img)

# Apply mood filters
happy_img = apply_mood_filter(img, "happy")
mysterious_img = apply_mood_filter(img, "mysterious")
nostalgic_img = apply_mood_filter(img, "nostalgic")
```

### Brand Color Adaptation

```python
def adapt_to_brand_colors(img, brand_hue_shift=0, brand_saturation=1.0):
    """Adapt image colors to match brand guidelines."""
    
    # Shift hue to match brand colors
    brand_adapted = img.hue_rotate(brand_hue_shift)
    
    # Adjust saturation to match brand intensity
    brand_adapted = brand_adapted.saturate(brand_saturation)
    
    # Slight contrast boost for brand consistency
    brand_adapted = brand_adapted.contrast(1.05)
    
    return brand_adapted

# Brand color examples
tech_brand = adapt_to_brand_colors(img, brand_hue_shift=240, brand_saturation=1.3)  # Blue tech
eco_brand = adapt_to_brand_colors(img, brand_hue_shift=120, brand_saturation=1.2)   # Green eco
luxury_brand = adapt_to_brand_colors(img, brand_hue_shift=45, brand_saturation=0.8) # Gold luxury
```

## 📱 Social Media Filter Effects

### Instagram-Style Filters

```python
class InstagramFilters:
    """Instagram-inspired filter effects."""
    
    @staticmethod
    def valencia(img):
        """Valencia filter effect."""
        return (img.sepia(0.1)
                  .saturate(1.2)
                  .contrast(1.1)
                  .brightness(10))
    
    @staticmethod
    def nashville(img):
        """Nashville filter effect."""
        return (img.sepia(0.2)
                  .saturate(1.3)
                  .contrast(1.2)
                  .hue_rotate(15))
    
    @staticmethod
    def kelvin(img):
        """Kelvin filter effect."""
        return (img.hue_rotate(15)
                  .saturate(1.5)
                  .contrast(1.1)
                  .brightness(10))
    
    @staticmethod
    def x_pro_ii(img):
        """X-Pro II filter effect."""
        return (img.sepia(0.3)
                  .saturate(1.4)
                  .contrast(1.3)
                  .brightness(-5))
    
    @staticmethod
    def lo_fi(img):
        """Lo-Fi filter effect."""
        return (img.saturate(1.1)
                  .contrast(1.5)
                  .brightness(-10)
                  .sepia(0.1))

# Apply Instagram filters
instagram = InstagramFilters()
valencia_img = instagram.valencia(img)
nashville_img = instagram.nashville(img)
kelvin_img = instagram.kelvin(img)
```

### TikTok-Style Effects

```python
def tiktok_aesthetic_filter(img, style="vibrant"):
    """Apply TikTok-style aesthetic filters."""
    
    if style == "vibrant":
        return (img.saturate(1.6)
                  .contrast(1.2)
                  .brightness(15)
                  .hue_rotate(10))
    
    elif style == "vintage":
        return (img.sepia(0.4)
                  .saturate(0.9)
                  .contrast(0.9)
                  .brightness(-5))
    
    elif style == "neon":
        return (img.saturate(2.0)
                  .contrast(1.4)
                  .hue_rotate(280)
                  .brightness(20))
    
    elif style == "soft":
        return (img.saturate(1.1)
                  .brightness(20)
                  .contrast(0.9)
                  .sepia(0.1))
    
    return img

# Apply TikTok styles
vibrant_tiktok = tiktok_aesthetic_filter(img, "vibrant")
neon_tiktok = tiktok_aesthetic_filter(img, "neon")
```

## 🔍 CSS Filter Analysis and Debugging

### Filter Effect Comparison

```python
def compare_css_filters(img, save_comparison=True):
    """Create a comparison grid of different CSS filters."""
    
    filters = {
        "Original": img,
        "Grayscale 50%": img.grayscale_filter(0.5),
        "Sepia 70%": img.sepia(0.7),
        "Invert 100%": img.invert(1.0),
        "Hue +90°": img.hue_rotate(90),
        "Saturate 150%": img.saturate(1.5),
        "Desaturate 50%": img.saturate(0.5),
        "Hue +180°": img.hue_rotate(180),
    }
    
    if save_comparison:
        for name, filtered_img in filters.items():
            safe_name = name.replace(" ", "_").replace("%", "pct").replace("+", "plus").replace("°", "deg")
            filtered_img.save(f"css_filter_comparison_{safe_name}.png")
    
    return filters

# Create comparison
comparison = compare_css_filters(img)
```

### Filter Intensity Testing

```python
def test_filter_intensities(img, filter_type="saturate"):
    """Test different intensities of a specific filter."""
    
    if filter_type == "saturate":
        levels = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5]
        for level in levels:
            result = img.saturate(level)
            result.save(f"intensity_test_saturate_{level}.png")
    
    elif filter_type == "sepia":
        levels = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
        for level in levels:
            result = img.sepia(level)
            result.save(f"intensity_test_sepia_{level}.png")
    
    elif filter_type == "hue_rotate":
        angles = [0, 60, 120, 180, 240, 300]
        for angle in angles:
            result = img.hue_rotate(angle)
            result.save(f"intensity_test_hue_rotate_{angle}.png")

# Test different filter intensities
test_filter_intensities(img, "saturate")
test_filter_intensities(img, "sepia")
test_filter_intensities(img, "hue_rotate")
```

## 🎯 Best Practices

### Performance Optimization

```python
# Efficient: Chain CSS filters together
efficient = img.sepia(0.8).saturate(1.2).hue_rotate(15).contrast(1.1)

# Less efficient: Multiple intermediate variables
# temp1 = img.sepia(0.8)
# temp2 = temp1.saturate(1.2)
# temp3 = temp2.hue_rotate(15)
# result = temp3.contrast(1.1)

# Batch processing with CSS filters
def batch_apply_css_filter(image_paths, filter_func, output_dir):
    """Apply CSS filter to multiple images."""
    from pathlib import Path
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    for path in image_paths:
        img = puhu.open(path)
        filtered = filter_func(img)
        output_file = output_path / f"css_filtered_{Path(path).name}"
        filtered.save(output_file)

# Usage
vintage_filter = lambda x: x.sepia(0.8).saturate(0.9).contrast(0.9)
batch_apply_css_filter(["photo1.jpg", "photo2.jpg"], vintage_filter, "output")
```

### Filter Validation

```python
def validate_css_filter_params(filter_name, value):
    """Validate CSS filter parameters."""
    
    validations = {
        "grayscale": (0.0, 1.0),
        "sepia": (0.0, 1.0),
        "invert": (0.0, 1.0),
        "saturate": (0.0, 5.0),  # Allow up to 500% saturation
        "hue_rotate": (0, 360),  # Degrees
    }
    
    if filter_name not in validations:
        raise ValueError(f"Unknown CSS filter: {filter_name}")
    
    min_val, max_val = validations[filter_name]
    if not (min_val <= value <= max_val):
        raise ValueError(f"{filter_name} value {value} out of range [{min_val}, {max_val}]")
    
    return True

# Safe filter application
def safe_css_filter(img, filter_name, value):
    """Safely apply CSS filter with validation."""
    try:
        validate_css_filter_params(filter_name, value)
        
        if filter_name == "grayscale":
            return img.grayscale_filter(value)
        elif filter_name == "sepia":
            return img.sepia(value)
        elif filter_name == "invert":
            return img.invert(value)
        elif filter_name == "saturate":
            return img.saturate(value)
        elif filter_name == "hue_rotate":
            return img.hue_rotate(value)
        
    except ValueError as e:
        print(f"Filter error: {e}")
        return img

# Usage
safe_result = safe_css_filter(img, "saturate", 1.5)
```

## 🔗 Next Steps

- **[Filters](filters.md)** - Basic image filters
- **[Pixel Manipulation](pixel-manipulation.md)** - Direct pixel operations
- **[Shadow Effects](shadows.md)** - Drop shadows and glow effects
- **[Examples](examples.md)** - Real-world CSS filter usage
- **[Performance Guide](performance.md)** - Optimization techniques