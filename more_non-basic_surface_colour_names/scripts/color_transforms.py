#!/usr/bin/env python3
"""
Color Space Transformation Functions

Implements core color space transformations for screen-to-surface color analysis.
Uses colour-science library where available, implements from scratch where needed
for educational understanding.

Part of Phase 1.2: Color Space Transformation Implementation
"""

import numpy as np
from typing import Tuple, List, Dict, Optional, Literal
import warnings

try:
    import colour
    COLOUR_AVAILABLE = True
except ImportError:
    COLOUR_AVAILABLE = False
    warnings.warn(
        "colour-science library not available. "
        "Install with: pip install colour-science"
    )


# ============================================================================
# Constants and Matrices
# ============================================================================

# Standard RGB to XYZ transformation matrix (ITU-R BT.709, D65 white point)
# Source: https://en.wikipedia.org/wiki/Rec._709
RGB_TO_XYZ_MATRIX = np.array([
    [0.4124564, 0.3575761, 0.1804375],
    [0.2126729, 0.7151522, 0.0721750],
    [0.0193339, 0.1191920, 0.9503041]
])

# Inverse: XYZ to RGB
XYZ_TO_RGB_MATRIX = np.array([
    [ 3.2404542, -1.5371385, -0.4985314],
    [-0.9692660,  1.8760108,  0.0415560],
    [ 0.0556434, -0.2040259,  1.0572252]
])

# Chromatic adaptation matrices
# Bradford CAT
BRADFORD_MATRIX = np.array([
    [ 0.8951,  0.2664, -0.1614],
    [-0.7502,  1.7135,  0.0367],
    [ 0.0389, -0.0685,  1.0296]
])

BRADFORD_INV = np.linalg.inv(BRADFORD_MATRIX)

# CAT02
CAT02_MATRIX = np.array([
    [ 0.7328,  0.4296, -0.1624],
    [-0.7036,  1.6975,  0.0061],
    [ 0.0030,  0.0136,  0.9834]
])

CAT02_INV = np.linalg.inv(CAT02_MATRIX)

# Von Kries (Hunt-Pointer-Estevez cone fundamentals)
VON_KRIES_MATRIX = np.array([
    [ 0.4002,  0.7075, -0.0807],
    [-0.2280,  1.1500,  0.0612],
    [ 0.0000,  0.0000,  0.9184]
])

VON_KRIES_INV = np.linalg.inv(VON_KRIES_MATRIX)

# Standard illuminants (CIE 1931 2° Standard Observer)
# Source: https://en.wikipedia.org/wiki/Standard_illuminant
ILLUMINANTS = {
    'D65': np.array([95.047, 100.000, 108.883]),   # Daylight 6500K
    'D50': np.array([96.422, 100.000, 82.521]),    # Daylight 5000K
    'C':   np.array([98.074, 100.000, 118.232]),   # Average daylight (obsolete but used for Munsell)
    'A':   np.array([109.850, 100.000, 35.585]),   # Incandescent 2856K
}

# Chromatic adaptation transform method to matrix mapping
CAT_MATRICES = {
    'bradford': (BRADFORD_MATRIX, BRADFORD_INV),
    'cat02': (CAT02_MATRIX, CAT02_INV),
    'von_kries': (VON_KRIES_MATRIX, VON_KRIES_INV),
}


# ============================================================================
# Gamma Correction Functions
# ============================================================================

def srgb_to_linear(srgb: np.ndarray) -> np.ndarray:
    """
    Convert sRGB values to linear RGB using the official sRGB transfer function.

    The sRGB standard uses a piecewise function, not pure gamma 2.2:
    - Linear segment near black (avoids infinite slope at zero)
    - Power function for other values

    Args:
        srgb: Array of sRGB values in range [0, 1]

    Returns:
        Linear RGB values in range [0, 1]

    Reference:
        https://en.wikipedia.org/wiki/SRGB
    """
    srgb = np.asarray(srgb, dtype=float)

    # Ensure values are in [0, 1]
    if np.any((srgb < 0) | (srgb > 1)):
        warnings.warn("sRGB values outside [0, 1] range. Clipping.")
        srgb = np.clip(srgb, 0, 1)

    linear = np.where(
        srgb <= 0.04045,
        srgb / 12.92,
        np.power((srgb + 0.055) / 1.055, 2.4)
    )

    return linear


