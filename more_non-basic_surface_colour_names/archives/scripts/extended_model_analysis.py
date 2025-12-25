#!/usr/bin/env python3
"""
Extended Model Analysis

Additional model selection criteria:
1. AIC/BIC information criteria
2. Nested F-tests for model comparison
3. Bootstrap coefficient stability
4. Analysis of overlays that did NOT improve
"""

import json
import math
import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Tuple
import warnings
warnings.filterwarnings('ignore')


# =============================================================================
# Data Loading (copied from rigorous_validation.py)
# =============================================================================

@dataclass
class OverlayData:
    name: str
    centore_hue: float
    xkcd_hue: float
    shift: float
    n_xkcd: int
    value_shift: float
    chroma_shift: float


def normalize_angle(angle: float) -> float:
    while angle > 180:
        angle -= 360
    while angle < -180:
        angle += 360
    return angle


def load_data() -> List[OverlayData]:
    with open('distribution_comparison_results.json', 'r') as f:
        results = json.load(f)

    data = []
    for name, overlay in results['overlays'].items():
        circ_stats = overlay['circular_statistics']
        data.append(OverlayData(
            name=name,
            centore_hue=circ_stats['hue']['centore_mean'],
            xkcd_hue=circ_stats['hue']['xkcd_mean'],
            shift=normalize_angle(circ_stats['hue']['shift']),
            n_xkcd=overlay['n_xkcd'],
            value_shift=circ_stats['value']['shift'],
            chroma_shift=circ_stats['chroma']['shift'],
        ))
    return data


def circular_diff(a: float, b: float) -> float:
    return normalize_angle(a - b)


# =============================================================================
# Model Classes
# =============================================================================

class FourierModel:
    def __init__(self, n_harmonics: int):
        self.n_harmonics = n_harmonics
        self.n_params = 1 + 2 * n_harmonics
        self.coeffs = np.zeros(self.n_params)

    def _basis(self, hue: float) -> np.ndarray:
        hue_rad = math.radians(hue)
        basis = [1.0]
        for k in range(1, self.n_harmonics + 1):
            basis.append(math.cos(k * hue_rad))
            basis.append(math.sin(k * hue_rad))
        return np.array(basis)

    def fit(self, data: List[OverlayData], use_centore_hue: bool = True):
        n = len(data)
        X = np.zeros((n, self.n_params))
        y = np.zeros(n)
        w = np.zeros(n)

        for i, d in enumerate(data):
            hue = d.centore_hue if use_centore_hue else d.xkcd_hue
            X[i] = self._basis(hue)
            y[i] = d.shift
            w[i] = np.sqrt(d.n_xkcd)

        W = np.diag(w)
        XtW = X.T @ W
        self.coeffs = np.linalg.lstsq(XtW @ X, XtW @ y, rcond=None)[0]

    def predict(self, hue: float) -> float:
        return float(np.dot(self.coeffs, self._basis(hue)))


class GlobalLinearModel:
    def __init__(self):
        self.n_params = 1
        self.offset = 0.0

    def fit(self, data: List[OverlayData], use_centore_hue: bool = True):
        weights = [d.n_xkcd for d in data]
        shifts = [d.shift for d in data]
        sin_sum = sum(w * math.sin(math.radians(s)) for w, s in zip(weights, shifts))
        cos_sum = sum(w * math.cos(math.radians(s)) for w, s in zip(weights, shifts))
        self.offset = math.degrees(math.atan2(sin_sum, cos_sum))

    def predict(self, hue: float) -> float:
        return self.offset


