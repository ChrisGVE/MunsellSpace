#!/usr/bin/env python3
"""
Phase 5 Transformation Research Visualizations (Task 114)

Generates publication-quality figures for Phase 5 research:
1. Pareto frontier 3D scatter plot
2. Loss correlation heatmap
3. Aggregation method comparison
4. Per-family loss distributions
5. Jacobian spatial distribution
6. Volume stability convergence

Output: datasets/transformation_analysis/figures/
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from mpl_toolkits.mplot3d import Axes3D


# Configure matplotlib for publication quality
def setup_style():
    """Configure matplotlib/seaborn style."""
    sns.set_context("paper", font_scale=1.2)
    sns.set_style("whitegrid")
    plt.rcParams.update({
        'figure.dpi': 150,
        'savefig.dpi': 300,
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'DejaVu Sans', 'Helvetica'],
        'axes.labelsize': 12,
        'axes.titlesize': 14,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.titlesize': 16,
    })


BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "datasets" / "transformation_analysis"
FIGURES_DIR = DATA_DIR / "figures"


def save_figure(fig, filename: str):
    """Save figure in PNG and SVG formats."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    png_path = FIGURES_DIR / f"{filename}.png"
    svg_path = FIGURES_DIR / f"{filename}.svg"

    fig.savefig(png_path, dpi=300, bbox_inches='tight', facecolor='white')
    fig.savefig(svg_path, format='svg', bbox_inches='tight')
    print(f"  Saved: {png_path.name}, {svg_path.name}")
    plt.close(fig)


def load_json(filename: str) -> Optional[Dict]:
    """Load JSON file from DATA_DIR."""
    path = DATA_DIR / filename
    if not path.exists():
        print(f"  Warning: {filename} not found")
        return None
    with open(path) as f:
        return json.load(f)


# ============================================================================
# Visualization 1: Pareto Frontier 3D Scatter
# ============================================================================

def plot_pareto_frontier_3d():
    """Generate 3D Pareto frontier visualization from Phase 5.1."""
    print("\n1. Pareto Frontier 3D Plot...")

    data = load_json("pareto_analysis.json")
    if not data:
        print("  Skipping: pareto_analysis.json not found")
        return

    # Data structure: all_points is a list of strategy dicts
    strategies = data.get("all_points", [])
    if not strategies:
        print("  Skipping: No strategy data found")
        return

    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Extract data points
    names = []
    centroids = []
    volumes = []
    shapes = []
    combined = []
    is_pareto = []

    for strategy in strategies:
        names.append(strategy.get('name', 'unknown'))
        centroids.append(strategy.get('centroid', 0))
        volumes.append(strategy.get('volume', 0))
        shapes.append(strategy.get('shape', 0))
        combined.append(strategy.get('combined', 0))
        is_pareto.append(strategy.get('is_pareto_optimal', False))

    # Create scatter plot
    scatter = ax.scatter(centroids, volumes, shapes,
                        c=combined, cmap='viridis_r',
                        s=200, alpha=0.8, edgecolors='black', linewidths=1)

    # Add labels for each point
    for i, name in enumerate(names):
        ax.text(centroids[i], volumes[i], shapes[i], f"  {name}",
                fontsize=8, alpha=0.8)

    # Highlight Pareto-optimal points
    for i in range(len(names)):
        if is_pareto[i]:
            ax.scatter([centroids[i]], [volumes[i]], [shapes[i]],
                      s=400, facecolors='none', edgecolors='red', linewidths=2)

    ax.set_xlabel('Centroid Loss', fontsize=12)
    ax.set_ylabel('Volume Loss', fontsize=12)
    ax.set_zlabel('Shape Loss', fontsize=12)
    ax.set_title('Phase 5.1: Pareto Frontier Analysis\n(Red circles = Pareto-optimal strategies)',
                fontsize=14)

    # Add colorbar
    cbar = fig.colorbar(scatter, ax=ax, shrink=0.6, label='Combined Loss')

    save_figure(fig, "pareto_frontier_3d")


# ============================================================================
# Visualization 2: Loss Correlation Heatmap
# ============================================================================

