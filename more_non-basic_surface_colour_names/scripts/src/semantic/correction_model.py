#!/usr/bin/env python3
"""
Correction Model Development for Screen-to-Physical Color Conversion

This script develops and compares multiple approaches for correcting the
systematic biases between screen colors (XKCD) and physical colors (Centore).

Key findings to model:
- Value bias: +0.81 (uniform, linear correction likely sufficient)
- Chroma bias: +3.82 (uniform, linear correction likely sufficient)
- Hue bias: Non-uniform, category-dependent (requires non-linear model)
"""

import json
import math
import numpy as np
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional, Callable
import warnings
warnings.filterwarnings('ignore')

# Try to import optional dependencies
try:
    from scipy.interpolate import CubicSpline, UnivariateSpline
    from scipy.optimize import minimize
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False
    print("Warning: scipy not available, some models will be skipped")

try:
    from sklearn.gaussian_process import GaussianProcessRegressor
    from sklearn.gaussian_process.kernels import RBF, Matern, WhiteKernel, ExpSineSquared
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    print("Warning: sklearn not available, GP models will be skipped")


@dataclass
class CategoryBias:
    """Bias data for a single color category."""
    name: str
    centore_hue: float  # degrees
    xkcd_hue: float     # degrees
    hue_diff: float     # XKCD - Centore (degrees)
    value_diff: float
    chroma_diff: float
    n_matches: int
    centore_value: float = 0.0
    centore_chroma: float = 0.0
    xkcd_value: float = 0.0
    xkcd_chroma: float = 0.0


def load_bias_data(filepath: Path) -> List[CategoryBias]:
    """Load category bias data from comparison results."""
    with open(filepath) as f:
        data = json.load(f)

    biases = []
    for cat, info in data['comparisons'].items():
        bias = CategoryBias(
            name=cat,
            centore_hue=info['centore_centroid']['hue_num'],
            xkcd_hue=info['xkcd_centroid']['hue_num'],
            hue_diff=info['bias']['hue_diff'],
            value_diff=info['bias']['value_diff'],
            chroma_diff=info['bias']['chroma_diff'],
            n_matches=info['xkcd_matches'],
            centore_value=info['centore_centroid']['value'],
            centore_chroma=info['centore_centroid']['chroma'],
            xkcd_value=info['xkcd_centroid']['value'],
            xkcd_chroma=info['xkcd_centroid']['chroma'],
        )
        biases.append(bias)

    return biases


def circular_diff(a: float, b: float) -> float:
    """Compute circular difference between two angles in degrees."""
    diff = a - b
    while diff > 180:
        diff -= 360
    while diff < -180:
        diff += 360
    return diff


def circular_mean(angles: List[float]) -> float:
    """Compute circular mean of angles in degrees."""
    sin_sum = sum(math.sin(math.radians(a)) for a in angles)
    cos_sum = sum(math.cos(math.radians(a)) for a in angles)
    return math.degrees(math.atan2(sin_sum, cos_sum))


# =============================================================================
# Model 1: Global Linear Correction (Baseline)
# =============================================================================

class GlobalLinearCorrection:
    """Apply constant offsets to all colors."""

    def __init__(self):
        self.hue_offset = 0.0
        self.value_offset = 0.0
        self.chroma_offset = 0.0

    def fit(self, biases: List[CategoryBias]):
        """Fit by computing weighted mean of biases."""
        total_weight = sum(b.n_matches for b in biases if b.name != 'gray')

        # For hue, use circular mean weighted by sample size
        # Actually, we want the correction, which is -bias
        hue_diffs = []
        weights = []
        for b in biases:
            if b.name == 'gray':  # Skip neutral color
                continue
            hue_diffs.append(b.hue_diff)
            weights.append(b.n_matches)

        # Weighted circular mean of hue differences
        sin_sum = sum(w * math.sin(math.radians(h)) for w, h in zip(weights, hue_diffs))
        cos_sum = sum(w * math.cos(math.radians(h)) for w, h in zip(weights, hue_diffs))
        self.hue_offset = math.degrees(math.atan2(sin_sum, cos_sum))

        # Value and chroma: weighted arithmetic mean
        self.value_offset = sum(b.value_diff * b.n_matches for b in biases) / total_weight
        self.chroma_offset = sum(b.chroma_diff * b.n_matches for b in biases) / total_weight

    def predict_hue_correction(self, hue: float, value: float = None, chroma: float = None) -> float:
        """Return the hue correction to apply (subtract from screen hue)."""
        return self.hue_offset

    def predict_value_correction(self, hue: float = None, value: float = None, chroma: float = None) -> float:
        return self.value_offset

    def predict_chroma_correction(self, hue: float = None, value: float = None, chroma: float = None) -> float:
        return self.chroma_offset


