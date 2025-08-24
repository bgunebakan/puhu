# Examples

Real-world usage examples and tutorials for common image processing tasks.

## 🚀 Getting Started Examples

### Basic Image Processing

```python
import puhu

# Load, process, and save an image
def basic_photo_enhancement(input_path, output_path):
    """Basic photo enhancement workflow."""
    # Load image
    img = puhu.open(input_path)
    print(f"Loaded image: {img.size} {img.mode}")
    
    # Apply enhancements
    enhanced = (img
                .brightness(10)      # Slight brightness boost
                .contrast(1.1)       # Increase contrast
                .sharpen(1.2)        # Sharpen details
                .saturate(1.05))     # Enhance colors
    
    # Save result
    enhanced.save(output_path)
    print(f"Enhanced image saved to {output_path}")
    
    return enhanced

# Usage
enhanced_photo = basic_photo_enhancement("photo.jpg", "enhanced_photo.jpg")
```

### Batch Processing

```python
from pathlib import Path

def batch_resize_images(input_dir, output_dir, target_size=(800, 600)):
    """Resize all images in a directory."""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Supported image extensions
    extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
    
    processed = 0
    for image_file in input_path.iterdir():
        if image_file.suffix.lower() in extensions:
            try:
                # Load and resize
                img = puhu.open(image_file)
                resized = img.resize(target_size)
                
                # Save with same name
                output_file = output_path / image_file.name
                resized.save(output_file)
                
                print(f"Resized {image_file.name}: {img.size} → {resized.size}")
                processed += 1
                
            except Exception as e:
                print(f"Error processing {image_file.name}: {e}")
    
    print(f"Processed {processed} images")

# Usage
batch_resize_images("input_photos", "resized_photos", (1024, 768))
```

## 📸 Photography Examples

### Portrait Enhancement

```python
def enhance_portrait(img):
    """Enhance portrait photos with skin-friendly adjustments."""
    return (img
            .blur(0.3)           # Subtle skin smoothing
            .brightness(8)       # Gentle brightening
            .contrast(1.05)      # Slight contrast boost
            .saturate(1.1)       # Enhance skin tones
            .sharpen(1.1))       # Restore sharpness

def create_portrait_variations(input_path):
    """Create multiple portrait variations."""
    img = puhu.open(input_path).convert("RGBA")
    
    variations = {
        "natural": enhance_portrait(img),
        "warm": enhance_portrait(img).hue_rotate(10).saturate(1.2),
        "cool": enhance_portrait(img).hue_rotate(200).saturate(1.1),
        "vintage": (enhance_portrait(img)
                   .sepia(0.3)
                   .contrast(0.95)
                   .brightness(-5)),
        "dramatic": (img.contrast(1.3)
                       .saturate(1.4)
                       .sharpen(1.5)
                       .brightness(5)),
    }
    
    for style, processed_img in variations.items():
        processed_img.save(f"portrait_{style}.png")
    
    return variations

# Usage
portrait_variations = create_portrait_variations("portrait.jpg")
```

### Landscape Enhancement

```python
def enhance_landscape(img):
    """Enhance landscape photos for vibrant colors and sharp details."""
    return (img
            .sharpen(1.3)        # Enhance details
            .contrast(1.15)      # Increase contrast
            .saturate(1.3)       # Vibrant colors
            .brightness(-3))     # Slight darkening for drama

def create_landscape_moods(input_path):
    """Create different mood variations for landscape photos."""
    img = puhu.open(input_path)
    
    moods = {
        "golden_hour": (enhance_landscape(img)
                       .hue_rotate(15)
                       .saturate(1.4)
                       .brightness(10)),
        
        "blue_hour": (enhance_landscape(img)
                     .hue_rotate(220)
                     .saturate(1.2)
                     .brightness(-10)),
        
        "dramatic": (img.contrast(1.5)
                       .saturate(1.6)
                       .sharpen(1.4)
                       .brightness(-8)),
        
        "soft_pastel": (img.saturate(0.8)
                          .brightness(15)
                          .contrast(0.9)
                          .blur(0.3)),
        
        "black_white": (img.grayscale_filter(1.0)
                          .contrast(1.3)
                          .brightness(5)),
    }
    
    for mood, processed_img in moods.items():
        processed_img.save(f"landscape_{mood}.jpg")
    
    return moods

# Usage
landscape_moods = create_landscape_moods("landscape.jpg")
```