def plot_loss_correlation_heatmap():
    """Generate correlation heatmap for alternative loss metrics."""
    print("\n2. Loss Correlation Heatmap...")

    data = load_json("alternative_metrics.json")
    if not data:
        print("  Skipping: alternative_metrics.json not found")
        return

    # Data structure: per_family dict with metrics for each family
    per_family = data.get("per_family", {})
    if not per_family:
        print("  Skipping: No per-family data found")
        return

    # Build correlation matrix from per-family data
    metrics = ['hausdorff', 'chamfer', 'emd', 'spectral', 'iou']
    available_metrics = []

    # Check which metrics are available
    first_family = next(iter(per_family.values()), {})
    for m in metrics:
        if m in first_family:
            available_metrics.append(m)

    if len(available_metrics) < 2:
        print("  Skipping: Not enough metrics for correlation")
        return

    # Build data arrays
    metric_data = {m: [] for m in available_metrics}
    for family, values in per_family.items():
        for m in available_metrics:
            metric_data[m].append(values.get(m, 0))

    # Compute correlation matrix
    n_metrics = len(available_metrics)
    corr_array = np.zeros((n_metrics, n_metrics))
    for i, m1 in enumerate(available_metrics):
        for j, m2 in enumerate(available_metrics):
            corr_array[i, j] = np.corrcoef(metric_data[m1], metric_data[m2])[0, 1]

    fig, ax = plt.subplots(figsize=(10, 8))

    # Create heatmap
    mask = np.triu(np.ones_like(corr_array, dtype=bool), k=1)
    heatmap = sns.heatmap(corr_array,
                          mask=mask,
                          annot=True,
                          fmt='.2f',
                          cmap='RdBu_r',
                          vmin=-1, vmax=1,
                          center=0,
                          xticklabels=available_metrics,
                          yticklabels=available_metrics,
                          square=True,
                          linewidths=0.5,
                          ax=ax)

    ax.set_title('Phase 5.1: Alternative Loss Metrics Correlation\n(Hausdorff-Chamfer r=0.99)',
                fontsize=14)

    plt.tight_layout()
    save_figure(fig, "loss_correlation_heatmap")


# ============================================================================
# Visualization 3: Aggregation Method Comparison
# ============================================================================

def plot_aggregation_comparison():
    """Generate aggregation method comparison charts."""
    print("\n3. Aggregation Method Comparison...")

    data = load_json("aggregation_comparison.json")
    if not data:
        print("  Skipping: aggregation_comparison.json not found")
        return

    # Data structure: results list with method dicts
    results = data.get("results", [])
    if not results:
        print("  Skipping: No results data found")
        return

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Prepare data
    method_names = []
    mean_losses = []
    worst_losses = []
    worst_families = []

    for result in results:
        method = result.get('method', 'unknown')
        # Calculate mean from per_family_losses
        per_family = result.get('per_family_losses', {})
        if per_family:
            mean_loss = np.mean(list(per_family.values()))
        else:
            mean_loss = result.get('combined_loss', 0)

        method_names.append(method)
        mean_losses.append(mean_loss)
        worst_losses.append(result.get('worst_loss', 0))
        worst_families.append(result.get('worst_family', 'N/A'))

    if not method_names:
        print("  Skipping: Could not extract method statistics")
        return

    # Sort by mean loss
    indices = np.argsort(mean_losses)
    method_names = [method_names[i] for i in indices]
    mean_losses = [mean_losses[i] for i in indices]
    worst_losses = [worst_losses[i] for i in indices]
    worst_families = [worst_families[i] for i in indices]

    # Colors - highlight problematic methods
    colors = ['#ff6b6b' if wl > 1.0 else '#4ecdc4' for wl in worst_losses]

    # Plot 1: Mean loss
    ax1 = axes[0]
    bars1 = ax1.barh(method_names, mean_losses, color=colors, edgecolor='black')
    ax1.set_xlabel('Mean Combined Loss', fontsize=12)
    ax1.set_title('Mean Loss by Aggregation Method', fontsize=12)
    ax1.axvline(x=np.mean(mean_losses), color='gray', linestyle='--', label='Average')
    ax1.legend(loc='lower right')

    # Plot 2: Worst case loss
    ax2 = axes[1]
    bars2 = ax2.barh(method_names, worst_losses, color=colors, edgecolor='black')
    ax2.set_xlabel('Worst-Case Loss', fontsize=12)
    ax2.set_title('Worst Family Loss by Aggregation Method', fontsize=12)

    # Add family annotations
    for i, (bar, fam) in enumerate(zip(bars2, worst_families)):
        ax2.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2,
                f'{fam}', va='center', fontsize=9, alpha=0.8)

    plt.suptitle('Phase 5.1: Aggregation Method Comparison\n(Red = Unstable, worst loss > 1.0)',
                fontsize=14, y=1.02)

    plt.tight_layout()
    save_figure(fig, "aggregation_comparison")


