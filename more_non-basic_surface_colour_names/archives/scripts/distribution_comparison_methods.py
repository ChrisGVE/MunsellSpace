#!/usr/bin/env python3
"""
Distribution Comparison Methods for Color Bias Detection

Implements four statistical approaches to compare Centore (physical) and XKCD (screen)
color distributions, with proper null hypothesis testing and p-values.

Methods:
1. Sliced Wasserstein Distance (with hue unfolding for circularity)
2. Circular Statistics (von Mises for hue dimension)
3. Procrustes Analysis (rigid transformation alignment)
4. GMM + KL Divergence (distribution modeling)

Usage:
    python distribution_comparison_methods.py
"""

import json
import re
import math
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

# Try to import optional dependencies
try:
    from scipy import stats
    from scipy.spatial import procrustes
    from scipy.stats import wasserstein_distance
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    print("Warning: scipy not available. Some methods will be skipped.")

try:
    from sklearn.mixture import GaussianMixture
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("Warning: sklearn not available. GMM method will be skipped.")


@dataclass
class MunsellPoint:
    """A point in Munsell color space."""
    hue_num: float  # 0-360 degrees
    value: float    # 0-10
    chroma: float   # 0+
    name: str = ""

    def to_cartesian(self) -> np.ndarray:
        """Convert to Cartesian coordinates (x, y, z) where z is value."""
        if self.chroma < 0.5:
            return np.array([0.0, 0.0, self.value])
        hue_rad = self.hue_num * np.pi / 180.0
        x = self.chroma * np.cos(hue_rad)
        y = self.chroma * np.sin(hue_rad)
        return np.array([x, y, self.value])

    def to_cylindrical(self) -> np.ndarray:
        """Return (hue, value, chroma) as array."""
        return np.array([self.hue_num, self.value, self.chroma])


class DataLoader:
    """Load and parse Centore and XKCD color data."""

    HUE_FAMILIES = {
        'R': 0, 'YR': 36, 'Y': 72, 'GY': 108,
        'G': 144, 'BG': 180, 'B': 216, 'PB': 252,
        'P': 288, 'RP': 324
    }

    # Original 20 Centore overlays (from his paper)
    CENTORE_20 = [
        'aqua', 'beige', 'coral', 'fuchsia', 'gold', 'lavender', 'lilac',
        'magenta', 'mauve', 'navy', 'peach', 'rose', 'rust', 'sand',
        'tan', 'taupe', 'teal', 'turquoise', 'violet', 'wine'
    ]

    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.polyhedron_dir = self.project_root / "PolyhedronFilesJustNames"
        self.investigation_dir = Path(__file__).parent

    def parse_munsell_notation(self, notation: str) -> Optional[MunsellPoint]:
        """Parse Munsell notation string to MunsellPoint."""
        notation = notation.strip()

        # Handle neutral colors
        if notation.startswith('N ') or notation.startswith('N/'):
            try:
                value = float(notation.split()[1].split('/')[0])
                return MunsellPoint(0.0, value, 0.0)
            except (IndexError, ValueError):
                return None

        # Parse chromatic colors: "5.61P 5.37/4.79"
        match = re.match(
            r'(\d+\.?\d*)(R|YR|Y|GY|G|BG|B|PB|P|RP)\s+(\d+\.?\d*)/(\d+\.?\d*)',
            notation
        )
        if match:
            hue_value = float(match.group(1))
            hue_family = match.group(2)
            value = float(match.group(3))
            chroma = float(match.group(4))

            family_base = self.HUE_FAMILIES.get(hue_family, 0)
            hue_num = family_base + (hue_value / 10.0) * 36.0
            if hue_num >= 360:
                hue_num -= 360

            return MunsellPoint(hue_num, value, chroma)
        return None

    def load_centore_samples(self, overlay_name: str) -> List[MunsellPoint]:
        """Load sample points from Centore polyhedron file."""
        filepath = self.polyhedron_dir / f"PolyhedronDataFor{overlay_name}.txt"
        if not filepath.exists():
            return []

        points = []
        in_samples = False

        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith("Samples, with Munsell coordinates"):
                    in_samples = True
                    continue
                if in_samples and line:
                    # Format: "Sample Name\tMunsell notation"
                    parts = line.split('\t')
                    if len(parts) >= 2:
                        notation = parts[-1]
                        point = self.parse_munsell_notation(notation)
                        if point:
                            point.name = parts[0]
                            points.append(point)
        return points

    def load_xkcd_matches(self, overlay_name: str) -> List[MunsellPoint]:
        """Load XKCD colors matching an overlay name from munsell_conversions.json."""
        munsell_file = self.investigation_dir / "munsell_conversions.json"
        if not munsell_file.exists():
            return []

        with open(munsell_file, 'r') as f:
            data = json.load(f)

        colors = data.get('colors', {})
        pattern = re.compile(rf'\b{overlay_name}\b', re.IGNORECASE)

        points = []
        for name, color_data in colors.items():
            if pattern.search(name):
                munsell = color_data.get('munsell', {})
                hue_num = munsell.get('hue_num')
                value = munsell.get('value')
                chroma = munsell.get('chroma')
                if hue_num is not None and value is not None and chroma is not None:
                    points.append(MunsellPoint(hue_num, value, chroma, name))
        return points

    def load_all_overlays(self) -> Dict[str, Tuple[List[MunsellPoint], List[MunsellPoint]]]:
        """Load both datasets for all 20 Centore overlays."""
        result = {}
        for name in self.CENTORE_20:
            centore = self.load_centore_samples(name)
            xkcd = self.load_xkcd_matches(name)
            if centore and xkcd:
                result[name] = (centore, xkcd)
        return result


