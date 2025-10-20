Pillow Compatibility
====================

Puhu is designed to be a drop-in replacement for common Pillow (PIL) operations, providing better performance while maintaining API compatibility.

.. note::
   Puhu aims to be compatible with the most commonly used Pillow features. Not all Pillow functionality is implemented yet.

Fully Compatible Features
--------------------------

The following Pillow features are fully supported and API-compatible:

Core Functions
~~~~~~~~~~~~~~

**Supported**

- ``Image.open()`` - Open images from files or bytes
- ``Image.new()`` - Create new images
- ``Image.save()`` - Save images to files

Image Operations
~~~~~~~~~~~~~~~~

**Supported**

- ``resize()`` - Resize images with resampling filters
- ``crop()`` - Crop rectangular regions
- ``rotate()`` - Rotate by 90°, 180°, 270°
- ``transpose()`` - Flip and mirror operations
- ``copy()`` - Create image copies
- ``thumbnail()`` - Create thumbnails (in-place)

Properties and Attributes
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Supported**

- ``size`` - Image dimensions as (width, height)
- ``width`` - Image width in pixels
- ``height`` - Image height in pixels
- ``mode`` - Color mode (RGB, RGBA, L, etc.)
- ``format`` - File format (JPEG, PNG, etc.)

Resampling Filters
~~~~~~~~~~~~~~~~~~

**Supported**

- ``NEAREST`` - Nearest neighbor
- ``BILINEAR`` - Bilinear interpolation
- ``BICUBIC`` - Bicubic interpolation

Image Formats
~~~~~~~~~~~~~

**Supported**

- **PNG** - Portable Network Graphics
- **JPEG** - Joint Photographic Experts Group
- **BMP** - Windows Bitmap
- **TIFF** - Tagged Image File Format
- **GIF** - Graphics Interchange Format
- **WEBP** - WebP format

Planned Features
----------------

The following features are planned for future releases:

High Priority
~~~~~~~~~~~~~

**In Development**

- ``paste()`` - Paste images onto other images
- ``split()`` - Split into individual bands
- ``merge()`` - Merge bands into a new image
- ``fromarray()`` - Create from NumPy arrays
- ``tobytes()`` / ``frombytes()`` - Byte conversion (partially available via ``to_bytes()``)

Medium Priority
~~~~~~~~~~~~~~~

**Planned**

- ``filter()`` - Apply filters (blur, sharpen, etc.)
- ``getpixel()`` / ``putpixel()`` - Pixel access
- ``point()`` - Point operations
- ``convert()`` - Mode conversion
- ``getbbox()`` - Get bounding box
- ``getcolors()`` - Get color histogram

Lower Priority
~~~~~~~~~~~~~~

**Consideration**

- ``ImageDraw`` module - Drawing primitives
- ``ImageFilter`` module - Advanced filters
- ``ImageEnhance`` module - Enhancement operations
- ``ImageOps`` module - Utility operations
- Advanced metadata (EXIF, ICC profiles)

Not Planned
-----------

The following features are not currently planned:

- ``show()`` - Display images (platform-dependent)
- Animated GIF support (reading/writing animations)
- Font rendering and text operations
- Advanced color management

Migration Guide
---------------

Migrating from Pillow to Puhu
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Step 1: Update imports**

.. code-block:: python

   # Before (Pillow)
   from PIL import Image

   # After (Puhu)
   from puhu import Image
   # or
   import puhu

**Step 2: Test your code**

Most basic operations should work without modification:

.. code-block:: python

   # This code works with both Pillow and Puhu
   img = Image.open("photo.jpg")
   img = img.resize((800, 600))
   img = img.crop((0, 0, 400, 300))
   img.save("output.png")

**Step 3: Check for unsupported features**

If you use features not yet supported in Puhu, you have options:

.. code-block:: python

   # Option 1: Use Puhu for supported operations, Pillow for others
   import puhu
   from PIL import Image as PILImage

   # Use Puhu for performance-critical operations
   img = puhu.open("photo.jpg")
   img = img.resize((800, 600))
   img.save("temp.png")

   # Convert to Pillow for unsupported operations
   pil_img = PILImage.open("temp.png")
   pil_img = pil_img.filter(ImageFilter.BLUR)
   pil_img.save("output.png")

   # Option 2: Contribute the missing feature!
   # See docs/contributing.rst

Compatibility Testing
---------------------

We maintain a comprehensive compatibility test suite that compares Puhu's behavior with Pillow. This ensures that:

- Image dimensions match exactly
- Pixel values are identical (or within acceptable tolerance for lossy operations)
- Error handling is consistent
- API signatures match Pillow's interface

API Differences
---------------

While Puhu aims for API compatibility, there are some intentional differences:

Error Messages
~~~~~~~~~~~~~~

Puhu provides more detailed error messages with specific coordinate information:

.. code-block:: python

   # Pillow: Generic error
   # ValueError: invalid crop box

   # Puhu: Detailed error
   # ValueError: Crop bounds (100, 100, 2000, 1500) exceed image
   #             dimensions (1920, 1080)

Lazy Loading
~~~~~~~~~~~~

Both Pillow and Puhu use lazy loading, but Puhu's implementation is optimized for common workflows:

.. code-block:: python

   # Image data is loaded only when needed
   img = puhu.open("large_image.jpg")  # Fast, no loading yet

   # First operation triggers loading
   img = img.resize((800, 600))  # Loads and processes

   # Subsequent operations are fast
   img = img.crop((0, 0, 400, 300))

Memory Management
~~~~~~~~~~~~~~~~~

Puhu uses Rust's memory management for better efficiency:

- No Python GIL for image operations
- Automatic memory deallocation
- Reduced memory copying

Getting Help
------------

If you encounter compatibility issues:

1. Check this documentation for supported features
2. Search `GitHub Issues <https://github.com/bgunebakan/puhu/issues>`_
3. Open a new issue with:

   - Minimal code example
   - Expected behavior (Pillow)
   - Actual behavior (Puhu)
   - Error messages

Contributing
------------

Help us improve Pillow compatibility:

- Report compatibility issues
- Submit test cases
- Implement missing features

See :doc:`contributing` for more information.
