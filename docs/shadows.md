# Shadow Effects

Drop shadows, inner shadows, and glow effects for creating depth and visual impact.

## ✨ Overview

Puhu's shadow effects add depth, dimension, and visual appeal to images. These effects work best with RGBA images that support transparency, allowing for realistic shadow blending and layering.

## 🌑 Drop Shadows

### Basic Drop Shadow

#### `Image.drop_shadow(offset_x, offset_y, blur_radius, color)`

Add a drop shadow behind the image content.

**Parameters:**
- `offset_x` (int): Horizontal shadow offset (positive = right, negative = left)
- `offset_y` (int): Vertical shadow offset (positive = down, negative = up)
- `blur_radius` (float): Shadow blur amount (0.0 = sharp, higher = softer)
- `color` (tuple): Shadow color as RGBA tuple `(r, g, b, a)`

**Returns:** New `Image` instance with drop shadow applied

**Requirements:** Works best with RGBA images for proper transparency handling

**Examples:**

```python
import puhu

# Load and convert image to RGBA for best shadow results
img = puhu.open("photo.jpg").convert("RGBA")

# Basic drop shadow
basic_shadow = img.drop_shadow(5, 5, 3.0, (0, 0, 0, 128))

# Soft shadow
soft_shadow = img.drop_shadow(8, 8, 6.0, (0, 0, 0, 100))

# Hard shadow
hard_shadow = img.drop_shadow(3, 3, 0.5, (0, 0, 0, 200))

# Colored shadows
red_shadow = img.drop_shadow(4, 4, 4.0, (255, 0, 0, 120))
blue_shadow = img.drop_shadow(6, 6, 5.0, (0, 0, 255, 100))

# Different shadow directions
shadows = {
    "bottom_right": img.drop_shadow(5, 5, 3.0, (0, 0, 0, 128)),
    "bottom_left": img.drop_shadow(-5, 5, 3.0, (0, 0, 0, 128)),
    "top_right": img.drop_shadow(5, -5, 3.0, (0, 0, 0, 128)),
    "top_left": img.drop_shadow(-5, -5, 3.0, (0, 0, 0, 128)),
}

for direction, shadow_img in shadows.items():
    shadow_img.save(f"shadow_{direction}.png")

# Progressive shadow intensity
intensities = [50, 100, 150, 200, 255]
for intensity in intensities:
    shadow = img.drop_shadow(5, 5, 4.0, (0, 0, 0, intensity))
    shadow.save(f"shadow_intensity_{intensity}.png")

# Progressive shadow blur
blur_levels = [0.5, 1.0, 2.0, 4.0, 8.0]
for blur in blur_levels:
    shadow = img.drop_shadow(5, 5, blur, (0, 0, 0, 128))
    shadow.save(f"shadow_blur_{blur}.png")
```

### Advanced Drop Shadow Techniques

```python
def create_realistic_shadow(img, light_angle=45, distance=10, blur=5.0, opacity=128):
    """Create a realistic drop shadow based on light angle."""
    import math
    
    # Convert angle to radians
    angle_rad = math.radians(light_angle)
    
    # Calculate shadow offset based on light angle
    offset_x = int(distance * math.cos(angle_rad))
    offset_y = int(distance * math.sin(angle_rad))
    
    return img.drop_shadow(offset_x, offset_y, blur, (0, 0, 0, opacity))

# Create shadows for different lighting conditions
lighting_conditions = {
    "overhead": create_realistic_shadow(img, 90, 8, 4.0, 100),    # Light from above
    "side_left": create_realistic_shadow(img, 0, 12, 5.0, 120),   # Light from left
    "side_right": create_realistic_shadow(img, 180, 12, 5.0, 120), # Light from right
    "dramatic": create_realistic_shadow(img, 135, 15, 3.0, 180),  # Dramatic angle
}

def create_multiple_shadows(img, shadow_configs):
    """Apply multiple drop shadows for complex lighting effects."""
    result = img
    
    for config in shadow_configs:
        result = result.drop_shadow(
            config["offset_x"], config["offset_y"],
            config["blur"], config["color"]
        )
    
    return result

# Multiple shadow configuration for complex lighting
multi_shadow_config = [
    {"offset_x": 3, "offset_y": 3, "blur": 2.0, "color": (0, 0, 0, 100)},    # Main shadow
    {"offset_x": 8, "offset_y": 8, "blur": 8.0, "color": (0, 0, 0, 50)},     # Ambient shadow
    {"offset_x": -1, "offset_y": -1, "blur": 1.0, "color": (255, 255, 255, 80)}, # Highlight
]

complex_shadow = create_multiple_shadows(img, multi_shadow_config)

def create_floating_effect(img, height=15):
    """Create a floating effect with ground shadow."""
    # Create a soft, large shadow below the object
    ground_shadow = img.drop_shadow(0, height, height * 0.8, (0, 0, 0, 80))
    
    # Add a subtle direct shadow
    direct_shadow = ground_shadow.drop_shadow(2, 2, 1.0, (0, 0, 0, 60))
    
    return direct_shadow

floating_img = create_floating_effect(img, 20)
```