# =============================================================================
# Method 1: Sliced Wasserstein Distance with Hue Unfolding
# =============================================================================

class SlicedWassersteinMethod:
    """
    Sliced Wasserstein Distance for comparing point cloud distributions.
    Uses hue unfolding to handle circular nature of hue dimension.
    """

    def __init__(self, n_projections: int = 100):
        self.n_projections = n_projections

    def unfold_hue(self, points: np.ndarray) -> np.ndarray:
        """
        Unfold hue dimension to handle circularity.
        Each point is replicated at hue, hue-360, and hue+360.
        Input: (N, 3) array of (hue, value, chroma)
        Output: (3N, 3) array with unfolded hue
        """
        n = len(points)
        unfolded = np.zeros((3 * n, 3))

        for i, (h, v, c) in enumerate(points):
            unfolded[i] = [h - 360, v, c]       # left copy
            unfolded[n + i] = [h, v, c]          # original
            unfolded[2*n + i] = [h + 360, v, c]  # right copy

        return unfolded

    def sliced_wasserstein_1d(self, x: np.ndarray, y: np.ndarray) -> float:
        """Compute 1D Wasserstein distance."""
        x_sorted = np.sort(x)
        y_sorted = np.sort(y)

        # Interpolate to same size if needed
        n = max(len(x), len(y))
        x_interp = np.interp(np.linspace(0, 1, n), np.linspace(0, 1, len(x)), x_sorted)
        y_interp = np.interp(np.linspace(0, 1, n), np.linspace(0, 1, len(y)), y_sorted)

        return np.mean(np.abs(x_interp - y_interp))

    def compute_swd(self, points1: np.ndarray, points2: np.ndarray) -> float:
        """Compute Sliced Wasserstein Distance between two point clouds."""
        distances = []

        for _ in range(self.n_projections):
            # Random projection direction
            direction = np.random.randn(3)
            direction /= np.linalg.norm(direction)

            # Project points
            proj1 = points1 @ direction
            proj2 = points2 @ direction

            # 1D Wasserstein
            distances.append(self.sliced_wasserstein_1d(proj1, proj2))

        return np.mean(distances)

    def permutation_test(self, centore: List[MunsellPoint], xkcd: List[MunsellPoint],
                         n_permutations: int = 1000) -> Tuple[float, float, float]:
        """
        Perform permutation test for null hypothesis.
        H0: Both samples come from the same distribution.

        Returns: (observed_swd, p_value, effect_size)
        """
        # Convert to cylindrical arrays
        c_cyl = np.array([p.to_cylindrical() for p in centore])
        x_cyl = np.array([p.to_cylindrical() for p in xkcd])

        # Unfold hue for circular handling
        c_unfolded = self.unfold_hue(c_cyl)
        x_unfolded = self.unfold_hue(x_cyl)

        # Observed distance
        observed_swd = self.compute_swd(c_unfolded, x_unfolded)

        # Permutation test
        combined = np.vstack([c_cyl, x_cyl])
        n_centore = len(c_cyl)

        null_distribution = []
        for _ in range(n_permutations):
            np.random.shuffle(combined)
            perm_c = combined[:n_centore]
            perm_x = combined[n_centore:]

            perm_c_unfolded = self.unfold_hue(perm_c)
            perm_x_unfolded = self.unfold_hue(perm_x)

            null_distribution.append(self.compute_swd(perm_c_unfolded, perm_x_unfolded))

        null_distribution = np.array(null_distribution)
        p_value = np.mean(null_distribution >= observed_swd)

        # Effect size: how many std deviations above null mean
        null_mean = np.mean(null_distribution)
        null_std = np.std(null_distribution)
        effect_size = (observed_swd - null_mean) / null_std if null_std > 0 else 0

        return observed_swd, p_value, effect_size

    def compute_shift_vector(self, centore: List[MunsellPoint], xkcd: List[MunsellPoint]) -> Dict:
        """Compute the average shift from XKCD to Centore centroids."""
        c_cyl = np.array([p.to_cylindrical() for p in centore])
        x_cyl = np.array([p.to_cylindrical() for p in xkcd])

        c_mean = np.mean(c_cyl, axis=0)
        x_mean = np.mean(x_cyl, axis=0)

        # Handle hue circularity for mean shift
        hue_diff = c_mean[0] - x_mean[0]
        if hue_diff > 180:
            hue_diff -= 360
        elif hue_diff < -180:
            hue_diff += 360

        return {
            'hue_shift': hue_diff,
            'value_shift': c_mean[1] - x_mean[1],
            'chroma_shift': c_mean[2] - x_mean[2],
            'centore_centroid': {'hue': c_mean[0], 'value': c_mean[1], 'chroma': c_mean[2]},
            'xkcd_centroid': {'hue': x_mean[0], 'value': x_mean[1], 'chroma': x_mean[2]}
        }


