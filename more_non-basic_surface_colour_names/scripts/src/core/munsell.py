"""
Munsell color coordinate handling.

This module provides data structures and parsing functions for Munsell color
notation, supporting both chromatic and neutral (achromatic) colors.

Validated against Centore's 30 polyhedra with 100% concordance.

Reference:
    Centore, P. (2020) "Beige, aqua, fuchsia, etc." JAIC Vol. 25, pp. 24-54.
"""

import re
import math
from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class MunsellCoord:
    """
    Munsell color coordinate supporting both chromatic and neutral colors.

    The Munsell system uses three dimensions:
    - Hue: Circular scale with 10 major hue families (R, YR, Y, GY, G, BG, B, PB, P, RP)
    - Value: Lightness from 0 (black) to 10 (white)
    - Chroma: Saturation/colorfulness from 0 (neutral gray) outward

    Neutral colors (grays) have no hue and are denoted as "N{value}" (e.g., "N5" for middle gray).

    Attributes:
        hue_number: Numeric position within hue family (0-10, e.g., 5R means hue_number=5)
        hue_letter: Hue family code ('R', 'YR', etc.) or 'N' for neutral
        value: Lightness value (0-10)
        chroma: Saturation (0 for neutral, increases outward)

    Example:
        >>> coord = MunsellCoord(5.0, 'R', 4.0, 14.0)  # 5R 4/14 (saturated red)
        >>> coord = MunsellCoord(0.0, 'N', 9.02, 0.0)  # N9.02 (near-white gray)
    """
    hue_number: float
    hue_letter: str  # 'N' for neutral (achromatic)
    value: float
    chroma: float

    @property
    def is_neutral(self) -> bool:
        """Check if this is a neutral (achromatic) color."""
        return self.hue_letter == 'N'

    @property
    def hue_continuous(self) -> float:
        """
        Convert to continuous 0-100 hue scale.

        The Munsell hue circle is divided into 10 families of 10 steps each.
        This converts the (hue_number, hue_letter) pair to a single 0-100 value.

        Returns:
            Hue on 0-100 scale where 0=R, 10=YR, 20=Y, ..., 90=RP, 100=R again.
            Returns 0.0 for neutral colors (by convention).
        """
        if self.is_neutral:
            return 0.0  # Neutral has no hue, use 0 by convention
        hue_order = ['R', 'YR', 'Y', 'GY', 'G', 'BG', 'B', 'PB', 'P', 'RP']
        idx = hue_order.index(self.hue_letter)
        return (idx * 10) + self.hue_number

    def to_cartesian(self) -> Tuple[float, float, float]:
        """
        Convert to Centore's Cartesian coordinate system.

        Centore uses a cylindrical-to-Cartesian mapping where:
        - x = Chroma * cos(Hue * pi/50)
        - y = Chroma * sin(Hue * pi/50)
        - z = Value

        The factor pi/50 converts the 0-100 hue scale to radians (100 -> 2*pi).

        For neutral colors (chroma=0), x=y=0 regardless of hue.

        Returns:
            Tuple (x, y, z) in Centore's Cartesian space.

        Reference:
            Centore (2020), equations 1-3.
        """
        if self.is_neutral:
            # Neutral colors have chroma=0, so x=y=0
            return (0.0, 0.0, self.value)
        h = self.hue_continuous
        angle = h * math.pi / 50  # Convert 0-100 scale to radians
        x = self.chroma * math.cos(angle)
        y = self.chroma * math.sin(angle)
        z = self.value
        return (x, y, z)

    def __str__(self) -> str:
        """Return standard Munsell notation string."""
        if self.is_neutral:
            return f"N{self.value}"
        return f"{self.hue_number}{self.hue_letter} {self.value}/{self.chroma}"


def parse_munsell(s: str) -> Optional[MunsellCoord]:
    """
    Parse a Munsell notation string into a MunsellCoord object.

    Supports two notation formats:
    1. Chromatic: "{hue_number}{hue_letter} {value}/{chroma}"
       Examples: "5R 4/14", "7.5YR 6/8", "10GY 5.5/10"

    2. Neutral: "N{value}"
       Examples: "N5", "N9.02"

    Args:
        s: Munsell notation string to parse.

    Returns:
        MunsellCoord object if parsing succeeds, None otherwise.

    Example:
        >>> parse_munsell("5R 4/14")
        MunsellCoord(hue_number=5.0, hue_letter='R', value=4.0, chroma=14.0)
        >>> parse_munsell("N9.02")
        MunsellCoord(hue_number=0.0, hue_letter='N', value=9.02, chroma=0.0)
    """
    s = s.strip()

    # Check for neutral color first: N followed by value (e.g., "N9.02")
    neutral_pattern = r'^N(\d+\.?\d*)$'
    neutral_match = re.match(neutral_pattern, s)
    if neutral_match:
        return MunsellCoord(
            hue_number=0.0,
            hue_letter='N',
            value=float(neutral_match.group(1)),
            chroma=0.0
        )

    # Standard chromatic pattern: {hue_number}{hue_letter} {value}/{chroma}
    pattern = r'(\d+\.?\d*)(R|YR|Y|GY|G|BG|B|PB|P|RP)\s+(\d+\.?\d*)/(\d+\.?\d*)'
    match = re.match(pattern, s)
    if not match:
        return None
    return MunsellCoord(
        hue_number=float(match.group(1)),
        hue_letter=match.group(2),
        value=float(match.group(3)),
        chroma=float(match.group(4))
    )


def parse_munsell_from_line(line: str) -> Optional[MunsellCoord]:
    """
    Extract and parse Munsell notation from a line that may contain other text.

    Useful for parsing sample lines from Centore's data files where the Munsell
    notation is embedded in a longer line with other metadata.

    Args:
        line: Text line potentially containing Munsell notation.

    Returns:
        MunsellCoord if found, None otherwise.

    Example:
        >>> parse_munsell_from_line("2014-15\\tna\\tinteriors\\tPurplish White\\tN9.02\\t-99.00")
        MunsellCoord(hue_number=0.0, hue_letter='N', value=9.02, chroma=0.0)
    """
    # Check for neutral color first (e.g., "N9.02")
    neutral_match = re.search(r'\bN(\d+\.?\d*)\b', line)
    if neutral_match:
        return MunsellCoord(
            hue_number=0.0,
            hue_letter='N',
            value=float(neutral_match.group(1)),
            chroma=0.0
        )

    # Check for chromatic color
    chromatic_match = re.search(
        r'(\d+\.?\d*)(R|YR|Y|GY|G|BG|B|PB|P|RP)\s+(\d+\.?\d*)/(\d+\.?\d*)',
        line
    )
    if chromatic_match:
        return parse_munsell(chromatic_match.group(0))

    return None