## 🎨 Creative Effects

### Instagram-Style Filters

```python
class InstagramFilters:
    """Collection of Instagram-inspired filters."""
    
    @staticmethod
    def valencia(img):
        """Valencia filter - warm, faded look."""
        return (img
                .sepia(0.1)
                .saturate(1.2)
                .contrast(1.1)
                .brightness(10)
                .hue_rotate(5))
    
    @staticmethod
    def nashville(img):
        """Nashville filter - pink/orange tint."""
        return (img
                .sepia(0.2)
                .saturate(1.3)
                .contrast(1.2)
                .hue_rotate(15)
                .brightness(5))
    
    @staticmethod
    def kelvin(img):
        """Kelvin filter - warm, high contrast."""
        return (img
                .hue_rotate(15)
                .saturate(1.5)
                .contrast(1.1)
                .brightness(10)
                .sharpen(1.1))
    
    @staticmethod
    def x_pro_ii(img):
        """X-Pro II filter - vintage, high contrast."""
        return (img
                .sepia(0.3)
                .saturate(1.4)
                .contrast(1.3)
                .brightness(-5)
                .sharpen(1.2))
    
    @staticmethod
    def lo_fi(img):
        """Lo-Fi filter - desaturated, high contrast."""
        return (img
                .saturate(1.1)
                .contrast(1.5)
                .brightness(-10)
                .sepia(0.1))
    
    @staticmethod
    def earlybird(img):
        """Earlybird filter - sepia with vignette effect."""
        return (img
                .sepia(0.4)
                .saturate(0.9)
                .contrast(1.1)
                .brightness(-8))

def apply_instagram_filters(input_path):
    """Apply all Instagram-style filters to an image."""
    img = puhu.open(input_path)
    filters = InstagramFilters()
    
    filter_methods = [
        ('valencia', filters.valencia),
        ('nashville', filters.nashville),
        ('kelvin', filters.kelvin),
        ('x_pro_ii', filters.x_pro_ii),
        ('lo_fi', filters.lo_fi),
        ('earlybird', filters.earlybird),
    ]
    
    results = {}
    for name, filter_func in filter_methods:
        filtered = filter_func(img)
        filtered.save(f"instagram_{name}.jpg")
        results[name] = filtered
        print(f"Applied {name} filter")
    
    return results

# Usage
instagram_filters = apply_instagram_filters("photo.jpg")
```

### Artistic Effects

```python
def create_pop_art(img, colors=None):
    """Create pop art effect with posterization and color shifts."""
    if colors is None:
        colors = [0, 60, 120, 180, 240, 300]  # Hue shifts
    
    # Base processing
    base = (img
            .posterize(4)        # Reduce colors
            .saturate(1.8)       # High saturation
            .contrast(1.4))      # High contrast
    
    variations = {}
    for i, hue_shift in enumerate(colors):
        variation = base.hue_rotate(hue_shift)
        variations[f"pop_art_{i}"] = variation
        variation.save(f"pop_art_{i}.png")
    
    return variations

def create_oil_painting_effect(img):
    """Simulate oil painting effect."""
    return (img
            .blur(2.0)           # Smooth details
            .sharpen(0.7)        # Reduce sharpness
            .contrast(1.3)       # Increase contrast
            .saturate(1.4)       # Rich colors
            .posterize(6))       # Reduce color levels

def create_pencil_sketch(img):
    """Create pencil sketch effect."""
    # Convert to grayscale first
    gray = img.convert("L")
    
    # Detect edges
    edges = gray.edge_detect()
    
    # Invert for pencil effect
    sketch = edges.invert(1.0)
    
    # Adjust contrast
    sketch = sketch.contrast(1.5)
    
    return sketch.convert("RGB")

def create_watercolor_effect(img):
    """Create watercolor painting effect."""
    return (img
            .blur(3.0)           # Soft edges
            .saturate(1.6)       # Vibrant colors
            .brightness(15)      # Lighter tones
            .contrast(0.8)       # Softer contrast
            .posterize(8))       # Simplified colors

# Usage examples
img = puhu.open("photo.jpg")

pop_art_variations = create_pop_art(img)
oil_painting = create_oil_painting_effect(img)
pencil_sketch = create_pencil_sketch(img)
watercolor = create_watercolor_effect(img)

# Save artistic effects
oil_painting.save("oil_painting.jpg")
pencil_sketch.save("pencil_sketch.jpg")
watercolor.save("watercolor.jpg")
```

