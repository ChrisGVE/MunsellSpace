# Polyhedron Construction Methodology

## Summary

This document describes the methodology for constructing color name polyhedra in Munsell color space, based on Centore's JAIC 2020 paper "Beige, aqua, fuchsia, etc.: Definitions for some non-basic surface colour names" (Volume 25, pp. 24-54).

**Key Finding**: Centore uses an **Inner Convex Hull** method for outlier removal, not a pure convex hull.

## Terminology

### Minimal Generating Set

A **convex hull minimal generating set** refers to the smallest subset of points (the "extreme points" or "vertices") that define the boundary of the smallest convex shape (hull) containing all points. Per Lay [4]:

> "These are the points a rubber band would touch if stretched around all points in 2D."

For a given set of points, this minimal set forms the vertices of the convex polytope.

**Reference**: Lay SR (2007) "Convex Sets and Their Applications", Dover Publications, Mineola NY [Centore citation 4]

### Inner Convex Hull

The **inner convex hull** is obtained by:
1. Computing the convex hull of a point set S
2. Discarding all vertices V of that hull
3. Computing the convex hull of the remaining points S−V

This removes potential outliers that lie on the boundary of the original hull.

---

## Centore's Algorithm (from JAIC 2020, pp. 31-35)

### Overview

From the paper (p. 33):

> "The set V of vertices of the convex hull H of S was found. These vertices are a minimal generating set [4] for H... Any potential outlier is likely in the set V, so we will discard all points in V, getting the set S−V. After the discarding, we calculate the convex hull Γ of S−V."

### Step 1: Collect Color Samples

**Source**: CAUS (Color Association of the United States) fabric samples
- Each sample has a color name and spectrophotometer-measured Munsell coordinates
- Filter samples matching target color name (e.g., all samples containing "beige")

From the paper (p. 31):
> "The CAUS library contains 9261 fabric samples, each of which has been assigned a fanciful colour name (such as 'Purple Margarita' or 'Citrus Punch'), and also measured with a spectrophotometer to obtain a Munsell specification."

**PLACEHOLDER - Exact matching criteria**:
The paper states samples are filtered by color name but does not specify exact string matching rules (case-sensitivity, partial vs. full match, word boundaries).
*Citation*: "filtered by a fanciful colour name" (p. 31)

### Step 2: Convert to Cartesian Coordinates

From the paper (p. 32):
> "For color-matching applications, it is common to convert from a Munsell specification to Cartesian coordinates (x, y, z)"

**Coordinate system** (p. 32):
- x = C × cos(H × π/50)
- y = C × sin(H × π/50)
- z = V

Where:
- H = Munsell hue number (0-100 scale, where 100 = full circle)
- V = Munsell value (0-10)
- C = Munsell chroma (0-20+)

**Note**: The paper uses hue on a 0-100 scale where 100 = 360°. The formula `H × π/50` converts to radians.

```python
def munsell_to_cartesian(hue_100, value, chroma):
    """
    Convert Munsell cylindrical to Cartesian coordinates.

    Args:
        hue_100: Munsell hue on 0-100 scale (100 = full circle)
        value: Munsell value (0-10)
        chroma: Munsell chroma (0-20+)

    Centore's formula from JAIC 2020, p. 32:
        x = C × cos(H × π/50)
        y = C × sin(H × π/50)
        z = V
    """
    hue_rad = hue_100 * math.pi / 50.0
    x = chroma * math.cos(hue_rad)
    y = chroma * math.sin(hue_rad)
    z = value
    return (x, y, z)
```

### Step 3: Compute Outer Convex Hull

From the paper (p. 33):
> "The convex hull H of S was calculated... The set V of vertices of the convex hull H of S was found."

```python
from scipy.spatial import ConvexHull

def compute_outer_hull(samples_cartesian):
    """Compute convex hull H of sample points S."""
    points = np.array(samples_cartesian)
    hull = ConvexHull(points)
    return hull, points[hull.vertices]  # H, V
```

### Step 4: Discard Outer Hull Vertices (Outlier Removal)

**This is the key outlier removal step.**

From the paper (p. 33):
> "Any potential outlier is likely in the set V, so we will discard all points in V, getting the set S−V."

```python
def remove_outer_vertices(all_samples, outer_vertices):
    """Remove outer hull vertices from sample set."""
    # Create mask for non-vertex samples
    vertex_set = set(map(tuple, outer_vertices))
    inner_samples = [s for s in all_samples if tuple(s) not in vertex_set]
    return np.array(inner_samples)  # S−V
```

### Step 5: Compute Inner Convex Hull (Final Polyhedron)

From the paper (p. 33):
> "After the discarding, we calculate the convex hull Γ of S−V. The convex set Γ is the polyhedron we were seeking."

```python
def compute_inner_hull(inner_samples):
    """Compute inner convex hull Γ from S−V."""
    hull = ConvexHull(inner_samples)
    vertices = inner_samples[hull.vertices]
    faces = hull.simplices
    return vertices, faces  # Γ
```

### Step 6: Compute Centroid

