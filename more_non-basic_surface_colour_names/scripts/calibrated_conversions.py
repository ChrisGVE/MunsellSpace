#!/usr/bin/env python3
"""
Calibrated Color Conversions Module

Profile-independent RGB-Munsell conversions with optional screen-surface
calibration correction based on Track B Phase 3 analysis.

Part of Task #119: Profile-independent RGB-Munsell transformation
"""

import json
import numpy as np
from pathlib import Path
from typing import Union, Tuple, Optional, Dict, Literal
from dataclasses import dataclass
import warnings

from rgb_profiles import RGBProfile, get_profile, SRGB, WHITE_POINTS_XYZ

# Try to import munsellspace for accurate conversions
try:
    import munsellspace
    HAS_MUNSELLSPACE = True
except ImportError:
    HAS_MUNSELLSPACE = False
    warnings.warn("munsellspace not installed. Using approximations.")

# Try to import colour-science for reference
try:
    import colour
    HAS_COLOUR = True
except ImportError:
    HAS_COLOUR = False


# =============================================================================
# Calibration Data
# =============================================================================

@dataclass
class CalibrationBias:
    """Screen-surface calibration bias values."""
    value_bias: float      # Munsell value units (+ = screen lighter)
    chroma_bias: float     # Munsell chroma units (+ = screen more saturated)
    hue_bias_mean: float   # Degrees (mean rotation)
    hue_bias_std: float    # Degrees (standard deviation)
    per_family: Dict[str, Dict[str, float]]  # Per-family biases

# Default calibration from Track B Phase 3 analysis
# Using non-XKCD sources (Meodai, ColorHexa, Wikipedia)
DEFAULT_CALIBRATION = CalibrationBias(
    value_bias=2.06,      # Screen appears 2.06 units lighter
    chroma_bias=0.80,     # Screen appears 0.80 units more saturated
    hue_bias_mean=-31.8,  # Mean hue rotation (degrees)
    hue_bias_std=21.0,    # Non-uniform, category-dependent
    per_family={}         # Loaded from JSON if available
)


def load_calibration_data(data_path: Optional[Path] = None) -> CalibrationBias:
    """
    Load calibration data from Track B Phase 3 results.

    Args:
        data_path: Path to calibration JSON file. If None, uses default location.

    Returns:
        CalibrationBias with loaded or default values
    """
    if data_path is None:
        # Default location
        data_path = Path(__file__).parent.parent / 'writeups' / 'results' / 'data' / 'track_b_phase3_calibration.json'

    if not data_path.exists():
        return DEFAULT_CALIBRATION

    try:
        with open(data_path) as f:
            data = json.load(f)

        agg = data.get('aggregate_bias', {})

        # Build per-family dictionary
        per_family = {}
        for fam in data.get('per_family', []):
            if fam.get('value_bias') is not None:
                per_family[fam['family'].lower()] = {
                    'value_bias': fam.get('value_bias', 0),
                    'chroma_bias': fam.get('chroma_bias', 0),
                    'hue_bias': fam.get('hue_bias', 0),
                }

        return CalibrationBias(
            value_bias=agg.get('value', {}).get('mean', DEFAULT_CALIBRATION.value_bias),
            chroma_bias=agg.get('chroma', {}).get('mean', DEFAULT_CALIBRATION.chroma_bias),
            hue_bias_mean=agg.get('hue', {}).get('mean', DEFAULT_CALIBRATION.hue_bias_mean),
            hue_bias_std=agg.get('hue', {}).get('std', DEFAULT_CALIBRATION.hue_bias_std),
            per_family=per_family
        )

    except Exception as e:
        warnings.warn(f"Failed to load calibration data: {e}")
        return DEFAULT_CALIBRATION


# Global calibration (lazy loaded)
_calibration: Optional[CalibrationBias] = None


def get_calibration() -> CalibrationBias:
    """Get calibration data, loading from file if not already loaded."""
    global _calibration
    if _calibration is None:
        _calibration = load_calibration_data()
    return _calibration


# =============================================================================
# Chromatic Adaptation
# =============================================================================

# Bradford chromatic adaptation matrix
BRADFORD_MATRIX = np.array([
    [ 0.8951,  0.2664, -0.1614],
    [-0.7502,  1.7135,  0.0367],
    [ 0.0389, -0.0685,  1.0296]
])
BRADFORD_INV = np.linalg.inv(BRADFORD_MATRIX)


