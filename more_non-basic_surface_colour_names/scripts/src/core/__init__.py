"""
Core module for polyhedron construction using Centore's methodology.

This module contains validated functions for:
- Munsell color coordinate handling (munsell.py)
- Convex hull geometry operations (geometry.py)
- File I/O utilities (io.py)

All functions have been validated against Centore's 30 published polyhedra
with 100% concordance (Track A verification, 2025-12-25).

Reference:
    Centore, P. (2020) "Beige, aqua, fuchsia, etc.: more non-basic surface
    colour names and their Munsell settings." Journal of the American Institute
    for Conservation (JAIC), Vol. 25, pp. 24-54.
"""

from .munsell import MunsellCoord, parse_munsell
from .geometry import compute_inner_hull, compute_filled_solid_centroid

__all__ = [
    'MunsellCoord',
    'parse_munsell',
    'compute_inner_hull',
    'compute_filled_solid_centroid',
]
