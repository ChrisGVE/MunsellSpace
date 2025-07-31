#!/usr/bin/env python3
"""
ISCC-NBS Polygon Validation Script

This script validates the integrity and coverage of ISCC-NBS color polygons by checking:
1. All polygon edges form only 90° or 270° angles (right angles only)
2. Complete color space coverage with no gaps
3. No polygon intersections or overlaps
4. Proper polygon closure (last point connects to first)
5. Valid coordinate ranges for hue, value, and chroma

Author: MunsellSpace Contributors
License: MIT
"""

import csv
import math
from collections import defaultdict
from typing import List, Tuple, Dict, Set, Optional
from dataclasses import dataclass


@dataclass
class MunsellPoint:
    """Represents a point in Munsell color space"""
    hue1: str
    hue2: str  
    chroma: float
    value: float
    
    def __post_init__(self):
        # Handle >15 chroma notation
        if isinstance(self.chroma, str) and self.chroma.startswith('>'):
            self.chroma = float(self.chroma[1:])
            self.is_open_chroma = True
        else:
            self.chroma = float(self.chroma)
            self.is_open_chroma = False


@dataclass 
class IsccNbsPolygon:
    """Represents an ISCC-NBS color polygon"""
    color_number: int
    descriptor: str
    color_name: str
    modifier: Optional[str]
    revised_color: str
    points: List[MunsellPoint]
    
    def __post_init__(self):
        # Sort points by point identifier to ensure correct polygon ordering
        self.points.sort(key=lambda p: (p.hue1, p.hue2, p.chroma, p.value))


def parse_hue_to_degrees(hue: str) -> float:
    """Convert Munsell hue notation to degrees (0-360)"""
    hue_families = {
        'R': 0, 'YR': 36, 'Y': 72, 'GY': 108, 'G': 144,
        'BG': 180, 'B': 216, 'PB': 252, 'P': 288, 'RP': 324
    }
    
    # Parse hue like "5R", "10YR", etc.
    if len(hue) < 2:
        raise ValueError(f"Invalid hue notation: {hue}")
    
    # Extract number and family
    family = hue[-2:] if hue[-2:] in hue_families else hue[-1:]
    number_str = hue[:-len(family)]
    
    if not number_str:
        number = 5  # Default to 5 if no number specified
    else:
        number = float(number_str)
    
    if family not in hue_families:
        raise ValueError(f"Unknown hue family: {family}")
    
    base_angle = hue_families[family]
    # Each hue step is 3.6 degrees (36/10)
    angle = base_angle + (number - 5) * 3.6
    
    # Normalize to 0-360 range
    return angle % 360


def get_iscc_nbs_hue_slices() -> List[Tuple[str, float, float]]:
    """Get the 30 ISCC-NBS hue slices as organized ranges"""
    # The 30 official ISCC-NBS hue ranges
    official_ranges = [
        "1R-4R", "4R-6R", "6R-7R", "7R-8R", "8R-9R", "9R-1YR", 
        "1YR-2YR", "2YR-3YR", "3YR-5YR", "5YR-7YR", "7YR-8YR", "8YR-1Y",
        "1Y-4Y", "4Y-7Y", "7Y-9Y", "9Y-2GY", "2GY-4GY", "4GY-8GY",
        "8GY-3G", "3G-9G", "9G-10BG", "10BG-9B", "9B-5PB", "5PB-6PB",
        "6PB-7PB", "7PB-9PB", "9PB-3P", "3P-9P", "9P-3RP", "3RP-9RP"
    ]
    
    slices = []
    
    for range_str in official_ranges:
        hue1_str, hue2_str = range_str.split('-')
        
        # Convert to degrees
        start_deg = parse_hue_to_degrees(hue1_str)
        end_deg = parse_hue_to_degrees(hue2_str)
        
        # Handle wraparound (e.g., 9RP-3R where end < start)
        if end_deg <= start_deg:
            end_deg += 360
            
        slices.append((range_str, start_deg, end_deg))
    
    return slices


def polygon_intersects_hue_slice(polygon: IsccNbsPolygon, slice_start: float, slice_end: float) -> bool:
    """Check if a polygon's hue range intersects with a hue slice"""
    if not polygon.points:
        return False
    
    # Get polygon's hue range
    hue1 = polygon.points[0].hue1
    hue2 = polygon.points[0].hue2
    
    poly_start = parse_hue_to_degrees(hue1)
    poly_end = parse_hue_to_degrees(hue2)
    
    # Handle wraparound
    if poly_end <= poly_start:
        poly_end += 360
    
    # Adjust slice end for comparison if needed
    adjusted_slice_end = slice_end
    if slice_end > 360:
        adjusted_slice_end = slice_end
    
    # Check for intersection
    return not (poly_end <= slice_start or poly_start >= adjusted_slice_end)


def calculate_interior_angle(p1: Tuple[float, float], p2: Tuple[float, float], p3: Tuple[float, float]) -> float:
    """Calculate the interior angle at p2 in polygon traversal p1->p2->p3
    Returns angle in degrees (0-360°) where:
    - 90° = convex right angle
    - 270° = concave right angle
    """
    # Vector from p2 to p1
    v1 = (p1[0] - p2[0], p1[1] - p2[1])
    # Vector from p2 to p3  
    v2 = (p3[0] - p2[0], p3[1] - p2[1])
    
    if v1 == (0, 0) or v2 == (0, 0):
        return 0
    
    # Use atan2 to get full 360° range with proper orientation
    angle1 = math.atan2(v1[1], v1[0])
    angle2 = math.atan2(v2[1], v2[0])
    
    # Calculate interior angle (clockwise from v1 to v2)
    interior_angle = angle2 - angle1
    
    # Normalize to 0-360° range
    if interior_angle < 0:
        interior_angle += 2 * math.pi
    
    return math.degrees(interior_angle)


