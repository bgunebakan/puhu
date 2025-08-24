"""
Python Image class that wraps the Rust Puhu implementation
"""

from pathlib import Path
from typing import Any, List, Optional, Tuple, Union

from ._core import Image as RustImage
from .enums import Resampling, Transpose

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    np = None
    HAS_NUMPY = False


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

    @classmethod
    def fromarray(
        cls,
        obj: Any,
        mode: Optional[str] = None,
    ) -> "Image":
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
        if not HAS_NUMPY:
            raise ImportError("numpy is required for fromarray(). Install with: pip install numpy")

        if not isinstance(obj, np.ndarray):
            raise ValueError("Expected numpy array")

        # Convert to uint8 if needed
        if obj.dtype != np.uint8:
            if obj.dtype in [np.float32, np.float64]:
                # Assume values are in [0, 1] range
                obj = (obj * 255).astype(np.uint8)
            else:
                obj = obj.astype(np.uint8)

        # Ensure array is contiguous
        if not obj.flags.c_contiguous:
            obj = np.ascontiguousarray(obj)

        rust_image = RustImage.fromarray(obj, mode)
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

    def convert(self, mode: str) -> "Image":
        """
        Convert the image to a different mode.

        Args:
            mode: Target mode (e.g., 'RGB', 'L', 'RGBA', 'LA')

        Returns:
            New converted Image instance
        """
        rust_image = self._rust_image.convert(mode)
        return Image(rust_image)

    def split(self) -> List["Image"]:
        """
        Split the image into individual channel images.

        Returns:
            List of Image instances, one for each channel
            - RGB images return [R, G, B]
            - RGBA images return [R, G, B, A]
            - Grayscale images return [L]
            - LA images return [L, A]
        """
        rust_images = self._rust_image.split()
        return [Image(rust_img) for rust_img in rust_images]

    def paste(
        self,
        im: "Image",
        box: Optional[Union[Tuple[int, int], Tuple[int, int, int, int]]] = None,
        mask: Optional["Image"] = None,
    ) -> "Image":
        """
        Paste another image onto this image.

        Args:
            im: Image to paste
            box: Position to paste at. Can be:
                - (x, y) tuple for position
                - (x, y, x2, y2) tuple for position and size (size ignored)
                - None for (0, 0)
            mask: Optional mask image for alpha blending

        Returns:
            New Image instance with the pasted content
        """
        # Parse position from box parameter
        if box is None:
            position = (0, 0)
        elif len(box) == 2:
            position = box
        elif len(box) == 4:
            position = (box[0], box[1])  # Ignore size for now
        else:
            raise ValueError("box must be a 2-tuple (x, y) or 4-tuple (x, y, x2, y2)")

        # Get rust mask image if provided
        rust_mask = mask._rust_image if mask is not None else None

        rust_image = self._rust_image.paste(im._rust_image, position, rust_mask)
        return Image(rust_image)

    def blur(self, radius: float) -> "Image":
        """
        Apply Gaussian blur to the image.

        Args:
            radius: Blur radius (higher values = more blur)

        Returns:
            New blurred Image instance
        """
        rust_image = self._rust_image.blur(radius)
        return Image(rust_image)

    def sharpen(self, strength: float = 1.0) -> "Image":
        """
        Apply sharpening filter to the image.

        Args:
            strength: Sharpening strength (default: 1.0)

        Returns:
            New sharpened Image instance
        """
        rust_image = self._rust_image.sharpen(strength)
        return Image(rust_image)

    def edge_detect(self) -> "Image":
        """
        Apply edge detection filter (Sobel operator).

        Returns:
            New grayscale Image instance with edges highlighted
        """
        rust_image = self._rust_image.edge_detect()
        return Image(rust_image)

    def emboss(self) -> "Image":
        """
        Apply emboss filter to the image.

        Returns:
            New embossed Image instance
        """
        rust_image = self._rust_image.emboss()
        return Image(rust_image)

    def brightness(self, adjustment: int) -> "Image":
        """
        Adjust image brightness.

        Args:
            adjustment: Brightness adjustment (-255 to 255)
                       Positive values brighten, negative values darken

        Returns:
            New Image instance with adjusted brightness
        """
        rust_image = self._rust_image.brightness(adjustment)
        return Image(rust_image)

    def contrast(self, factor: float) -> "Image":
        """
        Adjust image contrast.

        Args:
            factor: Contrast factor
                   1.0 = no change
                   > 1.0 = increase contrast
                   < 1.0 = decrease contrast
                   0.0 = gray image

        Returns:
            New Image instance with adjusted contrast
        """
        rust_image = self._rust_image.contrast(factor)
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

    # CSS-like filters
    def sepia(self, amount=1.0):
        """Apply sepia filter.

        Args:
            amount (float): Sepia amount (0.0 to 1.0)

        Returns:
            Image: New image with sepia effect
        """
        return Image(self._rust_image.sepia(amount))

    def grayscale_filter(self, amount=1.0):
        """Apply grayscale filter.

        Args:
            amount (float): Grayscale amount (0.0 to 1.0)

        Returns:
            Image: New image with grayscale effect
        """
        return Image(self._rust_image.grayscale_filter(amount))

    def invert(self, amount=1.0):
        """Apply invert filter.

        Args:
            amount (float): Invert amount (0.0 to 1.0)

        Returns:
            Image: New image with invert effect
        """
        return Image(self._rust_image.invert(amount))

    def hue_rotate(self, degrees):
        """Apply hue rotation filter.

        Args:
            degrees (float): Rotation in degrees

        Returns:
            Image: New image with rotated hue
        """
        return Image(self._rust_image.hue_rotate(degrees))

    def saturate(self, amount=1.0):
        """Apply saturation filter.

        Args:
            amount (float): Saturation amount (0.0 = grayscale, 1.0 = normal, >1.0 = more saturated)

        Returns:
            Image: New image with adjusted saturation
        """
        return Image(self._rust_image.saturate(amount))

    # Pixel manipulation methods
    def getpixel(self, x, y):
        """Get pixel value at coordinates.

        Args:
            x (int): X coordinate
            y (int): Y coordinate

        Returns:
            tuple: (R, G, B, A) pixel values
        """
        return self._rust_image.getpixel(x, y)

    def putpixel(self, x, y, color):
        """Set pixel value at coordinates.

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            color (tuple): (R, G, B, A) color values

        Returns:
            Image: New image with modified pixel
        """
        return Image(self._rust_image.putpixel(x, y, color))

    def histogram(self):
        """Get image histogram.

        Returns:
            tuple: (R_hist, G_hist, B_hist, A_hist) histograms as lists
        """
        return self._rust_image.histogram()

    def dominant_color(self):
        """Get dominant color in image.

        Returns:
            tuple: (R, G, B, A) dominant color
        """
        return self._rust_image.dominant_color()

    def average_color(self):
        """Get average color in image.

        Returns:
            tuple: (R, G, B, A) average color
        """
        return self._rust_image.average_color()

    def replace_color(self, target_color, replacement_color, tolerance=0):
        """Replace pixels of one color with another.

        Args:
            target_color (tuple): (R, G, B, A) color to replace
            replacement_color (tuple): (R, G, B, A) replacement color
            tolerance (int): Color matching tolerance (0-255)

        Returns:
            Image: New image with replaced colors
        """
        return Image(self._rust_image.replace_color(target_color, replacement_color, tolerance))

    def threshold(self, threshold_value):
        """Apply threshold to create binary image.

        Args:
            threshold_value (int): Threshold value (0-255)

        Returns:
            Image: New binary image
        """
        return Image(self._rust_image.threshold(threshold_value))

    def posterize(self, levels):
        """Apply posterization effect.

        Args:
            levels (int): Number of color levels

        Returns:
            Image: New posterized image
        """
        return Image(self._rust_image.posterize(levels))

    # Drawing methods
    def draw_rectangle(self, x, y, width, height, color):
        """Draw a filled rectangle.

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            width (int): Rectangle width
            height (int): Rectangle height
            color (tuple): (R, G, B, A) color

        Returns:
            Image: New image with rectangle drawn
        """
        return Image(self._rust_image.draw_rectangle(x, y, width, height, color))

    def draw_circle(self, center_x, center_y, radius, color):
        """Draw a filled circle.

        Args:
            center_x (int): Center X coordinate
            center_y (int): Center Y coordinate
            radius (int): Circle radius
            color (tuple): (R, G, B, A) color

        Returns:
            Image: New image with circle drawn
        """
        return Image(self._rust_image.draw_circle(center_x, center_y, radius, color))

    def draw_line(self, x0, y0, x1, y1, color):
        """Draw a line.

        Args:
            x0 (int): Start X coordinate
            y0 (int): Start Y coordinate
            x1 (int): End X coordinate
            y1 (int): End Y coordinate
            color (tuple): (R, G, B, A) color

        Returns:
            Image: New image with line drawn
        """
        return Image(self._rust_image.draw_line(x0, y0, x1, y1, color))

    def draw_text(self, text, x, y, color, scale=1):
        """Draw text using basic bitmap font.

        Args:
            text (str): Text to draw
            x (int): X coordinate
            y (int): Y coordinate
            color (tuple): (R, G, B, A) color
            scale (int): Text scale factor

        Returns:
            Image: New image with text drawn
        """
        return Image(self._rust_image.draw_text(text, x, y, color, scale))

    # Shadow effects
    def drop_shadow(self, offset_x, offset_y, blur_radius, shadow_color):
        """Apply drop shadow effect.

        Args:
            offset_x (int): Shadow X offset
            offset_y (int): Shadow Y offset
            blur_radius (float): Shadow blur radius
            shadow_color (tuple): (R, G, B, A) shadow color

        Returns:
            Image: New image with drop shadow
        """
        return Image(self._rust_image.drop_shadow(offset_x, offset_y, blur_radius, shadow_color))

    def inner_shadow(self, offset_x, offset_y, blur_radius, shadow_color):
        """Apply inner shadow effect.

        Args:
            offset_x (int): Shadow X offset
            offset_y (int): Shadow Y offset
            blur_radius (float): Shadow blur radius
            shadow_color (tuple): (R, G, B, A) shadow color

        Returns:
            Image: New image with inner shadow
        """
        return Image(self._rust_image.inner_shadow(offset_x, offset_y, blur_radius, shadow_color))

    def glow(self, blur_radius, glow_color, intensity=1.0):
        """Apply glow effect.

        Args:
            blur_radius (float): Glow blur radius
            glow_color (tuple): (R, G, B, A) glow color
            intensity (float): Glow intensity

        Returns:
            Image: New image with glow effect
        """
        return Image(self._rust_image.glow(blur_radius, glow_color, intensity))