# =============================================================================
# Model 2: Piecewise Linear by Hue Region
# =============================================================================

class PiecewiseLinearCorrection:
    """Divide hue wheel into regions with different offsets."""

    def __init__(self, n_regions: int = 6):
        self.n_regions = n_regions
        self.region_size = 360 / n_regions
        self.hue_offsets = [0.0] * n_regions
        self.value_offset = 0.0
        self.chroma_offset = 0.0

    def _get_region(self, hue: float) -> int:
        """Get region index for a hue."""
        return int(hue / self.region_size) % self.n_regions

    def fit(self, biases: List[CategoryBias]):
        """Fit by computing mean bias per region."""
        # Value and chroma: global mean (they're relatively uniform)
        chromatic = [b for b in biases if b.name != 'gray']
        total_weight = sum(b.n_matches for b in chromatic)
        self.value_offset = sum(b.value_diff * b.n_matches for b in chromatic) / total_weight
        self.chroma_offset = sum(b.chroma_diff * b.n_matches for b in chromatic) / total_weight

        # Hue: per-region mean
        region_biases = [[] for _ in range(self.n_regions)]
        region_weights = [[] for _ in range(self.n_regions)]

        for b in chromatic:
            region = self._get_region(b.xkcd_hue)  # Use XKCD hue (input)
            region_biases[region].append(b.hue_diff)
            region_weights[region].append(b.n_matches)

        for i in range(self.n_regions):
            if region_biases[i]:
                # Weighted circular mean
                sin_sum = sum(w * math.sin(math.radians(h))
                              for w, h in zip(region_weights[i], region_biases[i]))
                cos_sum = sum(w * math.cos(math.radians(h))
                              for w, h in zip(region_weights[i], region_biases[i]))
                if sin_sum != 0 or cos_sum != 0:
                    self.hue_offsets[i] = math.degrees(math.atan2(sin_sum, cos_sum))

    def predict_hue_correction(self, hue: float, value: float = None, chroma: float = None) -> float:
        region = self._get_region(hue)
        return self.hue_offsets[region]

    def predict_value_correction(self, hue: float = None, value: float = None, chroma: float = None) -> float:
        return self.value_offset

    def predict_chroma_correction(self, hue: float = None, value: float = None, chroma: float = None) -> float:
        return self.chroma_offset


# =============================================================================
# Model 3: Fourier/Trigonometric Polynomial
# =============================================================================

class FourierCorrection:
    """Model hue correction as a Fourier series (captures circular nature)."""

    def __init__(self, n_harmonics: int = 3):
        self.n_harmonics = n_harmonics
        # Coefficients: a0, a1, b1, a2, b2, ...
        self.hue_coeffs = np.zeros(1 + 2 * n_harmonics)
        self.value_offset = 0.0
        self.chroma_offset = 0.0

    def _basis(self, hue: float) -> np.ndarray:
        """Compute Fourier basis functions for a hue."""
        hue_rad = math.radians(hue)
        basis = [1.0]  # constant term
        for k in range(1, self.n_harmonics + 1):
            basis.append(math.cos(k * hue_rad))
            basis.append(math.sin(k * hue_rad))
        return np.array(basis)

    def fit(self, biases: List[CategoryBias]):
        """Fit using weighted least squares."""
        chromatic = [b for b in biases if b.name != 'gray']

        # Value and chroma: global mean
        total_weight = sum(b.n_matches for b in chromatic)
        self.value_offset = sum(b.value_diff * b.n_matches for b in chromatic) / total_weight
        self.chroma_offset = sum(b.chroma_diff * b.n_matches for b in chromatic) / total_weight

        # Hue: weighted least squares on Fourier basis
        n = len(chromatic)
        X = np.zeros((n, len(self.hue_coeffs)))
        y = np.zeros(n)
        w = np.zeros(n)

        for i, b in enumerate(chromatic):
            X[i] = self._basis(b.xkcd_hue)
            y[i] = b.hue_diff
            w[i] = math.sqrt(b.n_matches)  # sqrt for weighted LS

        # Weighted least squares: solve (X'WX)c = X'Wy
        W = np.diag(w)
        XtW = X.T @ W
        try:
            self.hue_coeffs = np.linalg.solve(XtW @ X, XtW @ y)
        except np.linalg.LinAlgError:
            # Fallback to pseudo-inverse
            self.hue_coeffs = np.linalg.lstsq(W @ X, W @ y, rcond=None)[0]

    def predict_hue_correction(self, hue: float, value: float = None, chroma: float = None) -> float:
        basis = self._basis(hue)
        return float(np.dot(self.hue_coeffs, basis))

    def predict_value_correction(self, hue: float = None, value: float = None, chroma: float = None) -> float:
        return self.value_offset

    def predict_chroma_correction(self, hue: float = None, value: float = None, chroma: float = None) -> float:
        return self.chroma_offset


