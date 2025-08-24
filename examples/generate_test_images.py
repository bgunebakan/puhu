#!/usr/bin/env python3
"""
Generate test images for Puhu examples using PIL/Pillow.
This script creates various test images that can be used to demonstrate Puhu functionality.
"""

import os
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
    import numpy as np
    HAS_DEPS = True
except ImportError as e:
    print(f"Missing dependencies: {e}")
    print("Install with: pip install Pillow numpy")
    HAS_DEPS = False

def create_gradient_image(width=300, height=200, filename="gradient.png"):
    """Create a gradient image."""
    img = Image.new('RGB', (width, height))
    pixels = img.load()
    
    for x in range(width):
        for y in range(height):
            # Create a diagonal gradient
            r = int(255 * x / width)
            g = int(255 * y / height)
            b = int(255 * (x + y) / (width + height))
            pixels[x, y] = (r, g, b)
    
    return img

def create_colorful_squares(width=400, height=300, filename="colorful_squares.png"):
    """Create an image with colorful squares."""
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    colors = [
        (255, 0, 0),    # Red
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (255, 255, 0),  # Yellow
        (255, 0, 255),  # Magenta
        (0, 255, 255),  # Cyan
        (255, 128, 0),  # Orange
        (128, 0, 255),  # Purple
    ]
    
    square_size = 80
    cols = width // square_size
    rows = height // square_size
    
    for row in range(rows):
        for col in range(cols):
            color_idx = (row * cols + col) % len(colors)
            x1 = col * square_size
            y1 = row * square_size
            x2 = x1 + square_size
            y2 = y1 + square_size
            
            draw.rectangle([x1, y1, x2, y2], fill=colors[color_idx])
    
    return img

def create_geometric_pattern(width=350, height=350, filename="geometric.png"):
    """Create a geometric pattern."""
    img = Image.new('RGB', (width, height), 'black')
    draw = ImageDraw.Draw(img)
    
    center_x, center_y = width // 2, height // 2
    
    # Draw concentric circles
    for i in range(10):
        radius = 20 + i * 15
        color_intensity = 255 - i * 20
        color = (color_intensity, color_intensity // 2, 255 - color_intensity)
        
        draw.ellipse([
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius
        ], outline=color, width=3)
    
    # Draw lines
    for angle in range(0, 360, 30):
        import math
        end_x = center_x + int(150 * math.cos(math.radians(angle)))
        end_y = center_y + int(150 * math.sin(math.radians(angle)))
        draw.line([center_x, center_y, end_x, end_y], fill=(255, 255, 255), width=2)
    
    return img

def create_text_image(width=500, height=200, filename="text_sample.png"):
    """Create an image with text."""
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # Try to use a default font, fallback to basic if not available
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
    except:
        try:
            font = ImageFont.load_default()
        except:
            font = None
    
    text = "Puhu Image Processing"
    
    # Get text size and center it
    if font:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    else:
        text_width, text_height = 200, 20  # Rough estimate
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Draw text with shadow
    draw.text((x + 2, y + 2), text, fill='gray', font=font)
    draw.text((x, y), text, fill='black', font=font)
    
    # Add some decorative elements
    draw.rectangle([10, 10, width-10, height-10], outline='blue', width=3)
    
    return img

def create_alpha_test_image(width=200, height=200, filename="alpha_test.png"):
    """Create an RGBA image for alpha testing."""
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))  # Transparent background
    draw = ImageDraw.Draw(img)
    
    # Draw overlapping circles with different alpha values
    colors = [
        (255, 0, 0, 128),    # Semi-transparent red
        (0, 255, 0, 128),    # Semi-transparent green
        (0, 0, 255, 128),    # Semi-transparent blue
    ]
    
    positions = [(50, 50), (100, 50), (75, 100)]
    
    for i, (color, pos) in enumerate(zip(colors, positions)):
        draw.ellipse([
            pos[0] - 40, pos[1] - 40,
            pos[0] + 40, pos[1] + 40
        ], fill=color)
    
    return img

def create_noise_image(width=300, height=200, filename="noise.png"):
    """Create a noisy image using numpy."""
    if not HAS_DEPS:
        return None
        
    # Create random noise
    noise = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
    
    # Add some structure to make it more interesting
    for y in range(height):
        for x in range(width):
            # Add some patterns
            if (x + y) % 20 < 10:
                noise[y, x] = [noise[y, x, 0], 0, 0]  # Red stripes
            if x % 30 < 15:
                noise[y, x, 1] = min(255, noise[y, x, 1] + 50)  # Green enhancement
    
    return Image.fromarray(noise)

def main():
    """Generate all test images."""
    if not HAS_DEPS:
        print("Cannot generate test images without PIL and numpy")
        return 1
    
    # Create output directory
    img_dir = Path("examples/img")
    img_dir.mkdir(parents=True, exist_ok=True)
    
    print("Generating test images...")
    
    # Generate various test images
    images = [
        ("gradient.png", create_gradient_image()),
        ("colorful_squares.png", create_colorful_squares()),
        ("geometric.png", create_geometric_pattern()),
        ("text_sample.png", create_text_image()),
        ("alpha_test.png", create_alpha_test_image()),
        ("noise.png", create_noise_image()),
    ]
    
    for filename, img in images:
        if img is not None:
            filepath = img_dir / filename
            img.save(filepath)
            print(f"✓ Created {filepath}")
        else:
            print(f"✗ Failed to create {filename}")
    
    print(f"\nGenerated {len([i for i in images if i[1] is not None])} test images in {img_dir}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
