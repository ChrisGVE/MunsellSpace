#!/usr/bin/env python3
"""
Hypothesis Testing for Hue Correction Model Selection

This script tests several null hypotheses to validate that:
1. Hue bias exists (is not zero)
2. The bias is non-uniform (varies by hue region)
3. Fourier 4 provides significant improvement over simpler models
4. The model captures real signal (not just noise)

Note: Uses permutation tests and bootstrap methods to avoid scipy dependency.
"""

import json
import math
import numpy as np
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple


# Simple statistical functions to replace scipy.stats
def t_test_1samp(data, popmean=0):
    """One-sample t-test."""
    n = len(data)
    mean = np.mean(data)
    std = np.std(data, ddof=1)
    se = std / np.sqrt(n)
    t_stat = (mean - popmean) / se if se > 0 else float('inf')
    # Approximate p-value using normal distribution for large n
    # For n=29, this is reasonable
    p_value = 2 * (1 - normal_cdf(abs(t_stat)))
    return t_stat, p_value


def normal_cdf(x):
    """Approximate normal CDF using error function approximation."""
    # Abramowitz and Stegun approximation
    a1 = 0.254829592
    a2 = -0.284496736
    a3 = 1.421413741
    a4 = -1.453152027
    a5 = 1.061405429
    p = 0.3275911

    sign = 1 if x >= 0 else -1
    x = abs(x) / math.sqrt(2)

    t = 1.0 / (1.0 + p * x)
    y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-x * x)

    return 0.5 * (1.0 + sign * y)


def f_cdf(f_stat, df1, df2):
    """Approximate F-distribution CDF using beta function approximation."""
    if f_stat <= 0:
        return 0.0
    x = df1 * f_stat / (df1 * f_stat + df2)
    # Use incomplete beta function approximation
    # For our purposes, use permutation test instead
    return None  # Will use permutation test


def wilcoxon_test(differences):
    """Wilcoxon signed-rank test (simplified).

    Returns: (statistic, p_value_two_sided, p_value_one_sided_greater)

    The one-sided p-value tests H₁: median(differences) > 0.
    """
    # Remove zeros
    differences = differences[differences != 0]
    n = len(differences)
    if n == 0:
        return 0, 1.0, 0.5

    # Rank absolute values
    abs_diff = np.abs(differences)
    ranks = np.argsort(np.argsort(abs_diff)) + 1

    # Sum of positive ranks
    w_plus = np.sum(ranks[differences > 0])
    w_minus = np.sum(ranks[differences < 0])
    w = min(w_plus, w_minus)

    # Normal approximation for n >= 10
    mean_w = n * (n + 1) / 4
    std_w = np.sqrt(n * (n + 1) * (2 * n + 1) / 24)
    z = (w - mean_w) / std_w if std_w > 0 else 0

    p_value_two_sided = 2 * (1 - normal_cdf(abs(z)))

    # One-sided: test if differences are positive (Fourier better)
    # Use z-score based on W+ vs expected
    z_one_sided = (w_plus - mean_w) / std_w if std_w > 0 else 0
    p_value_one_sided = 1 - normal_cdf(z_one_sided)

    return w, p_value_two_sided, p_value_one_sided


def binomial_test(successes, n, p=0.5):
    """Approximate binomial test using normal approximation."""
    mean = n * p
    std = np.sqrt(n * p * (1 - p))
    z = (successes - mean) / std if std > 0 else 0
    p_value = 1 - normal_cdf(z)  # one-sided
    return p_value


@dataclass
class CategoryBias:
    name: str
    xkcd_hue: float
    hue_diff: float
    n_matches: int


def load_bias_data(filepath: Path) -> List[CategoryBias]:
    with open(filepath) as f:
        data = json.load(f)

    biases = []
    for cat, info in data['comparisons'].items():
        if cat == 'gray':  # Skip neutral
            continue
        bias = CategoryBias(
            name=cat,
            xkcd_hue=info['xkcd_centroid']['hue_num'],
            hue_diff=info['bias']['hue_diff'],
            n_matches=info['xkcd_matches'],
        )
        biases.append(bias)
    return biases