# ============================================================================
# Visualization 4: Per-Family Loss Distribution
# ============================================================================

def plot_family_loss_distributions():
    """Generate per-family loss distribution visualization."""
    print("\n4. Per-Family Loss Distributions...")

    # Try loading from aggregation comparison (has per-family data)
    data = load_json("aggregation_comparison.json")
    if not data:
        print("  Skipping: aggregation_comparison.json not found")
        return

    # Extract per-family data from first result (mean method)
    results = data.get("results", [])
    if not results:
        print("  Skipping: No results data found")
        return

    # Find the "mean" method result
    per_family = None
    for result in results:
        if result.get('method') == 'mean':
            per_family = result.get('per_family_losses', {})
            break

    if not per_family:
        # Fall back to first result
        per_family = results[0].get('per_family_losses', {})

    if not per_family:
        print("  Skipping: No per-family data found")
        return

    families = list(per_family.keys())
    losses = list(per_family.values())

    # Sort by loss
    sorted_indices = np.argsort(losses)
    families = [families[i] for i in sorted_indices]
    losses = [losses[i] for i in sorted_indices]

    fig, ax = plt.subplots(figsize=(14, 8))

    # Color by loss magnitude
    colors = plt.cm.RdYlGn_r(np.array(losses) / max(losses))

    bars = ax.barh(families, losses, color=colors, edgecolor='black', linewidth=0.5)

    # Add mean line
    mean_loss = np.mean(losses)
    ax.axvline(x=mean_loss, color='blue', linestyle='--', linewidth=2,
               label=f'Mean: {mean_loss:.3f}')

    # Highlight problematic families
    problem_families = ['peach', 'lime', 'coral', 'gray']
    for i, fam in enumerate(families):
        if fam.lower() in problem_families:
            ax.text(losses[i] + 0.01, i, '*', fontsize=14, color='red', va='center')

    ax.set_xlabel('Combined Loss', fontsize=12)
    ax.set_ylabel('Color Family', fontsize=12)
    ax.set_title('Phase 5.1: Per-Family Loss Distribution\n(* = identified problem families)',
                fontsize=14)
    ax.legend(loc='lower right')

    plt.tight_layout()
    save_figure(fig, "per_family_loss_distribution")


# ============================================================================
# Visualization 5: Jacobian Spatial Distribution
# ============================================================================

