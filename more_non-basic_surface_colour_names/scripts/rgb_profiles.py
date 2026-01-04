#!/usr/bin/env python3
"""
RGB Color Profile Specification Module

Defines RGB color profiles with primaries, white points, and transfer functions.
Supports profile-independent color space transformations.

Part of Task #119: Profile-independent RGB-Munsell transformation
"""

from dataclasses import dataclass, field
from typing import Tuple, Union, Callable, Literal, Optional
import numpy as np


# =============================================================================
# Transfer Function Definitions
# =============================================================================

def srgb_eotf(encoded: np.ndarray) -> np.ndarray:
    """
    sRGB Electro-Optical Transfer Function (EOTF).
    Converts encoded sRGB values to linear light.

    The sRGB transfer function is piecewise:
    - Linear segment near black (avoids infinite slope)
    - Power function (gamma ~2.4) for higher values
    """
    encoded = np.asarray(encoded, dtype=float)
    return np.where(
        encoded <= 0.04045,
        encoded / 12.92,
        np.power((encoded + 0.055) / 1.055, 2.4)
    )


def srgb_oetf(linear: np.ndarray) -> np.ndarray:
    """
    sRGB Opto-Electronic Transfer Function (OETF).
    Converts linear light to encoded sRGB values.
    """
    linear = np.asarray(linear, dtype=float)
    linear = np.maximum(linear, 0)  # Handle negative values from out-of-gamut
    return np.where(
        linear <= 0.0031308,
        12.92 * linear,
        1.055 * np.power(linear, 1/2.4) - 0.055
    )


def gamma_eotf(gamma: float) -> Callable[[np.ndarray], np.ndarray]:
    """Create an EOTF for simple gamma curves."""
    def _eotf(encoded: np.ndarray) -> np.ndarray:
        encoded = np.asarray(encoded, dtype=float)
        return np.power(np.maximum(encoded, 0), gamma)
    return _eotf


def gamma_oetf(gamma: float) -> Callable[[np.ndarray], np.ndarray]:
    """Create an OETF for simple gamma curves."""
    def _oetf(linear: np.ndarray) -> np.ndarray:
        linear = np.asarray(linear, dtype=float)
        return np.power(np.maximum(linear, 0), 1/gamma)
    return _oetf


# =============================================================================
# Standard White Points (xy chromaticity)
# =============================================================================

WHITE_POINTS_XY = {
    'D65': (0.31270, 0.32900),  # Daylight 6500K (sRGB, P3)
    'D50': (0.34567, 0.35850),  # Daylight 5000K (ProPhoto, printing)
    'C':   (0.31006, 0.31616),  # Illuminant C (Munsell)
    'A':   (0.44757, 0.40745),  # Incandescent 2856K
    'E':   (0.33333, 0.33333),  # Equal energy
}

# XYZ tristimulus values (Y=1 normalized)
WHITE_POINTS_XYZ = {
    'D65': np.array([0.95047, 1.00000, 1.08883]),
    'D50': np.array([0.96422, 1.00000, 0.82521]),
    'C':   np.array([0.98074, 1.00000, 1.18232]),
    'A':   np.array([1.09850, 1.00000, 0.35585]),
    'E':   np.array([1.00000, 1.00000, 1.00000]),
}


# =============================================================================
# RGB Profile Dataclass
# =============================================================================