## 🖼️ Compositing and Collages

### Photo Collage Creation

```python
def create_grid_collage(image_paths, grid_size, cell_size, spacing=10):
    """Create a grid-based photo collage."""
    cols, rows = grid_size
    cell_width, cell_height = cell_size
    
    # Calculate canvas size
    canvas_width = cols * cell_width + (cols - 1) * spacing
    canvas_height = rows * cell_height + (rows - 1) * spacing
    
    # Create white background
    collage = puhu.new("RGB", (canvas_width, canvas_height), "white")
    
    # Place images
    for i, image_path in enumerate(image_paths[:cols * rows]):
        if not Path(image_path).exists():
            continue
            
        try:
            # Load and resize image
            img = puhu.open(image_path)
            resized = img.resize(cell_size)
            
            # Calculate position
            row = i // cols
            col = i % cols
            x = col * (cell_width + spacing)
            y = row * (cell_height + spacing)
            
            # Paste image
            collage = collage.paste(resized, (x, y))
            
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
    
    return collage

def create_polaroid_collage(image_paths, canvas_size=(1200, 800)):
    """Create a scattered Polaroid-style collage."""
    import random
    import math
    
    canvas = puhu.new("RGB", canvas_size, (240, 240, 240))  # Light gray background
    
    polaroid_size = (200, 240)  # Polaroid dimensions
    photo_size = (180, 180)     # Photo area
    
    for image_path in image_paths:
        if not Path(image_path).exists():
            continue
            
        try:
            # Load and prepare image
            img = puhu.open(image_path)
            photo = img.resize(photo_size)
            
            # Create Polaroid frame
            polaroid = puhu.new("RGB", polaroid_size, "white")
            
            # Paste photo onto Polaroid (centered, with bottom margin for text)
            photo_x = (polaroid_size[0] - photo_size[0]) // 2
            photo_y = 10  # Top margin
            polaroid = polaroid.paste(photo, (photo_x, photo_y))
            
            # Add shadow to Polaroid
            polaroid_rgba = polaroid.convert("RGBA")
            with_shadow = polaroid_rgba.drop_shadow(5, 5, 8.0, (0, 0, 0, 100))
            
            # Random position and slight rotation effect (simulated with offset)
            max_x = canvas_size[0] - polaroid_size[0] - 50
            max_y = canvas_size[1] - polaroid_size[1] - 50
            x = random.randint(25, max_x)
            y = random.randint(25, max_y)
            
            # Paste onto canvas
            canvas = canvas.paste(with_shadow, (x, y))
            
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
    
    return canvas

# Usage
image_list = ["photo1.jpg", "photo2.jpg", "photo3.jpg", "photo4.jpg", 
              "photo5.jpg", "photo6.jpg", "photo7.jpg", "photo8.jpg"]

# Grid collage
grid_collage = create_grid_collage(image_list, (3, 3), (300, 200), 15)
grid_collage.save("grid_collage.jpg")

# Polaroid collage
polaroid_collage = create_polaroid_collage(image_list, (1400, 1000))
polaroid_collage.save("polaroid_collage.jpg")
```

### Before/After Comparisons

