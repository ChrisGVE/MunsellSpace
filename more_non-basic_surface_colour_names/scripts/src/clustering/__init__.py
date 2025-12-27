"""
Color family clustering module.

Phase C of the color name pipeline: Multi-method family clustering.
"""

from .family_clustering import (
    FamilyClustering,
    ColorPoint,
    ColorFamily,
)

__all__ = [
    'FamilyClustering',
    'ColorPoint',
    'ColorFamily',
]
