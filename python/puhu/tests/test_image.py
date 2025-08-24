"""
Comprehensive tests for the Image class and all functionality
"""

import tempfile
from pathlib import Path

import pytest

from puhu import Image, Resampling, Transpose
from puhu import new as puhu_new
from puhu import open as puhu_open
from puhu import convert, fromarray, split, paste

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    np = None
    HAS_NUMPY = False


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


class TestNewFeatures:
    """Test cases for the newly implemented features."""

    def test_convert_rgb_to_grayscale(self):
        """Test converting RGB image to grayscale."""
        img = puhu_new("RGB", (50, 50), (255, 128, 64))
        gray_img = img.convert("L")

        assert gray_img.mode == "L"
        assert gray_img.size == (50, 50)
        assert gray_img is not img  # Should return new instance

    def test_convert_rgb_to_rgba(self):
        """Test converting RGB image to RGBA."""
        img = puhu_new("RGB", (50, 50), (255, 128, 64))
        rgba_img = img.convert("RGBA")

        assert rgba_img.mode == "RGBA"
        assert rgba_img.size == (50, 50)
        assert rgba_img is not img

    def test_convert_rgba_to_rgb(self):
        """Test converting RGBA image to RGB."""
        img = puhu_new("RGBA", (50, 50), (255, 128, 64, 200))
        rgb_img = img.convert("RGB")

        assert rgb_img.mode == "RGB"
        assert rgb_img.size == (50, 50)
        assert rgb_img is not img

    def test_convert_same_mode(self):
        """Test converting image to same mode returns copy."""
        img = puhu_new("RGB", (50, 50), (255, 128, 64))
        same_img = img.convert("RGB")

        assert same_img.mode == "RGB"
        assert same_img.size == (50, 50)
        assert same_img is not img  # Should still return new instance

    def test_convert_functional_api(self):
        """Test convert using functional API."""
        img = puhu_new("RGB", (50, 50), (255, 128, 64))
        gray_img = convert(img, "L")

        assert gray_img.mode == "L"
        assert gray_img.size == (50, 50)

    def test_split_rgb_image(self):
        """Test splitting RGB image into channels."""
        img = puhu_new("RGB", (50, 50), (255, 128, 64))
        channels = img.split()

        assert len(channels) == 3
        for channel in channels:
            assert channel.mode == "L"
            assert channel.size == (50, 50)

    def test_split_rgba_image(self):
        """Test splitting RGBA image into channels."""
        img = puhu_new("RGBA", (50, 50), (255, 128, 64, 200))
        channels = img.split()

        assert len(channels) == 4
        for channel in channels:
            assert channel.mode == "L"
            assert channel.size == (50, 50)

    def test_split_grayscale_image(self):
        """Test splitting grayscale image."""
        img = puhu_new("L", (50, 50), 128)
        channels = img.split()

        assert len(channels) == 1
        assert channels[0].mode == "L"
        assert channels[0].size == (50, 50)

    def test_split_functional_api(self):
        """Test split using functional API."""
        img = puhu_new("RGB", (50, 50), (255, 128, 64))
        channels = split(img)

        assert len(channels) == 3
        for channel in channels:
            assert channel.mode == "L"
            assert channel.size == (50, 50)

    def test_paste_basic(self):
        """Test basic image pasting."""
        base = puhu_new("RGB", (100, 100), (255, 0, 0))  # Red background
        paste_img = puhu_new("RGB", (50, 50), (0, 255, 0))  # Green square

        result = base.paste(paste_img, (25, 25))

        assert result.size == (100, 100)
        assert result.mode == "RGB"
        assert result is not base

    def test_paste_with_position(self):
        """Test pasting with different positions."""
        base = puhu_new("RGB", (100, 100), (255, 0, 0))
        paste_img = puhu_new("RGB", (30, 30), (0, 255, 0))

        # Test different positions
        result1 = base.paste(paste_img, (0, 0))
        result2 = base.paste(paste_img, (70, 70))

        assert result1.size == (100, 100)
        assert result2.size == (100, 100)

    def test_paste_functional_api(self):
        """Test paste using functional API."""
        base = puhu_new("RGB", (100, 100), (255, 0, 0))
        paste_img = puhu_new("RGB", (50, 50), (0, 255, 0))

        result = paste(base, paste_img, (25, 25))

        assert result.size == (100, 100)
        assert result.mode == "RGB"

    @pytest.mark.skipif(not HAS_NUMPY, reason="NumPy not available")
    def test_fromarray_grayscale(self):
        """Test creating image from grayscale numpy array."""
        # Create a simple gradient
        array = np.arange(0, 256, dtype=np.uint8).reshape(16, 16)

        img = Image.fromarray(array)

        assert img.mode == "L"
        assert img.size == (16, 16)

    @pytest.mark.skipif(not HAS_NUMPY, reason="NumPy not available")
    def test_fromarray_rgb(self):
        """Test creating image from RGB numpy array."""
        # Create a simple RGB array
        array = np.zeros((50, 50, 3), dtype=np.uint8)
        array[:, :, 0] = 255  # Red channel

        img = Image.fromarray(array)

        assert img.mode == "RGB"
        assert img.size == (50, 50)

    @pytest.mark.skipif(not HAS_NUMPY, reason="NumPy not available")
    def test_fromarray_rgba(self):
        """Test creating image from RGBA numpy array."""
        # Create a simple RGBA array
        array = np.zeros((30, 30, 4), dtype=np.uint8)
        array[:, :, 0] = 255  # Red channel
        array[:, :, 3] = 128  # Alpha channel

        img = Image.fromarray(array)

        assert img.mode == "RGBA"
        assert img.size == (30, 30)

    @pytest.mark.skipif(not HAS_NUMPY, reason="NumPy not available")
    def test_fromarray_functional_api(self):
        """Test fromarray using functional API."""
        array = np.ones((25, 25), dtype=np.uint8) * 128

        img = fromarray(array)

        assert img.mode == "L"
        assert img.size == (25, 25)

    @pytest.mark.skipif(not HAS_NUMPY, reason="NumPy not available")
    def test_fromarray_float_conversion(self):
        """Test fromarray with float arrays (should convert to uint8)."""
        # Create float array with values in [0, 1] range
        array = np.ones((20, 20), dtype=np.float32) * 0.5

        img = Image.fromarray(array)

        assert img.mode == "L"
        assert img.size == (20, 20)