```python
def create_before_after_comparison(original_path, processed_img, layout="horizontal"):
    """Create before/after comparison image."""
    original = puhu.open(original_path)
    
    # Ensure both images are the same size
    if original.size != processed_img.size:
        processed_img = processed_img.resize(original.size)
    
    if layout == "horizontal":
        # Side by side
        canvas_width = original.width * 2 + 20  # 20px separator
        canvas_height = original.height
        canvas = puhu.new("RGB", (canvas_width, canvas_height), "white")
        
        # Paste images
        canvas = canvas.paste(original, (0, 0))
        canvas = canvas.paste(processed_img, (original.width + 20, 0))
        
        # Add labels
        canvas = canvas.draw_text("BEFORE", 10, 10, (255, 255, 255, 255), 2)
        canvas = canvas.draw_text("AFTER", original.width + 30, 10, (255, 255, 255, 255), 2)
        
    else:  # vertical
        # Top and bottom
        canvas_width = original.width
        canvas_height = original.height * 2 + 20  # 20px separator
        canvas = puhu.new("RGB", (canvas_width, canvas_height), "white")
        
        # Paste images
        canvas = canvas.paste(original, (0, 0))
        canvas = canvas.paste(processed_img, (0, original.height + 20))
        
        # Add labels
        canvas = canvas.draw_text("BEFORE", 10, 10, (255, 255, 255, 255), 2)
        canvas = canvas.draw_text("AFTER", 10, original.height + 30, (255, 255, 255, 255), 2)
    
    return canvas

# Usage
original_photo = "original.jpg"
enhanced = puhu.open(original_photo).brightness(20).contrast(1.2).saturate(1.1)

comparison_h = create_before_after_comparison(original_photo, enhanced, "horizontal")
comparison_v = create_before_after_comparison(original_photo, enhanced, "vertical")

comparison_h.save("before_after_horizontal.jpg")
comparison_v.save("before_after_vertical.jpg")
```

## 📊 Data Visualization

### Creating Charts and Graphs

```python
def create_bar_chart(data, labels, title="Bar Chart", colors=None):
    """Create a bar chart image."""
    if colors is None:
        colors = [(52, 152, 219, 255), (46, 204, 113, 255), (231, 76, 60, 255),
                 (241, 196, 15, 255), (155, 89, 182, 255), (230, 126, 34, 255)]
    
    # Chart dimensions
    width, height = 600, 400
    margin = 60
    chart_width = width - 2 * margin
    chart_height = height - 2 * margin - 40  # Extra space for title
    
    # Create canvas
    canvas = puhu.new("RGB", (width, height), "white")
    
    # Draw title
    title_x = (width - len(title) * 12) // 2
    canvas = canvas.draw_text(title, title_x, 20, (0, 0, 0, 255), 2)
    
    # Calculate bar dimensions
    max_value = max(data) if data else 1
    bar_width = chart_width // len(data) - 10
    
    for i, (value, label) in enumerate(zip(data, labels)):
        # Calculate bar height and position
        bar_height = int((value / max_value) * chart_height)
        x = margin + i * (chart_width // len(data))
        y = height - margin - bar_height
        
        # Draw bar
        color = colors[i % len(colors)]
        canvas = canvas.draw_rectangle(x, y, bar_width, bar_height, color)
        
        # Draw value on top of bar
        value_text = str(value)
        text_x = x + (bar_width - len(value_text) * 8) // 2
        canvas = canvas.draw_text(value_text, text_x, y - 20, (0, 0, 0, 255), 1)
        
        # Draw label below bar
        label_x = x + (bar_width - len(label) * 8) // 2
        canvas = canvas.draw_text(label, label_x, height - margin + 10, (0, 0, 0, 255), 1)
    
    return canvas

def create_pie_chart(data, labels, title="Pie Chart", colors=None):
    """Create a pie chart image."""
    import math
    
    if colors is None:
        colors = [(52, 152, 219, 255), (46, 204, 113, 255), (231, 76, 60, 255),
                 (241, 196, 15, 255), (155, 89, 182, 255), (230, 126, 34, 255)]
    
    # Chart dimensions
    size = 400
    canvas = puhu.new("RGB", (size, size), "white")
    
    # Draw title
    title_x = (size - len(title) * 12) // 2
    canvas = canvas.draw_text(title, title_x, 20, (0, 0, 0, 255), 2)
    
    # Chart parameters
    center_x, center_y = size // 2, size // 2 + 20
    radius = 120
    
    total = sum(data)
    current_angle = 0
    
    for i, (value, label) in enumerate(zip(data, labels)):
        # Calculate slice angle
        slice_angle = (value / total) * 2 * math.pi
        
        # Draw slice (simplified - using lines from center)
        color = colors[i % len(colors)]
        
        # Draw multiple lines to fill the slice
        num_lines = max(1, int(slice_angle * radius / 3))
        for j in range(num_lines):
            angle = current_angle + (j / num_lines) * slice_angle
            end_x = center_x + int(radius * math.cos(angle))
            end_y = center_y + int(radius * math.sin(angle))
            canvas = canvas.draw_line(center_x, center_y, end_x, end_y, color)
        
        # Draw label
        label_angle = current_angle + slice_angle / 2
        label_radius = radius + 30
        label_x = center_x + int(label_radius * math.cos(label_angle))
        label_y = center_y + int(label_radius * math.sin(label_angle))
        
        # Adjust label position to avoid overlap
        label_x -= len(label) * 4
        canvas = canvas.draw_text(label, label_x, label_y, (0, 0, 0, 255), 1)
        
        current_angle += slice_angle
    
    return canvas

# Usage
sales_data = [25, 40, 30, 55, 20]
sales_labels = ["Q1", "Q2", "Q3", "Q4", "Q5"]

bar_chart = create_bar_chart(sales_data, sales_labels, "Quarterly Sales")
pie_chart = create_pie_chart(sales_data, sales_labels, "Sales Distribution")

bar_chart.save("sales_bar_chart.png")
pie_chart.save("sales_pie_chart.png")
```

