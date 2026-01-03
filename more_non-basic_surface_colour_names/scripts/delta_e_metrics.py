#!/usr/bin/env python3
"""
Delta E Metrics for Color Difference Calculation

Implements multiple color difference formulas for perceptual analysis:
- CIEDE2000 (ΔE*00) - Current CIE standard
- CIE94 (ΔE*94) - Previous CIE standard
- CMC(l:c) - Textile industry standard
- Euclidean in Munsell Cartesian space

Based on research documented in:
    more_non-basic_surface_colour_names/writeups/methodology/NONUNIFORM_SPACE_METRICS.md

References:
    - Sharma, Wu, Dalal (2005): "The CIEDE2000 Color-Difference Formula:
      Implementation Notes, Supplementary Test Data, and Mathematical Observations"
      Color Research & Application, vol. 30, No. 1, pp. 21-30
    - CIE Technical Report 142-2001: CIEDE2000 specification
    - ISO 105-J03:2009: CMC(l:c) specification

Author: Research Analyst (Claude Code)
Date: 2026-01-03
"""

import math
from typing import Tuple, List, Dict, Optional
from dataclasses import dataclass
import numpy as np


@dataclass
class LABColor:
    """CIE L*a*b* color representation."""
    L: float  # Lightness (0-100)
    a: float  # Red-green axis
    b: float  # Yellow-blue axis

    def to_lch(self) -> Tuple[float, float, float]:
        """Convert to L*C*h* cylindrical representation."""
        C = math.sqrt(self.a**2 + self.b**2)
        h = math.atan2(self.b, self.a)  # Radians
        return self.L, C, h


@dataclass
class MunsellColor:
    """Munsell color in cylindrical notation."""
    H: float  # Hue (0-100 scale)
    V: float  # Value (0-10)
    C: float  # Chroma (0+)

    def to_cartesian(self) -> Tuple[float, float, float]:
        """
        Convert to Cartesian coordinates using Centore's formula.

        Returns:
            (x, y, z) where:
                x = C × cos(H × π/50)
                y = C × sin(H × π/50)
                z = V
        """
        theta = self.H * math.pi / 50.0
        x = self.C * math.cos(theta)
        y = self.C * math.sin(theta)
        z = self.V
        return x, y, z


def delta_e_76(lab1: LABColor, lab2: LABColor) -> float:
    """
    CIE76 ΔE*ab - Simple Euclidean distance in CIELAB.

    Formula:
        ΔE*ab = √[(ΔL*)² + (Δa*)² + (Δb*)²]

    Args:
        lab1: First color in CIE L*a*b*
        lab2: Second color in CIE L*a*b*

    Returns:
        Color difference value (0+)

    Notes:
        - Simple but does not account for perceptual non-uniformities
        - Adequate for large color differences
        - Poor performance in blue region and near neutral axis
    """
    dL = lab1.L - lab2.L
    da = lab1.a - lab2.a
    db = lab1.b - lab2.b
    return math.sqrt(dL**2 + da**2 + db**2)


def delta_e_94(lab1: LABColor, lab2: LABColor,
               kL: float = 1.0, kC: float = 1.0, kH: float = 1.0) -> float:
    """
    CIE94 ΔE*94 color difference formula.

    Formula:
        ΔE*94 = √[(ΔL*/kL·SL)² + (ΔC*/kC·SC)² + (ΔH*/kH·SH)²]

        Where:
            SL = 1
            SC = 1 + 0.045·Cab*
            SH = 1 + 0.015·Cab*

    Args:
        lab1: First color in CIE L*a*b*
        lab2: Second color in CIE L*a*b*
        kL: Lightness weighting (default 1.0 for smooth surfaces, 2.0 for textiles)
        kC: Chroma weighting (default 1.0)
        kH: Hue weighting (default 1.0)

    Returns:
        Color difference value (0+)

    Notes:
        Standard parameter values:
        - Smooth surfaces (paint, plastic): kL=1, kC=1, kH=1
        - Rough surfaces (textiles): kL=2, kC=1, kH=1
    """
    # Convert to LCh
    L1, C1, h1 = lab1.to_lch()
    L2, C2, h2 = lab2.to_lch()

    # Differences
    dL = L1 - L2
    dC = C1 - C2
    da = lab1.a - lab2.a
    db = lab1.b - lab2.b

    # Hue difference (must account for deltaH, not deltah)
    dH_squared = da**2 + db**2 - dC**2
    dH = math.sqrt(max(0, dH_squared))  # Avoid sqrt of negative due to rounding

    # Weighting functions
    SL = 1.0
    SC = 1.0 + 0.045 * C1
    SH = 1.0 + 0.015 * C1

    # Weighted differences
    term_L = (dL / (kL * SL))**2
    term_C = (dC / (kC * SC))**2
    term_H = (dH / (kH * SH))**2

    return math.sqrt(term_L + term_C + term_H)


