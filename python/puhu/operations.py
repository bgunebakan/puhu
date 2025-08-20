"""
Functional API for image operations
provides Pillow-compatible module-level functions
"""

from pathlib import Path
from typing import Optional, Tuple, Union

from .enums import Resampling
from .image import Image


def open(
    fp: Union[str, Path, bytes],
    mode: Optional[str] = None,
    formats: Optional[list] = None,
) -> Image:
    """
    Open an image file.

    Args:
        fp: File path, file object, or bytes
        mode: Optional mode hint TODO: implement
        formats: Optional list of formats TODO: implement

    Returns:
        Image instance
    """
    return Image.open(fp, mode, formats)


def new(
    mode: str,
    size: Tuple[int, int],
    color: Union[int, Tuple[int, ...], str] = 0,
) -> Image:
    """
    Create a new image with the given mode and size.

    Args:
        mode: Image mode (e.g., 'RGB', 'RGBA', 'L', 'LA')
        size: Image size as (width, height)
        color: Fill color. Can be:
            - Single integer for grayscale modes
            - Tuple of integers for RGB/RGBA modes
            - String color name (basic colors only)
            - Default is 0 (black/transparent)

    Returns:
        New Image instance
    """
    return Image.new(mode, size, color)


def save(
    image: Image, fp: Union[str, Path], format: Optional[str] = None, **options
) -> None:
    """
    Save an image to a file.

    Args:
        image: Image instance to save
        fp: File path to save to
        format: Image format (e.g., 'JPEG', 'PNG')
        **options: Additional save options (not yet implemented)
    """
    image.save(fp, format, **options)


def resize(
    image: Image,
    size: Tuple[int, int],
    resample: Union[int, str] = Resampling.BILINEAR,
) -> Image:
    """
    Resize an image.

    Args:
        image: Image instance to resize
        size: Target size as (width, height)
        resample: Resampling filter

    Returns:
        New resized Image instance
    """
    return image.resize(size, resample)


def crop(image: Image, box: Tuple[int, int, int, int]) -> Image:
    """
    Crop an image.

    Args:
        image: Image instance to crop
        box: Crop box as (left, top, right, bottom)

    Returns:
        New cropped Image instance
    """
    return image.crop(box)


def rotate(image: Image, angle: float, expand: bool = False) -> Image:
    """
    Rotate an image.

    Args:
        image: Image instance to rotate
        angle: Rotation angle in degrees
        expand: Whether to expand the image to fit the rotated content

    Returns:
        New rotated Image instance
    """
    return image.rotate(angle, expand)


def convert(image: Image, mode: str) -> Image:
    """
    Convert an image to a different mode.

    Args:
        image: Image instance to convert
        mode: Target mode (e.g., 'RGB', 'L', 'RGBA')

    Returns:
        New converted Image instance

    Note:
        This is a placeholder - mode conversion is not yet implemented
    """
    raise NotImplementedError("Mode conversion not yet implemented")


def thumbnail(
    image: Image,
    size: Tuple[int, int],
    resample: Union[int, str] = Resampling.BICUBIC,
) -> None:
    """
    Create a thumbnail version of the image in-place.

    Args:
        image: Image instance to thumbnail
        size: Maximum size as (width, height)
        resample: Resampling filter
    """
    image.thumbnail(size, resample)