### Infographic Elements

```python
def create_metric_card(value, unit, label, color, size=(150, 120)):
    """Create a metric card for dashboards."""
    width, height = size
    card = puhu.new("RGB", size, "white")
    
    # Add colored top bar
    card = card.draw_rectangle(0, 0, width, 8, color)
    
    # Add value (large text)
    value_str = str(value)
    value_x = (width - len(value_str) * 16) // 2
    card = card.draw_text(value_str, value_x, 25, color, 3)
    
    # Add unit (smaller text)
    unit_x = (width - len(unit) * 8) // 2
    card = card.draw_text(unit, unit_x, 55, (128, 128, 128, 255), 1)
    
    # Add label (bottom)
    label_x = (width - len(label) * 8) // 2
    card = card.draw_text(label, label_x, 85, (64, 64, 64, 255), 1)
    
    # Add subtle shadow
    card_rgba = card.convert("RGBA")
    with_shadow = card_rgba.drop_shadow(2, 2, 4.0, (0, 0, 0, 50))
    
    return with_shadow

def create_dashboard(metrics_data):
    """Create a dashboard with multiple metric cards."""
    # Calculate layout
    cards_per_row = 4
    card_size = (150, 120)
    spacing = 20
    margin = 40
    
    rows = (len(metrics_data) + cards_per_row - 1) // cards_per_row
    
    canvas_width = cards_per_row * card_size[0] + (cards_per_row - 1) * spacing + 2 * margin
    canvas_height = rows * card_size[1] + (rows - 1) * spacing + 2 * margin + 60
    
    # Create canvas
    dashboard = puhu.new("RGB", (canvas_width, canvas_height), (245, 245, 245))
    
    # Add title
    title = "PERFORMANCE DASHBOARD"
    title_x = (canvas_width - len(title) * 16) // 2
    dashboard = dashboard.draw_text(title, title_x, 20, (64, 64, 64, 255), 3)
    
    # Add metric cards
    for i, (value, unit, label, color) in enumerate(metrics_data):
        row = i // cards_per_row
        col = i % cards_per_row
        
        x = margin + col * (card_size[0] + spacing)
        y = 80 + row * (card_size[1] + spacing)
        
        card = create_metric_card(value, unit, label, color, card_size)
        dashboard = dashboard.paste(card, (x, y))
    
    return dashboard

# Usage
dashboard_metrics = [
    (1250, "K", "Users", (52, 152, 219, 255)),
    (85, "%", "Satisfaction", (46, 204, 113, 255)),
    (12, "%", "Growth", (231, 76, 60, 255)),
    (45, "K", "Revenue", (155, 89, 182, 255)),
    (320, "", "Orders", (241, 196, 15, 255)),
    (98, "%", "Uptime", (26, 188, 156, 255)),
]

dashboard = create_dashboard(dashboard_metrics)
dashboard.save("performance_dashboard.png")
```