# =============================================================================
# Method 2: Circular Statistics (von Mises) for Hue
# =============================================================================

class CircularStatisticsMethod:
    """
    Circular statistics for comparing hue distributions.
    Uses von Mises distribution modeling and Watson's U² test.
    """

    def circular_mean(self, angles_deg: np.ndarray) -> float:
        """Compute circular mean of angles in degrees."""
        angles_rad = np.deg2rad(angles_deg)
        sin_mean = np.mean(np.sin(angles_rad))
        cos_mean = np.mean(np.cos(angles_rad))
        return np.rad2deg(np.arctan2(sin_mean, cos_mean)) % 360

    def circular_std(self, angles_deg: np.ndarray) -> float:
        """Compute circular standard deviation."""
        angles_rad = np.deg2rad(angles_deg)
        R = np.sqrt(np.mean(np.cos(angles_rad))**2 + np.mean(np.sin(angles_rad))**2)
        return np.rad2deg(np.sqrt(-2 * np.log(R))) if R > 0 else 180

    def mean_resultant_length(self, angles_deg: np.ndarray) -> float:
        """Compute mean resultant length (concentration measure)."""
        angles_rad = np.deg2rad(angles_deg)
        return np.sqrt(np.mean(np.cos(angles_rad))**2 + np.mean(np.sin(angles_rad))**2)

    def watson_u2_test(self, sample1: np.ndarray, sample2: np.ndarray) -> Tuple[float, float]:
        """
        Watson's U² two-sample test for circular data.
        H0: Both samples come from the same circular distribution.

        Returns: (U² statistic, approximate p-value)
        """
        # Convert to radians and sort
        s1 = np.sort(np.deg2rad(sample1) % (2 * np.pi))
        s2 = np.sort(np.deg2rad(sample2) % (2 * np.pi))

        n1, n2 = len(s1), len(s2)
        n = n1 + n2

        # Combine and compute ranks
        combined = np.concatenate([s1, s2])
        labels = np.concatenate([np.ones(n1), np.zeros(n2)])
        order = np.argsort(combined)

        # Compute cumulative distribution differences
        d1 = np.zeros(n)
        d2 = np.zeros(n)

        c1, c2 = 0, 0
        for i, idx in enumerate(order):
            if labels[idx] == 1:
                c1 += 1
            else:
                c2 += 1
            d1[i] = c1 / n1
            d2[i] = c2 / n2

        dk = d1 - d2
        d_bar = np.mean(dk)

        # U² statistic
        u2 = (n1 * n2 / n**2) * np.sum((dk - d_bar)**2)

        # Approximate p-value using asymptotic distribution
        # Critical values: 0.05 -> 0.152, 0.01 -> 0.187
        if u2 > 0.187:
            p_value = 0.005
        elif u2 > 0.152:
            p_value = 0.025
        elif u2 > 0.119:
            p_value = 0.05
        elif u2 > 0.092:
            p_value = 0.10
        else:
            p_value = 0.20

        return u2, p_value

    def analyze(self, centore: List[MunsellPoint], xkcd: List[MunsellPoint]) -> Dict:
        """
        Perform circular statistics analysis on hue dimension.
        Also analyzes value and chroma using standard statistics.
        """
        c_hue = np.array([p.hue_num for p in centore])
        x_hue = np.array([p.hue_num for p in xkcd])

        c_val = np.array([p.value for p in centore])
        x_val = np.array([p.value for p in xkcd])

        c_chr = np.array([p.chroma for p in centore])
        x_chr = np.array([p.chroma for p in xkcd])

        # Hue analysis (circular)
        c_hue_mean = self.circular_mean(c_hue)
        x_hue_mean = self.circular_mean(x_hue)

        hue_diff = x_hue_mean - c_hue_mean
        if hue_diff > 180:
            hue_diff -= 360
        elif hue_diff < -180:
            hue_diff += 360

        u2_stat, hue_p_value = self.watson_u2_test(c_hue, x_hue)

        # Value analysis (linear) - use Mann-Whitney U test
        if SCIPY_AVAILABLE:
            val_stat, val_p_value = stats.mannwhitneyu(c_val, x_val, alternative='two-sided')
            chr_stat, chr_p_value = stats.mannwhitneyu(c_chr, x_chr, alternative='two-sided')
        else:
            val_stat, val_p_value = 0, 1.0
            chr_stat, chr_p_value = 0, 1.0

        return {
            'hue': {
                'centore_mean': c_hue_mean,
                'xkcd_mean': x_hue_mean,
                'shift': hue_diff,
                'centore_concentration': self.mean_resultant_length(c_hue),
                'xkcd_concentration': self.mean_resultant_length(x_hue),
                'watson_u2': u2_stat,
                'p_value': hue_p_value,
                'significant': hue_p_value < 0.05
            },
            'value': {
                'centore_mean': np.mean(c_val),
                'xkcd_mean': np.mean(x_val),
                'shift': np.mean(x_val) - np.mean(c_val),
                'p_value': val_p_value,
                'significant': val_p_value < 0.05
            },
            'chroma': {
                'centore_mean': np.mean(c_chr),
                'xkcd_mean': np.mean(x_chr),
                'shift': np.mean(x_chr) - np.mean(c_chr),
                'p_value': chr_p_value,
                'significant': chr_p_value < 0.05
            }
        }