def delta_e_cmc(lab1: LABColor, lab2: LABColor, l: float = 2.0, c: float = 1.0) -> float:
    """
    CMC(l:c) color difference formula.

    Developed by the Colour Measurement Committee of the Society of Dyers and Colourists.
    Based on CIE L*C*h* with adjustable lightness:chroma weighting.

    Args:
        lab1: First color in CIE L*a*b* (reference color)
        lab2: Second color in CIE L*a*b* (sample color)
        l: Lightness weighting factor (default 2.0)
        c: Chroma weighting factor (default 1.0)

    Returns:
        Color difference value (0+)

    Notes:
        Common parameter combinations:
        - CMC(2:1): Acceptability decisions (default)
        - CMC(1:1): Imperceptibility threshold

        The formula uses the reference color (lab1) to compute weighting functions.
    """
    # Convert reference color to LCh
    L1, C1, h1 = lab1.to_lch()
    L2, C2, h2 = lab2.to_lch()

    # Differences
    dL = L1 - L2
    dC = C1 - C2
    da = lab1.a - lab2.a
    db = lab1.b - lab2.b

    # Hue difference
    dH_squared = da**2 + db**2 - dC**2
    dH = math.sqrt(max(0, dH_squared))

    # Convert hue to degrees for calculations
    h1_deg = math.degrees(h1)
    if h1_deg < 0:
        h1_deg += 360

    # Weighting functions (based on reference color)
    if L1 < 16:
        SL = 0.511
    else:
        SL = 0.040975 * L1 / (1 + 0.01765 * L1)

    SC = 0.0638 * C1 / (1 + 0.0131 * C1) + 0.638

    # Hue weighting depends on hue angle
    if 164 <= h1_deg <= 345:
        T = 0.56 + abs(0.2 * math.cos(h1 + math.radians(168)))
    else:
        T = 0.36 + abs(0.4 * math.cos(h1 + math.radians(35)))

    F = math.sqrt(C1**4 / (C1**4 + 1900))
    SH = SC * (F * T + 1 - F)

    # Weighted differences
    term_L = (dL / (l * SL))**2
    term_C = (dC / (c * SC))**2
    term_H = (dH / SH)**2

    return math.sqrt(term_L + term_C + term_H)