def plot_jacobian_distribution():
    """Generate Jacobian distribution visualization from Phase 5.2."""
    print("\n5. Jacobian Spatial Distribution...")

    # jacobian_map.json is a list of point dicts, not a dict with "points" key
    data = load_json("jacobian_map.json")
    stats = load_json("jacobian_analysis.json")

    if data is None or stats is None:
        print("  Skipping: Jacobian analysis data not found")
        return

    # Data structure: list of {"rgb": [...], "munsell": [x, y, z], "jacobian_det": ...}
    # munsell is Cartesian coordinates [x, y, z] where z is Value
    points = data if isinstance(data, list) else data.get("points", [])
    if not points:
        print("  Skipping: No Jacobian points found")
        return

    # Extract data
    det_j_values = []
    munsell_values = []  # z coordinate is Value
    munsell_chromas = []  # sqrt(x^2 + y^2) is Chroma

    for pt in points:
        det_j = pt.get("jacobian_det")
        munsell = pt.get("munsell", [])

        if det_j is not None and isinstance(munsell, list) and len(munsell) >= 3:
            det_j_values.append(det_j)
            # Munsell Cartesian: [x, y, z] where z = Value, sqrt(x^2+y^2) = Chroma
            x, y, z = munsell[0], munsell[1], munsell[2]
            munsell_values.append(z)  # Value
            munsell_chromas.append(np.sqrt(x*x + y*y))  # Chroma

    if not det_j_values:
        print("  Skipping: Could not extract Jacobian values")
        return

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # Plot 1: Histogram of det(J)
    ax1 = axes[0]
    ax1.hist(det_j_values, bins=50, color='steelblue', edgecolor='black', alpha=0.7)
    ax1.axvline(x=np.mean(det_j_values), color='red', linestyle='--',
                label=f'Mean: {np.mean(det_j_values):.1f}')
    ax1.set_xlabel('|det(J)|', fontsize=12)
    ax1.set_ylabel('Count', fontsize=12)
    ax1.set_title('Jacobian Determinant Distribution', fontsize=12)
    ax1.legend()

    # Plot 2: Jacobian vs Munsell Value
    ax2 = axes[1]
    ax2.scatter(munsell_values, det_j_values, alpha=0.5, s=10, c='steelblue')
    ax2.set_xlabel('Munsell Value', fontsize=12)
    ax2.set_ylabel('|det(J)|', fontsize=12)
    ax2.set_title('Jacobian vs Value (Luminance)', fontsize=12)

    # Plot 3: Jacobian vs Munsell Chroma
    ax3 = axes[2]
    ax3.scatter(munsell_chromas, det_j_values, alpha=0.5, s=10, c='steelblue')
    ax3.set_xlabel('Munsell Chroma', fontsize=12)
    ax3.set_ylabel('|det(J)|', fontsize=12)
    ax3.set_title('Jacobian vs Chroma (Saturation)', fontsize=12)

    # Get stats from nested structure
    statistics = stats.get("statistics", {})
    jacobian_stats = statistics.get("jacobian_det_abs", {})
    volume_scaling = statistics.get("volume_scaling", {})

    mean_j = jacobian_stats.get("mean", np.mean(det_j_values))
    cv = volume_scaling.get("coefficient_of_variation", np.std(det_j_values) / np.mean(det_j_values))

    plt.suptitle(f'Phase 5.2: Jacobian Analysis (Mean={mean_j:.1f}, CV={cv:.4f})',
                fontsize=14, y=1.02)

    plt.tight_layout()
    save_figure(fig, "jacobian_distribution")


# ============================================================================
# Visualization 6: Volume Stability Convergence
# ============================================================================

def plot_volume_stability():
    """Generate volume stability analysis from bootstrap data."""
    print("\n6. Volume Stability Convergence...")

    data = load_json("sample_size_analysis.json")
    if not data:
        print("  Skipping: sample_size_analysis.json not found")
        return

    families = data.get("families", {})
    if not families:
        print("  Skipping: No family data found")
        return

    # Prepare convergence curves
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Plot 1: CV vs Sample Size (selected families)
    ax1 = axes[0]

    # Select representative families (largest, smallest, median)
    family_sizes = [(name, fam.get("n_points", 0)) for name, fam in families.items()]
    family_sizes.sort(key=lambda x: x[1])

    # Pick 5 representative families
    n_fam = len(family_sizes)
    if n_fam >= 5:
        selected_indices = [0, n_fam//4, n_fam//2, 3*n_fam//4, n_fam-1]
        selected = [family_sizes[i][0] for i in selected_indices]
    else:
        selected = [f[0] for f in family_sizes]

    colors = plt.cm.tab10(np.linspace(0, 1, len(selected)))

    for i, family_name in enumerate(selected):
        fam_data = families.get(family_name, {})
        bootstrap = fam_data.get("bootstrap_results", {})

        sample_sizes = []
        cvs = []

        for n_str, stats in sorted(bootstrap.items(), key=lambda x: int(x[0])):
            if isinstance(stats, dict) and "cv" in stats:
                sample_sizes.append(int(n_str))
                cvs.append(stats["cv"])

        if sample_sizes and cvs:
            ax1.plot(sample_sizes, cvs, marker='o', label=family_name, color=colors[i])

    ax1.axhline(y=0.05, color='red', linestyle='--', label='Stability threshold (CV=0.05)')
    ax1.set_xlabel('Sample Size (N)', fontsize=12)
    ax1.set_ylabel('Coefficient of Variation (CV)', fontsize=12)
    ax1.set_title('Volume Stability vs Sample Size', fontsize=12)
    ax1.legend(loc='upper right', fontsize=9)
    ax1.set_xscale('log')

    # Plot 2: Stability status summary
    ax2 = axes[1]

    stable_count = sum(1 for f in families.values() if f.get("status") == "stable")
    unstable_count = sum(1 for f in families.values() if f.get("status") in ["unstable", "insufficient"])

    bars = ax2.bar(['Stable', 'Unstable'], [stable_count, unstable_count],
                   color=['#4ecdc4', '#ff6b6b'], edgecolor='black')

    ax2.set_ylabel('Number of Families', fontsize=12)
    ax2.set_title(f'Volume Stability Summary\n({stable_count}/{stable_count + unstable_count} families stable)',
                  fontsize=12)

    # Add count labels
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontsize=14, fontweight='bold')

    plt.suptitle('Phase 5.2: Bootstrap Sample Size Analysis', fontsize=14, y=1.02)

    plt.tight_layout()
    save_figure(fig, "volume_stability")


