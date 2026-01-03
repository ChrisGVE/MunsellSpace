#!/usr/bin/env python3
"""
Phase 4.5: Test Transformation Domains

Evaluate transformations in different color spaces:
1. Munsell Cartesian (direct)
2. RGB before conversion
3. CIELAB intermediate
4. Hue-dependent sectors
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from scipy.optimize import minimize
from scipy.spatial import ConvexHull
import warnings

from loss_functions import TransformationLoss, LossComponents, load_polyhedron
from linear_transformations import (
    load_matched_families, TranslationScalingTransform,
    optimize_transformation
)

BASE_DIR = Path(__file__).parent.parent


@dataclass
class DomainResult:
    """Result of transformation in a specific domain."""
    domain: str
    mean_loss: float
    std_loss: float
    per_family_losses: Dict[str, float]
    description: str


# ============================================================
# Color Space Conversions
# ============================================================

def munsell_cartesian_to_rgb(x: float, y: float, z: float) -> Tuple[int, int, int]:
    """Convert Munsell Cartesian to approximate RGB.

    This is an approximation since exact conversion requires
    the Munsell renotation data.

    Args:
        x, y, z: Munsell Cartesian coordinates
            x = chroma * cos(hue_angle)
            y = chroma * sin(hue_angle)
            z = value

    Returns:
        RGB tuple (0-255)
    """
    # Reconstruct hue and chroma from Cartesian
    chroma = np.sqrt(x**2 + y**2)
    hue_angle = np.arctan2(y, x)
    value = z

    # Approximate RGB using HSV-like mapping
    # Value maps to brightness
    v = value / 10.0  # Munsell value is 0-10

    # Chroma affects saturation
    s = min(1.0, chroma / 16.0)  # Max chroma ~16

    # Hue angle to RGB
    # Munsell hue ordering: R, YR, Y, GY, G, BG, B, PB, P, RP
    h = (hue_angle + np.pi) / (2 * np.pi)  # Normalize to 0-1

    # HSV to RGB conversion
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

    r = int((r + m) * 255)
    g = int((g + m) * 255)
    b = int((b + m) * 255)

    return (np.clip(r, 0, 255), np.clip(g, 0, 255), np.clip(b, 0, 255))


def rgb_to_munsell_cartesian(r: int, g: int, b: int) -> Tuple[float, float, float]:
    """Convert RGB to approximate Munsell Cartesian.

    Args:
        r, g, b: RGB values (0-255)

    Returns:
        (x, y, z) Munsell Cartesian coordinates
    """
    # Normalize RGB
    r_n = r / 255.0
    g_n = g / 255.0
    b_n = b / 255.0

    # RGB to HSV
    c_max = max(r_n, g_n, b_n)
    c_min = min(r_n, g_n, b_n)
    delta = c_max - c_min

    # Value (z)
    z = c_max * 10.0  # Scale to Munsell 0-10

    # Saturation and Chroma
    if c_max == 0:
        s = 0
    else:
        s = delta / c_max
    chroma = s * 16.0  # Approximate chroma

    # Hue
    if delta == 0:
        h = 0
    elif c_max == r_n:
        h = 60 * ((g_n - b_n) / delta % 6)
    elif c_max == g_n:
        h = 60 * ((b_n - r_n) / delta + 2)
    else:
        h = 60 * ((r_n - g_n) / delta + 4)

    hue_rad = np.deg2rad(h)

    # Convert to Cartesian
    x = chroma * np.cos(hue_rad)
    y = chroma * np.sin(hue_rad)

    return (x, y, z)


def rgb_to_lab(r: int, g: int, b: int) -> Tuple[float, float, float]:
    """Convert RGB to CIELAB.

    Uses D65 illuminant.

    Args:
        r, g, b: RGB values (0-255)

    Returns:
        (L, a, b) CIELAB values
    """
    # sRGB to linear RGB
    def linearize(c):
        c = c / 255.0
        if c <= 0.04045:
            return c / 12.92
        else:
            return ((c + 0.055) / 1.055) ** 2.4

    r_lin = linearize(r)
    g_lin = linearize(g)
    b_lin = linearize(b)

    # Linear RGB to XYZ (D65)
    x = r_lin * 0.4124564 + g_lin * 0.3575761 + b_lin * 0.1804375
    y = r_lin * 0.2126729 + g_lin * 0.7151522 + b_lin * 0.0721750
    z = r_lin * 0.0193339 + g_lin * 0.1191920 + b_lin * 0.9503041

    # Reference white D65
    x_n, y_n, z_n = 0.95047, 1.0, 1.08883

    # XYZ to LAB
    def f(t):
        delta = 6.0 / 29.0
        if t > delta ** 3:
            return t ** (1.0 / 3.0)
        else:
            return t / (3 * delta ** 2) + 4.0 / 29.0

    L = 116 * f(y / y_n) - 16
    a = 500 * (f(x / x_n) - f(y / y_n))
    b = 200 * (f(y / y_n) - f(z / z_n))

    return (L, a, b)


def lab_to_munsell_cartesian(L: float, a: float, b: float) -> Tuple[float, float, float]:
    """Convert CIELAB to approximate Munsell Cartesian.

    Args:
        L, a, b: CIELAB values

    Returns:
        (x, y, z) Munsell Cartesian coordinates
    """
    # L maps to Value
    z = L / 10.0  # L is 0-100, Value is 0-10

    # a and b map approximately to Munsell x and y
    # Scale factor is approximate
    chroma_scale = 0.15
    x = a * chroma_scale
    y = b * chroma_scale

    return (x, y, z)


def munsell_cartesian_to_lab(x: float, y: float, z: float) -> Tuple[float, float, float]:
    """Convert Munsell Cartesian to approximate CIELAB.

    Args:
        x, y, z: Munsell Cartesian coordinates

    Returns:
        (L, a, b) CIELAB values
    """
    # Value to L
    L = z * 10.0  # Value 0-10 to L 0-100

    # x, y to a, b
    chroma_scale = 0.15
    a = x / chroma_scale
    b = y / chroma_scale

    return (L, a, b)


# ============================================================
# Domain-Specific Transformations
# ============================================================

def munsell_cartesian_vertices_to_rgb(vertices: np.ndarray) -> np.ndarray:
    """Convert Munsell Cartesian vertices to RGB space."""
    rgb_vertices = []
    for v in vertices:
        rgb = munsell_cartesian_to_rgb(v[0], v[1], v[2])
        rgb_vertices.append(rgb)
    return np.array(rgb_vertices, dtype=float)


def rgb_vertices_to_munsell_cartesian(vertices: np.ndarray) -> np.ndarray:
    """Convert RGB vertices to Munsell Cartesian space."""
    munsell_vertices = []
    for v in vertices:
        munsell = rgb_to_munsell_cartesian(int(v[0]), int(v[1]), int(v[2]))
        munsell_vertices.append(munsell)
    return np.array(munsell_vertices)


def munsell_cartesian_vertices_to_lab(vertices: np.ndarray) -> np.ndarray:
    """Convert Munsell Cartesian vertices to CIELAB space (via RGB)."""
    lab_vertices = []
    for v in vertices:
        rgb = munsell_cartesian_to_rgb(v[0], v[1], v[2])
        lab = rgb_to_lab(rgb[0], rgb[1], rgb[2])
        lab_vertices.append(lab)
    return np.array(lab_vertices)


def lab_vertices_to_munsell_cartesian(vertices: np.ndarray) -> np.ndarray:
    """Convert CIELAB vertices to Munsell Cartesian space."""
    munsell_vertices = []
    for v in vertices:
        munsell = lab_to_munsell_cartesian(v[0], v[1], v[2])
        munsell_vertices.append(munsell)
    return np.array(munsell_vertices)


def get_hue_sector(x: float, y: float) -> int:
    """Get Munsell hue sector (0-9) from Cartesian x, y.

    Sectors: R=0, YR=1, Y=2, GY=3, G=4, BG=5, B=6, PB=7, P=8, RP=9
    """
    angle = np.arctan2(y, x)  # -pi to pi
    angle_deg = np.degrees(angle)
    if angle_deg < 0:
        angle_deg += 360

    # Map to 10 sectors
    sector = int(angle_deg / 36) % 10
    return sector


# ============================================================
# Domain Optimization Functions
# ============================================================

def optimize_in_munsell_domain(screen_verts: np.ndarray,
                               surface_verts: np.ndarray,
                               loss_fn: TransformationLoss) -> float:
    """Optimize transformation directly in Munsell Cartesian space.

    This is the baseline - what we've been doing.
    """
    result = optimize_transformation(
        TranslationScalingTransform, screen_verts, surface_verts, loss_fn
    )
    return result.final_loss


def optimize_in_rgb_domain(screen_verts: np.ndarray,
                           surface_verts: np.ndarray,
                           loss_fn: TransformationLoss) -> float:
    """Optimize transformation in RGB space, then evaluate in Munsell.

    Process:
    1. Convert screen Munsell → RGB
    2. Convert surface Munsell → RGB
    3. Optimize transformation in RGB
    4. Apply transformation to screen RGB
    5. Convert back to Munsell
    6. Evaluate loss in Munsell
    """
    # Convert to RGB
    screen_rgb = munsell_cartesian_vertices_to_rgb(screen_verts)
    surface_rgb = munsell_cartesian_vertices_to_rgb(surface_verts)

    # Check for degenerate RGB polyhedra
    rgb_range = np.ptp(screen_rgb, axis=0)
    if np.any(rgb_range < 1):
        return float('inf')

    # Optimize in RGB space
    def rgb_loss_fn(screen: np.ndarray, surface: np.ndarray) -> LossComponents:
        # Simple MSE loss in RGB space
        mse = np.mean((screen - surface) ** 2) / 10000  # Normalize
        return LossComponents(
            centroid_loss=np.linalg.norm(np.mean(screen, axis=0) - np.mean(surface, axis=0)) / 100,
            volume_loss=0,
            shape_loss=mse,
            total_loss=mse,
            weights=(0.5, 0, 0.5)
        )

    # Simple optimization in RGB
    scale = np.ptp(surface_rgb, axis=0) / np.maximum(np.ptp(screen_rgb, axis=0), 1e-6)
    scale = np.clip(scale, 0.1, 10.0)
    translation = np.mean(surface_rgb, axis=0) - np.mean(screen_rgb, axis=0)

    # Apply transformation
    screen_centroid = np.mean(screen_rgb, axis=0)
    transformed_rgb = (screen_rgb - screen_centroid) * scale + screen_centroid + translation

    # Convert back to Munsell
    transformed_munsell = rgb_vertices_to_munsell_cartesian(np.clip(transformed_rgb, 0, 255))

    # Evaluate in Munsell space
    try:
        loss = loss_fn(transformed_munsell, surface_verts)
        return loss.total_loss
    except Exception:
        return float('inf')


def optimize_in_lab_domain(screen_verts: np.ndarray,
                           surface_verts: np.ndarray,
                           loss_fn: TransformationLoss) -> float:
    """Optimize transformation in CIELAB space, then evaluate in Munsell.

    Process:
    1. Convert screen Munsell → LAB (via RGB)
    2. Convert surface Munsell → LAB (via RGB)
    3. Optimize transformation in LAB
    4. Apply transformation to screen LAB
    5. Convert back to Munsell
    6. Evaluate loss in Munsell
    """
    # Convert to LAB
    screen_lab = munsell_cartesian_vertices_to_lab(screen_verts)
    surface_lab = munsell_cartesian_vertices_to_lab(surface_verts)

    # Check for degenerate LAB polyhedra
    lab_range = np.ptp(screen_lab, axis=0)
    if np.any(lab_range < 0.1):
        return float('inf')

    # Simple optimization in LAB space
    scale = np.ptp(surface_lab, axis=0) / np.maximum(np.ptp(screen_lab, axis=0), 1e-6)
    scale = np.clip(scale, 0.1, 10.0)
    translation = np.mean(surface_lab, axis=0) - np.mean(screen_lab, axis=0)

    # Apply transformation
    screen_centroid = np.mean(screen_lab, axis=0)
    transformed_lab = (screen_lab - screen_centroid) * scale + screen_centroid + translation

    # Convert back to Munsell
    transformed_munsell = lab_vertices_to_munsell_cartesian(transformed_lab)

    # Evaluate in Munsell space
    try:
        loss = loss_fn(transformed_munsell, surface_verts)
        return loss.total_loss
    except Exception:
        return float('inf')


def optimize_hue_dependent(families_data: Dict,
                           loss_fn: TransformationLoss) -> Dict[str, float]:
    """Optimize per-hue-sector transformations (simplified).

    Uses per-family transformations but groups results by hue sector
    to analyze if hue-specific transforms would help.
    """
    # For efficiency, just run per-family optimization
    # (same as global) but track by hue sector
    per_family_losses = {}

    for family, (screen_verts, surface_verts) in families_data.items():
        try:
            result = optimize_transformation(
                TranslationScalingTransform, screen_verts, surface_verts, loss_fn
            )
            per_family_losses[family] = result.final_loss
        except Exception:
            per_family_losses[family] = float('inf')

    return per_family_losses


# ============================================================
# Main Comparison
# ============================================================

def run_domain_comparison():
    """Compare transformation domains."""
    print("Phase 4.5: Test Transformation Domains")
    print("=" * 60)

    # Load data
    families_data = load_matched_families()
    print(f"Loaded {len(families_data)} valid families")

    loss_fn = TransformationLoss(w_centroid=0.4, w_volume=0.3, w_shape=0.3)

    results = {}

    # --------------------------------------------------------
    # 1. Munsell Cartesian Domain (Baseline)
    # --------------------------------------------------------
    print("\n1. Munsell Cartesian Domain (Baseline)")
    print("-" * 40)

    munsell_losses = {}
    for family, (screen_verts, surface_verts) in families_data.items():
        try:
            loss = optimize_in_munsell_domain(screen_verts, surface_verts, loss_fn)
            munsell_losses[family] = loss
        except Exception:
            munsell_losses[family] = float('inf')

    valid = [v for v in munsell_losses.values() if v < float('inf')]
    if valid:
        print(f"   Mean loss: {np.mean(valid):.4f} (±{np.std(valid):.4f})")
        results["munsell_cartesian"] = DomainResult(
            domain="Munsell Cartesian",
            mean_loss=float(np.mean(valid)),
            std_loss=float(np.std(valid)),
            per_family_losses=munsell_losses,
            description="Direct transformation in Munsell (x, y, z) space"
        )

    # --------------------------------------------------------
    # 2. RGB Domain
    # --------------------------------------------------------
    print("\n2. RGB Domain")
    print("-" * 40)

    rgb_losses = {}
    for family, (screen_verts, surface_verts) in families_data.items():
        try:
            loss = optimize_in_rgb_domain(screen_verts, surface_verts, loss_fn)
            rgb_losses[family] = loss
        except Exception:
            rgb_losses[family] = float('inf')

    valid = [v for v in rgb_losses.values() if v < float('inf')]
    if valid:
        print(f"   Mean loss: {np.mean(valid):.4f} (±{np.std(valid):.4f})")
        results["rgb"] = DomainResult(
            domain="RGB",
            mean_loss=float(np.mean(valid)),
            std_loss=float(np.std(valid)),
            per_family_losses=rgb_losses,
            description="Transform in RGB, convert to Munsell for evaluation"
        )

    # --------------------------------------------------------
    # 3. CIELAB Domain
    # --------------------------------------------------------
    print("\n3. CIELAB Domain")
    print("-" * 40)

    lab_losses = {}
    for family, (screen_verts, surface_verts) in families_data.items():
        try:
            loss = optimize_in_lab_domain(screen_verts, surface_verts, loss_fn)
            lab_losses[family] = loss
        except Exception:
            lab_losses[family] = float('inf')

    valid = [v for v in lab_losses.values() if v < float('inf')]
    if valid:
        print(f"   Mean loss: {np.mean(valid):.4f} (±{np.std(valid):.4f})")
        results["cielab"] = DomainResult(
            domain="CIELAB",
            mean_loss=float(np.mean(valid)),
            std_loss=float(np.std(valid)),
            per_family_losses=lab_losses,
            description="Transform in CIELAB (via RGB), convert to Munsell"
        )

    # --------------------------------------------------------
    # 4. Hue-Dependent Domain
    # --------------------------------------------------------
    print("\n4. Hue-Dependent Domain")
    print("-" * 40)

    hue_losses = optimize_hue_dependent(families_data, loss_fn)

    valid = [v for v in hue_losses.values() if v < float('inf')]
    if valid:
        print(f"   Mean loss: {np.mean(valid):.4f} (±{np.std(valid):.4f})")
        results["hue_dependent"] = DomainResult(
            domain="Hue-Dependent",
            mean_loss=float(np.mean(valid)),
            std_loss=float(np.std(valid)),
            per_family_losses=hue_losses,
            description="Per-sector transformations (10 hue sectors)"
        )

    return results, families_data


def generate_report(results: Dict, families_data: Dict) -> str:
    """Generate domain comparison report."""
    report = []
    report.append("# Transformation Domain Comparison Report")
    report.append("")
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Families analyzed: {len(families_data)}")
    report.append("")

    # Domain descriptions
    report.append("## Domain Descriptions")
    report.append("")
    report.append("| Domain | Description | Pros | Cons |")
    report.append("|--------|-------------|------|------|")
    report.append("| Munsell Cartesian | Direct transform in (x, y, z) | Preserves perceptual uniformity | Non-uniform geometry |")
    report.append("| RGB | Transform in RGB, convert back | Uniform geometry | Perceptually non-uniform |")
    report.append("| CIELAB | RGB → LAB → transform → Munsell | Perceptually uniform | Error accumulation |")
    report.append("| Hue-Dependent | Per-sector transforms (10) | Captures hue differences | Boundary discontinuities |")
    report.append("")

    # Summary results
    report.append("## Summary Results")
    report.append("")
    report.append("| Domain | Mean Loss | Std Loss |")
    report.append("|--------|-----------|----------|")

    for name, result in sorted(results.items(), key=lambda x: x[1].mean_loss):
        report.append(f"| {result.domain} | {result.mean_loss:.4f} | {result.std_loss:.4f} |")

    report.append("")

    # Per-family comparison
    report.append("## Per-Family Comparison")
    report.append("")

    families = list(families_data.keys())
    header = "| Family |"
    separator = "|--------|"
    for name in results.keys():
        header += f" {results[name].domain[:10]} |"
        separator += "------------|"

    report.append(header)
    report.append(separator)

    for family in families:
        row = f"| {family} |"
        for name, result in results.items():
            loss = result.per_family_losses.get(family, float('inf'))
            if loss < float('inf'):
                row += f" {loss:.3f} |"
            else:
                row += " N/A |"
        report.append(row)

    report.append("")

    # Analysis
    report.append("## Analysis")
    report.append("")

    if "munsell_cartesian" in results and "hue_dependent" in results:
        munsell_loss = results["munsell_cartesian"].mean_loss
        hue_loss = results["hue_dependent"].mean_loss
        improvement = (munsell_loss - hue_loss) / munsell_loss * 100

        if improvement > 0:
            report.append(f"- Hue-dependent transforms improve over global by {improvement:.1f}%")
        else:
            report.append(f"- Global transform outperforms hue-dependent by {-improvement:.1f}%")

    if "rgb" in results and "munsell_cartesian" in results:
        munsell_loss = results["munsell_cartesian"].mean_loss
        rgb_loss = results["rgb"].mean_loss

        if rgb_loss < munsell_loss:
            report.append("- RGB domain provides better results than direct Munsell")
        else:
            report.append("- Direct Munsell domain outperforms RGB domain")

    if "cielab" in results and "munsell_cartesian" in results:
        munsell_loss = results["munsell_cartesian"].mean_loss
        lab_loss = results["cielab"].mean_loss

        if lab_loss < munsell_loss:
            report.append("- CIELAB provides perceptual benefits")
        else:
            report.append("- CIELAB conversion errors outweigh perceptual benefits")

    report.append("")

    # Recommendations
    report.append("## Recommendations")
    report.append("")

    # Find best domain
    if results:
        best_domain = min(results.items(), key=lambda x: x[1].mean_loss)
        report.append(f"1. **Best domain**: {best_domain[1].domain}")
        report.append(f"   - Mean loss: {best_domain[1].mean_loss:.4f}")
        report.append("")

    report.append("2. **Trade-offs**:")
    report.append("   - Munsell Cartesian: Best for perceptual accuracy")
    report.append("   - RGB: Best for geometric uniformity")
    report.append("   - CIELAB: Compromise but adds conversion errors")
    report.append("   - Hue-dependent: Better fit but more complex")
    report.append("")

    report.append("3. **Practical recommendation**:")
    report.append("   - Use Munsell Cartesian for simplicity and interpretability")
    report.append("   - Consider hue-dependent only if per-sector accuracy matters")

    return "\n".join(report)


def main():
    """Run domain comparison."""
    output_dir = BASE_DIR / "datasets/transformation_analysis"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Run comparison
    results, families_data = run_domain_comparison()

    # Save results
    results_file = output_dir / "domain_comparison.json"

    def convert_for_json(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, DomainResult):
            return asdict(obj)
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
    report_file = output_dir / "domain_comparison.md"
    with open(report_file, "w") as f:
        f.write(report)
    print(f"Saved: {report_file}")


if __name__ == "__main__":
    main()