## 🎯 Practical Applications

### Watermarking and Branding

```python
def add_logo_watermark(image, logo_path, position="bottom_right", opacity=0.7, scale=0.1):
    """Add a logo watermark to an image."""
    # Load logo
    logo = puhu.open(logo_path).convert("RGBA")
    
    # Scale logo relative to image size
    img_width, img_height = image.size
    logo_width = int(img_width * scale)
    logo_height = int(logo.height * (logo_width / logo.width))
    logo_resized = logo.resize((logo_width, logo_height))
    
    # Adjust opacity
    # Note: This is a simplified opacity adjustment
    # Real implementation would require proper alpha blending
    
    # Calculate position
    margin = 20
    if position == "bottom_right":
        x = img_width - logo_width - margin
        y = img_height - logo_height - margin
    elif position == "bottom_left":
        x = margin
        y = img_height - logo_height - margin
    elif position == "top_right":
        x = img_width - logo_width - margin
        y = margin
    elif position == "top_left":
        x = margin
        y = margin
    elif position == "center":
        x = (img_width - logo_width) // 2
        y = (img_height - logo_height) // 2
    else:
        x, y = position  # Assume it's a tuple
    
    # Convert main image to RGBA for proper blending
    img_rgba = image.convert("RGBA")
    
    # Paste logo
    watermarked = img_rgba.paste(logo_resized, (x, y))
    
    return watermarked

def add_text_watermark(image, text, position="bottom_right", 
                      font_scale=2, color=(255, 255, 255, 180)):
    """Add a text watermark to an image."""
    img_width, img_height = image.size
    
    # Calculate text dimensions (approximate)
    text_width = len(text) * 8 * font_scale
    text_height = 12 * font_scale
    
    # Calculate position
    margin = 20
    if position == "bottom_right":
        x = img_width - text_width - margin
        y = img_height - text_height - margin
    elif position == "bottom_left":
        x = margin
        y = img_height - text_height - margin
    elif position == "top_right":
        x = img_width - text_width - margin
        y = margin
    elif position == "top_left":
        x = margin
        y = margin
    elif position == "center":
        x = (img_width - text_width) // 2
        y = (img_height - text_height) // 2
    else:
        x, y = position
    
    # Add text with shadow for better visibility
    result = image.draw_text(text, x + 2, y + 2, (0, 0, 0, 100), font_scale)  # Shadow
    result = result.draw_text(text, x, y, color, font_scale)  # Main text
    
    return result

# Usage
photo = puhu.open("photo.jpg")

# Add logo watermark
# logo_watermarked = add_logo_watermark(photo, "logo.png", "bottom_right", 0.8, 0.15)

# Add text watermark
text_watermarked = add_text_watermark(photo, "© 2024 Puhu Graphics", "bottom_right")

text_watermarked.save("watermarked_photo.jpg")
```

### Social Media Content Creation

