"""
Puhu - A high-performance, memory-safe image processing library

Provides the high-level API while addressing
performance and memory-safety issues through a Rust backend.
"""

from .enums import ImageFormat, ImageMode, Resampling, Transpose
from .image import Image
from .operations import (
    blur, brightness, contrast, convert, crop, edge_detect, emboss,
    fromarray, new, open, paste, resize, rotate, save, sharpen, split
)

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
    "fromarray",
    "split",
    "paste",
    # Filters
    "blur",
    "sharpen",
    "edge_detect",
    "emboss",
    "brightness",
    "contrast",
]