def linear_to_srgb(linear: np.ndarray) -> np.ndarray:
    """
    Convert linear RGB values to sRGB using the official sRGB transfer function.

    Args:
        linear: Array of linear RGB values in range [0, 1]

    Returns:
        sRGB values in range [0, 1]

    Reference:
        https://en.wikipedia.org/wiki/SRGB
    """
    linear = np.asarray(linear, dtype=float)

    # Clip negative values (can occur from out-of-gamut XYZ)
    linear = np.maximum(linear, 0)

    srgb = np.where(
        linear <= 0.0031308,
        12.92 * linear,
        1.055 * np.power(linear, 1/2.4) - 0.055
    )

    return np.clip(srgb, 0, 1)


def gamma_correction(values: np.ndarray, gamma: float = 2.2, inverse: bool = False) -> np.ndarray:
    """
    Apply simple gamma correction (for non-sRGB workflows).

    Args:
        values: Array of values to correct
        gamma: Gamma value (default 2.2, typical for displays)
        inverse: If True, apply inverse gamma (encoding), else apply gamma (decoding)

    Returns:
        Gamma-corrected values

    Note:
        For proper sRGB handling, use srgb_to_linear() and linear_to_srgb() instead.
    """
    values = np.asarray(values, dtype=float)
    values = np.maximum(values, 0)  # Avoid negative values

    if inverse:
        # Encoding: linear → gamma
        return np.power(values, 1/gamma)
    else:
        # Decoding: gamma → linear
        return np.power(values, gamma)


# ============================================================================
# RGB ↔ XYZ Conversions
# ============================================================================

def rgb_to_xyz(rgb: np.ndarray, gamma: float = 2.2) -> np.ndarray:
    """
    Convert RGB to CIE XYZ (D65 white point).

    Args:
        rgb: RGB values in range [0, 1], shape (..., 3)
        gamma: Gamma value for decoding (default 2.2 for sRGB approximation)
               Use None to skip gamma correction (input already linear)

    Returns:
        XYZ values (Y normalized to 100 for white), shape (..., 3)

    Notes:
        - Uses ITU-R BT.709 / sRGB transformation matrix
        - For precise sRGB, set gamma=None and call srgb_to_linear() first
    """
    rgb = np.asarray(rgb, dtype=float)
    original_shape = rgb.shape
    rgb = rgb.reshape(-1, 3)

    # Gamma correction if requested
    if gamma is not None:
        linear_rgb = srgb_to_linear(rgb) if gamma == 2.2 else gamma_correction(rgb, gamma)
    else:
        linear_rgb = rgb

    # Matrix multiplication
    xyz = linear_rgb @ RGB_TO_XYZ_MATRIX.T

    # Scale Y to 100 for white
    xyz *= 100

    return xyz.reshape(original_shape)


