# Drawing Operations

Shape and text drawing capabilities in Puhu for creating graphics and annotations.

## 🎨 Overview

Puhu provides built-in drawing operations for creating shapes, lines, and text directly on images. These operations are optimized for performance and support alpha blending for smooth, professional-looking graphics.

## 📐 Shape Drawing

### Rectangles

#### `Image.draw_rectangle(x, y, width, height, color)`

Draw a filled rectangle on the image.

**Parameters:**
- `x` (int): Left edge X coordinate
- `y` (int): Top edge Y coordinate  
- `width` (int): Rectangle width
- `height` (int): Rectangle height
- `color` (tuple): RGBA color tuple `(r, g, b, a)`

**Returns:** New `Image` instance with rectangle drawn

**Examples:**

```python
import puhu

# Create a canvas
canvas = puhu.new("RGB", (400, 300), "white")

# Draw basic rectangles
red_rect = canvas.draw_rectangle(50, 50, 100, 80, (255, 0, 0, 255))
blue_rect = red_rect.draw_rectangle(200, 100, 120, 60, (0, 0, 255, 255))

# Draw with transparency
transparent_rect = blue_rect.draw_rectangle(100, 150, 150, 100, (0, 255, 0, 128))

# Chain multiple rectangles
multi_rect = (canvas
              .draw_rectangle(10, 10, 50, 50, (255, 0, 0, 255))
              .draw_rectangle(70, 10, 50, 50, (0, 255, 0, 255))
              .draw_rectangle(130, 10, 50, 50, (0, 0, 255, 255)))

# Create a grid pattern
def draw_grid(canvas, cell_size, grid_color=(200, 200, 200, 255)):
    """Draw a grid pattern on the canvas."""
    width, height = canvas.size
    cell_width, cell_height = cell_size
    
    result = canvas
    
    # Draw vertical lines (as thin rectangles)
    for x in range(0, width, cell_width):
        result = result.draw_rectangle(x, 0, 1, height, grid_color)
    
    # Draw horizontal lines
    for y in range(0, height, cell_height):
        result = result.draw_rectangle(0, y, width, 1, grid_color)
    
    return result

grid_canvas = draw_grid(canvas, (50, 50))

# Create a checkerboard pattern
def draw_checkerboard(size, cell_size, color1=(255, 255, 255, 255), color2=(0, 0, 0, 255)):
    """Create a checkerboard pattern."""
    width, height = size
    cell_width, cell_height = cell_size
    
    canvas = puhu.new("RGB", size, color1[:3])
    
    for y in range(0, height, cell_height):
        for x in range(0, width, cell_width):
            # Alternate colors based on position
            if (x // cell_width + y // cell_height) % 2 == 1:
                canvas = canvas.draw_rectangle(x, y, cell_width, cell_height, color2)
    
    return canvas

checkerboard = draw_checkerboard((400, 300), (40, 40))

# Draw overlapping rectangles with alpha blending
def draw_overlapping_demo(canvas):
    """Demonstrate alpha blending with overlapping rectangles."""
    return (canvas
            .draw_rectangle(50, 50, 150, 100, (255, 0, 0, 180))    # Semi-transparent red
            .draw_rectangle(100, 75, 150, 100, (0, 255, 0, 180))   # Semi-transparent green
            .draw_rectangle(75, 100, 150, 100, (0, 0, 255, 180)))  # Semi-transparent blue

overlapping = draw_overlapping_demo(canvas)
```

**Use Cases:**
- Creating UI elements and buttons
- Drawing backgrounds and frames
- Making geometric patterns
- Creating color swatches and palettes
- Building infographics and charts

### Circles

#### `Image.draw_circle(center_x, center_y, radius, color)`

Draw a filled circle on the image.

**Parameters:**
- `center_x` (int): Circle center X coordinate
- `center_y` (int): Circle center Y coordinate
- `radius` (int): Circle radius in pixels
- `color` (tuple): RGBA color tuple `(r, g, b, a)`

**Returns:** New `Image` instance with circle drawn

**Examples:**

