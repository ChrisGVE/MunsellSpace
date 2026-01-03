#!/usr/bin/env python3
"""
Extended Domain Comparison: All Methods × All Domains

Tests transformation methods across color space domains:
- Methods: Translation+Scaling, Polynomial (deg 2), Affine
- Domains: Munsell Cartesian, RGB
- Evaluation: Always in Munsell Cartesian (convert back from RGB)

This addresses the question: Do non-linear methods work better in RGB space?
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from scipy.optimize import minimize
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge
import warnings

from loss_functions import TransformationLoss, LossComponents, load_polyhedron
from linear_transformations import (
    load_matched_families, TranslationScalingTransform, AffineTransform,
    optimize_transformation
)

BASE_DIR = Path(__file__).parent.parent


@dataclass
class ExtendedResult:
    """Result of method × domain combination."""
    method: str
    domain: str
    mean_loss: float
    std_loss: float
    per_family_losses: Dict[str, float]


# ============================================================
# Color Space Conversions (Approximate)
# ============================================================

def munsell_to_rgb_approx(vertices: np.ndarray) -> np.ndarray:
    """Convert Munsell Cartesian to approximate RGB.

    Note: This is an approximation. Exact conversion requires
    Munsell renotation data or the MunsellSpace library.
    """
    rgb = np.zeros_like(vertices)

    for i, (x, y, z) in enumerate(vertices):
        # Reconstruct hue and chroma
        chroma = np.sqrt(x**2 + y**2)
        hue_angle = np.arctan2(y, x)
        value = z

        # HSV-like mapping
        v = np.clip(value / 10.0, 0, 1)
        s = np.clip(chroma / 16.0, 0, 1)
        h = (hue_angle + np.pi) / (2 * np.pi)

        # HSV to RGB
        c = v * s
        x_hsv = c * (1 - abs((h * 6) % 2 - 1))
        m = v - c

        h_sector = int(h * 6) % 6
        if h_sector == 0:
            r, g, b = c, x_hsv, 0
        elif h_sector == 1:
            r, g, b = x_hsv, c, 0
        elif h_sector == 2:
            r, g, b = 0, c, x_hsv
        elif h_sector == 3:
            r, g, b = 0, x_hsv, c
        elif h_sector == 4:
            r, g, b = x_hsv, 0, c
        else:
            r, g, b = c, 0, x_hsv

        rgb[i] = [(r + m) * 255, (g + m) * 255, (b + m) * 255]

    return np.clip(rgb, 0, 255)


def rgb_to_munsell_approx(vertices: np.ndarray) -> np.ndarray:
    """Convert RGB to approximate Munsell Cartesian."""
    munsell = np.zeros_like(vertices)

    for i, (r, g, b) in enumerate(vertices):
        # Normalize
        r_n, g_n, b_n = r / 255.0, g / 255.0, b / 255.0

        c_max = max(r_n, g_n, b_n)
        c_min = min(r_n, g_n, b_n)
        delta = c_max - c_min

        # Value
        z = c_max * 10.0

        # Saturation/Chroma
        s = delta / c_max if c_max > 0 else 0
        chroma = s * 16.0

        # Hue
        if delta == 0:
            h_deg = 0
        elif c_max == r_n:
            h_deg = 60 * ((g_n - b_n) / delta % 6)
        elif c_max == g_n:
            h_deg = 60 * ((b_n - r_n) / delta + 2)
        else:
            h_deg = 60 * ((r_n - g_n) / delta + 4)

        hue_rad = np.deg2rad(h_deg)

        x = chroma * np.cos(hue_rad)
        y = chroma * np.sin(hue_rad)

        munsell[i] = [x, y, z]

    return munsell


# ============================================================
# Transformation Methods in Different Domains
# ============================================================

def translation_scaling_munsell(screen: np.ndarray, surface: np.ndarray,
                                loss_fn: TransformationLoss) -> float:
    """Translation+Scaling in Munsell domain."""
    result = optimize_transformation(
        TranslationScalingTransform, screen, surface, loss_fn
    )
    return result.final_loss


def translation_scaling_rgb(screen: np.ndarray, surface: np.ndarray,
                           loss_fn: TransformationLoss) -> float:
    """Translation+Scaling in RGB domain, evaluate in Munsell."""
    # Convert to RGB
    screen_rgb = munsell_to_rgb_approx(screen)
    surface_rgb = munsell_to_rgb_approx(surface)

    # Fit transformation in RGB
    screen_range = np.ptp(screen_rgb, axis=0)
    surface_range = np.ptp(surface_rgb, axis=0)
    scale = surface_range / np.maximum(screen_range, 1e-6)
    scale = np.clip(scale, 0.1, 10.0)

    translation = np.mean(surface_rgb, axis=0) - np.mean(screen_rgb, axis=0)

    # Apply transformation in RGB
    screen_centroid = np.mean(screen_rgb, axis=0)
    transformed_rgb = (screen_rgb - screen_centroid) * scale + screen_centroid + translation
    transformed_rgb = np.clip(transformed_rgb, 0, 255)

    # Convert back to Munsell
    transformed_munsell = rgb_to_munsell_approx(transformed_rgb)

    # Evaluate in Munsell
    try:
        loss = loss_fn(transformed_munsell, surface)
        return loss.total_loss
    except Exception:
        return float('inf')


def polynomial_munsell(screen: np.ndarray, surface: np.ndarray,
                       loss_fn: TransformationLoss, degree: int = 2) -> float:
    """Polynomial transformation in Munsell domain."""
    poly = PolynomialFeatures(degree=degree, include_bias=True)
    X = poly.fit_transform(screen)

    # Fit polynomial for each output dimension
    models = []
    for dim in range(3):
        model = Ridge(alpha=1.0)
        model.fit(X, surface[:, dim])
        models.append(model)

    # Transform
    transformed = np.zeros_like(screen)
    for dim, model in enumerate(models):
        transformed[:, dim] = model.predict(X)

    try:
        loss = loss_fn(transformed, surface)
        return loss.total_loss
    except Exception:
        return float('inf')


def polynomial_rgb(screen: np.ndarray, surface: np.ndarray,
                   loss_fn: TransformationLoss, degree: int = 2) -> float:
    """Polynomial transformation in RGB domain, evaluate in Munsell."""
    # Convert to RGB
    screen_rgb = munsell_to_rgb_approx(screen)
    surface_rgb = munsell_to_rgb_approx(surface)

    # Fit polynomial in RGB
    poly = PolynomialFeatures(degree=degree, include_bias=True)
    X = poly.fit_transform(screen_rgb)

    models = []
    for dim in range(3):
        model = Ridge(alpha=1.0)
        model.fit(X, surface_rgb[:, dim])
        models.append(model)

    # Transform in RGB
    transformed_rgb = np.zeros_like(screen_rgb)
    for dim, model in enumerate(models):
        transformed_rgb[:, dim] = model.predict(X)
    transformed_rgb = np.clip(transformed_rgb, 0, 255)

    # Convert back to Munsell
    transformed_munsell = rgb_to_munsell_approx(transformed_rgb)

    try:
        loss = loss_fn(transformed_munsell, surface)
        return loss.total_loss
    except Exception:
        return float('inf')


def affine_munsell(screen: np.ndarray, surface: np.ndarray,
                   loss_fn: TransformationLoss) -> float:
    """Affine transformation in Munsell domain."""
    result = optimize_transformation(AffineTransform, screen, surface, loss_fn)
    return result.final_loss


def affine_rgb(screen: np.ndarray, surface: np.ndarray,
               loss_fn: TransformationLoss) -> float:
    """Affine transformation in RGB domain, evaluate in Munsell."""
    # Convert to RGB
    screen_rgb = munsell_to_rgb_approx(screen)
    surface_rgb = munsell_to_rgb_approx(surface)

    # Least squares affine fit in RGB
    # Solve: surface = screen @ A.T + b
    n = len(screen_rgb)
    X = np.hstack([screen_rgb, np.ones((n, 1))])

    # Solve for each output dimension
    params = np.linalg.lstsq(X, surface_rgb, rcond=None)[0]
    A = params[:3, :].T
    b = params[3, :]

    # Apply transformation in RGB
    transformed_rgb = screen_rgb @ A.T + b
    transformed_rgb = np.clip(transformed_rgb, 0, 255)

    # Convert back to Munsell
    transformed_munsell = rgb_to_munsell_approx(transformed_rgb)

    try:
        loss = loss_fn(transformed_munsell, surface)
        return loss.total_loss
    except Exception:
        return float('inf')


# ============================================================
# Main Comparison
# ============================================================

def run_extended_comparison():
    """Run comparison of all methods × all domains."""
    print("Extended Domain Comparison: All Methods × All Domains")
    print("=" * 70)

    families_data = load_matched_families()
    print(f"Loaded {len(families_data)} valid families")

    loss_fn = TransformationLoss(w_centroid=0.4, w_volume=0.3, w_shape=0.3)

    # Method × Domain combinations
    combinations = [
        ("Translation+Scaling", "Munsell", translation_scaling_munsell),
        ("Translation+Scaling", "RGB", translation_scaling_rgb),
        ("Polynomial (deg 2)", "Munsell", lambda s, t, l: polynomial_munsell(s, t, l, degree=2)),
        ("Polynomial (deg 2)", "RGB", lambda s, t, l: polynomial_rgb(s, t, l, degree=2)),
        ("Affine", "Munsell", affine_munsell),
        ("Affine", "RGB", affine_rgb),
    ]

    results = []

    for method_name, domain_name, transform_fn in combinations:
        print(f"\n{method_name} in {domain_name} domain:")
        print("-" * 50)

        per_family = {}
        for family, (screen, surface) in families_data.items():
            try:
                loss = transform_fn(screen, surface, loss_fn)
                per_family[family] = loss
            except Exception as e:
                per_family[family] = float('inf')

        valid = [v for v in per_family.values() if v < float('inf')]
        if valid:
            mean_loss = np.mean(valid)
            std_loss = np.std(valid)
            print(f"  Mean loss: {mean_loss:.4f} (±{std_loss:.4f})")

            results.append(ExtendedResult(
                method=method_name,
                domain=domain_name,
                mean_loss=float(mean_loss),
                std_loss=float(std_loss),
                per_family_losses=per_family
            ))

    return results, families_data


def generate_report(results: List[ExtendedResult], families_data: Dict) -> str:
    """Generate comparison report."""
    report = []
    report.append("# Extended Domain Comparison Report")
    report.append("")
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Families analyzed: {len(families_data)}")
    report.append("")

    report.append("## Summary: All Methods × All Domains")
    report.append("")
    report.append("| Method | Domain | Mean Loss | Std Loss |")
    report.append("|--------|--------|-----------|----------|")

    for r in sorted(results, key=lambda x: x.mean_loss):
        report.append(f"| {r.method} | {r.domain} | {r.mean_loss:.4f} | {r.std_loss:.4f} |")

    report.append("")

    # Grouped by method
    report.append("## Analysis by Method")
    report.append("")

    methods = set(r.method for r in results)
    for method in methods:
        method_results = [r for r in results if r.method == method]
        if len(method_results) >= 2:
            munsell = next((r for r in method_results if r.domain == "Munsell"), None)
            rgb = next((r for r in method_results if r.domain == "RGB"), None)

            if munsell and rgb:
                ratio = rgb.mean_loss / munsell.mean_loss if munsell.mean_loss > 0 else float('inf')
                report.append(f"### {method}")
                report.append(f"- Munsell: {munsell.mean_loss:.4f}")
                report.append(f"- RGB: {rgb.mean_loss:.4f}")
                report.append(f"- RGB/Munsell ratio: {ratio:.1f}x")
                report.append("")

    # Key findings
    report.append("## Key Findings")
    report.append("")

    best = min(results, key=lambda x: x.mean_loss)
    report.append(f"1. **Best combination**: {best.method} in {best.domain} domain ({best.mean_loss:.4f})")

    # Check if any RGB method beats Munsell
    munsell_results = [r for r in results if r.domain == "Munsell"]
    rgb_results = [r for r in results if r.domain == "RGB"]

    best_munsell = min(munsell_results, key=lambda x: x.mean_loss).mean_loss
    best_rgb = min(rgb_results, key=lambda x: x.mean_loss).mean_loss

    if best_rgb < best_munsell:
        report.append(f"2. **RGB can outperform Munsell** for some methods")
    else:
        report.append(f"2. **Munsell domain is consistently better** ({best_munsell:.4f} vs {best_rgb:.4f})")

    report.append("")
    report.append("## Limitations")
    report.append("")
    report.append("- RGB↔Munsell conversions are **approximate** (HSV-based)")
    report.append("- Exact conversion requires Munsell renotation data")
    report.append("- Some error in RGB domain is due to conversion, not the method")
    report.append("- Future work: Use MunsellSpace library for accurate conversion")

    return "\n".join(report)


def main():
    """Run extended domain comparison."""
    output_dir = BASE_DIR / "datasets/transformation_analysis"
    output_dir.mkdir(parents=True, exist_ok=True)

    results, families_data = run_extended_comparison()

    # Save results
    results_file = output_dir / "extended_domain_comparison.json"

    with open(results_file, "w") as f:
        json.dump([asdict(r) for r in results], f, indent=2)
    print(f"\nSaved: {results_file}")

    # Generate report
    report = generate_report(results, families_data)
    report_file = output_dir / "extended_domain_comparison.md"
    with open(report_file, "w") as f:
        f.write(report)
    print(f"Saved: {report_file}")


if __name__ == "__main__":
    main()
