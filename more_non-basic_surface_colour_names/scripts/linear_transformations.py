#!/usr/bin/env python3
"""
Phase 4.2: Linear Transformation Search

Implement and evaluate linear transformation classes for screen-to-surface
color polyhedra transformation:
1. Translation only (3 params)
2. Scaling only (3 params)
3. Global affine (12 params)
4. Per-family affine (12 params per family)
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass, asdict
from scipy.optimize import minimize
from scipy.spatial import ConvexHull
import warnings
from datetime import datetime

# Import loss functions
from loss_functions import (
    TransformationLoss, LossComponents, load_polyhedron,
    centroid_loss, volume_loss, hausdorff_loss
)

BASE_DIR = Path(__file__).parent.parent


@dataclass
class TransformationResult:
    """Result of transformation optimization."""
    name: str
    params: np.ndarray
    initial_loss: float
    final_loss: float
    improvement: float
    centroid_loss: float
    volume_loss: float
    shape_loss: float
    n_iterations: int
    success: bool


class TranslationTransform:
    """Translation-only transformation: T(x) = x + b"""

    n_params = 3
    name = "translation"

    @staticmethod
    def apply(vertices: np.ndarray, params: np.ndarray) -> np.ndarray:
        """Apply translation to vertices."""
        return vertices + params.reshape(1, 3)

    @staticmethod
    def get_initial_params(screen_vertices: np.ndarray,
                           surface_vertices: np.ndarray) -> np.ndarray:
        """Initialize with centroid difference."""
        screen_centroid = np.mean(screen_vertices, axis=0)
        surface_centroid = np.mean(surface_vertices, axis=0)
        return surface_centroid - screen_centroid


class ScalingTransform:
    """Scaling-only transformation: T(x) = s * x (centered)"""

    n_params = 3
    name = "scaling"

    @staticmethod
    def apply(vertices: np.ndarray, params: np.ndarray) -> np.ndarray:
        """Apply per-axis scaling around centroid."""
        centroid = np.mean(vertices, axis=0)
        centered = vertices - centroid
        scaled = centered * params.reshape(1, 3)
        return scaled + centroid

    @staticmethod
    def get_initial_params(screen_vertices: np.ndarray,
                           surface_vertices: np.ndarray) -> np.ndarray:
        """Initialize with range ratios."""
        screen_range = np.ptp(screen_vertices, axis=0)
        surface_range = np.ptp(surface_vertices, axis=0)

        # Avoid division by zero
        screen_range = np.maximum(screen_range, 1e-6)
        ratios = surface_range / screen_range

        return np.clip(ratios, 0.1, 10.0)


class AffineTransform:
    """Full affine transformation: T(x) = Ax + b"""

    n_params = 12  # 3x3 matrix + 3 translation
    name = "affine"

    @staticmethod
    def apply(vertices: np.ndarray, params: np.ndarray) -> np.ndarray:
        """Apply affine transformation."""
        A = params[:9].reshape(3, 3)
        b = params[9:12]
        return vertices @ A.T + b

    @staticmethod
    def get_initial_params(screen_vertices: np.ndarray,
                           surface_vertices: np.ndarray) -> np.ndarray:
        """Initialize with identity matrix and centroid translation."""
        # Identity matrix
        A = np.eye(3).flatten()

        # Translation from centroid difference
        screen_centroid = np.mean(screen_vertices, axis=0)
        surface_centroid = np.mean(surface_vertices, axis=0)
        b = surface_centroid - screen_centroid

        return np.concatenate([A, b])


class TranslationScalingTransform:
    """Combined translation and scaling: T(x) = s * (x - c_screen) + c_surface"""

    n_params = 6  # 3 scale + 3 translation
    name = "translation_scaling"

    @staticmethod
    def apply(vertices: np.ndarray, params: np.ndarray) -> np.ndarray:
        """Apply translation and scaling."""
        scale = params[:3]
        translation = params[3:6]

        centroid = np.mean(vertices, axis=0)
        centered = vertices - centroid
        scaled = centered * scale.reshape(1, 3)
        return scaled + centroid + translation

    @staticmethod
    def get_initial_params(screen_vertices: np.ndarray,
                           surface_vertices: np.ndarray) -> np.ndarray:
        """Initialize with range ratios and centroid diff."""
        # Scale initialization
        screen_range = np.ptp(screen_vertices, axis=0)
        surface_range = np.ptp(surface_vertices, axis=0)
        screen_range = np.maximum(screen_range, 1e-6)
        scale = np.clip(surface_range / screen_range, 0.1, 10.0)

        # Translation initialization
        screen_centroid = np.mean(screen_vertices, axis=0)
        surface_centroid = np.mean(surface_vertices, axis=0)
        translation = surface_centroid - screen_centroid

        return np.concatenate([scale, translation])


def optimize_transformation(transform_class,
                            screen_vertices: np.ndarray,
                            surface_vertices: np.ndarray,
                            loss_fn: TransformationLoss,
                            max_iter: int = 50) -> TransformationResult:
    """Optimize transformation parameters to minimize loss.

    Args:
        transform_class: Transformation class with apply() and get_initial_params()
        screen_vertices: Source polyhedron vertices
        surface_vertices: Target polyhedron vertices
        loss_fn: Loss function to minimize
        max_iter: Maximum iterations for optimizer

    Returns:
        TransformationResult with optimized parameters
    """
    # Get initial parameters
    x0 = transform_class.get_initial_params(screen_vertices, surface_vertices)

    # Compute initial loss
    transformed = transform_class.apply(screen_vertices, x0)
    initial_components = loss_fn(transformed, surface_vertices)
    initial_loss = initial_components.total_loss

    # Define objective function
    def objective(params):
        transformed = transform_class.apply(screen_vertices, params)
        try:
            loss = loss_fn(transformed, surface_vertices)
            return loss.total_loss
        except Exception:
            return 1e6

    # Optimize
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        result = minimize(
            objective,
            x0,
            method='L-BFGS-B',
            options={'maxiter': max_iter, 'disp': False}
        )

    # Compute final loss components
    final_transformed = transform_class.apply(screen_vertices, result.x)
    final_components = loss_fn(final_transformed, surface_vertices)

    improvement = (initial_loss - final_components.total_loss) / max(initial_loss, 1e-6)

    return TransformationResult(
        name=transform_class.name,
        params=result.x,
        initial_loss=initial_loss,
        final_loss=final_components.total_loss,
        improvement=improvement,
        centroid_loss=final_components.centroid_loss,
        volume_loss=final_components.volume_loss,
        shape_loss=final_components.shape_loss,
        n_iterations=result.nit,
        success=result.success
    )


def optimize_global_transformation(transform_class,
                                   families_data: Dict,
                                   loss_fn: TransformationLoss,
                                   max_iter: int = 100) -> Tuple[np.ndarray, Dict]:
    """Optimize a single global transformation across all families.

    Args:
        transform_class: Transformation class to optimize
        families_data: Dict mapping family -> (screen_vertices, surface_vertices)
        loss_fn: Loss function to minimize
        max_iter: Maximum iterations

    Returns:
        Tuple of (optimal_params, per_family_losses)
    """
    # Collect all data for initialization
    all_screen = np.vstack([v[0] for v in families_data.values()])
    all_surface = np.vstack([v[1] for v in families_data.values()])

    x0 = transform_class.get_initial_params(all_screen, all_surface)

    def global_objective(params):
        total_loss = 0.0
        for screen_verts, surface_verts in families_data.values():
            transformed = transform_class.apply(screen_verts, params)
            try:
                loss = loss_fn(transformed, surface_verts)
                total_loss += loss.total_loss
            except Exception:
                total_loss += 100.0
        return total_loss / len(families_data)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        result = minimize(
            global_objective,
            x0,
            method='L-BFGS-B',
            options={'maxiter': max_iter, 'disp': False}
        )

    # Compute per-family losses with optimal params
    per_family = {}
    for family, (screen_verts, surface_verts) in families_data.items():
        transformed = transform_class.apply(screen_verts, result.x)
        try:
            loss = loss_fn(transformed, surface_verts)
            per_family[family] = asdict(loss)
        except Exception:
            per_family[family] = {"total_loss": float('inf')}

    return result.x, per_family


def load_matched_families():
    """Load all matched family polyhedra."""
    matched_file = BASE_DIR / "datasets/matched_families/included_families.json"
    screen_dir = BASE_DIR / "datasets/screen_polyhedra/threshold_0.6"
    surface_dir = BASE_DIR / "datasets/surface_polyhedra"

    with open(matched_file) as f:
        matched = json.load(f)

    families_data = {}
    for family_info in matched:
        family = family_info["family"]

        screen_file = screen_dir / f"{family}_polyhedron.json"
        surface_file = surface_dir / f"{family}_polyhedron.json"

        if not screen_file.exists() or not surface_file.exists():
            continue

        try:
            screen_vertices = load_polyhedron(screen_file)
            surface_vertices = load_polyhedron(surface_file)

            # Skip degenerate cases (like gray/white with 0 chroma)
            if len(screen_vertices) < 4 or len(surface_vertices) < 4:
                continue

            # Check for degenerate dimensions
            screen_range = np.ptp(screen_vertices, axis=0)
            surface_range = np.ptp(surface_vertices, axis=0)
            if np.any(screen_range < 0.01) or np.any(surface_range < 0.01):
                continue

            families_data[family] = (screen_vertices, surface_vertices)

        except Exception:
            pass

    return families_data


def run_transformation_comparison():
    """Compare all transformation classes."""
    print("Phase 4.2: Linear Transformation Search")
    print("=" * 60)

    # Load data
    families_data = load_matched_families()
    print(f"Loaded {len(families_data)} valid families for comparison")

    loss_fn = TransformationLoss(w_centroid=0.4, w_volume=0.3, w_shape=0.3)

    transform_classes = [
        TranslationTransform,
        ScalingTransform,
        TranslationScalingTransform,
        AffineTransform,
    ]

    results = {}

    # Per-family optimization
    print("\n1. Per-Family Optimization")
    print("-" * 40)

    for tclass in transform_classes:
        print(f"\n{tclass.name} ({tclass.n_params} params):")

        family_results = []
        for family, (screen_verts, surface_verts) in families_data.items():
            try:
                result = optimize_transformation(
                    tclass, screen_verts, surface_verts, loss_fn
                )
                family_results.append({
                    "family": family,
                    **asdict(result)
                })
                if result.improvement > 0.1:
                    print(f"  {family}: {result.initial_loss:.3f} -> {result.final_loss:.3f} "
                          f"({result.improvement*100:.1f}% improvement)")
            except Exception as e:
                print(f"  {family}: Error - {e}")

        results[f"per_family_{tclass.name}"] = family_results

        # Summary stats
        if family_results:
            improvements = [r["improvement"] for r in family_results]
            final_losses = [r["final_loss"] for r in family_results]
            print(f"\n  Summary: mean improvement={np.mean(improvements)*100:.1f}%, "
                  f"mean final loss={np.mean(final_losses):.3f}")

    # Global optimization
    print("\n2. Global Transformation Optimization")
    print("-" * 40)

    global_results = {}
    for tclass in transform_classes:
        print(f"\n{tclass.name} (global):")

        try:
            params, per_family_losses = optimize_global_transformation(
                tclass, families_data, loss_fn
            )

            losses = [v["total_loss"] for v in per_family_losses.values()
                      if v["total_loss"] < float('inf')]

            global_results[tclass.name] = {
                "params": params.tolist(),
                "per_family_losses": per_family_losses,
                "mean_loss": float(np.mean(losses)) if losses else float('inf'),
                "std_loss": float(np.std(losses)) if losses else 0.0
            }

            print(f"  Mean loss: {global_results[tclass.name]['mean_loss']:.4f} "
                  f"(±{global_results[tclass.name]['std_loss']:.4f})")

        except Exception as e:
            print(f"  Error: {e}")

    results["global"] = global_results

    return results, families_data


def generate_report(results, families_data):
    """Generate comparison report."""
    report = []
    report.append("# Linear Transformation Comparison Report")
    report.append("")
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"\nFamilies analyzed: {len(families_data)}")
    report.append("")

    # Transformation class descriptions
    report.append("## Transformation Classes")
    report.append("")
    report.append("| Class | Parameters | Description |")
    report.append("|-------|------------|-------------|")
    report.append("| Translation | 3 | T(x) = x + b |")
    report.append("| Scaling | 3 | T(x) = s * (x - centroid) + centroid |")
    report.append("| Translation+Scaling | 6 | Combined translation and per-axis scaling |")
    report.append("| Affine | 12 | T(x) = Ax + b (full 3x3 matrix) |")
    report.append("")

    # Per-family results summary
    report.append("## Per-Family Optimization Results")
    report.append("")

    report.append("| Transform | Mean Improvement | Mean Final Loss | Best Family |")
    report.append("|-----------|------------------|-----------------|-------------|")

    for tclass_name in ["translation", "scaling", "translation_scaling", "affine"]:
        key = f"per_family_{tclass_name}"
        if key in results and results[key]:
            data = results[key]
            improvements = [r["improvement"] for r in data]
            final_losses = [r["final_loss"] for r in data]
            best = min(data, key=lambda x: x["final_loss"])
            report.append(f"| {tclass_name} | {np.mean(improvements)*100:.1f}% | "
                         f"{np.mean(final_losses):.3f} | {best['family']} ({best['final_loss']:.3f}) |")

    report.append("")

    # Global transformation results
    report.append("## Global Transformation Results")
    report.append("")

    if "global" in results:
        report.append("| Transform | Mean Loss | Std Loss |")
        report.append("|-----------|-----------|----------|")
        for name, data in results["global"].items():
            report.append(f"| {name} | {data['mean_loss']:.4f} | {data['std_loss']:.4f} |")
        report.append("")

    # Recommendations
    report.append("## Recommendations")
    report.append("")

    # Find best per-family approach
    best_per_family = None
    best_per_family_loss = float('inf')
    for tclass_name in ["translation", "scaling", "translation_scaling", "affine"]:
        key = f"per_family_{tclass_name}"
        if key in results and results[key]:
            mean_loss = np.mean([r["final_loss"] for r in results[key]])
            if mean_loss < best_per_family_loss:
                best_per_family_loss = mean_loss
                best_per_family = tclass_name

    report.append(f"1. **Best per-family approach**: {best_per_family}")
    report.append(f"   - Mean final loss: {best_per_family_loss:.4f}")
    report.append("")

    if "global" in results:
        best_global = min(results["global"].items(), key=lambda x: x[1]["mean_loss"])
        report.append(f"2. **Best global approach**: {best_global[0]}")
        report.append(f"   - Mean loss: {best_global[1]['mean_loss']:.4f}")
        report.append("")

    report.append("3. **Trade-off analysis**:")
    report.append("   - Per-family: Better fit, but risk of overfitting")
    report.append("   - Global: More generalizable, captures systematic bias")
    report.append("   - Recommendation: Use global for initial correction, per-family for refinement")

    return "\n".join(report)


def main():
    """Run transformation comparison."""
    output_dir = BASE_DIR / "datasets/transformation_analysis"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Run comparison
    results, families_data = run_transformation_comparison()

    # Save results
    results_file = output_dir / "transformation_comparison.json"

    # Convert numpy arrays for JSON serialization
    def convert_for_json(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {k: convert_for_json(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_for_json(v) for v in obj]
        return obj

    with open(results_file, "w") as f:
        json.dump(convert_for_json(results), f, indent=2)
    print(f"\nSaved: {results_file}")

    # Generate report
    report = generate_report(results, families_data)
    report_file = output_dir / "transformation_comparison.md"
    with open(report_file, "w") as f:
        f.write(report)
    print(f"Saved: {report_file}")


if __name__ == "__main__":
    main()