## 🔆 Glow Effects

### Basic Glow

#### `Image.glow(blur_radius, color, intensity=1.0)`

Add a glow effect around the image content.

**Parameters:**
- `blur_radius` (float): Glow blur radius (higher = larger glow)
- `color` (tuple): Glow color as RGBA tuple `(r, g, b, a)`
- `intensity` (float): Glow intensity multiplier (1.0 = normal, higher = brighter)

**Returns:** New `Image` instance with glow effect applied

**Examples:**

```python
# Convert to RGBA for best glow results
img = puhu.open("photo.jpg").convert("RGBA")

# Basic white glow
white_glow = img.glow(8.0, (255, 255, 255, 150), 1.0)

# Colored glows
red_glow = img.glow(6.0, (255, 0, 0, 180), 1.2)
blue_glow = img.glow(10.0, (0, 100, 255, 120), 1.5)
green_glow = img.glow(5.0, (0, 255, 100, 200), 1.0)

# Different glow sizes
glow_sizes = [3.0, 6.0, 10.0, 15.0, 20.0]
for size in glow_sizes:
    glow = img.glow(size, (255, 255, 0, 150), 1.0)
    glow.save(f"glow_size_{size}.png")

# Different glow intensities
intensities = [0.5, 1.0, 1.5, 2.0, 3.0]
for intensity in intensities:
    glow = img.glow(8.0, (0, 255, 255, 150), intensity)
    glow.save(f"glow_intensity_{intensity}.png")

# Neon-style glows
neon_colors = [
    (255, 0, 255, 200),    # Magenta
    (0, 255, 255, 200),    # Cyan
    (255, 255, 0, 200),    # Yellow
    (255, 100, 0, 200),    # Orange
    (100, 255, 100, 200),  # Lime
]

for i, color in enumerate(neon_colors):
    neon_glow = img.glow(12.0, color, 2.0)
    neon_glow.save(f"neon_glow_{i}.png")
```

### Advanced Glow Techniques

```python
def create_halo_effect(img, inner_radius=5.0, outer_radius=15.0):
    """Create a halo effect with multiple glow layers."""
    # Inner bright glow
    inner_glow = img.glow(inner_radius, (255, 255, 255, 200), 2.0)
    
    # Outer soft glow
    outer_glow = inner_glow.glow(outer_radius, (255, 255, 200, 100), 1.0)
    
    return outer_glow

halo_img = create_halo_effect(img, 4.0, 18.0)

def create_energy_effect(img):
    """Create an energy/power effect with multiple colored glows."""
    # Base energy glow
    energy = img.glow(8.0, (0, 200, 255, 180), 1.5)
    
    # Add electric blue outer glow
    energy = energy.glow(15.0, (100, 150, 255, 100), 1.0)
    
    # Add white core glow
    energy = energy.glow(3.0, (255, 255, 255, 220), 2.5)
    
    return energy

energy_img = create_energy_effect(img)

def create_fire_glow(img):
    """Create a fire-like glow effect."""
    # Orange core
    fire = img.glow(5.0, (255, 100, 0, 200), 2.0)
    
    # Red middle layer
    fire = fire.glow(10.0, (255, 50, 0, 150), 1.5)
    
    # Yellow outer glow
    fire = fire.glow(18.0, (255, 200, 0, 100), 1.0)
    
    return fire

fire_img = create_fire_glow(img)

def create_magical_aura(img):
    """Create a magical aura with shifting colors."""
    # Purple base
    magical = img.glow(12.0, (150, 0, 255, 120), 1.2)
    
    # Blue middle
    magical = magical.glow(8.0, (0, 100, 255, 150), 1.0)
    
    # Pink highlights
    magical = magical.glow(4.0, (255, 100, 200, 180), 1.8)
    
    return magical

magical_img = create_magical_aura(img)
```