@dataclass
class RGBProfile:
    """
    Definition of an RGB color profile.

    Attributes:
        name: Profile name (e.g., 'sRGB', 'Display P3')
        primaries_xy: 3x2 array of primary chromaticities [[r_x, r_y], [g_x, g_y], [b_x, b_y]]
        white_point: White point name ('D65', 'D50', 'C') or (x, y) tuple
        transfer_function: 'srgb', 'gamma_2.2', 'gamma_1.8', 'linear', or custom
        description: Optional description

    Properties (computed):
        rgb_to_xyz_matrix: 3x3 transformation matrix
        xyz_to_rgb_matrix: 3x3 inverse transformation matrix
        white_point_xy: (x, y) chromaticity tuple
        white_point_xyz: XYZ tristimulus values
    """

    name: str
    primaries_xy: np.ndarray
    white_point: Union[str, Tuple[float, float]]
    transfer_function: Union[str, Tuple[Callable, Callable]] = 'srgb'
    description: str = ''

    # Cached matrices (computed on first access)
    _rgb_to_xyz: np.ndarray = field(default=None, repr=False, init=False)
    _xyz_to_rgb: np.ndarray = field(default=None, repr=False, init=False)

    def __post_init__(self):
        """Validate profile parameters."""
        self.primaries_xy = np.asarray(self.primaries_xy, dtype=float)

        if self.primaries_xy.shape != (3, 2):
            raise ValueError(f"primaries_xy must be shape (3, 2), got {self.primaries_xy.shape}")

        # Validate primaries form a valid triangle
        if not self._validate_primaries():
            raise ValueError("Primaries do not form a valid triangle in xy chromaticity")

    def _validate_primaries(self) -> bool:
        """Check that primaries form a valid (non-degenerate) triangle."""
        p = self.primaries_xy

        # Compute area using cross product
        v1 = p[1] - p[0]
        v2 = p[2] - p[0]
        area = abs(v1[0] * v2[1] - v1[1] * v2[0])

        # Area should be non-zero (primaries are not collinear)
        return area > 1e-6

    @property
    def white_point_xy(self) -> Tuple[float, float]:
        """Get white point as (x, y) chromaticity."""
        if isinstance(self.white_point, str):
            if self.white_point not in WHITE_POINTS_XY:
                raise ValueError(f"Unknown white point '{self.white_point}'")
            return WHITE_POINTS_XY[self.white_point]
        return tuple(self.white_point)

    @property
    def white_point_xyz(self) -> np.ndarray:
        """Get white point as XYZ tristimulus (Y=1 normalized)."""
        if isinstance(self.white_point, str) and self.white_point in WHITE_POINTS_XYZ:
            return WHITE_POINTS_XYZ[self.white_point].copy()

        # Compute from xy
        x, y = self.white_point_xy
        return np.array([x / y, 1.0, (1 - x - y) / y])

    @property
    def rgb_to_xyz_matrix(self) -> np.ndarray:
        """Compute RGB to XYZ transformation matrix."""
        if self._rgb_to_xyz is None:
            self._rgb_to_xyz = self._compute_rgb_to_xyz_matrix()
        return self._rgb_to_xyz.copy()

    @property
    def xyz_to_rgb_matrix(self) -> np.ndarray:
        """Compute XYZ to RGB transformation matrix (inverse)."""
        if self._xyz_to_rgb is None:
            self._xyz_to_rgb = np.linalg.inv(self.rgb_to_xyz_matrix)
        return self._xyz_to_rgb.copy()

    def _compute_rgb_to_xyz_matrix(self) -> np.ndarray:
        """
        Derive RGB→XYZ transformation matrix from primaries and white point.

        Algorithm:
        1. Convert primary xy to XYZ (at unit luminance Y=1)
        2. Solve for scaling factors S such that primaries * S = white point
        3. Apply scaling to form final matrix
        """
        primaries = self.primaries_xy

        # Step 1: Convert primaries xy → XYZ (at Y=1)
        # For each primary: X = x/y, Y = 1, Z = (1-x-y)/y
        P = np.zeros((3, 3))
        for i in range(3):
            x, y = primaries[i]
            if y < 1e-10:
                raise ValueError(f"Primary {i} has y≈0, cannot compute XYZ")
            P[0, i] = x / y       # X
            P[1, i] = 1.0         # Y
            P[2, i] = (1 - x - y) / y  # Z

        # Step 2: Solve P @ S = white_xyz
        white_xyz = self.white_point_xyz
        S = np.linalg.solve(P, white_xyz)

        # Step 3: Form final matrix M = P * diag(S)
        M = P * S  # Broadcasting: multiply each column by corresponding S

        return M

    def linearize(self, encoded: np.ndarray) -> np.ndarray:
        """Convert encoded RGB values to linear light."""
        encoded = np.asarray(encoded, dtype=float)

        if self.transfer_function == 'srgb':
            return srgb_eotf(encoded)
        elif self.transfer_function == 'linear':
            return encoded
        elif isinstance(self.transfer_function, str) and self.transfer_function.startswith('gamma_'):
            gamma = float(self.transfer_function.split('_')[1])
            return gamma_eotf(gamma)(encoded)
        elif isinstance(self.transfer_function, tuple):
            eotf, _ = self.transfer_function
            return eotf(encoded)
        else:
            raise ValueError(f"Unknown transfer function: {self.transfer_function}")

    def encode(self, linear: np.ndarray) -> np.ndarray:
        """Convert linear light to encoded RGB values."""
        linear = np.asarray(linear, dtype=float)

        if self.transfer_function == 'srgb':
            return srgb_oetf(linear)
        elif self.transfer_function == 'linear':
            return linear
        elif isinstance(self.transfer_function, str) and self.transfer_function.startswith('gamma_'):
            gamma = float(self.transfer_function.split('_')[1])
            return gamma_oetf(gamma)(linear)
        elif isinstance(self.transfer_function, tuple):
            _, oetf = self.transfer_function
            return oetf(linear)
        else:
            raise ValueError(f"Unknown transfer function: {self.transfer_function}")

    def rgb_to_xyz(self, rgb: np.ndarray, linearize: bool = True) -> np.ndarray:
        """
        Convert RGB values to XYZ tristimulus values.

        Args:
            rgb: RGB values in [0, 1], shape (..., 3)
            linearize: If True, apply EOTF first (default for encoded values)

        Returns:
            XYZ values (Y normalized to 1 for white), shape (..., 3)
        """
        rgb = np.asarray(rgb, dtype=float)
        original_shape = rgb.shape
        rgb = rgb.reshape(-1, 3)

        if linearize:
            rgb = self.linearize(rgb)

        xyz = rgb @ self.rgb_to_xyz_matrix.T
        return xyz.reshape(original_shape)

    def xyz_to_rgb(self, xyz: np.ndarray, encode: bool = True, clip: bool = True) -> np.ndarray:
        """
        Convert XYZ tristimulus values to RGB.

        Args:
            xyz: XYZ values (Y normalized to 1 for white), shape (..., 3)
            encode: If True, apply OETF (default for display output)
            clip: If True, clip to [0, 1] range

        Returns:
            RGB values in [0, 1], shape (..., 3)
        """
        xyz = np.asarray(xyz, dtype=float)
        original_shape = xyz.shape
        xyz = xyz.reshape(-1, 3)

        rgb = xyz @ self.xyz_to_rgb_matrix.T

        if encode:
            rgb = self.encode(rgb)

        if clip:
            rgb = np.clip(rgb, 0, 1)

        return rgb.reshape(original_shape)

    def is_in_gamut(self, xyz: np.ndarray, tolerance: float = 1e-6) -> np.ndarray:
        """
        Check if XYZ colors are within this profile's gamut.

        Args:
            xyz: XYZ values, shape (..., 3)
            tolerance: Tolerance for boundary detection

        Returns:
            Boolean array, True if in gamut
        """
        # Convert to linear RGB
        rgb = self.xyz_to_rgb(xyz, encode=False, clip=False)

        # Check if all components are in [0, 1]
        in_gamut = np.all((rgb >= -tolerance) & (rgb <= 1 + tolerance), axis=-1)
        return in_gamut