```python
canvas = puhu.new("RGB", (400, 300), "white")

# Draw basic circles
red_circle = canvas.draw_circle(100, 100, 40, (255, 0, 0, 255))
blue_circle = red_circle.draw_circle(250, 150, 60, (0, 0, 255, 255))

# Draw with transparency
transparent_circle = blue_circle.draw_circle(175, 125, 50, (0, 255, 0, 128))

# Chain multiple circles
multi_circles = (canvas
                 .draw_circle(80, 80, 30, (255, 0, 0, 255))
                 .draw_circle(160, 80, 30, (0, 255, 0, 255))
                 .draw_circle(240, 80, 30, (0, 0, 255, 255))
                 .draw_circle(320, 80, 30, (255, 255, 0, 255)))

# Create concentric circles
def draw_concentric_circles(canvas, center, radii, colors):
    """Draw concentric circles with different colors."""
    center_x, center_y = center
    result = canvas
    
    # Draw from largest to smallest for proper layering
    for radius, color in zip(reversed(radii), reversed(colors)):
        result = result.draw_circle(center_x, center_y, radius, color)
    
    return result

radii = [60, 45, 30, 15]
colors = [(255, 0, 0, 255), (255, 128, 0, 255), (255, 255, 0, 255), (255, 255, 255, 255)]
concentric = draw_concentric_circles(canvas, (200, 150), radii, colors)

# Create a pattern of circles
def draw_circle_pattern(canvas, spacing=80):
    """Draw a pattern of circles across the canvas."""
    width, height = canvas.size
    result = canvas
    
    colors = [
        (255, 0, 0, 200),    # Red
        (0, 255, 0, 200),    # Green
        (0, 0, 255, 200),    # Blue
        (255, 255, 0, 200),  # Yellow
        (255, 0, 255, 200),  # Magenta
        (0, 255, 255, 200),  # Cyan
    ]
    
    color_index = 0
    for y in range(spacing//2, height, spacing):
        for x in range(spacing//2, width, spacing):
            color = colors[color_index % len(colors)]
            result = result.draw_circle(x, y, spacing//3, color)
            color_index += 1
    
    return result

circle_pattern = draw_circle_pattern(canvas, 70)

# Create Olympic rings
def draw_olympic_rings(canvas):
    """Draw the Olympic rings pattern."""
    # Ring positions and colors
    rings = [
        (120, 120, (0, 129, 200, 255)),    # Blue
        (200, 120, (0, 0, 0, 255)),        # Black
        (280, 120, (237, 41, 57, 255)),    # Red
        (160, 160, (255, 179, 0, 255)),    # Yellow
        (240, 160, (0, 166, 81, 255)),     # Green
    ]
    
    result = canvas
    radius = 35
    
    for x, y, color in rings:
        # Draw outer circle
        result = result.draw_circle(x, y, radius, color)
        # Draw inner circle (white) to create ring effect
        result = result.draw_circle(x, y, radius - 8, (255, 255, 255, 255))
    
    return result

olympic = draw_olympic_rings(puhu.new("RGB", (400, 300), "white"))
```

**Use Cases:**
- Creating dots and markers
- Drawing buttons and icons
- Making decorative patterns
- Creating logos and symbols
- Building data visualizations (scatter plots)

### Lines

#### `Image.draw_line(x1, y1, x2, y2, color)`

Draw a line between two points using Bresenham's algorithm.

**Parameters:**
- `x1, y1` (int): Starting point coordinates
- `x2, y2` (int): Ending point coordinates
- `color` (tuple): RGBA color tuple `(r, g, b, a)`

**Returns:** New `Image` instance with line drawn

**Examples:**