# ============================================================================
# Summary Dashboard
# ============================================================================

def plot_summary_dashboard():
    """Generate summary dashboard combining key findings."""
    print("\n7. Summary Dashboard...")

    fig = plt.figure(figsize=(16, 12))

    # Create grid layout
    gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)

    # Load all data
    pareto = load_json("pareto_analysis.json")
    metrics = load_json("alternative_metrics.json")
    jacobian = load_json("jacobian_analysis.json")
    sample = load_json("sample_size_analysis.json")

    # Panel 1: Key findings text
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.axis('off')

    # Extract Jacobian CV from nested structure
    jacobian_cv = 'N/A'
    if jacobian:
        statistics = jacobian.get("statistics", {})
        volume_scaling = statistics.get("volume_scaling", {})
        jacobian_cv = volume_scaling.get("coefficient_of_variation", 'N/A')
        if isinstance(jacobian_cv, float):
            jacobian_cv = f"{jacobian_cv:.4f}"

    findings = [
        "PHASE 5 KEY FINDINGS",
        "",
        "Phase 5.1: Loss Function Analysis",
        "  - Volume-only: 0.054 combined loss (best)",
        "  - Shape varies only 5% across strategies",
        "  - Hausdorff-Chamfer r=0.99 (interchangeable)",
        "",
        "Phase 5.2: Volume Stability",
        f"  - Jacobian CV: {jacobian_cv}",
        f"  - Stable families: {sample['summary']['stable_families'] if sample else 'N/A'}/35",
        "  - No per-family corrections needed",
    ]

    ax1.text(0.05, 0.95, '\n'.join(findings), transform=ax1.transAxes,
             fontsize=11, verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    # Panel 2: Pareto strategies (simplified)
    ax2 = fig.add_subplot(gs[0, 1])
    if pareto:
        strategies = pareto.get("all_points", [])
        if strategies:
            names = [s.get('name', 'unknown') for s in strategies[:6]]
            combined = [s.get('combined', 0) for s in strategies[:6]]

            colors = ['#4ecdc4' if c < 0.1 else '#ffd93d' if c < 0.2 else '#ff6b6b' for c in combined]
            ax2.barh(names, combined, color=colors, edgecolor='black')
            ax2.set_xlabel('Combined Loss')
            ax2.set_title('Loss by Strategy')
        else:
            ax2.text(0.5, 0.5, 'No strategy data', ha='center', va='center')
            ax2.axis('off')
    else:
        ax2.text(0.5, 0.5, 'No Pareto data', ha='center', va='center')
        ax2.axis('off')

    # Panel 3: Metrics correlation (simplified)
    ax3 = fig.add_subplot(gs[0, 2])
    if metrics:
        per_family = metrics.get("per_family", {})
        if per_family:
            # Build correlation from per_family data
            metric_names = ['hausdorff', 'chamfer', 'emd', 'spectral']
            metric_data = {m: [] for m in metric_names}
            for fam, values in per_family.items():
                for m in metric_names:
                    if m in values:
                        metric_data[m].append(values[m])

            # Check we have data
            if all(len(metric_data[m]) > 0 for m in metric_names):
                n = len(metric_names)
                corr_array = np.zeros((n, n))
                for i, m1 in enumerate(metric_names):
                    for j, m2 in enumerate(metric_names):
                        corr_array[i, j] = np.corrcoef(metric_data[m1], metric_data[m2])[0, 1]

                sns.heatmap(corr_array, annot=True, fmt='.2f', cmap='RdBu_r',
                           xticklabels=metric_names, yticklabels=metric_names,
                           ax=ax3, cbar=False, vmin=-1, vmax=1)
                ax3.set_title('Metric Correlations')
            else:
                ax3.text(0.5, 0.5, 'Insufficient metric data', ha='center', va='center')
                ax3.axis('off')
        else:
            ax3.text(0.5, 0.5, 'No correlation data', ha='center', va='center')
            ax3.axis('off')
    else:
        ax3.text(0.5, 0.5, 'No metrics data', ha='center', va='center')
        ax3.axis('off')

    # Panel 4: Jacobian distribution
    ax4 = fig.add_subplot(gs[1, 0])
    if jacobian:
        statistics = jacobian.get("statistics", {})
        jacobian_stats = statistics.get("jacobian_det_abs", {})
        volume_scaling = statistics.get("volume_scaling", {})

        mean_j = jacobian_stats.get("mean", 0)
        std_j = jacobian_stats.get("std", 0)
        cv = volume_scaling.get("coefficient_of_variation", 0)

        # Simple bar showing mean with error bar
        ax4.bar(['|det(J)|'], [mean_j], yerr=[std_j], color='steelblue',
                edgecolor='black', capsize=10)
        ax4.set_ylabel('Jacobian Determinant')
        ax4.set_title(f'Volume Scaling\n(CV={cv:.4f})')
    else:
        ax4.text(0.5, 0.5, 'No Jacobian data', ha='center', va='center')
        ax4.axis('off')

    # Panel 5: Per-family stability
    ax5 = fig.add_subplot(gs[1, 1:])
    if sample:
        summary = sample.get("summary", {})
        families_data = sample.get("families", {})

        # Extract min_stable_n for stable families
        stable_ns = []
        for fam, data in families_data.items():
            if data.get("status") == "stable" and data.get("min_stable_n"):
                stable_ns.append(data["min_stable_n"])

        if stable_ns:
            ax5.hist(stable_ns, bins=20, color='steelblue', edgecolor='black', alpha=0.7)
            ax5.axvline(x=np.median(stable_ns), color='red', linestyle='--',
                       label=f'Median: {np.median(stable_ns):.0f}')
            ax5.set_xlabel('Minimum Stable Sample Size (N)')
            ax5.set_ylabel('Number of Families')
            ax5.set_title('Sample Size Required for Volume Stability')
            ax5.legend()
        else:
            ax5.text(0.5, 0.5, 'No stable family data', ha='center', va='center')
            ax5.axis('off')
    else:
        ax5.text(0.5, 0.5, 'No sample size data', ha='center', va='center')
        ax5.axis('off')

    plt.suptitle('Phase 5 Transformation Research: Summary Dashboard',
                fontsize=16, fontweight='bold', y=0.98)

    save_figure(fig, "phase5_summary_dashboard")


# ============================================================================
# Main
# ============================================================================

def main():
    print("=" * 70)
    print("Phase 5 Transformation Research Visualizations (Task 114)")
    print("=" * 70)

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    setup_style()

    print(f"\nOutput directory: {FIGURES_DIR}")

    # Generate all visualizations
    plot_pareto_frontier_3d()
    plot_loss_correlation_heatmap()
    plot_aggregation_comparison()
    plot_family_loss_distributions()
    plot_jacobian_distribution()
    plot_volume_stability()
    plot_summary_dashboard()

    print(f"\n{'=' * 70}")
    print("VISUALIZATION GENERATION COMPLETE")
    print(f"{'=' * 70}")

    # List generated files
    if FIGURES_DIR.exists():
        files = list(FIGURES_DIR.glob("*.png"))
        print(f"\nGenerated {len(files)} figures:")
        for f in sorted(files):
            print(f"  - {f.name}")


if __name__ == "__main__":
    main()
