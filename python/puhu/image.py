"""
Python Image class that wraps the Rust Puhu implementation
"""

from pathlib import Path
from typing import Any, Optional, Tuple, Union

from ._core import Image as RustImage
from .enums import Resampling, Transpose


class Image:
    """
    A high-performance image class backed by Rust.

    This class provides a Pillow-compatible API while leveraging Rust's
    performance and memory safety for all image operations.
    """

    def __init__(self, rust_image=None):
        """Initialize an Image instance."""
        if RustImage is None:
            raise ImportError(
                "Puhu Rust extension not available. "
                "Please install with: pip install puhu"
            )

        if rust_image is None:
            rust_image = RustImage()
        self._rust_image = rust_image

    @classmethod
    def open(
        cls,
        fp: Union[str, Path, bytes],
        mode: Optional[str] = None,
        formats: Optional[list] = None,
    ) -> "Image":
        """
        Open an image file.

        Args:
            fp: File path, file object, or bytes
            mode: Optional mode hint TODO: implement
            formats: Optional list of formats to try TODO: implement

        Returns:
            Image instance
        """
        if isinstance(fp, Path):
            fp = str(fp)

        rust_image = RustImage.open(fp)
        return cls(rust_image)

    @classmethod
    def new(
        cls,
        mode: str,
        size: Tuple[int, int],
        color: Union[int, Tuple[int, ...], str] = 0,
    ) -> "Image":
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
        # Convert color to RGBA tuple
        rgba_color = cls._parse_color(color, mode)

        rust_image = RustImage.new(mode, size, rgba_color)
        return cls(rust_image)

    @staticmethod
    def _parse_color(
        color: Union[int, Tuple[int, ...], str], mode: str
    ) -> Optional[Tuple[int, int, int, int]]:
        """
        Parse color input into RGBA tuple format.
        """
        if color is None:
            return None

        # Handle string colors (basic support)
        if isinstance(color, str):
            color_map = {
                "black": (0, 0, 0, 255),
                "white": (255, 255, 255, 255),
                "red": (255, 0, 0, 255),
                "green": (0, 255, 0, 255),
                "blue": (0, 0, 255, 255),
                "yellow": (255, 255, 0, 255),
                "cyan": (0, 255, 255, 255),
                "magenta": (255, 0, 255, 255),
            }
            if color.lower() in color_map:
                return color_map[color.lower()]
            else:
                raise ValueError(f"Unsupported color name: {color}")

        # Handle integer (grayscale)
        if isinstance(color, int):
            if mode in ["L", "LA"]:
                return (color, 0, 0, 255 if mode == "L" else color)
            else:
                return (color, color, color, 255)

        # Handle tuple
        if isinstance(color, (tuple, list)):
            color = tuple(color)
            if len(color) == 1:
                return (color[0], color[0], color[0], 255)
            elif len(color) == 2:
                # For LA mode: (grayscale, alpha)
                if mode == "LA":
                    return (color[0], 0, 0, color[1])
                else:
                    # For other modes, treat as grayscale with alpha
                    return (color[0], color[0], color[0], color[1])
            elif len(color) == 3:
                return (color[0], color[1], color[2], 255)
            elif len(color) == 4:
                return color
            else:
                raise ValueError(f"Invalid color tuple length: {len(color)}")

        raise ValueError(f"Unsupported color type: {type(color)}")

    def save(
        self, fp: Union[str, Path], format: Optional[str] = None, **options
    ) -> None:
        """
        Save the image to a file.

        Args:
            fp: File path to save to
            format: Image format (e.g., 'JPEG', 'PNG')
            **options: Additional save options (TODO: implement)
        """
        if isinstance(fp, Path):
            fp = str(fp)

        self._rust_image.save(fp, format)

    def resize(
        self,
        size: Tuple[int, int],
        resample: Union[int, str] = Resampling.BILINEAR,
    ) -> "Image":
        """
        Resize the image.

        Args:
            size: Target size as (width, height)
            resample: Resampling filter

        Returns:
            New resized Image instance
        """
        if isinstance(resample, int):
            resample = Resampling.from_int(resample)

        rust_image = self._rust_image.resize(size, resample)
        return Image(rust_image)

    def crop(self, box: Tuple[int, int, int, int]) -> "Image":
        """
        Crop the image.

        Args:
            box: Crop box as (left, top, right, bottom)

        Returns:
            New cropped Image instance
        """
        # Convert Pillow-style box (left, top, right, bottom) to
        # our format (x, y, width, height)
        left, top, right, bottom = box
        width = right - left
        height = bottom - top

        rust_image = self._rust_image.crop((left, top, width, height))
        return Image(rust_image)

    def rotate(
        self,
        angle: float,
        expand: bool = False,
        fillcolor: Optional[Any] = None,
    ) -> "Image":
        """
        Rotate the image.

        Args:
            angle: Rotation angle in degrees
            expand: Whether to expand the image to fit the rotated content
            fillcolor: Fill color for empty areas (TODO: implement)

        Returns:
            New rotated Image instance
        """
        # Only support 90-degree rotations TODO: implement arbitrary angles
        angle = angle % 360

        if angle in [90, 180, 270]:
            rust_image = self._rust_image.rotate(float(angle))
        else:
            raise NotImplementedError(
                f"Arbitrary angle rotation ({angle}°) not yet implemented. "
                "Only 90°, 180°, and 270° rotations are supported."
            )

        return Image(rust_image)

    def transpose(self, method: Union[int, str]) -> "Image":
        """
        Transpose the image.

        Args:
            method: Transpose method

        Returns:
            New transposed Image instance
        """
        if isinstance(method, int):
            method = Transpose.from_int(method)

        if method == Transpose.FLIP_LEFT_RIGHT:
            method_str = "FLIP_LEFT_RIGHT"
        elif method == Transpose.FLIP_TOP_BOTTOM:
            method_str = "FLIP_TOP_BOTTOM"
        elif method == Transpose.ROTATE_90:
            method_str = "ROTATE_90"
        elif method == Transpose.ROTATE_180:
            method_str = "ROTATE_180"
        elif method == Transpose.ROTATE_270:
            method_str = "ROTATE_270"
        else:
            raise NotImplementedError(f"Transpose method {method} not yet implemented")

        rust_image = self._rust_image.transpose(method_str)

        return Image(rust_image)

    def copy(self) -> "Image":
        """Create a copy of the image."""
        rust_image = self._rust_image.copy()
        return Image(rust_image)

    def thumbnail(
        self,
        size: Tuple[int, int],
        resample: Union[int, str] = Resampling.BICUBIC,
    ) -> None:
        """
        Create a thumbnail version of the image in-place.

        Args:
            size: Maximum size as (width, height)
            resample: Resampling filter
        """
        # Calculate thumbnail size preserving aspect ratio
        current_width, current_height = self.size
        max_width, max_height = size

        width_ratio = max_width / current_width
        height_ratio = max_height / current_height
        scale = min(width_ratio, height_ratio)

        new_width = int(current_width * scale)
        new_height = int(current_height * scale)

        # Resize in-place by replacing the rust image
        self._rust_image = self._rust_image.resize((new_width, new_height), resample)

    def to_bytes(self) -> bytes:
        """Get the raw pixel data as bytes."""
        return self._rust_image.to_bytes()

    def convert(
        self,
        mode: str,
        matrix: Optional[Tuple[float, ...]] = None,
        dither: Optional[str] = None,
        palette: str = "WEB",
        colors: int = 256,
    ) -> "Image":
        """
        Convert the image to a different mode.

        Args:
            mode: Target mode (e.g., 'L', 'RGB', 'RGBA', 'LA', '1', 'P')
            matrix: Optional conversion matrix (4-tuple or 12-tuple of floats).
                   If given, this should be a 4- or 12-tuple containing floating point values.
            dither: Dithering method, used when converting from mode "RGB" to "P" 
                   or from "RGB" or "L" to "1". Available methods are "NONE" or 
                   "FLOYDSTEINBERG" (default). Note that this is not used when matrix is supplied.
            palette: Palette to use when converting from mode "RGB" to "P".
                    Available palettes are "WEB" (default) or "ADAPTIVE".
            colors: Number of colors to use for the "ADAPTIVE" palette. Defaults to 256.

        Returns:
            Image instance in the target mode

        Examples:
            >>> img = Image.new('RGB', (100, 100))
            >>> gray = img.convert('L')  # Convert to grayscale
            >>> rgba = img.convert('RGBA')  # Add alpha channel
            >>> bw = img.convert('1')  # Convert to black and white with dithering
            >>> bw_no_dither = img.convert('1', dither='NONE')  # No dithering
            >>> palette_img = img.convert('P', palette='ADAPTIVE', colors=128)  # 128-color palette
        """
        matrix_list = list(matrix) if matrix is not None else None

        rust_image = self._rust_image.convert(
            mode, matrix=matrix_list, dither=dither, palette=palette, colors=colors
        )
        return Image(rust_image)

    # Properties
    @property
    def size(self) -> Tuple[int, int]:
        """Image size as (width, height)."""
        return self._rust_image.size

    @property
    def width(self) -> int:
        """Image width in pixels."""
        return self._rust_image.width

    @property
    def height(self) -> int:
        """Image height in pixels."""
        return self._rust_image.height

    @property
    def mode(self) -> str:
        """Image mode (e.g., 'RGB', 'RGBA', 'L')."""
        return self._rust_image.mode

    @property
    def format(self) -> Optional[str]:
        """Image format (e.g., 'JPEG', 'PNG')."""
        return self._rust_image.format

    @property
    def info(self) -> dict:
        """Image metadata dictionary."""
        # TODO: Implement metadata extraction in Rust
        return {}

    def __repr__(self) -> str:
        """String representation of the image."""
        return self._rust_image.__repr__()

    def __eq__(self, other) -> bool:
        """Compare two images for equality."""
        if not isinstance(other, Image):
            return False

        # Basic comparison TODO: improve with pixel-level comparison
        return (
            self.size == other.size
            and self.mode == other.mode
            and self.to_bytes() == other.to_bytes()
        )
