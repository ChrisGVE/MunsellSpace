"""
Data Aggregator

Combines multiple data sources with:
- Deduplication by name
- Conflict resolution (source priority)
- Filtering by criteria
- No data copying - all operations are on-demand
"""

from pathlib import Path
from typing import Iterator, List, Optional, Dict, Set, Callable
from collections import defaultdict

from .schema import ColorEntry, ColorSource, CoordinateType
from .sources import BaseDataSource, get_source, SOURCE_REGISTRY, DATASETS_ROOT


class DataAggregator:
    """
    Aggregates data from multiple sources.

    Provides:
    - Unified iteration over multiple sources
    - Deduplication by normalized name
    - Priority-based conflict resolution
    - Filtering capabilities
    """

    # Default source priority (higher = preferred)
    DEFAULT_PRIORITY = {
        ColorSource.CENTORE: 100,  # Reference standard
        ColorSource.GOLDEN_ACRYLICS: 90,  # Native Munsell
        ColorSource.WILLIAMSBURG_OILS: 90,  # Native Munsell
        ColorSource.WCS: 80,  # Academic standard
        ColorSource.WIKIPEDIA: 50,
        ColorSource.MEODAI: 40,
        ColorSource.COLORHEXA: 30,
        ColorSource.XKCD: 20,  # Screen colors, lower priority for surface work
        ColorSource.UNKNOWN: 10,
    }

    def __init__(self, root: Optional[Path] = None):
        """Initialize aggregator."""
        self.root = root or DATASETS_ROOT
        self._sources: List[BaseDataSource] = []
        self._priority: Dict[ColorSource, int] = dict(self.DEFAULT_PRIORITY)

    def add_source(self, source: BaseDataSource) -> 'DataAggregator':
        """Add a data source to aggregate."""
        self._sources.append(source)
        return self

    def add_sources(self, *names: str) -> 'DataAggregator':
        """Add multiple sources by name."""
        for name in names:
            self._sources.append(get_source(name, self.root))
        return self

    def set_priority(self, source: ColorSource, priority: int) -> 'DataAggregator':
        """Set priority for a source (higher = preferred)."""
        self._priority[source] = priority
        return self

    def iter_all(self) -> Iterator[ColorEntry]:
        """
        Iterate over all entries from all sources.

        Does NOT deduplicate - returns all entries.
        """
        for source in self._sources:
            if source.exists():
                yield from source.iter_entries()

    def iter_unique(self, prefer_munsell: bool = True) -> Iterator[ColorEntry]:
        """
        Iterate over unique entries (by normalized name).

        When duplicates exist, returns the highest-priority entry.
        If prefer_munsell is True, entries with Munsell coordinates
        get a priority boost.
        """
        seen: Dict[str, ColorEntry] = {}
        scores: Dict[str, int] = {}

        for entry in self.iter_all():
            name = entry.name  # Already normalized
            score = self._priority.get(entry.source, 0)

            # Boost score if has Munsell coordinates and we prefer them
            if prefer_munsell and entry.munsell:
                score += 50

            if name not in seen or score > scores[name]:
                seen[name] = entry
                scores[name] = score

        yield from seen.values()

    def iter_filtered(
        self,
        has_munsell: Optional[bool] = None,
        has_rgb: Optional[bool] = None,
        family: Optional[str] = None,
        source: Optional[ColorSource] = None,
        min_confidence: Optional[float] = None,
        name_contains: Optional[str] = None,
        name_pattern: Optional[str] = None,
    ) -> Iterator[ColorEntry]:
        """
        Iterate with filters applied.

        Args:
            has_munsell: If True, only entries with Munsell coordinates
            has_rgb: If True, only entries with RGB coordinates
            family: Filter by color family
            source: Filter by source
            min_confidence: Minimum confidence score
            name_contains: Name must contain this substring
            name_pattern: Regex pattern for name matching
        """
        import re as regex

        for entry in self.iter_all():
            # Apply filters
            if has_munsell is not None:
                if has_munsell and not entry.munsell:
                    continue
                if not has_munsell and entry.munsell:
                    continue

            if has_rgb is not None:
                if has_rgb and not (entry.rgb_hex or entry.rgb_decimal):
                    continue
                if not has_rgb and (entry.rgb_hex or entry.rgb_decimal):
                    continue

            if family is not None and entry.family != family:
                continue

            if source is not None and entry.source != source:
                continue

            if min_confidence is not None:
                if entry.confidence is None or entry.confidence < min_confidence:
                    continue

            if name_contains is not None:
                if name_contains.lower() not in entry.name.lower():
                    continue

            if name_pattern is not None:
                if not regex.search(name_pattern, entry.name, regex.IGNORECASE):
                    continue

            yield entry

    def group_by_family(self) -> Dict[str, List[ColorEntry]]:
        """Group entries by color family."""
        groups: Dict[str, List[ColorEntry]] = defaultdict(list)
        for entry in self.iter_all():
            if entry.family:
                groups[entry.family].append(entry)
        return dict(groups)

    def group_by_source(self) -> Dict[ColorSource, List[ColorEntry]]:
        """Group entries by source."""
        groups: Dict[ColorSource, List[ColorEntry]] = defaultdict(list)
        for entry in self.iter_all():
            groups[entry.source].append(entry)
        return dict(groups)

    def get_statistics(self) -> Dict:
        """Get aggregate statistics."""
        total = 0
        by_source: Dict[str, int] = defaultdict(int)
        with_munsell = 0
        with_rgb = 0
        with_family = 0
        unique_names: Set[str] = set()
        unique_families: Set[str] = set()

        for entry in self.iter_all():
            total += 1
            by_source[entry.source.value] += 1
            unique_names.add(entry.name)

            if entry.munsell:
                with_munsell += 1
            if entry.rgb_hex or entry.rgb_decimal:
                with_rgb += 1
            if entry.family:
                with_family += 1
                unique_families.add(entry.family)

        return {
            'total_entries': total,
            'unique_names': len(unique_names),
            'by_source': dict(by_source),
            'with_munsell': with_munsell,
            'with_rgb': with_rgb,
            'with_family': with_family,
            'unique_families': sorted(unique_families),
        }

    def to_list(self, unique: bool = True, **filters) -> List[ColorEntry]:
        """
        Get all entries as a list.

        Args:
            unique: If True, deduplicate by name
            **filters: Filter arguments (see iter_filtered)

        Returns:
            List of ColorEntry objects
        """
        if filters:
            entries = list(self.iter_filtered(**filters))
        elif unique:
            entries = list(self.iter_unique())
        else:
            entries = list(self.iter_all())
        return entries


