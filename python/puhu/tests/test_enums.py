"""
Comprehensive tests for the enum functionality
"""

import pytest

from puhu import ImageFormat, ImageMode, Resampling, Transpose


class TestEnums:
    """Test enum functionality."""

    def test_resampling_enum(self):
        """Test Resampling enum values."""
        assert hasattr(Resampling, "NEAREST")
        assert hasattr(Resampling, "BILINEAR")
        assert hasattr(Resampling, "BICUBIC")
        assert hasattr(Resampling, "LANCZOS")

    def test_transpose_enum(self):
        """Test Transpose enum values."""
        assert hasattr(Transpose, "FLIP_LEFT_RIGHT")
        assert hasattr(Transpose, "FLIP_TOP_BOTTOM")
        assert hasattr(Transpose, "ROTATE_90")
        assert hasattr(Transpose, "ROTATE_180")
        assert hasattr(Transpose, "ROTATE_270")

    def test_image_mode_enum(self):
        """Test ImageMode enum values."""
        assert hasattr(ImageMode, "RGB")
        assert hasattr(ImageMode, "RGBA")
        assert hasattr(ImageMode, "L")

    def test_image_format_enum(self):
        """Test ImageFormat enum values."""
        assert hasattr(ImageFormat, "PNG")
        assert hasattr(ImageFormat, "JPEG")
        assert hasattr(ImageFormat, "BMP")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