# =============================================================================
# Model 4: Cubic Spline Interpolation
# =============================================================================

class SplineCorrection:
    """Interpolate hue correction using cubic splines."""

    def __init__(self):
        self.spline = None
        self.value_offset = 0.0
        self.chroma_offset = 0.0

    def fit(self, biases: List[CategoryBias]):
        """Fit spline through category centroids."""
        if not HAS_SCIPY:
            return

        chromatic = [b for b in biases if b.name != 'gray']

        # Value and chroma: global mean
        total_weight = sum(b.n_matches for b in chromatic)
        self.value_offset = sum(b.value_diff * b.n_matches for b in chromatic) / total_weight
        self.chroma_offset = sum(b.chroma_diff * b.n_matches for b in chromatic) / total_weight

        # Sort by XKCD hue for spline fitting
        sorted_biases = sorted(chromatic, key=lambda b: b.xkcd_hue)

        hues = [b.xkcd_hue for b in sorted_biases]
        diffs = [b.hue_diff for b in sorted_biases]

        # Handle circular wraparound by extending data
        # Add points before 0 and after 360
        extended_hues = [h - 360 for h in hues] + hues + [h + 360 for h in hues]
        extended_diffs = diffs + diffs + diffs

        # Fit smoothing spline with weights
        weights = [math.sqrt(b.n_matches) for b in sorted_biases]
        extended_weights = weights + weights + weights

        try:
            self.spline = UnivariateSpline(
                extended_hues, extended_diffs,
                w=extended_weights,
                s=len(extended_hues) * 50,  # Smoothing factor
                k=3  # Cubic
            )
        except Exception as e:
            print(f"Spline fitting failed: {e}")
            # Fallback to simple cubic spline
            self.spline = CubicSpline(extended_hues, extended_diffs, bc_type='periodic')

    def predict_hue_correction(self, hue: float, value: float = None, chroma: float = None) -> float:
        if self.spline is None:
            return 0.0
        return float(self.spline(hue))

    def predict_value_correction(self, hue: float = None, value: float = None, chroma: float = None) -> float:
        return self.value_offset

    def predict_chroma_correction(self, hue: float = None, value: float = None, chroma: float = None) -> float:
        return self.chroma_offset


# =============================================================================
# Model 5: Gaussian Process Regression
# =============================================================================

class GPCorrection:
    """Gaussian Process regression with periodic kernel for hue."""

    def __init__(self):
        self.gp = None
        self.value_offset = 0.0
        self.chroma_offset = 0.0
        self._train_X = None
        self._train_y = None

    def fit(self, biases: List[CategoryBias]):
        """Fit GP model."""
        if not HAS_SKLEARN:
            return

        chromatic = [b for b in biases if b.name != 'gray']

        # Value and chroma: global mean
        total_weight = sum(b.n_matches for b in chromatic)
        self.value_offset = sum(b.value_diff * b.n_matches for b in chromatic) / total_weight
        self.chroma_offset = sum(b.chroma_diff * b.n_matches for b in chromatic) / total_weight

        # Prepare data for GP: use sin/cos representation for circularity
        X = np.array([[math.sin(math.radians(b.xkcd_hue)),
                       math.cos(math.radians(b.xkcd_hue))]
                      for b in chromatic])
        y = np.array([b.hue_diff for b in chromatic])

        self._train_X = X
        self._train_y = y

        # Kernel: RBF + White noise (for smooth interpolation)
        kernel = 1.0 * RBF(length_scale=1.0) + WhiteKernel(noise_level=10.0)

        self.gp = GaussianProcessRegressor(
            kernel=kernel,
            alpha=0.1,  # Regularization
            n_restarts_optimizer=5
        )

        self.gp.fit(X, y)

    def predict_hue_correction(self, hue: float, value: float = None, chroma: float = None) -> float:
        if self.gp is None:
            return 0.0
        X = np.array([[math.sin(math.radians(hue)), math.cos(math.radians(hue))]])
        return float(self.gp.predict(X)[0])

    def predict_value_correction(self, hue: float = None, value: float = None, chroma: float = None) -> float:
        return self.value_offset

    def predict_chroma_correction(self, hue: float = None, value: float = None, chroma: float = None) -> float:
        return self.chroma_offset