def circular_diff(a: float, b: float) -> float:
    diff = a - b
    while diff > 180:
        diff -= 360
    while diff < -180:
        diff += 360
    return diff


# =============================================================================
# Models (simplified for hypothesis testing)
# =============================================================================

def fit_global_linear(biases: List[CategoryBias]) -> float:
    """Return weighted circular mean of biases."""
    weights = [b.n_matches for b in biases]
    hue_diffs = [b.hue_diff for b in biases]
    sin_sum = sum(w * math.sin(math.radians(h)) for w, h in zip(weights, hue_diffs))
    cos_sum = sum(w * math.cos(math.radians(h)) for w, h in zip(weights, hue_diffs))
    return math.degrees(math.atan2(sin_sum, cos_sum))


def fit_fourier(biases: List[CategoryBias], n_harmonics: int) -> np.ndarray:
    """Fit Fourier model and return coefficients."""
    n_params = 1 + 2 * n_harmonics
    n = len(biases)

    X = np.zeros((n, n_params))
    y = np.zeros(n)
    w = np.zeros(n)

    for i, b in enumerate(biases):
        hue_rad = math.radians(b.xkcd_hue)
        X[i, 0] = 1.0
        for k in range(1, n_harmonics + 1):
            X[i, 2*k - 1] = math.cos(k * hue_rad)
            X[i, 2*k] = math.sin(k * hue_rad)
        y[i] = b.hue_diff
        w[i] = math.sqrt(b.n_matches)

    W = np.diag(w)
    XtW = X.T @ W
    coeffs = np.linalg.solve(XtW @ X, XtW @ y)
    return coeffs


def predict_fourier(hue: float, coeffs: np.ndarray) -> float:
    n_harmonics = (len(coeffs) - 1) // 2
    hue_rad = math.radians(hue)
    pred = coeffs[0]
    for k in range(1, n_harmonics + 1):
        pred += coeffs[2*k - 1] * math.cos(k * hue_rad)
        pred += coeffs[2*k] * math.sin(k * hue_rad)
    return pred


def compute_sse(biases: List[CategoryBias], predict_fn) -> float:
    """Sum of squared errors (weighted)."""
    sse = 0.0
    for b in biases:
        pred = predict_fn(b.xkcd_hue)
        err = circular_diff(pred, b.hue_diff)
        sse += b.n_matches * err**2
    return sse


def compute_weighted_mae(biases: List[CategoryBias], predict_fn) -> float:
    total_weight = sum(b.n_matches for b in biases)
    weighted_err = sum(abs(circular_diff(predict_fn(b.xkcd_hue), b.hue_diff)) * b.n_matches
                       for b in biases)
    return weighted_err / total_weight


# =============================================================================
# Hypothesis Test 1: Is hue bias significantly different from zero?
# =============================================================================

def test_bias_not_zero(biases: List[CategoryBias], n_permutations: int = 10000) -> dict:
    """
    H₀: Mean hue bias = 0 (no systematic difference between screen and physical)
    H₁: Mean hue bias ≠ 0

    Test: One-sample t-test on circular mean, plus permutation test
    """
    hue_diffs = np.array([b.hue_diff for b in biases])
    weights = np.array([b.n_matches for b in biases])

    # Weighted mean
    weighted_mean = np.sum(hue_diffs * weights) / np.sum(weights)

    # One-sample t-test (treating as linear for small angles)
    t_stat, p_value_ttest = t_test_1samp(hue_diffs, 0)

    # Permutation test: under H₀, signs of biases are random
    np.random.seed(42)
    observed_mean = np.mean(hue_diffs)
    null_means = []
    for _ in range(n_permutations):
        # Randomly flip signs
        signs = np.random.choice([-1, 1], size=len(hue_diffs))
        null_means.append(np.mean(hue_diffs * signs))

    null_means = np.array(null_means)
    p_value_perm = np.mean(np.abs(null_means) >= np.abs(observed_mean))

    return {
        'test': 'H₀: Mean hue bias = 0',
        'observed_mean': observed_mean,
        'weighted_mean': weighted_mean,
        't_statistic': t_stat,
        'p_value_ttest': p_value_ttest,
        'p_value_permutation': p_value_perm,
        'reject_H0': p_value_perm < 0.05,
    }