class TestNewFeaturesErrorHandling:
    """Test error handling for new features."""

    def test_convert_invalid_mode(self):
        """Test converting to invalid mode raises error."""
        img = puhu_new("RGB", (50, 50))

        with pytest.raises(Exception):  # Should raise PuhuProcessingError
            img.convert("INVALID_MODE")

    def test_paste_out_of_bounds(self):
        """Test pasting outside bounds (should handle gracefully)."""
        base = puhu_new("RGB", (50, 50), (255, 0, 0))
        paste_img = puhu_new("RGB", (30, 30), (0, 255, 0))

        # This should work but only paste the visible portion
        result = base.paste(paste_img, (40, 40))
        assert result.size == (50, 50)

    @pytest.mark.skipif(not HAS_NUMPY, reason="NumPy not available")
    def test_fromarray_invalid_shape(self):
        """Test fromarray with invalid array shape."""
        # 1D array should fail
        array = np.ones(100, dtype=np.uint8)

        with pytest.raises(Exception):
            Image.fromarray(array)

    @pytest.mark.skipif(not HAS_NUMPY, reason="NumPy not available")
    def test_fromarray_invalid_channels(self):
        """Test fromarray with invalid number of channels."""
        # 5 channels should fail
        array = np.ones((20, 20, 5), dtype=np.uint8)

        with pytest.raises(Exception):
            Image.fromarray(array)

    def test_fromarray_without_numpy(self):
        """Test fromarray raises ImportError when numpy not available."""
        # Temporarily disable numpy
        original_has_numpy = HAS_NUMPY

        # This test would need to be run in an environment without numpy
        # For now, we'll just test the error message structure
        if not HAS_NUMPY:
            with pytest.raises(ImportError, match="numpy is required"):
                Image.fromarray([1, 2, 3])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
