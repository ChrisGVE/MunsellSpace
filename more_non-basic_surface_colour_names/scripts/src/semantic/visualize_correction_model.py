#!/usr/bin/env python3
"""
Visualize the Fourier Hue Correction Model

Creates comprehensive visualizations of the correction model showing:
1. The continuous correction curve
2. Data points (Centore reference) vs model predictions
3. Residuals analysis
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import hsv_to_rgb

def load_model():
    """Load the fitted model parameters."""
    with open('fourier_correction_model.json', 'r') as f:
        return json.load(f)

def load_distribution_results():
    """Load distribution comparison results."""
    with open('distribution_comparison_results.json', 'r') as f:
        return json.load(f)

def normalize_angle(angle):
    """Normalize angle to [-180, 180]."""
    while angle > 180:
        angle -= 360
    while angle < -180:
        angle += 360
    return angle

def fourier_predict(hue, coeffs, n_harmonics):
    """Predict hue shift using Fourier model."""
    hue_rad = np.radians(hue)
    correction = coeffs['a0']
    for k in range(1, n_harmonics + 1):
        correction += coeffs[f'a{k}'] * np.cos(k * hue_rad)
        correction += coeffs[f'b{k}'] * np.sin(k * hue_rad)
    return correction

def main():
    model = load_model()
    dist_results = load_distribution_results()

    coeffs = model['model']['coefficients']
    n_harmonics = model['model']['n_harmonics']

    # Extract data points
    overlays = []
    for name, overlay in dist_results['overlays'].items():
        circ_stats = overlay['circular_statistics']['hue']
        overlays.append({
            'name': name,
            'centore_hue': circ_stats['centore_mean'],
            'shift': normalize_angle(circ_stats['shift']),
            'n_xkcd': overlay['n_xkcd'],
        })

    # Sort by Centore hue
    overlays.sort(key=lambda x: x['centore_hue'])

    # Generate correction curve
    hues = np.linspace(0, 360, 361)
    corrections = [fourier_predict(h, coeffs, n_harmonics) for h in hues]

    # Normalize corrections for display
    corrections_normalized = [normalize_angle(c) for c in corrections]

    # Create figure with multiple subplots
    fig = plt.figure(figsize=(16, 12))

    # ===== Plot 1: Correction curve with data points =====
    ax1 = fig.add_subplot(2, 2, 1)

    # Background color gradient (hue wheel)
    for i in range(360):
        rgb = hsv_to_rgb([i/360, 0.5, 0.95])
        ax1.axvspan(i, i+1, color=rgb, alpha=0.3)

    # Plot the correction curve
    ax1.plot(hues, corrections_normalized, 'b-', linewidth=2, label='Fourier model (5 harmonics)')

    # Plot data points
    x_data = [o['centore_hue'] for o in overlays]
    y_data = [o['shift'] for o in overlays]
    sizes = [o['n_xkcd'] / 20 for o in overlays]  # Scale by sample size

    ax1.scatter(x_data, y_data, s=sizes, c='red', edgecolors='black',
               linewidth=0.5, zorder=5, label='Centore reference (size=N)')

    # Add overlay labels
    for o in overlays:
        ax1.annotate(o['name'], (o['centore_hue'], o['shift']),
                    fontsize=7, ha='left', va='bottom', rotation=20)

    ax1.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax1.set_xlabel('Centore Reference Hue (°)', fontsize=12)
    ax1.set_ylabel('Hue Shift: XKCD - Centore (°)', fontsize=12)
    ax1.set_title('Hue Correction Model vs Reference Data', fontsize=14)
    ax1.set_xlim(0, 360)
    ax1.set_ylim(-180, 180)
    ax1.legend(loc='lower left')
    ax1.grid(True, alpha=0.3)

    # ===== Plot 2: Residuals =====
    ax2 = fig.add_subplot(2, 2, 2)

    residuals = []
    for o in overlays:
        pred = fourier_predict(o['centore_hue'], coeffs, n_harmonics)
        residual = normalize_angle(pred - o['shift'])
        residuals.append({
            'name': o['name'],
            'hue': o['centore_hue'],
            'residual': residual,
            'n_xkcd': o['n_xkcd']
        })

    residual_vals = [r['residual'] for r in residuals]
    hue_vals = [r['hue'] for r in residuals]
    colors = ['green' if abs(r) < 2 else 'orange' if abs(r) < 5 else 'red' for r in residual_vals]

    bars = ax2.bar(range(len(residuals)), residual_vals, color=colors, edgecolor='black', linewidth=0.5)
    ax2.set_xticks(range(len(residuals)))
    ax2.set_xticklabels([r['name'] for r in residuals], rotation=45, ha='right', fontsize=8)
    ax2.axhline(y=0, color='gray', linestyle='-', alpha=0.5)
    ax2.set_ylabel('Residual (Predicted - Actual) (°)')
    ax2.set_title('Model Residuals by Overlay')
    ax2.grid(True, alpha=0.3, axis='y')

    # Add threshold lines
    ax2.axhline(y=2, color='green', linestyle='--', alpha=0.5, label='±2°')
    ax2.axhline(y=-2, color='green', linestyle='--', alpha=0.5)
    ax2.axhline(y=5, color='orange', linestyle='--', alpha=0.5, label='±5°')
    ax2.axhline(y=-5, color='orange', linestyle='--', alpha=0.5)
    ax2.legend()

    # ===== Plot 3: Polar visualization of correction =====
    ax3 = fig.add_subplot(2, 2, 3, projection='polar')

    # Convert to radians
    theta = np.radians(hues)
    # Radius represents magnitude of correction
    r_correction = np.abs(corrections_normalized)

    # Color by direction (positive=red, negative=blue)
    for i in range(len(hues) - 1):
        color = 'orangered' if corrections_normalized[i] > 0 else 'dodgerblue'
        ax3.plot(theta[i:i+2], r_correction[i:i+2], color=color, linewidth=1)

    # Add data points
    for o in overlays:
        t = np.radians(o['centore_hue'])
        r = abs(o['shift'])
        color = 'orangered' if o['shift'] > 0 else 'dodgerblue'
        ax3.scatter([t], [r], c=color, s=50, edgecolors='black', linewidth=0.5, zorder=5)

    ax3.set_title('Correction Magnitude by Hue\n(red=positive shift, blue=negative)', fontsize=12)
    ax3.set_theta_zero_location('N')
    ax3.set_theta_direction(-1)

    # ===== Plot 4: Before/After hue positions =====
    ax4 = fig.add_subplot(2, 2, 4)

    # Draw the color wheel as background
    for i in range(360):
        rgb = hsv_to_rgb([i/360, 0.6, 0.9])
        ax4.scatter([i], [0.5], c=[rgb], s=20, marker='s')

    # Plot Centore positions (bottom) and XKCD positions (top)
    for o in overlays:
        centore_h = o['centore_hue']
        xkcd_h = dist_results['overlays'][o['name']]['circular_statistics']['hue']['xkcd_mean']

        # Draw arrow from XKCD to Centore (showing the correction direction)
        arrow_color = 'green' if abs(o['shift']) < 30 else 'orange' if abs(o['shift']) < 90 else 'red'

        ax4.annotate('', xy=(centore_h, 0.2), xytext=(xkcd_h, 0.8),
                    arrowprops=dict(arrowstyle='->', color=arrow_color, lw=1.5, alpha=0.7))

        # Mark positions
        ax4.scatter([centore_h], [0.2], c='blue', s=40, marker='v', zorder=5)
        ax4.scatter([xkcd_h], [0.8], c='red', s=40, marker='^', zorder=5)

    # Add legend
    ax4.scatter([], [], c='blue', s=40, marker='v', label='Centore (reference)')
    ax4.scatter([], [], c='red', s=40, marker='^', label='XKCD (screen)')
    ax4.legend(loc='upper right')

    ax4.set_xlim(0, 360)
    ax4.set_ylim(0, 1)
    ax4.set_xlabel('Hue (°)')
    ax4.set_yticks([0.2, 0.8])
    ax4.set_yticklabels(['Reference', 'Screen'])
    ax4.set_title('Hue Mapping: Screen → Reference')
    ax4.grid(True, alpha=0.3, axis='x')

    plt.tight_layout()
    plt.savefig('correction_model_visualization.png', dpi=150, bbox_inches='tight')
    print("Saved: correction_model_visualization.png")

    # Print summary statistics
    print("\n" + "=" * 60)
    print("MODEL SUMMARY")
    print("=" * 60)
    print(f"Model: Fourier ({n_harmonics} harmonics)")
    print(f"Weighted MAE (CV): {model['cv_results']['weighted_mae']:.2f}°")
    print(f"\nCoefficients:")
    for key, val in coeffs.items():
        print(f"  {key}: {val:+.4f}")
    print(f"\nValue offset: {model['model']['value_offset']:+.3f}")
    print(f"Chroma offset: {model['model']['chroma_offset']:+.3f}")

    print("\n" + "-" * 60)
    print("Residuals:")
    print("-" * 60)
    residual_vals = [abs(r['residual']) for r in residuals]
    print(f"  Mean |residual|: {np.mean(residual_vals):.2f}°")
    print(f"  Max |residual|: {max(residual_vals):.2f}°")
    print(f"  Within ±2°: {sum(1 for r in residual_vals if r < 2)}/{len(residual_vals)}")
    print(f"  Within ±5°: {sum(1 for r in residual_vals if r < 5)}/{len(residual_vals)}")

if __name__ == '__main__':
    main()