# =============================================================================
# Method 3: Procrustes Analysis
# =============================================================================

class ProcrustesMethod:
    """
    Procrustes analysis for comparing point cloud shapes.
    Finds optimal rigid transformation to align XKCD to Centore.
    """

    def analyze(self, centore: List[MunsellPoint], xkcd: List[MunsellPoint],
                n_permutations: int = 1000) -> Dict:
        """
        Perform Procrustes analysis and PROTEST permutation test.
        H0: The point clouds have the same shape (no systematic transformation needed).
        """
        if not SCIPY_AVAILABLE:
            return {'error': 'scipy not available'}

        # Convert to Cartesian for Procrustes (works in Euclidean space)
        c_cart = np.array([p.to_cartesian() for p in centore])
        x_cart = np.array([p.to_cartesian() for p in xkcd])

        # Subsample to same size (Procrustes requires matching point counts)
        min_n = min(len(c_cart), len(x_cart))

        # Random subsample for comparison
        np.random.seed(42)
        c_idx = np.random.choice(len(c_cart), min_n, replace=False)
        x_idx = np.random.choice(len(x_cart), min_n, replace=False)

        c_sub = c_cart[c_idx]
        x_sub = x_cart[x_idx]

        # Procrustes analysis
        mtx1, mtx2, disparity = procrustes(c_sub, x_sub)

        # PROTEST: permutation test for Procrustes disparity
        observed_disparity = disparity

        null_distribution = []
        for _ in range(n_permutations):
            perm_idx = np.random.permutation(min_n)
            _, _, perm_disparity = procrustes(c_sub, x_sub[perm_idx])
            null_distribution.append(perm_disparity)

        null_distribution = np.array(null_distribution)
        p_value = np.mean(null_distribution <= observed_disparity)

        # Compute transformation statistics
        # Centroid shift
        c_centroid = np.mean(c_cart, axis=0)
        x_centroid = np.mean(x_cart, axis=0)
        translation = x_centroid - c_centroid

        return {
            'procrustes_disparity': observed_disparity,
            'p_value': p_value,
            'significant': p_value < 0.05,
            'translation': {
                'x': translation[0],
                'y': translation[1],
                'z': translation[2]
            },
            'centore_centroid': {'x': c_centroid[0], 'y': c_centroid[1], 'z': c_centroid[2]},
            'xkcd_centroid': {'x': x_centroid[0], 'y': x_centroid[1], 'z': x_centroid[2]},
            'null_mean': np.mean(null_distribution),
            'null_std': np.std(null_distribution)
        }


