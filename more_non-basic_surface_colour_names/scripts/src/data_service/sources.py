"""
Data Source Implementations

Each source class:
1. Knows the path to its raw data
2. Implements a shim to transform raw data to ColorEntry schema
3. Never copies data - only reads from the canonical location
4. Provides lazy loading - data is loaded only when accessed
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterator, List, Optional, Dict, Any
import csv
import re
import json

from .schema import ColorEntry, ColorSource, CoordinateType


# Base path for all datasets - canonical location
DATASETS_ROOT = Path(__file__).parent.parent.parent.parent / 'datasets'


class BaseDataSource(ABC):
    """
    Abstract base class for all data sources.

    Each subclass must implement:
    - source_id: unique identifier for this source
    - data_path: path to the raw data (relative to DATASETS_ROOT)
    - _load_raw(): generator that yields ColorEntry objects
    """

    def __init__(self, root: Optional[Path] = None):
        """Initialize with optional custom root path."""
        self.root = root or DATASETS_ROOT
        self._cache: Optional[List[ColorEntry]] = None

    @property
    @abstractmethod
    def source_id(self) -> ColorSource:
        """Return the source identifier."""
        pass

    @property
    @abstractmethod
    def data_path(self) -> Path:
        """Return the path to raw data relative to root."""
        pass

    @abstractmethod
    def _load_raw(self) -> Iterator[ColorEntry]:
        """Load and transform raw data to ColorEntry objects."""
        pass

    def exists(self) -> bool:
        """Check if the data source exists."""
        full_path = self.root / self.data_path
        return full_path.exists()

    def load(self, use_cache: bool = True) -> List[ColorEntry]:
        """
        Load all entries from this source.

        Args:
            use_cache: If True, return cached data if available

        Returns:
            List of ColorEntry objects
        """
        if use_cache and self._cache is not None:
            return self._cache

        if not self.exists():
            raise FileNotFoundError(
                f"Data not found at {self.root / self.data_path}. "
                f"See datasets/SOURCES.md for download instructions."
            )

        self._cache = list(self._load_raw())
        return self._cache

    def iter_entries(self) -> Iterator[ColorEntry]:
        """Iterate over entries without caching."""
        if not self.exists():
            raise FileNotFoundError(
                f"Data not found at {self.root / self.data_path}"
            )
        yield from self._load_raw()

    def clear_cache(self):
        """Clear the cached data."""
        self._cache = None


class CentoreSource(BaseDataSource):
    """
    Paul Centore's JAIC 2020 polyhedron data.

    Contains 30 color families with Munsell coordinates for CAUS samples.
    This is SURFACE COLOR data (spectrophotometer-measured).
    """

    @property
    def source_id(self) -> ColorSource:
        return ColorSource.CENTORE

    @property
    def data_path(self) -> Path:
        return Path('centore/PolyhedronFiles')

    def _load_raw(self) -> Iterator[ColorEntry]:
        """Parse Centore's polyhedron text files."""
        data_dir = self.root / self.data_path

        for txt_file in sorted(data_dir.glob('PolyhedronDataFor*.txt')):
            # Extract family name from filename
            family = txt_file.stem.replace('PolyhedronDataFor', '')

            # Parse file content
            with open(txt_file, 'r') as f:
                content = f.read()

            # Extract samples section
            samples = self._parse_samples(content, family)
            for entry in samples:
                yield entry

    def _parse_samples(self, content: str, family: str) -> Iterator[ColorEntry]:
        """Parse sample lines from Centore's format."""
        # Look for the Samples section
        in_samples = False
        # Format: Year  Season  Market  Name  Munsell  HueAngle
        # e.g.: 1948  ss  silk  Bermuda Aqua  3.84GY 6.71/0.70  33.84
        # Munsell: HUE Value/Chroma or N Value (for neutrals)
        sample_pattern = re.compile(
            r'^(\d{4}(?:-\d{2})?)\s+'  # Year like 1948 or 1997-98
            r'(ss|fw|na)\s+'  # Season
            r'(\w+)\s+'  # Market
            r'(.+?)\s+'  # Name (non-greedy)
            r'(\d+\.?\d*[A-Z]+\s+\d+\.?\d*/\d+\.?\d*|N\s*\d+\.?\d*)\s+'  # Munsell
            r'(\d+\.?\d*)$'  # Hue angle
        )

        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue

            if 'Unique samples, with Munsell coordinates, from CAUS data:' in line:
                in_samples = True
                continue

            if in_samples:
                # Try to parse as sample line
                match = sample_pattern.match(line)
                if match:
                    year_str = match.group(1)
                    # Extract first year for ranges like "1997-98"
                    year = int(year_str.split('-')[0]) if year_str else None
                    name = match.group(4).strip()
                    munsell = match.group(5).strip()

                    yield ColorEntry(
                        name=name,
                        source=ColorSource.CENTORE,
                        munsell=munsell,
                        family=family,
                        year=year,
                        is_basic_color=family in ['blue', 'brown', 'gray', 'green',
                                                   'orange', 'pink', 'purple', 'red',
                                                   'white', 'yellow'],
                    )