```python
def create_instagram_post(image_path, caption, hashtags=None):
    """Create an Instagram-style post with image and text overlay."""
    # Load and prepare image
    img = puhu.open(image_path)
    
    # Instagram square format
    size = min(img.width, img.height)
    
    # Center crop to square
    left = (img.width - size) // 2
    top = (img.height - size) // 2
    square_img = img.crop((left, top, left + size, top + size))
    
    # Resize to Instagram size
    instagram_size = 1080
    final_img = square_img.resize((instagram_size, instagram_size))
    
    # Apply Instagram-style filter
    filtered = (final_img
                .saturate(1.2)
                .contrast(1.1)
                .brightness(5)
                .sharpen(1.05))
    
    # Add text overlay if caption is short enough
    if len(caption) <= 50:  # Short caption can be overlaid
        # Add semi-transparent background for text
        text_bg_height = 80
        text_bg = puhu.new("RGBA", (instagram_size, text_bg_height), (0, 0, 0, 120))
        
        # Paste text background
        filtered_rgba = filtered.convert("RGBA")
        with_bg = filtered_rgba.paste(text_bg, (0, instagram_size - text_bg_height))
        
        # Add caption text
        text_x = 20
        text_y = instagram_size - text_bg_height + 20
        final = with_bg.draw_text(caption, text_x, text_y, (255, 255, 255, 255), 2)
    else:
        final = filtered
    
    return final

def create_story_template(background_color=(255, 255, 255), accent_color=(52, 152, 219, 255)):
    """Create an Instagram story template."""
    # Instagram story dimensions
    story_width, story_height = 1080, 1920
    
    # Create background
    story = puhu.new("RGB", (story_width, story_height), background_color)
    
    # Add decorative elements
    # Top accent bar
    story = story.draw_rectangle(0, 0, story_width, 8, accent_color)
    
    # Decorative circles
    story = story.draw_circle(100, 200, 40, accent_color)
    story = story.draw_circle(story_width - 100, 200, 40, accent_color)
    
    # Text areas (placeholders)
    # Title area
    story = story.draw_rectangle(80, 300, story_width - 160, 100, (245, 245, 245, 255))
    story = story.draw_text("YOUR TITLE HERE", 100, 330, (128, 128, 128, 255), 3)
    
    # Content area
    story = story.draw_rectangle(80, 500, story_width - 160, 800, (250, 250, 250, 255))
    
    # Bottom accent
    story = story.draw_rectangle(0, story_height - 8, story_width, 8, accent_color)
    
    return story

# Usage
# instagram_post = create_instagram_post("photo.jpg", "Beautiful sunset! #photography")
story_template = create_story_template()

# instagram_post.save("instagram_post.jpg")
story_template.save("story_template.png")
```

### E-commerce Product Images

```python
def create_product_showcase(product_image_path, background_color="white"):
    """Create a clean product showcase image."""
    # Load product image
    product = puhu.open(product_image_path).convert("RGBA")
    
    # Create larger canvas with padding
    padding = 100
    canvas_width = product.width + 2 * padding
    canvas_height = product.height + 2 * padding
    
    # Create background
    showcase = puhu.new("RGB", (canvas_width, canvas_height), background_color)
    
    # Add subtle shadow to product
    product_with_shadow = product.drop_shadow(10, 10, 20.0, (0, 0, 0, 50))
    
    # Center product on canvas
    x = (canvas_width - product.width) // 2
    y = (canvas_height - product.height) // 2
    
    showcase = showcase.paste(product_with_shadow, (x, y))
    
    return showcase

def create_product_grid(product_images, grid_size=(2, 2), canvas_size=(1200, 1200)):
    """Create a product grid for catalogs."""
    cols, rows = grid_size
    canvas_width, canvas_height = canvas_size
    
    # Calculate cell dimensions
    cell_width = canvas_width // cols
    cell_height = canvas_height // rows
    
    # Create canvas
    grid = puhu.new("RGB", canvas_size, "white")
    
    # Add grid lines
    line_color = (230, 230, 230, 255)
    
    # Vertical lines
    for i in range(1, cols):
        x = i * cell_width
        grid = grid.draw_line(x, 0, x, canvas_height, line_color)
    
    # Horizontal lines
    for i in range(1, rows):
        y = i * cell_height
        grid = grid.draw_line(0, y, canvas_width, y, line_color)
    
    # Add products
    for i, product_path in enumerate(product_images[:cols * rows]):
        if not Path(product_path).exists():
            continue
            
        try:
            # Load and prepare product
            product = puhu.open(product_path)
            
            # Resize to fit cell with padding
            padding = 40
            max_size = (cell_width - padding, cell_height - padding)
            
            # Maintain aspect ratio
            aspect = product.width / product.height
            if aspect > 1:  # Wider than tall
                new_width = max_size[0]
                new_height = int(new_width / aspect)
            else:  # Taller than wide
                new_height = max_size[1]
                new_width = int(new_height * aspect)
            
            resized_product = product.resize((new_width, new_height))
            
            # Calculate position
            row = i // cols
            col = i % cols
            
            cell_x = col * cell_width
            cell_y = row * cell_height
            
            # Center product in cell
            x = cell_x + (cell_width - new_width) // 2
            y = cell_y + (cell_height - new_height) // 2
            
            grid = grid.paste(resized_product, (x, y))
            
        except Exception as e:
            print(f"Error processing {product_path}: {e}")
    
    return grid

# Usage
product_images = ["product1.jpg", "product2.jpg", "product3.jpg", "product4.jpg"]

# Individual product showcase
# product_showcase = create_product_showcase("product1.jpg")
# product_showcase.save("product_showcase.jpg")

# Product grid
product_grid = create_product_grid(product_images, (2, 2), (1000, 1000))
product_grid.save("product_grid.jpg")
```

