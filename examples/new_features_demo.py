#!/usr/bin/env python3
"""
Demonstration of Puhu's new high-priority features:
- convert(): Image mode conversion
- split(): Channel splitting
- paste(): Image compositing
- fromarray(): NumPy array to image conversion

Note: This script requires the Rust extension to be built with `maturin develop`
"""

import sys
import os

# Add the parent directory to the path to import puhu
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python'))

try:
    import puhu
    print("✓ Puhu imported successfully")
except ImportError as e:
    print(f"✗ Failed to import puhu: {e}")
    print("Make sure to build the Rust extension with: maturin develop")
    sys.exit(1)

try:
    import numpy as np
    HAS_NUMPY = True
    print("✓ NumPy available")
except ImportError:
    HAS_NUMPY = False
    print("⚠ NumPy not available - fromarray() examples will be skipped")

def demo_convert():
    """Demonstrate image mode conversion."""
    print("\n" + "="*50)
    print("CONVERT DEMO - Image Mode Conversion")
    print("="*50)
    
    # Create a colorful RGB image
    img = puhu.new("RGB", (100, 100), (255, 128, 64))
    print(f"Original image: {img.mode} {img.size}")
    
    # Convert to grayscale
    gray = img.convert("L")
    print(f"Grayscale: {gray.mode} {gray.size}")
    
    # Convert to RGBA (add alpha channel)
    rgba = img.convert("RGBA")
    print(f"With alpha: {rgba.mode} {rgba.size}")
    
    # Convert back to RGB
    rgb_again = rgba.convert("RGB")
    print(f"Back to RGB: {rgb_again.mode} {rgb_again.size}")
    
    print("✓ Mode conversion completed successfully")

def demo_split():
    """Demonstrate channel splitting."""
    print("\n" + "="*50)
    print("SPLIT DEMO - Channel Splitting")
    print("="*50)
    
    # Create RGB image
    rgb_img = puhu.new("RGB", (50, 50), (255, 128, 64))
    print(f"RGB image: {rgb_img.mode} {rgb_img.size}")
    
    # Split into channels
    channels = rgb_img.split()
    print(f"Split into {len(channels)} channels:")
    for i, channel in enumerate(channels):
        print(f"  Channel {i}: {channel.mode} {channel.size}")
    
    # Create RGBA image
    rgba_img = puhu.new("RGBA", (50, 50), (255, 128, 64, 200))
    print(f"\nRGBA image: {rgba_img.mode} {rgba_img.size}")
    
    # Split RGBA
    rgba_channels = rgba_img.split()
    print(f"Split into {len(rgba_channels)} channels:")
    for i, channel in enumerate(rgba_channels):
        print(f"  Channel {i}: {channel.mode} {channel.size}")
    
    # Grayscale image
    gray_img = puhu.new("L", (50, 50), 128)
    gray_channels = gray_img.split()
    print(f"\nGrayscale split: {len(gray_channels)} channel(s)")
    
    print("✓ Channel splitting completed successfully")

def demo_paste():
    """Demonstrate image pasting/compositing."""
    print("\n" + "="*50)
    print("PASTE DEMO - Image Compositing")
    print("="*50)
    
    # Create base image (white background)
    base = puhu.new("RGB", (200, 200), (255, 255, 255))
    print(f"Base image: {base.mode} {base.size}")
    
    # Create overlay (red square)
    overlay = puhu.new("RGB", (100, 100), (255, 0, 0))
    print(f"Overlay: {overlay.mode} {overlay.size}")
    
    # Paste at center
    result = base.paste(overlay, (50, 50))
    print(f"Result: {result.mode} {result.size}")
    
    # Create another overlay (blue square)
    blue_overlay = puhu.new("RGB", (60, 60), (0, 0, 255))
    
    # Paste with different position
    result2 = result.paste(blue_overlay, (120, 120))
    print(f"Final result: {result2.mode} {result2.size}")
    
    print("✓ Image pasting completed successfully")

def demo_fromarray():
    """Demonstrate NumPy array to image conversion."""
    if not HAS_NUMPY:
        print("\n⚠ Skipping fromarray demo - NumPy not available")
        return
        
    print("\n" + "="*50)
    print("FROMARRAY DEMO - NumPy Integration")
    print("="*50)
    
    # Create grayscale array
    gray_array = np.arange(0, 256, dtype=np.uint8).reshape(16, 16)
    gray_img = puhu.fromarray(gray_array)
    print(f"From grayscale array: {gray_img.mode} {gray_img.size}")
    
    # Create RGB array
    rgb_array = np.zeros((50, 50, 3), dtype=np.uint8)
    rgb_array[:, :, 0] = 255  # Red channel
    rgb_array[:25, :, 1] = 255  # Green in top half
    rgb_img = puhu.fromarray(rgb_array)
    print(f"From RGB array: {rgb_img.mode} {rgb_img.size}")
    
    # Create RGBA array
    rgba_array = np.ones((30, 30, 4), dtype=np.uint8) * 128
    rgba_array[:, :, 3] = 200  # Alpha channel
    rgba_img = puhu.fromarray(rgba_array)
    print(f"From RGBA array: {rgba_img.mode} {rgba_img.size}")
    
    # Float array (will be converted)
    float_array = np.random.random((25, 25, 3)).astype(np.float32)
    float_img = puhu.fromarray(float_array)
    print(f"From float array: {float_img.mode} {float_img.size}")
    
    print("✓ NumPy array conversion completed successfully")

def demo_functional_api():
    """Demonstrate functional API for new features."""
    print("\n" + "="*50)
    print("FUNCTIONAL API DEMO")
    print("="*50)
    
    # Create test image
    img = puhu.new("RGB", (100, 100), (255, 128, 64))
    
    # Use functional API
    gray = puhu.convert(img, "L")
    print(f"Functional convert: {gray.mode}")
    
    channels = puhu.split(img)
    print(f"Functional split: {len(channels)} channels")
    
    base = puhu.new("RGB", (150, 150), "white")
    result = puhu.paste(base, img, (25, 25))
    print(f"Functional paste: {result.mode} {result.size}")
    
    if HAS_NUMPY:
        array = np.ones((40, 40, 3), dtype=np.uint8) * 100
        array_img = puhu.fromarray(array)
        print(f"Functional fromarray: {array_img.mode} {array_img.size}")
    
    print("✓ Functional API demo completed successfully")

def main():
    """Run all demos."""
    print("Puhu New Features Demonstration")
    print("This script demonstrates the newly implemented high-priority features")
    
    try:
        demo_convert()
        demo_split()
        demo_paste()
        demo_fromarray()
        demo_functional_api()
        
        print("\n" + "="*50)
        print("🎉 ALL DEMOS COMPLETED SUCCESSFULLY!")
        print("="*50)
        print("\nThe following features are now available in Puhu:")
        print("• convert() - Image mode conversion")
        print("• split() - Channel splitting")
        print("• paste() - Image compositing")
        print("• fromarray() - NumPy array to image conversion")
        print("\nBoth method-based and functional APIs are supported.")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        print("Make sure the Rust extension is built with: maturin develop")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