class PiecewiseLinearModel:
    def __init__(self, n_regions: int = 6):
        self.n_regions = n_regions
        self.n_params = n_regions
        self.region_size = 360 / n_regions
        self.offsets = [0.0] * n_regions

    def _get_region(self, hue: float) -> int:
        return int(hue / self.region_size) % self.n_regions

    def fit(self, data: List[OverlayData], use_centore_hue: bool = True):
        region_shifts = [[] for _ in range(self.n_regions)]
        region_weights = [[] for _ in range(self.n_regions)]

        for d in data:
            hue = d.centore_hue if use_centore_hue else d.xkcd_hue
            region = self._get_region(hue)
            region_shifts[region].append(d.shift)
            region_weights[region].append(d.n_xkcd)

        for i in range(self.n_regions):
            if region_shifts[i]:
                sin_sum = sum(w * math.sin(math.radians(s))
                             for w, s in zip(region_weights[i], region_shifts[i]))
                cos_sum = sum(w * math.cos(math.radians(s))
                             for w, s in zip(region_weights[i], region_shifts[i]))
                if sin_sum != 0 or cos_sum != 0:
                    self.offsets[i] = math.degrees(math.atan2(sin_sum, cos_sum))

    def predict(self, hue: float) -> float:
        return self.offsets[self._get_region(hue)]


# =============================================================================
# Metrics
# =============================================================================

def compute_sse(data: List[OverlayData], predict_fn) -> float:
    """Sum of squared errors (unweighted for AIC/BIC)."""
    sse = 0.0
    for d in data:
        pred = predict_fn(d.centore_hue)
        err = circular_diff(pred, d.shift)
        sse += err**2
    return sse


def compute_weighted_sse(data: List[OverlayData], predict_fn) -> float:
    """Weighted sum of squared errors."""
    sse = 0.0
    for d in data:
        pred = predict_fn(d.centore_hue)
        err = circular_diff(pred, d.shift)
        sse += d.n_xkcd * err**2
    return sse


def compute_rss(data: List[OverlayData], predict_fn) -> float:
    """Residual sum of squares."""
    return compute_sse(data, predict_fn)


def compute_mae(data: List[OverlayData], predict_fn) -> float:
    errors = [abs(circular_diff(predict_fn(d.centore_hue), d.shift)) for d in data]
    return np.mean(errors)


def compute_loocv_mae(data: List[OverlayData], model_class, model_kwargs: dict) -> float:
    """Leave-one-out cross-validation MAE."""
    cv_errors = []
    for i in range(len(data)):
        train_data = [d for j, d in enumerate(data) if j != i]
        test_d = data[i]
        model = model_class(**model_kwargs)
        model.fit(train_data)
        pred = model.predict(test_d.centore_hue)
        cv_errors.append(abs(circular_diff(pred, test_d.shift)))
    return np.mean(cv_errors)


# =============================================================================
# PART 1: AIC/BIC Analysis
# =============================================================================