def order_polygon_points(points: List[MunsellPoint]) -> List[MunsellPoint]:
    """Order polygon points for proper counter-clockwise traversal"""
    if len(points) < 3:
        return points
    
    # Convert to (value, chroma) coordinates for geometry calculations
    coords = [(p.value, p.chroma) for p in points]
    
    # Find centroid of the polygon
    centroid_v = sum(c[0] for c in coords) / len(coords)
    centroid_c = sum(c[1] for c in coords) / len(coords)
    centroid = (centroid_v, centroid_c)
    
    # Calculate polar angle from centroid to each point
    def polar_angle(coord):
        return math.atan2(coord[1] - centroid[1], coord[0] - centroid[0])
    
    # Sort points by polar angle (counter-clockwise)
    point_angles = [(point, polar_angle((point.value, point.chroma))) for point in points]
    point_angles.sort(key=lambda x: x[1])
    
    return [point for point, angle in point_angles]


def load_iscc_nbs_data(filepath: str) -> Dict[str, IsccNbsPolygon]:
    """Load ISCC-NBS polygon data from CSV file, separating groups"""
    polygons = {}
    
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            color_number = int(row['color_number'])
            points_id = row['points']  # This identifies the group (e.g., "1.1", "1.2", "2.1", etc.)
            
            # Extract the polygon group number from points_id (e.g., "1.1" -> group "1")
            polygon_group = points_id.split('.')[0]
            
            # Create unique polygon ID combining color number and group
            polygon_id = f"{color_number}.{polygon_group}"  # e.g., "7.1", "7.2"
            
            # Handle >15 chroma notation (now should be 50)
            chroma_str = row['chroma']
            if chroma_str.startswith('>'):
                chroma = float(chroma_str[1:])  # Should now be 50
                is_open_chroma = True
            else:
                chroma = float(chroma_str)
                is_open_chroma = False
            
            point = MunsellPoint(
                hue1=row['hue1'],
                hue2=row['hue2'],
                chroma=chroma,
                value=float(row['value'])
            )
            point.is_open_chroma = is_open_chroma
            
            # Create polygon group if it doesn't exist
            if polygon_id not in polygons:
                polygons[polygon_id] = IsccNbsPolygon(
                    color_number=color_number,
                    descriptor=row['iscc-nbs-descriptor'],
                    color_name=row['iscc-nbs-color'],
                    modifier=row['iscc-nbs-modifier'] if row['iscc-nbs-modifier'] else None,
                    revised_color=row['revised-color'],
                    points=[]
                )
                # Store the original polygon group number for reporting
                polygons[polygon_id].original_polygon_number = polygon_group
            
            polygons[polygon_id].points.append(point)
    
    # Keep original point order from CSV data - it already represents proper polygon traversal
    # The CSV data points are ordered correctly for traversing the polygon boundary
    for polygon in polygons.values():
        # No sorting needed - the CSV point order (by group, then by point number) is correct
        pass
    
    return polygons


def validate_right_angles(polygon: IsccNbsPolygon, polygon_id: str) -> List[str]:
    """Validate that all polygon angles are 90° or 270° in value/chroma space"""
    errors = []
    
    if len(polygon.points) < 3:
        errors.append(f"Polygon {polygon_id} ({polygon.descriptor}) has insufficient points ({len(polygon.points)})")
        return errors
    
    # Verify all points have the same hue range (they should within a group)
    hue_ranges = set((p.hue1, p.hue2) for p in polygon.points)
    if len(hue_ranges) > 1:
        errors.append(f"Polygon {polygon_id} ({polygon.descriptor}) has inconsistent hue ranges: {hue_ranges}")
        return errors
    
    # Extract value/chroma coordinates (2D space within the hue range)
    coordinates = [(point.value, point.chroma) for point in polygon.points]
    
    # Check angles at each vertex
    n = len(coordinates)
    for i in range(n):
        p1 = coordinates[(i - 1) % n]  # Previous point
        p2 = coordinates[i]            # Current point  
        p3 = coordinates[(i + 1) % n]  # Next point
        
        angle = calculate_interior_angle(p1, p2, p3)
        
        # Check if angle is exactly 90° or 270° (convex or concave right angles)
        # Round to nearest degree to handle floating point precision
        rounded_angle = round(angle)
        is_right_angle = (rounded_angle == 90 or rounded_angle == 270)
        
        if not is_right_angle:
            errors.append(f"Polygon {polygon_id} ({polygon.descriptor}) has non-right angle "
                         f"at point {i} (V:{p2[0]}, C:{p2[1]}): {angle:.1f}° (expected exactly 90° or 270°)")
    
    return errors


