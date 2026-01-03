"""
Standard Schema for Color Data

All data sources must transform their data to conform to this schema.
This ensures consistent handling across the entire pipeline.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, Tuple, List
import re


class CoordinateType(Enum):
    """Type of color coordinate system."""
    RGB_HEX = auto()      # "#RRGGBB" format
    RGB_DECIMAL = auto()  # (R, G, B) 0-255
    RGB_FLOAT = auto()    # (R, G, B) 0.0-1.0
    MUNSELL = auto()      # "5R 4/14" notation
    MUNSELL_CARTESIAN = auto()  # (x, y, z) Centore's formula
    LAB = auto()          # (L*, a*, b*) CIELAB
    XYZ = auto()          # CIE XYZ


class ColorSource(Enum):
    """Known data sources."""
    CENTORE = "centore"
    XKCD = "xkcd"
    MEODAI = "meodai"
    COLORHEXA = "colorhexa"
    WIKIPEDIA = "wikipedia"
    COLORNAME_COM = "colorname_com"
    WCS = "wcs"
    GOLDEN_ACRYLICS = "golden"
    WILLIAMSBURG_OILS = "williamsburg"
    RAL_CLASSIC = "ral"
    NCS = "ncs"
    PANTONE = "pantone"
    COPIC = "copic"
    RHS = "rhs"
    UNKNOWN = "unknown"


@dataclass
class ColorEntry:
    """
    Standard color entry schema.

    All data sources transform their data to this format.
    Missing values are represented as None, not special strings.
    """
    # Required fields
    name: str
    source: ColorSource

    # Coordinate fields (at least one should be populated)
    rgb_hex: Optional[str] = None           # "#RRGGBB"
    rgb_decimal: Optional[Tuple[int, int, int]] = None  # (R, G, B) 0-255
    munsell: Optional[str] = None           # "5R 4/14"
    munsell_cartesian: Optional[Tuple[float, float, float]] = None  # (x, y, z)
    lab: Optional[Tuple[float, float, float]] = None  # (L*, a*, b*)

    # Semantic fields
    family: Optional[str] = None            # Color family assignment
    is_basic_color: Optional[bool] = None   # Berlin & Kay basic term

    # Metadata
    sample_count: Optional[int] = None      # Number of samples (for aggregated)
    confidence: Optional[float] = None      # Confidence score 0-1
    year: Optional[int] = None              # Year of sample collection

    # Additional context
    description: Optional[str] = None
    tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Validate and normalize entry."""
        # Normalize name
        self.name = self._normalize_name(self.name)

        # Normalize RGB hex
        if self.rgb_hex:
            self.rgb_hex = self._normalize_hex(self.rgb_hex)

    @staticmethod
    def _normalize_name(name: str) -> str:
        """Normalize color name: lowercase, single spaces, trimmed."""
        name = name.lower().strip()
        name = re.sub(r'\s+', ' ', name)
        # Remove surrounding quotes
        if (name.startswith('"') and name.endswith('"')) or \
           (name.startswith("'") and name.endswith("'")):
            name = name[1:-1]
        return name

    @staticmethod
    def _normalize_hex(hex_str: str) -> str:
        """Normalize hex color to uppercase #RRGGBB format."""
        hex_str = hex_str.strip().upper()
        if not hex_str.startswith('#'):
            hex_str = '#' + hex_str
        # Expand short form #RGB to #RRGGBB
        if len(hex_str) == 4:
            hex_str = '#' + hex_str[1]*2 + hex_str[2]*2 + hex_str[3]*2
        return hex_str

    @property
    def has_coordinates(self) -> bool:
        """Check if entry has any coordinate data."""
        return any([
            self.rgb_hex,
            self.rgb_decimal,
            self.munsell,
            self.munsell_cartesian,
            self.lab
        ])

    @property
    def coordinate_type(self) -> Optional[CoordinateType]:
        """Return the primary coordinate type available."""
        if self.munsell:
            return CoordinateType.MUNSELL
        if self.munsell_cartesian:
            return CoordinateType.MUNSELL_CARTESIAN
        if self.rgb_hex or self.rgb_decimal:
            return CoordinateType.RGB_HEX if self.rgb_hex else CoordinateType.RGB_DECIMAL
        if self.lab:
            return CoordinateType.LAB
        return None

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            'name': self.name,
            'source': self.source.value,
            'rgb_hex': self.rgb_hex,
            'rgb_decimal': list(self.rgb_decimal) if self.rgb_decimal else None,
            'munsell': self.munsell,
            'munsell_cartesian': list(self.munsell_cartesian) if self.munsell_cartesian else None,
            'lab': list(self.lab) if self.lab else None,
            'family': self.family,
            'is_basic_color': self.is_basic_color,
            'sample_count': self.sample_count,
            'confidence': self.confidence,
            'year': self.year,
            'description': self.description,
            'tags': self.tags,
        }

    @classmethod
    def from_dict(cls, d: dict) -> 'ColorEntry':
        """Create entry from dictionary."""
        return cls(
            name=d['name'],
            source=ColorSource(d.get('source', 'unknown')),
            rgb_hex=d.get('rgb_hex'),
            rgb_decimal=tuple(d['rgb_decimal']) if d.get('rgb_decimal') else None,
            munsell=d.get('munsell'),
            munsell_cartesian=tuple(d['munsell_cartesian']) if d.get('munsell_cartesian') else None,
            lab=tuple(d['lab']) if d.get('lab') else None,
            family=d.get('family'),
            is_basic_color=d.get('is_basic_color'),
            sample_count=d.get('sample_count'),
            confidence=d.get('confidence'),
            year=d.get('year'),
            description=d.get('description'),
            tags=d.get('tags', []),
        )


# Berlin & Kay basic color terms
BASIC_COLOR_TERMS = frozenset([
    'red', 'yellow', 'green', 'blue', 'black', 'white',
    'gray', 'grey', 'orange', 'brown', 'pink', 'purple'
])


def is_basic_color_term(name: str) -> bool:
    """Check if a name is or contains a basic color term."""
    name_lower = name.lower()
    return name_lower in BASIC_COLOR_TERMS or any(
        term in name_lower.split() for term in BASIC_COLOR_TERMS
    )