## 🔧 Performance Examples

### Optimized Batch Processing

```python
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

def process_single_image(args):
    """Process a single image with given parameters."""
    input_path, output_path, operations = args
    
    try:
        # Load image
        img = puhu.open(input_path)
        
        # Apply operations
        result = img
        for operation, params in operations:
            if operation == "resize":
                result = result.resize(params)
            elif operation == "brightness":
                result = result.brightness(params)
            elif operation == "contrast":
                result = result.contrast(params)
            elif operation == "saturate":
                result = result.saturate(params)
            elif operation == "blur":
                result = result.blur(params)
            elif operation == "sharpen":
                result = result.sharpen(params)
        
        # Save result
        result.save(output_path)
        return f"Processed: {input_path} -> {output_path}"
        
    except Exception as e:
        return f"Error processing {input_path}: {e}"

def batch_process_parallel(input_dir, output_dir, operations, max_workers=4):
    """Process images in parallel for better performance."""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Prepare arguments for parallel processing
    args_list = []
    extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
    
    for image_file in input_path.iterdir():
        if image_file.suffix.lower() in extensions:
            output_file = output_path / image_file.name
            args_list.append((str(image_file), str(output_file), operations))
    
    # Process in parallel
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(process_single_image, args_list))
    
    end_time = time.time()
    
    # Print results
    for result in results:
        print(result)
    
    print(f"\nProcessed {len(args_list)} images in {end_time - start_time:.2f} seconds")
    print(f"Average time per image: {(end_time - start_time) / len(args_list):.2f} seconds")

# Usage
enhancement_operations = [
    ("resize", (800, 600)),
    ("brightness", 10),
    ("contrast", 1.1),
    ("saturate", 1.05),
    ("sharpen", 1.1),
]

# Process images in parallel
batch_process_parallel("input_photos", "enhanced_photos", enhancement_operations, max_workers=4)
```

### Memory-Efficient Processing

```python
def process_large_images_efficiently(image_paths, max_dimension=2000):
    """Process large images efficiently by resizing first."""
    results = []
    
    for image_path in image_paths:
        try:
            # Load image
            img = puhu.open(image_path)
            print(f"Processing {image_path}: {img.size}")
            
            # Check if image is too large
            if max(img.width, img.height) > max_dimension:
                # Calculate new size maintaining aspect ratio
                if img.width > img.height:
                    new_width = max_dimension
                    new_height = int(img.height * (max_dimension / img.width))
                else:
                    new_height = max_dimension
                    new_width = int(img.width * (max_dimension / img.height))
                
                print(f"  Resizing to {new_width}x{new_height} for efficiency")
                img = img.resize((new_width, new_height))
            
            # Apply processing
            processed = (img
                        .brightness(10)
                        .contrast(1.1)
                        .saturate(1.05)
                        .sharpen(1.1))
            
            # Save with optimized filename
            output_path = f"processed_{Path(image_path).stem}.jpg"
            processed.save(output_path)
            
            results.append(output_path)
            print(f"  Saved: {output_path}")
            
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
    
    return results

# Usage
large_images = ["large_photo1.jpg", "large_photo2.jpg", "large_photo3.jpg"]
processed_images = process_large_images_efficiently(large_images, 1500)
```

## 🔗 Next Steps

- **[API Reference](api-reference.md)** - Complete method documentation
- **[Performance Guide](performance.md)** - Optimization techniques
- **[Migration Guide](migration.md)** - Migrating from Pillow
- **[Contributing](contributing.md)** - How to contribute to Puhu