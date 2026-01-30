"""
Puhu - A high-performance, memory-safe image processing library

Provides the high-level API while addressing
performance and memory-safety issues through a Rust backend.
"""

from .enums import Palette  # noqa: F401
from .enums import Dither, ImageFormat, ImageMode, Resampling, Transpose
from .image import Image
from .operations import convert, crop, new, open, resize, rotate, save

__version__ = "0.3.0"
__author__ = "Bilal Tonga"

__all__ = [
    "Image",
    "ImageMode",
    "ImageFormat",
    "Resampling",
    "Transpose",
    "Dither",
    "Palette",
    "open",
    "new",
    "save",
    "resize",
    "crop",
    "rotate",
    "convert",
]
