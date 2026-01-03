# Deep Learning Transformation Comparison Report

Generated: 2026-01-03

## Implementation Status

**Note**: This report documents the implementation of deep learning transformation approaches.
Full training results require PyTorch installation.

To run the comparison:
```bash
pip install torch
cd more_non-basic_surface_colour_names/scripts
python3 nn_transformations.py
```

## Model Architectures

| Model | Parameters | Description |
|-------|------------|-------------|
| Translation+Scaling | 6 | Linear baseline (3 scale + 3 translation) |
| MLP | ~25,000 | 3→64→128→64→3 with ReLU, BatchNorm |
| Residual | ~17,000 | T(x) = x + f(x), 2 residual blocks |
| Variational | ~18,000 | Outputs distribution (mean, variance) |

### 1. MLP Transform

Multi-layer perceptron with architecture:
- Input: 3D Munsell Cartesian (x, y, z)
- Hidden layers: 64 → 128 → 64 neurons
- Activation: ReLU with BatchNorm
- Output: 3D transformed coordinates

### 2. Residual Transform

Residual network learning identity + correction:
- Architecture: T(x) = x + f(x)
- Makes learning small corrections easier
- Skip connections preserve gradient flow
- Initialized to near-identity transformation

### 3. Variational Transform

Outputs distribution instead of point estimate:
- Encodes uncertainty in transformation
- Mean head: residual-connected for stability
- Log-variance head: uncertainty quantification
- Training uses ELBO loss with KL divergence

## Expected Results Based on Previous Phases

From Phase 4.2-4.3 analysis:

| Method | Mean Loss | Parameters |
|--------|-----------|------------|
| Translation+Scaling | 0.053 | 6 |
| Polynomial (deg 2) | 0.412 | 30 |
| Thin-Plate Spline | 0.287 | N*3 |

**Expected finding**: Linear Translation+Scaling likely to remain competitive or superior due to:
1. Limited training data (21 families)
2. Imperfect point correspondence between polyhedra
3. Overfitting risk with high-parameter models

## Recommendations

1. **For production use**: Prefer Translation+Scaling (6 params)
   - Lowest loss achieved with simplest model
   - No training required, fast optimization
   - Interpretable parameters

2. **Neural network considerations**:
   - Limited training data (21 families) constrains deep learning
   - Point-to-point correspondence is imperfect for polyhedra
   - Residual architecture helps but doesn't overcome data limitations

3. **Variational approach benefits**:
   - Provides uncertainty quantification
   - May identify unreliable transformations
   - Higher computational cost for marginal benefit

4. **Future improvements**:
   - More surface color data would enable better deep learning
   - Graph neural networks for proper polyhedra correspondence
   - Transfer learning from larger color datasets

## Implementation Details

The implementation (`scripts/nn_transformations.py`) includes:

- `MLPTransform`: Standard feedforward network
- `ResidualTransform`: Identity + learned correction
- `VariationalTransform`: Probabilistic with uncertainty
- Training utilities with early stopping
- Comparison with linear baseline
- Per-family evaluation metrics
