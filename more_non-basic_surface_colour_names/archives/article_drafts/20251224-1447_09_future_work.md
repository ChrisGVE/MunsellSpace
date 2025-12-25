# Future Work: Non-Linear Hue Correction

## Overview

The key finding of this research - that hue bias is non-uniform and category-
dependent - necessitates non-linear modeling for accurate screen-to-physical
color correction.

This section outlines proposed approaches for Stage 5: Non-Linear Modeling.

---

## 1. Problem Formulation

### Goal

Learn a correction function:

```
Δhue = f(hue_screen, value, chroma)
```

Where:
- Input: Screen color in Munsell coordinates
- Output: Hue correction to apply
- Constraint: f must be smooth and physically plausible

### Training Data

| Source | n | Use |
|--------|---|-----|
| Category centroids | 30 | Primary training targets |
| Individual color biases | 101,894 | Optional training data |
| Held-out categories | 5-10 | Validation set |

### Evaluation Metrics

1. **Mean Absolute Error (MAE)**: Average |predicted - actual| hue correction
2. **Root Mean Square Error (RMSE)**: Penalizes large errors
3. **Max Error**: Worst-case correction accuracy
4. **Cross-Validation Score**: Generalization to held-out categories

---

## 2. Approach 1: Piecewise Linear by Hue Region

### Concept

Divide the hue wheel into regions with different linear slopes.

### Implementation

```python
def piecewise_linear_correction(hue):
    """Apply region-specific linear correction."""
    if 0 <= hue < 60:      # Red-Yellow region
        return hue * slope_1 + intercept_1
    elif 60 <= hue < 120:  # Yellow-Green region
        return hue * slope_2 + intercept_2
    elif 120 <= hue < 180: # Green-Cyan region
        return hue * slope_3 + intercept_3
    elif 180 <= hue < 240: # Cyan-Blue region
        return hue * slope_4 + intercept_4
    elif 240 <= hue < 300: # Blue-Purple region
        return hue * slope_5 + intercept_5
    else:                  # Purple-Red region
        return hue * slope_6 + intercept_6
```

### Pros and Cons

| Pros | Cons |
|------|------|
| Simple, interpretable | Discontinuities at boundaries |
| Fast to compute | May not capture within-region variation |
| Easy to fit (linear regression) | Arbitrary region boundaries |

### Estimated Complexity

- Parameters: 12 (6 slopes + 6 intercepts)
- Fitting: Least squares per region
- Validation: Leave-one-category-out cross-validation

---

## 3. Approach 2: Polynomial in Cylindrical Coordinates

### Concept

Fit a polynomial in (hue, value, chroma) to predict hue correction.

### Implementation

```python
def polynomial_correction(hue, value, chroma, coefficients):
    """
    Polynomial model:
    Δhue = Σ a_ijk * hue^i * value^j * chroma^k

    For degree 2:
    Δhue = a_000 + a_100*h + a_010*v + a_001*c
         + a_200*h² + a_110*h*v + a_101*h*c + ...
    """
    terms = []
    for i in range(degree + 1):
        for j in range(degree + 1 - i):
            for k in range(degree + 1 - i - j):
                terms.append(coefficients[i,j,k] * hue**i * value**j * chroma**k)
    return sum(terms)
```

### Handling Circular Hue

Hue is circular (0° = 360°). Options:
1. Use sin(hue) and cos(hue) instead of raw hue
2. Fit on hue domain with wraparound constraints
3. Use Fourier basis for hue dimension

### Pros and Cons

| Pros | Cons |
|------|------|
| Smooth, differentiable | High degree may overfit |
| Captures interactions (h×v, h×c) | Many parameters |
| Well-understood mathematics | Circular hue requires care |

### Estimated Complexity

- Degree 2: 10 parameters
- Degree 3: 20 parameters
- Degree 4: 35 parameters
- Fitting: Ridge regression (regularized least squares)

---

## 4. Approach 3: Gaussian Process Regression

### Concept

Non-parametric Bayesian regression that provides uncertainty estimates.

### Implementation

```python
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, WhiteKernel

def train_gp_correction(X_train, y_train):
    """
    Train GP model for hue correction.
    X: (hue, value, chroma) for each category centroid
    y: observed hue bias for each category
    """
    # Matern kernel for smooth but flexible function
    kernel = Matern(nu=2.5) + WhiteKernel(noise_level=1e-5)

    gp = GaussianProcessRegressor(kernel=kernel)
    gp.fit(X_train, y_train)

    return gp

def predict_correction(gp, hue, value, chroma):
    """Predict hue correction with uncertainty."""
    X = np.array([[hue, value, chroma]])
    mean, std = gp.predict(X, return_std=True)
    return mean[0], std[0]
```

### Pros and Cons

| Pros | Cons |
|------|------|
| Uncertainty quantification | Computationally expensive |
| Non-parametric flexibility | Scales poorly with data size |
| Automatic complexity tuning | Circular hue requires custom kernel |

### Estimated Complexity

- Parameters: O(n²) for n training points
- Fitting: O(n³) matrix inversion
- Prediction: O(n) per query
- For 30 category centroids: Very tractable

---

