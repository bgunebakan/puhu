"""
Tests for the Image class and basic functionality
"""

import pytest
import tempfile
import os
from pathlib import Path

try:
    import puhu
    from puhu import Image

    SAFEIMAGE_AVAILABLE = True
except ImportError:
    SAFEIMAGE_AVAILABLE = False


@pytest.mark.skipif(not SAFEIMAGE_AVAILABLE, reason="Puhu not built yet")
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

    @pytest.mark.skipif(True, reason="Requires test image file")
    def test_open_save_roundtrip(self):
        """Test opening and saving an image."""
        # This test would require a sample image file
        # For now, we'll skip it until we have test assets
        pass

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

        # Create thumbnail in-place
        original_id = id(larger._rust_image)
        larger.thumbnail((50, 50))

        # Should maintain aspect ratio: 200:100 = 2:1
        # So for max 50x50, result should be 50x25
        assert larger.size == (50, 25)
        # Should modify in-place (though the rust object might be replaced)
        assert larger.width <= 50
        assert larger.height <= 50


@pytest.mark.skipif(not SAFEIMAGE_AVAILABLE, reason="Puhu not built yet")
class TestFunctionalAPI:
    """Test cases for the functional API."""

    def test_functional_imports(self):
        """Test that functional API can be imported."""
        from puhu import open, save, resize, crop, rotate

        assert callable(open)
        assert callable(save)
        assert callable(resize)
        assert callable(crop)
        assert callable(rotate)

    def test_functional_resize(self):
        """Test functional resize."""
        from puhu import resize

        img = Image()
        resized = resize(img, (20, 20))
        assert resized.size == (20, 20)

    def test_functional_crop(self):
        """Test functional crop."""
        from puhu import crop

        img = Image().resize((100, 100))
        cropped = crop(img, (10, 10, 60, 60))
        assert cropped.size == (50, 50)


if __name__ == "__main__":
    pytest.main([__file__])