## 🌘 Inner Shadows

### Basic Inner Shadow

#### `Image.inner_shadow(offset_x, offset_y, blur_radius, color)`

Add an inner shadow effect for depth and inset appearance.

**Parameters:**
- `offset_x` (int): Horizontal shadow offset
- `offset_y` (int): Vertical shadow offset
- `blur_radius` (float): Shadow blur amount
- `color` (tuple): Shadow color as RGBA tuple `(r, g, b, a)`

**Returns:** New `Image` instance with inner shadow applied

**Examples:**

```python
# Convert to RGBA for best inner shadow results
img = puhu.open("photo.jpg").convert("RGBA")

# Basic inner shadow
basic_inner = img.inner_shadow(3, 3, 2.0, (0, 0, 0, 100))

# Subtle inner shadow for depth
subtle_inner = img.inner_shadow(2, 2, 4.0, (0, 0, 0, 60))

# Strong inner shadow for dramatic effect
strong_inner = img.inner_shadow(5, 5, 1.0, (0, 0, 0, 180))

# Colored inner shadows
red_inner = img.inner_shadow(3, 3, 3.0, (255, 0, 0, 120))
blue_inner = img.inner_shadow(4, 4, 2.5, (0, 0, 255, 100))

# Different inner shadow directions
inner_shadows = {
    "top_left": img.inner_shadow(-3, -3, 2.0, (0, 0, 0, 120)),
    "top_right": img.inner_shadow(3, -3, 2.0, (0, 0, 0, 120)),
    "bottom_left": img.inner_shadow(-3, 3, 2.0, (0, 0, 0, 120)),
    "bottom_right": img.inner_shadow(3, 3, 2.0, (0, 0, 0, 120)),
}

for direction, shadow_img in inner_shadows.items():
    shadow_img.save(f"inner_shadow_{direction}.png")

# Progressive inner shadow blur
blur_levels = [0.5, 1.0, 2.0, 4.0, 6.0]
for blur in blur_levels:
    inner = img.inner_shadow(3, 3, blur, (0, 0, 0, 120))
    inner.save(f"inner_shadow_blur_{blur}.png")
```

### Advanced Inner Shadow Effects

```python
def create_embossed_effect(img):
    """Create an embossed effect using inner shadows."""
    # Light inner shadow from top-left
    embossed = img.inner_shadow(-2, -2, 1.0, (255, 255, 255, 100))
    
    # Dark inner shadow from bottom-right
    embossed = embossed.inner_shadow(2, 2, 1.0, (0, 0, 0, 120))
    
    return embossed

embossed_img = create_embossed_effect(img)

def create_inset_button_effect(img):
    """Create an inset button appearance."""
    # Main inner shadow
    button = img.inner_shadow(2, 2, 3.0, (0, 0, 0, 100))
    
    # Subtle highlight on opposite side
    button = button.inner_shadow(-1, -1, 1.0, (255, 255, 255, 80))
    
    return button

button_img = create_inset_button_effect(img)

def create_carved_effect(img):
    """Create a carved or etched appearance."""
    # Deep inner shadow
    carved = img.inner_shadow(4, 4, 2.0, (0, 0, 0, 150))
    
    # Subtle counter-highlight
    carved = carved.inner_shadow(-1, -1, 2.0, (255, 255, 255, 60))
    
    return carved

carved_img = create_carved_effect(img)
```