## 5. Approach 4: Neural Network

### Concept

Learn the correction function using a small neural network.

### Architecture

```python
import torch.nn as nn

class HueCorrectionNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            # Input: (sin(hue), cos(hue), value, chroma)
            nn.Linear(4, 32),
            nn.ReLU(),
            nn.Linear(32, 32),
            nn.ReLU(),
            nn.Linear(32, 1)  # Output: Δhue
        )

    def forward(self, hue, value, chroma):
        # Convert hue to sin/cos for circular handling
        x = torch.stack([
            torch.sin(hue * np.pi / 180),
            torch.cos(hue * np.pi / 180),
            value,
            chroma
        ], dim=-1)
        return self.net(x)
```

### Training Strategy

- Loss: MSE on hue correction
- Regularization: L2 weight decay
- Validation: K-fold cross-validation on categories
- Early stopping to prevent overfitting

### Pros and Cons

| Pros | Cons |
|------|------|
| Universal function approximation | Requires more data |
| Handles complex patterns | Black box |
| GPU-accelerated | Risk of overfitting with 30 points |

### Estimated Complexity

- Parameters: ~2,000 (small network)
- Training: Gradient descent, ~1000 epochs
- Prediction: O(1) per query
- Overfitting risk: High with only 30 training points

---

## 6. Approach 5: Spline Interpolation

### Concept

Fit smooth splines through category centroids in hue space.

### Implementation

```python
from scipy.interpolate import UnivariateSpline, RBFInterpolator

def spline_correction(category_hues, category_biases):
    """
    Fit spline through category centroids.
    Returns interpolation function.
    """
    # Sort by hue for 1D spline
    order = np.argsort(category_hues)
    hues = category_hues[order]
    biases = category_biases[order]

    # Handle circular wrap (duplicate endpoints)
    hues_ext = np.concatenate([hues - 360, hues, hues + 360])
    biases_ext = np.concatenate([biases, biases, biases])

    # Fit smoothing spline
    spline = UnivariateSpline(hues_ext, biases_ext, s=smoothing)

    return spline
```

### For 3D (hue, value, chroma)

```python
def rbf_correction(centroids_hvl, biases):
    """
    Radial Basis Function interpolation in 3D Munsell space.
    """
    rbf = RBFInterpolator(centroids_hvl, biases, kernel='thin_plate_spline')
    return rbf
```

### Pros and Cons

| Pros | Cons |
|------|------|
| Passes through training points | May oscillate between points |
| Smooth interpolation | Smoothing parameter tuning needed |
| Well-understood mathematics | Extrapolation unreliable |

### Estimated Complexity

- Parameters: n control points (30 for centroids)
- Fitting: O(n³) for RBF
- Prediction: O(n) per query

---

## 7. Recommended Approach

### Phase 1: Baseline Comparison

Test all five approaches on the 30-category dataset:

1. Split: 25 training, 5 validation
2. Fit each model on training set
3. Evaluate MAE on validation set
4. Repeat with different splits (k-fold)

### Phase 2: Refinement

Based on Phase 1 results:

- If simple model wins → Use piecewise linear or polynomial
- If GP wins → Explore custom circular kernels
- If NN wins → Collect more data or use data augmentation
- If spline wins → Tune smoothing parameters

### Phase 3: Integration

Integrate best model into MunsellSpace library:

```rust
pub fn correct_screen_color(munsell: &MunsellColor) -> MunsellColor {
    // Apply learned corrections
    let value_corrected = munsell.value - 0.81;
    let chroma_corrected = munsell.chroma - 3.82;
    let hue_correction = predict_hue_correction(munsell);
    let hue_corrected = (munsell.hue + hue_correction) % 360.0;

    MunsellColor::new(hue_corrected, value_corrected, chroma_corrected)
}
```

---

## 8. Validation Strategy

### Internal Validation

- Leave-one-category-out cross-validation
- Compare predicted vs actual bias for held-out category

### External Validation

- Collect new color naming data (not from XKCD)
- Compare corrected screen colors to physical samples
- User study: Do corrected colors "feel" more accurate?

### Physical Validation

- Print corrected colors on calibrated printer
- Measure with spectrophotometer
- Compare to Centore reference

---

## 9. Success Criteria

| Metric | Target |
|--------|--------|
| Hue MAE | < 10° |
| Hue RMSE | < 15° |
| Max hue error | < 30° |
| Value MAE | < 0.5 units |
| Chroma MAE | < 2.0 units |

### Stretch Goals

| Metric | Target |
|--------|--------|
| Hue MAE | < 5° |
| Perceptual validation | Users prefer corrected colors |
| Physical match | ΔE < 3 (barely perceptible) |

---

## 10. Timeline and Milestones

### Milestone 1: Model Comparison

- Implement all five approaches
- Run k-fold cross-validation
- Select best performing model

### Milestone 2: Refinement

- Tune hyperparameters of best model
- Add uncertainty quantification
- Validate on held-out data

### Milestone 3: Integration

- Implement in Rust (MunsellSpace library)
- Add Python bindings
- Write documentation

### Milestone 4: Publication

- Write methodology section
- Generate figures and tables
- Submit to appropriate venue