```python
canvas = puhu.new("RGB", (400, 300), "white")

# Draw basic lines
horizontal_line = canvas.draw_line(50, 150, 350, 150, (255, 0, 0, 255))
vertical_line = horizontal_line.draw_line(200, 50, 200, 250, (0, 255, 0, 255))
diagonal_line = vertical_line.draw_line(50, 50, 350, 250, (0, 0, 255, 255))

# Draw multiple lines
multi_lines = (canvas
               .draw_line(0, 0, 400, 300, (255, 0, 0, 255))
               .draw_line(400, 0, 0, 300, (0, 255, 0, 255))
               .draw_line(200, 0, 200, 300, (0, 0, 255, 255))
               .draw_line(0, 150, 400, 150, (255, 255, 0, 255)))

# Create a star pattern
def draw_star(canvas, center, size, color):
    """Draw a star shape using lines."""
    center_x, center_y = center
    result = canvas
    
    # Calculate star points
    import math
    points = []
    for i in range(10):  # 5 outer points + 5 inner points
        angle = i * math.pi / 5
        if i % 2 == 0:  # Outer points
            radius = size
        else:  # Inner points
            radius = size * 0.4
        
        x = center_x + int(radius * math.cos(angle - math.pi/2))
        y = center_y + int(radius * math.sin(angle - math.pi/2))
        points.append((x, y))
    
    # Draw lines connecting the points
    for i in range(len(points)):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % len(points)]
        result = result.draw_line(x1, y1, x2, y2, color)
    
    return result

star = draw_star(canvas, (200, 150), 80, (255, 0, 0, 255))

# Create a grid using lines
def draw_line_grid(canvas, cell_size, line_color=(128, 128, 128, 255)):
    """Draw a grid using lines."""
    width, height = canvas.size
    cell_width, cell_height = cell_size
    result = canvas
    
    # Vertical lines
    for x in range(0, width + 1, cell_width):
        result = result.draw_line(x, 0, x, height, line_color)
    
    # Horizontal lines
    for y in range(0, height + 1, cell_height):
        result = result.draw_line(0, y, width, y, line_color)
    
    return result

line_grid = draw_line_grid(canvas, (50, 50))

# Draw a sine wave
def draw_sine_wave(canvas, amplitude=50, frequency=2, color=(255, 0, 0, 255)):
    """Draw a sine wave across the canvas."""
    import math
    
    width, height = canvas.size
    center_y = height // 2
    result = canvas
    
    prev_x, prev_y = 0, center_y
    
    for x in range(1, width):
        y = center_y + int(amplitude * math.sin(2 * math.pi * frequency * x / width))
        result = result.draw_line(prev_x, prev_y, x, y, color)
        prev_x, prev_y = x, y
    
    return result

sine_wave = draw_sine_wave(canvas, 60, 3)

# Create a sunburst pattern
def draw_sunburst(canvas, center, num_rays=16, length=100, color=(255, 255, 0, 255)):
    """Draw a sunburst pattern."""
    import math
    
    center_x, center_y = center
    result = canvas
    
    for i in range(num_rays):
        angle = 2 * math.pi * i / num_rays
        end_x = center_x + int(length * math.cos(angle))
        end_y = center_y + int(length * math.sin(angle))
        result = result.draw_line(center_x, center_y, end_x, end_y, color)
    
    return result

sunburst = draw_sunburst(canvas, (200, 150), 20, 120)
```

**Use Cases:**
- Drawing borders and frames
- Creating geometric patterns
- Making graphs and charts
- Drawing arrows and connectors
- Creating artistic line patterns

## ✏️ Text Drawing

### Basic Text

#### `Image.draw_text(text, x, y, color, scale=1)`

Draw text on the image using a built-in bitmap font.

**Parameters:**
- `text` (str): Text to draw
- `x, y` (int): Text position (top-left corner)
- `color` (tuple): RGBA color tuple `(r, g, b, a)`
- `scale` (int): Text scale factor (1 = normal size, 2 = double size, etc.)

**Returns:** New `Image` instance with text drawn

**Examples:**

