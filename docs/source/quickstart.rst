Quick Start Guide
=================

This guide will help you get started with puhu for common image processing tasks.

Basic Image Operations
----------------------

Opening Images
~~~~~~~~~~~~~~

Open an image from a file:

.. code-block:: python

   import puhu

   # Open from file path
   img = puhu.open("photo.jpg")

   # Open from bytes
   with open("photo.jpg", "rb") as f:
       img = puhu.open(f.read())

Creating New Images
~~~~~~~~~~~~~~~~~~~

Create images from scratch:

.. code-block:: python

   # Create a black RGB image
   img = puhu.new("RGB", (800, 600))

   # Create with a specific color (by name)
   img = puhu.new("RGB", (800, 600), "red")

   # Create with RGB tuple
   img = puhu.new("RGB", (800, 600), (255, 128, 0))

   # Create grayscale image
   img = puhu.new("L", (800, 600), 128)

Saving Images
~~~~~~~~~~~~~

Save images in various formats:

.. code-block:: python

   # Format auto-detected from extension
   img.save("output.png")
   img.save("output.jpg")

   # Explicitly specify format
   img.save("output.webp", format="WEBP")

Image Transformations
---------------------

Resizing
~~~~~~~~

.. code-block:: python

   # Resize to specific dimensions
   resized = img.resize((800, 600))

   # Resize with resampling filter
   resized = img.resize((400, 300), resample=puhu.Resampling.BILINEAR)

   # Available resampling filters:
   # - NEAREST: Fastest, lowest quality
   # - BILINEAR: Good balance (default)
   # - BICUBIC: High quality, slower

Cropping
~~~~~~~~

.. code-block:: python

   # Crop to a specific region (left, top, right, bottom)
   cropped = img.crop((100, 100, 500, 400))

   # Crop from center
   width, height = img.size
   left = width // 4
   top = height // 4
   right = 3 * width // 4
   bottom = 3 * height // 4
   center_crop = img.crop((left, top, right, bottom))

Rotating
~~~~~~~~

.. code-block:: python

   # Rotate by 90, 180, or 270 degrees
   rotated_90 = img.rotate(90)
   rotated_180 = img.rotate(180)
   rotated_270 = img.rotate(270)

Flipping and Transposing
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Flip horizontally
   flipped_h = img.transpose(puhu.Transpose.FLIP_LEFT_RIGHT)

   # Flip vertically
   flipped_v = img.transpose(puhu.Transpose.FLIP_TOP_BOTTOM)

Creating Thumbnails
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Create thumbnail (modifies image in-place)
   img.thumbnail((200, 200))

   # To preserve original, make a copy first
   thumb = img.copy()
   thumb.thumbnail((200, 200))

Image Properties
----------------

Accessing Metadata
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Get image dimensions
   width = img.width
   height = img.height
   size = img.size  # Returns (width, height) tuple

   # Get color mode
   mode = img.mode  # e.g., "RGB", "RGBA", "L"

   # Get format (if opened from file)
   format = img.format  # e.g., "JPEG", "PNG"

Working with Bytes
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Get raw pixel data as bytes
   pixel_data = img.to_bytes()

   # Get byte length
   byte_length = len(pixel_data)

Drop-in Pillow Replacement
---------------------------

Replace Pillow imports
~~~~~~~~~~~~~~~~~~~~~~

Puhu is designed to be a drop-in replacement for common Pillow operations:

.. code-block:: python

   # Instead of:
   # from PIL import Image

   # Use:
   from puhu import Image

   # Your existing code works unchanged!
   img = Image.open("photo.jpg")
   img = img.resize((400, 300))
   img.save("resized.jpg")

Complete Workflow Example
--------------------------

Here's a complete example combining multiple operations:

.. code-block:: python

   import puhu

   # Open an image
   img = puhu.open("input.jpg")
   print(f"Original size: {img.size}")

   # Resize to standard HD
   img = img.resize((1920, 1080))

   # Crop to remove borders
   img = img.crop((50, 50, 1870, 1030))

   # Rotate if needed
   img = img.rotate(90)

   # Create a thumbnail version
   thumb = img.copy()
   thumb.thumbnail((300, 300))

   # Save both versions
   img.save("processed.png")
   thumb.save("thumbnail.png")

   print(f"Saved processed image: {img.size}")
   print(f"Saved thumbnail: {thumb.size}")

Performance Tips
----------------

1. **Use appropriate resampling filters**: Choose the right balance between speed and quality

   - ``NEAREST``: Fastest for thumbnails
   - ``BILINEAR``: Good default
   - ``BICUBIC``: Best quality for enlargement

2. **Batch operations**: When processing multiple images, reuse objects when possible

3. **Choose efficient formats**:

   - PNG: Lossless, larger files
   - JPEG: Lossy, smaller files
   - WEBP: Modern, good compression

4. **Lazy loading**: Puhu uses lazy loading, so operations are chained efficiently

Next Steps
----------

- Explore the full :doc:`api` reference
- Check :doc:`pillow_compatibility` for detailed compatibility information
- Learn about :doc:`contributing` if you want to help improve puhu
