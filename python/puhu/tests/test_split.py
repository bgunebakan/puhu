"""
Tests for Image.split() and Image.getbands() — Pillow-compatible band splitting.
"""

from puhu import Image


class TestSplit:
    def test_returns_tuple(self):
        img = Image.new("RGB", (2, 2), (10, 20, 30))
        result = img.split()
        assert isinstance(result, tuple)

    def test_l_mode_returns_one_band(self):
        img = Image.new("L", (4, 4), 128)
        bands = img.split()
        assert len(bands) == 1

    def test_l_mode_band_mode_is_l(self):
        img = Image.new("L", (4, 4), 128)
        (band,) = img.split()
        assert band.mode == "L"

    def test_l_mode_is_copy(self):
        img = Image.new("L", (4, 4), 128)
        (band,) = img.split()
        assert band is not img
        assert band.to_bytes() == img.to_bytes()

    def test_la_mode_returns_two_bands(self):
        img = Image.new("LA", (4, 4), (100, 200))
        bands = img.split()
        assert len(bands) == 2

    def test_la_mode_band_modes(self):
        img = Image.new("LA", (4, 4), (100, 200))
        for band in img.split():
            assert band.mode == "L"

    def test_la_pixel_accuracy(self):
        img = Image.new("LA", (2, 2), (77, 200))
        luma, alpha = img.split()
        assert list(luma.to_bytes()) == [77, 77, 77, 77]
        assert list(alpha.to_bytes()) == [200, 200, 200, 200]

    def test_rgb_mode_returns_three_bands(self):
        img = Image.new("RGB", (4, 4), (10, 20, 30))
        assert len(img.split()) == 3

    def test_rgb_mode_band_modes(self):
        img = Image.new("RGB", (4, 4), (10, 20, 30))
        for band in img.split():
            assert band.mode == "L"

    def test_rgb_pixel_accuracy(self):
        img = Image.new("RGB", (2, 2), (10, 20, 30))
        r, g, b = img.split()
        assert list(r.to_bytes()) == [10, 10, 10, 10]
        assert list(g.to_bytes()) == [20, 20, 20, 20]
        assert list(b.to_bytes()) == [30, 30, 30, 30]

    def test_rgba_mode_returns_four_bands(self):
        img = Image.new("RGBA", (4, 4), (10, 20, 30, 200))
        assert len(img.split()) == 4

    def test_rgba_mode_band_modes(self):
        img = Image.new("RGBA", (4, 4), (10, 20, 30, 200))
        for band in img.split():
            assert band.mode == "L"

    def test_rgba_pixel_accuracy(self):
        img = Image.new("RGBA", (2, 2), (10, 20, 30, 200))
        r, g, b, a = img.split()
        assert list(r.to_bytes()) == [10, 10, 10, 10]
        assert list(g.to_bytes()) == [20, 20, 20, 20]
        assert list(b.to_bytes()) == [30, 30, 30, 30]
        assert list(a.to_bytes()) == [200, 200, 200, 200]

    def test_bands_have_correct_size(self):
        img = Image.new("RGB", (8, 6), (10, 20, 30))
        r, g, b = img.split()
        assert r.size == (8, 6)
        assert g.size == (8, 6)
        assert b.size == (8, 6)

    def test_bands_are_independent(self):
        """Modifying original after split does not affect returned bands."""
        img = Image.new("RGB", (2, 2), (10, 20, 30))
        r_before, _, _ = img.split()
        original_bytes = r_before.to_bytes()

        img.paste((255, 0, 0), (0, 0, 2, 2))
        assert r_before.to_bytes() == original_bytes

    def test_split_then_split_single_band(self):
        """Splitting an already-single-band image again returns a 1-tuple."""
        img = Image.new("RGB", (2, 2), (10, 20, 30))
        (r,) = img.split()[0].split()
        assert r.mode == "L"
        assert len(r.to_bytes()) == 4


class TestGetbands:
    def test_l_mode(self):
        img = Image.new("L", (2, 2), 0)
        assert img.getbands() == ("L",)

    def test_la_mode(self):
        img = Image.new("LA", (2, 2), (0, 255))
        assert img.getbands() == ("L", "A")

    def test_rgb_mode(self):
        img = Image.new("RGB", (2, 2), (0, 0, 0))
        assert img.getbands() == ("R", "G", "B")

    def test_rgba_mode(self):
        img = Image.new("RGBA", (2, 2), (0, 0, 0, 255))
        assert img.getbands() == ("R", "G", "B", "A")

    def test_returns_tuple(self):
        img = Image.new("RGB", (2, 2), (0, 0, 0))
        assert isinstance(img.getbands(), tuple)