def xyz_to_rgb(xyz: np.ndarray, gamma: float = 2.2, clip: bool = True) -> np.ndarray:
    """
    Convert CIE XYZ to RGB (D65 white point).

    Args:
        xyz: XYZ values (Y normalized to 100), shape (..., 3)
        gamma: Gamma value for encoding (default 2.2 for sRGB approximation)
               Use None to skip gamma correction (output linear RGB)
        clip: If True, clip out-of-gamut values to [0, 1]

    Returns:
        RGB values in range [0, 1], shape (..., 3)

    Notes:
        - Uses ITU-R BT.709 / sRGB transformation matrix
        - For precise sRGB, set gamma=None and call linear_to_srgb() after
        - Out-of-gamut XYZ values will produce RGB outside [0, 1]
    """
    xyz = np.asarray(xyz, dtype=float)
    original_shape = xyz.shape
    xyz = xyz.reshape(-1, 3)

    # Scale from 100-normalized to matrix convention
    xyz_scaled = xyz / 100

    # Matrix multiplication
    linear_rgb = xyz_scaled @ XYZ_TO_RGB_MATRIX.T

    # Gamma encoding if requested
    if gamma is not None:
        rgb = linear_to_srgb(linear_rgb) if gamma == 2.2 else gamma_correction(linear_rgb, gamma, inverse=True)
    else:
        rgb = linear_rgb

    # Clip to valid range if requested
    if clip:
        rgb = np.clip(rgb, 0, 1)

    return rgb.reshape(original_shape)


# ============================================================================
# XYZ ↔ CIELAB Conversions
# ============================================================================

def _lab_f(t: np.ndarray) -> np.ndarray:
    """CIELAB f() function with linear segment near zero."""
    delta = 6/29
    return np.where(
        t > delta**3,
        np.cbrt(t),
        t / (3 * delta**2) + 4/29
    )


def _lab_f_inv(t: np.ndarray) -> np.ndarray:
    """Inverse of CIELAB f() function."""
    delta = 6/29
    return np.where(
        t > delta,
        t**3,
        3 * delta**2 * (t - 4/29)
    )


def xyz_to_lab(xyz: np.ndarray, illuminant: str = 'D65') -> np.ndarray:
    """
    Convert CIE XYZ to CIELAB.

    Args:
        xyz: XYZ values (Y normalized to 100), shape (..., 3)
        illuminant: Reference white point ('D65', 'D50', 'C', 'A')

    Returns:
        L*a*b* values, shape (..., 3)
        L* in [0, 100], a* and b* typically in [-128, 127]

    Reference:
        https://en.wikipedia.org/wiki/CIELAB_color_space
    """
    xyz = np.asarray(xyz, dtype=float)
    original_shape = xyz.shape
    xyz = xyz.reshape(-1, 3)

    # Get reference white
    if illuminant not in ILLUMINANTS:
        raise ValueError(f"Unknown illuminant '{illuminant}'. Choose from: {list(ILLUMINANTS.keys())}")
    white = ILLUMINANTS[illuminant]

    # Normalize by white point
    xyz_normalized = xyz / white

    # Apply f() function
    f_values = _lab_f(xyz_normalized)

    # Compute L*, a*, b*
    L = 116 * f_values[:, 1] - 16
    a = 500 * (f_values[:, 0] - f_values[:, 1])
    b = 200 * (f_values[:, 1] - f_values[:, 2])

    lab = np.stack([L, a, b], axis=-1)
    return lab.reshape(original_shape)


def lab_to_xyz(lab: np.ndarray, illuminant: str = 'D65') -> np.ndarray:
    """
    Convert CIELAB to CIE XYZ.

    Args:
        lab: L*a*b* values, shape (..., 3)
        illuminant: Reference white point ('D65', 'D50', 'C', 'A')

    Returns:
        XYZ values (Y normalized to 100), shape (..., 3)

    Reference:
        https://en.wikipedia.org/wiki/CIELAB_color_space
    """
    lab = np.asarray(lab, dtype=float)
    original_shape = lab.shape
    lab = lab.reshape(-1, 3)

    # Get reference white
    if illuminant not in ILLUMINANTS:
        raise ValueError(f"Unknown illuminant '{illuminant}'. Choose from: {list(ILLUMINANTS.keys())}")
    white = ILLUMINANTS[illuminant]

    # Extract L*, a*, b*
    L, a, b_val = lab[:, 0], lab[:, 1], lab[:, 2]

    # Compute f() values
    f_y = (L + 16) / 116
    f_x = a / 500 + f_y
    f_z = f_y - b_val / 200

    # Apply inverse f() function
    xyz_normalized = np.stack([
        _lab_f_inv(f_x),
        _lab_f_inv(f_y),
        _lab_f_inv(f_z)
    ], axis=-1)

    # Denormalize by white point
    xyz = xyz_normalized * white

    return xyz.reshape(original_shape)


