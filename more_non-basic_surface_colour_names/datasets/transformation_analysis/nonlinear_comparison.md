# Non-Linear Transformation Comparison Report

Generated: 2026-01-03 12:05:06

## Transformation Classes

| Class | Parameters | Description |
|-------|------------|-------------|
| Polynomial (deg 2) | 30 | Quadratic features + Ridge regression |
| Polynomial (deg 3) | 60 | Cubic features + Ridge regression |
| RBF Multiquadric | N*3 | φ(r) = sqrt(r² + ε²) |
| RBF Gaussian | N*3 | φ(r) = exp(-r²/ε²) |
| Thin-Plate Spline | N*3+12 | Minimizes bending energy |

## Summary Results

| Transform | Mean Improvement | Mean Loss | Valid Families |
|-----------|------------------|-----------|----------------|
| polynomial_deg2 | 55.9% | 0.4122 | 21 |
| polynomial_deg3 | 64.8% | 0.3371 | 21 |
| rbf_multiquadric | 65.1% | 0.3292 | 21 |
| rbf_gaussian | 71.2% | 0.3144 | 21 |
| thin_plate_spline | 71.2% | 0.2872 | 21 |

## Comparison with Linear Baseline

| Method | Mean Loss | Std Loss | Parameters |
|--------|-----------|----------|------------|
| translation_scaling | 0.0535 | 0.0123 | 6 |
| polynomial_deg2 | 0.4122 | 0.0821 | 30 |
| thin_plate_spline | 0.2872 | 0.0840 | N*3 |

## Recommendations

1. **Linear methods remain competitive** - non-linear adds complexity
   without proportional improvement

2. **Polynomial (degree 2)**: Good balance of flexibility and stability
   - Ridge regularization prevents overfitting
   - Fixed number of parameters

3. **Thin-plate splines**: Best for smooth interpolation
   - Requires control point correspondences
   - May overfit with few samples

4. **For production use**:
   - Start with Translation+Scaling (linear)
   - Apply polynomial refinement if residuals are systematic
   - Use TPS only for high-accuracy requirements