def chromatic_adapt(
    xyz: np.ndarray,
    src_illuminant: str,
    dst_illuminant: str
) -> np.ndarray:
    """
    Apply Bradford chromatic adaptation from source to destination illuminant.

    Args:
        xyz: XYZ tristimulus values, shape (..., 3)
        src_illuminant: Source illuminant ('D65', 'D50', 'C')
        dst_illuminant: Destination illuminant

    Returns:
        Adapted XYZ values
    """
    if src_illuminant == dst_illuminant:
        return xyz.copy()

    xyz = np.asarray(xyz, dtype=float)
    original_shape = xyz.shape
    xyz = xyz.reshape(-1, 3)

    src_wp = WHITE_POINTS_XYZ[src_illuminant]
    dst_wp = WHITE_POINTS_XYZ[dst_illuminant]

    # Convert white points to cone response space
    rho_src = BRADFORD_MATRIX @ src_wp
    rho_dst = BRADFORD_MATRIX @ dst_wp

    # Diagonal scaling
    scale = np.where(np.abs(rho_src) > 1e-10, rho_dst / rho_src, 1.0)
    D = np.diag(scale)

    # Full transformation
    M = BRADFORD_INV @ D @ BRADFORD_MATRIX

    xyz_adapted = xyz @ M.T
    return xyz_adapted.reshape(original_shape)


# =============================================================================
# Munsell Conversion Utilities
# =============================================================================

