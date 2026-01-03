# Research Observations Log

This log captures detailed observations, challenges, and insights from transformation research experiments.
Each entry is tagged with an experiment ID for cross-referencing with the experiment registry.

---

## 2026-01-03: Phase 4 Summary (Migrated)

### Domain Comparison Findings (EXP-007 to EXP-009)

- **Munsell Cartesian domain is dramatically better**: 27x lower loss than RGB, 30x lower than CIELAB
- RGB and CIELAB domains introduce prohibitive conversion errors
- **Key insight**: Optimization must happen in the target space; any intermediate conversion degrades results

### Linear vs Non-linear Methods (EXP-001 to EXP-006)

- Translation+Scaling (6 parameters) achieves 0.053 mean loss - best overall
- Non-linear methods (polynomial, RBF, TPS) achieve 0.28-0.41 mean loss
- **Paradox**: Simpler linear transformation outperforms complex non-linear methods
- Possible explanation: Non-linear methods overfit to vertex positions, not shape correspondence

### Extended Domain Comparison (EXP-010 to EXP-012)

- Affine transformation (12 params) achieves 0.078 loss - slightly worse than Translation+Scaling
- Additional degrees of freedom in Affine may cause overfitting
- Confirmed: Munsell domain consistently outperforms RGB regardless of transformation method

---

## Open Questions

1. **Volume transformation invariance**: Does dV in RGB map to same perceptual volume everywhere in Munsell? (Jacobian analysis needed)

2. **Sample size effects**: Is convex hull volume dependent on sample count? (Bootstrap analysis needed)

3. **Loss function trade-offs**: Should we optimize centroid, volume, and shape independently? Current combined loss may hide conflicts.

4. **Aggregation method**: Mean loss across families may hide outliers. Consider sum loss or minimax.

5. **Shape correspondence**: Current methods align vertices, not surfaces. Consider Procrustes and shape-statistical approaches.

---

## Challenges Encountered

### PyTorch Compatibility
- PyTorch not available for Python 3.13
- Neural network experiments (Task 74) created placeholder implementation
- Future: Use conda environment with Python 3.11 for deep learning

### Approximate Color Conversions
- RGB↔Munsell and LAB↔Munsell conversions are approximate (HSV-based)
- Exact conversion requires Munsell renotation data
- Some error in RGB domain results is due to conversion, not the transformation method

### Polynomial Method Failures
- Polynomial methods failed silently on some families in extended comparison
- Likely due to sklearn fitting issues with vertex correspondence
- Need investigation

---

## Methodology Notes

### Loss Function Weights
Current: L_total = 0.4 × L_centroid + 0.3 × L_volume + 0.3 × L_shape

- L_centroid: Normalized Euclidean distance between polyhedra centroids
- L_volume: |V_screen/V_surface - 1| (volume ratio deviation)
- L_shape: Hausdorff distance (surface-to-surface)

### Families Analyzed
21 families with valid polyhedra (3D extent in both screen and surface):
aqua, aquamarine, blue, brown, coral, fuchsia, gold, green, indigo, lime,
magenta, mauve, peach, plum, red, rust, tan, teal, violet, wine, yellow

---

## Experiment Entries

### [EXP-001] 2026-01-03 14:36
Baseline linear transformation. Best performer in Phase 4.

### [EXP-007] 2026-01-03 14:36
Munsell Cartesian domain test. Establishes baseline for domain comparison.

### [EXP-010] 2026-01-03 14:36
Translation+Scaling in Munsell domain. Confirms best performance at 0.0535 mean loss.

### [EXP-013] 2026-01-03 14:42
When optimizing centroid only, combined loss is 0.1580

### [EXP-014] 2026-01-03 14:42
When optimizing volume only, combined loss is 0.0540

### [EXP-015] 2026-01-03 14:42
When optimizing shape only, combined loss is 0.3076

### [EXP-016] 2026-01-03 14:51
When optimizing centroid+volume, shape degrades to 0.1799

### [EXP-017] 2026-01-03 14:51
When optimizing centroid+shape, volume degrades to 0.3566

### [EXP-018] 2026-01-03 14:51
When optimizing volume+shape, centroid degrades to 0.0692

---

## 2026-01-03: Phase 5.1 Loss Function Analysis

### Single-Component Optimization (EXP-013 to EXP-015)

- **Volume-only achieves 0.054 combined loss** - nearly identical to full combined (0.0535)!
- Centroid-only: combined = 0.158 (poor)
- Shape-only: combined = 0.308 (worst)
- **Key insight**: Volume matching is the dominant objective

### Pairwise Component Analysis (EXP-016 to EXP-018)

- Centroid+Volume: combined = 0.056, shape = 0.180 (acceptable)
- Centroid+Shape: combined = 0.158, volume = 0.357 (degraded)
- Volume+Shape: combined = 0.079, centroid = 0.069 (acceptable)

**Critical finding**: Volume-only (0.054) still outperforms best pairwise (0.056)

### Trade-off Summary

| Strategy | Combined Loss | Rank |
|----------|--------------|------|
| Volume-only | 0.054 | 1 |
| Combined (full) | 0.054 | 2 |
| Centroid+Volume | 0.056 | 3 |
| Volume+Shape | 0.079 | 4 |
| Centroid-only | 0.158 | 5 |
| Centroid+Shape | 0.158 | 6 |
| Shape-only | 0.308 | 7 |

**Conclusion**: Volume matching alone achieves near-optimal results. The current weighted combination (0.4/0.3/0.3) appears to work primarily because it includes volume.
