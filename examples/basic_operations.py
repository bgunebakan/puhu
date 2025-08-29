#!/usr/bin/env python3
"""
Basic Operations Example for Puhu Image Processing Library

This example demonstrates the core functionality of Puhu:
- Opening and saving images
- Basic transformations (resize, crop, rotate)
- Image creation and copying
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

def test_basic_operations():
    """Test basic image operations."""
    try:
        import puhu
        print("✓ Puhu imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import puhu: {e}")
        print("Make sure to build the Rust extension with: maturin develop")
        return False

    img_dir, output_dir = setup_paths()
    
    try:
        print("\n" + "="*60)
        print("BASIC OPERATIONS DEMO")
        print("="*60)
        
        # Test 1: Open an image
        print("\n1. Opening image...")
        img_path = img_dir / "colorful_squares.png"
        if not img_path.exists():
            print(f"✗ Test image not found: {img_path}")
            return False
            
        img = puhu.open(str(img_path))
        print(f"✓ Opened image: {img.size} {img.mode}")
        
        # Test 2: Basic properties
        print(f"   Width: {img.width}, Height: {img.height}")
        print(f"   Mode: {img.mode}, Format: {img.format}")
        
        # Test 3: Resize image
        print("\n2. Resizing image...")
        resized = img.resize((200, 150))
        print(f"✓ Resized to: {resized.size}")
        resized.save(str(output_dir / "resized.png"))
        print(f"✓ Saved resized image")
        
        # Test 4: Crop image
        print("\n3. Cropping image...")
        cropped = img.crop((50, 50, 250, 200))
        print(f"✓ Cropped to: {cropped.size}")
        cropped.save(str(output_dir / "cropped.png"))
        print(f"✓ Saved cropped image")
        
        # Test 5: Rotate image
        print("\n4. Rotating image...")
        rotated_90 = img.rotate(90)
        rotated_180 = img.rotate(180)
        rotated_270 = img.rotate(270)
        
        print(f"✓ 90° rotation: {rotated_90.size}")
        print(f"✓ 180° rotation: {rotated_180.size}")
        print(f"✓ 270° rotation: {rotated_270.size}")
        
        rotated_90.save(str(output_dir / "rotated_90.png"))
        rotated_180.save(str(output_dir / "rotated_180.png"))
        rotated_270.save(str(output_dir / "rotated_270.png"))
        print(f"✓ Saved rotated images")
        
        # Test 6: Transpose operations
        print("\n5. Transpose operations...")
        from puhu import Transpose
        
        flipped_h = img.transpose(Transpose.FLIP_LEFT_RIGHT)
        flipped_v = img.transpose(Transpose.FLIP_TOP_BOTTOM)
        
        print(f"✓ Horizontal flip: {flipped_h.size}")
        print(f"✓ Vertical flip: {flipped_v.size}")
        
        flipped_h.save(str(output_dir / "flipped_horizontal.png"))
        flipped_v.save(str(output_dir / "flipped_vertical.png"))
        print(f"✓ Saved flipped images")
        
        # Test 7: Copy image
        print("\n6. Copying image...")
        copied = img.copy()
        print(f"✓ Copied image: {copied.size}")
        
        # Test 8: Create new image
        print("\n7. Creating new images...")
        new_rgb = puhu.new("RGB", (300, 200), (255, 128, 64))
        new_rgba = puhu.new("RGBA", (200, 200), (0, 255, 0, 128))
        new_gray = puhu.new("L", (150, 150), 128)
        
        print(f"✓ RGB image: {new_rgb.size} {new_rgb.mode}")
        print(f"✓ RGBA image: {new_rgba.size} {new_rgba.mode}")
        print(f"✓ Grayscale image: {new_gray.size} {new_gray.mode}")
        
        new_rgb.save(str(output_dir / "new_rgb.png"))
        new_rgba.save(str(output_dir / "new_rgba.png"))
        new_gray.save(str(output_dir / "new_gray.png"))
        print(f"✓ Saved new images")
        
        # Test 9: Thumbnail
        print("\n8. Creating thumbnail...")
        thumb_img = img.copy()
        thumb_img.thumbnail((100, 100))
        print(f"✓ Thumbnail size: {thumb_img.size}")
        thumb_img.save(str(output_dir / "thumbnail.png"))
        print(f"✓ Saved thumbnail")
        
        # Test 10: Different resampling methods
        print("\n9. Testing resampling methods...")
        from puhu import Resampling
        
        methods = [
            ("nearest", Resampling.NEAREST),
            ("bilinear", Resampling.BILINEAR),
            ("bicubic", Resampling.BICUBIC),
            ("lanczos", Resampling.LANCZOS),
        ]
        
        for name, method in methods:
            resampled = img.resize((150, 100), method)
            resampled.save(str(output_dir / f"resampled_{name}.png"))
            print(f"✓ {name.capitalize()} resampling: {resampled.size}")
        
        print("\n" + "="*60)
        print("🎉 ALL BASIC OPERATIONS COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"Check the output directory: {output_dir}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during basic operations: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run basic operations demo."""
    print("Puhu Basic Operations Demo")
    print("This script tests all basic image operations")
    
    if test_basic_operations():
        print("\n✅ Basic operations test passed!")
        return 0
    else:
        print("\n❌ Basic operations test failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
