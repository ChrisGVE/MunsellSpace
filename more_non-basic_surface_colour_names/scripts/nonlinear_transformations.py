#!/usr/bin/env python3
"""
Phase 4.3: Non-Linear Transformation Search

Implement and evaluate non-linear transformations:
1. Polynomial (degree 2, 3)
2. Radial basis functions (RBF)
3. Thin-plate splines
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from scipy.optimize import minimize
from scipy.interpolate import Rbf
from scipy.spatial import ConvexHull
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_score, KFold
import warnings
from datetime import datetime

from loss_functions import TransformationLoss, load_polyhedron
from linear_transformations import (
    TranslationScalingTransform, load_matched_families, TransformationResult
)

BASE_DIR = Path(__file__).parent.parent


@dataclass
class NonlinearResult:
    """Result of non-linear transformation."""
    name: str
    initial_loss: float
    final_loss: float
    improvement: float
    n_params: int
    cv_score: Optional[float] = None


class PolynomialTransform:
    """Polynomial transformation using feature expansion."""

    def __init__(self, degree: int = 2, alpha: float = 1.0):
        """Initialize polynomial transform.

        Args:
            degree: Polynomial degree (2 or 3)
            alpha: Ridge regularization strength
        """
        self.degree = degree
        self.alpha = alpha
        self.poly = PolynomialFeatures(degree=degree, include_bias=True)
        self.models = [Ridge(alpha=alpha) for _ in range(3)]  # One per output dim
        self.is_fitted = False

    @property
    def name(self):
        return f"polynomial_deg{self.degree}"

    @property
    def n_params(self):
        # Number of polynomial features * 3 output dimensions
        n_features = self.poly.fit_transform(np.zeros((1, 3))).shape[1]
        return n_features * 3

    def fit(self, source: np.ndarray, target: np.ndarray):
        """Fit polynomial transformation from source to target."""
        X = self.poly.fit_transform(source)
        for i, model in enumerate(self.models):
            model.fit(X, target[:, i])
        self.is_fitted = True

    def transform(self, vertices: np.ndarray) -> np.ndarray:
        """Apply learned transformation."""
        if not self.is_fitted:
            raise ValueError("Transform not fitted")
        X = self.poly.transform(vertices)
        result = np.column_stack([
            model.predict(X) for model in self.models
        ])
        return result

    def cross_validate(self, source: np.ndarray, target: np.ndarray,
                       cv: int = 5) -> float:
        """Evaluate with cross-validation."""
        X = self.poly.fit_transform(source)
        scores = []
        for i in range(3):
            cv_scores = cross_val_score(
                Ridge(alpha=self.alpha), X, target[:, i],
                cv=min(cv, len(source)), scoring='r2'
            )
            scores.append(np.mean(cv_scores))
        return np.mean(scores)


class RBFTransform:
    """Radial basis function transformation."""

    def __init__(self, function: str = 'multiquadric', epsilon: float = 1.0):
        """Initialize RBF transform.

        Args:
            function: RBF kernel ('multiquadric', 'gaussian', 'linear', 'thin_plate')
            epsilon: RBF shape parameter
        """
        self.function = function
        self.epsilon = epsilon
        self.rbf_models = None
        self.is_fitted = False

    @property
    def name(self):
        return f"rbf_{self.function}"

    @property
    def n_params(self):
        # Approximate: depends on number of training points
        return "N_points * 3"

    def fit(self, source: np.ndarray, target: np.ndarray):
        """Fit RBF interpolation from source to target."""
        self.rbf_models = []
        for i in range(3):
            rbf = Rbf(source[:, 0], source[:, 1], source[:, 2],
                      target[:, i], function=self.function,
                      epsilon=self.epsilon, smooth=0.1)
            self.rbf_models.append(rbf)
        self.is_fitted = True

    def transform(self, vertices: np.ndarray) -> np.ndarray:
        """Apply RBF interpolation."""
        if not self.is_fitted:
            raise ValueError("Transform not fitted")
        result = np.column_stack([
            rbf(vertices[:, 0], vertices[:, 1], vertices[:, 2])
            for rbf in self.rbf_models
        ])
        return result


class ThinPlateSplineTransform:
    """Thin-plate spline transformation."""

    def __init__(self, smooth: float = 0.0):
        """Initialize thin-plate spline transform.

        Args:
            smooth: Smoothing parameter (0 = interpolation)
        """
        self.smooth = smooth
        self.rbf_models = None
        self.is_fitted = False

    @property
    def name(self):
        return "thin_plate_spline"

    @property
    def n_params(self):
        return "N_points * 3 + 12"  # Control points + affine

    def fit(self, source: np.ndarray, target: np.ndarray):
        """Fit thin-plate spline from source to target."""
        self.rbf_models = []
        for i in range(3):
            rbf = Rbf(source[:, 0], source[:, 1], source[:, 2],
                      target[:, i], function='thin_plate',
                      smooth=self.smooth)
            self.rbf_models.append(rbf)
        self.is_fitted = True

    def transform(self, vertices: np.ndarray) -> np.ndarray:
        """Apply thin-plate spline transformation."""
        if not self.is_fitted:
            raise ValueError("Transform not fitted")
        result = np.column_stack([
            rbf(vertices[:, 0], vertices[:, 1], vertices[:, 2])
            for rbf in self.rbf_models
        ])
        return result


def compute_correspondence(screen_vertices: np.ndarray,
                           surface_vertices: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Compute point correspondences between polyhedra.

    Uses centroid-based correspondence: map points relative to centroids.
    """
    screen_centroid = np.mean(screen_vertices, axis=0)
    surface_centroid = np.mean(surface_vertices, axis=0)

    # Normalize by centering
    screen_centered = screen_vertices - screen_centroid
    surface_centered = surface_vertices - surface_centroid

    # For each screen point, find closest surface point (approximate)
    # This is a simplification - proper correspondence is more complex
    n_screen = len(screen_vertices)
    n_surface = len(surface_vertices)

    # Sample points uniformly if sizes differ significantly
    if n_screen > n_surface:
        indices = np.linspace(0, n_screen - 1, n_surface, dtype=int)
        source = screen_vertices[indices]
        target = surface_vertices
    else:
        indices = np.linspace(0, n_surface - 1, n_screen, dtype=int)
        source = screen_vertices
        target = surface_vertices[indices]

    return source, target