# ============================================================================
# Chromatic Adaptation
# ============================================================================

def apply_chromatic_adaptation(
    xyz: np.ndarray,
    source_wp: np.ndarray,
    dest_wp: np.ndarray,
    method: Literal['bradford', 'cat02', 'von_kries'] = 'bradford'
) -> np.ndarray:
    """
    Apply chromatic adaptation transform (CAT) to convert XYZ values
    from one illuminant to another using von Kries-based methods.

    Args:
        xyz: XYZ tristimulus values, shape (..., 3)
        source_wp: Source white point XYZ, shape (3,)
        dest_wp: Destination white point XYZ, shape (3,)
        method: CAT method - 'bradford' (recommended), 'cat02', or 'von_kries'

    Returns:
        Adapted XYZ values, shape (..., 3)

    References:
        - Bradford: https://colorjs.io/docs/adaptation
        - CAT02: https://www.colour-science.org/api/0.3.0/html/colour.adaptation.cat.html
        - Von Kries: https://en.wikipedia.org/wiki/Chromatic_adaptation

    Example:
        >>> xyz_c = np.array([50, 60, 70])  # Color under Illuminant C
        >>> xyz_d65 = apply_chromatic_adaptation(
        ...     xyz_c,
        ...     ILLUMINANTS['C'],
        ...     ILLUMINANTS['D65'],
        ...     method='bradford'
        ... )
    """
    xyz = np.asarray(xyz, dtype=float)
    source_wp = np.asarray(source_wp, dtype=float)
    dest_wp = np.asarray(dest_wp, dtype=float)

    original_shape = xyz.shape
    xyz = xyz.reshape(-1, 3)

    # Get transformation matrix
    if method not in CAT_MATRICES:
        raise ValueError(f"Unknown CAT method '{method}'. Choose from: {list(CAT_MATRICES.keys())}")

    M, M_inv = CAT_MATRICES[method]

    # Convert white points to cone response space
    rho_src = M @ source_wp
    rho_dst = M @ dest_wp

    # Compute diagonal scaling matrix
    # Avoid division by zero
    scale = np.where(rho_src > 1e-10, rho_dst / rho_src, 1.0)
    D = np.diag(scale)

    # Full transformation: M^-1 * D * M
    transformation = M_inv @ D @ M

    # Apply transformation
    xyz_adapted = xyz @ transformation.T

    return xyz_adapted.reshape(original_shape)


# ============================================================================
# Error Analysis Functions
# ============================================================================

