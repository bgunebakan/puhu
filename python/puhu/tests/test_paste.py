import pytest

from puhu import Image


class TestPaste:
    """Test cases for the paste method."""

    def test_paste_basic_box(self):
        """Test basic paste with 2-tuple box."""
        bg = Image.new("RGB", (10, 10), (255, 255, 255))
        fg = Image.new("RGB", (5, 5), (255, 0, 0))
        bg.paste(fg, (0, 0))

        # Check top-left pixel (should be red)
        data = bg.to_bytes()
        assert data[0] == 255
        assert data[1] == 0
        assert data[2] == 0

        # Check a pixel outside the pasted region (should be white)
        # Position (6, 6) -> index (6 * 10 + 6) * 3 = 198
        offset = (6 * 10 + 6) * 3
        assert data[offset] == 255
        assert data[offset + 1] == 255
        assert data[offset + 2] == 255

    def test_paste_4tuple_box(self):
        """Test paste with 4-tuple box."""
        bg = Image.new("RGB", (10, 10), (255, 255, 255))
        fg = Image.new("RGB", (5, 5), (0, 255, 0))  # Green
        # Paste into (2, 2, 7, 7) - 5x5 area
        bg.paste(fg, (2, 2, 7, 7))

        data = bg.to_bytes()

        # Check inside region (2, 2) -> (2 * 10 + 2) * 3 = 66
        offset = (2 * 10 + 2) * 3
        assert data[offset] == 0
        assert data[offset + 1] == 255
        assert data[offset + 2] == 0

    def test_paste_color_tuple(self):
        """Test paste with color tuple."""
        bg = Image.new("RGB", (10, 10), "white")
        # Fill top half with blue
        bg.paste((0, 0, 255), (0, 0, 10, 5))

        data = bg.to_bytes()

        # (0, 0) should be blue
        assert data[0] == 0
        assert data[1] == 0
        assert data[2] == 255

        # (0, 6) should be white (row 6 start: 6 * 10 * 3 = 180)
        offset = 60 * 3
        assert data[offset] == 255
        assert data[offset + 1] == 255
        assert data[offset + 2] == 255

    def test_paste_single_int(self):
        """Test paste with single integer (grayscale fill)."""
        bg = Image.new("RGB", (10, 10), "black")
        bg.paste(255, (0, 0, 5, 5))  # White square

        data = bg.to_bytes()
        assert data[0] == 255
        assert data[1] == 255
        assert data[2] == 255

        # Outside should be black
        offset_out = (0 * 10 + 6) * 3
        assert data[offset_out] == 0

    def test_paste_color_string(self):
        """Test paste with color strings (hex and name)."""
        bg = Image.new("RGB", (10, 10), "white")

        bg.paste("red", (0, 0, 5, 5))
        data = bg.to_bytes()
        assert data[0] == 255
        assert data[1] == 0
        assert data[2] == 0

        bg.paste("#00FF00", (5, 0, 10, 5))
        data = bg.to_bytes()
        # Position (5, 0) -> 5 * 3 = 15
        assert data[15] == 0
        assert data[16] == 255
        assert data[17] == 0

    def test_paste_mask(self):
        """Test paste with mask."""
        bg = Image.new("RGB", (10, 10), (0, 0, 0))  # Black
        fg = Image.new("RGB", (10, 10), (255, 255, 255))  # White
        # Mask: Left half black (0), Right half white (255)
        mask = Image.new("L", (10, 10), 0)
        mask.paste(255, (5, 0, 10, 10))

        bg.paste(fg, (0, 0), mask)

        data = bg.to_bytes()

        # Left pixel (0,0) should remain black (masked out)
        assert data[0] == 0

        # Right pixel (9,0) should be white (fully pasted)
        # (0 * 10 + 9) * 3 = 27
        assert data[27] == 255
        assert data[28] == 255
        assert data[29] == 255

    def test_abbreviated_syntax(self):
        """Test paste(im, mask) syntax."""
        bg = Image.new("RGB", (10, 10), "black")
        fg = Image.new("RGB", (10, 10), "white")
        mask = Image.new("L", (10, 10), 255)  # Full opacity

        bg.paste(fg, mask)  # Should act as paste(fg, (0,0), mask)

        data = bg.to_bytes()
        assert data[0] == 255  # Should be white

    def test_paste_mode_conversion(self):
        """Test automatic mode conversion during paste."""
        bg = Image.new("RGB", (10, 10), "white")
        fg = Image.new("L", (5, 5), 0)  # Black grayscale

        bg.paste(fg, (0, 0))

        data = bg.to_bytes()
        # Should be black RGB
        assert data[0] == 0
        assert data[1] == 0
        assert data[2] == 0

    def test_error_handling(self):
        """Test error conditions."""
        bg = Image.new("RGB", (10, 10))

        # Parsing error for invalid color string
        with pytest.raises(Exception):
            bg.paste("not_a_color", (0, 0, 5, 5))

    def test_paste_negative_coords(self):
        """Test paste with negative coordinates (clipping)."""
        bg = Image.new("RGB", (10, 10), (0, 0, 0))  # Black
        fg = Image.new("RGB", (5, 5), (255, 255, 255))  # White

        # Paste at (-2, -2)
        # Expected: top-left 3x3 of bg should be white (from bottom-right of fg)
        bg.paste(fg, (-2, -2))

        data = bg.to_bytes()
        # (0, 0) should be white
        assert data[0] == 255
        assert data[1] == 255
        assert data[2] == 255

        # (3, 3) should be black
        offset = (3 * 10 + 3) * 3
        assert data[offset] == 0

    def test_paste_out_of_bounds(self):
        """Test paste that goes out of bounds (clipping)."""
        bg = Image.new("RGB", (10, 10), (0, 0, 0))  # Black
        fg = Image.new("RGB", (5, 5), (255, 255, 255))  # White

        # Paste at (7, 7) - should clip at (10, 10)
        bg.paste(fg, (7, 7))

        data = bg.to_bytes()
        # (7, 7) should be white
        offset = (7 * 10 + 7) * 3
        assert data[offset] == 255

        # (6, 6) should be black
        offset = (6 * 10 + 6) * 3
        assert data[offset] == 0

    def test_paste_rgba_to_rgb(self):
        """Test pasting RGBA onto RGB without mask follows Pillow semantics."""
        bg = Image.new("RGB", (10, 10), (0, 0, 0))  # Black
        fg = Image.new("RGBA", (5, 5), (255, 255, 255, 128))  # Semi-transparent white

        bg.paste(fg, (0, 0))

        data = bg.to_bytes()
        # Pillow-compatible: alpha channel is not used unless mask is provided
        assert data[0] == 255
        assert data[1] == 255
        assert data[2] == 255

    def test_paste_mask_size_mismatch_raises(self):
        """Mask size must match source image size."""
        bg = Image.new("RGB", (10, 10), "black")
        fg = Image.new("RGB", (5, 5), "white")
        mask = Image.new("L", (4, 5), 255)

        with pytest.raises(Exception) as exc_info:
            bg.paste(fg, (0, 0), mask)

        assert "Mask size" in str(exc_info.value)

    def test_paste_color_without_4tuple_raises(self):
        """Color paste without mask requires a 4-item box for region size."""
        bg = Image.new("RGB", (10, 10), "black")

        with pytest.raises(Exception) as exc_info:
            bg.paste((255, 0, 0), (2, 2))

        assert "Cannot determine region size for color fill" in str(exc_info.value)

    def test_paste_with_fully_transparent_mask_is_noop(self):
        """Fully transparent mask should not alter destination pixels."""
        bg = Image.new("RGB", (10, 10), (10, 20, 30))
        fg = Image.new("RGB", (5, 5), (255, 255, 255))
        mask = Image.new("L", (5, 5), 0)

        before = bg.to_bytes()
        bg.paste(fg, (0, 0), mask)
        after = bg.to_bytes()

        assert before == after

    def test_paste_masked_rgba_to_rgb_matches_pillow(self):
        """Parity check: masked RGBA->RGB paste should match Pillow bytes."""
        pil_image = pytest.importorskip("PIL.Image")

        # Pillow result
        p_bg = pil_image.new("RGB", (10, 10), (10, 20, 30))
        p_fg = pil_image.new("RGBA", (5, 5), (200, 100, 50, 255))
        p_mask = pil_image.new("L", (5, 5), 128)
        p_bg.paste(p_fg, (0, 0), p_mask)

        # Puhu result
        u_bg = Image.new("RGB", (10, 10), (10, 20, 30))
        u_fg = Image.new("RGBA", (5, 5), (200, 100, 50, 255))
        u_mask = Image.new("L", (5, 5), 128)
        u_bg.paste(u_fg, (0, 0), u_mask)

        assert u_bg.to_bytes() == p_bg.tobytes()

    def test_paste_grayscale_color_rules_match_pillow(self):
        """Parity check: L-mode color input rules should match Pillow behavior."""
        pil_image = pytest.importorskip("PIL.Image")

        # int works and should match bytes
        p_bg = pil_image.new("L", (10, 10), 0)
        p_bg.paste(128, (0, 0, 5, 5))
        u_bg = Image.new("L", (10, 10), 0)
        u_bg.paste(128, (0, 0, 5, 5))
        assert u_bg.to_bytes() == p_bg.tobytes()

        # single-element tuple works and should match bytes
        p_bg = pil_image.new("L", (10, 10), 0)
        p_bg.paste((128,), (0, 0, 5, 5))
        u_bg = Image.new("L", (10, 10), 0)
        u_bg.paste((128,), (0, 0, 5, 5))
        assert u_bg.to_bytes() == p_bg.tobytes()

        # RGB tuple should fail in both
        p_bg = pil_image.new("L", (10, 10), 0)
        with pytest.raises(Exception):
            p_bg.paste((255, 0, 0), (0, 0, 5, 5))
        u_bg = Image.new("L", (10, 10), 0)
        with pytest.raises(Exception):
            u_bg.paste((255, 0, 0), (0, 0, 5, 5))
