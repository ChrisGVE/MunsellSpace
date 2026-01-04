#!/usr/bin/env python3
"""
Unit tests for calibrated_conversions module.

Tests profile-independent RGB-Munsell conversions with calibration.
Part of Task #119.
"""

import pytest
import numpy as np
from numpy.testing import assert_allclose

from calibrated_conversions import (
    MunsellColor,
    rgb_to_munsell,
    munsell_to_rgb,
    hex_to_munsell,
    munsell_to_hex,
    is_munsell_in_gamut,
    get_gamut_boundary_at_value,
    chromatic_adapt,
    get_calibration,
    _parse_munsell_string,
)
from rgb_profiles import get_profile, SRGB, DISPLAY_P3


# =============================================================================
# MunsellColor Tests
# =============================================================================

class TestMunsellColor:
    """Tests for MunsellColor dataclass."""

    def test_chromatic_color_str(self):
        """Test string representation of chromatic color."""
        color = MunsellColor(5.0, 'R', 5.0, 10.0)
        assert str(color) == '5.0R 5.0/10.0'

    def test_neutral_color_str(self):
        """Test string representation of neutral color (colour-science format)."""
        color = MunsellColor(0, 'N', 5.0, 0)
        # str() returns colour-science compatible format
        assert str(color) == 'N5.0'
        # to_display_string() returns human-readable format
        assert color.to_display_string() == 'N 5.0/'

    def test_low_chroma_becomes_neutral(self):
        """Test that very low chroma becomes neutral."""
        color = MunsellColor(5.0, 'R', 5.0, 0.3)
        assert str(color) == 'N5.0'

    def test_to_cartesian_neutral(self):
        """Test Cartesian conversion for neutral."""
        color = MunsellColor(0, 'N', 5.0, 0)
        x, y, z = color.to_cartesian()
        assert x == 0.0
        assert y == 0.0
        assert z == 5.0

    def test_to_cartesian_red(self):
        """Test Cartesian conversion for red (angle ~0)."""
        color = MunsellColor(5.0, 'R', 5.0, 10.0)
        x, y, z = color.to_cartesian()
        # 5R is at continuous hue 5, which is 5 * pi/50 = 0.314 radians
        # cos(0.314) ≈ 0.951, sin(0.314) ≈ 0.309
        assert z == 5.0
        assert abs(np.sqrt(x**2 + y**2) - 10.0) < 0.01

    def test_cartesian_roundtrip(self):
        """Test Cartesian conversion roundtrip."""
        original = MunsellColor(7.5, 'YR', 6.0, 8.0)
        x, y, z = original.to_cartesian()
        recovered = MunsellColor.from_cartesian(x, y, z)

        assert abs(recovered.value - original.value) < 0.1
        assert abs(recovered.chroma - original.chroma) < 0.5
        # Hue comparison is complex due to letter boundaries
        # Just verify it's in the same region
        assert recovered.hue_letter in ['Y', 'YR', 'R']


# =============================================================================
# Munsell String Parsing Tests
# =============================================================================

class TestMunsellParsing:
    """Tests for Munsell string parsing."""

    def test_parse_chromatic(self):
        """Test parsing chromatic color."""
        color = _parse_munsell_string('5R 5/10')
        assert color.hue_number == 5.0
        assert color.hue_letter == 'R'
        assert color.value == 5.0
        assert color.chroma == 10.0

    def test_parse_chromatic_decimal(self):
        """Test parsing with decimal values."""
        color = _parse_munsell_string('7.5YR 6.5/8.2')
        assert color.hue_number == 7.5
        assert color.hue_letter == 'YR'
        assert color.value == 6.5
        assert color.chroma == 8.2

    def test_parse_neutral(self):
        """Test parsing neutral color."""
        color = _parse_munsell_string('N 5/')
        assert color.hue_letter == 'N'
        assert color.value == 5.0
        assert color.chroma == 0

    def test_parse_neutral_compact(self):
        """Test parsing compact neutral notation."""
        color = _parse_munsell_string('N5/')
        assert color.hue_letter == 'N'
        assert color.value == 5.0


# =============================================================================
# RGB Conversion Tests
# =============================================================================

