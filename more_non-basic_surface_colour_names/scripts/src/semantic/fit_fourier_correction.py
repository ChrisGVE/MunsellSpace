#!/usr/bin/env python3
"""
Fit Fourier Harmonic Model for Hue Correction

Uses the circular statistics results from distribution_comparison_methods.py
to fit an optimal Fourier correction model for screen-to-physical hue conversion.
"""

import json
import math
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple

def load_hue_bias_data() -> List[Dict]:
    """Load hue bias data from distribution comparison results."""
    with open('distribution_comparison_results.json', 'r') as f:
        results = json.load(f)

    data = []
    for name, overlay in results['overlays'].items():
        circ_stats = overlay['circular_statistics']['hue']
        data.append({
            'name': name,
            'centore_hue': circ_stats['centore_mean'],
            'xkcd_hue': circ_stats['xkcd_mean'],
            'shift': circ_stats['shift'],  # XKCD - Centore (circular)
            'n_centore': overlay['n_centore'],
            'n_xkcd': overlay['n_xkcd'],
            # Value and chroma shifts
            'value_shift': overlay['circular_statistics']['value']['shift'],
            'chroma_shift': overlay['circular_statistics']['chroma']['shift'],
        })

    return data


def normalize_angle(angle: float) -> float:
    """Normalize angle to [-180, 180] range."""
    while angle > 180:
        angle -= 360
    while angle < -180:
        angle += 360
    return angle


class FourierHueCorrection:
    """Fourier series model for hue correction."""

    def __init__(self, n_harmonics: int = 4):
        self.n_harmonics = n_harmonics
        # Coefficients: a0, a1, b1, a2, b2, ...
        self.coeffs = np.zeros(1 + 2 * n_harmonics)
        self.value_offset = 0.0
        self.chroma_offset = 0.0

    def _basis(self, hue: float) -> np.ndarray:
        """Compute Fourier basis functions for a hue value."""
        # Use Centore hue as the input (ground truth position)
        hue_rad = math.radians(hue)
        basis = [1.0]  # constant term a0
        for k in range(1, self.n_harmonics + 1):
            basis.append(math.cos(k * hue_rad))  # a_k
            basis.append(math.sin(k * hue_rad))  # b_k
        return np.array(basis)

    def fit(self, data: List[Dict], use_centore_hue: bool = True):
        """
        Fit model using weighted least squares.

        Args:
            data: List of bias data dictionaries
            use_centore_hue: If True, use Centore hue as predictor (for correction).
                            If False, use XKCD hue as predictor (for inverse mapping).
        """
        n = len(data)

        # Design matrix
        X = np.zeros((n, len(self.coeffs)))
        y = np.zeros(n)
        weights = np.zeros(n)

        for i, d in enumerate(data):
            hue_input = d['centore_hue'] if use_centore_hue else d['xkcd_hue']
            X[i] = self._basis(hue_input)
            y[i] = normalize_angle(d['shift'])
            weights[i] = np.sqrt(d['n_xkcd'])  # Weight by sample size

        # Weighted least squares
        W = np.diag(weights)
        XtW = X.T @ W
        self.coeffs = np.linalg.lstsq(XtW @ X, XtW @ y, rcond=None)[0]

        # Value and chroma: simple weighted means
        total_weight = sum(d['n_xkcd'] for d in data)
        self.value_offset = sum(d['value_shift'] * d['n_xkcd'] for d in data) / total_weight
        self.chroma_offset = sum(d['chroma_shift'] * d['n_xkcd'] for d in data) / total_weight

    def predict(self, hue: float) -> float:
        """Predict hue shift for a given hue."""
        basis = self._basis(hue)
        return float(np.dot(self.coeffs, basis))

    def get_coefficients(self) -> Dict:
        """Return coefficients in a structured format."""
        result = {'a0': self.coeffs[0]}
        for k in range(1, self.n_harmonics + 1):
            result[f'a{k}'] = self.coeffs[2*k - 1]
            result[f'b{k}'] = self.coeffs[2*k]
        return result


def leave_one_out_cv(data: List[Dict], n_harmonics: int) -> Dict:
    """Leave-one-out cross-validation."""
    errors = []
    weights = []

    for i in range(len(data)):
        # Train on all but one
        train_data = [d for j, d in enumerate(data) if j != i]
        test_d = data[i]

        model = FourierHueCorrection(n_harmonics=n_harmonics)
        model.fit(train_data)

        # Predict on held-out
        pred = model.predict(test_d['centore_hue'])
        actual = normalize_angle(test_d['shift'])
        err = abs(normalize_angle(pred - actual))

        errors.append(err)
        weights.append(test_d['n_xkcd'])

    total_weight = sum(weights)

    return {
        'mae': np.mean(errors),
        'rmse': np.sqrt(np.mean([e**2 for e in errors])),
        'max_error': max(errors),
        'weighted_mae': sum(e * w for e, w in zip(errors, weights)) / total_weight,
    }


