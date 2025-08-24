#!/usr/bin/env python3
"""
Filters Demo for Puhu Image Processing Library

This example demonstrates the newly implemented filter functionality:
- blur(): Gaussian blur
- sharpen(): Sharpening filter
- edge_detect(): Edge detection (Sobel operator)
- emboss(): Emboss effect
- brightness(): Brightness adjustment
- contrast(): Contrast adjustment
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the path to import puhu
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python'))

def setup_paths():
    """Setup input and output paths."""
    examples_dir = Path(__file__).parent
    img_dir = examples_dir / "img"
    output_dir = examples_dir / "output"
    output_dir.mkdir(exist_ok=True)
    return img_dir, output_dir

def test_blur_filters():
    """Test blur filters with different radii."""
    import puhu
    
    img_dir, output_dir = setup_paths()
    
    print("\n" + "="*60)
    print("BLUR FILTERS")
    print("="*60)
    
    # Load test image
    img = puhu.open(str(img_dir / "colorful_squares.png"))
    print(f"Original image: {img.mode} {img.size}")
    
    # Test different blur radii
    blur_radii = [1.0, 2.0, 5.0, 10.0]
    
    for radius in blur_radii:
        blurred = img.blur(radius)
        output_path = output_dir / f"blur_radius_{radius:.1f}.png"
        blurred.save(str(output_path))
        print(f"✓ Blur radius {radius}: -> {output_path.name}")
    
    # Test functional API
    func_blurred = puhu.blur(img, 3.0)
    func_blurred.save(str(output_dir / "blur_functional.png"))
    print(f"✓ Functional blur API")
    
    return True

def test_sharpening_filters():
    """Test sharpening filters with different strengths."""
    import puhu
    
    img_dir, output_dir = setup_paths()
    
    print("\n" + "="*60)
    print("SHARPENING FILTERS")
    print("="*60)
    
    # Load test image
    img = puhu.open(str(img_dir / "geometric.png"))
    print(f"Original image: {img.mode} {img.size}")
    
    # Test different sharpening strengths
    strengths = [0.5, 1.0, 2.0, 3.0]
    
    for strength in strengths:
        sharpened = img.sharpen(strength)
        output_path = output_dir / f"sharpen_strength_{strength:.1f}.png"
        sharpened.save(str(output_path))
        print(f"✓ Sharpen strength {strength}: -> {output_path.name}")
    
    # Test functional API
    func_sharpened = puhu.sharpen(img, 1.5)
    func_sharpened.save(str(output_dir / "sharpen_functional.png"))
    print(f"✓ Functional sharpen API")
    
    return True

def test_edge_detection():
    """Test edge detection filter."""
    import puhu
    
    img_dir, output_dir = setup_paths()
    
    print("\n" + "="*60)
    print("EDGE DETECTION")
    print("="*60)
    
    # Test on different images
    test_images = [
        ("colorful_squares.png", "squares"),
        ("geometric.png", "geometric"),
        ("text_sample.png", "text"),
    ]
    
    for filename, suffix in test_images:
        img = puhu.open(str(img_dir / filename))
        print(f"Processing {filename}: {img.mode} {img.size}")
        
        # Apply edge detection
        edges = img.edge_detect()
        output_path = output_dir / f"edges_{suffix}.png"
        edges.save(str(output_path))
        print(f"✓ Edge detection: -> {output_path.name}")
    
    # Test functional API
    img = puhu.open(str(img_dir / "gradient.png"))
    func_edges = puhu.edge_detect(img)
    func_edges.save(str(output_dir / "edges_functional.png"))
    print(f"✓ Functional edge detection API")
    
    return True

def test_emboss_filter():
    """Test emboss filter."""
    import puhu
    
    img_dir, output_dir = setup_paths()
    
    print("\n" + "="*60)
    print("EMBOSS FILTER")
    print("="*60)
    
    # Test on different images
    test_images = [
        ("colorful_squares.png", "squares"),
        ("geometric.png", "geometric"),
        ("text_sample.png", "text"),
    ]
    
    for filename, suffix in test_images:
        img = puhu.open(str(img_dir / filename))
        print(f"Processing {filename}: {img.mode} {img.size}")
        
        # Apply emboss
        embossed = img.emboss()
        output_path = output_dir / f"emboss_{suffix}.png"
        embossed.save(str(output_path))
        print(f"✓ Emboss: -> {output_path.name}")
    
    # Test functional API
    img = puhu.open(str(img_dir / "gradient.png"))
    func_embossed = puhu.emboss(img)
    func_embossed.save(str(output_dir / "emboss_functional.png"))
    print(f"✓ Functional emboss API")
    
    return True

def test_brightness_adjustment():
    """Test brightness adjustment."""
    import puhu
    
    img_dir, output_dir = setup_paths()
    
    print("\n" + "="*60)
    print("BRIGHTNESS ADJUSTMENT")
    print("="*60)
    
    # Load test image
    img = puhu.open(str(img_dir / "colorful_squares.png"))
    print(f"Original image: {img.mode} {img.size}")
    
    # Test different brightness adjustments
    adjustments = [-100, -50, 0, 50, 100]
    
    for adj in adjustments:
        brightened = img.brightness(adj)
        output_path = output_dir / f"brightness_{adj:+d}.png"
        brightened.save(str(output_path))
        print(f"✓ Brightness {adj:+d}: -> {output_path.name}")
    
    # Test functional API
    func_bright = puhu.brightness(img, 75)
    func_bright.save(str(output_dir / "brightness_functional.png"))
    print(f"✓ Functional brightness API")
    
    return True

def test_contrast_adjustment():
    """Test contrast adjustment."""
    import puhu
    
    img_dir, output_dir = setup_paths()
    
    print("\n" + "="*60)
    print("CONTRAST ADJUSTMENT")
    print("="*60)
    
    # Load test image
    img = puhu.open(str(img_dir / "gradient.png"))
    print(f"Original image: {img.mode} {img.size}")
    
    # Test different contrast factors
    factors = [0.5, 0.8, 1.0, 1.5, 2.0]
    
    for factor in factors:
        contrasted = img.contrast(factor)
        output_path = output_dir / f"contrast_{factor:.1f}.png"
        contrasted.save(str(output_path))
        print(f"✓ Contrast {factor:.1f}: -> {output_path.name}")
    
    # Test functional API
    func_contrast = puhu.contrast(img, 1.8)
    func_contrast.save(str(output_dir / "contrast_functional.png"))
    print(f"✓ Functional contrast API")
    
    return True

def test_filter_combinations():
    """Test combining multiple filters."""
    import puhu
    
    img_dir, output_dir = setup_paths()
    
    print("\n" + "="*60)
    print("FILTER COMBINATIONS")
    print("="*60)
    
    # Load test image
    img = puhu.open(str(img_dir / "geometric.png"))
    print(f"Original image: {img.mode} {img.size}")
    
    # Combination 1: Blur + Sharpen
    combo1 = img.blur(2.0).sharpen(1.5)
    combo1.save(str(output_dir / "combo_blur_sharpen.png"))
    print(f"✓ Blur + Sharpen combination")
    
    # Combination 2: Brightness + Contrast
    combo2 = img.brightness(30).contrast(1.3)
    combo2.save(str(output_dir / "combo_bright_contrast.png"))
    print(f"✓ Brightness + Contrast combination")
    
    # Combination 3: Multiple filters
    combo3 = img.brightness(20).contrast(1.2).sharpen(0.8)
    combo3.save(str(output_dir / "combo_multiple.png"))
    print(f"✓ Multiple filters combination")
    
    # Combination 4: Edge detection on blurred image
    combo4 = img.blur(1.0).edge_detect()
    combo4.save(str(output_dir / "combo_blur_edges.png"))
    print(f"✓ Blur + Edge detection combination")
    
    return True

def main():
    """Run filters demo."""
    try:
        import puhu
        print("✓ Puhu imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import puhu: {e}")
        print("Make sure to build the Rust extension with: maturin develop")
        return 1

    print("Puhu Filters Demo")
    print("This script demonstrates all image filtering capabilities")
    
    img_dir, output_dir = setup_paths()
    
    try:
        test_blur_filters()
        test_sharpening_filters()
        test_edge_detection()
        test_emboss_filter()
        test_brightness_adjustment()
        test_contrast_adjustment()
        test_filter_combinations()
        
        print("\n" + "="*60)
        print("🎉 ALL FILTER DEMOS COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"Check the output directory: {output_dir}")
        print("\nNew filters available:")
        print("• blur() - Gaussian blur with adjustable radius")
        print("• sharpen() - Sharpening filter with adjustable strength")
        print("• edge_detect() - Edge detection using Sobel operator")
        print("• emboss() - Emboss effect")
        print("• brightness() - Brightness adjustment")
        print("• contrast() - Contrast adjustment")
        print("\nAll filters support both method-based and functional APIs.")
        print("Filters can be chained together for complex effects.")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error during filters demo: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