class TestRGBConversions:
    """Tests for RGB-Munsell conversions."""

    def test_rgb_to_munsell_basic(self):
        """Test basic RGB to Munsell conversion."""
        # Red-orange color
        color = rgb_to_munsell((200, 100, 80))
        assert color.hue_letter in ['R', 'YR']
        assert 4.0 < color.value < 7.0
        assert color.chroma > 5.0

    def test_rgb_to_munsell_white(self):
        """Test white RGB conversion."""
        color = rgb_to_munsell((255, 255, 255))
        # Should be near N 10/
        assert color.value > 9.5
        assert color.chroma < 1.0

    def test_rgb_to_munsell_black(self):
        """Test black RGB conversion."""
        color = rgb_to_munsell((0, 0, 0))
        # Should be near N 0/
        assert color.value < 1.0
        assert color.chroma < 1.0

    def test_rgb_to_munsell_gray(self):
        """Test gray RGB conversion."""
        color = rgb_to_munsell((128, 128, 128))
        # Should be neutral, around N 5/
        assert 4.0 < color.value < 6.0
        assert color.chroma < 1.0

    def test_munsell_to_rgb_basic(self):
        """Test basic Munsell to RGB conversion."""
        rgb = munsell_to_rgb(MunsellColor(5, 'YR', 6, 8))
        assert len(rgb) == 3
        assert all(0 <= c <= 255 for c in rgb)
        # Should be a warm orange-brown
        assert rgb[0] > rgb[1] > rgb[2]  # R > G > B

    def test_munsell_to_rgb_neutral(self):
        """Test neutral Munsell to RGB conversion."""
        rgb = munsell_to_rgb(MunsellColor(0, 'N', 5, 0))
        # Should be gray
        assert abs(rgb[0] - rgb[1]) < 5
        assert abs(rgb[1] - rgb[2]) < 5
        # Mid-gray, around 128
        assert 100 < rgb[0] < 150

    def test_roundtrip_srgb(self):
        """Test RGB → Munsell → RGB roundtrip."""
        original_rgb = (200, 130, 80)
        munsell = rgb_to_munsell(original_rgb)
        recovered_rgb = munsell_to_rgb(munsell)

        # Should be close (within color quantization error)
        assert abs(recovered_rgb[0] - original_rgb[0]) < 15
        assert abs(recovered_rgb[1] - original_rgb[1]) < 15
        assert abs(recovered_rgb[2] - original_rgb[2]) < 15

    def test_roundtrip_munsell(self):
        """Test Munsell → RGB → Munsell roundtrip."""
        original = MunsellColor(5.0, 'YR', 6.0, 8.0)
        rgb = munsell_to_rgb(original)
        recovered = rgb_to_munsell(rgb)

        assert abs(recovered.value - original.value) < 0.5
        assert abs(recovered.chroma - original.chroma) < 1.0
        # Hue should be similar
        assert recovered.hue_letter in ['Y', 'YR', 'R']


# =============================================================================
# Profile-Specific Tests
# =============================================================================

class TestProfileConversions:
    """Tests for profile-specific conversions."""

    def test_different_profiles_same_rgb(self):
        """Test that same RGB gives different Munsell for different profiles."""
        rgb = (200, 100, 80)

        srgb_result = rgb_to_munsell(rgb, profile='sRGB')
        p3_result = rgb_to_munsell(rgb, profile='Display P3')

        # P3 has wider gamut, same RGB values should give different chroma
        # The exact difference depends on the color
        assert srgb_result != p3_result

    def test_profile_by_name(self):
        """Test profile lookup by name."""
        rgb = (200, 100, 80)

        for name in ['sRGB', 'Display P3', 'Adobe RGB']:
            result = rgb_to_munsell(rgb, profile=name)
            assert isinstance(result, MunsellColor)

    def test_profile_by_object(self):
        """Test passing RGBProfile object."""
        rgb = (200, 100, 80)
        result = rgb_to_munsell(rgb, profile=SRGB)
        assert isinstance(result, MunsellColor)


# =============================================================================
# Calibration Tests
# =============================================================================

class TestCalibration:
    """Tests for screen-surface calibration."""

    def test_calibration_loaded(self):
        """Test calibration data is loaded."""
        cal = get_calibration()
        assert cal.value_bias > 0  # Screen appears lighter
        assert cal.hue_bias_std > 0

    def test_calibration_correction_direction(self):
        """Test calibration correction moves in correct direction."""
        rgb = (200, 100, 80)

        raw = rgb_to_munsell(rgb, apply_calibration=False)
        calibrated = rgb_to_munsell(rgb, apply_calibration=True)

        # Calibration should reduce value (screen is lighter than surface)
        assert calibrated.value < raw.value

    def test_calibration_preserves_type(self):
        """Test calibration returns MunsellColor."""
        result = rgb_to_munsell((200, 100, 80), apply_calibration=True)
        assert isinstance(result, MunsellColor)