def delta_e_2000(lab1: LABColor, lab2: LABColor,
                 kL: float = 1.0, kC: float = 1.0, kH: float = 1.0) -> float:
    """
    CIEDE2000 ΔE*00 color difference formula (CIE standard).

    Implementation based on:
        Sharma, Wu, Dalal (2005): "The CIEDE2000 Color-Difference Formula"
        Color Research & Application, vol. 30, No. 1, pp. 21-30

    This is the most sophisticated and accurate color difference formula,
    accounting for:
        - Hue rotation in blue region
        - Compensation for neutral colors
        - Improved lightness, chroma, and hue weighting

    Args:
        lab1: First color in CIE L*a*b*
        lab2: Second color in CIE L*a*b*
        kL: Lightness weighting (default 1.0)
        kC: Chroma weighting (default 1.0)
        kH: Hue weighting (default 1.0)

    Returns:
        Color difference value (0+)

    Notes:
        Perceptual thresholds:
        - ΔE00 < 1.0: Just noticeable difference (JND)
        - ΔE00 < 2.0: Generally imperceptible under normal viewing
        - ΔE00 > 5.0: Clear perceptual difference
    """
    # Step 1: Calculate C̄ (average chroma) for a' calculation
    C1 = math.sqrt(lab1.a**2 + lab1.b**2)
    C2 = math.sqrt(lab2.a**2 + lab2.b**2)
    C_bar = (C1 + C2) / 2.0

    # Step 2: Calculate G (chroma weighting for a' adjustment)
    C_bar_7 = C_bar**7
    G = 0.5 * (1 - math.sqrt(C_bar_7 / (C_bar_7 + 25**7)))

    # Step 3: Calculate a' (adjusted a*)
    a1_prime = lab1.a * (1 + G)
    a2_prime = lab2.a * (1 + G)

    # Step 4: Calculate C' (chroma from adjusted a')
    C1_prime = math.sqrt(a1_prime**2 + lab1.b**2)
    C2_prime = math.sqrt(a2_prime**2 + lab2.b**2)

    # Step 5: Calculate h' (hue angle from adjusted a')
    h1_prime = math.atan2(lab1.b, a1_prime)
    h2_prime = math.atan2(lab2.b, a2_prime)

    # Convert to degrees [0, 360)
    h1_prime_deg = math.degrees(h1_prime) % 360
    h2_prime_deg = math.degrees(h2_prime) % 360

    # Step 6: Calculate ΔL', ΔC', ΔH'
    dL_prime = lab2.L - lab1.L
    dC_prime = C2_prime - C1_prime

    # Hue difference calculation (accounts for circular nature)
    if C1_prime * C2_prime == 0:
        dh_prime = 0
    else:
        dh_prime = h2_prime_deg - h1_prime_deg
        if dh_prime > 180:
            dh_prime -= 360
        elif dh_prime < -180:
            dh_prime += 360

    # ΔH' (hue difference)
    dH_prime = 2 * math.sqrt(C1_prime * C2_prime) * math.sin(math.radians(dh_prime / 2))

    # Step 7: Calculate L̄', C̄', H̄' (averages)
    L_bar_prime = (lab1.L + lab2.L) / 2.0
    C_bar_prime = (C1_prime + C2_prime) / 2.0

    # Average hue (accounts for circular nature)
    if C1_prime * C2_prime == 0:
        H_bar_prime = h1_prime_deg + h2_prime_deg
    else:
        h_sum = h1_prime_deg + h2_prime_deg
        h_diff = abs(h1_prime_deg - h2_prime_deg)
        if h_diff <= 180:
            H_bar_prime = h_sum / 2.0
        elif h_sum < 360:
            H_bar_prime = (h_sum + 360) / 2.0
        else:
            H_bar_prime = (h_sum - 360) / 2.0

    # Step 8: Calculate T (hue-dependent function)
    T = (1 - 0.17 * math.cos(math.radians(H_bar_prime - 30)) +
         0.24 * math.cos(math.radians(2 * H_bar_prime)) +
         0.32 * math.cos(math.radians(3 * H_bar_prime + 6)) -
         0.20 * math.cos(math.radians(4 * H_bar_prime - 63)))

    # Step 9: Calculate Δθ (hue rotation term)
    dTheta = 30 * math.exp(-((H_bar_prime - 275) / 25)**2)

    # Step 10: Calculate RC (chroma rotation term)
    C_bar_prime_7 = C_bar_prime**7
    RC = 2 * math.sqrt(C_bar_prime_7 / (C_bar_prime_7 + 25**7))

    # Step 11: Calculate SL, SC, SH (weighting functions)
    L_bar_prime_minus_50_squared = (L_bar_prime - 50)**2
    SL = 1 + (0.015 * L_bar_prime_minus_50_squared /
              math.sqrt(20 + L_bar_prime_minus_50_squared))
    SC = 1 + 0.045 * C_bar_prime
    SH = 1 + 0.015 * C_bar_prime * T

    # Step 12: Calculate RT (rotation term for hue and chroma interaction)
    RT = -math.sin(math.radians(2 * dTheta)) * RC

    # Step 13: Calculate final CIEDE2000 color difference
    term_L = (dL_prime / (kL * SL))**2
    term_C = (dC_prime / (kC * SC))**2
    term_H = (dH_prime / (kH * SH))**2
    term_RT = RT * (dC_prime / (kC * SC)) * (dH_prime / (kH * SH))

    return math.sqrt(term_L + term_C + term_H + term_RT)