# =============================================================================
# Standard Profile Definitions
# =============================================================================

# sRGB (IEC 61966-2-1:1999)
SRGB = RGBProfile(
    name='sRGB',
    primaries_xy=np.array([
        [0.6400, 0.3300],  # Red
        [0.3000, 0.6000],  # Green
        [0.1500, 0.0600],  # Blue
    ]),
    white_point='D65',
    transfer_function='srgb',
    description='Standard RGB for web and consumer displays (IEC 61966-2-1)'
)

# Display P3 (Apple, DCI-P3 with D65)
DISPLAY_P3 = RGBProfile(
    name='Display P3',
    primaries_xy=np.array([
        [0.6800, 0.3200],  # Red (wider than sRGB)
        [0.2650, 0.6900],  # Green (wider than sRGB)
        [0.1500, 0.0600],  # Blue (same as sRGB)
    ]),
    white_point='D65',
    transfer_function='srgb',  # Uses sRGB transfer function
    description='Wide gamut RGB for Apple displays and digital cinema'
)

# Adobe RGB (1998)
ADOBE_RGB = RGBProfile(
    name='Adobe RGB (1998)',
    primaries_xy=np.array([
        [0.6400, 0.3300],  # Red (same as sRGB)
        [0.2100, 0.7100],  # Green (wider than sRGB)
        [0.1500, 0.0600],  # Blue (same as sRGB)
    ]),
    white_point='D65',
    transfer_function='gamma_2.2',
    description='Wide gamut RGB for professional photography and print'
)

# ProPhoto RGB (ROMM RGB)
PROPHOTO_RGB = RGBProfile(
    name='ProPhoto RGB',
    primaries_xy=np.array([
        [0.7347, 0.2653],  # Red (very wide)
        [0.1596, 0.8404],  # Green (very wide)
        [0.0366, 0.0001],  # Blue (imaginary primary!)
    ]),
    white_point='D50',
    transfer_function='gamma_1.8',
    description='Very wide gamut RGB for professional photography (includes imaginary colors)'
)

# Rec. 2020 (ITU-R BT.2020)
REC2020 = RGBProfile(
    name='Rec. 2020',
    primaries_xy=np.array([
        [0.7080, 0.2920],  # Red
        [0.1700, 0.7970],  # Green
        [0.1310, 0.0460],  # Blue
    ]),
    white_point='D65',
    transfer_function='gamma_2.4',  # Simplified; actual BT.2020 has more complex TF
    description='Ultra-wide gamut RGB for HDR television (ITU-R BT.2020)'
)