def evaluate_nonlinear_transform(transform, screen_vertices: np.ndarray,
                                 surface_vertices: np.ndarray,
                                 loss_fn: TransformationLoss) -> NonlinearResult:
    """Evaluate a non-linear transformation on a family pair."""
    # Compute initial loss (no transformation)
    initial_loss = loss_fn(screen_vertices, surface_vertices).total_loss

    # Get correspondences
    source, target = compute_correspondence(screen_vertices, surface_vertices)

    # Fit transformation
    try:
        transform.fit(source, target)

        # Transform screen vertices
        transformed = transform.transform(screen_vertices)

        # Compute final loss
        final_loss = loss_fn(transformed, surface_vertices).total_loss

        # Cross-validation score if available
        cv_score = None
        if hasattr(transform, 'cross_validate'):
            try:
                cv_score = transform.cross_validate(source, target)
            except Exception:
                pass

        improvement = (initial_loss - final_loss) / max(initial_loss, 1e-6)

        return NonlinearResult(
            name=transform.name,
            initial_loss=initial_loss,
            final_loss=final_loss,
            improvement=improvement,
            n_params=transform.n_params if isinstance(transform.n_params, int) else 0,
            cv_score=cv_score
        )
    except Exception as e:
        return NonlinearResult(
            name=transform.name,
            initial_loss=initial_loss,
            final_loss=float('inf'),
            improvement=0.0,
            n_params=0,
            cv_score=None
        )