def munsell_euclidean_distance(m1: MunsellColor, m2: MunsellColor) -> float:
    """
    Euclidean distance in Munsell Cartesian coordinates.

    Uses Centore's cylindrical-to-Cartesian transformation:
        x = C × cos(H × π/50)
        y = C × sin(H × π/50)
        z = V

    Args:
        m1: First color in Munsell notation
        m2: Second color in Munsell notation

    Returns:
        Euclidean distance in Munsell units

    Notes:
        - Simple geometric distance
        - Does not account for perceptual non-uniformities
        - Appropriate for convex hull calculations
        - May overweight chroma differences relative to hue/value
    """
    x1, y1, z1 = m1.to_cartesian()
    x2, y2, z2 = m2.to_cartesian()
    return math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)


@dataclass
class ColorPairComparison:
    """Results of comparing two colors using multiple metrics."""
    color1_name: str
    color2_name: str
    delta_e_76: float
    delta_e_94: float
    delta_e_cmc_2_1: float
    delta_e_cmc_1_1: float
    delta_e_2000: float
    munsell_distance: Optional[float] = None


def compare_metrics(color_pairs: List[Tuple[str, LABColor, LABColor,
                                             Optional[MunsellColor],
                                             Optional[MunsellColor]]]) -> List[ColorPairComparison]:
    """
    Compare multiple color difference metrics on a set of color pairs.

    Args:
        color_pairs: List of tuples containing:
            (pair_name, lab1, lab2, munsell1_optional, munsell2_optional)

    Returns:
        List of ColorPairComparison objects with all metrics computed

    Example:
        >>> pairs = [
        ...     ("red-pink", LABColor(53, 80, 67), LABColor(64, 48, 21), None, None),
        ...     ("blue-cyan", LABColor(32, 79, -108), LABColor(91, -48, -14), None, None)
        ... ]
        >>> results = compare_metrics(pairs)
        >>> for r in results:
        ...     print(f"{r.color1_name}: ΔE00={r.delta_e_2000:.2f}")
    """
    results = []

    for pair_data in color_pairs:
        name, lab1, lab2 = pair_data[:3]
        m1 = pair_data[3] if len(pair_data) > 3 else None
        m2 = pair_data[4] if len(pair_data) > 4 else None

        # Compute all CIELAB-based metrics
        de76 = delta_e_76(lab1, lab2)
        de94 = delta_e_94(lab1, lab2)
        de_cmc_2_1 = delta_e_cmc(lab1, lab2, l=2.0, c=1.0)
        de_cmc_1_1 = delta_e_cmc(lab1, lab2, l=1.0, c=1.0)
        de00 = delta_e_2000(lab1, lab2)

        # Compute Munsell distance if coordinates provided
        munsell_dist = None
        if m1 is not None and m2 is not None:
            munsell_dist = munsell_euclidean_distance(m1, m2)

        results.append(ColorPairComparison(
            color1_name=name.split('-')[0] if '-' in name else name,
            color2_name=name.split('-')[1] if '-' in name else "reference",
            delta_e_76=de76,
            delta_e_94=de94,
            delta_e_cmc_2_1=de_cmc_2_1,
            delta_e_cmc_1_1=de_cmc_1_1,
            delta_e_2000=de00,
            munsell_distance=munsell_dist
        ))

    return results