def aic_bic_analysis(data: List[OverlayData]) -> Dict:
    """
    Compute AIC and BIC for each model.

    AIC = n * ln(RSS/n) + 2k
    BIC = n * ln(RSS/n) + k * ln(n)

    Where:
    - n = number of observations
    - k = number of parameters
    - RSS = residual sum of squares

    Lower is better for both.
    """

    print("=" * 80)
    print("PART 1: AIC/BIC INFORMATION CRITERIA")
    print("=" * 80)
    print("\nAIC = n·ln(RSS/n) + 2k")
    print("BIC = n·ln(RSS/n) + k·ln(n)")
    print("Lower values indicate better model (balances fit vs complexity)")

    n = len(data)

    model_configs = [
        ('Global Linear', GlobalLinearModel, {}),
        ('Piecewise 4', PiecewiseLinearModel, {'n_regions': 4}),
        ('Piecewise 6', PiecewiseLinearModel, {'n_regions': 6}),
        ('Piecewise 12', PiecewiseLinearModel, {'n_regions': 12}),
        ('Fourier 1', FourierModel, {'n_harmonics': 1}),
        ('Fourier 2', FourierModel, {'n_harmonics': 2}),
        ('Fourier 3', FourierModel, {'n_harmonics': 3}),
        ('Fourier 4', FourierModel, {'n_harmonics': 4}),
        ('Fourier 5', FourierModel, {'n_harmonics': 5}),
        ('Fourier 6', FourierModel, {'n_harmonics': 6}),
    ]

    results = []

    for name, model_class, model_kwargs in model_configs:
        model = model_class(**model_kwargs)
        model.fit(data)

        k = model.n_params
        rss = compute_rss(data, model.predict)

        # AIC and BIC
        # Using the standard formulation assuming Gaussian errors
        if rss > 0:
            log_likelihood_term = n * np.log(rss / n)
        else:
            log_likelihood_term = -np.inf

        aic = log_likelihood_term + 2 * k
        bic = log_likelihood_term + k * np.log(n)

        # AICc (corrected AIC for small samples)
        if n - k - 1 > 0:
            aicc = aic + (2 * k * (k + 1)) / (n - k - 1)
        else:
            aicc = np.inf

        # CV MAE for comparison
        cv_mae = compute_loocv_mae(data, model_class, model_kwargs)

        results.append({
            'name': name,
            'k': k,
            'rss': rss,
            'aic': aic,
            'aicc': aicc,
            'bic': bic,
            'cv_mae': cv_mae,
        })

    # Find best by each criterion
    best_aic = min(results, key=lambda r: r['aic'])
    best_aicc = min(results, key=lambda r: r['aicc'])
    best_bic = min(results, key=lambda r: r['bic'])

    # Compute delta values (difference from best)
    for r in results:
        r['delta_aic'] = r['aic'] - best_aic['aic']
        r['delta_aicc'] = r['aicc'] - best_aicc['aicc']
        r['delta_bic'] = r['bic'] - best_bic['bic']

    # Print results
    print(f"\n{'Model':<15} {'k':>3} {'RSS':>10} {'AIC':>10} {'ΔAIC':>8} {'AICc':>10} {'BIC':>10} {'ΔBIC':>8}")
    print("-" * 85)

    for r in results:
        aic_marker = " ◄" if r['name'] == best_aic['name'] else ""
        bic_marker = " ◄" if r['name'] == best_bic['name'] else ""
        print(f"{r['name']:<15} {r['k']:>3} {r['rss']:>10.1f} {r['aic']:>10.2f} {r['delta_aic']:>+8.2f}{aic_marker} "
              f"{r['aicc']:>10.2f} {r['bic']:>10.2f} {r['delta_bic']:>+8.2f}{bic_marker}")

    print("\n" + "-" * 85)
    print(f"Best by AIC:  {best_aic['name']} (k={best_aic['k']})")
    print(f"Best by AICc: {best_aicc['name']} (k={best_aicc['k']}) [corrected for small samples]")
    print(f"Best by BIC:  {best_bic['name']} (k={best_bic['k']}) [penalizes complexity more]")

    # Interpretation
    print("\nInterpretation of ΔAIC/ΔBIC:")
    print("  0-2:   Substantial support (models essentially equivalent)")
    print("  2-4:   Less support")
    print("  4-7:   Considerably less support")
    print("  >10:   Essentially no support")

    return {
        'results': results,
        'best_aic': best_aic['name'],
        'best_aicc': best_aicc['name'],
        'best_bic': best_bic['name'],
    }


# =============================================================================
# PART 2: Nested F-Tests
# =============================================================================