# =============================================================================
# Hypothesis Test 2: Is hue bias non-uniform (varies by region)?
# =============================================================================

def test_bias_nonuniform(biases: List[CategoryBias], n_permutations: int = 10000) -> dict:
    """
    H₀: Hue bias is constant (doesn't vary with hue position)
    H₁: Hue bias varies with hue position

    Test: Compare variance of biases to variance under shuffled assignment
    """
    hue_diffs = np.array([b.hue_diff for b in biases])

    # Observed variance
    observed_var = np.var(hue_diffs)

    # Under H₀, the assignment of biases to hue positions is random
    # We shuffle biases and measure if real data has structure
    np.random.seed(42)

    # Use Fourier 1 R² as test statistic (captures hue-dependence)
    coeffs = fit_fourier(biases, n_harmonics=1)

    # Compute R² for observed data
    ss_total = sum((b.hue_diff - np.mean(hue_diffs))**2 for b in biases)
    ss_resid = sum((b.hue_diff - predict_fourier(b.xkcd_hue, coeffs))**2 for b in biases)
    observed_r2 = 1 - ss_resid / ss_total if ss_total > 0 else 0

    # Permutation: shuffle biases among hue positions
    null_r2s = []
    for _ in range(n_permutations):
        shuffled_diffs = np.random.permutation(hue_diffs)
        shuffled_biases = [CategoryBias(b.name, b.xkcd_hue, d, b.n_matches)
                          for b, d in zip(biases, shuffled_diffs)]
        coeffs_null = fit_fourier(shuffled_biases, n_harmonics=1)
        ss_resid_null = sum((sb.hue_diff - predict_fourier(sb.xkcd_hue, coeffs_null))**2
                           for sb in shuffled_biases)
        r2_null = 1 - ss_resid_null / ss_total if ss_total > 0 else 0
        null_r2s.append(r2_null)

    null_r2s = np.array(null_r2s)
    p_value = np.mean(null_r2s >= observed_r2)

    return {
        'test': 'H₀: Hue bias is uniform (constant)',
        'observed_variance': observed_var,
        'observed_r2_fourier1': observed_r2,
        'null_r2_mean': np.mean(null_r2s),
        'null_r2_95th': np.percentile(null_r2s, 95),
        'p_value': p_value,
        'reject_H0': p_value < 0.05,
    }


# =============================================================================
# Hypothesis Test 3: Does Fourier 4 improve over Fourier 3? (Nested model F-test)
# =============================================================================