def run_nonlinear_comparison():
    """Compare non-linear transformation classes."""
    print("Phase 4.3: Non-Linear Transformation Search")
    print("=" * 60)

    # Load data
    families_data = load_matched_families()
    print(f"Loaded {len(families_data)} valid families")

    loss_fn = TransformationLoss(w_centroid=0.4, w_volume=0.3, w_shape=0.3)

    # Transformations to test
    transforms = [
        PolynomialTransform(degree=2, alpha=1.0),
        PolynomialTransform(degree=3, alpha=10.0),  # More regularization for degree 3
        RBFTransform(function='multiquadric', epsilon=1.0),
        RBFTransform(function='gaussian', epsilon=2.0),
        ThinPlateSplineTransform(smooth=0.1),
    ]

    results = {t.name: [] for t in transforms}

    print("\nEvaluating non-linear transformations...")
    print("-" * 40)

    for family, (screen_verts, surface_verts) in families_data.items():
        print(f"\n{family}:")

        for transform in transforms:
            # Create fresh transform instance
            if isinstance(transform, PolynomialTransform):
                t = PolynomialTransform(degree=transform.degree, alpha=transform.alpha)
            elif isinstance(transform, RBFTransform):
                t = RBFTransform(function=transform.function, epsilon=transform.epsilon)
            else:
                t = ThinPlateSplineTransform(smooth=transform.smooth)

            result = evaluate_nonlinear_transform(t, screen_verts, surface_verts, loss_fn)
            results[t.name].append({
                "family": family,
                **asdict(result)
            })

            if result.improvement > 0.1:
                print(f"  {t.name}: {result.initial_loss:.3f} -> {result.final_loss:.3f} "
                      f"({result.improvement*100:.1f}%)")

    # Compute summary statistics
    print("\n" + "=" * 60)
    print("Summary Statistics")
    print("-" * 60)

    summary = {}
    for name, family_results in results.items():
        valid_results = [r for r in family_results if r["final_loss"] < float('inf')]
        if valid_results:
            improvements = [r["improvement"] for r in valid_results]
            final_losses = [r["final_loss"] for r in valid_results]
            summary[name] = {
                "mean_improvement": float(np.mean(improvements)),
                "std_improvement": float(np.std(improvements)),
                "mean_final_loss": float(np.mean(final_losses)),
                "std_final_loss": float(np.std(final_losses)),
                "n_valid": len(valid_results)
            }
            print(f"{name}:")
            print(f"  Mean improvement: {summary[name]['mean_improvement']*100:.1f}%")
            print(f"  Mean final loss: {summary[name]['mean_final_loss']:.4f}")

    return results, summary


def compare_with_linear():
    """Compare non-linear results with linear baseline."""
    print("\n" + "=" * 60)
    print("Comparison with Linear Baseline")
    print("-" * 60)

    families_data = load_matched_families()
    loss_fn = TransformationLoss(w_centroid=0.4, w_volume=0.3, w_shape=0.3)

    linear_losses = []
    poly2_losses = []
    tps_losses = []

    for family, (screen_verts, surface_verts) in families_data.items():
        # Linear baseline (translation+scaling)
        from linear_transformations import optimize_transformation
        linear_result = optimize_transformation(
            TranslationScalingTransform, screen_verts, surface_verts, loss_fn
        )
        linear_losses.append(linear_result.final_loss)

        # Polynomial degree 2
        poly = PolynomialTransform(degree=2, alpha=1.0)
        poly_result = evaluate_nonlinear_transform(poly, screen_verts, surface_verts, loss_fn)
        poly2_losses.append(poly_result.final_loss)

        # Thin-plate spline
        tps = ThinPlateSplineTransform(smooth=0.1)
        tps_result = evaluate_nonlinear_transform(tps, screen_verts, surface_verts, loss_fn)
        tps_losses.append(tps_result.final_loss)

    comparison = {
        "translation_scaling": {
            "mean_loss": float(np.mean(linear_losses)),
            "std_loss": float(np.std(linear_losses)),
            "n_params": 6
        },
        "polynomial_deg2": {
            "mean_loss": float(np.mean([l for l in poly2_losses if l < float('inf')])),
            "std_loss": float(np.std([l for l in poly2_losses if l < float('inf')])),
            "n_params": 30  # 10 features * 3 outputs
        },
        "thin_plate_spline": {
            "mean_loss": float(np.mean([l for l in tps_losses if l < float('inf')])),
            "std_loss": float(np.std([l for l in tps_losses if l < float('inf')])),
            "n_params": "N*3"
        }
    }

    print("\n| Method | Mean Loss | Std Loss | Params |")
    print("|--------|-----------|----------|--------|")
    for name, data in comparison.items():
        print(f"| {name} | {data['mean_loss']:.4f} | {data['std_loss']:.4f} | {data['n_params']} |")

    return comparison