# =============================================================================
# Evaluation
# =============================================================================

def evaluate_model(model, test_biases: List[CategoryBias]) -> Dict[str, float]:
    """Evaluate model on test data."""
    hue_errors = []
    value_errors = []
    chroma_errors = []
    weighted_hue_errors = []

    for b in test_biases:
        if b.name == 'gray':
            continue

        pred_hue = model.predict_hue_correction(b.xkcd_hue, b.xkcd_value, b.xkcd_chroma)
        pred_value = model.predict_value_correction(b.xkcd_hue, b.xkcd_value, b.xkcd_chroma)
        pred_chroma = model.predict_chroma_correction(b.xkcd_hue, b.xkcd_value, b.xkcd_chroma)

        # Error is difference between predicted correction and actual bias
        hue_err = abs(circular_diff(pred_hue, b.hue_diff))
        value_err = abs(pred_value - b.value_diff)
        chroma_err = abs(pred_chroma - b.chroma_diff)

        hue_errors.append(hue_err)
        value_errors.append(value_err)
        chroma_errors.append(chroma_err)
        weighted_hue_errors.append(hue_err * b.n_matches)

    total_weight = sum(b.n_matches for b in test_biases if b.name != 'gray')

    return {
        'hue_mae': np.mean(hue_errors),
        'hue_rmse': np.sqrt(np.mean([e**2 for e in hue_errors])),
        'hue_max': max(hue_errors),
        'hue_weighted_mae': sum(weighted_hue_errors) / total_weight,
        'value_mae': np.mean(value_errors),
        'chroma_mae': np.mean(chroma_errors),
    }


def leave_one_out_cv(model_class, biases: List[CategoryBias], **kwargs) -> Dict[str, float]:
    """Leave-one-out cross-validation."""
    chromatic = [b for b in biases if b.name != 'gray']

    hue_errors = []
    value_errors = []
    chroma_errors = []
    weights = []

    for i, test_bias in enumerate(chromatic):
        # Train on all but one
        train_biases = [b for j, b in enumerate(chromatic) if j != i]

        # Fit model
        model = model_class(**kwargs)
        model.fit(train_biases)

        # Predict on held-out
        pred_hue = model.predict_hue_correction(test_bias.xkcd_hue)
        hue_err = abs(circular_diff(pred_hue, test_bias.hue_diff))

        pred_value = model.predict_value_correction()
        value_err = abs(pred_value - test_bias.value_diff)

        pred_chroma = model.predict_chroma_correction()
        chroma_err = abs(pred_chroma - test_bias.chroma_diff)

        hue_errors.append(hue_err)
        value_errors.append(value_err)
        chroma_errors.append(chroma_err)
        weights.append(test_bias.n_matches)

    total_weight = sum(weights)

    return {
        'hue_mae': np.mean(hue_errors),
        'hue_rmse': np.sqrt(np.mean([e**2 for e in hue_errors])),
        'hue_max': max(hue_errors),
        'hue_weighted_mae': sum(e * w for e, w in zip(hue_errors, weights)) / total_weight,
        'value_mae': np.mean(value_errors),
        'chroma_mae': np.mean(chroma_errors),
    }


# =============================================================================
# Main
# =============================================================================