def aggregate_sources(*names: str, root: Optional[Path] = None) -> DataAggregator:
    """
    Convenience function to create an aggregator with specified sources.

    Args:
        *names: Source names to aggregate
        root: Optional custom root path

    Returns:
        Configured DataAggregator

    Example:
        agg = aggregate_sources('centore', 'xkcd', 'meodai')
        for entry in agg.iter_unique():
            print(entry.name)
    """
    agg = DataAggregator(root)
    agg.add_sources(*names)
    return agg


def aggregate_surface_sources(root: Optional[Path] = None) -> DataAggregator:
    """
    Aggregate all surface color sources (have Munsell coordinates).

    Returns:
        DataAggregator configured for surface color analysis
    """
    return aggregate_sources('centore', 'surface', root=root)


def aggregate_screen_sources(root: Optional[Path] = None) -> DataAggregator:
    """
    Aggregate all screen color sources (RGB only).

    Returns:
        DataAggregator configured for screen color analysis
    """
    return aggregate_sources('xkcd', 'meodai', 'colorhexa', 'wikipedia', root=root)


def aggregate_all(root: Optional[Path] = None) -> DataAggregator:
    """
    Aggregate all available sources.

    Returns:
        DataAggregator with all sources
    """
    agg = DataAggregator(root)
    for name in SOURCE_REGISTRY.keys():
        try:
            source = get_source(name, root)
            if source.exists():
                agg.add_source(source)
        except Exception:
            pass  # Skip sources that can't be loaded
    return agg