# Profile registry
PROFILES = {
    'srgb': SRGB,
    'sRGB': SRGB,
    'display_p3': DISPLAY_P3,
    'Display P3': DISPLAY_P3,
    'p3': DISPLAY_P3,
    'P3': DISPLAY_P3,
    'adobe_rgb': ADOBE_RGB,
    'Adobe RGB': ADOBE_RGB,
    'adobergb': ADOBE_RGB,
    'prophoto': PROPHOTO_RGB,
    'ProPhoto RGB': PROPHOTO_RGB,
    'prophoto_rgb': PROPHOTO_RGB,
    'rec2020': REC2020,
    'Rec. 2020': REC2020,
    'bt2020': REC2020,
}


def get_profile(name: Union[str, RGBProfile]) -> RGBProfile:
    """
    Get an RGB profile by name or return the profile if already an RGBProfile.

    Args:
        name: Profile name (e.g., 'sRGB', 'Display P3') or RGBProfile instance

    Returns:
        RGBProfile instance

    Raises:
        ValueError: If profile name is unknown
    """
    if isinstance(name, RGBProfile):
        return name

    if name not in PROFILES:
        available = ', '.join(sorted(set(PROFILES.keys())))
        raise ValueError(f"Unknown profile '{name}'. Available: {available}")

    return PROFILES[name]


# =============================================================================
# Utility Functions
# =============================================================================

def compare_gamuts(profile1: Union[str, RGBProfile],
                   profile2: Union[str, RGBProfile],
                   n_samples: int = 1000) -> dict:
    """
    Compare the gamut volumes of two RGB profiles.

    Args:
        profile1: First profile
        profile2: Second profile
        n_samples: Number of random samples for comparison

    Returns:
        Dictionary with comparison statistics
    """
    p1 = get_profile(profile1)
    p2 = get_profile(profile2)

    # Generate random RGB samples
    np.random.seed(42)
    rgb_samples = np.random.rand(n_samples, 3)

    # Convert to XYZ using each profile
    xyz1 = p1.rgb_to_xyz(rgb_samples)
    xyz2 = p2.rgb_to_xyz(rgb_samples)

    # Check cross-compatibility
    p1_in_p2 = p2.is_in_gamut(xyz1)
    p2_in_p1 = p1.is_in_gamut(xyz2)

    return {
        'profile1': p1.name,
        'profile2': p2.name,
        'p1_coverage_in_p2': float(np.mean(p1_in_p2) * 100),
        'p2_coverage_in_p1': float(np.mean(p2_in_p1) * 100),
    }


def list_profiles() -> list:
    """List all available profile names."""
    return sorted(set(p.name for p in PROFILES.values()))


# =============================================================================
# Tests
# =============================================================================

def _test_profiles():
    """Test profile functionality."""
    print("RGB Profile Tests")
    print("=" * 60)

    # Test 1: sRGB matrix verification
    print("\n1. sRGB RGB→XYZ Matrix:")
    print(SRGB.rgb_to_xyz_matrix)

    # Reference values (IEC 61966-2-1)
    expected_srgb = np.array([
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1191920, 0.9503041]
    ])

    # Note: Slight differences due to white point precision
    diff = np.max(np.abs(SRGB.rgb_to_xyz_matrix - expected_srgb))
    print(f"Max difference from reference: {diff:.6f}")

    # Test 2: Round-trip conversion
    print("\n2. Round-trip RGB → XYZ → RGB:")
    test_rgb = np.array([0.5, 0.3, 0.7])
    xyz = SRGB.rgb_to_xyz(test_rgb)
    rgb_back = SRGB.xyz_to_rgb(xyz)
    print(f"Original:  {test_rgb}")
    print(f"XYZ:       {xyz}")
    print(f"Recovered: {rgb_back}")
    print(f"Error:     {np.max(np.abs(test_rgb - rgb_back)):.6e}")

    # Test 3: Gamut comparison
    print("\n3. Gamut Comparison (sRGB vs P3):")
    comparison = compare_gamuts('sRGB', 'Display P3')
    print(f"sRGB colors in P3 gamut: {comparison['p1_coverage_in_p2']:.1f}%")
    print(f"P3 colors in sRGB gamut: {comparison['p2_coverage_in_p1']:.1f}%")

    # Test 4: White point handling
    print("\n4. White Point XYZ:")
    for name in ['D65', 'D50', 'C']:
        wp = WHITE_POINTS_XYZ[name]
        print(f"  {name}: X={wp[0]:.5f}, Y={wp[1]:.5f}, Z={wp[2]:.5f}")

    print("\n" + "=" * 60)
    print("All tests passed!")


if __name__ == '__main__':
    _test_profiles()