def print_comparison_table(comparisons: List[ColorPairComparison]) -> None:
    """
    Print a formatted table of color difference comparisons.

    Args:
        comparisons: List of ColorPairComparison objects
    """
    print("\n" + "="*100)
    print("COLOR DIFFERENCE METRIC COMPARISON")
    print("="*100)
    print(f"{'Pair':<20} {'ΔE*76':<10} {'ΔE*94':<10} {'CMC(2:1)':<10} "
          f"{'CMC(1:1)':<10} {'ΔE*00':<10} {'Munsell':<10}")
    print("-"*100)

    for comp in comparisons:
        pair_name = f"{comp.color1_name}-{comp.color2_name}"
        munsell_str = f"{comp.munsell_distance:.2f}" if comp.munsell_distance else "N/A"
        print(f"{pair_name:<20} {comp.delta_e_76:<10.2f} {comp.delta_e_94:<10.2f} "
              f"{comp.delta_e_cmc_2_1:<10.2f} {comp.delta_e_cmc_1_1:<10.2f} "
              f"{comp.delta_e_2000:<10.2f} {munsell_str:<10}")

    print("="*100)
    print("\nInterpretation (CIEDE2000):")
    print("  ΔE*00 < 1.0  : Just noticeable difference (JND)")
    print("  ΔE*00 < 2.0  : Generally imperceptible")
    print("  ΔE*00 2-5    : Perceptible but close")
    print("  ΔE*00 > 5.0  : Clear perceptual difference")
    print()


# Demonstration and validation
if __name__ == "__main__":
    print("Delta E Metrics Implementation")
    print("Based on Sharma et al. (2005) and CIE standards\n")

    # Test cases based on Sharma et al. (2005) test data
    test_cases = [
        # (name, L1, a1, b1, L2, a2, b2, expected_ΔE00)
        ("Sharma Test 1", 50.0, 2.6772, -79.7751, 50.0, 0.0, -82.7485, 2.0425),
        ("Sharma Test 2", 50.0, 3.1571, -77.2803, 50.0, 0.0, -82.7485, 2.8615),
        ("Sharma Test 5", 50.0, -1.3802, -84.2814, 50.0, 0.0, -82.7485, 1.0000),
        ("Sharma Test 10", 50.0, 2.4900, -0.0010, 50.0, -2.4900, 0.0009, 7.1792),
        ("Gray pair", 50.0, 0.0, 0.0, 50.0, 0.0, 0.0, 0.0),  # Identical grays
    ]

    print("VALIDATION TEST: Sharma et al. (2005) Test Data")
    print("-" * 80)

    for name, L1, a1, b1, L2, a2, b2, expected in test_cases:
        lab1 = LABColor(L1, a1, b1)
        lab2 = LABColor(L2, a2, b2)
        computed = delta_e_2000(lab1, lab2)
        error = abs(computed - expected)
        status = "✓ PASS" if error < 0.0001 else "✗ FAIL"
        print(f"{name:<20} Expected: {expected:.4f}  Computed: {computed:.4f}  "
              f"Error: {error:.4f}  {status}")

    print("\n" + "="*80)
    print("COMPREHENSIVE COMPARISON: Multiple Color Pairs")
    print("="*80 + "\n")

    # Example color pairs for comprehensive comparison
    demo_pairs = [
        ("red-pink",
         LABColor(53.23, 80.11, 67.22),
         LABColor(81.26, 14.58, 23.29),
         MunsellColor(5, 5.3, 12.0),
         MunsellColor(2.5, 8.1, 5.5)),

        ("blue-cyan",
         LABColor(32.30, 79.20, -107.86),
         LABColor(91.11, -48.09, -14.13),
         MunsellColor(52.5, 3.2, 14.8),
         MunsellColor(75, 9.1, 7.2)),

        ("yellow-gold",
         LABColor(97.14, -21.55, 94.48),
         LABColor(80.0, 5.0, 75.0),
         MunsellColor(15, 9.7, 11.5),
         MunsellColor(12.5, 8.0, 10.0)),

        ("neutral-gray",
         LABColor(50.0, 0.0, 0.0),
         LABColor(70.0, 0.0, 0.0),
         MunsellColor(0, 5.0, 0.0),
         MunsellColor(0, 7.0, 0.0)),
    ]

    results = compare_metrics(demo_pairs)
    print_comparison_table(results)

    print("\nNOTES:")
    print("- CMC(2:1) is commonly used for acceptability decisions")
    print("- CMC(1:1) is used for imperceptibility thresholds")
    print("- CIEDE2000 is the current CIE standard (most accurate)")
    print("- Munsell distance is geometric only (not perceptually uniform)")
    print()
