"""
Data Service Framework

A unified data access layer that ensures:
1. All data is accessed from the canonical source location (datasets/)
2. No copies are ever made - only references and transformations
3. All scripts use a consistent interface
4. Data transformations are lazy and on-demand

Usage:
    from data_service import DataService

    service = DataService()

    # Get all color entries from a specific source
    centore_colors = service.get_source('centore').load()

    # Get aggregated data from multiple sources
    all_colors = service.aggregate(['centore', 'xkcd', 'meodai'])

    # Filter by criteria
    surface_colors = service.aggregate(
        sources=['centore', 'golden', 'williamsburg'],
        color_space='munsell'
    )
"""

from .schema import ColorEntry, ColorSource, CoordinateType
from .sources import (
    BaseDataSource,
    CentoreSource,
    XKCDSource,
    MeodaiSource,
    ColorHexaSource,
    WikipediaSource,
    SurfaceColorsSource,
    WCSSource,
)
from .aggregator import DataAggregator
from .service import DataService

__all__ = [
    # Schema
    'ColorEntry',
    'ColorSource',
    'CoordinateType',
    # Sources
    'BaseDataSource',
    'CentoreSource',
    'XKCDSource',
    'MeodaiSource',
    'ColorHexaSource',
    'WikipediaSource',
    'SurfaceColorsSource',
    'WCSSource',
    # Aggregation
    'DataAggregator',
    # Service
    'DataService',
]
