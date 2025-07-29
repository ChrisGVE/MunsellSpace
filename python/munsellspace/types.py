"""
Type definitions for MunsellSpace Python API.
"""

from dataclasses import dataclass
from typing import Union, Optional
import re


class ConversionError(Exception):
    """
    Exception raised when color conversion fails.
    
    This can occur due to:
    - Invalid RGB values (not in 0-255 range)
    - Out-of-gamut colors that cannot be represented in Munsell space
    - Internal conversion errors from the Rust backend
    """
    pass


@dataclass
class MunsellColor:
    """
    Represents a color in the Munsell color system.
    
    The Munsell color system describes colors using three dimensions:
    - Hue: Color family (R, YR, Y, GY, G, BG, B, PB, P, RP)
    - Value: Lightness from 0 (black) to 10 (white)  
    - Chroma: Saturation from 0 (neutral) to 15+ (vivid)
    
    Attributes:
        notation (str): Complete Munsell notation (e.g., "5R 4.0/14.0" or "N 5.6/")
        hue (Optional[str]): Hue component (None for neutral colors)
        value (float): Value (lightness) component
        chroma (Optional[float]): Chroma (saturation) component (None for neutral colors)
    
    Examples:
        >>> # Chromatic color
        >>> color = MunsellColor("5R 4.0/14.0", "5R", 4.0, 14.0)
        >>> print(color.is_neutral())  # False
        >>> 
        >>> # Neutral color  
        >>> gray = MunsellColor("N 5.6/", None, 5.6, None)
        >>> print(gray.is_neutral())  # True
    """
    notation: str
    hue: Optional[str]
    value: float
    chroma: Optional[float]
    
    def __str__(self) -> str:
        """Return the Munsell notation string."""
        return self.notation
    
    def is_neutral(self) -> bool:
        """
        Check if this is a neutral (achromatic) color.
        
        Returns:
            bool: True if the color is neutral (no hue/chroma), False otherwise
        """
        return self.hue is None or self.chroma is None
    
    def is_chromatic(self) -> bool:
        """
        Check if this is a chromatic color.
        
        Returns:
            bool: True if the color has hue and chroma, False otherwise
        """
        return not self.is_neutral()
    
    @classmethod
    def from_notation(cls, notation: str) -> 'MunsellColor':
        """
        Parse a Munsell notation string into a MunsellColor object.
        
        Args:
            notation (str): Munsell notation (e.g., "5R 4.0/14.0" or "N 5.6/")
            
        Returns:
            MunsellColor: Parsed color object
            
        Raises:
            ConversionError: If the notation string is invalid
            
        Examples:
            >>> color = MunsellColor.from_notation("5R 4.0/14.0")
            >>> print(color.hue)  # "5R"
            >>> print(color.value)  # 4.0
            >>> print(color.chroma)  # 14.0
            
            >>> gray = MunsellColor.from_notation("N 5.6/")
            >>> print(gray.is_neutral())  # True
        """
        notation = notation.strip()
        
        # Handle neutral colors (e.g., "N 5.6/" or "N 5.6")
        neutral_match = re.match(r'^N\s+([0-9.]+)/?$', notation)
        if neutral_match:
            value = float(neutral_match.group(1))
            return cls(notation, None, value, None)
        
        # Handle chromatic colors (e.g., "5R 4.0/14.0")
        chromatic_match = re.match(r'^([0-9.]+[A-Z]+)\s+([0-9.]+)/([0-9.]+)$', notation)
        if chromatic_match:
            hue = chromatic_match.group(1)
            value = float(chromatic_match.group(2))
            chroma = float(chromatic_match.group(3))
            return cls(notation, hue, value, chroma)
        
        raise ConversionError(f"Invalid Munsell notation: {notation}")
    
    def to_dict(self) -> dict:
        """
        Convert to dictionary representation.
        
        Returns:
            dict: Dictionary with notation, hue, value, and chroma keys
        """
        return {
            "notation": self.notation,
            "hue": self.hue,
            "value": self.value,
            "chroma": self.chroma,
            "is_neutral": self.is_neutral()
        }