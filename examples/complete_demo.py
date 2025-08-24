#!/usr/bin/env python3
"""
Complete Puhu Demo - Showcasing All Features

This comprehensive example demonstrates all Puhu capabilities:
- Basic operations (open, save, resize, crop, rotate, etc.)
- Advanced features (convert, split, paste, fromarray)
- Image filters (blur, sharpen, edge_detect, emboss, brightness, contrast)
- Both method-based and functional APIs
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

def create_image_gallery():
    """Create a comprehensive image processing gallery."""
    import puhu
    
    img_dir, output_dir = setup_paths()
    
    print("\n" + "="*70)
    print("CREATING COMPREHENSIVE IMAGE PROCESSING GALLERY")
    print("="*70)
    
    # Load base image
    base_img = puhu.open(str(img_dir / "colorful_squares.png"))
    print(f"Base image loaded: {base_img.mode} {base_img.size}")
    
    # Create a gallery layout (3x3 grid)
    gallery_width = 600
    gallery_height = 600
    cell_width = gallery_width // 3
    cell_height = gallery_height // 3
    
    # Create white background
    gallery = puhu.new("RGB", (gallery_width, gallery_height), (255, 255, 255))
    
    # Resize base image to fit cells
    cell_img = base_img.resize((cell_width - 10, cell_height - 10))
    
    # Create different processed versions
    processed_images = [
        ("Original", cell_img),
        ("Blurred", cell_img.blur(3.0)),
        ("Sharpened", cell_img.sharpen(2.0)),
        ("Grayscale", cell_img.convert("L").convert("RGB")),
        ("High Contrast", cell_img.contrast(1.8)),
        ("Brightened", cell_img.brightness(50)),
        ("Edge Detection", cell_img.edge_detect().convert("RGB")),
        ("Embossed", cell_img.emboss()),
        ("Combined", cell_img.blur(1.0).sharpen(1.5).brightness(20)),
    ]
    
    # Place images in grid
    for i, (name, img) in enumerate(processed_images):
        row = i // 3
        col = i % 3
        x = col * cell_width + 5
        y = row * cell_height + 5
        
        gallery = gallery.paste(img, (x, y))
        print(f"✓ Added {name} at position ({x}, {y})")
    
    # Save gallery
    gallery.save(str(output_dir / "complete_gallery.png"))
    print(f"✓ Gallery saved: complete_gallery.png")
    
    return True

def demonstrate_advanced_compositing():
    """Demonstrate advanced image compositing techniques."""
    import puhu
    
    img_dir, output_dir = setup_paths()
    
    print("\n" + "="*70)
    print("ADVANCED COMPOSITING TECHNIQUES")
    print("="*70)
    
    # Create a complex composition
    canvas = puhu.new("RGB", (800, 600), (30, 30, 50))  # Dark blue background
    
    # Load and process multiple images
    img1 = puhu.open(str(img_dir / "colorful_squares.png")).resize((200, 150))
    img2 = puhu.open(str(img_dir / "geometric.png")).resize((180, 180))
    img3 = puhu.open(str(img_dir / "gradient.png")).resize((250, 120))
    
    # Apply different effects to each image
    img1_processed = img1.brightness(30).contrast(1.2)
    img2_processed = img2.blur(1.0).sharpen(1.5)
    img3_processed = img3.convert("L").convert("RGB").contrast(1.5)
    
    # Create alpha overlay
    if HAS_NUMPY:
        # Create a semi-transparent overlay using numpy
        overlay_array = np.ones((150, 200, 4), dtype=np.uint8)
        overlay_array[:, :, 0] = 255  # Red
        overlay_array[:, :, 1] = 100  # Green
        overlay_array[:, :, 2] = 50   # Blue
        overlay_array[:, :, 3] = 100  # Alpha (semi-transparent)
        
        alpha_overlay = puhu.fromarray(overlay_array)
        print("✓ Created alpha overlay from NumPy array")
    else:
        alpha_overlay = puhu.new("RGBA", (200, 150), (255, 100, 50, 100))
        print("✓ Created alpha overlay (NumPy not available)")
    
    # Composite images onto canvas
    canvas = canvas.paste(img1_processed, (50, 50))
    canvas = canvas.paste(img2_processed, (300, 100))
    canvas = canvas.paste(img3_processed, (500, 400))
    
    # Add alpha overlay
    canvas = canvas.paste(alpha_overlay, (100, 300))
    
    # Apply final effects
    final_composition = canvas.brightness(10).contrast(1.1)
    
    # Save composition
    final_composition.save(str(output_dir / "advanced_composition.png"))
    print(f"✓ Advanced composition saved")
    
    return True

def demonstrate_channel_manipulation():
    """Demonstrate channel splitting and manipulation."""
    import puhu
    
    img_dir, output_dir = setup_paths()
    
    print("\n" + "="*70)
    print("CHANNEL MANIPULATION")
    print("="*70)
    
    # Load image
    img = puhu.open(str(img_dir / "colorful_squares.png"))
    
    # Split into channels
    channels = img.split()
    print(f"Split image into {len(channels)} channels")
    
    # Process each channel differently
    processed_channels = []
    effects = ["brightness(50)", "contrast(1.5)", "blur(2.0)"]
    
    for i, (channel, effect) in enumerate(zip(channels, effects)):
        if effect.startswith("brightness"):
            value = int(effect.split("(")[1].split(")")[0])
            processed = channel.brightness(value)
        elif effect.startswith("contrast"):
            value = float(effect.split("(")[1].split(")")[0])
            processed = channel.contrast(value)
        elif effect.startswith("blur"):
            value = float(effect.split("(")[1].split(")")[0])
            processed = channel.blur(value)
        else:
            processed = channel
        
        processed_channels.append(processed)
        processed.save(str(output_dir / f"channel_{i}_processed.png"))
        print(f"✓ Processed channel {i} with {effect}")
    
    # Create a comparison image
    comparison_width = img.width * 2
    comparison_height = img.height * 2
    comparison = puhu.new("RGB", (comparison_width, comparison_height), "white")
    
    # Place original and processed channels
    comparison = comparison.paste(img, (0, 0))
    
    for i, channel in enumerate(processed_channels):
        x = (i % 2) * img.width
        y = img.height + (i // 2) * (img.height // 2)
        if i < 3:  # Only place first 3 channels
            channel_rgb = channel.convert("RGB")
            comparison = comparison.paste(channel_rgb, (x, y))
    
    comparison.save(str(output_dir / "channel_manipulation.png"))
    print(f"✓ Channel manipulation comparison saved")
    
    return True

def demonstrate_filter_chains():
    """Demonstrate complex filter chains."""
    import puhu
    
    img_dir, output_dir = setup_paths()
    
    print("\n" + "="*70)
    print("COMPLEX FILTER CHAINS")
    print("="*70)
    
    # Load base image
    img = puhu.open(str(img_dir / "geometric.png"))
    
    # Define different filter chains
    filter_chains = [
        ("Artistic", lambda x: x.blur(1.5).sharpen(2.0).contrast(1.3).brightness(20)),
        ("Vintage", lambda x: x.brightness(-20).contrast(0.8).blur(0.5)),
        ("High Detail", lambda x: x.sharpen(1.5).contrast(1.4).brightness(10)),
        ("Soft Focus", lambda x: x.blur(2.0).brightness(15).contrast(1.1)),
        ("Dramatic", lambda x: x.contrast(2.0).brightness(-10).sharpen(1.0)),
    ]
    
    # Apply each filter chain
    results = []
    for name, chain in filter_chains:
        result = chain(img)
        result.save(str(output_dir / f"filter_chain_{name.lower().replace(' ', '_')}.png"))
        results.append((name, result))
        print(f"✓ Applied {name} filter chain")
    
    # Create comparison grid
    grid_width = img.width * 3
    grid_height = img.height * 2
    grid = puhu.new("RGB", (grid_width, grid_height), "white")
    
    # Place original in center
    grid = grid.paste(img, (img.width, 0))
    
    # Place filtered versions around it
    positions = [(0, 0), (2 * img.width, 0), (0, img.height), 
                 (img.width, img.height), (2 * img.width, img.height)]
    
    for i, ((name, result), pos) in enumerate(zip(results, positions)):
        if i < len(positions):
            grid = grid.paste(result, pos)
    
    grid.save(str(output_dir / "filter_chains_comparison.png"))
    print(f"✓ Filter chains comparison saved")
    
    return True

def main():
    """Run complete demo."""
    try:
        import puhu
        print("✓ Puhu imported successfully")
        print(f"✓ NumPy available: {HAS_NUMPY}")
    except ImportError as e:
        print(f"✗ Failed to import puhu: {e}")
        print("Make sure to build the Rust extension with: maturin develop")
        return 1

    print("Puhu Complete Demo")
    print("This script demonstrates ALL Puhu capabilities in a comprehensive showcase")
    
    img_dir, output_dir = setup_paths()
    
    try:
        create_image_gallery()
        demonstrate_advanced_compositing()
        demonstrate_channel_manipulation()
        demonstrate_filter_chains()
        
        print("\n" + "="*70)
        print("🎉 COMPLETE DEMO FINISHED SUCCESSFULLY!")
        print("="*70)
        print(f"Check the output directory: {output_dir}")
        print("\nPuhu now includes:")
        print("✓ All basic operations (open, save, resize, crop, rotate, etc.)")
        print("✓ Advanced features (convert, split, paste, fromarray)")
        print("✓ Comprehensive filter suite (blur, sharpen, edge_detect, etc.)")
        print("✓ Both method-based and functional APIs")
        print("✓ NumPy integration for array-based operations")
        print("✓ High-performance Rust backend with Python convenience")
        print("\nPuhu is now feature-complete for most image processing tasks!")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error during complete demo: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
