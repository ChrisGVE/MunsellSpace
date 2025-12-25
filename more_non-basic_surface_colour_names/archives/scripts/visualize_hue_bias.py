#!/usr/bin/env python3
"""
Visualize the hue-dependent bias pattern between Centore reference and XKCD screen data.

This script analyzes the systematic bias in hue perception between colorimetrically
measured Centore overlays and screen-selected XKCD color data.
"""

import json
import numpy as np
import matplotlib.pyplot as plt

def load_results():
    """Load the distribution comparison results."""
    with open('distribution_comparison_results.json', 'r') as f:
        return json.load(f)

def extract_hue_data(results):
    """Extract Centore hue positions and measured shifts."""
    data = []
    for name, overlay in results['overlays'].items():
        centore_hue = overlay['sliced_wasserstein']['shift']['centore_centroid']['hue']
        # Use circular statistics for more accurate hue measurement
        circ_stats = overlay['circular_statistics']['hue']
        centore_mean = circ_stats['centore_mean']
        xkcd_mean = circ_stats['xkcd_mean']

        # Calculate angular difference (handling circularity)
        shift = circ_stats['shift']

        # Also get the raw SWD shift for comparison
        swd_shift = overlay['sliced_wasserstein']['shift']['hue_shift']

        data.append({
            'name': name,
            'centore_hue': centore_mean,
            'xkcd_hue': xkcd_mean,
            'circular_shift': shift,
            'swd_shift': swd_shift,
            'n_centore': overlay['n_centore'],
            'n_xkcd': overlay['n_xkcd'],
        })

    return data

def normalize_angle(angle):
    """Normalize angle to [-180, 180] range."""
    while angle > 180:
        angle -= 360
    while angle < -180:
        angle += 360
    return angle