## 🎨 Combining Shadow Effects

### Multiple Shadow Combinations

```python
def create_layered_shadow_effect(img):
    """Combine multiple shadow effects for complex appearance."""
    # Start with drop shadow
    result = img.drop_shadow(5, 5, 4.0, (0, 0, 0, 120))
    
    # Add glow
    result = result.glow(8.0, (255, 255, 200, 100), 1.2)
    
    # Add inner shadow for depth
    result = result.inner_shadow(2, 2, 2.0, (0, 0, 0, 80))
    
    return result

layered_effect = create_layered_shadow_effect(img)

def create_floating_glow_effect(img):
    """Create a floating object with glow."""
    # Ground shadow (soft and offset)
    floating = img.drop_shadow(0, 15, 12.0, (0, 0, 0, 60))
    
    # Object glow
    floating = floating.glow(6.0, (255, 255, 255, 150), 1.5)
    
    # Subtle direct shadow
    floating = floating.drop_shadow(2, 2, 1.0, (0, 0, 0, 40))
    
    return floating

floating_glow = create_floating_glow_effect(img)

def create_neon_sign_effect(img, neon_color=(0, 255, 255, 200)):
    """Create a neon sign effect."""
    # Inner glow
    neon = img.glow(3.0, neon_color, 3.0)
    
    # Outer glow
    neon = neon.glow(12.0, neon_color, 1.5)
    
    # Reflection shadow below
    reflection_color = (neon_color[0], neon_color[1], neon_color[2], 80)
    neon = neon.drop_shadow(0, 8, 6.0, reflection_color)
    
    return neon

neon_sign = create_neon_sign_effect(img, (255, 0, 255, 200))

def create_glass_effect(img):
    """Create a glass-like appearance with shadows."""
    # Subtle drop shadow
    glass = img.drop_shadow(2, 2, 4.0, (0, 0, 0, 60))
    
    # Inner highlight
    glass = glass.inner_shadow(-1, -1, 2.0, (255, 255, 255, 100))
    
    # Soft glow
    glass = glass.glow(5.0, (255, 255, 255, 80), 0.8)
    
    return glass

glass_effect = create_glass_effect(img)
```

### Text Shadow Effects

```python
def create_text_with_shadows(canvas, text, x, y, text_color, scale=2):
    """Create text with various shadow effects."""
    # Draw text with drop shadow
    with_shadow = canvas.draw_text(text, x + 3, y + 3, (0, 0, 0, 128), scale)
    with_shadow = with_shadow.draw_text(text, x, y, text_color, scale)
    
    return with_shadow

def create_glowing_text(canvas, text, x, y, text_color, glow_color, scale=2):
    """Create text with glow effect."""
    # This is a conceptual implementation
    # Real glow would require the text to be drawn as an image first
    
    # Draw multiple offset copies for glow effect
    glow_offsets = [(-2, -2), (-2, 0), (-2, 2), (0, -2), (0, 2), (2, -2), (2, 0), (2, 2)]
    
    result = canvas
    for offset_x, offset_y in glow_offsets:
        result = result.draw_text(text, x + offset_x, y + offset_y, glow_color, scale)
    
    # Draw main text on top
    result = result.draw_text(text, x, y, text_color, scale)
    
    return result

# Create canvas for text effects
text_canvas = puhu.new("RGB", (400, 200), (20, 20, 20))

# Text with drop shadow
shadow_text = create_text_with_shadows(
    text_canvas, "SHADOW", 50, 50, (255, 255, 255, 255)
)

# Glowing text
glow_text = create_glowing_text(
    text_canvas, "GLOW", 50, 120, 
    (255, 255, 255, 255), (0, 255, 255, 100)
)
```

## 🎯 Practical Applications

### UI Element Shadows

