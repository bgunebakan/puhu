API Reference
=============

This page documents the complete API of the puhu library.

Core Functions
--------------

.. py:function:: puhu.open(fp)

   Open and identify an image file or bytes.

   :param fp: A filename (string), pathlib.Path object, or file object, or bytes
   :type fp: str or Path or bytes
   :return: An Image object
   :rtype: Image
   :raises IOError: If the file cannot be opened or identified

   Example::

       img = puhu.open("photo.jpg")
       img = puhu.open(Path("photo.jpg"))

       with open("photo.jpg", "rb") as f:
           img = puhu.open(f.read())


.. py:function:: puhu.new(mode, size, color=None)

   Create a new image with the given mode and size.

   :param mode: The mode to use for the new image. See :ref:`image-modes`.
   :type mode: str
   :param size: A 2-tuple containing (width, height) in pixels
   :type size: tuple[int, int]
   :param color: The color to use for the image. Default is black. Can be a color name, RGB tuple, or integer for grayscale.
   :type color: str or tuple or int or None
   :return: An Image object
   :rtype: Image

   Example::

       # Black image
       img = puhu.new("RGB", (800, 600))

       # Red image
       img = puhu.new("RGB", (800, 600), "red")
       img = puhu.new("RGB", (800, 600), (255, 0, 0))

       # Gray image
       img = puhu.new("L", (800, 600), 128)


Image Class
-----------

.. py:class:: Image

   Represents an image object in puhu.

   Properties
   ~~~~~~~~~~

   .. py:attribute:: width
      :type: int

      The width of the image in pixels.

   .. py:attribute:: height
      :type: int

      The height of the image in pixels.

   .. py:attribute:: size
      :type: tuple[int, int]

      The size of the image as a 2-tuple (width, height).

   .. py:attribute:: mode
      :type: str

      The image mode. See :ref:`image-modes` for available modes.

   .. py:attribute:: format
      :type: str or None

      The file format of the source file (e.g., "JPEG", "PNG"), or None if the image was not loaded from a file.

   Methods
   ~~~~~~~

   .. py:method:: resize(size, resample=Resampling.BILINEAR)

      Returns a resized copy of this image.

      :param size: The requested size in pixels as a 2-tuple (width, height)
      :type size: tuple[int, int]
      :param resample: The resampling filter. One of :py:class:`Resampling` values.
      :type resample: Resampling
      :return: A new Image object
      :rtype: Image

      Example::

          resized = img.resize((800, 600))
          resized = img.resize((400, 300), resample=puhu.Resampling.BICUBIC)


   .. py:method:: crop(box)

      Returns a rectangular region from this image.

      :param box: The crop rectangle as a 4-tuple (left, top, right, bottom)
      :type box: tuple[int, int, int, int]
      :return: A new Image object
      :rtype: Image
      :raises ValueError: If the crop box is invalid or out of bounds

      Example::

          cropped = img.crop((100, 100, 500, 400))


   .. py:method:: rotate(angle)

      Returns a rotated copy of this image.

      :param angle: The rotation angle in degrees. Only 90, 180, and 270 are supported.
      :type angle: int
      :return: A new Image object
      :rtype: Image
      :raises ValueError: If the angle is not 90, 180, or 270

      Example::

          rotated = img.rotate(90)


   .. py:method:: transpose(method)

      Returns a flipped or transposed copy of this image.

      :param method: One of :py:class:`Transpose` values
      :type method: Transpose
      :return: A new Image object
      :rtype: Image

      Example::

          flipped = img.transpose(puhu.Transpose.FLIP_LEFT_RIGHT)
          mirrored = img.transpose(puhu.Transpose.FLIP_TOP_BOTTOM)


   .. py:method:: copy()

      Returns a copy of this image.

      :return: A new Image object
      :rtype: Image

      Example::

          img_copy = img.copy()


   .. py:method:: thumbnail(size)

      Modifies this image to contain a thumbnail version of itself, no larger than the given size.
      This method modifies the image in place.

      :param size: The maximum size as a 2-tuple (width, height)
      :type size: tuple[int, int]

      Example::

          img.thumbnail((200, 200))


   .. py:method:: paste(im, box=None, mask=None)

      Pastes another image or color into this image.

      The box argument specifies where to paste:

      - **None**: Paste at (0, 0)
      - **2-tuple (x, y)**: Upper left corner. Supports negative values for clipping.
      - **4-tuple (left, upper, right, lower)**: Exact region (source size must match)

      If the modes don't match, the pasted image is automatically converted.

      :param im: Source image, color tuple (RGB/RGBA), single integer (grayscale), or color string
      :type im: Image or tuple or int or str
      :param box: Where to paste. 2-tuple for position, 4-tuple for exact region, or None for (0, 0)
      :type box: tuple[int, int] or tuple[int, int, int, int] or None
      :param mask: Optional mask image ("L" or "1" mode). Where mask is 255, source is copied fully.
      :type mask: Image or None

      Example::

          # Paste image at position
          bg.paste(fg, (100, 100))

          # Paste with negative coords (clips source)
          bg.paste(fg, (-10, -10))

          # Fill region with color
          img.paste((255, 0, 0), (0, 0, 100, 100))
          img.paste("red", (0, 0, 100, 100))

          # Paste with mask
          bg.paste(fg, (0, 0), mask)

          # Abbreviated syntax: paste(im, mask)
          bg.paste(fg, mask)


   .. py:method:: save(fp, format=None)

      Saves this image to the specified file.

      :param fp: A filename (string) or pathlib.Path object
      :type fp: str or Path
      :param format: Optional format override. If not specified, format is determined from the file extension.
      :type format: str or None
      :raises IOError: If the file cannot be written

      Example::

          img.save("output.png")
          img.save("output.jpg", format="JPEG")


   .. py:method:: to_bytes()

      Returns the raw pixel data of the image as bytes.

      :return: Raw pixel data
      :rtype: bytes

      Example::

          pixel_data = img.to_bytes()