def analyze_conversion_error(
    colors: np.ndarray,
    chain: List[str],
    reference_illuminant: str = 'D65'
) -> Dict[str, any]:
    """
    Measure error accumulation through a color conversion chain via round-trip conversion.

    Args:
        colors: Starting colors, shape (N, 3)
        chain: Conversion chain as list of space names
               Example: ['rgb', 'xyz', 'lab', 'xyz', 'rgb']
        reference_illuminant: Illuminant for XYZ/LAB conversions

    Returns:
        Dictionary with error statistics:
        - 'max_error': Maximum component-wise error
        - 'mean_error': Mean component-wise error
        - 'rmse': Root mean square error
        - 'delta_e': Mean CIEDE2000 color difference (if applicable)
        - 'errors': Per-color errors, shape (N,)

    Example:
        >>> rgb_colors = np.random.rand(100, 3)
        >>> stats = analyze_conversion_error(
        ...     rgb_colors,
        ...     ['rgb', 'xyz', 'lab', 'xyz', 'rgb']
        ... )
        >>> print(f"RMSE: {stats['rmse']:.6f}")
    """
    colors = np.asarray(colors, dtype=float)
    current = colors.copy()

    # Define conversion functions
    conversions = {
        ('rgb', 'xyz'): lambda c: rgb_to_xyz(c, gamma=None),  # Assume input is linear
        ('xyz', 'rgb'): lambda c: xyz_to_rgb(c, gamma=None, clip=False),
        ('xyz', 'lab'): lambda c: xyz_to_lab(c, illuminant=reference_illuminant),
        ('lab', 'xyz'): lambda c: lab_to_xyz(c, illuminant=reference_illuminant),
    }

    # Apply conversion chain
    for i in range(len(chain) - 1):
        src = chain[i]
        dst = chain[i + 1]

        key = (src, dst)
        if key not in conversions:
            raise ValueError(f"No conversion defined for {src} → {dst}")

        current = conversions[key](current)

    # Compute errors
    errors = current - colors
    component_errors = np.abs(errors)

    max_error = np.max(component_errors)
    mean_error = np.mean(component_errors)
    rmse = np.sqrt(np.mean(errors**2))
    per_color_rmse = np.sqrt(np.mean(errors**2, axis=1))

    result = {
        'max_error': max_error,
        'mean_error': mean_error,
        'rmse': rmse,
        'errors': per_color_rmse,
        'error_components': errors
    }

    # If round-trip ends in LAB, compute CIEDE2000 (requires colour-science)
    if chain[-1] == 'lab' and chain[0] == 'lab' and COLOUR_AVAILABLE:
        try:
            delta_e = colour.delta_E(colors, current, method='CIE 2000')
            result['delta_e_2000'] = float(np.mean(delta_e))
            result['delta_e_max'] = float(np.max(delta_e))
        except Exception as e:
            warnings.warn(f"Could not compute CIEDE2000: {e}")

    return result


# ============================================================================
# Munsell Conversions
# ============================================================================

# Munsell hue angles (radians) for each major hue
# Standard Munsell hue notation: R, YR, Y, GY, G, BG, B, PB, P, RP
# Each major hue spans 36 degrees (10 steps), with 5 being the pure hue
MUNSELL_HUE_ANGLES = {
    'R': 0,      # Red at 0°
    'YR': 36,    # Yellow-Red at 36°
    'Y': 72,     # Yellow at 72°
    'GY': 108,   # Green-Yellow at 108°
    'G': 144,    # Green at 144°
    'BG': 180,   # Blue-Green at 180°
    'B': 216,    # Blue at 216°
    'PB': 252,   # Purple-Blue at 252°
    'P': 288,    # Purple at 288°
    'RP': 324,   # Red-Purple at 324°
}