```python
canvas = puhu.new("RGB", (400, 300), "white")

# Draw basic text
hello_text = canvas.draw_text("Hello, Puhu!", 50, 50, (0, 0, 0, 255), 1)

# Draw text at different scales
scaled_text = (canvas
               .draw_text("Scale 1", 50, 50, (255, 0, 0, 255), 1)
               .draw_text("Scale 2", 50, 80, (0, 255, 0, 255), 2)
               .draw_text("Scale 3", 50, 120, (0, 0, 255, 255), 3))

# Draw text in different colors
colorful_text = (canvas
                 .draw_text("RED", 50, 50, (255, 0, 0, 255), 2)
                 .draw_text("GREEN", 50, 90, (0, 255, 0, 255), 2)
                 .draw_text("BLUE", 50, 130, (0, 0, 255, 255), 2)
                 .draw_text("YELLOW", 50, 170, (255, 255, 0, 255), 2))

# Create a title with shadow effect
def draw_text_with_shadow(canvas, text, x, y, text_color, shadow_color, scale=1, shadow_offset=(2, 2)):
    """Draw text with a drop shadow effect."""
    shadow_x = x + shadow_offset[0]
    shadow_y = y + shadow_offset[1]
    
    # Draw shadow first
    result = canvas.draw_text(text, shadow_x, shadow_y, shadow_color, scale)
    # Draw main text on top
    result = result.draw_text(text, x, y, text_color, scale)
    
    return result

title_with_shadow = draw_text_with_shadow(
    canvas, "PUHU GRAPHICS", 100, 100,
    (255, 255, 255, 255),  # White text
    (0, 0, 0, 128),        # Semi-transparent black shadow
    3, (3, 3)
)

# Create a text label with background
def draw_text_label(canvas, text, x, y, text_color, bg_color, scale=1, padding=5):
    """Draw text with a background rectangle."""
    # Estimate text dimensions (simplified)
    char_width = 8 * scale  # Approximate character width
    char_height = 12 * scale  # Approximate character height
    
    text_width = len(text) * char_width
    text_height = char_height
    
    # Draw background rectangle
    result = canvas.draw_rectangle(
        x - padding, y - padding,
        text_width + 2 * padding, text_height + 2 * padding,
        bg_color
    )
    
    # Draw text on top
    result = result.draw_text(text, x, y, text_color, scale)
    
    return result

labeled_text = draw_text_label(
    canvas, "LABEL", 150, 150,
    (255, 255, 255, 255),  # White text
    (255, 0, 0, 255),      # Red background
    2, 8
)

# Create multiple lines of text
def draw_multiline_text(canvas, lines, x, y, color, scale=1, line_spacing=None):
    """Draw multiple lines of text."""
    if line_spacing is None:
        line_spacing = 12 * scale + 4  # Default line spacing
    
    result = canvas
    current_y = y
    
    for line in lines:
        result = result.draw_text(line, x, current_y, color, scale)
        current_y += line_spacing
    
    return result

poem_lines = [
    "Roses are red,",
    "Violets are blue,",
    "Puhu draws text,",
    "And graphics too!"
]

poem = draw_multiline_text(canvas, poem_lines, 50, 50, (0, 0, 0, 255), 1, 20)

# Create centered text
def draw_centered_text(canvas, text, y, color, scale=1):
    """Draw text centered horizontally on the canvas."""
    width, height = canvas.size
    
    # Estimate text width
    char_width = 8 * scale
    text_width = len(text) * char_width
    
    # Calculate center position
    x = (width - text_width) // 2
    
    return canvas.draw_text(text, x, y, color, scale)

centered = draw_centered_text(canvas, "CENTERED TEXT", 150, (0, 0, 0, 255), 2)
```

**Use Cases:**
- Adding labels and annotations
- Creating titles and headers
- Making watermarks
- Building user interfaces
- Creating memes and captions

## 🎨 Complex Drawing Combinations

### Creating Logos and Icons

```python
def draw_simple_logo(size=(200, 200)):
    """Create a simple logo combining shapes and text."""
    canvas = puhu.new("RGB", size, "white")
    
    center_x, center_y = size[0] // 2, size[1] // 2
    
    # Draw background circle
    logo = canvas.draw_circle(center_x, center_y, 80, (0, 100, 200, 255))
    
    # Draw inner circle
    logo = logo.draw_circle(center_x, center_y, 60, (255, 255, 255, 255))
    
    # Draw letter "P"
    logo = logo.draw_text("P", center_x - 15, center_y - 15, (0, 100, 200, 255), 4)
    
    return logo

simple_logo = draw_simple_logo()

def draw_company_logo(canvas):
    """Create a more complex company logo."""
    # Background
    result = canvas.draw_rectangle(50, 50, 300, 100, (0, 50, 100, 255))
    
    # Company name
    result = result.draw_text("PUHU CORP", 70, 70, (255, 255, 255, 255), 3)
    
    # Decorative elements
    result = result.draw_circle(320, 75, 15, (255, 200, 0, 255))
    result = result.draw_circle(340, 75, 15, (255, 100, 0, 255))
    result = result.draw_circle(360, 75, 15, (255, 0, 0, 255))
    
    return result

company_logo = draw_company_logo(puhu.new("RGB", (400, 200), "white"))
```

### Creating Charts and Graphs