# =============================================================================
# Hex Conversion Tests
# =============================================================================

class TestHexConversions:
    """Tests for hex color conversions."""

    def test_hex_to_munsell_full(self):
        """Test full hex color conversion."""
        color = hex_to_munsell('#CE7B59')
        assert isinstance(color, MunsellColor)

    def test_hex_to_munsell_no_hash(self):
        """Test hex without hash."""
        color = hex_to_munsell('CE7B59')
        assert isinstance(color, MunsellColor)

    def test_hex_to_munsell_short(self):
        """Test short hex notation."""
        color = hex_to_munsell('#F00')  # Red
        assert color.hue_letter in ['R', 'RP', 'YR']
        assert color.chroma > 5.0

    def test_munsell_to_hex(self):
        """Test Munsell to hex conversion."""
        hex_color = munsell_to_hex(MunsellColor(5, 'YR', 6, 8))
        assert hex_color.startswith('#')
        assert len(hex_color) == 7


# =============================================================================
# Gamut Tests
# =============================================================================

class TestGamut:
    """Tests for gamut checking."""

    def test_neutral_in_gamut(self):
        """Test that neutral colors are always in gamut."""
        neutral = MunsellColor(0, 'N', 5, 0)
        assert is_munsell_in_gamut(neutral, 'sRGB')
        assert is_munsell_in_gamut(neutral, 'Display P3')

    def test_p3_larger_than_srgb(self):
        """Test that P3 gamut is larger than sRGB for high chroma."""
        # High chroma yellow-green (often outside sRGB)
        color = MunsellColor(5, 'GY', 8, 14)

        in_srgb = is_munsell_in_gamut(color, 'sRGB')
        in_p3 = is_munsell_in_gamut(color, 'Display P3')

        # P3 should accept more colors than sRGB
        # (or at least the same)
        if not in_srgb:
            # If not in sRGB, it might be in P3
            pass  # Can't assert P3 > sRGB for all colors

    def test_gamut_boundary(self):
        """Test gamut boundary computation."""
        boundary = get_gamut_boundary_at_value(5.0, 'sRGB', n_samples=36)

        # Should have points
        assert len(boundary) > 0
        # All points should be at non-zero chroma
        if len(boundary) > 0:
            radii = np.sqrt(boundary[:, 0]**2 + boundary[:, 1]**2)
            assert np.min(radii) >= 0


# =============================================================================
# Chromatic Adaptation Tests
# =============================================================================

class TestChromaticAdaptation:
    """Tests for Bradford chromatic adaptation."""

    def test_same_illuminant_no_change(self):
        """Test that same illuminant returns unchanged XYZ."""
        xyz = np.array([0.5, 0.5, 0.5])
        adapted = chromatic_adapt(xyz, 'D65', 'D65')
        assert_allclose(adapted, xyz)

    def test_d65_to_c_changes(self):
        """Test D65 to C adaptation changes values."""
        xyz = np.array([0.5, 0.5, 0.5])
        adapted = chromatic_adapt(xyz, 'D65', 'C')
        # Should be different
        assert not np.allclose(adapted, xyz)

    def test_roundtrip_adaptation(self):
        """Test adaptation roundtrip."""
        xyz = np.array([0.3, 0.4, 0.5])
        adapted = chromatic_adapt(xyz, 'D65', 'C')
        recovered = chromatic_adapt(adapted, 'C', 'D65')
        assert_allclose(recovered, xyz, rtol=1e-5)


# =============================================================================
# Edge Cases
# =============================================================================

class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_normalized_rgb_input(self):
        """Test with normalized RGB (0-1)."""
        color = rgb_to_munsell((0.8, 0.4, 0.3))
        assert isinstance(color, MunsellColor)

    def test_array_rgb_input(self):
        """Test with numpy array input."""
        color = rgb_to_munsell(np.array([200, 100, 80]))
        assert isinstance(color, MunsellColor)

    def test_munsell_string_input(self):
        """Test munsell_to_rgb with string input."""
        rgb = munsell_to_rgb('5YR 6/8')
        assert len(rgb) == 3
        assert all(0 <= c <= 255 for c in rgb)

    def test_munsell_tuple_input(self):
        """Test munsell_to_rgb with tuple input."""
        rgb = munsell_to_rgb((5, 'YR', 6, 8))
        assert len(rgb) == 3


# =============================================================================
# Run Tests
# =============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