def rgb_to_munsell_cartesian(rgb: np.ndarray) -> Optional[np.ndarray]:
    """
    Convert sRGB to Munsell Cartesian coordinates (x, y, z).

    Munsell Cartesian coordinates are:
        x = Chroma * cos(Hue_radians)
        y = Chroma * sin(Hue_radians)
        z = Value

    Args:
        rgb: sRGB values in range [0, 1], shape (3,) or (N, 3)

    Returns:
        Munsell Cartesian coordinates (x, y, z), same shape as input
        Returns None if conversion fails (e.g., out of gamut)

    Notes:
        - Uses colour-science library for accurate conversion if available
        - Falls back to HSV-based approximation otherwise
        - Hue angle follows Munsell notation (R=0°, Y=72°, G=144°, B=216°)
    """
    rgb = np.asarray(rgb, dtype=float)

    # Handle single color vs batch
    single_color = rgb.ndim == 1
    if single_color:
        rgb = rgb.reshape(1, 3)

    # Clamp RGB to valid range
    rgb = np.clip(rgb, 0, 1)

    if COLOUR_AVAILABLE:
        try:
            # Use colour-science for accurate conversion
            # Convert sRGB to xyY first, then to Munsell
            xyz = rgb_to_xyz(rgb)

            results = []
            for i in range(len(rgb)):
                try:
                    # colour.xyY_to_munsell_colour expects xyY
                    xyz_single = xyz[i] / 100  # Normalize for colour-science

                    # Check for very dark colors (near black)
                    if xyz_single[1] < 0.001:  # Y (luminance) very low
                        # Black has undefined hue, return neutral
                        results.append(np.array([0.0, 0.0, 0.0]))
                        continue

                    # Convert XYZ to xyY
                    sum_xyz = np.sum(xyz_single)
                    if sum_xyz < 1e-10:
                        results.append(np.array([0.0, 0.0, 0.0]))
                        continue

                    x_chrom = xyz_single[0] / sum_xyz
                    y_chrom = xyz_single[1] / sum_xyz
                    Y = xyz_single[1] * 100  # Luminance percentage

                    xyY = np.array([x_chrom, y_chrom, Y])

                    # Get Munsell specification
                    munsell_spec = colour.xyY_to_munsell_colour(xyY)

                    # Parse Munsell specification (format: "H V/C" e.g., "5R 5/10")
                    # Returns tuple (hue_number, hue_letter, value, chroma)
                    hue_value, hue_letter, value, chroma = colour.munsell_colour_to_munsell_specification(munsell_spec)

                    # Convert to angle
                    base_angle = MUNSELL_HUE_ANGLES.get(hue_letter, 0)
                    # Hue value is 0-10 within each hue sector (36 degrees)
                    # 5 is the pure hue, so offset from base
                    hue_degrees = base_angle + (hue_value - 5) * 3.6
                    hue_radians = np.radians(hue_degrees)

                    # Convert to Cartesian
                    x = chroma * np.cos(hue_radians)
                    y = chroma * np.sin(hue_radians)
                    z = value

                    results.append(np.array([x, y, z]))

                except Exception:
                    # If colour-science fails, use fallback for this color
                    result = _rgb_to_munsell_cartesian_approx(rgb[i])
                    results.append(result if result is not None else np.array([0.0, 0.0, 0.0]))

            result = np.array(results)
            return result[0] if single_color else result

        except Exception:
            pass  # Fall through to approximation

    # Fallback: HSV-based approximation
    results = []
    for i in range(len(rgb)):
        result = _rgb_to_munsell_cartesian_approx(rgb[i])
        if result is None:
            return None
        results.append(result)

    result = np.array(results)
    return result[0] if single_color else result


def _rgb_to_munsell_cartesian_approx(rgb: np.ndarray) -> Optional[np.ndarray]:
    """
    Approximate RGB to Munsell Cartesian using HSV-based mapping.

    This is a rough approximation that maps:
    - HSV Hue (0-360) to Munsell Hue angle
    - HSV Saturation × Value × 14 to approximate Munsell Chroma
    - HSV Value × 10 to Munsell Value

    Args:
        rgb: Single RGB color, shape (3,)

    Returns:
        Approximate Munsell Cartesian (x, y, z), or None if invalid
    """
    r, g, b = rgb

    # Convert to HSV
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    diff = max_c - min_c

    # Value (Munsell scale 0-10)
    value = max_c * 10

    # Saturation
    if max_c < 1e-10:
        saturation = 0
    else:
        saturation = diff / max_c

    # Hue (in degrees, 0-360)
    if diff < 1e-10:
        hue_degrees = 0  # Achromatic
    elif max_c == r:
        hue_degrees = 60 * (((g - b) / diff) % 6)
    elif max_c == g:
        hue_degrees = 60 * (((b - r) / diff) + 2)
    else:  # max_c == b
        hue_degrees = 60 * (((r - g) / diff) + 4)

    # Map HSV hue to Munsell hue
    # HSV: Red=0°, Yellow=60°, Green=120°, Cyan=180°, Blue=240°, Magenta=300°
    # Munsell: R=0°, Y=72°, G=144°, B=216°
    # Approximate mapping (HSV hue is somewhat close to Munsell)
    # HSV to Munsell adjustment: Munsell yellow is at 72°, HSV yellow at 60°
    munsell_hue = hue_degrees * (360 / 360)  # Direct mapping for now

    # Approximate chroma (Munsell chroma typically 0-14 for surface colors)
    # This is a very rough approximation
    chroma = saturation * value * 1.4  # Scale factor for typical surface colors

    # Convert to Cartesian
    hue_radians = np.radians(munsell_hue)
    x = chroma * np.cos(hue_radians)
    y = chroma * np.sin(hue_radians)
    z = value

    return np.array([x, y, z])