def nested_f_tests(data: List[OverlayData]) -> Dict:
    """
    Perform nested F-tests comparing consecutive Fourier models.

    F = [(RSS_reduced - RSS_full) / (df_reduced - df_full)] / [RSS_full / df_full]

    This tests whether adding more harmonics significantly improves the fit.
    """

    print("\n" + "=" * 80)
    print("PART 2: NESTED F-TESTS (Model Comparison)")
    print("=" * 80)
    print("\nTests whether adding complexity significantly improves fit.")
    print("H₀: Simpler model is adequate (additional parameters = 0)")

    n = len(data)
    np.random.seed(42)
    n_perm = 10000

    # Fit all Fourier models
    fourier_models = {}
    for k in range(0, 7):  # 0 = global mean, 1-6 = Fourier harmonics
        if k == 0:
            model = GlobalLinearModel()
        else:
            model = FourierModel(k)
        model.fit(data)
        fourier_models[k] = {
            'model': model,
            'rss': compute_rss(data, model.predict),
            'k': model.n_params,
            'df': n - model.n_params,
        }

    print(f"\n{'Comparison':<25} {'ΔRSS':>10} {'Δk':>4} {'F-stat':>10} {'p-value':>10} {'Result':<15}")
    print("-" * 85)

    results = []

    # Compare consecutive models
    comparisons = [
        ('Global → Fourier 1', 0, 1),
        ('Fourier 1 → Fourier 2', 1, 2),
        ('Fourier 2 → Fourier 3', 2, 3),
        ('Fourier 3 → Fourier 4', 3, 4),
        ('Fourier 4 → Fourier 5', 4, 5),
        ('Fourier 5 → Fourier 6', 5, 6),
    ]

    for name, k_reduced, k_full in comparisons:
        reduced = fourier_models[k_reduced]
        full = fourier_models[k_full]

        delta_rss = reduced['rss'] - full['rss']
        delta_k = full['k'] - reduced['k']
        df_full = full['df']

        if full['rss'] > 0 and df_full > 0:
            f_stat = (delta_rss / delta_k) / (full['rss'] / df_full)
        else:
            f_stat = np.inf

        # Permutation test for p-value
        shifts = np.array([d.shift for d in data])
        null_f_stats = []

        for _ in range(n_perm):
            shuffled_shifts = np.random.permutation(shifts)
            shuffled_data = [OverlayData(d.name, d.centore_hue, d.xkcd_hue, s, d.n_xkcd, d.value_shift, d.chroma_shift)
                            for d, s in zip(data, shuffled_shifts)]

            if k_reduced == 0:
                m_reduced = GlobalLinearModel()
            else:
                m_reduced = FourierModel(k_reduced)
            m_reduced.fit(shuffled_data)

            m_full = FourierModel(k_full)
            m_full.fit(shuffled_data)

            rss_r = compute_rss(shuffled_data, m_reduced.predict)
            rss_f = compute_rss(shuffled_data, m_full.predict)

            if rss_f > 0:
                null_f = ((rss_r - rss_f) / delta_k) / (rss_f / df_full)
                null_f_stats.append(null_f)

        null_f_stats = np.array(null_f_stats)
        p_value = np.mean(null_f_stats >= f_stat)

        significant = p_value < 0.05
        result = "SIGNIFICANT" if significant else "not significant"

        results.append({
            'comparison': name,
            'delta_rss': delta_rss,
            'delta_k': delta_k,
            'f_stat': f_stat,
            'p_value': p_value,
            'significant': significant,
        })

        print(f"{name:<25} {delta_rss:>10.1f} {delta_k:>4} {f_stat:>10.2f} {p_value:>10.4f} {result:<15}")

    # Find the last significant improvement
    last_significant = None
    for r in results:
        if r['significant']:
            last_significant = r['comparison']

    print("\n" + "-" * 85)
    if last_significant:
        print(f"Last significant improvement: {last_significant}")
        # Determine optimal model from F-tests
        for i, r in enumerate(results):
            if not r['significant']:
                if i == 0:
                    optimal = "Global Linear"
                else:
                    optimal = f"Fourier {i}"
                break
        else:
            optimal = "Fourier 6"
        print(f"F-test optimal model: {optimal}")

    return {'comparisons': results}


# =============================================================================
# PART 3: Bootstrap Coefficient Stability
# =============================================================================

