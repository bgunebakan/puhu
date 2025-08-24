#!/usr/bin/env python3
"""
Advanced Features Example for Puhu Image Processing Library

This example demonstrates the newly implemented features:
- convert(): Image mode conversion
- split(): Channel splitting
- paste(): Image compositing
- fromarray(): NumPy array to image conversion
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

def test_convert_operations():
    """Test image mode conversion."""
    import puhu
    
    img_dir, output_dir = setup_paths()
    
    print("\n" + "="*60)
    print("CONVERT OPERATIONS")
    print("="*60)
    
    # Load a colorful image
    img_path = img_dir / "colorful_squares.png"
    img = puhu.open(str(img_path))
    print(f"Original image: {img.mode} {img.size}")
    
    # Convert to different modes
    conversions = [
        ("L", "grayscale"),
        ("RGBA", "with_alpha"),
    ]
    
    for mode, suffix in conversions:
        converted = img.convert(mode)
        output_path = output_dir / f"converted_{suffix}.png"
        converted.save(str(output_path))
        print(f"✓ Converted to {mode}: {converted.size} -> {output_path.name}")
    
    # Test round-trip conversion
    rgba_img = img.convert("RGBA")
    back_to_rgb = rgba_img.convert("RGB")
    back_to_rgb.save(str(output_dir / "roundtrip_rgb.png"))
    print(f"✓ Round-trip RGB->RGBA->RGB: {back_to_rgb.mode}")
    
    return True

def test_split_operations():
    """Test channel splitting."""
    import puhu
    
    img_dir, output_dir = setup_paths()
    
    print("\n" + "="*60)
    print("SPLIT OPERATIONS")
    print("="*60)
    
    # Test RGB splitting
    rgb_img = puhu.open(str(img_dir / "colorful_squares.png"))
    rgb_channels = rgb_img.split()
    
    print(f"RGB image split into {len(rgb_channels)} channels:")
    channel_names = ["red", "green", "blue"]
    for i, (channel, name) in enumerate(zip(rgb_channels, channel_names)):
        output_path = output_dir / f"channel_{name}.png"
        channel.save(str(output_path))
        print(f"  ✓ {name.capitalize()} channel: {channel.mode} -> {output_path.name}")
    
    # Test RGBA splitting
    rgba_img = rgb_img.convert("RGBA")
    rgba_channels = rgba_img.split()
    
    print(f"\nRGBA image split into {len(rgba_channels)} channels:")
    rgba_names = ["red", "green", "blue", "alpha"]
    for i, (channel, name) in enumerate(zip(rgba_channels, rgba_names)):
        output_path = output_dir / f"rgba_channel_{name}.png"
        channel.save(str(output_path))
        print(f"  ✓ {name.capitalize()} channel: {channel.mode} -> {output_path.name}")
    
    # Test grayscale splitting
    gray_img = rgb_img.convert("L")
    gray_channels = gray_img.split()
    
    print(f"\nGrayscale image split into {len(gray_channels)} channel(s):")
    gray_channels[0].save(str(output_dir / "gray_channel.png"))
    print(f"  ✓ Grayscale channel: {gray_channels[0].mode}")
    
    return True

def test_paste_operations():
    """Test image pasting/compositing."""
    import puhu
    
    img_dir, output_dir = setup_paths()
    
    print("\n" + "="*60)
    print("PASTE OPERATIONS")
    print("="*60)
    
    # Create base image
    base = puhu.new("RGB", (400, 300), (255, 255, 255))  # White background
    print(f"Base image: {base.size} {base.mode}")
    
    # Load overlay image
    overlay = puhu.open(str(img_dir / "geometric.png"))
    overlay_resized = overlay.resize((150, 150))
    print(f"Overlay image: {overlay_resized.size} {overlay_resized.mode}")
    
    # Test basic pasting at different positions
    positions = [
        ((50, 50), "top_left"),
        ((200, 50), "top_right"),
        ((50, 150), "bottom_left"),
        ((200, 150), "bottom_right"),
        ((125, 75), "center"),
    ]
    
    for (x, y), name in positions:
        result = base.paste(overlay_resized, (x, y))
        output_path = output_dir / f"paste_{name}.png"
        result.save(str(output_path))
        print(f"✓ Pasted at ({x}, {y}): -> {output_path.name}")
    
    # Test pasting with alpha
    alpha_overlay = puhu.open(str(img_dir / "alpha_test.png"))
    alpha_result = base.paste(alpha_overlay, (150, 100))
    alpha_result.save(str(output_dir / "paste_with_alpha.png"))
    print(f"✓ Pasted with alpha transparency")
    
    # Create a complex composition
    composition = puhu.new("RGB", (600, 400), (50, 50, 50))  # Dark gray background
    
    # Add multiple overlays
    overlays = [
        (puhu.open(str(img_dir / "colorful_squares.png")).resize((200, 150)), (50, 50)),
        (puhu.open(str(img_dir / "geometric.png")).resize((150, 150)), (300, 50)),
        (puhu.open(str(img_dir / "gradient.png")).resize((180, 120)), (200, 200)),
    ]
    
    for overlay_img, pos in overlays:
        composition = composition.paste(overlay_img, pos)
    
    composition.save(str(output_dir / "complex_composition.png"))
    print(f"✓ Created complex composition")
    
    return True

def test_fromarray_operations():
    """Test NumPy array to image conversion."""
    if not HAS_NUMPY:
        print("\n⚠ Skipping fromarray tests - NumPy not available")
        return True
    
    import puhu
    
    img_dir, output_dir = setup_paths()
    
    print("\n" + "="*60)
    print("FROMARRAY OPERATIONS")
    print("="*60)
    
    # Test 1: Grayscale array
    print("1. Creating image from grayscale array...")
    gray_array = np.arange(0, 256, dtype=np.uint8).reshape(16, 16)
    gray_img = puhu.fromarray(gray_array)
    gray_img.save(str(output_dir / "from_gray_array.png"))
    print(f"✓ Grayscale array -> {gray_img.mode} {gray_img.size}")
    
    # Test 2: RGB array
    print("2. Creating image from RGB array...")
    rgb_array = np.zeros((100, 100, 3), dtype=np.uint8)
    rgb_array[:50, :, 0] = 255  # Red top half
    rgb_array[50:, :, 1] = 255  # Green bottom half
    rgb_array[:, :50, 2] = 255  # Blue left half
    
    rgb_img = puhu.fromarray(rgb_array)
    rgb_img.save(str(output_dir / "from_rgb_array.png"))
    print(f"✓ RGB array -> {rgb_img.mode} {rgb_img.size}")
    
    # Test 3: RGBA array
    print("3. Creating image from RGBA array...")
    rgba_array = np.ones((80, 80, 4), dtype=np.uint8) * 128
    # Create a gradient alpha channel
    for y in range(80):
        rgba_array[y, :, 3] = int(255 * y / 80)
    rgba_array[:, :, 0] = 255  # Red channel
    
    rgba_img = puhu.fromarray(rgba_array)
    rgba_img.save(str(output_dir / "from_rgba_array.png"))
    print(f"✓ RGBA array -> {rgba_img.mode} {rgba_img.size}")
    
    # Test 4: Float array (should be converted)
    print("4. Creating image from float array...")
    float_array = np.random.random((60, 60, 3)).astype(np.float32)
    float_img = puhu.fromarray(float_array)
    float_img.save(str(output_dir / "from_float_array.png"))
    print(f"✓ Float array -> {float_img.mode} {float_img.size}")
    
    # Test 5: Noise pattern
    print("5. Creating noise pattern...")
    noise = np.random.randint(0, 256, (120, 120, 3), dtype=np.uint8)
    # Add some structure
    noise[::10, :] = [255, 0, 0]  # Red horizontal lines
    noise[:, ::10] = [0, 255, 0]  # Green vertical lines
    
    noise_img = puhu.fromarray(noise)
    noise_img.save(str(output_dir / "structured_noise.png"))
    print(f"✓ Structured noise -> {noise_img.mode} {noise_img.size}")
    
    return True

def test_functional_api():
    """Test functional API for all new features."""
    import puhu
    
    img_dir, output_dir = setup_paths()
    
    print("\n" + "="*60)
    print("FUNCTIONAL API")
    print("="*60)
    
    # Load test image
    img = puhu.open(str(img_dir / "colorful_squares.png"))
    
    # Test functional convert
    gray_func = puhu.convert(img, "L")
    gray_func.save(str(output_dir / "functional_convert.png"))
    print(f"✓ Functional convert: {gray_func.mode}")
    
    # Test functional split
    channels_func = puhu.split(img)
    for i, channel in enumerate(channels_func):
        channel.save(str(output_dir / f"functional_split_{i}.png"))
    print(f"✓ Functional split: {len(channels_func)} channels")
    
    # Test functional paste
    base = puhu.new("RGB", (300, 200), "white")
    overlay = img.resize((100, 100))
    pasted_func = puhu.paste(base, overlay, (100, 50))
    pasted_func.save(str(output_dir / "functional_paste.png"))
    print(f"✓ Functional paste: {pasted_func.size}")
    
    # Test functional fromarray (if NumPy available)
    if HAS_NUMPY:
        array = np.ones((50, 50, 3), dtype=np.uint8) * 200
        array_img_func = puhu.fromarray(array)
        array_img_func.save(str(output_dir / "functional_fromarray.png"))
        print(f"✓ Functional fromarray: {array_img_func.mode}")
    
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
    print("This script tests all newly implemented features")
    
    img_dir, output_dir = setup_paths()
    
    try:
        test_convert_operations()
        test_split_operations()
        test_paste_operations()
        test_fromarray_operations()
        test_functional_api()
        
        print("\n" + "="*60)
        print("🎉 ALL ADVANCED FEATURES COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"Check the output directory: {output_dir}")
        print("\nNew features tested:")
        print("• convert() - Image mode conversion")
        print("• split() - Channel splitting")
        print("• paste() - Image compositing")
        if HAS_NUMPY:
            print("• fromarray() - NumPy array to image conversion")
        else:
            print("• fromarray() - Skipped (NumPy not available)")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error during advanced features test: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
