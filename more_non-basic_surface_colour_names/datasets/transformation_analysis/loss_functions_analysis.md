# Loss Functions Analysis Report

## Loss Function Design

Combined loss: `L_total = w1 * L_centroid + w2 * L_volume + w3 * L_shape`

### Component Definitions

1. **L_centroid**: Normalized Euclidean distance between centroids
   - Normalized by average polyhedron radius
   - Range: [0, inf), 0 = perfect alignment

2. **L_volume**: Volume ratio deviation
   - `|V_screen / V_surface - 1|`
   - Range: [0, inf), 0 = equal volumes

3. **L_shape**: Normalized Hausdorff distance
   - Average bidirectional Hausdorff
   - Normalized by average diameter
   - Range: [0, 1], 0 = identical shape

## Baseline Loss by Family (No Transformation)

| Family | Category | L_centroid | L_volume | L_shape | L_total |
|--------|----------|------------|----------|---------|---------|
| plum | new-candidate | 0.370 | 0.057 | 0.198 | 0.224 |
| yellow | basic | 0.639 | 0.299 | 0.196 | 0.404 |
| wine | non-basic | 0.713 | 0.400 | 0.176 | 0.458 |
| magenta | non-basic | 0.760 | 0.649 | 0.225 | 0.566 |
| green | basic | 1.401 | 0.054 | 0.255 | 0.653 |
| red | basic | 1.158 | 0.638 | 0.132 | 0.694 |
| mauve | non-basic | 1.039 | 1.443 | 0.300 | 0.938 |
| fuchsia | non-basic | 0.398 | 2.559 | 0.183 | 0.982 |
| teal | non-basic | 2.024 | 0.447 | 0.430 | 1.073 |
| rust | non-basic | 0.488 | 3.162 | 0.204 | 1.205 |
| tan | non-basic | 1.079 | 2.415 | 0.307 | 1.248 |
| blue | basic | 0.887 | 3.264 | 0.299 | 1.423 |
| lime | new-candidate | 0.918 | 3.861 | 0.295 | 1.614 |
| coral | non-basic | 1.083 | 3.965 | 0.285 | 1.708 |
| aqua | non-basic | 1.464 | 3.419 | 0.462 | 1.750 |
| brown | basic | 1.392 | 5.569 | 0.308 | 2.320 |
| gold | non-basic | 0.405 | 8.524 | 0.254 | 2.795 |
| indigo | new-candidate | 1.130 | 8.629 | 0.342 | 3.143 |
| aquamarine | new-candidate | 0.774 | 72.779 | 0.514 | 22.297 |
| violet | non-basic | 0.849 | 83.651 | 0.355 | 25.541 |
| peach | non-basic | 0.500 | 243.089 | 0.432 | 73.256 |

### Summary Statistics

- Mean total loss: 6.8712
- Std total loss: 16.2801
- Min total loss: 0.2243 (plum)
- Max total loss: 73.2563 (peach)

## Weight Sensitivity Analysis

| Configuration | w_centroid | w_volume | w_shape | Mean Loss |
|---------------|------------|----------|---------|-----------|
| centroid_only | 1.00 | 0.00 | 0.00 | 0.9272 |
| volume_only | 0.00 | 1.00 | 0.00 | 21.3749 |
| shape_only | 0.00 | 0.00 | 1.00 | 0.2928 |
| equal | 0.33 | 0.33 | 0.34 | 7.4593 |
| centroid_emphasis | 0.40 | 0.30 | 0.30 | 6.8712 |

## Recommendations

1. **Default weights**: w_centroid=0.4, w_volume=0.3, w_shape=0.3
   - Emphasizes centroid alignment as primary objective
   - Balances volume and shape preservation

2. **For optimization**:
   - Start with centroid-only for fast initial alignment
   - Refine with full loss for final optimization