def test_fourier4_vs_fourier3(biases: List[CategoryBias]) -> dict:
    """
    H₀: Fourier 4 is no better than Fourier 3 (4th harmonic coefficients = 0)
    H₁: Fourier 4 provides significant improvement

    Test: F-test for nested models
    """
    n = len(biases)
    total_weight = sum(b.n_matches for b in biases)

    # Fit both models
    coeffs3 = fit_fourier(biases, n_harmonics=3)
    coeffs4 = fit_fourier(biases, n_harmonics=4)

    # Compute weighted SSE for each
    sse3 = compute_sse(biases, lambda h: predict_fourier(h, coeffs3))
    sse4 = compute_sse(biases, lambda h: predict_fourier(h, coeffs4))

    # Degrees of freedom
    p3 = 7  # 1 + 2*3 parameters
    p4 = 9  # 1 + 2*4 parameters
    df1 = p4 - p3  # Additional parameters (2)
    df2 = n - p4   # Residual DoF for larger model

    # F statistic
    if sse4 > 0 and df2 > 0:
        f_stat = ((sse3 - sse4) / df1) / (sse4 / df2)
    else:
        f_stat = float('inf')

    # Permutation test for F-test
    np.random.seed(42)
    n_perm = 10000
    hue_diffs = np.array([b.hue_diff for b in biases])
    null_f_stats = []
    for _ in range(n_perm):
        shuffled = np.random.permutation(hue_diffs)
        shuffled_biases = [CategoryBias(b.name, b.xkcd_hue, d, b.n_matches)
                          for b, d in zip(biases, shuffled)]
        c3 = fit_fourier(shuffled_biases, n_harmonics=3)
        c4 = fit_fourier(shuffled_biases, n_harmonics=4)
        sse3_null = compute_sse(shuffled_biases, lambda h: predict_fourier(h, c3))
        sse4_null = compute_sse(shuffled_biases, lambda h: predict_fourier(h, c4))
        if sse4_null > 0:
            f_null = ((sse3_null - sse4_null) / df1) / (sse4_null / df2)
            null_f_stats.append(f_null)
    p_value = np.mean(np.array(null_f_stats) >= f_stat) if null_f_stats else 1.0

    return {
        'test': 'H₀: Fourier 4 = Fourier 3 (4th harmonic not needed)',
        'sse_fourier3': sse3,
        'sse_fourier4': sse4,
        'sse_reduction': sse3 - sse4,
        'sse_reduction_pct': (sse3 - sse4) / sse3 * 100 if sse3 > 0 else 0,
        'f_statistic': f_stat,
        'df1': df1,
        'df2': df2,
        'p_value': p_value,
        'reject_H0': p_value < 0.05,
    }


# =============================================================================
# Hypothesis Test 4: Does Fourier 4 improve over Global Linear?
# =============================================================================

def test_fourier4_vs_linear(biases: List[CategoryBias]) -> dict:
    """
    H₀: Fourier 4 is no better than global linear (all Fourier coefficients except a₀ = 0)
    H₁: Fourier 4 provides significant improvement

    Test: F-test for nested models
    """
    n = len(biases)

    # Fit models
    global_mean = fit_global_linear(biases)
    coeffs4 = fit_fourier(biases, n_harmonics=4)

    # SSE
    sse_linear = compute_sse(biases, lambda h: global_mean)
    sse_fourier4 = compute_sse(biases, lambda h: predict_fourier(h, coeffs4))

    # Degrees of freedom
    p_linear = 1
    p_fourier4 = 9
    df1 = p_fourier4 - p_linear  # 8 additional parameters
    df2 = n - p_fourier4

    # F statistic
    if sse_fourier4 > 0 and df2 > 0:
        f_stat = ((sse_linear - sse_fourier4) / df1) / (sse_fourier4 / df2)
    else:
        f_stat = float('inf')

    # Permutation test for significance
    np.random.seed(42)
    n_perm = 10000
    hue_diffs = np.array([b.hue_diff for b in biases])
    null_f_stats = []
    for _ in range(n_perm):
        shuffled = np.random.permutation(hue_diffs)
        shuffled_biases = [CategoryBias(b.name, b.xkcd_hue, d, b.n_matches)
                          for b, d in zip(biases, shuffled)]
        gm_null = fit_global_linear(shuffled_biases)
        c4_null = fit_fourier(shuffled_biases, n_harmonics=4)
        sse_l_null = compute_sse(shuffled_biases, lambda h: gm_null)
        sse_f_null = compute_sse(shuffled_biases, lambda h: predict_fourier(h, c4_null))
        if sse_f_null > 0:
            f_null = ((sse_l_null - sse_f_null) / df1) / (sse_f_null / df2)
            null_f_stats.append(f_null)
    p_value = np.mean(np.array(null_f_stats) >= f_stat) if null_f_stats else 1.0

    # Also compute improvement in MAE
    mae_linear = compute_weighted_mae(biases, lambda h: global_mean)
    mae_fourier4 = compute_weighted_mae(biases, lambda h: predict_fourier(h, coeffs4))

    return {
        'test': 'H₀: Fourier 4 = Global Linear (hue-dependent terms not needed)',
        'sse_linear': sse_linear,
        'sse_fourier4': sse_fourier4,
        'sse_reduction_pct': (sse_linear - sse_fourier4) / sse_linear * 100,
        'mae_linear': mae_linear,
        'mae_fourier4': mae_fourier4,
        'mae_improvement': mae_linear - mae_fourier4,
        'f_statistic': f_stat,
        'df1': df1,
        'df2': df2,
        'p_value': p_value,
        'reject_H0': p_value < 0.05,
    }