The paper describes centroid calculation using a "filled solid" approach (pp. 33-34).

From the paper (p. 33):
> "We also want a 'typical' colour for each polyhedron. Geometrically, the filled-solid centroid of a polyhedron is a representative point."

**Filled-Solid Centroid Equations** (p. 34, equations 6-8):

The centroid is computed by:
1. Triangulating the polyhedron surface into faces
2. Forming tetrahedra from each face to an arbitrary point P₀
3. Computing weighted average of tetrahedron centroids

**PLACEHOLDER - Exact centroid formula**:
The paper provides equations 6-8 but the full derivation requires careful implementation.
*Citation*: "Equations 6-8 calculate the filled-solid centroid" (p. 34)

For practical purposes, a simpler approximation may suffice:

```python
def compute_centroid_simple(vertices):
    """
    Simple centroid as mean of vertices.

    Note: This differs from Centore's filled-solid centroid.
    """
    return np.mean(vertices, axis=0)
```

---

## Complete Algorithm

```python
def build_centore_polyhedron(samples_munsell):
    """
    Build polyhedron using Centore's inner convex hull method.

    JAIC 2020, pp. 31-35

    Args:
        samples_munsell: List of (hue_100, value, chroma) tuples

    Returns:
        vertices: Polyhedron vertices in Cartesian coordinates
        faces: Triangle face indices
        centroid: Filled-solid centroid
    """
    # Step 1: Already have samples

    # Step 2: Convert to Cartesian
    S = np.array([munsell_to_cartesian(h, v, c) for h, v, c in samples_munsell])

    if len(S) < 4:
        raise ValueError("Need at least 4 samples for 3D hull")

    # Step 3: Compute outer convex hull
    H = ConvexHull(S)
    V = S[H.vertices]  # Outer hull vertices (minimal generating set)

    # Step 4: Remove outer vertices (outlier removal)
    vertex_indices = set(H.vertices)
    S_minus_V = np.array([S[i] for i in range(len(S)) if i not in vertex_indices])

    if len(S_minus_V) < 4:
        # Not enough points for inner hull - fall back to outer
        return V, H.simplices, np.mean(V, axis=0)

    # Step 5: Compute inner convex hull (final polyhedron)
    Gamma = ConvexHull(S_minus_V)
    vertices = S_minus_V[Gamma.vertices]
    faces = Gamma.simplices

    # Step 6: Compute centroid
    centroid = compute_filled_solid_centroid(vertices, faces)  # PLACEHOLDER

    return vertices, faces, centroid
```

---

## Limitations (from JAIC 2020, pp. 35-36)

Centore explicitly acknowledges these limitations:

### 1. Uncontrolled Viewing Illumination

From the paper (p. 35):
> "The CAUS names were assigned by viewing samples under some illumination, probably not precisely specified."

**Impact**: Color names may not accurately reflect how samples appear under standard D65 illumination.

### 2. Fanciful/Distinctive Name Bias

From the paper (p. 35):
> "The CAUS names are fanciful, meant to be distinctive... A manufacturer of beige fabric might call it 'Café au Lait' rather than 'beige', to sound more appealing."

**Impact**: Common color terms may be underrepresented in favor of creative marketing names.

### 3. Fashion Industry Domain

From the paper (p. 35):
> "The CAUS samples are from the fashion and textile industry."

**Impact**: Results may not generalize to other domains (paint, printing, natural colors).

### 4. Specialized Color Terminology

From the paper (p. 35-36):
> "Fashion colour terminology can be specialized. 'Navy', for instance, originally referred to the dark blue of naval uniforms."

**Impact**: Historical or industry-specific meanings may differ from general usage.

### 5. Unknown Subject Demographics

From the paper (p. 36):
> "The demographics of the subjects who assigned colour names are not known."

**Impact**: Cannot assess cultural, regional, or professional biases.

### 6. Possible Sample Fading

From the paper (p. 36):
> "The CAUS fabrics might have faded since being measured."

**Impact**: Current measurements may differ from original samples.

### 7. English Language Only

From the paper (p. 36):
> "The analysis is limited to English colour names."

**Impact**: Results do not address cross-cultural or multilingual color naming.

---

## Placeholders for Undefined Aspects

### PLACEHOLDER 1: Exact Sample Matching Criteria

**Question**: How exactly are samples matched to color names?
- Case-sensitive or insensitive?
- Exact match, substring, or word boundary?
- How are compound names handled?

**Citation**: "filtered by a fanciful colour name" (p. 31)

**Current assumption**: Case-insensitive substring match

### PLACEHOLDER 2: Handling Degenerate Cases

**Question**: What happens when:
- Fewer than 4 samples exist?
- All samples are coplanar?
- Inner hull has fewer than 4 points?

**Citation**: Not explicitly addressed in paper

**Current assumption**: Fall back to outer hull or skip color

### PLACEHOLDER 3: Filled-Solid Centroid Implementation

**Question**: Exact implementation of equations 6-8

**Citation**: "Equations 6-8 calculate the filled-solid centroid" (p. 34)

**Current assumption**: Use arithmetic mean of vertices as approximation