def main():
    results = load_results()
    data = extract_hue_data(results)

    # Sort by Centore hue for visualization
    data.sort(key=lambda x: x['centore_hue'])

    # Extract arrays
    names = [d['name'] for d in data]
    centore_hues = np.array([d['centore_hue'] for d in data])
    xkcd_hues = np.array([d['xkcd_hue'] for d in data])
    circular_shifts = np.array([d['circular_shift'] for d in data])
    swd_shifts = np.array([d['swd_shift'] for d in data])

    print("=" * 80)
    print("HUE BIAS ANALYSIS: Centore (Reference) vs XKCD (Screen)")
    print("=" * 80)
    print()

    # Print per-overlay data
    print(f"{'Overlay':<12} {'Centore H°':>10} {'XKCD H°':>10} {'Shift°':>10} {'Direction':<15}")
    print("-" * 60)

    for d in data:
        shift = d['circular_shift']
        direction = "XKCD warmer" if shift > 0 else "XKCD cooler"
        print(f"{d['name']:<12} {d['centore_hue']:>10.1f} {d['xkcd_hue']:>10.1f} {shift:>+10.1f} {direction:<15}")

    print()
    print("=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)

    # Normalize shifts to [-180, 180]
    normalized_shifts = np.array([normalize_angle(s) for s in circular_shifts])

    print(f"\nCircular shift statistics (normalized to ±180°):")
    print(f"  Mean:   {np.mean(normalized_shifts):+.2f}°")
    print(f"  Median: {np.median(normalized_shifts):+.2f}°")
    print(f"  Std:    {np.std(normalized_shifts):.2f}°")
    print(f"  Range:  [{np.min(normalized_shifts):.1f}°, {np.max(normalized_shifts):.1f}°]")

    # Analyze by color wheel quadrant
    print("\n" + "-" * 60)
    print("Analysis by Color Wheel Position:")
    print("-" * 60)

    # Define hue regions (Munsell-style)
    regions = [
        ("Red-Yellow (0-60°)", 0, 60),
        ("Yellow-Green (60-120°)", 60, 120),
        ("Green-Cyan (120-180°)", 120, 180),
        ("Cyan-Blue (180-240°)", 180, 240),
        ("Blue-Purple (240-300°)", 240, 300),
        ("Purple-Red (300-360°)", 300, 360),
    ]

    for region_name, low, high in regions:
        region_data = [d for d in data if low <= d['centore_hue'] < high]
        if region_data:
            region_shifts = [normalize_angle(d['circular_shift']) for d in region_data]
            mean_shift = np.mean(region_shifts)
            overlays = ", ".join([d['name'] for d in region_data])
            print(f"\n{region_name}:")
            print(f"  Overlays: {overlays}")
            print(f"  Mean shift: {mean_shift:+.1f}°")

    # Create visualizations
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # Plot 1: Centore hue vs Shift (scatter with labels)
    ax1 = axes[0, 0]
    colors = plt.cm.hsv(centore_hues / 360)
    ax1.scatter(centore_hues, normalized_shifts, c=colors, s=100, edgecolors='black', linewidth=0.5)
    for i, name in enumerate(names):
        ax1.annotate(name, (centore_hues[i], normalized_shifts[i]),
                    fontsize=8, ha='left', va='bottom', rotation=30)
    ax1.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax1.set_xlabel('Centore Reference Hue (°)')
    ax1.set_ylabel('Hue Shift: XKCD - Centore (°)')
    ax1.set_title('Hue-Dependent Bias Pattern')
    ax1.set_xlim(0, 360)
    ax1.grid(True, alpha=0.3)

    # Plot 2: Polar plot showing shift vectors
    ax2 = axes[0, 1]
    ax2 = plt.subplot(2, 2, 2, projection='polar')
    theta = np.radians(centore_hues)
    # Use shift magnitude as radial distance, color by direction
    for i in range(len(data)):
        color = 'orangered' if normalized_shifts[i] > 0 else 'dodgerblue'
        arrow_length = abs(normalized_shifts[i]) / 30  # Scale for visibility
        ax2.annotate('',
                    xy=(theta[i] + np.radians(normalized_shifts[i]/5), arrow_length),
                    xytext=(theta[i], 0),
                    arrowprops=dict(arrowstyle='->', color=color, lw=1.5))
    ax2.set_title('Bias Direction on Color Wheel\n(red=warmer, blue=cooler)')

    # Plot 3: Bar chart of shifts ordered by hue
    ax3 = axes[1, 0]
    bar_colors = ['orangered' if s > 0 else 'dodgerblue' for s in normalized_shifts]
    bars = ax3.bar(range(len(names)), normalized_shifts, color=bar_colors, edgecolor='black', linewidth=0.5)
    ax3.set_xticks(range(len(names)))
    ax3.set_xticklabels(names, rotation=45, ha='right', fontsize=8)
    ax3.axhline(y=0, color='gray', linestyle='-', alpha=0.5)
    ax3.set_ylabel('Hue Shift (°)')
    ax3.set_title('Hue Shift by Overlay (ordered by Centore hue)')
    ax3.grid(True, alpha=0.3, axis='y')

    # Plot 4: Centore vs XKCD hue positions
    ax4 = axes[1, 1]
    ax4.scatter(centore_hues, xkcd_hues, c=colors, s=100, edgecolors='black', linewidth=0.5)
    ax4.plot([0, 360], [0, 360], 'k--', alpha=0.3, label='Perfect agreement')
    for i, name in enumerate(names):
        ax4.annotate(name, (centore_hues[i], xkcd_hues[i]),
                    fontsize=7, ha='left', va='bottom')
    ax4.set_xlabel('Centore Reference Hue (°)')
    ax4.set_ylabel('XKCD Screen Hue (°)')
    ax4.set_title('Hue Position: Reference vs Screen')
    ax4.set_xlim(0, 360)
    ax4.set_ylim(0, 360)
    ax4.set_aspect('equal')
    ax4.grid(True, alpha=0.3)
    ax4.legend()

    plt.tight_layout()
    plt.savefig('hue_bias_analysis.png', dpi=150, bbox_inches='tight')
    print(f"\nVisualization saved to: hue_bias_analysis.png")

    # Also save the extracted data for further analysis
    output_data = {
        'overlays': data,
        'summary': {
            'mean_shift': float(np.mean(normalized_shifts)),
            'median_shift': float(np.median(normalized_shifts)),
            'std_shift': float(np.std(normalized_shifts)),
            'min_shift': float(np.min(normalized_shifts)),
            'max_shift': float(np.max(normalized_shifts)),
        }
    }

    with open('hue_bias_analysis.json', 'w') as f:
        json.dump(output_data, f, indent=2)
    print(f"Data saved to: hue_bias_analysis.json")

    # Return data for Fourier fitting
    return centore_hues, normalized_shifts, names

if __name__ == '__main__':
    main()