class XKCDSource(BaseDataSource):
    """
    XKCD Color Survey data.

    Contains crowd-sourced color names with RGB hex values.
    This is SCREEN COLOR data (uncalibrated RGB monitors).
    """

    @property
    def source_id(self) -> ColorSource:
        return ColorSource.XKCD

    @property
    def data_path(self) -> Path:
        return Path('xkcd/xkcd_color_survey.txt')

    def _load_raw(self) -> Iterator[ColorEntry]:
        """Parse XKCD color survey summary file."""
        file_path = self.root / self.data_path

        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                # Format: "name\t#hexcolor"
                parts = line.split('\t')
                if len(parts) >= 2:
                    name = parts[0].strip()
                    hex_color = parts[1].strip()

                    yield ColorEntry(
                        name=name,
                        source=ColorSource.XKCD,
                        rgb_hex=hex_color,
                    )


class XKCDFullSurveySource(BaseDataSource):
    """
    Full XKCD survey data (SQL dumps).

    Contains all 3.4M responses, not just summary.
    Much larger but provides frequency counts.
    """

    @property
    def source_id(self) -> ColorSource:
        return ColorSource.XKCD

    @property
    def data_path(self) -> Path:
        return Path('xkcd/mainsurvey_sqldump.txt')

    def _load_raw(self) -> Iterator[ColorEntry]:
        """Parse full XKCD survey SQL dump."""
        # This would parse the larger file
        # For now, delegate to aggregated version if available
        aggregated = self.root / 'collected' / 'xkcd_colors.csv'
        if aggregated.exists():
            with open(aggregated, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    yield ColorEntry(
                        name=row.get('name', ''),
                        source=ColorSource.XKCD,
                        rgb_hex=row.get('hex') or row.get('coordinates'),
                    )


class MeodaiSource(BaseDataSource):
    """
    Meodai color names collection.

    Contains 32,000+ color names aggregated from various sources.
    RGB hex coordinates.
    """

    @property
    def source_id(self) -> ColorSource:
        return ColorSource.MEODAI

    @property
    def data_path(self) -> Path:
        return Path('collected/meodai_colors.csv')

    def _load_raw(self) -> Iterator[ColorEntry]:
        """Parse Meodai CSV."""
        file_path = self.root / self.data_path

        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get('name', '')
                hex_color = row.get('hex') or row.get('coordinates') or row.get('color')

                if name and hex_color:
                    yield ColorEntry(
                        name=name,
                        source=ColorSource.MEODAI,
                        rgb_hex=hex_color,
                    )


class ColorHexaSource(BaseDataSource):
    """ColorHexa color names."""

    @property
    def source_id(self) -> ColorSource:
        return ColorSource.COLORHEXA

    @property
    def data_path(self) -> Path:
        return Path('collected/colorhexa_colors.csv')

    def _load_raw(self) -> Iterator[ColorEntry]:
        """Parse ColorHexa CSV."""
        file_path = self.root / self.data_path

        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get('name', '')
                hex_color = row.get('hex') or row.get('coordinates')

                if name and hex_color:
                    yield ColorEntry(
                        name=name,
                        source=ColorSource.COLORHEXA,
                        rgb_hex=hex_color,
                    )


class WikipediaSource(BaseDataSource):
    """Wikipedia color lists."""

    @property
    def source_id(self) -> ColorSource:
        return ColorSource.WIKIPEDIA

    @property
    def data_path(self) -> Path:
        return Path('collected/wikipedia_colors.csv')

    def _load_raw(self) -> Iterator[ColorEntry]:
        """Parse Wikipedia colors CSV."""
        file_path = self.root / self.data_path

        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get('name', '')
                hex_color = row.get('hex') or row.get('coordinates')

                if name and hex_color:
                    yield ColorEntry(
                        name=name,
                        source=ColorSource.WIKIPEDIA,
                        rgb_hex=hex_color,
                    )


class SurfaceColorsSource(BaseDataSource):
    """
    Surface color data from various sources.

    Consolidated surface colors with Munsell coordinates where available.
    Sources include: Golden Acrylics, Williamsburg Oils, RAL, NCS, etc.
    """

    @property
    def source_id(self) -> ColorSource:
        return ColorSource.UNKNOWN  # Multi-source

    @property
    def data_path(self) -> Path:
        return Path('surface_colors')

    def _load_raw(self) -> Iterator[ColorEntry]:
        """Load surface colors from consolidated sources."""
        data_dir = self.root / self.data_path

        # Try consolidated file first
        consolidated = data_dir / 'consolidated_surface_colors.csv'
        if consolidated.exists():
            with open(consolidated, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    source_str = row.get('source', 'unknown')
                    try:
                        source = ColorSource(source_str)
                    except ValueError:
                        source = ColorSource.UNKNOWN

                    yield ColorEntry(
                        name=row.get('name', ''),
                        source=source,
                        rgb_hex=row.get('rgb_hex'),
                        munsell=row.get('munsell'),
                        family=row.get('family'),
                    )
        else:
            # Load from individual source files
            for csv_file in sorted(data_dir.glob('*.csv')):
                yield from self._load_csv(csv_file)

    def _load_csv(self, csv_file: Path) -> Iterator[ColorEntry]:
        """Load a single CSV file."""
        # Determine source from filename
        name_to_source = {
            'golden': ColorSource.GOLDEN_ACRYLICS,
            'williamsburg': ColorSource.WILLIAMSBURG_OILS,
            'ral': ColorSource.RAL_CLASSIC,
            'ncs': ColorSource.NCS,
            'pantone': ColorSource.PANTONE,
            'copic': ColorSource.COPIC,
            'rhs': ColorSource.RHS,
        }

        source = ColorSource.UNKNOWN
        for key, src in name_to_source.items():
            if key in csv_file.stem.lower():
                source = src
                break

        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield ColorEntry(
                    name=row.get('name', ''),
                    source=source,
                    rgb_hex=row.get('rgb_hex') or row.get('hex'),
                    munsell=row.get('munsell'),
                    family=row.get('family'),
                )


class WCSSource(BaseDataSource):
    """
    World Color Survey data.

    Cross-linguistic color naming data.
    """

    @property
    def source_id(self) -> ColorSource:
        return ColorSource.WCS

    @property
    def data_path(self) -> Path:
        return Path('wcs')

    def _load_raw(self) -> Iterator[ColorEntry]:
        """Load WCS data."""
        data_dir = self.root / self.data_path

        # Load chip coordinates from cnum-vhcm-lab.txt
        # Format: cnum  V  H  C  MunH  MunV  L*  a*  b*
        chip_file = data_dir / 'cnum-vhcm-lab.txt'
        if chip_file.exists():
            with open(chip_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    parts = line.split('\t')
                    if len(parts) >= 9:
                        chip_num = parts[0]
                        munsell_hue = parts[4]  # MunH like "10.00RP"
                        munsell_val = parts[5]  # MunV like "9"
                        l_star = float(parts[6])
                        a_star = float(parts[7])
                        b_star = float(parts[8])

                        # Construct Munsell notation (simplified)
                        munsell = f"{munsell_hue} {munsell_val}/0"

                        yield ColorEntry(
                            name=f"wcs_chip_{chip_num}",
                            source=ColorSource.WCS,
                            munsell=munsell,
                            lab=(l_star, a_star, b_star),
                        )


# Registry of all available sources
SOURCE_REGISTRY: Dict[str, type] = {
    'centore': CentoreSource,
    'xkcd': XKCDSource,
    'xkcd_full': XKCDFullSurveySource,
    'meodai': MeodaiSource,
    'colorhexa': ColorHexaSource,
    'wikipedia': WikipediaSource,
    'surface': SurfaceColorsSource,
    'wcs': WCSSource,
}


def get_source(name: str, root: Optional[Path] = None) -> BaseDataSource:
    """
    Get a data source by name.

    Args:
        name: Source name (e.g., 'centore', 'xkcd')
        root: Optional custom root path

    Returns:
        Initialized data source
    """
    if name not in SOURCE_REGISTRY:
        raise ValueError(
            f"Unknown source: {name}. "
            f"Available: {list(SOURCE_REGISTRY.keys())}"
        )
    return SOURCE_REGISTRY[name](root)