Enums and Constants
-------------------

.. _image-modes:

Image Modes
~~~~~~~~~~~

Puhu supports the following image modes:

- **"1"**: 1-bit pixels, black and white
- **"L"**: 8-bit pixels, grayscale
- **"RGB"**: 3x8-bit pixels, true color
- **"RGBA"**: 4x8-bit pixels, true color with transparency

.. py:class:: Resampling

   An enumeration of resampling filters for the :py:meth:`Image.resize` method.

   .. py:attribute:: NEAREST
      :value: 0

      Nearest neighbor resampling. Fastest, lowest quality.

   .. py:attribute:: BILINEAR
      :value: 2

      Bilinear resampling. Good balance of speed and quality (default).

   .. py:attribute:: BICUBIC
      :value: 3

      Bicubic resampling. High quality, slower than bilinear.


.. py:class:: Transpose

   An enumeration of transpose/flip operations for the :py:meth:`Image.transpose` method.

   .. py:attribute:: FLIP_LEFT_RIGHT

      Flip the image horizontally (left to right).

   .. py:attribute:: FLIP_TOP_BOTTOM

      Flip the image vertically (top to bottom).


Supported Formats
-----------------

Input Formats
~~~~~~~~~~~~~

Puhu can read the following image formats:

- **PNG**: Portable Network Graphics
- **JPEG**: Joint Photographic Experts Group
- **BMP**: Windows Bitmap
- **TIFF**: Tagged Image File Format
- **GIF**: Graphics Interchange Format
- **WEBP**: WebP format

Output Formats
~~~~~~~~~~~~~~

Puhu can write the following image formats:

- **PNG**: Portable Network Graphics (lossless)
- **JPEG**: Joint Photographic Experts Group (lossy)
- **BMP**: Windows Bitmap (lossless)
- **TIFF**: Tagged Image File Format (lossless)
- **GIF**: Graphics Interchange Format (lossless)
- **WEBP**: WebP format (lossy and lossless)

Exceptions
----------

.. py:exception:: IOError

   Raised when an image file cannot be opened, identified, or saved.

.. py:exception:: ValueError

   Raised when invalid parameters are provided to image operations (e.g., invalid crop bounds, unsupported rotation angle).

Examples
--------

Complete Workflow
~~~~~~~~~~~~~~~~~

.. code-block:: python

   import puhu

   # Open image
   img = puhu.open("input.jpg")

   # Check properties
   print(f"Size: {img.size}")
   print(f"Mode: {img.mode}")
   print(f"Format: {img.format}")

   # Process image
   img = img.resize((1920, 1080))
   img = img.crop((0, 0, 1920, 1000))
   img = img.rotate(90)

   # Save result
   img.save("output.png")

Batch Processing
~~~~~~~~~~~~~~~~

.. code-block:: python

   import puhu
   from pathlib import Path

   input_dir = Path("input_images")
   output_dir = Path("output_images")
   output_dir.mkdir(exist_ok=True)

   for img_path in input_dir.glob("*.jpg"):
       img = puhu.open(img_path)

       # Create thumbnail
       thumb = img.copy()
       thumb.thumbnail((300, 300))

       # Save thumbnail
       output_path = output_dir / f"{img_path.stem}_thumb.png"
       thumb.save(output_path)

       print(f"Processed {img_path.name}")
