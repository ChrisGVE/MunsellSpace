#!/usr/bin/env python3
"""
Task 117: Gamut Comparison Visualization for Academic Paper

Generates a multi-panel publication-quality figure showing:
1. Panel A: CIE xy chromaticity diagram with spectrum locus, sRGB/P3 triangles
2. Panel B: Munsell value slices showing gamut boundaries at V=3, 5, 7
3. Panel C: Screen-surface calibration visualization (hue rotation, V/C bias)

Output: writeups/figures/gamut_comparison.{png,svg,pdf}
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Polygon, FancyArrowPatch
from matplotlib.colors import hsv_to_rgb
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Configure matplotlib for publication quality
plt.rcParams.update({
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'DejaVu Sans', 'Helvetica'],
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.titlesize': 14,
    'mathtext.fontset': 'dejavusans',
})

BASE_DIR = Path(__file__).parent.parent
FIGURES_DIR = BASE_DIR / "writeups" / "figures"
DATA_DIR = BASE_DIR / "writeups" / "results" / "data"

# =============================================================================
# Color Space Data
# =============================================================================

# CIE 1931 2° Standard Observer Spectrum Locus (380-700nm at 5nm intervals)
# Source: CIE 15:2004
SPECTRUM_LOCUS_XY = np.array([
    [0.1741, 0.0050],  # 380nm
    [0.1740, 0.0050],  # 385nm
    [0.1738, 0.0049],  # 390nm
    [0.1736, 0.0049],  # 395nm
    [0.1733, 0.0048],  # 400nm
    [0.1730, 0.0048],  # 405nm
    [0.1726, 0.0048],  # 410nm
    [0.1721, 0.0048],  # 415nm
    [0.1714, 0.0051],  # 420nm
    [0.1703, 0.0058],  # 425nm
    [0.1689, 0.0069],  # 430nm
    [0.1669, 0.0086],  # 435nm
    [0.1644, 0.0109],  # 440nm
    [0.1611, 0.0138],  # 445nm
    [0.1566, 0.0177],  # 450nm
    [0.1510, 0.0227],  # 455nm
    [0.1440, 0.0297],  # 460nm
    [0.1355, 0.0399],  # 465nm
    [0.1241, 0.0578],  # 470nm
    [0.1096, 0.0868],  # 475nm
    [0.0913, 0.1327],  # 480nm
    [0.0687, 0.2007],  # 485nm
    [0.0454, 0.2950],  # 490nm
    [0.0235, 0.4127],  # 495nm
    [0.0082, 0.5384],  # 500nm
    [0.0039, 0.6548],  # 505nm
    [0.0139, 0.7502],  # 510nm
    [0.0389, 0.8120],  # 515nm
    [0.0743, 0.8338],  # 520nm
    [0.1142, 0.8262],  # 525nm
    [0.1547, 0.8059],  # 530nm
    [0.1929, 0.7816],  # 535nm
    [0.2296, 0.7543],  # 540nm
    [0.2658, 0.7243],  # 545nm
    [0.3016, 0.6923],  # 550nm
    [0.3373, 0.6589],  # 555nm
    [0.3731, 0.6245],  # 560nm
    [0.4087, 0.5896],  # 565nm
    [0.4441, 0.5547],  # 570nm
    [0.4788, 0.5202],  # 575nm
    [0.5125, 0.4866],  # 580nm
    [0.5448, 0.4544],  # 585nm
    [0.5752, 0.4242],  # 590nm
    [0.6029, 0.3965],  # 595nm
    [0.6270, 0.3725],  # 600nm
    [0.6482, 0.3514],  # 605nm
    [0.6658, 0.3340],  # 610nm
    [0.6801, 0.3197],  # 615nm
    [0.6915, 0.3083],  # 620nm
    [0.7006, 0.2993],  # 625nm
    [0.7079, 0.2920],  # 630nm
    [0.7140, 0.2859],  # 635nm
    [0.7190, 0.2809],  # 640nm
    [0.7230, 0.2770],  # 645nm
    [0.7260, 0.2740],  # 650nm
    [0.7283, 0.2717],  # 655nm
    [0.7300, 0.2700],  # 660nm
    [0.7311, 0.2689],  # 665nm
    [0.7320, 0.2680],  # 670nm
    [0.7327, 0.2673],  # 675nm
    [0.7334, 0.2666],  # 680nm
    [0.7340, 0.2660],  # 685nm
    [0.7344, 0.2656],  # 690nm
    [0.7346, 0.2654],  # 695nm
    [0.7347, 0.2653],  # 700nm
])

# RGB Color Space Primary Chromaticities
SRGB_PRIMARIES = np.array([
    [0.6400, 0.3300],  # Red
    [0.3000, 0.6000],  # Green
    [0.1500, 0.0600],  # Blue
])

P3_PRIMARIES = np.array([
    [0.6800, 0.3200],  # Red
    [0.2650, 0.6900],  # Green
    [0.1500, 0.0600],  # Blue
])

ADOBE_RGB_PRIMARIES = np.array([
    [0.6400, 0.3300],  # Red
    [0.2100, 0.7100],  # Green
    [0.1500, 0.0600],  # Blue
])

# White points
D65 = np.array([0.3127, 0.3290])
ILLUMINANT_C = np.array([0.3101, 0.3162])


# =============================================================================
# Panel A: CIE xy Chromaticity Diagram
# =============================================================================

def plot_chromaticity_diagram(ax):
    """Plot CIE xy chromaticity diagram with color space gamuts."""

    # Plot spectrum locus
    locus = np.vstack([SPECTRUM_LOCUS_XY, SPECTRUM_LOCUS_XY[0]])  # Close the curve
    ax.plot(locus[:, 0], locus[:, 1], 'k-', linewidth=1.5, label='Spectrum locus')

    # Fill with a light representation of visible colors (simplified)
    from matplotlib.patches import Polygon as MplPolygon
    from matplotlib.colors import LinearSegmentedColormap

    # Create a filled polygon for the visible gamut (light gray background)
    visible_gamut = MplPolygon(SPECTRUM_LOCUS_XY, closed=True,
                                facecolor='#f0f0f0', edgecolor='none', alpha=0.5)
    ax.add_patch(visible_gamut)

    # Plot sRGB gamut
    srgb_triangle = np.vstack([SRGB_PRIMARIES, SRGB_PRIMARIES[0]])
    ax.plot(srgb_triangle[:, 0], srgb_triangle[:, 1], 'b-', linewidth=2, label='sRGB')
    srgb_patch = MplPolygon(SRGB_PRIMARIES, closed=True,
                            facecolor='blue', edgecolor='none', alpha=0.15)
    ax.add_patch(srgb_patch)

    # Plot P3 gamut
    p3_triangle = np.vstack([P3_PRIMARIES, P3_PRIMARIES[0]])
    ax.plot(p3_triangle[:, 0], p3_triangle[:, 1], 'g-', linewidth=2, label='Display P3')
    p3_patch = MplPolygon(P3_PRIMARIES, closed=True,
                          facecolor='green', edgecolor='none', alpha=0.1)
    ax.add_patch(p3_patch)

    # Plot Adobe RGB gamut
    adobe_triangle = np.vstack([ADOBE_RGB_PRIMARIES, ADOBE_RGB_PRIMARIES[0]])
    ax.plot(adobe_triangle[:, 0], adobe_triangle[:, 1], 'r--', linewidth=1.5,
            label='Adobe RGB', alpha=0.7)

    # Mark white points
    ax.plot(*D65, 'ko', markersize=6)
    ax.annotate('D65', D65, textcoords='offset points', xytext=(5, 5), fontsize=8)

    ax.plot(*ILLUMINANT_C, 'k^', markersize=5)
    ax.annotate('C', ILLUMINANT_C, textcoords='offset points', xytext=(5, -10), fontsize=8)

    # Mark wavelength labels
    wavelengths_to_label = [450, 480, 500, 520, 550, 580, 600, 650]
    wavelength_indices = {w: (w - 380) // 5 for w in wavelengths_to_label}

    for wl, idx in wavelength_indices.items():
        if 0 <= idx < len(SPECTRUM_LOCUS_XY):
            x, y = SPECTRUM_LOCUS_XY[idx]
            # Offset direction based on position
            if wl < 500:
                offset = (-15, -5)
            elif wl < 550:
                offset = (-5, 10)
            else:
                offset = (5, 5)
            ax.annotate(f'{wl}', (x, y), textcoords='offset points',
                       xytext=offset, fontsize=7, color='gray')

    # Formatting
    ax.set_xlim(0, 0.8)
    ax.set_ylim(0, 0.9)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('(A) CIE 1931 xy Chromaticity')
    ax.legend(loc='upper right', fontsize=8)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)


# =============================================================================
# Panel B: Munsell Value Slices
# =============================================================================

def munsell_to_cartesian(hue_number: float, hue_letter: str, value: float, chroma: float) -> Tuple[float, float, float]:
    """Convert Munsell HVC to Cartesian (x, y, z) coordinates."""
    # Munsell hue order and conversion to angle
    hue_order = ['R', 'YR', 'Y', 'GY', 'G', 'BG', 'B', 'PB', 'P', 'RP']
    try:
        hue_idx = hue_order.index(hue_letter)
    except ValueError:
        hue_idx = 0

    # Continuous hue: 0-100 scale
    continuous_hue = hue_idx * 10 + hue_number

    # Convert to radians (Munsell convention: R=0° at positive x-axis)
    angle_rad = continuous_hue * np.pi / 50.0

    x = chroma * np.cos(angle_rad)
    y = chroma * np.sin(angle_rad)
    z = value

    return (x, y, z)


def get_munsell_max_chroma_at_value(value: int) -> Dict[str, float]:
    """Get approximate maximum Munsell chroma for each hue at given value.

    These are simplified approximations based on typical renotation limits.
    """
    # Approximate max chromas vary by hue and value
    # Higher values have different max chromas than lower values

    if value <= 2:
        base_chroma = 4
    elif value <= 4:
        base_chroma = 8
    elif value <= 6:
        base_chroma = 12
    elif value <= 8:
        base_chroma = 10
    else:
        base_chroma = 6

    # Hue-dependent multipliers (reds and blues tend to have higher chroma)
    hue_multipliers = {
        'R': 1.4, 'YR': 1.2, 'Y': 1.0, 'GY': 0.8, 'G': 0.7,
        'BG': 0.8, 'B': 1.0, 'PB': 1.3, 'P': 1.2, 'RP': 1.3
    }

    return {hue: base_chroma * mult for hue, mult in hue_multipliers.items()}


def rgb_to_munsell_approx(r: int, g: int, b: int) -> Tuple[float, float, float]:
    """Approximate RGB to Munsell (returns x, y, z in Cartesian Munsell space)."""
    # Normalize
    r_n, g_n, b_n = r / 255.0, g / 255.0, b / 255.0

    # Approximate value from luminance
    value = (0.2126 * r_n + 0.7152 * g_n + 0.0722 * b_n) * 10

    # Approximate chroma and hue from HSV
    max_c = max(r_n, g_n, b_n)
    min_c = min(r_n, g_n, b_n)
    delta = max_c - min_c

    if delta < 0.01:  # Neutral
        return (0, 0, value)

    # Chroma (scaled)
    chroma = delta * 14 / max(max_c, 0.01)

    # Hue angle
    if max_c == r_n:
        h = 60 * (((g_n - b_n) / delta) % 6)
    elif max_c == g_n:
        h = 60 * ((b_n - r_n) / delta + 2)
    else:
        h = 60 * ((r_n - g_n) / delta + 4)

    # Convert HSV hue (0-360) to Munsell continuous hue (0-100)
    # HSV: 0=R, 60=Y, 120=G, 180=C, 240=B, 300=M
    # Munsell: 0=R, 20=Y, 40=G, 50=BG, 60=B, 80=P, 100=R
    h_munsell = (h / 360.0) * 100.0

    angle_rad = h_munsell * np.pi / 50.0
    x = chroma * np.cos(angle_rad)
    y = chroma * np.sin(angle_rad)

    return (x, y, value)


def compute_srgb_gamut_at_value(target_value: float, n_samples: int = 72) -> np.ndarray:
    """Compute sRGB gamut boundary at a specific Munsell value level."""

    # Sample RGB cube and filter by value
    boundary_points = []

    # Sample edges of RGB cube
    for i in range(256):
        for r, g, b in [
            (i, 0, 0), (i, 255, 0), (i, 0, 255), (i, 255, 255),
            (0, i, 0), (255, i, 0), (0, i, 255), (255, i, 255),
            (0, 0, i), (255, 0, i), (0, 255, i), (255, 255, i),
        ]:
            x, y, v = rgb_to_munsell_approx(r, g, b)
            if abs(v - target_value) < 0.5:  # Within 0.5 of target value
                boundary_points.append([x, y])

    if not boundary_points:
        return np.array([])

    boundary_points = np.array(boundary_points)

    # Find convex hull or polar boundary
    if len(boundary_points) < 3:
        return boundary_points

    # Convert to polar and find max radius per angle
    angles = np.arctan2(boundary_points[:, 1], boundary_points[:, 0])
    radii = np.sqrt(boundary_points[:, 0]**2 + boundary_points[:, 1]**2)

    # Bin by angle and take max radius
    angle_bins = np.linspace(-np.pi, np.pi, n_samples + 1)
    boundary = []

    for i in range(n_samples):
        mask = (angles >= angle_bins[i]) & (angles < angle_bins[i + 1])
        if np.any(mask):
            max_r = np.max(radii[mask])
            mid_angle = (angle_bins[i] + angle_bins[i + 1]) / 2
            boundary.append([max_r * np.cos(mid_angle), max_r * np.sin(mid_angle)])

    return np.array(boundary) if boundary else np.array([])


def plot_munsell_value_slices(ax, values=[3, 5, 7]):
    """Plot Munsell chroma diagrams at different value levels."""

    colors = ['#e74c3c', '#2ecc71', '#3498db']  # Red, Green, Blue for V=3,5,7

    hue_order = ['R', 'YR', 'Y', 'GY', 'G', 'BG', 'B', 'PB', 'P', 'RP']

    for i, v in enumerate(values):
        # Get max chroma boundary for this value
        max_chromas = get_munsell_max_chroma_at_value(v)

        # Build boundary polygon
        boundary_points = []
        for hue_letter in hue_order:
            for hue_number in [2.5, 5.0, 7.5, 10.0]:
                chroma = max_chromas.get(hue_letter, 8)
                x, y, _ = munsell_to_cartesian(hue_number, hue_letter, v, chroma)
                boundary_points.append([x, y])

        boundary = np.array(boundary_points)
        boundary = np.vstack([boundary, boundary[0]])  # Close

        ax.plot(boundary[:, 0], boundary[:, 1], '-', color=colors[i],
                linewidth=2, label=f'V={v} (Munsell limit)', alpha=0.8)

        # sRGB gamut at this value
        srgb_boundary = compute_srgb_gamut_at_value(v)
        if len(srgb_boundary) > 2:
            srgb_boundary = np.vstack([srgb_boundary, srgb_boundary[0]])
            ax.plot(srgb_boundary[:, 0], srgb_boundary[:, 1], '--',
                   color=colors[i], linewidth=1.5, alpha=0.6)

    # Add hue labels
    for idx, hue in enumerate(hue_order):
        angle = idx * 10 * np.pi / 50  # Munsell angle
        label_r = 16
        ax.text(label_r * np.cos(angle), label_r * np.sin(angle), hue,
               ha='center', va='center', fontsize=8, color='gray')

    # Draw radial lines
    for idx in range(10):
        angle = idx * 10 * np.pi / 50
        ax.plot([0, 14*np.cos(angle)], [0, 14*np.sin(angle)],
               'k-', alpha=0.1, linewidth=0.5)

    # Draw chroma circles
    for c in [4, 8, 12]:
        circle = plt.Circle((0, 0), c, fill=False, color='gray',
                            linestyle=':', linewidth=0.5, alpha=0.5)
        ax.add_patch(circle)
        ax.text(c + 0.3, 0, f'C={c}', fontsize=7, color='gray')

    ax.set_xlim(-18, 18)
    ax.set_ylim(-18, 18)
    ax.set_xlabel('x (Chroma × cos θ)')
    ax.set_ylabel('y (Chroma × sin θ)')
    ax.set_title('(B) Munsell Gamut at Value Levels')
    ax.legend(loc='upper right', fontsize=8)
    ax.set_aspect('equal')
    ax.axhline(y=0, color='k', linewidth=0.5, alpha=0.3)
    ax.axvline(x=0, color='k', linewidth=0.5, alpha=0.3)


# =============================================================================
# Panel C: Calibration Bias Visualization
# =============================================================================

def load_calibration_data() -> Optional[Dict]:
    """Load Track B Phase 3 calibration results."""
    calib_path = DATA_DIR / "track_b_phase3_calibration.json"
    if calib_path.exists():
        with open(calib_path) as f:
            return json.load(f)
    return None


def plot_calibration_bias(ax):
    """Plot screen-surface calibration bias visualization."""

    calib = load_calibration_data()

    # Use actual data if available, otherwise use documented values
    if calib and 'aggregate_bias' in calib:
        value_bias = calib['aggregate_bias']['value']['mean']
        chroma_bias = calib['aggregate_bias']['chroma']['mean']
        hue_mean = calib['aggregate_bias']['hue']['mean']
        hue_std = calib['aggregate_bias']['hue']['std']
        per_family = calib.get('per_family', [])
    else:
        # Default values from research notes
        value_bias = 2.06
        chroma_bias = 0.80
        hue_mean = -31.8
        hue_std = 21.0
        per_family = []

    # Create hue wheel with rotation arrows
    hue_order = ['R', 'YR', 'Y', 'GY', 'G', 'BG', 'B', 'PB', 'P', 'RP']

    # Draw base hue wheel
    theta = np.linspace(0, 2*np.pi, 100)
    ax.plot(np.cos(theta), np.sin(theta), 'k-', linewidth=1, alpha=0.3)
    ax.plot(0.6*np.cos(theta), 0.6*np.sin(theta), 'k-', linewidth=0.5, alpha=0.2)

    # Plot per-family hue bias if available
    if per_family:
        for fam in per_family:
            if fam.get('hue_bias') is not None:
                # Find hue position
                family_name = fam['family'].lower()
                # Map family to approximate hue position
                family_hue_map = {
                    'red': 0, 'orange': 1, 'yellow': 2, 'green': 4,
                    'blue': 6, 'purple': 8, 'pink': 9, 'brown': 1,
                    'coral': 0.5, 'peach': 1, 'gold': 1.5, 'tan': 1.5,
                    'beige': 1.5, 'rust': 0.5, 'sand': 2, 'wine': 9,
                    'violet': 7, 'lavender': 7.5, 'lilac': 8, 'mauve': 8,
                    'magenta': 8.5, 'fuchsia': 8.5, 'rose': 9, 'teal': 5,
                    'turquoise': 5.5, 'aqua': 5, 'navy': 6.5, 'taupe': 1
                }

                hue_pos = family_hue_map.get(family_name, 0)
                base_angle = hue_pos * np.pi / 5  # 10 hue sectors

                # Draw rotation arrow
                rotation = np.radians(fam['hue_bias'])
                new_angle = base_angle + rotation

                # Arrow from original to rotated position
                r = 0.8
                ax.annotate('',
                           xy=(r*np.cos(new_angle), r*np.sin(new_angle)),
                           xytext=(r*np.cos(base_angle), r*np.sin(base_angle)),
                           arrowprops=dict(arrowstyle='->', color='red', alpha=0.5, lw=1))

    # Add hue labels
    for idx, hue in enumerate(hue_order):
        angle = idx * np.pi / 5
        ax.text(1.15*np.cos(angle), 1.15*np.sin(angle), hue,
               ha='center', va='center', fontsize=9, fontweight='bold')

        # Small colored dot
        # Map Munsell hue to approximate RGB for visualization
        hue_colors = {
            'R': '#e74c3c', 'YR': '#e67e22', 'Y': '#f1c40f', 'GY': '#a4d037',
            'G': '#2ecc71', 'BG': '#1abc9c', 'B': '#3498db', 'PB': '#5b6dcb',
            'P': '#9b59b6', 'RP': '#e84393'
        }
        ax.plot(0.95*np.cos(angle), 0.95*np.sin(angle), 'o',
               color=hue_colors.get(hue, 'gray'), markersize=8)

    # Add text box with bias summary
    textstr = (f'Screen → Surface Bias\n'
               f'─────────────────\n'
               f'Value:  {value_bias:+.2f}\n'
               f'Chroma: {chroma_bias:+.2f}\n'
               f'Hue:    {hue_mean:+.1f}° ± {hue_std:.1f}°')

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    ax.text(0.02, 0.02, textstr, transform=ax.transAxes, fontsize=9,
           verticalalignment='bottom', bbox=props, family='monospace')

    ax.set_xlim(-1.4, 1.4)
    ax.set_ylim(-1.4, 1.4)
    ax.set_title('(C) Screen-Surface Hue Rotation')
    ax.set_aspect('equal')
    ax.axis('off')

    # Add legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='>', color='red', alpha=0.5,
               label=f'Hue rotation (mean {hue_mean:.0f}°)',
               markersize=0, linewidth=2),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=8)


# =============================================================================
# Main Figure Generation
# =============================================================================

def generate_gamut_comparison_figure():
    """Generate the complete multi-panel gamut comparison figure."""

    print("=" * 70)
    print("Task 117: Gamut Comparison Visualization")
    print("=" * 70)

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    # Create figure with three panels
    fig = plt.figure(figsize=(14, 5))

    # Panel A: Chromaticity diagram
    ax1 = fig.add_subplot(131)
    print("\nGenerating Panel A: CIE xy Chromaticity Diagram...")
    plot_chromaticity_diagram(ax1)

    # Panel B: Munsell value slices
    ax2 = fig.add_subplot(132)
    print("Generating Panel B: Munsell Value Slices...")
    plot_munsell_value_slices(ax2)

    # Panel C: Calibration bias
    ax3 = fig.add_subplot(133)
    print("Generating Panel C: Calibration Bias Visualization...")
    plot_calibration_bias(ax3)

    plt.tight_layout()

    # Save in multiple formats
    base_name = "gamut_comparison"

    for fmt in ['png', 'svg', 'pdf']:
        output_path = FIGURES_DIR / f"{base_name}.{fmt}"
        fig.savefig(output_path, dpi=300 if fmt == 'png' else None,
                   bbox_inches='tight', facecolor='white')
        print(f"  Saved: {output_path}")

    plt.close(fig)

    print()
    print("=" * 70)
    print("Figure Generation Complete")
    print("=" * 70)
    print(f"\nOutput directory: {FIGURES_DIR}")


if __name__ == "__main__":
    generate_gamut_comparison_figure()