```python
def create_button_with_shadow(size, text, bg_color, text_color):
    """Create a button with realistic shadow."""
    width, height = size
    
    # Create button background
    button = puhu.new("RGBA", size, bg_color)
    
    # Add text
    text_x = (width - len(text) * 8) // 2
    text_y = (height - 12) // 2
    button = button.draw_text(text, text_x, text_y, text_color, 1)
    
    # Add drop shadow
    button_with_shadow = button.drop_shadow(2, 2, 3.0, (0, 0, 0, 100))
    
    # Add subtle inner highlight
    button_with_shadow = button_with_shadow.inner_shadow(-1, -1, 1.0, (255, 255, 255, 60))
    
    return button_with_shadow

# Create various buttons
primary_button = create_button_with_shadow(
    (120, 40), "PRIMARY", (52, 152, 219, 255), (255, 255, 255, 255)
)

success_button = create_button_with_shadow(
    (120, 40), "SUCCESS", (46, 204, 113, 255), (255, 255, 255, 255)
)

danger_button = create_button_with_shadow(
    (120, 40), "DANGER", (231, 76, 60, 255), (255, 255, 255, 255)
)

def create_card_with_shadow(size, content_color=(255, 255, 255, 255)):
    """Create a card UI element with shadow."""
    # Create card
    card = puhu.new("RGBA", size, content_color)
    
    # Add soft drop shadow
    card_with_shadow = card.drop_shadow(0, 4, 8.0, (0, 0, 0, 60))
    
    # Add subtle border glow
    card_with_shadow = card_with_shadow.glow(1.0, (0, 0, 0, 30), 0.5)
    
    return card_with_shadow

card = create_card_with_shadow((200, 150))
```

### Logo and Branding Effects

```python
def create_logo_with_effects(logo_img):
    """Add professional shadow effects to a logo."""
    # Convert to RGBA
    logo = logo_img.convert("RGBA")
    
    # Add subtle drop shadow
    with_shadow = logo.drop_shadow(3, 3, 5.0, (0, 0, 0, 80))
    
    # Add brand glow
    with_glow = with_shadow.glow(4.0, (255, 255, 255, 60), 1.0)
    
    return with_glow

def create_watermark_with_shadow(canvas, text, position="bottom_right"):
    """Create a watermark with shadow for better visibility."""
    width, height = canvas.size
    
    # Calculate position
    if position == "bottom_right":
        x = width - len(text) * 8 - 20
        y = height - 30
    else:
        x, y = position
    
    # Add shadow first
    result = canvas.draw_text(text, x + 1, y + 1, (0, 0, 0, 100), 1)
    
    # Add main text
    result = result.draw_text(text, x, y, (255, 255, 255, 200), 1)
    
    return result

# Apply to an image
watermarked = create_watermark_with_shadow(img, "© 2024 Puhu Graphics")
```

### Photo Enhancement

```python
def add_vignette_shadow(img, intensity=0.3):
    """Add a vignette effect using inner shadows."""
    # This is a conceptual implementation
    # Real vignette would require more sophisticated blending
    
    # Add dark inner shadow from all edges
    vignette = img.inner_shadow(10, 10, 20.0, (0, 0, 0, int(255 * intensity)))
    vignette = vignette.inner_shadow(-10, -10, 20.0, (0, 0, 0, int(255 * intensity)))
    vignette = vignette.inner_shadow(10, -10, 20.0, (0, 0, 0, int(255 * intensity)))
    vignette = vignette.inner_shadow(-10, 10, 20.0, (0, 0, 0, int(255 * intensity)))
    
    return vignette

def create_dreamy_glow(img, glow_color=(255, 255, 200, 80)):
    """Add a dreamy glow effect to photos."""
    # Soft outer glow
    dreamy = img.glow(15.0, glow_color, 1.0)
    
    # Subtle inner glow
    dreamy = dreamy.glow(5.0, (255, 255, 255, 40), 0.8)
    
    return dreamy

# Apply effects
vignette_img = add_vignette_shadow(img, 0.4)
dreamy_img = create_dreamy_glow(img)
```

## 📊 Shadow Effect Comparison