### PLACEHOLDER 4: Hue Encoding in Source Data

**Question**: What hue scale is used in the CAUS data files?
- 0-40 Munsell scale?
- 0-100 scale as in paper?
- 0-360 degrees?

**Citation**: "H × π/50" formula suggests 0-100 scale (p. 32)

**Current assumption**: Need to verify from PolyhedronFiles format

---

## Validation Against Centore's Data

To validate our implementation, we compare against Centore's published polyhedra:

**Expected outcome if correctly implemented**:
- Our inner hull vertices should match Centore's vertices exactly
- Vertex counts should match for each color category
- Centroids should match within numerical precision

## Implications for XKCD Data

### Differences from CAUS Data

| Aspect | CAUS | XKCD |
|--------|------|------|
| Measurement | Spectrophotometer | Computer monitors |
| Calibration | Controlled D65 | Uncalibrated, varied |
| Naming | Expert-assigned | Crowd-sourced, freeform |
| Sample size | 25-1673 per color | 100-20,000+ per color |
| Noise | Low | High |

### Recommended Approach for XKCD

Given XKCD's higher noise levels, apply Centore's inner convex hull method:

#### Option A: Inner Convex Hull (Match Centore)
- Apply exact same inner hull methodology for apples-to-apples comparison
- Single layer of outlier removal (discard outer hull vertices)
- Compare hull properties (volume, centroid) between datasets

#### Option B: Multiple Peeling Layers (More Aggressive)
- Apply multiple iterations of inner hull peeling
- Each iteration removes the current outer hull vertices
- More robust against XKCD's higher noise
- Less comparable to Centore but potentially more accurate

#### Recommended: Option A First, Then Option B
1. First build single-layer inner hulls to enable direct comparison with Centore
2. Then explore multiple peeling layers for practical applications
3. Document differences and trade-offs

---

## Additional Outlier Methods (Optional Enhancement)

### Convex Hull Peeling (Eddy 1982)

Iterative version of Centore's single-layer approach:

```python
def multi_layer_peeling(points, layers=1):
    """
    Remove multiple layers of outer hull vertices.

    Each layer removes the current hull vertices before
    computing the next hull.
    """
    remaining = points.copy()

    for _ in range(layers):
        if len(remaining) < 4:
            break

        hull = ConvexHull(remaining)
        vertex_indices = set(hull.vertices)
        remaining = np.array([
            remaining[i] for i in range(len(remaining))
            if i not in vertex_indices
        ])

    if len(remaining) < 4:
        # Fall back to last valid hull
        return points, ConvexHull(points)

    final_hull = ConvexHull(remaining)
    return remaining, final_hull
```

### Area-Weighted Peeling (arXiv:2410.04544)

From Sridhar & Svenning (2024):

```python
def area_weighted_peeling(points, k):
    """
    Remove k outliers by iteratively peeling points that
    most decrease hull volume (in 3D).

    Complexity: O(n log n) time, O(n) space
    """
    remaining = points.copy()
    removed = []

    for _ in range(k):
        if len(remaining) < 5:  # Need 4 for hull + 1 to remove
            break

        hull = ConvexHull(remaining)

        # Find vertex whose removal minimizes volume
        max_volume_decrease = -float('inf')
        point_to_remove = None

        for idx in hull.vertices:
            test_points = np.delete(remaining, idx, axis=0)
            try:
                new_hull = ConvexHull(test_points)
                volume_decrease = hull.volume - new_hull.volume
                if volume_decrease > max_volume_decrease:
                    max_volume_decrease = volume_decrease
                    point_to_remove = idx
            except Exception:
                continue

        if point_to_remove is not None:
            removed.append(remaining[point_to_remove])
            remaining = np.delete(remaining, point_to_remove, axis=0)

    return remaining, removed
```

---

## References

1. **Centore, P. (2020)** "Beige, aqua, fuchsia, etc.: Definitions for some non-basic surface colour names" - JAIC Vol. 25, pp. 24-54
   - PDF: https://www.munsellcolourscienceforpainters.com/ColourSciencePapers/BeigeAquaFuchsiaEtc.pdf

2. **Lay, S.R. (2007)** "Convex Sets and Their Applications" - Dover Publications, Mineola NY
   - Defines minimal generating set (convex hull vertices)

3. **Sridhar & Svenning (2024)** "Fast Area-Weighted Peeling of Convex Hulls for Outlier Detection"
   - arXiv: https://arxiv.org/abs/2410.04544

4. **Eddy, W.F. (1982)** "Convex Hull Peeling"
   - SpringerLink: https://link.springer.com/chapter/10.1007/978-3-642-51461-6_4

---

## Implementation Plan

1. [x] Document Centore methodology (this document)
2. [ ] Implement inner convex hull construction in Python
3. [ ] Validate implementation against Centore's published polyhedra
4. [ ] Apply to XKCD samples for 30 Centore overlay categories
5. [ ] Compare XKCD polyhedra to Centore polyhedra (centroid, volume, vertices)
6. [ ] Optionally implement multi-layer peeling for noise reduction