# =============================================================================
# Hypothesis Test 5: Permutation test - is model capturing signal or noise?
# =============================================================================

def test_model_vs_noise(biases: List[CategoryBias], n_permutations: int = 10000) -> dict:
    """
    H₀: The Fourier 4 model captures noise (hue-bias relationship is random)
    H₁: The model captures real signal

    Test: Permutation test - shuffle biases and compare model fit
    """
    np.random.seed(42)

    # Observed model performance
    coeffs = fit_fourier(biases, n_harmonics=4)
    observed_mae = compute_weighted_mae(biases, lambda h: predict_fourier(h, coeffs))

    hue_diffs = np.array([b.hue_diff for b in biases])

    # Null distribution: shuffle biases among positions
    null_maes = []
    for _ in range(n_permutations):
        shuffled_diffs = np.random.permutation(hue_diffs)
        shuffled_biases = [CategoryBias(b.name, b.xkcd_hue, d, b.n_matches)
                          for b, d in zip(biases, shuffled_diffs)]
        coeffs_null = fit_fourier(shuffled_biases, n_harmonics=4)
        mae_null = compute_weighted_mae(shuffled_biases,
                                        lambda h: predict_fourier(h, coeffs_null))
        null_maes.append(mae_null)

    null_maes = np.array(null_maes)
    p_value = np.mean(null_maes <= observed_mae)

    return {
        'test': 'H₀: Model captures noise (no real hue-bias relationship)',
        'observed_mae': observed_mae,
        'null_mae_mean': np.mean(null_maes),
        'null_mae_5th_percentile': np.percentile(null_maes, 5),
        'null_mae_median': np.median(null_maes),
        'p_value': p_value,
        'reject_H0': p_value < 0.05,
    }


# =============================================================================
# Hypothesis Test 6: Paired comparison of model errors
# =============================================================================

def test_paired_improvement(biases: List[CategoryBias]) -> dict:
    """
    H₀: Fourier 4 errors = Global Linear errors (no improvement)
    H₁: Fourier 4 errors < Global Linear errors

    Test: Wilcoxon signed-rank test on paired errors
    """
    global_mean = fit_global_linear(biases)
    coeffs4 = fit_fourier(biases, n_harmonics=4)

    errors_linear = []
    errors_fourier4 = []

    for b in biases:
        err_linear = abs(circular_diff(global_mean, b.hue_diff))
        err_fourier = abs(circular_diff(predict_fourier(b.xkcd_hue, coeffs4), b.hue_diff))
        errors_linear.append(err_linear)
        errors_fourier4.append(err_fourier)

    errors_linear = np.array(errors_linear)
    errors_fourier4 = np.array(errors_fourier4)
    differences = errors_linear - errors_fourier4

    # Wilcoxon signed-rank test (one-sided: Fourier better)
    stat, p_value_two_sided, p_value_greater = wilcoxon_test(differences)

    # Sign test
    n_improved = np.sum(differences > 0)
    n_worse = np.sum(differences < 0)
    sign_test_p = binomial_test(n_improved, n_improved + n_worse, 0.5)

    return {
        'test': 'H₀: Fourier 4 errors = Linear errors',
        'mean_error_linear': np.mean(errors_linear),
        'mean_error_fourier4': np.mean(errors_fourier4),
        'mean_improvement': np.mean(differences),
        'n_categories_improved': n_improved,
        'n_categories_worse': n_worse,
        'wilcoxon_statistic': stat,
        'p_value_two_sided': p_value_two_sided,
        'p_value_one_sided': p_value_greater,
        'sign_test_p_value': sign_test_p,
        'reject_H0': p_value_greater < 0.05,
    }