```python
def create_shadow_comparison(base_img):
    """Create a comparison of different shadow effects."""
    # Convert to RGBA
    img = base_img.convert("RGBA")
    
    effects = {
        "original": img,
        "drop_shadow": img.drop_shadow(5, 5, 4.0, (0, 0, 0, 128)),
        "soft_glow": img.glow(8.0, (255, 255, 255, 150), 1.2),
        "inner_shadow": img.inner_shadow(3, 3, 2.0, (0, 0, 0, 100)),
        "neon_glow": img.glow(10.0, (0, 255, 255, 200), 2.0),
        "combined": (img.drop_shadow(4, 4, 3.0, (0, 0, 0, 100))
                        .glow(6.0, (255, 255, 200, 120), 1.0)
                        .inner_shadow(2, 2, 1.0, (0, 0, 0, 60))),
    }
    
    return effects

# Create comparison
shadow_effects = create_shadow_comparison(img)
for effect_name, effect_img in shadow_effects.items():
    effect_img.save(f"shadow_effect_{effect_name}.png")

def analyze_shadow_performance(img, num_tests=5):
    """Analyze performance of different shadow effects."""
    import time
    
    effects_to_test = [
        ("drop_shadow", lambda x: x.drop_shadow(5, 5, 4.0, (0, 0, 0, 128))),
        ("glow", lambda x: x.glow(8.0, (255, 255, 255, 150), 1.2)),
        ("inner_shadow", lambda x: x.inner_shadow(3, 3, 2.0, (0, 0, 0, 100))),
    ]
    
    results = {}
    
    for effect_name, effect_func in effects_to_test:
        times = []
        for _ in range(num_tests):
            start_time = time.time()
            result = effect_func(img)
            end_time = time.time()
            times.append(end_time - start_time)
        
        avg_time = sum(times) / len(times)
        results[effect_name] = avg_time
    
    return results

# Analyze performance (if needed)
# performance_results = analyze_shadow_performance(img)
```

## 🔧 Performance Optimization

### Efficient Shadow Application

```python
# Efficient: Apply multiple effects in sequence
efficient_shadows = (img.drop_shadow(4, 4, 3.0, (0, 0, 0, 100))
                        .glow(6.0, (255, 255, 200, 120), 1.0)
                        .inner_shadow(2, 2, 1.0, (0, 0, 0, 60)))

# Less efficient: Multiple intermediate variables
# temp1 = img.drop_shadow(4, 4, 3.0, (0, 0, 0, 100))
# temp2 = temp1.glow(6.0, (255, 255, 200, 120), 1.0)
# result = temp2.inner_shadow(2, 2, 1.0, (0, 0, 0, 60))

# Batch shadow processing
def apply_shadow_preset(img, preset_name):
    """Apply predefined shadow presets efficiently."""
    presets = {
        "subtle": lambda x: x.drop_shadow(2, 2, 3.0, (0, 0, 0, 80)),
        "dramatic": lambda x: x.drop_shadow(8, 8, 2.0, (0, 0, 0, 150)),
        "glow": lambda x: x.glow(8.0, (255, 255, 255, 120), 1.5),
        "neon": lambda x: x.glow(12.0, (0, 255, 255, 200), 2.0),
        "embossed": lambda x: x.inner_shadow(2, 2, 1.0, (0, 0, 0, 120)),
        "floating": lambda x: x.drop_shadow(0, 10, 8.0, (0, 0, 0, 60)),
    }
    
    if preset_name in presets:
        return presets[preset_name](img)
    return img

# Apply presets
subtle_shadow = apply_shadow_preset(img, "subtle")
dramatic_shadow = apply_shadow_preset(img, "dramatic")
neon_effect = apply_shadow_preset(img, "neon")
```

## 🔗 Next Steps

- **[Compositing & Blending](compositing.md)** - Advanced image compositing
- **[Drawing Operations](drawing.md)** - Shape and text drawing
- **[Examples](examples.md)** - Real-world shadow effect examples
- **[Performance Guide](performance.md)** - Optimization techniques
- **[API Reference](api-reference.md)** - Complete method documentation