def munsell_cartesian_to_rgb(munsell_xyz: np.ndarray) -> Optional[np.ndarray]:
    """
    Convert Munsell Cartesian coordinates back to sRGB (approximate).

    Args:
        munsell_xyz: Munsell Cartesian (x, y, z) where z is Value

    Returns:
        sRGB values in [0, 1], or None if out of gamut

    Notes:
        This is an approximate inverse primarily for visualization.
        Use colour-science for accurate conversions.
    """
    x, y, z = munsell_xyz

    # Extract polar coordinates
    chroma = np.sqrt(x**2 + y**2)
    hue_radians = np.arctan2(y, x)
    hue_degrees = np.degrees(hue_radians) % 360
    value = z

    if COLOUR_AVAILABLE:
        try:
            # Find closest Munsell hue
            hue_letter = 'R'
            min_diff = 360
            for letter, angle in MUNSELL_HUE_ANGLES.items():
                diff = abs((hue_degrees - angle + 180) % 360 - 180)
                if diff < min_diff:
                    min_diff = diff
                    hue_letter = letter
                    base_angle = angle

            # Calculate hue number (0-10 within sector)
            hue_offset = (hue_degrees - base_angle + 180) % 360 - 180
            hue_number = 5 + hue_offset / 3.6
            hue_number = np.clip(hue_number, 0, 10)

            # Create Munsell specification
            munsell_spec = colour.munsell_specification_to_munsell_colour(
                (hue_number, hue_letter, value, chroma)
            )

            # Convert to xyY then to XYZ then to RGB
            xyY = colour.munsell_colour_to_xyY(munsell_spec)

            # xyY to XYZ
            x_chrom, y_chrom, Y = xyY
            if y_chrom < 1e-10:
                return np.array([0.0, 0.0, 0.0])

            xyz = np.array([
                x_chrom * Y / y_chrom,
                Y,
                (1 - x_chrom - y_chrom) * Y / y_chrom
            ])

            # XYZ to RGB
            rgb = xyz_to_rgb(xyz * 100)
            return np.clip(rgb, 0, 1)

        except Exception:
            pass  # Fall through to approximation

    # Fallback: approximate HSV-based conversion
    # Reverse the approximation from _rgb_to_munsell_cartesian_approx
    if value < 0.001:
        return np.array([0.0, 0.0, 0.0])

    # Approximate saturation from chroma and value
    saturation = chroma / (value * 1.4) if value > 0.001 else 0
    saturation = np.clip(saturation, 0, 1)

    # Convert HSV to RGB
    hue_normalized = (hue_degrees / 60) % 6
    i = int(hue_normalized)
    f = hue_normalized - i

    v = value / 10  # Scale back to 0-1
    p = v * (1 - saturation)
    q = v * (1 - saturation * f)
    t = v * (1 - saturation * (1 - f))

    if i == 0:
        rgb = np.array([v, t, p])
    elif i == 1:
        rgb = np.array([q, v, p])
    elif i == 2:
        rgb = np.array([p, v, t])
    elif i == 3:
        rgb = np.array([p, q, v])
    elif i == 4:
        rgb = np.array([t, p, v])
    else:
        rgb = np.array([v, p, q])

    return np.clip(rgb, 0, 1)


# ============================================================================
# Utility Functions
# ============================================================================

