Changelog
=========

All notable changes to Puhu will be documented here.

The format is based on `Keep a Changelog <https://keepachangelog.com/>`_.

Version 0.3.0 (Current)
-----------------------

**Added**

- ``paste()`` method for image composition with full Pillow compatibility:

  - 2-tuple and 4-tuple box coordinates
  - Negative coordinates with automatic clipping
  - Color fills via RGB/RGBA tuples, single integers, or color strings
  - Mask-based alpha blending
  - Abbreviated syntax ``paste(im, mask)``
  - Automatic mode conversion between source and destination

Version 0.2.2
-----------------------

**Added**

- Comprehensive documentation on ReadTheDocs
- Enhanced error messages with coordinate information
- Improved crop bounds validation

**Changed**

- Updated PyO3 from 0.19 to 0.22
- Improved memory efficiency by removing unnecessary clones
- Enhanced error propagation in getter methods

**Fixed**

- Fixed memory inefficiency in LazyImage::Bytes loading
- Fixed inconsistent mutability in getter methods
- Removed redundant unreachable patterns

Version 0.2.0
-------------

**Added**

- ``rotate()`` method for 90°, 180°, 270° rotations
- ``transpose()`` method for flipping operations
- ``thumbnail()`` method for in-place resizing
- ``copy()`` method for creating image copies
- Support for WEBP format
- Support for TIFF format
- Support for GIF format

**Changed**

- Improved resize performance
- Better error handling across all operations

**Fixed**

- Fixed crop bounds validation
- Fixed color conversion edge cases

Version 0.1.0
-------------

**Added**

- Initial release
- Core image operations: ``open()``, ``save()``, ``new()``
- Basic transformations: ``resize()``, ``crop()``
- Support for PNG, JPEG, BMP formats
- RGB, RGBA, and L (grayscale) modes
- Resampling filters: NEAREST, BILINEAR, BICUBIC
- Pillow-compatible API
- Cross-platform wheels (Linux, macOS, Windows)

Upcoming Features
-----------------

Planned for Next Release
~~~~~~~~~~~~~~~~~~~~~~~~

- ``paste()`` method for image composition
- ``split()`` and ``merge()`` for band operations
- ``fromarray()`` for NumPy integration
- Additional image modes

Under Consideration
~~~~~~~~~~~~~~~~~~~

- ``filter()`` operations (blur, sharpen, etc.)
- ``getpixel()`` and ``putpixel()`` for pixel access
- ``convert()`` for mode conversion
- EXIF metadata support
- Animated GIF support

Migration Notes
---------------

From 0.1.x to 0.2.x
~~~~~~~~~~~~~~~~~~~

**Breaking Changes**: None

**New Features**: The 0.2.x series adds new methods while maintaining full backward compatibility with 0.1.x.

**Recommended Actions**:

- Update to 0.2.x for performance improvements
- Start using new methods like ``rotate()`` and ``transpose()``
- Update error handling to use improved error messages

Contributing
------------

See :doc:`contributing` for information on how to contribute features or bug fixes.

Release Process
---------------

For maintainers, see `.github/RELEASE.md <https://github.com/bgunebakan/puhu/blob/main/.github/RELEASE.md>`_ for the complete release workflow.
