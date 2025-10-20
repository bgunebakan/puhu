.. Puhu documentation master file

Puhu 🦉 - High-Performance Image Processing
===========================================

.. image:: https://github.com/bgunebakan/puhu/workflows/CI/badge.svg
   :target: https://github.com/bgunebakan/puhu/actions
   :alt: CI

.. image:: https://img.shields.io/pypi/v/puhu.svg
   :target: https://pypi.org/project/puhu/
   :alt: PyPI

.. image:: https://img.shields.io/badge/python-3.8+-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python

.. image:: https://img.shields.io/badge/rust-1.70+-orange.svg
   :target: https://www.rust-lang.org/
   :alt: Rust

.. image:: https://img.shields.io/badge/license-MIT-green.svg
   :target: https://github.com/bgunebakan/puhu/blob/main/LICENSE
   :alt: License

A modern image processing library for Python, powered by Rust. Puhu provides a Pillow-compatible API while delivering significantly better performance for common image operations.

Key Features
------------

- **High Performance**: Significantly fast for common image operations
- **Pillow Compatible**: Drop-in replacement for most Pillow operations
- **Rust Powered**: Memory-safe and efficient core written in Rust
- **Easy to Use**: Simple, intuitive API that feels familiar
- **Format Support**: PNG, JPEG, BMP, TIFF, GIF, WEBP

Quick Example
-------------

.. code-block:: python

   import puhu

   # Open an image
   img = puhu.open("photo.jpg")

   # Resize image
   resized = img.resize((800, 600))

   # Crop image
   cropped = img.crop((100, 100, 500, 400))

   # Rotate image
   rotated = img.rotate(90)

   # Save image
   img.save("output.png")

Platform Support
----------------

Pre-built wheels available for:

- Linux (x86_64, ARM64)
- macOS (Intel, Apple Silicon M1/M2/M3)
- Windows (x64)
- Python 3.8+

Documentation Contents
----------------------

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   installation
   quickstart
   pillow_compatibility

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api

.. toctree::
   :maxdepth: 2
   :caption: Development

   contributing
   changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