def bootstrap_stability_analysis(data: List[OverlayData], n_bootstrap: int = 2000) -> Dict:
    """
    Analyze the stability of model coefficients under bootstrap resampling.

    A stable model should have coefficients that don't vary wildly.
    """

    print("\n" + "=" * 80)
    print("PART 3: BOOTSTRAP COEFFICIENT STABILITY")
    print("=" * 80)
    print("\nMeasures how stable model parameters are under resampling.")
    print("High CV (coefficient of variation) = unstable parameters = overfitting risk")

    np.random.seed(42)

    results = []

    # Test Fourier 1 through 5
    for n_harm in range(1, 6):
        model = FourierModel(n_harm)
        model.fit(data)
        original_coeffs = model.coeffs.copy()

        # Bootstrap
        boot_coeffs = []
        for _ in range(n_bootstrap):
            indices = np.random.choice(len(data), size=len(data), replace=True)
            boot_data = [data[i] for i in indices]
            boot_model = FourierModel(n_harm)
            boot_model.fit(boot_data)
            boot_coeffs.append(boot_model.coeffs)

        boot_coeffs = np.array(boot_coeffs)

        # Compute statistics
        means = np.mean(boot_coeffs, axis=0)
        stds = np.std(boot_coeffs, axis=0)

        # Coefficient of variation (CV) - relative variability
        # Using absolute mean to avoid division issues
        cvs = stds / (np.abs(means) + 1e-10)

        # Mean CV across all coefficients
        mean_cv = np.mean(cvs)
        max_cv = np.max(cvs)

        # Fraction of bootstrap samples where sign of each coeff matches original
        sign_stability = np.mean(np.sign(boot_coeffs) == np.sign(original_coeffs), axis=0)
        mean_sign_stability = np.mean(sign_stability)

        results.append({
            'n_harmonics': n_harm,
            'n_params': model.n_params,
            'mean_cv': mean_cv,
            'max_cv': max_cv,
            'mean_sign_stability': mean_sign_stability,
            'coeff_stds': stds,
            'coeff_means': means,
            'sign_stability': sign_stability,
        })

    # Print summary
    print(f"\n{'Model':<12} {'Params':>6} {'Mean CV':>10} {'Max CV':>10} {'Sign Stability':>15}")
    print("-" * 60)

    for r in results:
        stability_pct = r['mean_sign_stability'] * 100
        cv_flag = " ⚠️" if r['mean_cv'] > 1.0 else ""
        print(f"Fourier {r['n_harmonics']:<5} {r['n_params']:>6} {r['mean_cv']:>10.3f}{cv_flag} "
              f"{r['max_cv']:>10.3f} {stability_pct:>14.1f}%")

    # Detailed coefficient analysis for selected models
    print("\n" + "-" * 60)
    print("Detailed Coefficient Stability (Fourier 1 vs Fourier 4):")
    print("-" * 60)

    for r in results:
        if r['n_harmonics'] in [1, 4]:
            print(f"\nFourier {r['n_harmonics']}:")
            labels = ['a0'] + [item for k in range(1, r['n_harmonics'] + 1) for item in [f'a{k}', f'b{k}']]
            for i, label in enumerate(labels):
                sign_pct = r['sign_stability'][i] * 100
                cv = r['coeff_stds'][i] / (abs(r['coeff_means'][i]) + 1e-10)
                stable = "✓" if sign_pct > 95 and cv < 0.5 else "⚠️" if sign_pct > 80 else "✗"
                print(f"  {label}: mean={r['coeff_means'][i]:+8.2f}, std={r['coeff_stds'][i]:6.2f}, "
                      f"CV={cv:.2f}, sign stable={sign_pct:.0f}% {stable}")

    return {'results': results}


# =============================================================================
# PART 4: Analysis of Non-Improving Overlays
# =============================================================================