def main():
    print("=" * 80)
    print("FOURIER HARMONIC MODEL FOR HUE CORRECTION")
    print("=" * 80)

    # Load data
    data = load_hue_bias_data()
    print(f"\nLoaded {len(data)} overlays")

    # Print data summary
    print("\n" + "-" * 80)
    print("Input Data (sorted by Centore hue):")
    print("-" * 80)
    print(f"{'Overlay':<12} {'Centore H°':>12} {'XKCD H°':>12} {'Shift°':>12} {'N':>8}")
    print("-" * 80)

    for d in sorted(data, key=lambda x: x['centore_hue']):
        shift = normalize_angle(d['shift'])
        print(f"{d['name']:<12} {d['centore_hue']:>12.1f} {d['xkcd_hue']:>12.1f} {shift:>+12.1f} {d['n_xkcd']:>8}")

    # Model comparison via cross-validation
    print("\n" + "=" * 80)
    print("MODEL COMPARISON (Leave-One-Out Cross-Validation)")
    print("=" * 80)
    print(f"{'Model':<25} {'MAE':>10} {'RMSE':>10} {'Max Err':>10} {'W-MAE':>10}")
    print("-" * 80)

    best_model = None
    best_score = float('inf')

    for n_harm in range(1, 7):
        cv_results = leave_one_out_cv(data, n_harm)
        print(f"Fourier ({n_harm} harmonics){'':<10} {cv_results['mae']:>10.2f}° "
              f"{cv_results['rmse']:>10.2f}° {cv_results['max_error']:>10.2f}° "
              f"{cv_results['weighted_mae']:>10.2f}°")

        if cv_results['weighted_mae'] < best_score:
            best_score = cv_results['weighted_mae']
            best_model = n_harm

    print("-" * 80)
    print(f"Best model: Fourier ({best_model} harmonics) with weighted MAE = {best_score:.2f}°")

    # Fit best model on all data
    print("\n" + "=" * 80)
    print(f"FINAL MODEL: FOURIER ({best_model} harmonics)")
    print("=" * 80)

    model = FourierHueCorrection(n_harmonics=best_model)
    model.fit(data)

    # Print coefficients
    coeffs = model.get_coefficients()
    print("\nFourier Coefficients:")
    print("-" * 40)
    for key, value in coeffs.items():
        print(f"  {key}: {value:+.4f}")

    print(f"\nValue offset (mean): {model.value_offset:+.3f}")
    print(f"Chroma offset (mean): {model.chroma_offset:+.3f}")

    # Per-overlay predictions
    print("\n" + "-" * 80)
    print("Per-Overlay Predictions:")
    print("-" * 80)
    print(f"{'Overlay':<12} {'Actual':>12} {'Predicted':>12} {'Error':>10}")
    print("-" * 80)

    residuals = []
    for d in sorted(data, key=lambda x: x['centore_hue']):
        actual = normalize_angle(d['shift'])
        pred = model.predict(d['centore_hue'])
        err = abs(normalize_angle(pred - actual))
        residuals.append({'name': d['name'], 'actual': actual, 'pred': pred, 'error': err})
        print(f"{d['name']:<12} {actual:>+12.1f}° {pred:>+12.1f}° {err:>10.1f}°")

    print("-" * 80)
    print(f"Mean absolute error: {np.mean([r['error'] for r in residuals]):.2f}°")
    print(f"Max absolute error: {max(r['error'] for r in residuals):.2f}° ({max(residuals, key=lambda x: x['error'])['name']})")

    # Generate Rust code
    print("\n" + "=" * 80)
    print("RUST IMPLEMENTATION")
    print("=" * 80)
    print("""
/// Screen-to-physical hue correction using Fourier harmonics.
/// Based on calibration against Centore's colorimetric overlays.
pub struct ScreenToPhysicalCorrection {
    hue_coeffs: Vec<f64>,
    n_harmonics: usize,
    value_offset: f64,
    chroma_offset: f64,
}

impl ScreenToPhysicalCorrection {
    pub fn new() -> Self {
        Self {
            hue_coeffs: vec![""")

    for i, c in enumerate(model.coeffs):
        suffix = "," if i < len(model.coeffs) - 1 else ""
        print(f"                {c:.6f}{suffix}")

    print(f"""            ],
            n_harmonics: {best_model},
            value_offset: {model.value_offset:.6f},
            chroma_offset: {model.chroma_offset:.6f},
        }}
    }}

    /// Predict the hue shift to subtract from screen hue.
    /// Input: hue in degrees (Munsell convention)
    /// Returns: correction in degrees (subtract from screen hue to get physical hue)
    pub fn hue_correction(&self, screen_hue: f64) -> f64 {{
        let hue_rad = screen_hue.to_radians();
        let mut correction = self.hue_coeffs[0];
        for k in 1..=self.n_harmonics {{
            let idx = 2 * k - 1;
            correction += self.hue_coeffs[idx] * (k as f64 * hue_rad).cos();
            correction += self.hue_coeffs[idx + 1] * (k as f64 * hue_rad).sin();
        }}
        correction
    }}

    /// Apply full correction to convert screen color to physical color.
    pub fn correct(&self, screen_hue: f64, screen_value: f64, screen_chroma: f64)
        -> (f64, f64, f64)
    {{
        let mut corrected_hue = screen_hue - self.hue_correction(screen_hue);
        // Normalize to 0-360
        while corrected_hue < 0.0 {{ corrected_hue += 360.0; }}
        while corrected_hue >= 360.0 {{ corrected_hue -= 360.0; }}

        let corrected_value = screen_value - self.value_offset;
        let corrected_chroma = screen_chroma - self.chroma_offset;

        (corrected_hue, corrected_value.max(0.0), corrected_chroma.max(0.0))
    }}
}}""")

    # Save results
    output = {
        'model': {
            'type': 'fourier',
            'n_harmonics': best_model,
            'coefficients': coeffs,
            'value_offset': model.value_offset,
            'chroma_offset': model.chroma_offset,
        },
        'cv_results': {
            'weighted_mae': best_score,
        },
        'per_overlay': residuals,
    }

    with open('fourier_correction_model.json', 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\nModel saved to: fourier_correction_model.json")

    # Generate prediction table for all hues
    print("\n" + "-" * 80)
    print("Hue Correction Table (every 15°):")
    print("-" * 80)
    for hue in range(0, 360, 15):
        correction = model.predict(hue)
        print(f"  Centore hue {hue:3d}° → correction {correction:+.1f}°")


if __name__ == '__main__':
    main()