```python
def draw_bar_chart(canvas, data, labels, colors=None):
    """Draw a simple bar chart."""
    if colors is None:
        colors = [(255, 0, 0, 255), (0, 255, 0, 255), (0, 0, 255, 255), 
                 (255, 255, 0, 255), (255, 0, 255, 255)]
    
    width, height = canvas.size
    chart_area_height = height - 100  # Leave space for labels
    max_value = max(data) if data else 1
    
    bar_width = (width - 100) // len(data)
    result = canvas
    
    for i, (value, label) in enumerate(zip(data, labels)):
        # Calculate bar height
        bar_height = int((value / max_value) * chart_area_height)
        
        # Bar position
        x = 50 + i * bar_width
        y = height - 50 - bar_height
        
        # Draw bar
        color = colors[i % len(colors)]
        result = result.draw_rectangle(x, y, bar_width - 10, bar_height, color)
        
        # Draw label
        result = result.draw_text(label, x, height - 40, (0, 0, 0, 255), 1)
        
        # Draw value
        result = result.draw_text(str(value), x, y - 20, (0, 0, 0, 255), 1)
    
    return result

# Sample data
chart_data = [25, 40, 30, 55, 20]
chart_labels = ["A", "B", "C", "D", "E"]

bar_chart = draw_bar_chart(
    puhu.new("RGB", (400, 300), "white"),
    chart_data, chart_labels
)

def draw_pie_chart(canvas, data, labels, colors=None):
    """Draw a simple pie chart."""
    import math
    
    if colors is None:
        colors = [(255, 0, 0, 255), (0, 255, 0, 255), (0, 0, 255, 255),
                 (255, 255, 0, 255), (255, 0, 255, 255), (0, 255, 255, 255)]
    
    width, height = canvas.size
    center_x, center_y = width // 2, height // 2
    radius = min(width, height) // 3
    
    total = sum(data)
    result = canvas
    
    current_angle = 0
    
    for i, (value, label) in enumerate(zip(data, labels)):
        # Calculate slice angle
        slice_angle = (value / total) * 2 * math.pi
        
        # Draw slice (simplified - using lines from center)
        color = colors[i % len(colors)]
        
        # Draw multiple lines to fill the slice
        num_lines = int(slice_angle * radius / 2)  # Approximate fill
        for j in range(num_lines):
            angle = current_angle + (j / num_lines) * slice_angle
            end_x = center_x + int(radius * math.cos(angle))
            end_y = center_y + int(radius * math.sin(angle))
            result = result.draw_line(center_x, center_y, end_x, end_y, color)
        
        # Draw label
        label_angle = current_angle + slice_angle / 2
        label_x = center_x + int((radius + 20) * math.cos(label_angle))
        label_y = center_y + int((radius + 20) * math.sin(label_angle))
        result = result.draw_text(label, label_x, label_y, (0, 0, 0, 255), 1)
        
        current_angle += slice_angle
    
    return result

pie_chart = draw_pie_chart(
    puhu.new("RGB", (400, 400), "white"),
    chart_data, chart_labels
)
```

### Creating Decorative Patterns

```python
def draw_mandala_pattern(canvas, center, radius, num_petals=8):
    """Draw a simple mandala pattern."""
    import math
    
    center_x, center_y = center
    result = canvas
    
    # Draw concentric circles
    for r in range(radius // 4, radius, radius // 8):
        result = result.draw_circle(center_x, center_y, r, (100, 100, 100, 100))
    
    # Draw radiating lines
    for i in range(num_petals * 2):
        angle = 2 * math.pi * i / (num_petals * 2)
        end_x = center_x + int(radius * math.cos(angle))
        end_y = center_y + int(radius * math.sin(angle))
        result = result.draw_line(center_x, center_y, end_x, end_y, (150, 150, 150, 150))
    
    # Draw petal shapes (simplified as circles)
    for i in range(num_petals):
        angle = 2 * math.pi * i / num_petals
        petal_x = center_x + int((radius * 0.7) * math.cos(angle))
        petal_y = center_y + int((radius * 0.7) * math.sin(angle))
        result = result.draw_circle(petal_x, petal_y, radius // 6, (200, 100, 200, 180))
    
    # Center circle
    result = result.draw_circle(center_x, center_y, radius // 8, (255, 255, 255, 255))
    
    return result

mandala = draw_mandala_pattern(
    puhu.new("RGB", (400, 400), "white"),
    (200, 200), 150, 12
)

def draw_geometric_pattern(canvas, pattern_type="triangles"):
    """Draw various geometric patterns."""
    width, height = canvas.size
    result = canvas
    
    if pattern_type == "triangles":
        # Draw triangular pattern
        size = 40
        for y in range(0, height, size):
            for x in range(0, width, size * 2):
                # Upward triangle
                result = result.draw_line(x, y + size, x + size, y, (255, 0, 0, 255))
                result = result.draw_line(x + size, y, x + size * 2, y + size, (255, 0, 0, 255))
                result = result.draw_line(x + size * 2, y + size, x, y + size, (255, 0, 0, 255))
    
    elif pattern_type == "hexagons":
        # Draw hexagonal pattern (simplified as circles)
        size = 30
        for y in range(size, height, size * 2):
            for x in range(size, width, size * 2):
                result = result.draw_circle(x, y, size // 2, (0, 255, 0, 100))
    
    return result

triangle_pattern = draw_geometric_pattern(
    puhu.new("RGB", (400, 300), "white"),
    "triangles"
)
```

