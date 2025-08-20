"""
Puhu - A high-performance, memory-safe image processing library

Provides the high-level API while addressing
performance and memory-safety issues through a Rust backend.
"""

from .image import Image
from .enums import ImageMode, ImageFormat, Resampling, Transpose
from .operations import open, new, save, resize, crop, rotate, convert

__version__ = "0.1.0"
__author__ = "Bilal Tonga"

__all__ = [
    "Image",
    "ImageMode",
    "ImageFormat",
    "Resampling",
    "Transpose",
    "open",
    "new",
    "save",
    "resize",
    "crop",
    "rotate",
    "convert",
]
