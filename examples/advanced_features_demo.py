#!/usr/bin/env python3
"""
Advanced Features Demo for Puhu Image Processing Library

This example demonstrates all the newly implemented advanced features:
- CSS-like filters (sepia, grayscale, invert, hue_rotate, saturate)
- Pixel manipulation (getpixel, putpixel, histogram, etc.)
- Drawing operations (rectangles, circles, lines, text)
- Shadow effects (drop_shadow, inner_shadow, glow)
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the path to import puhu
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python'))

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

def setup_paths():
    """Setup input and output paths."""
    examples_dir = Path(__file__).parent
    img_dir = examples_dir / "img"
    output_dir = examples_dir / "output"
    output_dir.mkdir(exist_ok=True)
    return img_dir, output_dir

def test_css_filters():
    """Test CSS-like filters."""
    import puhu
    
    img_dir, output_dir = setup_paths()
    
    print("\n" + "="*60)
    print("CSS-LIKE FILTERS")
    print("="*60)
    
    # Load test image
    img = puhu.open(str(img_dir / "colorful_squares.png"))
    print(f"Original image: {img.mode} {img.size}")
    
    # Test CSS filters
    filters = [
        ("sepia", lambda x: x.sepia(1.0)),
        ("grayscale", lambda x: x.grayscale_filter(1.0)),
        ("invert", lambda x: x.invert(1.0)),
        ("hue_rotate", lambda x: x.hue_rotate(90)),
        ("saturate", lambda x: x.saturate(2.0)),
    ]
    
    for name, filter_func in filters:
        try:
            filtered = filter_func(img)
            output_path = output_dir / f"css_{name}.png"
            filtered.save(str(output_path))
            print(f"✓ {name.capitalize()}: -> {output_path.name}")
        except Exception as e:
            print(f"✗ {name.capitalize()} failed: {e}")
    
    return True

def test_pixel_manipulation():
    """Test pixel manipulation functions."""
    import puhu
    
    img_dir, output_dir = setup_paths()
    
    print("\n" + "="*60)
    print("PIXEL MANIPULATION")
    print("="*60)
    
    # Load test image
    img = puhu.open(str(img_dir / "colorful_squares.png"))
    print(f"Original image: {img.mode} {img.size}")
    
    # Test getpixel
    try:
        pixel = img.getpixel(50, 50)
        print(f"✓ Pixel at (50, 50): {pixel}")
    except Exception as e:
        print(f"✗ getpixel failed: {e}")
    
    # Test putpixel
    try:
        modified = img.putpixel(50, 50, (255, 0, 0, 255))
        modified.save(str(output_dir / "putpixel_test.png"))
        print(f"✓ putpixel: Modified pixel at (50, 50)")
    except Exception as e:
        print(f"✗ putpixel failed: {e}")
    
    # Test histogram
    try:
        r_hist, g_hist, b_hist, a_hist = img.histogram()
        print(f"✓ Histogram: R={len(r_hist)}, G={len(g_hist)}, B={len(b_hist)}, A={len(a_hist)}")
    except Exception as e:
        print(f"✗ histogram failed: {e}")
    
    # Test dominant color
    try:
        dominant = img.dominant_color()
        print(f"✓ Dominant color: {dominant}")
    except Exception as e:
        print(f"✗ dominant_color failed: {e}")
    
    # Test average color
    try:
        average = img.average_color()
        print(f"✓ Average color: {average}")
    except Exception as e:
        print(f"✗ average_color failed: {e}")
    
    # Test replace color
    try:
        replaced = img.replace_color((255, 255, 255, 255), (255, 0, 0, 255), 10)
        replaced.save(str(output_dir / "replace_color.png"))
        print(f"✓ replace_color: Replaced white with red")
    except Exception as e:
        print(f"✗ replace_color failed: {e}")
    
    # Test threshold
    try:
        thresholded = img.threshold(128)
        thresholded.save(str(output_dir / "threshold.png"))
        print(f"✓ threshold: Applied threshold at 128")
    except Exception as e:
        print(f"✗ threshold failed: {e}")
    
    # Test posterize
    try:
        posterized = img.posterize(4)
        posterized.save(str(output_dir / "posterize.png"))
        print(f"✓ posterize: Reduced to 4 levels")
    except Exception as e:
        print(f"✗ posterize failed: {e}")
    
    return True

def test_drawing_operations():
    """Test drawing operations."""
    import puhu
    
    img_dir, output_dir = setup_paths()
    
    print("\n" + "="*60)
    print("DRAWING OPERATIONS")
    print("="*60)
    
    # Create a canvas
    canvas = puhu.new("RGB", (400, 300), (255, 255, 255))
    print(f"Canvas created: {canvas.mode} {canvas.size}")
    
    # Test draw_rectangle
    try:
        canvas = canvas.draw_rectangle(50, 50, 100, 80, (255, 0, 0, 255))
        print(f"✓ draw_rectangle: Red rectangle at (50, 50)")
    except Exception as e:
        print(f"✗ draw_rectangle failed: {e}")
    
    # Test draw_circle
    try:
        canvas = canvas.draw_circle(200, 150, 40, (0, 255, 0, 255))
        print(f"✓ draw_circle: Green circle at (200, 150)")
    except Exception as e:
        print(f"✗ draw_circle failed: {e}")
    
    # Test draw_line
    try:
        canvas = canvas.draw_line(10, 10, 390, 290, (0, 0, 255, 255))
        print(f"✓ draw_line: Blue diagonal line")
    except Exception as e:
        print(f"✗ draw_line failed: {e}")
    
    # Test draw_text
    try:
        canvas = canvas.draw_text("PUHU", 150, 200, (0, 0, 0, 255), 2)
        print(f"✓ draw_text: 'PUHU' text at (150, 200)")
    except Exception as e:
        print(f"✗ draw_text failed: {e}")
    
    # Save canvas
    canvas.save(str(output_dir / "drawing_test.png"))
    print(f"✓ Drawing test saved")
    
    return True

def test_shadow_effects():
    """Test shadow effects."""
    import puhu
    
    img_dir, output_dir = setup_paths()
    
    print("\n" + "="*60)
    print("SHADOW EFFECTS")
    print("="*60)
    
    # Load test image
    img = puhu.open(str(img_dir / "geometric.png"))
    print(f"Original image: {img.mode} {img.size}")
    
    # Test drop_shadow
    try:
        shadow = img.drop_shadow(10, 10, 5.0, (0, 0, 0, 128))
        shadow.save(str(output_dir / "drop_shadow.png"))
        print(f"✓ drop_shadow: Applied drop shadow")
    except Exception as e:
        print(f"✗ drop_shadow failed: {e}")
    
    # Test inner_shadow
    try:
        inner = img.inner_shadow(5, 5, 3.0, (0, 0, 0, 100))
        inner.save(str(output_dir / "inner_shadow.png"))
        print(f"✓ inner_shadow: Applied inner shadow")
    except Exception as e:
        print(f"✗ inner_shadow failed: {e}")
    
    # Test glow
    try:
        glow = img.glow(8.0, (255, 255, 0, 150), 1.5)
        glow.save(str(output_dir / "glow.png"))
        print(f"✓ glow: Applied yellow glow")
    except Exception as e:
        print(f"✗ glow failed: {e}")
    
    return True

def main():
    """Run advanced features demo."""
    try:
        import puhu
        print("✓ Puhu imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import puhu: {e}")
        print("Make sure to build the Rust extension with: maturin develop")
        return 1

    print("Puhu Advanced Features Demo")
    print("This script demonstrates all newly implemented advanced features")
    
    img_dir, output_dir = setup_paths()
    
    try:
        test_css_filters()
        test_pixel_manipulation()
        test_drawing_operations()
        test_shadow_effects()
        
        print("\n" + "="*60)
        print("🎉 ALL ADVANCED FEATURES DEMOS COMPLETED!")
        print("="*60)
        print(f"Check the output directory: {output_dir}")
        print("\nAdvanced features demonstrated:")
        print("• CSS-like filters (sepia, grayscale, invert, hue_rotate, saturate)")
        print("• Pixel manipulation (getpixel, putpixel, histogram, etc.)")
        print("• Drawing operations (rectangles, circles, lines, text)")
        print("• Shadow effects (drop_shadow, inner_shadow, glow)")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error during advanced features demo: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