## 🎯 Practical Applications

### Creating Watermarks

```python
def add_watermark(image, text, position="bottom_right", opacity=128):
    """Add a text watermark to an image."""
    width, height = image.size
    
    # Calculate position
    if position == "bottom_right":
        x = width - len(text) * 8 - 20
        y = height - 30
    elif position == "bottom_left":
        x = 20
        y = height - 30
    elif position == "top_right":
        x = width - len(text) * 8 - 20
        y = 20
    elif position == "top_left":
        x = 20
        y = 20
    elif position == "center":
        x = (width - len(text) * 8) // 2
        y = height // 2
    else:
        x, y = position  # Assume it's a tuple
    
    # Add watermark
    return image.draw_text(text, x, y, (255, 255, 255, opacity), 1)

# Apply watermark to an image
img = puhu.open("photo.jpg")
watermarked = add_watermark(img, "© 2024 Puhu", "bottom_right", 150)

def add_logo_watermark(image, logo_size=(100, 50), position="bottom_right", opacity=128):
    """Add a logo watermark to an image."""
    width, height = image.size
    logo_width, logo_height = logo_size
    
    # Calculate position
    if position == "bottom_right":
        x = width - logo_width - 20
        y = height - logo_height - 20
    elif position == "bottom_left":
        x = 20
        y = height - logo_height - 20
    elif position == "top_right":
        x = width - logo_width - 20
        y = 20
    elif position == "top_left":
        x = 20
        y = 20
    else:
        x, y = position
    
    # Create simple logo
    result = image.draw_rectangle(x, y, logo_width, logo_height, (0, 0, 0, opacity))
    result = result.draw_text("LOGO", x + 10, y + 15, (255, 255, 255, 255), 2)
    
    return result

logo_watermarked = add_logo_watermark(img, (120, 40), "top_right", 100)
```

### Creating Annotations

```python
def add_annotation(image, text, point, arrow_length=30, color=(255, 0, 0, 255)):
    """Add an annotation with an arrow pointing to a specific location."""
    point_x, point_y = point
    
    # Calculate text position (offset from point)
    text_x = point_x + arrow_length + 10
    text_y = point_y - 10
    
    # Draw arrow line
    result = image.draw_line(point_x, point_y, text_x - 10, text_y + 5, color)
    
    # Draw arrowhead (simplified)
    result = result.draw_line(text_x - 10, text_y + 5, text_x - 15, text_y, color)
    result = result.draw_line(text_x - 10, text_y + 5, text_x - 15, text_y + 10, color)
    
    # Draw text with background
    text_bg_color = (255, 255, 255, 200)
    result = result.draw_rectangle(text_x - 5, text_y - 5, len(text) * 8 + 10, 20, text_bg_color)
    result = result.draw_text(text, text_x, text_y, (0, 0, 0, 255), 1)
    
    return result

# Add annotations to an image
annotated = add_annotation(img, "Important feature", (150, 100))
annotated = add_annotation(annotated, "Another detail", (300, 200), color=(0, 255, 0, 255))

def create_measurement_overlay(image, measurements):
    """Add measurement overlays to an image."""
    result = image
    
    for measurement in measurements:
        start_point, end_point, distance, unit = measurement
        x1, y1 = start_point
        x2, y2 = end_point
        
        # Draw measurement line
        result = result.draw_line(x1, y1, x2, y2, (255, 255, 0, 255))
        
        # Draw end markers
        result = result.draw_circle(x1, y1, 3, (255, 255, 0, 255))
        result = result.draw_circle(x2, y2, 3, (255, 255, 0, 255))
        
        # Draw measurement text
        mid_x = (x1 + x2) // 2
        mid_y = (y1 + y2) // 2 - 15
        text = f"{distance}{unit}"
        result = result.draw_text(text, mid_x, mid_y, (255, 255, 0, 255), 1)
    
    return result

# Example measurements
measurements = [
    ((50, 50), (200, 50), 150, "px"),
    ((50, 50), (50, 150), 100, "px"),
]

measured = create_measurement_overlay(img, measurements)
```