def check_gamut(rgb: np.ndarray, tolerance: float = 1e-6) -> Tuple[np.ndarray, float]:
    """
    Check which colors are within sRGB gamut.

    Args:
        rgb: RGB values, shape (..., 3)
        tolerance: Tolerance for out-of-gamut detection

    Returns:
        - Boolean array indicating in-gamut colors
        - Percentage of in-gamut colors
    """
    rgb = np.asarray(rgb)
    in_gamut = np.all((rgb >= -tolerance) & (rgb <= 1 + tolerance), axis=-1)
    percentage = 100 * np.mean(in_gamut)
    return in_gamut, percentage


def display_color_info(rgb: np.ndarray, name: str = "Color"):
    """
    Display comprehensive information about a color.

    Args:
        rgb: RGB value, shape (3,)
        name: Name/label for the color
    """
    rgb = np.asarray(rgb, dtype=float)

    print(f"\n{'=' * 60}")
    print(f"{name}")
    print(f"{'=' * 60}")
    print(f"sRGB:        [{rgb[0]:.4f}, {rgb[1]:.4f}, {rgb[2]:.4f}]")
    print(f"sRGB (8-bit): [{int(rgb[0]*255)}, {int(rgb[1]*255)}, {int(rgb[2]*255)}]")
    print(f"Hex:         #{int(rgb[0]*255):02x}{int(rgb[1]*255):02x}{int(rgb[2]*255):02x}")

    xyz = rgb_to_xyz(rgb)
    print(f"\nXYZ (D65):   [{xyz[0]:.2f}, {xyz[1]:.2f}, {xyz[2]:.2f}]")

    lab = xyz_to_lab(xyz)
    print(f"CIELAB:      L*={lab[0]:.2f}, a*={lab[1]:.2f}, b*={lab[2]:.2f}")

    # Check gamut
    in_gamut, _ = check_gamut(rgb)
    print(f"\nIn sRGB gamut: {in_gamut.item()}")
    print(f"{'=' * 60}\n")


# ============================================================================
# Example Usage and Tests
# ============================================================================

def _test_conversions():
    """Test color conversion functions with known values."""
    print("Testing Color Conversions\n")

    # Test 1: sRGB primary red
    print("Test 1: sRGB Red")
    red_srgb = np.array([1.0, 0.0, 0.0])
    display_color_info(red_srgb, "sRGB Red (primary)")

    # Test 2: Round-trip conversion
    print("\nTest 2: Round-trip RGB → XYZ → LAB → XYZ → RGB")
    test_colors = np.array([
        [1.0, 0.0, 0.0],  # Red
        [0.0, 1.0, 0.0],  # Green
        [0.0, 0.0, 1.0],  # Blue
        [0.5, 0.5, 0.5],  # Gray
    ])

    errors = analyze_conversion_error(
        srgb_to_linear(test_colors),
        ['rgb', 'xyz', 'lab', 'xyz', 'rgb']
    )

    print(f"Max error: {errors['max_error']:.2e}")
    print(f"RMSE: {errors['rmse']:.2e}")

    # Test 3: Chromatic adaptation
    print("\nTest 3: Chromatic Adaptation (Illuminant C → D65)")
    xyz_c = np.array([50.0, 60.0, 70.0])
    xyz_d65 = apply_chromatic_adaptation(
        xyz_c,
        ILLUMINANTS['C'],
        ILLUMINANTS['D65'],
        method='bradford'
    )
    print(f"XYZ under C:   {xyz_c}")
    print(f"XYZ under D65: {xyz_d65}")

    # Test 4: Gamut checking
    print("\nTest 4: Gamut Checking")
    test_rgb = np.array([
        [0.5, 0.5, 0.5],   # In gamut
        [1.2, 0.5, 0.5],   # Out of gamut
        [-0.1, 0.3, 0.7],  # Out of gamut
    ])
    in_gamut, pct = check_gamut(test_rgb)
    print(f"In-gamut status: {in_gamut}")
    print(f"Percentage in-gamut: {pct:.1f}%")


if __name__ == '__main__':
    _test_conversions()