def validate_coordinate_ranges(polygon: IsccNbsPolygon, polygon_id: str) -> List[str]:
    """Validate that all coordinates are within valid Munsell ranges"""
    errors = []
    
    valid_hues = {'R', 'YR', 'Y', 'GY', 'G', 'BG', 'B', 'PB', 'P', 'RP'}
    
    for i, point in enumerate(polygon.points):
        # Validate hue notation
        try:
            hue1_family = point.hue1[-2:] if point.hue1[-2:] in valid_hues else point.hue1[-1:]
            hue2_family = point.hue2[-2:] if point.hue2[-2:] in valid_hues else point.hue2[-1:]
            
            if hue1_family not in valid_hues:
                errors.append(f"Color {polygon.color_number} polygon {polygon_id} point {i+1}: invalid hue1 '{point.hue1}'")
            if hue2_family not in valid_hues:
                errors.append(f"Color {polygon.color_number} polygon {polygon_id} point {i+1}: invalid hue2 '{point.hue2}'")
                
            # Parse hue values to check range
            parse_hue_to_degrees(point.hue1)
            parse_hue_to_degrees(point.hue2)
            
        except ValueError as e:
            errors.append(f"Polygon {polygon.color_number} point {i}: {e}")
        
        # Validate value range (0-10)
        if not (0 <= point.value <= 10):
            errors.append(f"Polygon {polygon_id} point {i}: "
                         f"value {point.value} outside range [0, 10]")
        
        # Validate chroma range (≥0)
        if point.chroma < 0:
            errors.append(f"Polygon {polygon_id} point {i}: "
                         f"negative chroma {point.chroma}")
        
        # Check if chroma values >15 are now properly set to 50
        if point.is_open_chroma and point.chroma != 50:
            errors.append(f"Color {polygon.color_number} polygon {polygon_id} point {i+1}: "
                         f"open chroma should be 50, found {point.chroma}")
        
        # Check that chroma values are integers when chroma >= 3
        if point.chroma >= 3 and point.chroma != int(point.chroma):
            errors.append(f"Color {polygon.color_number} polygon {polygon_id} point {i+1}: "
                         f"chroma should be integer when chroma >= 3, found chroma {point.chroma}")
    
    return errors


def check_data_consistency(polygons: Dict[str, IsccNbsPolygon]) -> List[str]:
    """Check for data consistency issues"""
    errors = []
    
    # Check that we have all 267 color categories (count unique color numbers)
    color_numbers = set(p.color_number for p in polygons.values())
    expected_colors = set(range(1, 268))
    
    missing_colors = expected_colors - color_numbers
    extra_colors = color_numbers - expected_colors
    
    if missing_colors:
        errors.append(f"Missing color categories: {sorted(missing_colors)}")
    
    if extra_colors:
        errors.append(f"Unexpected color categories: {sorted(extra_colors)}")
    
    # Check for polygons with too few points
    for polygon_id, polygon in polygons.items():
        if len(polygon.points) < 3:
            errors.append(f"Polygon {polygon_id} ({polygon.descriptor}) has only {len(polygon.points)} points - need at least 3")
    
    # Check for duplicate point definitions within each polygon group
    for polygon_id, polygon in polygons.items():
        seen_points = set()
        for point in polygon.points:
            point_tuple = (point.hue1, point.hue2, point.chroma, point.value)
            if point_tuple in seen_points:
                errors.append(f"Polygon {polygon_id} ({polygon.descriptor}) has duplicate point: {point_tuple}")
            seen_points.add(point_tuple)
    
    return errors


def analyze_polygon_groups(polygons: Dict[str, IsccNbsPolygon]) -> List[str]:
    """Analyze polygon groups for each color category"""
    errors = []
    
    # Group polygons by color number
    color_groups = defaultdict(list)
    for polygon_id, polygon in polygons.items():
        color_groups[polygon.color_number].append((polygon_id, polygon))
    
    # Analyze each color category
    for color_number, group_list in color_groups.items():
        if len(group_list) == 1:
            # Single polygon - check that it has reasonable complexity
            polygon_id, polygon = group_list[0]
            if len(polygon.points) > 8:
                errors.append(f"Color {color_number} has single polygon {polygon_id} with {len(polygon.points)} points - consider if this should be split into groups")
        else:
            # Multiple polygons - check hue continuity between groups
            group_list.sort(key=lambda x: x[0])  # Sort by polygon_id
            for i in range(len(group_list) - 1):
                curr_id, curr_polygon = group_list[i]
                next_id, next_polygon = group_list[i + 1]
                
                # Check if adjacent groups have connecting hue ranges
                curr_hue2 = curr_polygon.points[0].hue2
                next_hue1 = next_polygon.points[0].hue1
                
                if curr_hue2 != next_hue1:
                    errors.append(f"Color {color_number}: Gap between polygon {curr_id} (ends at {curr_hue2}) and {next_id} (starts at {next_hue1})")
    
    return errors


def polygon_to_edges(points: List[MunsellPoint]) -> List[Tuple[Tuple[float, float], Tuple[float, float]]]:
    """Convert polygon points to list of edges (segments) in value/chroma space"""
    # Sort points to form proper polygon (assuming rectangular or near-rectangular shapes)
    # For complex polygons, we need to maintain the correct order from the CSV
    coords = [(p.value, p.chroma) for p in points]
    
    # Create edges by connecting consecutive points (and last to first)
    edges = []
    for i in range(len(coords)):
        start = coords[i]
        end = coords[(i + 1) % len(coords)]
        edges.append((start, end))
    
    return edges