def main():
    # Load data
    data_path = Path(__file__).parent / "centore_comparison_results.json"
    biases = load_bias_data(data_path)

    print("=" * 70)
    print("Screen-to-Physical Color Correction Model Comparison")
    print("=" * 70)

    # Filter out gray for hue analysis
    chromatic = [b for b in biases if b.name != 'gray']
    print(f"\nDataset: {len(chromatic)} chromatic categories (gray excluded)")
    print(f"Total matched colors: {sum(b.n_matches for b in chromatic):,}")

    # Print category summary sorted by hue bias
    print("\n" + "-" * 70)
    print("Category Hue Biases (sorted by bias):")
    print("-" * 70)
    for b in sorted(chromatic, key=lambda x: x.hue_diff):
        print(f"  {b.name:12s}  hue={b.xkcd_hue:6.1f}°  bias={b.hue_diff:+6.1f}°  n={b.n_matches:5d}")

    # Define models to compare
    models = [
        ("Global Linear", GlobalLinearCorrection, {}),
        ("Piecewise (6 regions)", PiecewiseLinearCorrection, {'n_regions': 6}),
        ("Piecewise (12 regions)", PiecewiseLinearCorrection, {'n_regions': 12}),
        ("Fourier (2 harmonics)", FourierCorrection, {'n_harmonics': 2}),
        ("Fourier (3 harmonics)", FourierCorrection, {'n_harmonics': 3}),
        ("Fourier (4 harmonics)", FourierCorrection, {'n_harmonics': 4}),
    ]

    if HAS_SCIPY:
        models.append(("Cubic Spline", SplineCorrection, {}))

    if HAS_SKLEARN:
        models.append(("Gaussian Process", GPCorrection, {}))

    # Run leave-one-out cross-validation
    print("\n" + "=" * 70)
    print("Leave-One-Out Cross-Validation Results")
    print("=" * 70)
    print(f"{'Model':<25s} {'Hue MAE':>10s} {'Hue RMSE':>10s} {'Hue Max':>10s} {'Hue W-MAE':>10s}")
    print("-" * 70)

    results = []
    for name, model_class, kwargs in models:
        cv_results = leave_one_out_cv(model_class, biases, **kwargs)
        results.append((name, cv_results))
        print(f"{name:<25s} {cv_results['hue_mae']:>10.2f}° {cv_results['hue_rmse']:>10.2f}° "
              f"{cv_results['hue_max']:>10.2f}° {cv_results['hue_weighted_mae']:>10.2f}°")

    # Find best model
    best_model = min(results, key=lambda x: x[1]['hue_weighted_mae'])
    print("-" * 70)
    print(f"Best model by weighted MAE: {best_model[0]}")

    # Train best model on full data and report
    print("\n" + "=" * 70)
    print(f"Best Model: {best_model[0]}")
    print("=" * 70)

    # Find the corresponding model class
    for name, model_class, kwargs in models:
        if name == best_model[0]:
            final_model = model_class(**kwargs)
            final_model.fit(biases)
            break

    print(f"\nValue correction: -{final_model.value_offset:.3f} (subtract from screen value)")
    print(f"Chroma correction: -{final_model.chroma_offset:.3f} (subtract from screen chroma)")

    print("\nHue correction by input hue:")
    print("-" * 40)
    for hue in range(0, 360, 30):
        correction = final_model.predict_hue_correction(hue)
        print(f"  Input hue {hue:3d}°: correction = {correction:+.1f}°")

    # Print predictions for each category
    print("\n" + "-" * 70)
    print("Per-Category Predictions vs Actual:")
    print("-" * 70)
    print(f"{'Category':<12s} {'Actual':>10s} {'Predicted':>10s} {'Error':>10s}")
    print("-" * 70)

    errors = []
    for b in sorted(chromatic, key=lambda x: x.xkcd_hue):
        pred = final_model.predict_hue_correction(b.xkcd_hue)
        err = abs(circular_diff(pred, b.hue_diff))
        errors.append((b.name, b.hue_diff, pred, err, b.n_matches))
        print(f"{b.name:<12s} {b.hue_diff:>+10.1f}° {pred:>+10.1f}° {err:>10.1f}°")

    print("-" * 70)
    print(f"{'Mean error:':<34s} {np.mean([e[3] for e in errors]):>10.1f}°")

    # Save model parameters for Rust implementation
    print("\n" + "=" * 70)
    print("Model Parameters for Rust Implementation")
    print("=" * 70)

    if isinstance(final_model, FourierCorrection):
        print("\n// Fourier coefficients for hue correction")
        print("// Correction = a0 + sum(a_k * cos(k*hue) + b_k * sin(k*hue))")
        print(f"const VALUE_CORRECTION: f64 = {final_model.value_offset:.6f};")
        print(f"const CHROMA_CORRECTION: f64 = {final_model.chroma_offset:.6f};")
        print(f"const HUE_COEFFS: [f64; {len(final_model.hue_coeffs)}] = [")
        for i, c in enumerate(final_model.hue_coeffs):
            if i == 0:
                print(f"    {c:.6f},  // a0 (constant)")
            elif i % 2 == 1:
                k = (i + 1) // 2
                print(f"    {c:.6f},  // a{k} (cos {k}x)")
            else:
                k = i // 2
                print(f"    {c:.6f},  // b{k} (sin {k}x)")
        print("];")

        # Generate Rust function
        print("\n// Rust implementation:")
        print("fn predict_hue_correction(hue_degrees: f64) -> f64 {")
        print("    let hue_rad = hue_degrees.to_radians();")
        print("    let mut correction = HUE_COEFFS[0];")
        print(f"    for k in 1..={final_model.n_harmonics} {{")
        print("        let idx = 2 * k - 1;")
        print("        correction += HUE_COEFFS[idx] * (k as f64 * hue_rad).cos();")
        print("        correction += HUE_COEFFS[idx + 1] * (k as f64 * hue_rad).sin();")
        print("    }")
        print("    correction")
        print("}")


if __name__ == "__main__":
    main()