def generate_report(results, summary, comparison):
    """Generate comparison report."""
    report = []
    report.append("# Non-Linear Transformation Comparison Report")
    report.append("")
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")

    report.append("## Transformation Classes")
    report.append("")
    report.append("| Class | Parameters | Description |")
    report.append("|-------|------------|-------------|")
    report.append("| Polynomial (deg 2) | 30 | Quadratic features + Ridge regression |")
    report.append("| Polynomial (deg 3) | 60 | Cubic features + Ridge regression |")
    report.append("| RBF Multiquadric | N*3 | φ(r) = sqrt(r² + ε²) |")
    report.append("| RBF Gaussian | N*3 | φ(r) = exp(-r²/ε²) |")
    report.append("| Thin-Plate Spline | N*3+12 | Minimizes bending energy |")
    report.append("")

    report.append("## Summary Results")
    report.append("")
    report.append("| Transform | Mean Improvement | Mean Loss | Valid Families |")
    report.append("|-----------|------------------|-----------|----------------|")
    for name, data in summary.items():
        report.append(f"| {name} | {data['mean_improvement']*100:.1f}% | "
                     f"{data['mean_final_loss']:.4f} | {data['n_valid']} |")
    report.append("")

    report.append("## Comparison with Linear Baseline")
    report.append("")
    report.append("| Method | Mean Loss | Std Loss | Parameters |")
    report.append("|--------|-----------|----------|------------|")
    for name, data in comparison.items():
        report.append(f"| {name} | {data['mean_loss']:.4f} | "
                     f"{data['std_loss']:.4f} | {data['n_params']} |")
    report.append("")

    report.append("## Recommendations")
    report.append("")

    # Find best method
    best_linear = comparison.get("translation_scaling", {}).get("mean_loss", float('inf'))
    best_nonlinear = min(
        comparison.get("polynomial_deg2", {}).get("mean_loss", float('inf')),
        comparison.get("thin_plate_spline", {}).get("mean_loss", float('inf'))
    )

    if best_nonlinear < best_linear * 0.9:
        report.append("1. **Non-linear methods provide significant improvement** over linear baseline")
        report.append(f"   - Linear baseline: {best_linear:.4f}")
        report.append(f"   - Best non-linear: {best_nonlinear:.4f}")
    else:
        report.append("1. **Linear methods remain competitive** - non-linear adds complexity")
        report.append("   without proportional improvement")

    report.append("")
    report.append("2. **Polynomial (degree 2)**: Good balance of flexibility and stability")
    report.append("   - Ridge regularization prevents overfitting")
    report.append("   - Fixed number of parameters")
    report.append("")
    report.append("3. **Thin-plate splines**: Best for smooth interpolation")
    report.append("   - Requires control point correspondences")
    report.append("   - May overfit with few samples")
    report.append("")
    report.append("4. **For production use**:")
    report.append("   - Start with Translation+Scaling (linear)")
    report.append("   - Apply polynomial refinement if residuals are systematic")
    report.append("   - Use TPS only for high-accuracy requirements")

    return "\n".join(report)


def main():
    """Run non-linear transformation comparison."""
    output_dir = BASE_DIR / "datasets/transformation_analysis"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Run comparison
    results, summary = run_nonlinear_comparison()

    # Compare with linear
    comparison = compare_with_linear()

    # Save results
    results_file = output_dir / "nonlinear_comparison.json"

    def convert_for_json(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {k: convert_for_json(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_for_json(v) for v in obj]
        elif isinstance(obj, (np.floating, np.integer)):
            return float(obj)
        return obj

    with open(results_file, "w") as f:
        json.dump(convert_for_json({
            "results": results,
            "summary": summary,
            "comparison": comparison
        }), f, indent=2)
    print(f"\nSaved: {results_file}")

    # Generate report
    report = generate_report(results, summary, comparison)
    report_file = output_dir / "nonlinear_comparison.md"
    with open(report_file, "w") as f:
        f.write(report)
    print(f"Saved: {report_file}")


if __name__ == "__main__":
    main()
