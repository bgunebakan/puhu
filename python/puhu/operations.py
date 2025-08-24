"""
Functional API for image operations
provides Pillow-compatible module-level functions
"""

from pathlib import Path
from typing import Any, List, Optional, Tuple, Union

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
    """
    return image.convert(mode)


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


def fromarray(obj: Any, mode: Optional[str] = None) -> Image:
    """
    Create an image from a numpy array.

    Args:
        obj: Numpy array with shape (H, W) for grayscale or (H, W, C) for RGB/RGBA
        mode: Optional mode hint (not currently used)

    Returns:
        New Image instance

    Raises:
        ImportError: If numpy is not available
        ValueError: If array has unsupported shape or dtype
    """
    return Image.fromarray(obj, mode)


def split(image: Image) -> List[Image]:
    """
    Split an image into individual channel images.

    Args:
        image: Image instance to split

    Returns:
        List of Image instances, one for each channel
        - RGB images return [R, G, B]
        - RGBA images return [R, G, B, A]
        - Grayscale images return [L]
        - LA images return [L, A]
    """
    return image.split()


def paste(
    base_image: Image,
    paste_image: Image,
    box: Optional[Union[Tuple[int, int], Tuple[int, int, int, int]]] = None,
    mask: Optional[Image] = None,
) -> Image:
    """
    Paste one image onto another.

    Args:
        base_image: Base image to paste onto
        paste_image: Image to paste
        box: Position to paste at. Can be:
            - (x, y) tuple for position
            - (x, y, x2, y2) tuple for position and size (size ignored)
            - None for (0, 0)
        mask: Optional mask image for alpha blending

    Returns:
        New Image instance with the pasted content
    """
    return base_image.paste(paste_image, box, mask)


def blur(image: Image, radius: float) -> Image:
    """
    Apply Gaussian blur to an image.

    Args:
        image: Image instance to blur
        radius: Blur radius (higher values = more blur)

    Returns:
        New blurred Image instance
    """
    return image.blur(radius)


def sharpen(image: Image, strength: float = 1.0) -> Image:
    """
    Apply sharpening filter to an image.

    Args:
        image: Image instance to sharpen
        strength: Sharpening strength (default: 1.0)

    Returns:
        New sharpened Image instance
    """
    return image.sharpen(strength)


def edge_detect(image: Image) -> Image:
    """
    Apply edge detection filter to an image.

    Args:
        image: Image instance to process

    Returns:
        New grayscale Image instance with edges highlighted
    """
    return image.edge_detect()


def emboss(image: Image) -> Image:
    """
    Apply emboss filter to an image.

    Args:
        image: Image instance to emboss

    Returns:
        New embossed Image instance
    """
    return image.emboss()


def brightness(image: Image, adjustment: int) -> Image:
    """
    Adjust image brightness.

    Args:
        image: Image instance to adjust
        adjustment: Brightness adjustment (-255 to 255)
                   Positive values brighten, negative values darken

    Returns:
        New Image instance with adjusted brightness
    """
    return image.brightness(adjustment)


def contrast(image: Image, factor: float) -> Image:
    """
    Adjust image contrast.

    Args:
        image: Image instance to adjust
        factor: Contrast factor
               1.0 = no change
               > 1.0 = increase contrast
               < 1.0 = decrease contrast
               0.0 = gray image

    Returns:
        New Image instance with adjusted contrast
    """
    return image.contrast(factor)