# =============================================================================
# Main
# =============================================================================

def main():
    data_path = Path(__file__).parent / "centore_comparison_results.json"
    biases = load_bias_data(data_path)

    print("=" * 80)
    print("HYPOTHESIS TESTING FOR HUE CORRECTION MODEL")
    print("=" * 80)
    print(f"\nDataset: {len(biases)} chromatic categories")
    print(f"Significance level: α = 0.05")

    # Run all tests
    tests = [
        test_bias_not_zero(biases),
        test_bias_nonuniform(biases),
        test_fourier4_vs_linear(biases),
        test_fourier4_vs_fourier3(biases),
        test_model_vs_noise(biases),
        test_paired_improvement(biases),
    ]

    for i, result in enumerate(tests, 1):
        print("\n" + "=" * 80)
        print(f"TEST {i}: {result['test']}")
        print("=" * 80)

        for key, value in result.items():
            if key == 'test':
                continue
            if isinstance(value, float):
                if 'p_value' in key.lower():
                    print(f"  {key}: {value:.6f}" + (" ***" if value < 0.001 else " **" if value < 0.01 else " *" if value < 0.05 else ""))
                else:
                    print(f"  {key}: {value:.4f}")
            elif isinstance(value, bool):
                print(f"  {key}: {'YES' if value else 'NO'}")
            else:
                print(f"  {key}: {value}")

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY OF HYPOTHESIS TESTS")
    print("=" * 80)
    print("\n  Significance levels: * p<0.05, ** p<0.01, *** p<0.001\n")

    print(f"  Test 1 (Bias ≠ 0):           {'REJECT H₀' if tests[0]['reject_H0'] else 'FAIL TO REJECT'}")
    print(f"  Test 2 (Bias non-uniform):   {'REJECT H₀' if tests[1]['reject_H0'] else 'FAIL TO REJECT'}")
    print(f"  Test 3 (F4 > Linear):        {'REJECT H₀' if tests[2]['reject_H0'] else 'FAIL TO REJECT'}")
    print(f"  Test 4 (F4 > F3):            {'REJECT H₀' if tests[3]['reject_H0'] else 'FAIL TO REJECT'}")
    print(f"  Test 5 (Model > Noise):      {'REJECT H₀' if tests[4]['reject_H0'] else 'FAIL TO REJECT'}")
    print(f"  Test 6 (Paired improvement): {'REJECT H₀' if tests[5]['reject_H0'] else 'FAIL TO REJECT'}")

    print("\n" + "=" * 80)
    print("CONCLUSION")
    print("=" * 80)

    all_rejected = all(t['reject_H0'] for t in tests)

    if all_rejected:
        print("""
  All null hypotheses are REJECTED at α = 0.05:

  1. Hue bias IS significantly different from zero
  2. Hue bias IS non-uniform (varies by hue region)
  3. Fourier 4 IS significantly better than global linear
  4. Fourier 4 IS significantly better than Fourier 3
  5. The model IS capturing real signal (not noise)
  6. Improvement IS statistically significant across categories

  The Fourier 4 harmonic model is statistically justified.
""")
    else:
        failed = [i+1 for i, t in enumerate(tests) if not t['reject_H0']]
        print(f"\n  Some null hypotheses could not be rejected: Tests {failed}")
        print("  Review the specific test results above for interpretation.")


if __name__ == "__main__":
    main()