### Creating Infographics

```python
def create_infographic_element(canvas, title, value, unit, position, color):
    """Create a single infographic element."""
    x, y = position
    
    # Background circle
    result = canvas.draw_circle(x + 50, y + 50, 40, color)
    
    # Value text
    result = result.draw_text(str(value), x + 35, y + 40, (255, 255, 255, 255), 2)
    
    # Unit text
    result = result.draw_text(unit, x + 45, y + 60, (255, 255, 255, 255), 1)
    
    # Title text
    result = result.draw_text(title, x, y + 110, (0, 0, 0, 255), 1)
    
    return result

def create_dashboard(size=(600, 400)):
    """Create a simple dashboard with multiple metrics."""
    canvas = puhu.new("RGB", size, (240, 240, 240))
    
    # Title
    result = canvas.draw_text("DASHBOARD", 200, 30, (0, 0, 0, 255), 3)
    
    # Metrics
    metrics = [
        ("Users", 1250, "K", (100, 100), (52, 152, 219, 255)),
        ("Sales", 85, "%", (250, 100), (46, 204, 113, 255)),
        ("Growth", 12, "%", (400, 100), (231, 76, 60, 255)),
        ("Revenue", 45, "K", (175, 250), (155, 89, 182, 255)),
        ("Orders", 320, "", (325, 250), (241, 196, 15, 255)),
    ]
    
    for title, value, unit, position, color in metrics:
        result = create_infographic_element(result, title, value, unit, position, color)
    
    return result

dashboard = create_dashboard()
```

## 🔧 Performance Tips

### Efficient Drawing

```python
# Efficient: Chain drawing operations
efficient_drawing = (canvas
                     .draw_rectangle(50, 50, 100, 100, (255, 0, 0, 255))
                     .draw_circle(200, 100, 50, (0, 255, 0, 255))
                     .draw_text("Efficient", 100, 200, (0, 0, 0, 255), 2))

# Less efficient: Multiple intermediate variables
# temp1 = canvas.draw_rectangle(50, 50, 100, 100, (255, 0, 0, 255))
# temp2 = temp1.draw_circle(200, 100, 50, (0, 255, 0, 255))
# result = temp2.draw_text("Less efficient", 100, 200, (0, 0, 0, 255), 2)

# Batch drawing operations
def batch_draw_shapes(canvas, shapes):
    """Draw multiple shapes efficiently."""
    result = canvas
    
    for shape in shapes:
        shape_type = shape["type"]
        if shape_type == "rectangle":
            result = result.draw_rectangle(
                shape["x"], shape["y"], shape["width"], shape["height"], shape["color"]
            )
        elif shape_type == "circle":
            result = result.draw_circle(
                shape["x"], shape["y"], shape["radius"], shape["color"]
            )
        elif shape_type == "line":
            result = result.draw_line(
                shape["x1"], shape["y1"], shape["x2"], shape["y2"], shape["color"]
            )
        elif shape_type == "text":
            result = result.draw_text(
                shape["text"], shape["x"], shape["y"], shape["color"], shape.get("scale", 1)
            )
    
    return result

# Define shapes to draw
shapes_to_draw = [
    {"type": "rectangle", "x": 50, "y": 50, "width": 100, "height": 80, "color": (255, 0, 0, 255)},
    {"type": "circle", "x": 200, "y": 100, "radius": 40, "color": (0, 255, 0, 255)},
    {"type": "line", "x1": 50, "y1": 200, "x2": 250, "y2": 200, "color": (0, 0, 255, 255)},
    {"type": "text", "text": "Batch Drawing", "x": 100, "y": 250, "color": (0, 0, 0, 255), "scale": 2},
]

batch_result = batch_draw_shapes(canvas, shapes_to_draw)
```

## 🔗 Next Steps

- **[Shadow Effects](shadows.md)** - Drop shadows and glow effects
- **[Compositing & Blending](compositing.md)** - Advanced image compositing
- **[Examples](examples.md)** - Real-world drawing examples
- **[Performance Guide](performance.md)** - Optimization techniques
- **[API Reference](api-reference.md)** - Complete method documentation