def segments_intersect_interior(seg1: Tuple[Tuple[float, float], Tuple[float, float]], 
                               seg2: Tuple[Tuple[float, float], Tuple[float, float]]) -> bool:
    """Check if two line segments intersect in their interiors (not just at endpoints)"""
    (x1, y1), (x2, y2) = seg1
    (x3, y3), (x4, y4) = seg2
    
    # Calculate direction vectors
    d1 = (x2 - x1, y2 - y1)
    d2 = (x4 - x3, y4 - y3)
    
    # Calculate cross product for orientation
    def cross_product(v1, v2):
        return v1[0] * v2[1] - v1[1] * v2[0]
    
    # Check if segments are parallel
    cross = cross_product(d1, d2)
    if abs(cross) < 1e-10:  # Parallel or collinear
        return False
    
    # Calculate intersection point parameters
    dx = x3 - x1
    dy = y3 - y1
    
    t = cross_product((dx, dy), d2) / cross
    u = cross_product((dx, dy), d1) / cross
    
    # Check if intersection is in interior of both segments (not at endpoints)
    tolerance = 1e-6  # Small tolerance to exclude endpoint touching
    return (tolerance < t < 1 - tolerance) and (tolerance < u < 1 - tolerance)


def point_in_polygon(point: Tuple[float, float], polygon_points: List[Tuple[float, float]]) -> bool:
    """Check if a point is inside a polygon using ray casting algorithm"""
    x, y = point
    n = len(polygon_points)
    inside = False
    
    p1x, p1y = polygon_points[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon_points[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    
    return inside


def polygon_area_intersection(poly1: IsccNbsPolygon, poly2: IsccNbsPolygon) -> Tuple[bool, str]:
    """Check if two polygons have overlapping interior areas (not just shared boundaries)"""
    # Convert to coordinate lists
    coords1 = [(p.value, p.chroma) for p in poly1.points]
    coords2 = [(p.value, p.chroma) for p in poly2.points]
    
    # Check if any vertex of polygon1 is strictly inside polygon2
    interior_points = []
    for point in coords1:
        if point_in_polygon(point, coords2):
            interior_points.append(point)
    
    # Check if any vertex of polygon2 is strictly inside polygon1  
    for point in coords2:
        if point_in_polygon(point, coords1):
            interior_points.append(point)
    
    # If no interior points found, there's no area overlap
    if not interior_points:
        return False, ""
    
    # Calculate average location of interior overlap
    avg_v = sum(point[0] for point in interior_points) / len(interior_points)
    avg_c = sum(point[1] for point in interior_points) / len(interior_points)
    
    # Estimate overlap region
    v_values = [point[0] for point in interior_points]
    c_values = [point[1] for point in interior_points]
    
    v_spread = max(v_values) - min(v_values) if len(v_values) > 1 else 0
    c_spread = max(c_values) - min(c_values) if len(c_values) > 1 else 0
    
    if v_spread > c_spread:
        primary_dim = "VALUE"
        primary_range = f"{min(v_values):.1f}-{max(v_values):.1f}" if len(v_values) > 1 else f"around {avg_v:.1f}"
        secondary_dim = "chroma"
        secondary_range = f"{min(c_values):.1f}-{max(c_values):.1f}" if len(c_values) > 1 else f"around {avg_c:.1f}"
    else:
        primary_dim = "CHROMA"
        primary_range = f"{min(c_values):.1f}-{max(c_values):.1f}" if len(c_values) > 1 else f"around {avg_c:.1f}"
        secondary_dim = "value"  
        secondary_range = f"{min(v_values):.1f}-{max(v_values):.1f}" if len(v_values) > 1 else f"around {avg_v:.1f}"
    
    intersection_details = f"area overlap primarily in {primary_dim} {primary_range} (also {secondary_dim} {secondary_range})"
    
    return True, intersection_details


def rectangle_from_points(points: List[MunsellPoint]) -> Tuple[float, float, float, float]:
    """Extract rectangle bounds from points (min_value, max_value, min_chroma, max_chroma)"""
    values = [p.value for p in points]
    chromas = [p.chroma for p in points]
    return (min(values), max(values), min(chromas), max(chromas))


def rectangles_intersect_interior(rect1: Tuple[float, float, float, float], 
                                 rect2: Tuple[float, float, float, float]) -> bool:
    """Check if two rectangles have interior intersection (not just touching edges)"""
    min_v1, max_v1, min_c1, max_c1 = rect1
    min_v2, max_v2, min_c2, max_c2 = rect2
    
    # No interior intersection if completely separated or just touching
    if max_v1 <= min_v2 or max_v2 <= min_v1:
        return False
    if max_c1 <= min_c2 or max_c2 <= min_c1:
        return False
    
    return True


def polygons_intersect_interior(poly1: IsccNbsPolygon, poly2: IsccNbsPolygon) -> bool:
    """Check if two polygons have true interior intersection (not just shared boundaries)"""
    # Extract coordinates from both polygons
    coords1 = [(p.value, p.chroma) for p in poly1.points]
    coords2 = [(p.value, p.chroma) for p in poly2.points]
    
    # First check: if bounding rectangles don't overlap, no intersection possible
    rect1 = rectangle_from_points(poly1.points)
    rect2 = rectangle_from_points(poly2.points)
    if not rectangles_intersect_interior(rect1, rect2):
        return False
    
    # Use the Separating Axes Theorem for convex polygons
    # For rectilinear polygons (only horizontal/vertical edges), we can use simpler logic
    
    # Check if any vertex of poly1 is strictly inside poly2
    for point in coords1:
        if point_in_polygon_interior(point, coords2):
            return True
    
    # Check if any vertex of poly2 is strictly inside poly1  
    for point in coords2:
        if point_in_polygon_interior(point, coords1):
            return True
    
    # Check for edge intersections (excluding shared boundaries)
    if polygons_have_crossing_edges(coords1, coords2):
        return True
    
    return False


def point_in_polygon_interior(point: Tuple[float, float], polygon: List[Tuple[float, float]]) -> bool:
    """Check if point is strictly inside polygon (not on boundary)"""
    x, y = point
    n = len(polygon)
    inside = False
    
    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]
        
        # Check if point is exactly on an edge (boundary case)
        if point_on_edge(point, (p1x, p1y), (p2x, p2y)):
            return False  # On boundary, not interior
        
        # Ray casting algorithm for interior test
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    
    return inside


def point_on_edge(point: Tuple[float, float], edge_start: Tuple[float, float], edge_end: Tuple[float, float]) -> bool:
    """Check if point lies exactly on the edge between edge_start and edge_end"""
    px, py = point
    x1, y1 = edge_start
    x2, y2 = edge_end
    
    # For rectilinear polygons, edges are either horizontal or vertical
    epsilon = 1e-10
    
    if abs(x1 - x2) < epsilon:  # Vertical edge
        return (abs(px - x1) < epsilon and 
                min(y1, y2) <= py <= max(y1, y2))
    elif abs(y1 - y2) < epsilon:  # Horizontal edge
        return (abs(py - y1) < epsilon and 
                min(x1, x2) <= px <= max(x1, x2))
    
    return False


def polygons_have_crossing_edges(coords1: List[Tuple[float, float]], coords2: List[Tuple[float, float]]) -> bool:
    """Check if polygons have edges that cross each other (not just touch at endpoints)"""
    # For rectilinear polygons, we only need to check horizontal-vertical crossings
    
    for i in range(len(coords1)):
        edge1_start = coords1[i]
        edge1_end = coords1[(i + 1) % len(coords1)]
        
        for j in range(len(coords2)):
            edge2_start = coords2[j]
            edge2_end = coords2[(j + 1) % len(coords2)]
            
            if edges_cross_interior(edge1_start, edge1_end, edge2_start, edge2_end):
                return True
    
    return False


def edges_cross_interior(e1_start: Tuple[float, float], e1_end: Tuple[float, float],
                        e2_start: Tuple[float, float], e2_end: Tuple[float, float]) -> bool:
    """Check if two edges cross in their interiors (not at endpoints)"""
    x1, y1 = e1_start
    x2, y2 = e1_end
    x3, y3 = e2_start
    x4, y4 = e2_end
    
    epsilon = 1e-10
    
    # For rectilinear polygons: check horizontal-vertical crossings
    # Edge 1 is vertical, Edge 2 is horizontal
    if (abs(x1 - x2) < epsilon and abs(y3 - y4) < epsilon):
        # Check if they cross in interior
        if (min(y1, y2) < y3 < max(y1, y2) and 
            min(x3, x4) < x1 < max(x3, x4)):
            return True
    
    # Edge 1 is horizontal, Edge 2 is vertical  
    if (abs(y1 - y2) < epsilon and abs(x3 - x4) < epsilon):
        # Check if they cross in interior
        if (min(x1, x2) < x3 < max(x1, x2) and 
            min(y3, y4) < y1 < max(y3, y4)):
            return True
    
    return False


def check_gaps_and_intersections(polygons: Dict[str, IsccNbsPolygon]) -> List[str]:
    """Check for gaps and intersections in color space coverage using organized hue slices"""
    errors = []
    
    # Get the 30 organized ISCC-NBS hue slices
    hue_slices = get_iscc_nbs_hue_slices()
    
    # Organize polygons by hue slices instead of raw hue ranges
    slice_groups = {}
    
    for slice_name, slice_start, slice_end in hue_slices:
        slice_groups[slice_name] = []
        
        # Find all polygons that intersect with this hue slice
        for polygon_id, polygon in polygons.items():
            if polygon_intersects_hue_slice(polygon, slice_start, slice_end):
                # Get rectangle bounds
                rect = rectangle_from_points(polygon.points)
                slice_groups[slice_name].append((polygon_id, polygon, rect))
        
        # Sort polygons within each slice by value, then chroma for consistent analysis
        slice_groups[slice_name].sort(key=lambda x: (x[2][0], x[2][2]))  # Sort by min_value, min_chroma
    
    # Check for intersections within each hue slice  
    intersection_count = 0
    intersection_results = []
    
    for slice_name, group_rects in slice_groups.items():
        if len(group_rects) < 2:
            continue
            
        # Check for intersections within this slice
        for i in range(len(group_rects)):
            for j in range(i + 1, len(group_rects)):
                polygon_id1, polygon1, rect1 = group_rects[i]
                polygon_id2, polygon2, rect2 = group_rects[j]
                
                # Check if polygons have true interior intersection (not just shared boundaries)
                if polygons_intersect_interior(polygon1, polygon2):
                    intersection_count += 1
                    intersection_results.append(
                        f"INTERSECTION #{intersection_count}:"
                    )
                    intersection_results.append(
                        f"    Color {polygon1.color_number} polygon {polygon1.original_polygon_number} ({polygon1.descriptor})"
                    )
                    intersection_results.append(
                        f"    Color {polygon2.color_number} polygon {polygon2.original_polygon_number} ({polygon2.descriptor})"
                    )
                    intersection_results.append(
                        f"    Hue slice {slice_name} - overlap region: V:{max(rect1[0], rect2[0]):.1f}-{min(rect1[1], rect2[1]):.1f}, C:{max(rect1[2], rect2[2]):.1f}-{min(rect1[3], rect2[3]):.1f}"
                    )
    
    # Add intersection results
    errors.extend(intersection_results)
    
    # Check for gaps within each organized hue slice - ACCOUNT FOR INTERMEDIATE POLYGONS
    # Only check gaps between polygons that have the SAME hue range (not spanning multiple slices)
    gap_results = []
    gap_count = 0
    
    for slice_name, group_rects in slice_groups.items():
        if len(group_rects) < 2:
            continue
        
        # Filter to only include polygons whose primary hue range matches this slice
        slice_native_polygons = []
        for polygon_id, polygon, rect in group_rects:
            hue1 = polygon.points[0].hue1
            hue2 = polygon.points[0].hue2
            poly_range = f"{hue1}-{hue2}"
            
            # Only include if this polygon's native range closely matches the slice
            # (avoid neutral colors that span all slices)
            if slice_name == poly_range or slice_name in poly_range:
                slice_native_polygons.append((polygon_id, polygon, rect))
        
        if len(slice_native_polygons) < 2:
            continue
        
        # For each pair of native polygons within this hue slice, check if there's a gap that isn't filled by other polygons
        for i in range(len(slice_native_polygons)):
            for j in range(i + 1, len(slice_native_polygons)):
                id1, poly1, rect1 = slice_native_polygons[i]
                id2, poly2, rect2 = slice_native_polygons[j]
                
                # Check for potential gap in value dimension
                gap_in_value = False
                gap_in_chroma = False
                
                # Value gap: check if there's space between max of one and min of other
                if rect1[1] < rect2[0] - 0.1:  # rect1 max_value < rect2 min_value (with tolerance)
                    gap_in_value = True
                    gap_min_v, gap_max_v = rect1[1], rect2[0]
                    gap_min_c = max(rect1[2], rect2[2])  # overlapping chroma range
                    gap_max_c = min(rect1[3], rect2[3])
                elif rect2[1] < rect1[0] - 0.1:  # rect2 max_value < rect1 min_value (with tolerance)
                    gap_in_value = True
                    gap_min_v, gap_max_v = rect2[1], rect1[0]
                    gap_min_c = max(rect1[2], rect2[2])  # overlapping chroma range
                    gap_max_c = min(rect1[3], rect2[3])
                
                # Chroma gap: check if there's space between max of one and min of other
                if rect1[3] < rect2[2] - 0.1:  # rect1 max_chroma < rect2 min_chroma (with tolerance)
                    # Only if they overlap in value
                    value_overlap_start = max(rect1[0], rect2[0])
                    value_overlap_end = min(rect1[1], rect2[1])
                    if value_overlap_start < value_overlap_end:
                        gap_in_chroma = True
                        gap_min_c, gap_max_c = rect1[3], rect2[2]
                        gap_min_v, gap_max_v = value_overlap_start, value_overlap_end
                elif rect2[3] < rect1[2] - 0.1:  # rect2 max_chroma < rect1 min_chroma (with tolerance)
                    # Only if they overlap in value
                    value_overlap_start = max(rect1[0], rect2[0])
                    value_overlap_end = min(rect1[1], rect2[1])
                    if value_overlap_start < value_overlap_end:
                        gap_in_chroma = True
                        gap_min_c, gap_max_c = rect2[3], rect1[2]
                        gap_min_v, gap_max_v = value_overlap_start, value_overlap_end
                
                # If we found a potential gap, check if it's filled by other polygons
                if gap_in_value or gap_in_chroma:
                    gap_filled = False
                    
                    # Check ALL polygons in this hue slice (including spanning ones) to see if any fill the gap
                    for id_k, poly_k, rect_k in group_rects:
                        if id_k != id1 and id_k != id2:  # Don't check the same two polygons
                            # Check if this polygon overlaps with the gap region
                            if (rect_k[0] <= gap_max_v and rect_k[1] >= gap_min_v and  # value overlap
                                rect_k[2] <= gap_max_c and rect_k[3] >= gap_min_c):    # chroma overlap
                                gap_filled = True
                                break
                    
                    # If gap is not filled by any other polygon, report it
                    if not gap_filled:
                        gap_count += 1
                        orig_poly1 = getattr(poly1, 'original_polygon_number', 'unknown')
                        orig_poly2 = getattr(poly2, 'original_polygon_number', 'unknown')
                        
                        gap_center_v = (gap_min_v + gap_max_v) / 2
                        gap_center_c = (gap_min_c + gap_max_c) / 2
                        gap_size_v = gap_max_v - gap_min_v
                        gap_size_c = gap_max_c - gap_min_c
                        
                        if gap_in_value:
                            gap_location = f"primarily in VALUE at {gap_center_v:.1f} (gap size: {gap_size_v:.1f}), chroma range: {gap_min_c:.1f}-{gap_max_c:.1f}"
                        else:
                            gap_location = f"primarily in CHROMA at {gap_center_c:.1f} (gap size: {gap_size_c:.1f}), value range: {gap_min_v:.1f}-{gap_max_v:.1f}"
                        
                        gap_results.append(f"GAP #{gap_count}:")
                        gap_results.append(f"    Color {poly1.color_number} polygon {orig_poly1} ({poly1.descriptor})")
                        gap_results.append(f"    Color {poly2.color_number} polygon {orig_poly2} ({poly2.descriptor})")
                        gap_results.append(f"    Hue slice {slice_name} - {gap_location}")
    
    # Add all gap results
    errors.extend(gap_results)
    
    # Summary statistics with new organized slice structure
    total_hue_slices = len(slice_groups)
    non_empty_slices = len([s for s in slice_groups.values() if s])
    total_polygon_assignments = sum(len(s) for s in slice_groups.values())
    
    errors.append(f"COVERAGE ANALYSIS: Found {total_hue_slices} ISCC-NBS hue slices ({non_empty_slices} non-empty)")
    errors.append(f"INTERSECTION ANALYSIS: Found {intersection_count} intersections")
    errors.append(f"GAP ANALYSIS: Found {gap_count} potential gaps")
    errors.append(f"ORGANIZATION: {total_polygon_assignments} polygon-to-slice assignments from {len(polygons)} total polygons")
    
    return errors


def analyze_color_space_coverage(polygons: Dict[str, IsccNbsPolygon]) -> List[str]:
    """Analyze overall color space coverage statistics"""
    errors = []
    
    # Collect all rectangles
    all_rects = []
    hue_ranges = set()
    
    for polygon_id, polygon in polygons.items():
        if not polygon.points:
            continue
            
        hue1 = polygon.points[0].hue1
        hue2 = polygon.points[0].hue2
        hue_ranges.add(f"{hue1}-{hue2}")
        
        rect = rectangle_from_points(polygon.points)
        all_rects.append(rect)
    
    if not all_rects:
        errors.append("No valid rectangles found for coverage analysis")
        return errors
    
    # Calculate overall bounds
    all_min_values = [rect[0] for rect in all_rects]
    all_max_values = [rect[1] for rect in all_rects]
    all_min_chromas = [rect[2] for rect in all_rects]
    all_max_chromas = [rect[3] for rect in all_rects]
    
    overall_min_value = min(all_min_values)
    overall_max_value = max(all_max_values)
    overall_min_chroma = min(all_min_chromas)
    overall_max_chroma = max(all_max_chromas)
    
    errors.append(f"VALUE RANGE: {overall_min_value} to {overall_max_value}")
    errors.append(f"CHROMA RANGE: {overall_min_chroma} to {overall_max_chroma}")
    errors.append(f"DISTINCT HUE RANGES: {len(hue_ranges)}")
    
    # Check if we cover expected Munsell ranges
    if overall_min_value > 0.5:
        errors.append(f"WARNING: Minimum value {overall_min_value} may not cover dark colors properly")
    if overall_max_value < 9.5:
        errors.append(f"WARNING: Maximum value {overall_max_value} may not cover light colors properly")
    if overall_min_chroma > 0.5:
        errors.append(f"WARNING: Minimum chroma {overall_min_chroma} may not cover neutral colors properly")
    
    return errors


def generate_validation_report(polygons: Dict[str, IsccNbsPolygon]) -> str:
    """Generate comprehensive validation report"""
    report = []
    report.append("ISCC-NBS Polygon Validation Report (Updated for Polygon Groups)")
    report.append("=" * 65)
    
    # Count unique color categories and total polygon groups
    color_numbers = set(p.color_number for p in polygons.values())
    report.append(f"Total color categories: {len(color_numbers)}")
    report.append(f"Total polygon groups: {len(polygons)}")
    report.append(f"Expected color categories: 267")
    report.append("")
    
    all_errors = []
    
    # 1. Data consistency validation
    report.append("1. DATA CONSISTENCY VALIDATION")
    report.append("-" * 35)
    
    consistency_errors = check_data_consistency(polygons)
    all_errors.extend(consistency_errors)
    
    if not consistency_errors:
        report.append("✓ All basic data consistency checks passed")
    else:
        for error in consistency_errors:
            report.append(f"  - {error}")
    
    # 2. Right angle validation (NEW)
    report.append("")
    report.append("2. RIGHT ANGLE VALIDATION (Value/Chroma Space)")
    report.append("-" * 48)
    
    right_angle_errors = []
    for polygon_id, polygon in polygons.items():
        errors = validate_right_angles(polygon, polygon_id)
        right_angle_errors.extend(errors)
        all_errors.extend(errors)
    
    if not right_angle_errors:
        report.append("✅ ALL POLYGONS HAVE PROPER RIGHT ANGLES")
    else:
        report.append(f"❌ Found {len(right_angle_errors)} right angle violations:")
        for error in right_angle_errors[:10]:  # Show first 10
            report.append(f"  - {error}")
        if len(right_angle_errors) > 10:
            report.append(f"  ... and {len(right_angle_errors) - 10} more angle violations")
    
    # 3. Coordinate validation
    report.append("")
    report.append("3. COORDINATE VALIDATION")
    report.append("-" * 25)
    
    coordinate_errors = []
    for polygon_id, polygon in polygons.items():
        errors = validate_coordinate_ranges(polygon, polygon_id)
        coordinate_errors.extend(errors)
        all_errors.extend(errors)
    
    if not coordinate_errors:
        report.append("✓ All coordinate ranges are valid")
    else:
        report.append(f"Found {len(coordinate_errors)} coordinate validation errors:")
        for error in coordinate_errors[:5]:
            report.append(f"  - {error}")
        if len(coordinate_errors) > 5:
            report.append(f"  ... and {len(coordinate_errors) - 5} more coordinate errors")
    
    # 4. Polygon group analysis (NEW)
    report.append("")
    report.append("4. POLYGON GROUP ANALYSIS")
    report.append("-" * 28)
    
    group_errors = analyze_polygon_groups(polygons)
    all_errors.extend(group_errors)
    
    if not group_errors:
        report.append("✓ All polygon groups appear properly structured")
    else:
        report.append(f"Found {len(group_errors)} group structure issues:")
        for error in group_errors:
            report.append(f"  - {error}")
    
    # 5. Gaps and intersections analysis (NEW)
    report.append("")
    report.append("5. GAPS AND INTERSECTIONS ANALYSIS")
    report.append("-" * 37)
    
    gap_intersection_results = check_gaps_and_intersections(polygons)
    
    # Separate analysis results from actual errors
    analysis_results = [r for r in gap_intersection_results if r.startswith(("COVERAGE ANALYSIS:", "INTERSECTION ANALYSIS:", "GAP ANALYSIS:"))]
    gap_intersection_errors = [r for r in gap_intersection_results if r not in analysis_results]
    
    for result in analysis_results:
        report.append(f"  {result}")
    
    if gap_intersection_errors:
        report.append("")
        report.append("Issues found:")
        for error in gap_intersection_errors:
            report.append(f"  - {error}")
            # Only add actual errors to main error list
            if not error.startswith("... and") and not error.startswith("POTENTIAL"):
                all_errors.append(error)
    
    # 6. Color space coverage analysis (NEW)
    report.append("")
    report.append("6. COLOR SPACE COVERAGE ANALYSIS")
    report.append("-" * 36)
    
    coverage_results = analyze_color_space_coverage(polygons)
    for result in coverage_results:
        if result.startswith("WARNING:"):
            report.append(f"  ⚠️  {result}")
            all_errors.append(result)
        else:
            report.append(f"  {result}")
    
    # 7. Summary
    report.append("")
    report.append("7. VALIDATION SUMMARY")
    report.append("-" * 23)
    
    if not all_errors:
        report.append("✅ ALL VALIDATIONS PASSED")
        report.append("The ISCC-NBS polygon data is correctly structured with proper right angles!")
    else:
        report.append(f"⚠️  FOUND {len(all_errors)} ISSUES TO REVIEW")
        
        # Categorize errors
        angle_issues = [e for e in all_errors if "angle" in e.lower()]
        coord_issues = [e for e in all_errors if "chroma should be 50" in e or "value" in e or "negative chroma" in e]
        consistency_issues = [e for e in all_errors if e not in angle_issues and e not in coord_issues]
        
        if angle_issues:
            report.append(f"  - {len(angle_issues)} right angle violations")
        if coord_issues:
            report.append(f"  - {len(coord_issues)} coordinate issues (including >15 → 50 updates)")  
        if consistency_issues:
            report.append(f"  - {len(consistency_issues)} data consistency issues")
    
    # 8. Statistics
    report.append("")
    report.append("8. DATASET STATISTICS")
    report.append("-" * 22)
    
    total_points = sum(len(p.points) for p in polygons.values())
    avg_points = total_points / len(polygons) if polygons else 0
    
    report.append(f"Total data points: {total_points}")
    report.append(f"Total polygon groups: {len(polygons)}")
    report.append(f"Average points per polygon group: {avg_points:.1f}")
    
    # Point distribution
    point_counts = defaultdict(int)
    for polygon in polygons.values():
        point_counts[len(polygon.points)] += 1
    
    report.append("Points per polygon group distribution:")
    for count in sorted(point_counts.keys()):
        report.append(f"  {count} points: {point_counts[count]} groups")
    
    # Group analysis by color
    color_group_counts = defaultdict(int)
    for polygon in polygons.values():
        color_group_counts[polygon.color_number] += 1
    
    multi_group_colors = [color for color, count in color_group_counts.items() if count > 1]
    if multi_group_colors:
        report.append(f"Colors with multiple polygon groups: {len(multi_group_colors)}")
        report.append(f"  Examples: {sorted(multi_group_colors)[:10]}")
    
    # Special notations
    open_chroma_count = sum(1 for p in polygons.values() 
                           for point in p.points 
                           if hasattr(point, 'is_open_chroma') and point.is_open_chroma)
    if open_chroma_count > 0:
        report.append(f"Open-ended chroma regions (should be 50): {open_chroma_count} points")
    
    return "\n".join(report)


def main():
    """Main validation function"""
    filepath = "ISCC-NBS-Definitions.csv"
    
    try:
        print("Loading ISCC-NBS polygon data...")
        polygons = load_iscc_nbs_data(filepath)
        
        print("Validating polygon integrity and coverage...")
        report = generate_validation_report(polygons)
        
        print(report)
        
        # Save report to file
        with open("iscc_nbs_validation_report.txt", "w") as f:
            f.write(report)
        
        print(f"\nDetailed report saved to: iscc_nbs_validation_report.txt")
        
    except FileNotFoundError:
        print(f"Error: Could not find data file '{filepath}'")
        print("Please ensure the ISCC-NBS-Definitions.csv file is in the current directory.")
    except Exception as e:
        print(f"Error during validation: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()