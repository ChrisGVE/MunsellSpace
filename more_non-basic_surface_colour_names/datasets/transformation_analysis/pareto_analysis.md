# Pareto Frontier Analysis (from Existing Results)

Generated: 2026-01-03 16:33
Total strategies evaluated: 6
Pareto-optimal strategies: 6

## Methodology

Pareto frontier constructed from existing optimization results:
- Single-component: centroid-only, volume-only, shape-only
- Pairwise: centroid+volume, centroid+shape, volume+shape

A strategy is Pareto-optimal if no other strategy dominates it
(i.e., is better in all three objectives simultaneously).

## All Evaluated Strategies

| Strategy | Centroid | Volume | Shape | Combined | Pareto? |
|----------|----------|--------|-------|----------|---------|
| volume_only | 0.0000 | 0.0000 | 0.1800 | 0.0540 | ✓ |
| centroid_volume | 0.0054 | 0.0000 | 0.1799 | 0.0561 | ✓ |
| volume_shape | 0.0692 | 0.0000 | 0.1707 | 0.0789 | ✓ |
| centroid_only | 0.0000 | 0.3566 | 0.1699 | 0.1580 | ✓ |
| centroid_shape | 0.0000 | 0.3566 | 0.1699 | 0.1580 | ✓ |
| shape_only | 0.2557 | 0.5540 | 0.1304 | 0.3076 | ✓ |

## Pareto Frontier

| Strategy | Centroid | Volume | Shape | Combined |
|----------|----------|--------|-------|----------|
| volume_only | 0.0000 | 0.0000 | 0.1800 | 0.0540 |
| centroid_volume | 0.0054 | 0.0000 | 0.1799 | 0.0561 |
| volume_shape | 0.0692 | 0.0000 | 0.1707 | 0.0789 |
| centroid_only | 0.0000 | 0.3566 | 0.1699 | 0.1580 |
| centroid_shape | 0.0000 | 0.3566 | 0.1699 | 0.1580 |
| shape_only | 0.2557 | 0.5540 | 0.1304 | 0.3076 |

## Extreme Points on Frontier

**Best Centroid**: centroid_only
  - Centroid: 0.0000

**Best Volume**: centroid_volume
  - Volume: 0.0000

**Best Shape**: shape_only
  - Shape: 0.1304

**Best Combined**: volume_only
  - Combined: 0.0540

## Trade-off Ranges on Frontier

| Objective | Min | Max | Range |
|-----------|-----|-----|-------|
| centroid | 0.0000 | 0.2557 | 0.2557 |
| volume | 0.0000 | 0.5540 | 0.5540 |
| shape | 0.1304 | 0.1800 | 0.0495 |

## Key Findings

1. **Volume-only is Pareto-optimal** - confirms its dominance
2. **Centroid+Volume is Pareto-optimal** - good balance point

## Recommendations

1. **For general use**: Use volume-only or centroid+volume optimization
2. **For maximum shape fidelity**: Accept volume degradation or use multi-objective
3. **The Pareto frontier confirms**: volume matching is the most efficient single objective