# =============================================================================
# Method 4: GMM + KL Divergence
# =============================================================================

class GMMKLMethod:
    """
    Gaussian Mixture Model fitting with KL divergence comparison.
    Models each distribution as a GMM and compares using Monte Carlo KL estimate.
    """

    def __init__(self, n_components: int = 3):
        self.n_components = n_components

    def fit_gmm(self, points: np.ndarray) -> Optional['GaussianMixture']:
        """Fit GMM to point cloud."""
        if not SKLEARN_AVAILABLE:
            return None

        n_comp = min(self.n_components, len(points) // 5)  # Need enough points
        if n_comp < 1:
            n_comp = 1

        gmm = GaussianMixture(n_components=n_comp, covariance_type='full', random_state=42)
        gmm.fit(points)
        return gmm

    def monte_carlo_kl(self, gmm1: 'GaussianMixture', gmm2: 'GaussianMixture',
                       n_samples: int = 10000) -> float:
        """Estimate KL divergence using Monte Carlo sampling."""
        samples = gmm1.sample(n_samples)[0]

        log_p = gmm1.score_samples(samples)
        log_q = gmm2.score_samples(samples)

        kl = np.mean(log_p - log_q)
        return max(0, kl)  # KL should be non-negative

    def symmetric_kl(self, gmm1: 'GaussianMixture', gmm2: 'GaussianMixture') -> float:
        """Compute symmetric KL divergence."""
        kl_pq = self.monte_carlo_kl(gmm1, gmm2)
        kl_qp = self.monte_carlo_kl(gmm2, gmm1)
        return (kl_pq + kl_qp) / 2

    def analyze(self, centore: List[MunsellPoint], xkcd: List[MunsellPoint],
                n_bootstrap: int = 100) -> Dict:
        """
        Fit GMMs and compare using KL divergence with bootstrap p-value.
        H0: The KL divergence is not significantly different from zero.
        """
        if not SKLEARN_AVAILABLE:
            return {'error': 'sklearn not available'}

        # Convert to Cartesian
        c_cart = np.array([p.to_cartesian() for p in centore])
        x_cart = np.array([p.to_cartesian() for p in xkcd])

        # Fit GMMs
        gmm_c = self.fit_gmm(c_cart)
        gmm_x = self.fit_gmm(x_cart)

        if gmm_c is None or gmm_x is None:
            return {'error': 'GMM fitting failed'}

        # Observed symmetric KL
        observed_kl = self.symmetric_kl(gmm_c, gmm_x)

        # Bootstrap for confidence interval
        combined = np.vstack([c_cart, x_cart])
        n_c = len(c_cart)

        bootstrap_kls = []
        for _ in range(n_bootstrap):
            # Resample from each distribution
            idx_c = np.random.choice(n_c, n_c, replace=True)
            idx_x = np.random.choice(len(x_cart), len(x_cart), replace=True)

            boot_c = c_cart[idx_c]
            boot_x = x_cart[idx_x]

            boot_gmm_c = self.fit_gmm(boot_c)
            boot_gmm_x = self.fit_gmm(boot_x)

            if boot_gmm_c and boot_gmm_x:
                bootstrap_kls.append(self.symmetric_kl(boot_gmm_c, boot_gmm_x))

        bootstrap_kls = np.array(bootstrap_kls)
        ci_lower = np.percentile(bootstrap_kls, 2.5)
        ci_upper = np.percentile(bootstrap_kls, 97.5)

        # P-value: probability of seeing KL <= 0 under bootstrap
        # (if CI doesn't include 0, it's significant)
        p_value = np.mean(bootstrap_kls <= 0) if len(bootstrap_kls) > 0 else 1.0

        return {
            'symmetric_kl': observed_kl,
            'ci_95_lower': ci_lower,
            'ci_95_upper': ci_upper,
            'p_value': p_value,
            'significant': ci_lower > 0.1,  # KL > 0.1 is meaningful difference
            'n_components_centore': gmm_c.n_components,
            'n_components_xkcd': gmm_x.n_components
        }


# =============================================================================
# Main Analysis Runner
# =============================================================================

def run_all_methods(overlay_name: str, centore: List[MunsellPoint],
                    xkcd: List[MunsellPoint]) -> Dict:
    """Run all four methods on a single overlay."""
    print(f"\n{'='*60}")
    print(f"Analyzing overlay: {overlay_name}")
    print(f"Centore samples: {len(centore)}, XKCD samples: {len(xkcd)}")
    print('='*60)

    results = {
        'overlay': overlay_name,
        'n_centore': len(centore),
        'n_xkcd': len(xkcd)
    }

    # Method 1: Sliced Wasserstein
    print("\n[1] Sliced Wasserstein Distance (with hue unfolding)...")
    swd = SlicedWassersteinMethod(n_projections=50)
    observed, p_val, effect = swd.permutation_test(centore, xkcd, n_permutations=500)
    shift = swd.compute_shift_vector(centore, xkcd)

    results['sliced_wasserstein'] = {
        'distance': observed,
        'p_value': p_val,
        'effect_size': effect,
        'significant': p_val < 0.05,
        'shift': shift
    }
    print(f"   SWD = {observed:.4f}, p = {p_val:.4f}, effect = {effect:.2f}")
    print(f"   Shift: hue={shift['hue_shift']:.1f}°, value={shift['value_shift']:.2f}, chroma={shift['chroma_shift']:.2f}")

    # Method 2: Circular Statistics
    print("\n[2] Circular Statistics (von Mises/Watson)...")
    circ = CircularStatisticsMethod()
    circ_result = circ.analyze(centore, xkcd)
    results['circular_statistics'] = circ_result

    print(f"   Hue: shift={circ_result['hue']['shift']:.1f}°, U²={circ_result['hue']['watson_u2']:.4f}, p={circ_result['hue']['p_value']:.3f}")
    print(f"   Value: shift={circ_result['value']['shift']:.2f}, p={circ_result['value']['p_value']:.4f}")
    print(f"   Chroma: shift={circ_result['chroma']['shift']:.2f}, p={circ_result['chroma']['p_value']:.4f}")

    # Method 3: Procrustes
    print("\n[3] Procrustes Analysis...")
    proc = ProcrustesMethod()
    proc_result = proc.analyze(centore, xkcd, n_permutations=500)
    results['procrustes'] = proc_result

    if 'error' not in proc_result:
        print(f"   Disparity = {proc_result['procrustes_disparity']:.4f}, p = {proc_result['p_value']:.4f}")
        trans = proc_result['translation']
        print(f"   Translation: x={trans['x']:.2f}, y={trans['y']:.2f}, z={trans['z']:.2f}")
    else:
        print(f"   Error: {proc_result['error']}")

    # Method 4: GMM + KL
    print("\n[4] GMM + KL Divergence...")
    gmm = GMMKLMethod(n_components=2)
    gmm_result = gmm.analyze(centore, xkcd, n_bootstrap=100)
    results['gmm_kl'] = gmm_result

    if 'error' not in gmm_result:
        print(f"   Symmetric KL = {gmm_result['symmetric_kl']:.4f}")
        print(f"   95% CI: [{gmm_result['ci_95_lower']:.4f}, {gmm_result['ci_95_upper']:.4f}]")
    else:
        print(f"   Error: {gmm_result['error']}")

    return results


def main():
    """Run analysis on all 20 Centore overlays."""
    print("="*70)
    print("Distribution Comparison Methods for Screen-to-Physical Color Bias")
    print("="*70)

    loader = DataLoader()
    overlays = loader.load_all_overlays()

    print(f"\nLoaded {len(overlays)} overlays with both Centore and XKCD data")

    all_results = {}
    summary = {
        'swd_significant': 0,
        'hue_significant': 0,
        'value_significant': 0,
        'chroma_significant': 0,
        'procrustes_significant': 0,
        'total_overlays': 0
    }

    for name, (centore, xkcd) in overlays.items():
        if len(centore) < 10 or len(xkcd) < 10:
            print(f"\nSkipping {name}: insufficient samples (Centore={len(centore)}, XKCD={len(xkcd)})")
            continue

        results = run_all_methods(name, centore, xkcd)
        all_results[name] = results

        summary['total_overlays'] += 1
        if results['sliced_wasserstein']['significant']:
            summary['swd_significant'] += 1
        if results['circular_statistics']['hue']['significant']:
            summary['hue_significant'] += 1
        if results['circular_statistics']['value']['significant']:
            summary['value_significant'] += 1
        if results['circular_statistics']['chroma']['significant']:
            summary['chroma_significant'] += 1
        if 'error' not in results['procrustes'] and results['procrustes']['significant']:
            summary['procrustes_significant'] += 1

    # Print summary
    print("\n" + "="*70)
    print("SUMMARY OF STATISTICAL TESTS")
    print("="*70)
    print(f"\nTotal overlays analyzed: {summary['total_overlays']}")
    print(f"\nSignificant differences (p < 0.05):")
    print(f"  - Sliced Wasserstein: {summary['swd_significant']}/{summary['total_overlays']}")
    print(f"  - Hue (Watson U²):    {summary['hue_significant']}/{summary['total_overlays']}")
    print(f"  - Value (Mann-Whitney): {summary['value_significant']}/{summary['total_overlays']}")
    print(f"  - Chroma (Mann-Whitney): {summary['chroma_significant']}/{summary['total_overlays']}")
    print(f"  - Procrustes:         {summary['procrustes_significant']}/{summary['total_overlays']}")

    # Aggregate bias analysis
    print("\n" + "="*70)
    print("AGGREGATE BIAS ANALYSIS")
    print("="*70)

    hue_shifts = []
    value_shifts = []
    chroma_shifts = []

    for name, results in all_results.items():
        shift = results['sliced_wasserstein']['shift']
        hue_shifts.append(shift['hue_shift'])
        value_shifts.append(shift['value_shift'])
        chroma_shifts.append(shift['chroma_shift'])

    print(f"\nHue shift (XKCD → Centore):")
    print(f"  Mean: {np.mean(hue_shifts):.2f}°, Std: {np.std(hue_shifts):.2f}°")
    print(f"  Range: [{min(hue_shifts):.2f}°, {max(hue_shifts):.2f}°]")

    print(f"\nValue shift (XKCD → Centore):")
    print(f"  Mean: {np.mean(value_shifts):.2f}, Std: {np.std(value_shifts):.2f}")

    print(f"\nChroma shift (XKCD → Centore):")
    print(f"  Mean: {np.mean(chroma_shifts):.2f}, Std: {np.std(chroma_shifts):.2f}")

    # Save results
    output_file = Path(__file__).parent / "distribution_comparison_results.json"

    def convert_for_json(obj):
        """Recursively convert numpy types and handle nested dicts."""
        if isinstance(obj, dict):
            return {k: convert_for_json(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_for_json(item) for item in obj]
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.float32, np.float64, np.floating)):
            return float(obj)
        elif isinstance(obj, (np.int32, np.int64, np.integer)):
            return int(obj)
        elif isinstance(obj, (np.bool_, bool)):
            return bool(obj)
        else:
            return obj

    output_data = {
        'summary': convert_for_json(summary),
        'overlays': convert_for_json(all_results)
    }

    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)

    print(f"\n\nResults saved to: {output_file}")

    return all_results, summary


if __name__ == "__main__":
    main()
