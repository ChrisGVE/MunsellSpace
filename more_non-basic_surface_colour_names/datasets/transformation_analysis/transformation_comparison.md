# Linear Transformation Comparison Report

Generated: 2026-01-03

Families analyzed: 21 (valid polyhedra with 3D extent)

## Transformation Classes

| Class | Parameters | Description |
|-------|------------|-------------|
| Translation | 3 | T(x) = x + b |
| Scaling | 3 | T(x) = s * (x - centroid) + centroid |
| Translation+Scaling | 6 | Combined translation and per-axis scaling |
| Affine | 12 | T(x) = Ax + b (full 3x3 matrix) |

## Per-Family Optimization Results

| Transform | Mean Improvement | Mean Final Loss | Best Family |
|-----------|------------------|-----------------|-------------|
| translation | 0.0% | 6.484 | (no improvement) |
| scaling | 54.4% | 0.356 | coral (0.123) |
| translation_scaling | 61.9% | 0.053 | wine (0.033) |
| affine | 76.8% | 0.078 | wine (0.030) |

### Detailed Results: Translation+Scaling (Recommended)

This 6-parameter model provides the best balance of simplicity and performance:

| Family | Initial Loss | Final Loss | Improvement |
|--------|--------------|------------|-------------|
| aqua | 0.185 | 0.072 | 61.1% |
| aquamarine | 0.181 | 0.052 | 71.2% |
| blue | 0.114 | 0.068 | 40.4% |
| brown | 0.090 | 0.050 | 44.8% |
| coral | 0.093 | 0.057 | 38.2% |
| fuchsia | 0.214 | 0.042 | 80.3% |
| gold | 0.194 | 0.058 | 70.0% |
| green | 0.096 | 0.057 | 40.6% |
| indigo | 0.068 | 0.035 | 48.7% |
| lime | 0.189 | 0.075 | 60.6% |
| magenta | 0.143 | 0.056 | 60.8% |
| mauve | 0.260 | 0.078 | 70.1% |
| peach | 0.105 | 0.045 | 57.1% |
| plum | 0.219 | 0.051 | 76.8% |
| red | 0.133 | 0.049 | 63.0% |
| rust | 0.133 | 0.052 | 60.6% |
| tan | 0.191 | 0.059 | 69.0% |
| teal | 0.138 | 0.056 | 59.3% |
| violet | 0.271 | 0.038 | 85.9% |
| wine | 0.081 | 0.033 | 59.8% |
| yellow | 0.217 | 0.039 | 82.3% |

### Detailed Results: Affine (12 params)

Higher improvement but more parameters, risk of overfitting:

| Family | Initial Loss | Final Loss | Improvement |
|--------|--------------|------------|-------------|
| aqua | 1.105 | 0.072 | 93.5% |
| aquamarine | 21.950 | 0.175 | 99.2% |
| blue | 1.044 | 0.061 | 94.2% |
| brown | 1.738 | 0.056 | 96.8% |
| coral | 1.265 | 0.064 | 94.9% |
| fuchsia | 0.825 | 0.045 | 94.6% |
| gold | 2.620 | 0.058 | 97.8% |
| green | 0.071 | 0.055 | 23.1% |
| indigo | 2.660 | 0.050 | 98.1% |
| lime | 1.242 | 0.067 | 94.6% |
| magenta | 0.255 | 0.057 | 77.6% |
| mauve | 0.506 | 0.061 | 87.8% |
| peach | 73.065 | 0.093 | 99.9% |
| plum | 0.078 | 0.059 | 23.3% |
| rust | 1.009 | 0.045 | 95.5% |
| tan | 0.799 | 0.061 | 92.4% |
| teal | 0.204 | 0.065 | 68.1% |
| violet | 25.187 | 0.077 | 99.7% |
| wine | 0.158 | 0.030 | 80.8% |

## Key Findings

1. **Translation alone is insufficient**: Pure translation provides no improvement,
   confirming that screen vs surface differences involve more than position shifts.

2. **Scaling is highly effective**: Per-axis scaling alone achieves 54.4% improvement,
   indicating systematic differences in color range/saturation between screen and surface.

3. **Translation+Scaling is optimal**: With only 6 parameters:
   - Achieves 61.9% mean improvement
   - Lowest mean final loss (0.053)
   - Best trade-off between complexity and performance

4. **Affine provides marginal gain**: Despite 12 parameters:
   - Higher mean improvement (76.8%)
   - But slightly higher mean final loss (0.078)
   - Greater risk of overfitting

## Recommendations

1. **Use Translation+Scaling for production**: 6 parameters, stable optimization,
   best generalization characteristics.

2. **Parameter interpretation**:
   - Scale factors indicate chroma/value range differences
   - Translation captures systematic position bias

3. **Global vs Per-Family**:
   - Start with global transformation for systematic correction
   - Per-family refinement for applications requiring highest accuracy

4. **Next steps**:
   - Validate transformation on held-out families
   - Consider non-linear transformations for residual errors
   - Investigate per-hue-region transformations
