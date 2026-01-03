"""
Main Data Service

The single entry point for all data access in the research pipeline.
Ensures:
1. All data comes from the canonical location
2. No copies are made
3. Consistent interface for all scripts
"""

from pathlib import Path
from typing import List, Optional, Dict, Iterator, Union
import json

from .schema import ColorEntry, ColorSource, CoordinateType
from .sources import BaseDataSource, get_source, SOURCE_REGISTRY, DATASETS_ROOT
from .aggregator import (
    DataAggregator,
    aggregate_sources,
    aggregate_surface_sources,
    aggregate_screen_sources,
    aggregate_all,
)


class DataService:
    """
    Unified data service for the color research pipeline.

    Usage:
        from data_service import DataService

        service = DataService()

        # Access a specific source
        centore = service.get_source('centore')
        for entry in centore.iter_entries():
            print(entry.name, entry.munsell)

        # Aggregate multiple sources
        agg = service.aggregate(['centore', 'xkcd'])
        stats = agg.get_statistics()

        # Get surface colors only (Munsell)
        surface = service.surface_colors()

        # Get screen colors only (RGB)
        screen = service.screen_colors()
    """

    def __init__(self, root: Optional[Path] = None):
        """
        Initialize the data service.

        Args:
            root: Custom root path for datasets.
                  Defaults to more_non-basic_surface_colour_names/datasets/
        """
        self.root = root or DATASETS_ROOT
        self._source_cache: Dict[str, BaseDataSource] = {}

    @property
    def datasets_path(self) -> Path:
        """Return the path to the datasets directory."""
        return self.root

    def available_sources(self) -> List[str]:
        """List all registered source names."""
        return list(SOURCE_REGISTRY.keys())

    def source_exists(self, name: str) -> bool:
        """Check if a source's data exists on disk."""
        try:
            source = get_source(name, self.root)
            return source.exists()
        except ValueError:
            return False

    def get_source(self, name: str, use_cache: bool = True) -> BaseDataSource:
        """
        Get a data source by name.

        Args:
            name: Source name (e.g., 'centore', 'xkcd')
            use_cache: Cache source instances

        Returns:
            Data source instance
        """
        if use_cache and name in self._source_cache:
            return self._source_cache[name]

        source = get_source(name, self.root)

        if use_cache:
            self._source_cache[name] = source

        return source

    def aggregate(
        self,
        sources: Union[List[str], str] = None,
        **kwargs
    ) -> DataAggregator:
        """
        Create an aggregator for multiple sources.

        Args:
            sources: List of source names, or 'surface', 'screen', 'all'
            **kwargs: Additional arguments passed to DataAggregator

        Returns:
            Configured DataAggregator
        """
        if sources is None:
            sources = 'all'

        if isinstance(sources, str):
            if sources == 'surface':
                return aggregate_surface_sources(self.root)
            elif sources == 'screen':
                return aggregate_screen_sources(self.root)
            elif sources == 'all':
                return aggregate_all(self.root)
            else:
                # Single source name
                sources = [sources]

        return aggregate_sources(*sources, root=self.root)

    def surface_colors(self) -> DataAggregator:
        """
        Get aggregator for surface color sources.

        These are colors with Munsell coordinates from
        physical color measurement.
        """
        return aggregate_surface_sources(self.root)

    def screen_colors(self) -> DataAggregator:
        """
        Get aggregator for screen color sources.

        These are colors with RGB coordinates from
        screen-based surveys.
        """
        return aggregate_screen_sources(self.root)

    def centore_families(self) -> List[str]:
        """Get list of Centore's 30 color families."""
        return [
            'aqua', 'beige', 'blue', 'brown', 'coral', 'fuchsia',
            'gold', 'gray', 'green', 'lavender', 'lilac', 'magenta',
            'mauve', 'navy', 'orange', 'peach', 'pink', 'purple',
            'red', 'rose', 'rust', 'sand', 'tan', 'taupe', 'teal',
            'turquoise', 'violet', 'white', 'wine', 'yellow'
        ]

    def basic_colors(self) -> List[str]:
        """Get Berlin & Kay basic color terms."""
        return [
            'red', 'yellow', 'green', 'blue', 'black', 'white',
            'gray', 'orange', 'brown', 'pink', 'purple'
        ]

    def non_basic_colors(self) -> List[str]:
        """Get non-basic colors from Centore's 30."""
        basic = set(self.basic_colors())
        return [f for f in self.centore_families() if f not in basic]

    def get_family_entries(
        self,
        family: str,
        sources: Union[List[str], str] = 'all'
    ) -> List[ColorEntry]:
        """
        Get all entries for a specific color family.

        Args:
            family: Family name (e.g., 'coral', 'navy')
            sources: Sources to search

        Returns:
            List of matching entries
        """
        agg = self.aggregate(sources)
        return list(agg.iter_filtered(family=family))

    def get_calibration_subset(self) -> DataAggregator:
        """
        Get the calibration subset for Track B Phase 3.

        Returns non-XKCD, non-Centore sources with
        names matching Centore's 30 families.

        This is the proper calibration set per the pipeline spec.
        """
        agg = DataAggregator(self.root)

        # Add vocabulary sources (not XKCD, not Centore)
        for source_name in ['meodai', 'colorhexa', 'wikipedia']:
            if self.source_exists(source_name):
                agg.add_source(self.get_source(source_name))

        return agg

    def print_status(self):
        """Print status of all data sources."""
        print("Data Service Status")
        print("=" * 50)
        print(f"Datasets root: {self.root}")
        print()

        for name in sorted(self.available_sources()):
            exists = self.source_exists(name)
            status = "OK" if exists else "MISSING"
            print(f"  {name:15} [{status}]")

        print()
        print("Use service.get_source('<name>') to access data")


# Global singleton instance
_default_service: Optional[DataService] = None


def get_data_service(root: Optional[Path] = None) -> DataService:
    """
    Get the global data service instance.

    Args:
        root: Custom root path (only used on first call)

    Returns:
        DataService singleton
    """
    global _default_service
    if _default_service is None or root is not None:
        _default_service = DataService(root)
    return _default_service


# Convenience functions for direct access
def load_source(name: str) -> List[ColorEntry]:
    """Load all entries from a source."""
    return get_data_service().get_source(name).load()


def load_aggregated(
    sources: Union[List[str], str] = 'all',
    unique: bool = True
) -> List[ColorEntry]:
    """Load aggregated entries from multiple sources."""
    return get_data_service().aggregate(sources).to_list(unique=unique)
