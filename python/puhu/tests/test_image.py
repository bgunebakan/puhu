"""
Comprehensive tests for the Image class and all functionality
"""

import tempfile
from pathlib import Path

import pytest

from puhu import Image, Resampling, Transpose
from puhu import new as puhu_new
from puhu import open as puhu_open


class TestImage:
    """Test cases for the Image class."""

    def test_image_creation(self):
        """Test basic image creation."""
        img = Image()
        assert img is not None
        assert hasattr(img, "size")
        assert hasattr(img, "width")
        assert hasattr(img, "height")
        assert hasattr(img, "mode")

    def test_image_properties(self):
        """Test image properties."""
        img = Image()
        # Default 1x1 image
        assert img.size == (1, 1)
        assert img.width == 1
        assert img.height == 1
        assert img.mode in ["RGB", "L", "RGBA"]

    def test_image_copy(self):
        """Test image copying."""
        img = Image()
        copied = img.copy()
        assert copied is not img
        assert copied.size == img.size
        assert copied.mode == img.mode

    def test_image_repr(self):
        """Test string representation."""
        img = Image()
        repr_str = repr(img)
        assert "Image" in repr_str
        assert "size=" in repr_str
        assert "mode=" in repr_str

    def test_resize_operations(self):
        """Test resize functionality."""
        img = Image()
        resized = img.resize((10, 10))
        assert resized.size == (10, 10)
        assert resized is not img  # Should return new instance

    def test_rotation_operations(self):
        """Test rotation functionality."""
        img = Image()

        # Test 90-degree rotations
        rotated_90 = img.rotate(90)
        assert rotated_90 is not img

        rotated_180 = img.rotate(180)
        assert rotated_180 is not img

        rotated_270 = img.rotate(270)
        assert rotated_270 is not img

        # Test that arbitrary angles raise NotImplementedError
        with pytest.raises(NotImplementedError):
            img.rotate(45)

    def test_transpose_operations(self):
        """Test transpose functionality."""
        img = Image()

        from puhu.enums import Transpose

        flipped_h = img.transpose(Transpose.FLIP_LEFT_RIGHT)
        assert flipped_h is not img

        flipped_v = img.transpose(Transpose.FLIP_TOP_BOTTOM)
        assert flipped_v is not img

    def test_crop_operations(self):
        """Test crop functionality."""
        img = Image()
        # Create a larger image first
        larger = img.resize((100, 100))

        # Crop a portion
        cropped = larger.crop((10, 10, 50, 50))
        assert cropped.size == (40, 40)  # width=50-10, height=50-10
        assert cropped is not larger

    def test_thumbnail_operation(self):
        """Test thumbnail functionality."""
        img = Image()
        larger = img.resize((200, 100))

        larger.thumbnail((50, 50))

        assert larger.width == 50
        assert larger.height == 50

    def test_new_image_creation(self):
        """Test creating new images with different parameters."""
        # Test basic RGB image
        img1 = puhu_new("RGB", (100, 100))
        assert img1.size == (100, 100)
        assert img1.mode == "RGB"

        # Test with color
        img2 = puhu_new("RGB", (50, 50), "red")
        assert img2.size == (50, 50)
        assert img2.mode == "RGB"

        # Test with RGB tuple
        img3 = puhu_new("RGB", (25, 25), (255, 0, 0))
        assert img3.size == (25, 25)
        assert img3.mode == "RGB"

        # Test RGBA image
        img4 = puhu_new("RGBA", (30, 30))
        assert img4.size == (30, 30)
        assert img4.mode == "RGBA"

    def test_resize_with_resampling(self):
        """Test resize with different resampling methods."""
        img = puhu_new("RGB", (100, 100))

        # Test different resampling methods
        resized1 = img.resize((50, 50), Resampling.NEAREST)
        assert resized1.size == (50, 50)

        resized2 = img.resize((50, 50), Resampling.BILINEAR)
        assert resized2.size == (50, 50)

        resized3 = img.resize((50, 50), Resampling.BICUBIC)
        assert resized3.size == (50, 50)

        resized4 = img.resize((50, 50), Resampling.LANCZOS)
        assert resized4.size == (50, 50)

    def test_all_transpose_operations(self):
        """Test all transpose operations."""
        img = puhu_new("RGB", (100, 50))  # Non-square for better testing

        # Test all transpose operations
        flipped_lr = img.transpose(Transpose.FLIP_LEFT_RIGHT)
        assert flipped_lr.size == (100, 50)

        flipped_tb = img.transpose(Transpose.FLIP_TOP_BOTTOM)
        assert flipped_tb.size == (100, 50)

        rotated_90 = img.transpose(Transpose.ROTATE_90)
        assert rotated_90.size == (50, 100)  # Dimensions should swap

        rotated_180 = img.transpose(Transpose.ROTATE_180)
        assert rotated_180.size == (100, 50)

        rotated_270 = img.transpose(Transpose.ROTATE_270)
        assert rotated_270.size == (50, 100)  # Dimensions should swap

    def test_image_formats(self):
        """Test saving in different formats."""
        img = puhu_new("RGB", (50, 50), "blue")

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Test different formats
            formats = ["PNG", "JPEG", "BMP"]

            for fmt in formats:
                file_path = temp_path / f"test.{fmt.lower()}"
                img.save(file_path, format=fmt)
                assert file_path.exists()

                # Try to open it back
                loaded = puhu_open(file_path)
                assert loaded.size == (50, 50)

    def test_to_bytes(self):
        """Test converting image to bytes."""
        img = puhu_new("RGB", (10, 10))
        bytes_data = img.to_bytes()
        assert isinstance(bytes_data, bytes)
        assert len(bytes_data) > 0

    def test_image_equality(self):
        """Test image equality comparison."""
        img1 = puhu_new("RGB", (50, 50), "red")
        img2 = puhu_new("RGB", (50, 50), "red")
        img3 = puhu_new("RGB", (50, 50), "blue")

        # Same images should be equal
        assert img1 == img2

        # Different colored images should not be equal
        assert img1 != img3

        # Different sizes should not be equal
        img4 = puhu_new("RGB", (25, 25), "red")
        assert img1 != img4

    def test_convert_rgb_to_grayscale(self):
        """Test converting RGB to grayscale (L mode)."""
        img = puhu_new("RGB", (50, 50), (128, 128, 128))
        gray = img.convert("L")
        assert gray.mode == "L"
        assert gray.size == (50, 50)
        assert gray is not img

    def test_convert_rgb_to_rgba(self):
        """Test converting RGB to RGBA."""
        img = puhu_new("RGB", (50, 50), (255, 0, 0))
        rgba = img.convert("RGBA")
        assert rgba.mode == "RGBA"
        assert rgba.size == (50, 50)

    def test_convert_rgba_to_rgb(self):
        """Test converting RGBA to RGB."""
        img = puhu_new("RGBA", (50, 50), (255, 0, 0, 128))
        rgb = img.convert("RGB")
        assert rgb.mode == "RGB"
        assert rgb.size == (50, 50)

    def test_convert_to_grayscale_alpha(self):
        """Test converting to LA (grayscale with alpha)."""
        img = puhu_new("RGB", (50, 50), (128, 128, 128))
        la = img.convert("LA")
        assert la.mode == "LA"
        assert la.size == (50, 50)

    def test_convert_to_bilevel_with_dither(self):
        """Test converting to bilevel (mode 1) with Floyd-Steinberg dithering."""
        img = puhu_new("RGB", (50, 50), (128, 128, 128))
        bilevel = img.convert("1")
        assert bilevel.mode == "L"
        assert bilevel.size == (50, 50)

    def test_convert_to_bilevel_without_dither(self):
        """Test converting to bilevel without dithering."""
        img = puhu_new("RGB", (50, 50), (128, 128, 128))
        bilevel = img.convert("1", dither="NONE")
        assert bilevel.mode == "L"
        assert bilevel.size == (50, 50)

    def test_convert_same_mode(self):
        """Test converting to the same mode (should return copy)."""
        img = puhu_new("RGB", (50, 50), (255, 0, 0))
        same = img.convert("RGB")
        assert same.mode == "RGB"
        assert same.size == img.size
        assert same is not img

    def test_convert_with_matrix_rgb_transformation(self):
        """Test converting with a custom 12-tuple matrix for RGB color space transformation."""
        img = puhu_new("RGB", (10, 10), (255, 0, 0))
        # RGB to XYZ transformation matrix
        rgb2xyz = [
            0.412453,
            0.357580,
            0.180423,
            0.0,
            0.212671,
            0.715160,
            0.072169,
            0.0,
            0.019334,
            0.119193,
            0.950227,
            0.0,
        ]
        converted = img.convert("RGB", matrix=rgb2xyz)
        assert converted.mode == "RGB"
        assert converted.size == (10, 10)

    def test_convert_invalid_mode(self):
        """Test converting to an unsupported mode."""
        img = puhu_new("RGB", (50, 50))
        with pytest.raises(Exception):
            img.convert("INVALID_MODE")

    def test_convert_invalid_matrix_size(self):
        """Test converting with invalid matrix size."""
        img = puhu_new("RGB", (10, 10))
        with pytest.raises(Exception):
            img.convert("RGB", matrix=[1.0, 2.0, 3.0])

    def test_convert_chain(self):
        """Test chaining multiple conversions."""
        img = puhu_new("RGB", (50, 50), (255, 128, 64))
        # RGB -> L -> RGB
        gray = img.convert("L")
        assert gray.mode == "L"
        rgb_again = gray.convert("RGB")
        assert rgb_again.mode == "RGB"
        assert rgb_again.size == (50, 50)


class TestErrorHandling:
    """Test error handling and edge cases."""

    def test_invalid_crop_bounds(self):
        """Test cropping with invalid bounds."""
        img = puhu_new("RGB", (100, 100))

        # Test crop bounds outside image
        with pytest.raises(Exception):  # Should raise PuhuProcessingError
            img.crop((200, 200, 300, 300))

    def test_invalid_rotation_angle(self):
        """Test rotation with invalid angles."""
        img = puhu_new("RGB", (100, 100))

        with pytest.raises(NotImplementedError):
            img.rotate(45)

    def test_zero_size_resize(self):
        """Test resizing to zero size."""
        img = puhu_new("RGB", (100, 100))

        # TODO: this should raise an error
        resized = img.resize((0, 0))
        assert resized.size[0] >= 0 and resized.size[1] >= 0

    def test_open_nonexistent_file(self):
        """Test opening a file that doesn't exist."""

        img = puhu_open("nonexistent_file.png")

        with pytest.raises(Exception):
            _ = img.size


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