@dataclass
class MunsellColor:
    """Munsell color specification."""
    hue_number: float   # 0-10 within hue letter
    hue_letter: str     # R, YR, Y, GY, G, BG, B, PB, P, RP, or N (neutral)
    value: float        # 0-10 (0=black, 10=white)
    chroma: float       # 0+ (0=neutral)

    def __str__(self):
        if self.hue_letter == 'N' or self.chroma < 0.5:
            # colour-science expects "N5/" without space for proper parsing
            return f"N{self.value:.1f}"
        return f"{self.hue_number:.1f}{self.hue_letter} {self.value:.1f}/{self.chroma:.1f}"

    def to_display_string(self) -> str:
        """Return human-readable Munsell notation with spaces."""
        if self.hue_letter == 'N' or self.chroma < 0.5:
            return f"N {self.value:.1f}/"
        return f"{self.hue_number:.1f}{self.hue_letter} {self.value:.1f}/{self.chroma:.1f}"

    def to_cartesian(self) -> Tuple[float, float, float]:
        """Convert to Cartesian coordinates (x, y, z) where z=Value."""
        if self.hue_letter == 'N' or self.chroma < 0.01:
            return (0.0, 0.0, self.value)

        # Munsell hue to angle
        hue_order = ['R', 'YR', 'Y', 'GY', 'G', 'BG', 'B', 'PB', 'P', 'RP']
        try:
            hue_idx = hue_order.index(self.hue_letter)
        except ValueError:
            hue_idx = 0

        # Continuous hue 0-100, then to radians
        continuous_hue = hue_idx * 10 + self.hue_number
        angle_rad = continuous_hue * np.pi / 50.0

        x = self.chroma * np.cos(angle_rad)
        y = self.chroma * np.sin(angle_rad)
        z = self.value

        return (x, y, z)

    @classmethod
    def from_cartesian(cls, x: float, y: float, z: float) -> 'MunsellColor':
        """Create MunsellColor from Cartesian coordinates."""
        chroma = np.sqrt(x**2 + y**2)
        value = z

        if chroma < 0.5:
            return cls(hue_number=0, hue_letter='N', value=value, chroma=0)

        # Angle to hue
        angle_rad = np.arctan2(y, x)
        if angle_rad < 0:
            angle_rad += 2 * np.pi

        continuous_hue = angle_rad * 50.0 / np.pi  # 0-100

        hue_order = ['R', 'YR', 'Y', 'GY', 'G', 'BG', 'B', 'PB', 'P', 'RP']
        hue_idx = int(continuous_hue // 10) % 10
        hue_number = continuous_hue % 10

        if hue_number < 0.01:
            hue_number = 10.0
            hue_idx = (hue_idx - 1) % 10

        return cls(
            hue_number=hue_number,
            hue_letter=hue_order[hue_idx],
            value=value,
            chroma=chroma
        )


# =============================================================================
# Profile-Independent Conversions
# =============================================================================

def rgb_to_munsell(
    rgb: Union[Tuple[int, int, int], np.ndarray],
    profile: Union[str, RGBProfile] = 'sRGB',
    apply_calibration: bool = False
) -> MunsellColor:
    """
    Convert RGB to Munsell color specification.

    Args:
        rgb: RGB values as (R, G, B) tuple (0-255) or normalized array (0-1)
        profile: RGB color profile (name or RGBProfile instance)
        apply_calibration: If True, apply screen-surface calibration correction

    Returns:
        MunsellColor specification

    Example:
        >>> color = rgb_to_munsell((206, 123, 89), profile='sRGB')
        >>> print(color)
        5.2YR 5.6/5.8
    """
    profile = get_profile(profile)

    # Normalize RGB
    rgb = np.asarray(rgb, dtype=float)
    if rgb.max() > 1.0:
        rgb = rgb / 255.0

    # RGB → XYZ (profile-specific)
    xyz = profile.rgb_to_xyz(rgb, linearize=True)

    # Chromatic adapt to Illuminant C (Munsell reference)
    if profile.white_point != 'C' and not (
        isinstance(profile.white_point, tuple) and
        np.allclose(profile.white_point, WHITE_POINTS_XYZ['C'][:2] / WHITE_POINTS_XYZ['C'][1])
    ):
        wp_name = profile.white_point if isinstance(profile.white_point, str) else 'D65'
        xyz = chromatic_adapt(xyz, wp_name, 'C')

    # XYZ → Munsell
    munsell = _xyz_to_munsell(xyz)

    # Apply calibration if requested
    if apply_calibration:
        munsell = _apply_calibration_correction(munsell)

    return munsell


def munsell_to_rgb(
    munsell: Union[MunsellColor, str, Tuple[float, str, float, float]],
    profile: Union[str, RGBProfile] = 'sRGB',
    clip: bool = True
) -> Tuple[int, int, int]:
    """
    Convert Munsell color to RGB.

    Args:
        munsell: MunsellColor, string notation (e.g., "5R 5/10"), or tuple (hue_num, hue_letter, value, chroma)
        profile: RGB color profile
        clip: If True, clip out-of-gamut colors to [0, 255]

    Returns:
        RGB tuple (0-255)

    Example:
        >>> rgb = munsell_to_rgb(MunsellColor(5, 'R', 5, 10), profile='sRGB')
        >>> print(rgb)
        (194, 89, 76)
    """
    profile = get_profile(profile)

    # Parse munsell input
    if isinstance(munsell, str):
        munsell = _parse_munsell_string(munsell)
    elif isinstance(munsell, tuple):
        munsell = MunsellColor(munsell[0], munsell[1], munsell[2], munsell[3])

    # Munsell → XYZ (under Illuminant C)
    xyz = _munsell_to_xyz(munsell)

    # Chromatic adapt from C to profile white point
    wp_name = profile.white_point if isinstance(profile.white_point, str) else 'D65'
    if wp_name != 'C':
        xyz = chromatic_adapt(xyz, 'C', wp_name)

    # XYZ → RGB (profile-specific)
    rgb = profile.xyz_to_rgb(xyz, encode=True, clip=clip)

    # Convert to 0-255 range
    rgb_int = tuple(int(np.round(c * 255)) for c in rgb)
    if clip:
        rgb_int = tuple(np.clip(rgb_int, 0, 255))

    return rgb_int


def _xyz_to_munsell(xyz: np.ndarray) -> MunsellColor:
    """Convert XYZ (under Illuminant C) to Munsell."""
    xyz = np.asarray(xyz, dtype=float)

    # colour-science uses Y in [0, 1] range with Y=1 being perfect white
    # Our XYZ can be in either convention, normalize appropriately
    if xyz[1] > 1.5:
        xyz = xyz / 100.0

    if HAS_COLOUR:
        try:
            # XYZ to xyY
            sum_xyz = np.sum(xyz)
            if sum_xyz < 1e-10:
                return MunsellColor(0, 'N', 0, 0)

            x = xyz[0] / sum_xyz
            y = xyz[1] / sum_xyz
            Y = xyz[1]  # Keep Y in [0, 1] range

            xyY = np.array([x, y, Y])

            # colour-science returns a string like "5.0YR 6.0/8.0" or "N5.0"
            munsell_str = colour.xyY_to_munsell_colour(xyY)
            return _parse_munsell_string(munsell_str)
        except Exception as e:
            # Fall back to approximation if conversion fails
            pass

    if HAS_MUNSELLSPACE:
        try:
            # MunsellSpace expects sRGB input
            from color_transforms import xyz_to_rgb
            rgb = xyz_to_rgb(xyz * 100, gamma=2.2, clip=True)
            rgb_255 = tuple(int(c * 255) for c in rgb)

            munsell_str = munsellspace.rgb_to_munsell(*rgb_255)
            if munsell_str:
                return _parse_munsell_string(munsell_str)
        except Exception:
            pass

    # Fallback: approximate conversion
    return _xyz_to_munsell_approx(xyz * 100 if xyz[1] <= 1.5 else xyz)


def _munsell_to_xyz(munsell: MunsellColor) -> np.ndarray:
    """Convert Munsell to XYZ (under Illuminant C)."""
    if HAS_COLOUR:
        try:
            # colour-science expects a string like "5YR 6/8" or "N5"
            munsell_str = str(munsell)

            # colour.munsell_colour_to_xyY returns xyY with Y in [0, 1]
            xyY = colour.munsell_colour_to_xyY(munsell_str)

            x, y, Y = xyY
            if y < 1e-10:
                return np.array([0.0, 0.0, 0.0])

            X = x * Y / y
            Z = (1 - x - y) * Y / y

            # Return XYZ in [0, 1] range (matching Y)
            return np.array([X, Y, Z])
        except Exception:
            pass

    # Fallback: approximate conversion
    return _munsell_to_xyz_approx(munsell)


def _xyz_to_munsell_approx(xyz: np.ndarray) -> MunsellColor:
    """Approximate XYZ to Munsell conversion."""
    # Simple approximation via CIELAB
    from color_transforms import xyz_to_lab, ILLUMINANTS

    # Adapt to D65 for LAB conversion
    xyz_d65 = chromatic_adapt(xyz, 'C', 'D65')
    lab = xyz_to_lab(xyz_d65, illuminant='D65')

    L, a, b = lab[0], lab[1], lab[2]

    # L* to Munsell Value (approximate)
    value = L / 10.0

    # a*, b* to chroma and hue
    chroma = np.sqrt(a**2 + b**2) / 5.0  # Rough scaling
    hue_rad = np.arctan2(b, a)
    hue_deg = np.degrees(hue_rad) % 360

    # Map LAB hue to Munsell hue (approximate)
    # LAB: Red≈25°, Yellow≈85°, Green≈160°, Blue≈270°
    # Munsell: R=0, Y=20, G=40, B=60, P=80
    hue_order = ['R', 'YR', 'Y', 'GY', 'G', 'BG', 'B', 'PB', 'P', 'RP']

    # Very rough mapping
    munsell_hue = ((hue_deg - 25) / 360) * 100  # Offset for red
    if munsell_hue < 0:
        munsell_hue += 100

    hue_idx = int(munsell_hue // 10) % 10
    hue_number = munsell_hue % 10
    if hue_number < 0.1:
        hue_number = 10.0
        hue_idx = (hue_idx - 1) % 10

    if chroma < 0.5:
        return MunsellColor(0, 'N', value, 0)

    return MunsellColor(hue_number, hue_order[hue_idx], value, chroma)


def _munsell_to_xyz_approx(munsell: MunsellColor) -> np.ndarray:
    """Approximate Munsell to XYZ conversion."""
    x, y, z = munsell.to_cartesian()

    # Value to Y (Munsell Value function)
    # Approximate: Y = V * 10 for V < 1, complex otherwise
    Y = (munsell.value / 10.0) ** 2.5 * 100  # Rough approximation

    # Chroma and hue to xy chromaticity (very approximate)
    # Use neutral white as base
    x_chrom = 0.31 + 0.02 * x / max(munsell.chroma, 1)
    y_chrom = 0.32 + 0.02 * y / max(munsell.chroma, 1)

    if y_chrom < 1e-10:
        return np.array([0.0, 0.0, 0.0])

    X = x_chrom * Y / y_chrom
    Z = (1 - x_chrom - y_chrom) * Y / y_chrom

    return np.array([X, Y, Z])


def _parse_munsell_string(s: str) -> MunsellColor:
    """Parse Munsell notation string (e.g., '5R 5/10' or 'N 5/' or 'N5.0')."""
    s = s.strip()

    # Handle neutral
    if s.startswith('N'):
        # Try "N 5/" format (with space)
        parts = s.split()
        if len(parts) >= 2:
            value_part = parts[1].rstrip('/')
            return MunsellColor(0, 'N', float(value_part), 0)

        # Try "N5.0" or "N10" format (no space) - extract number after N
        value_str = s[1:].rstrip('/')
        if value_str:
            try:
                value = float(value_str)
                return MunsellColor(0, 'N', value, 0)
            except ValueError:
                pass

        return MunsellColor(0, 'N', 5, 0)  # Default fallback

    # Parse "5.2YR 5.6/5.8" format
    hue_letters = ['R', 'YR', 'Y', 'GY', 'G', 'BG', 'B', 'PB', 'P', 'RP']

    for hl in sorted(hue_letters, key=len, reverse=True):
        if hl in s:
            idx = s.index(hl)
            hue_num = float(s[:idx])
            rest = s[idx + len(hl):].strip()

            # Parse value/chroma
            if '/' in rest:
                v_str, c_str = rest.split('/')
                value = float(v_str)
                chroma = float(c_str) if c_str else 0
            else:
                value = float(rest) if rest else 5
                chroma = 0

            return MunsellColor(hue_num, hl, value, chroma)

    raise ValueError(f"Cannot parse Munsell string: {s}")


def _apply_calibration_correction(munsell: MunsellColor) -> MunsellColor:
    """
    Apply screen-surface calibration correction.

    Corrects for the systematic bias between screen colors and surface colors:
    - Screen colors appear lighter (positive value bias)
    - Screen colors appear more saturated (positive chroma bias)
    - Screen colors have hue shift (category-dependent)

    To convert screen appearance to surface color prediction:
    - Subtract value bias
    - Subtract chroma bias
    - Add hue rotation (negative of measured bias)
    """
    cal = get_calibration()

    x, y, z = munsell.to_cartesian()

    # Correct value (subtract bias: screen is lighter)
    new_value = z - cal.value_bias
    new_value = np.clip(new_value, 0, 10)

    # Correct chroma (subtract bias: screen is more saturated)
    chroma = np.sqrt(x**2 + y**2)
    new_chroma = max(0, chroma - cal.chroma_bias)

    # Correct hue (add negative of mean bias)
    if chroma > 0.5:
        angle = np.arctan2(y, x)
        # Invert the bias direction for correction
        angle_corrected = angle - np.radians(cal.hue_bias_mean)
        new_x = new_chroma * np.cos(angle_corrected)
        new_y = new_chroma * np.sin(angle_corrected)
    else:
        new_x, new_y = 0, 0

    return MunsellColor.from_cartesian(new_x, new_y, new_value)


# =============================================================================
# Gamut Utilities
# =============================================================================

def is_munsell_in_gamut(
    munsell: MunsellColor,
    profile: Union[str, RGBProfile] = 'sRGB'
) -> bool:
    """
    Check if a Munsell color is representable in a given RGB profile.

    Args:
        munsell: Munsell color to check
        profile: RGB color profile

    Returns:
        True if the color is in gamut
    """
    profile = get_profile(profile)

    # Munsell → XYZ
    xyz = _munsell_to_xyz(munsell)

    # Adapt to profile white point
    wp_name = profile.white_point if isinstance(profile.white_point, str) else 'D65'
    if wp_name != 'C':
        xyz = chromatic_adapt(xyz, 'C', wp_name)

    # Check gamut
    return bool(profile.is_in_gamut(xyz.reshape(1, 3))[0])


def get_gamut_boundary_at_value(
    value: float,
    profile: Union[str, RGBProfile] = 'sRGB',
    n_samples: int = 72
) -> np.ndarray:
    """
    Get the RGB gamut boundary in Munsell coordinates at a specific value level.

    Args:
        value: Munsell value (0-10)
        profile: RGB color profile
        n_samples: Number of samples around the hue circle

    Returns:
        Array of (x, y) coordinates representing the gamut boundary
    """
    profile = get_profile(profile)
    boundary_points = []

    # Sample RGB cube edges and find max chroma at each hue
    for angle_deg in np.linspace(0, 360, n_samples, endpoint=False):
        angle_rad = np.radians(angle_deg)

        # Binary search for max chroma at this hue and value
        chroma_min, chroma_max = 0, 20
        last_valid_chroma = 0

        for _ in range(20):  # Binary search iterations
            chroma_mid = (chroma_min + chroma_max) / 2
            x = chroma_mid * np.cos(angle_rad)
            y = chroma_mid * np.sin(angle_rad)

            test_color = MunsellColor.from_cartesian(x, y, value)
            if is_munsell_in_gamut(test_color, profile):
                last_valid_chroma = chroma_mid
                chroma_min = chroma_mid
            else:
                chroma_max = chroma_mid

        if last_valid_chroma > 0:
            boundary_points.append([
                last_valid_chroma * np.cos(angle_rad),
                last_valid_chroma * np.sin(angle_rad)
            ])

    return np.array(boundary_points) if boundary_points else np.array([])


# =============================================================================
# Convenience Functions
# =============================================================================

def hex_to_munsell(
    hex_color: str,
    profile: Union[str, RGBProfile] = 'sRGB',
    apply_calibration: bool = False
) -> MunsellColor:
    """
    Convert hex color to Munsell.

    Args:
        hex_color: Hex color string (e.g., '#CE7B59' or 'CE7B59')
        profile: RGB color profile
        apply_calibration: Apply screen-surface correction

    Returns:
        MunsellColor specification
    """
    hex_color = hex_color.strip().lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join(c * 2 for c in hex_color)

    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    return rgb_to_munsell((r, g, b), profile, apply_calibration)


def munsell_to_hex(
    munsell: Union[MunsellColor, str],
    profile: Union[str, RGBProfile] = 'sRGB'
) -> str:
    """
    Convert Munsell to hex color.

    Args:
        munsell: Munsell color specification
        profile: RGB color profile

    Returns:
        Hex color string (e.g., '#CE7B59')
    """
    rgb = munsell_to_rgb(munsell, profile)
    return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'


# =============================================================================
# Tests
# =============================================================================

def _test_conversions():
    """Test profile-independent conversions."""
    print("Calibrated Conversions Tests")
    print("=" * 60)

    # Test 1: RGB to Munsell with different profiles
    print("\n1. Same RGB → Munsell with different profiles:")
    test_rgb = (200, 100, 80)

    for profile_name in ['sRGB', 'Display P3', 'Adobe RGB']:
        try:
            munsell = rgb_to_munsell(test_rgb, profile=profile_name)
            print(f"  {profile_name:15}: {munsell}")
        except Exception as e:
            print(f"  {profile_name:15}: Error - {e}")

    # Test 2: Calibration correction
    print("\n2. Calibration correction:")
    munsell_raw = rgb_to_munsell(test_rgb, apply_calibration=False)
    munsell_cal = rgb_to_munsell(test_rgb, apply_calibration=True)
    print(f"  Raw:        {munsell_raw}")
    print(f"  Calibrated: {munsell_cal}")

    cal = get_calibration()
    print(f"\n  Calibration biases:")
    print(f"    Value:  {cal.value_bias:+.2f}")
    print(f"    Chroma: {cal.chroma_bias:+.2f}")
    print(f"    Hue:    {cal.hue_bias_mean:+.1f}° ± {cal.hue_bias_std:.1f}°")

    # Test 3: Gamut check
    print("\n3. Gamut check (high chroma colors):")
    test_colors = [
        MunsellColor(5, 'R', 5, 10),   # Moderate chroma
        MunsellColor(5, 'R', 5, 16),   # High chroma
        MunsellColor(5, 'GY', 8, 14),  # Yellow-green, high chroma
    ]

    for color in test_colors:
        in_srgb = is_munsell_in_gamut(color, 'sRGB')
        in_p3 = is_munsell_in_gamut(color, 'Display P3')
        print(f"  {color}: sRGB={in_srgb}, P3={in_p3}")

    # Test 4: Round-trip
    print("\n4. Round-trip Munsell → RGB → Munsell:")
    original = MunsellColor(5, 'YR', 6, 8)
    rgb = munsell_to_rgb(original, 'sRGB')
    recovered = rgb_to_munsell(rgb, 'sRGB')
    print(f"  Original:  {original}")
    print(f"  RGB:       {rgb}")
    print(f"  Recovered: {recovered}")

    print("\n" + "=" * 60)
    print("Tests complete!")


if __name__ == '__main__':
    _test_conversions()