def analyze_non_improving_overlays(data: List[OverlayData]) -> Dict:
    """
    Detailed analysis of which overlays improved and which got worse.
    """

    print("\n" + "=" * 80)
    print("PART 4: OVERLAY-BY-OVERLAY ANALYSIS")
    print("=" * 80)

    # Fit the Fourier 1 model (our optimal)
    model = FourierModel(1)
    model.fit(data)

    overlay_results = []

    for d in sorted(data, key=lambda x: x.centore_hue):
        original_error = abs(circular_diff(d.xkcd_hue, d.centore_hue))
        predicted_shift = model.predict(d.centore_hue)
        corrected_hue = (d.xkcd_hue - predicted_shift) % 360
        corrected_error = abs(circular_diff(corrected_hue, d.centore_hue))
        improvement = original_error - corrected_error

        overlay_results.append({
            'name': d.name,
            'centore_hue': d.centore_hue,
            'xkcd_hue': d.xkcd_hue,
            'actual_shift': d.shift,
            'predicted_shift': predicted_shift,
            'prediction_error': circular_diff(predicted_shift, d.shift),
            'original_error': original_error,
            'corrected_error': corrected_error,
            'improvement': improvement,
            'improved': improvement > 0,
            'n_xkcd': d.n_xkcd,
        })

    # Sort by improvement (worst first)
    overlay_results.sort(key=lambda x: x['improvement'])

    print("\nAll overlays sorted by improvement (worst to best):")
    print("-" * 100)
    print(f"{'Overlay':<12} {'Centore H°':>10} {'Actual Shift':>12} {'Predicted':>10} {'Pred Error':>10} "
          f"{'Orig Err':>10} {'Corr Err':>10} {'Δ':>8}")
    print("-" * 100)

    for r in overlay_results:
        status = "✓" if r['improved'] else "✗"
        print(f"{r['name']:<12} {r['centore_hue']:>10.1f} {r['actual_shift']:>+12.1f}° "
              f"{r['predicted_shift']:>+10.1f}° {r['prediction_error']:>+10.1f}° "
              f"{r['original_error']:>10.1f}° {r['corrected_error']:>10.1f}° {r['improvement']:>+8.1f}° {status}")

    # Identify non-improving overlays
    non_improving = [r for r in overlay_results if not r['improved']]
    improving = [r for r in overlay_results if r['improved']]

    print("\n" + "=" * 80)
    print("ANALYSIS OF NON-IMPROVING OVERLAYS")
    print("=" * 80)

    if non_improving:
        print(f"\n{len(non_improving)} overlays got WORSE after correction:")
        print("-" * 80)

        for r in non_improving:
            print(f"\n{r['name'].upper()}:")
            print(f"  Centore reference hue: {r['centore_hue']:.1f}°")
            print(f"  XKCD screen hue: {r['xkcd_hue']:.1f}°")
            print(f"  Actual shift (XKCD - Centore): {r['actual_shift']:+.1f}°")
            print(f"  Model predicted shift: {r['predicted_shift']:+.1f}°")
            print(f"  Prediction error: {r['prediction_error']:+.1f}°")
            print(f"  Original error: {r['original_error']:.1f}° → Corrected error: {r['corrected_error']:.1f}°")
            print(f"  Got WORSE by: {-r['improvement']:.1f}°")
            print(f"  Sample size: {r['n_xkcd']} XKCD colors")

            # Explain why
            print(f"\n  EXPLANATION:")
            if abs(r['actual_shift']) < 20:
                print(f"    - Small actual shift ({r['actual_shift']:+.1f}°) - these colors are already close")
                print(f"    - Model predicts larger correction ({r['predicted_shift']:+.1f}°) based on hue position")
                print(f"    - Applying this correction OVERSHOOTS the target")
            if r['centore_hue'] < 30:
                print(f"    - Located in red region ({r['centore_hue']:.1f}°) - edge of the hue wheel")
                print(f"    - Fourier model captures average behavior, not local anomalies")

    # Statistical comparison
    print("\n" + "-" * 80)
    print("COMPARISON: Improving vs Non-Improving Overlays")
    print("-" * 80)

    imp_shifts = [r['actual_shift'] for r in improving]
    non_shifts = [r['actual_shift'] for r in non_improving]
    imp_hues = [r['centore_hue'] for r in improving]
    non_hues = [r['centore_hue'] for r in non_improving]

    print(f"\nImproving overlays (n={len(improving)}):")
    print(f"  Mean actual shift: {np.mean(imp_shifts):+.1f}° (range: {min(imp_shifts):+.1f}° to {max(imp_shifts):+.1f}°)")
    print(f"  Mean hue position: {np.mean(imp_hues):.1f}°")
    print(f"  Mean original error: {np.mean([r['original_error'] for r in improving]):.1f}°")

    print(f"\nNon-improving overlays (n={len(non_improving)}):")
    print(f"  Mean actual shift: {np.mean(non_shifts):+.1f}° (range: {min(non_shifts):+.1f}° to {max(non_shifts):+.1f}°)")
    print(f"  Mean hue position: {np.mean(non_hues):.1f}°")
    print(f"  Mean original error: {np.mean([r['original_error'] for r in non_improving]):.1f}°")

    print("\nKEY INSIGHT:")
    print("  Non-improving overlays (rose, wine) are in the RED region (hue ~10°) where:")
    print("  1. The actual shift is SMALL (7.7°, 12.1°) - they're already fairly accurate")
    print("  2. The model predicts a LARGER correction based on nearby colors")
    print("  3. This overcorrection makes them worse")
    print("\n  This is a limitation of using only 20 calibration points - local variations")
    print("  in the red region aren't captured by the smooth Fourier curve.")

    return {
        'overlay_results': overlay_results,
        'non_improving': non_improving,
        'improving': improving,
    }


# =============================================================================
# Main
# =============================================================================

def main():
    print("=" * 80)
    print("EXTENDED MODEL ANALYSIS")
    print("=" * 80)

    data = load_data()
    print(f"\nLoaded {len(data)} Centore overlays")

    # Part 1: AIC/BIC
    aic_results = aic_bic_analysis(data)

    # Part 2: Nested F-tests
    ftest_results = nested_f_tests(data)

    # Part 3: Bootstrap stability
    stability_results = bootstrap_stability_analysis(data)

    # Part 4: Non-improving overlays
    overlay_results = analyze_non_improving_overlays(data)

    # Final summary
    print("\n" + "=" * 80)
    print("SUMMARY: MODEL SELECTION CRITERIA COMPARISON")
    print("=" * 80)

    print(f"""
    Criterion               Optimal Model    Reasoning
    ─────────────────────────────────────────────────────────────────────────
    AIC                     {aic_results['best_aic']:<16} Balances fit and complexity
    AICc (small-sample)     {aic_results['best_aicc']:<16} Corrected for n=20
    BIC                     {aic_results['best_bic']:<16} Stronger complexity penalty
    Train-CV Ratio < 1.5    Fourier 1        Heuristic overfitting detection
    F-test (last signif.)   See above        Statistical significance of added params
    Bootstrap Stability     Fourier 1-2      Stable coefficient estimates
    """)

    # Save results
    output = {
        'aic_bic': {
            'best_aic': aic_results['best_aic'],
            'best_aicc': aic_results['best_aicc'],
            'best_bic': aic_results['best_bic'],
        },
        'f_tests': [
            {'comparison': r['comparison'], 'p_value': float(r['p_value']), 'significant': bool(r['significant'])}
            for r in ftest_results['comparisons']
        ],
        'non_improving_overlays': [r['name'] for r in overlay_results['non_improving']],
    }

    with open('extended_model_analysis_results.json', 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to: extended_model_analysis_results.json")


if __name__ == '__main__':
    main()
