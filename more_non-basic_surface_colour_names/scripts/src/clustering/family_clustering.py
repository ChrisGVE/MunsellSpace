#!/usr/bin/env python3
"""
Phase C: Multi-Method Family Clustering

Clusters color names into families using multiple methodologies:
1. K-means on RGB/Munsell coordinates (baseline)
2. DBSCAN on RGB/Munsell coordinates (density-based)
3. Gaussian Mixture Model (soft clustering)
4. SBERT semantic clustering (NLP-based)
5. Ensemble/consensus mechanism

Input: Consolidated color names with hex RGB values
Output: Color families with member colors and confidence scores

Reference:
    Pipeline architecture documented in writeups/methodology/pipeline.md
"""

import csv
import json
import math
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from collections import defaultdict
from dataclasses import dataclass, field
import numpy as np
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.neighbors import NearestNeighbors
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram
from scipy.spatial.distance import cdist, pdist


# Paths
SCRIPT_DIR = Path(__file__).parent
DATASETS_DIR = SCRIPT_DIR.parent.parent.parent / "datasets"
CONSOLIDATED_DIR = DATASETS_DIR / "consolidated"
OUTPUT_DIR = DATASETS_DIR / "clustered"


@dataclass
class ColorPoint:
    """A color with its coordinates and metadata."""
    name: str
    hex: str
    r: float
    g: float
    b: float
    source_count: int
    sources: str
    total_votes: int
    confidence: float

    # Munsell coordinates (computed later)
    munsell_hue: Optional[float] = None
    munsell_value: Optional[float] = None
    munsell_chroma: Optional[float] = None

    # Cartesian Munsell (for clustering)
    cart_x: Optional[float] = None
    cart_y: Optional[float] = None
    cart_z: Optional[float] = None

    # SBERT embedding (for semantic clustering)
    embedding: Optional[np.ndarray] = None

    @property
    def rgb_array(self) -> np.ndarray:
        return np.array([self.r, self.g, self.b])

    @property
    def munsell_array(self) -> Optional[np.ndarray]:
        if self.cart_x is None:
            return None
        return np.array([self.cart_x, self.cart_y, self.cart_z])


@dataclass
class ColorFamily:
    """A cluster of related colors forming a family."""
    id: int
    name: str  # Representative name
    members: List[str] = field(default_factory=list)
    centroid_rgb: Optional[np.ndarray] = None
    centroid_munsell: Optional[np.ndarray] = None
    method: str = "unknown"  # Which method discovered this family
    confidence: float = 0.0

    @property
    def size(self) -> int:
        return len(self.members)


class FamilyClustering:
    """Multi-method color family clustering."""

    def __init__(self, consolidated_path: Optional[Path] = None):
        self.consolidated_path = consolidated_path or (
            CONSOLIDATED_DIR / "color_names_consolidated.csv"
        )
        self.colors: Dict[str, ColorPoint] = {}
        self.families: Dict[str, List[ColorFamily]] = {}  # method -> families

        # Lazy-loaded SBERT model
        self._sbert_model = None

    def load_consolidated_data(self, limit: Optional[int] = None) -> int:
        """Load consolidated color names."""
        print(f"Loading consolidated data from {self.consolidated_path.name}...")

        count = 0
        with open(self.consolidated_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if limit and count >= limit:
                    break

                color = ColorPoint(
                    name=row['name'],
                    hex=row['hex'],
                    r=float(row['r']),
                    g=float(row['g']),
                    b=float(row['b']),
                    source_count=int(row['source_count']),
                    sources=row['sources'],
                    total_votes=int(row['total_votes']),
                    confidence=float(row['confidence'])
                )
                self.colors[color.name] = color
                count += 1

        print(f"  -> Loaded {count:,} colors")
        return count

    def convert_to_munsell(self, use_rust: bool = True) -> int:
        """Convert RGB colors to Munsell coordinates."""
        if not use_rust:
            print("Non-Rust Munsell conversion not implemented")
            return 0

        print("Converting RGB to Munsell via Rust converter...")

        # Find project root for Rust binary
        project_root = SCRIPT_DIR.parent.parent.parent.parent

        # Create temp input CSV
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.csv', delete=False, encoding='utf-8'
        ) as f:
            f.write("name,r,g,b\n")
            for name, color in self.colors.items():
                # Escape name if needed
                name_escaped = f'"{name}"' if ',' in name else name
                f.write(f"{name_escaped},{int(color.r)},{int(color.g)},{int(color.b)}\n")
            input_path = f.name

        # Create temp output file
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.csv', delete=False, encoding='utf-8'
        ) as f:
            output_path = f.name

        # Run Rust converter
        cmd = ['cargo', 'run', '--release', '--example', 'simple_rgb_to_munsell']

        try:
            with open(input_path, 'r') as stdin_file:
                with open(output_path, 'w') as stdout_file:
                    result = subprocess.run(
                        cmd,
                        stdin=stdin_file,
                        stdout=stdout_file,
                        stderr=subprocess.PIPE,
                        cwd=project_root,
                        text=True,
                        timeout=300
                    )

            if result.returncode != 0:
                print(f"  WARNING: Rust converter returned {result.returncode}")
                if result.stderr:
                    print(f"  stderr: {result.stderr[:500]}")
        except subprocess.TimeoutExpired:
            print("  ERROR: Rust converter timed out")
            return 0
        except FileNotFoundError:
            print("  ERROR: Cargo not found, skipping Munsell conversion")
            return 0

        # Parse output
        converted = 0
        with open(output_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row['name']
                if name not in self.colors:
                    continue

                color = self.colors[name]

                # Parse Munsell values
                color.munsell_hue = float(row['hue_num'])
                color.munsell_value = float(row['value'])
                color.munsell_chroma = float(row['chroma'])

                # Cartesian coordinates (already computed by Rust)
                color.cart_x = float(row['x'])
                color.cart_y = float(row['y'])
                color.cart_z = float(row['z'])

                converted += 1

        # Clean up temp files
        Path(input_path).unlink()
        Path(output_path).unlink()

        print(f"  -> Converted {converted:,} colors to Munsell")
        return converted

    def compute_sbert_embeddings(self, batch_size: int = 128) -> int:
        """Compute SBERT embeddings for all color names."""
        print("Computing SBERT embeddings...")

        if self._sbert_model is None:
            from sentence_transformers import SentenceTransformer
            self._sbert_model = SentenceTransformer('all-MiniLM-L6-v2')

        names = list(self.colors.keys())
        embeddings = self._sbert_model.encode(
            names,
            batch_size=batch_size,
            show_progress_bar=True,
            convert_to_numpy=True
        )

        for name, emb in zip(names, embeddings):
            self.colors[name].embedding = emb

        print(f"  -> Computed {len(names):,} embeddings")
        return len(names)

    # =========================================================================
    # Clustering Methods
    # =========================================================================

    def cluster_kmeans_rgb(
        self,
        n_clusters: int = 30,
        name: str = "kmeans_rgb"
    ) -> List[ColorFamily]:
        """K-means clustering on RGB coordinates."""
        print(f"Running K-means on RGB (k={n_clusters})...")

        # Prepare data
        names = list(self.colors.keys())
        X = np.array([self.colors[n].rgb_array for n in names])

        # Normalize
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Cluster
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X_scaled)

        # Build families
        families = self._build_families_from_labels(
            names, labels, X, method=name
        )

        self.families[name] = families
        print(f"  -> Created {len(families)} families")
        return families

    def cluster_kmeans_munsell(
        self,
        n_clusters: int = 30,
        name: str = "kmeans_munsell"
    ) -> List[ColorFamily]:
        """K-means clustering on Munsell Cartesian coordinates."""
        print(f"Running K-means on Munsell (k={n_clusters})...")

        # Filter to colors with Munsell coordinates
        names = [n for n in self.colors.keys()
                 if self.colors[n].munsell_array is not None]

        if len(names) < n_clusters:
            print(f"  WARNING: Only {len(names)} colors have Munsell coords")
            return []

        X = np.array([self.colors[n].munsell_array for n in names])

        # Normalize
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Cluster
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X_scaled)

        # Build families
        families = self._build_families_from_labels(
            names, labels, X, method=name
        )

        self.families[name] = families
        print(f"  -> Created {len(families)} families")
        return families

    def estimate_dbscan_eps(
        self,
        X_scaled: np.ndarray,
        min_samples: int = 5,
        percentile: float = 95.0
    ) -> float:
        """
        Estimate optimal eps for DBSCAN using k-distance graph method.

        Uses the elbow method on k-distance graph where k = min_samples.
        Returns the distance at the given percentile as a robust estimate.
        """
        # Compute k-nearest neighbor distances
        k = min(min_samples, len(X_scaled) - 1)
        nbrs = NearestNeighbors(n_neighbors=k + 1).fit(X_scaled)
        distances, _ = nbrs.kneighbors(X_scaled)

        # Get the k-th neighbor distance (excluding self)
        k_distances = np.sort(distances[:, k])

        # Use percentile for robust eps estimation
        # The elbow point is typically between 90-99th percentile
        eps = np.percentile(k_distances, percentile)

        return eps

    def cluster_dbscan_rgb(
        self,
        eps: Optional[float] = None,
        min_samples: int = 20,
        name: str = "dbscan_rgb",
        auto_eps_percentile: float = 92.0
    ) -> List[ColorFamily]:
        """DBSCAN clustering on RGB coordinates with auto eps estimation."""
        names = list(self.colors.keys())
        X = np.array([self.colors[n].rgb_array for n in names])

        # Normalize
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Auto-estimate eps if not provided
        if eps is None:
            eps = self.estimate_dbscan_eps(X_scaled, min_samples, auto_eps_percentile)
            print(f"Running DBSCAN on RGB (auto eps={eps:.4f}, min_samples={min_samples})...")
        else:
            print(f"Running DBSCAN on RGB (eps={eps}, min_samples={min_samples})...")

        # Cluster
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        labels = dbscan.fit_predict(X_scaled)

        # Filter out noise (-1 labels)
        n_noise = sum(1 for l in labels if l == -1)
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)

        print(f"  -> Found {n_clusters} clusters, {n_noise} noise points")

        # Build families
        families = self._build_families_from_labels(
            names, labels, X, method=name, exclude_noise=True
        )

        self.families[name] = families
        return families

    def cluster_dbscan_munsell(
        self,
        eps: Optional[float] = None,
        min_samples: int = 20,
        name: str = "dbscan_munsell",
        auto_eps_percentile: float = 92.0
    ) -> List[ColorFamily]:
        """DBSCAN clustering on Munsell coordinates with auto eps estimation."""
        # Filter to colors with Munsell coordinates
        names = [n for n in self.colors.keys()
                 if self.colors[n].munsell_array is not None]

        if len(names) < min_samples:
            print(f"  WARNING: Only {len(names)} colors have Munsell coords")
            return []

        X = np.array([self.colors[n].munsell_array for n in names])

        # Normalize
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Auto-estimate eps if not provided
        if eps is None:
            eps = self.estimate_dbscan_eps(X_scaled, min_samples, auto_eps_percentile)
            print(f"Running DBSCAN on Munsell (auto eps={eps:.4f}, min_samples={min_samples})...")
        else:
            print(f"Running DBSCAN on Munsell (eps={eps}, min_samples={min_samples})...")

        # Cluster
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        labels = dbscan.fit_predict(X_scaled)

        n_noise = sum(1 for l in labels if l == -1)
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)

        print(f"  -> Found {n_clusters} clusters, {n_noise} noise points")

        families = self._build_families_from_labels(
            names, labels, X, method=name, exclude_noise=True
        )

        self.families[name] = families
        return families

    def cluster_gmm_rgb(
        self,
        n_components: int = 30,
        name: str = "gmm_rgb"
    ) -> List[ColorFamily]:
        """Gaussian Mixture Model clustering on RGB."""
        print(f"Running GMM on RGB (n_components={n_components})...")

        names = list(self.colors.keys())
        X = np.array([self.colors[n].rgb_array for n in names])

        # Normalize
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Fit GMM
        gmm = GaussianMixture(
            n_components=n_components,
            random_state=42,
            covariance_type='full'
        )
        labels = gmm.fit_predict(X_scaled)

        # Build families
        families = self._build_families_from_labels(
            names, labels, X, method=name
        )

        self.families[name] = families
        print(f"  -> Created {len(families)} families")
        return families

    def cluster_sbert(
        self,
        n_clusters: int = 30,
        name: str = "sbert"
    ) -> List[ColorFamily]:
        """Cluster based on SBERT semantic embeddings."""
        print(f"Running K-means on SBERT embeddings (k={n_clusters})...")

        # Filter to colors with embeddings
        names = [n for n in self.colors.keys()
                 if self.colors[n].embedding is not None]

        if len(names) < n_clusters:
            print(f"  WARNING: Only {len(names)} colors have embeddings")
            return []

        X = np.array([self.colors[n].embedding for n in names])

        # Cluster (embeddings are already normalized by SBERT)
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X)

        # Build families (use RGB for centroid)
        rgb_data = np.array([self.colors[n].rgb_array for n in names])
        families = self._build_families_from_labels(
            names, labels, rgb_data, method=name
        )

        self.families[name] = families
        print(f"  -> Created {len(families)} families")
        return families

    def cluster_hierarchical_rgb(
        self,
        n_clusters: int = 30,
        linkage_method: str = "ward",
        name: str = "hierarchical_rgb"
    ) -> Tuple[List[ColorFamily], np.ndarray]:
        """
        Hierarchical/agglomerative clustering on RGB coordinates.

        Returns both families and linkage matrix for dendrogram visualization.
        """
        print(f"Running Hierarchical on RGB (k={n_clusters}, linkage={linkage_method})...")

        names = list(self.colors.keys())
        X = np.array([self.colors[n].rgb_array for n in names])

        # Normalize
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Compute linkage matrix (for dendrogram)
        Z = linkage(X_scaled, method=linkage_method)
        self._hierarchical_linkage = Z  # Store for later visualization

        # Cut dendrogram to get n_clusters
        labels = fcluster(Z, n_clusters, criterion='maxclust') - 1  # 0-indexed

        # Build families
        families = self._build_families_from_labels(
            names, labels, X, method=name
        )

        self.families[name] = families
        print(f"  -> Created {len(families)} families")

        return families, Z

    def get_family_distances(self, method: str = "kmeans_rgb") -> np.ndarray:
        """
        Compute pairwise distances between family centroids.

        Returns distance matrix for understanding family relationships.
        """
        if method not in self.families:
            raise ValueError(f"No families for method: {method}")

        families = self.families[method]
        centroids = []
        for family in families:
            if family.centroid_rgb is not None:
                centroids.append(family.centroid_rgb)
            else:
                # Compute centroid from members
                member_rgbs = [self.colors[m].rgb_array for m in family.members
                               if m in self.colors]
                if member_rgbs:
                    centroids.append(np.mean(member_rgbs, axis=0))

        if not centroids:
            return np.array([])

        centroids = np.array(centroids)
        distances = cdist(centroids, centroids, metric='euclidean')

        return distances

    def get_closest_families(
        self,
        method: str = "kmeans_rgb",
        top_n: int = 5
    ) -> List[Tuple[str, str, float]]:
        """
        Find the most similar pairs of families based on centroid distance.

        Returns list of (family1, family2, distance) tuples.
        """
        if method not in self.families:
            return []

        families = self.families[method]
        distances = self.get_family_distances(method)

        if len(distances) == 0:
            return []

        # Get upper triangle indices (exclude diagonal and duplicates)
        n = len(families)
        pairs = []
        for i in range(n):
            for j in range(i + 1, n):
                pairs.append((
                    families[i].name,
                    families[j].name,
                    float(distances[i, j])
                ))

        # Sort by distance (ascending)
        pairs.sort(key=lambda x: x[2])

        return pairs[:top_n]

    # =========================================================================
    # Helper Methods
    # =========================================================================

    def _build_families_from_labels(
        self,
        names: List[str],
        labels: np.ndarray,
        coordinates: np.ndarray,
        method: str,
        exclude_noise: bool = False
    ) -> List[ColorFamily]:
        """Build ColorFamily objects from clustering labels."""
        families = []

        label_to_names: Dict[int, List[Tuple[str, np.ndarray]]] = defaultdict(list)
        for name, label, coord in zip(names, labels, coordinates):
            if exclude_noise and label == -1:
                continue
            label_to_names[label].append((name, coord))

        for label, members in sorted(label_to_names.items()):
            if len(members) == 0:
                continue

            member_names = [m[0] for m in members]
            member_coords = np.array([m[1] for m in members])

            # Find representative: highest confidence color
            rep_name = max(
                member_names,
                key=lambda n: self.colors[n].confidence
            )

            # Compute centroid in clustering space
            centroid = np.mean(member_coords, axis=0)

            # Always compute RGB centroid from actual color data for display
            rgb_values = np.array([self.colors[n].rgb_array for n in member_names])
            rgb_centroid = np.mean(rgb_values, axis=0)

            family = ColorFamily(
                id=label,
                name=rep_name,
                members=member_names,
                centroid_rgb=rgb_centroid,
                method=method,
                confidence=np.mean([self.colors[n].confidence for n in member_names])
            )
            families.append(family)

        return families

    def find_optimal_k(
        self,
        method: str = "rgb",
        k_range: range = range(10, 50, 5)
    ) -> Tuple[int, Dict]:
        """Find optimal k using silhouette analysis."""
        print(f"Finding optimal k for {method} clustering...")

        if method == "rgb":
            names = list(self.colors.keys())
            X = np.array([self.colors[n].rgb_array for n in names])
        elif method == "munsell":
            names = [n for n in self.colors.keys()
                     if self.colors[n].munsell_array is not None]
            X = np.array([self.colors[n].munsell_array for n in names])
        elif method == "sbert":
            names = [n for n in self.colors.keys()
                     if self.colors[n].embedding is not None]
            X = np.array([self.colors[n].embedding for n in names])
        else:
            raise ValueError(f"Unknown method: {method}")

        # Normalize
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Sample for speed if dataset is large
        if len(X_scaled) > 10000:
            np.random.seed(42)
            indices = np.random.choice(len(X_scaled), 10000, replace=False)
            X_sample = X_scaled[indices]
        else:
            X_sample = X_scaled

        results = {}
        best_k = k_range.start
        best_score = -1

        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=5)
            labels = kmeans.fit_predict(X_sample)

            # Silhouette score
            score = silhouette_score(X_sample, labels)
            results[k] = {
                'silhouette': score,
                'inertia': kmeans.inertia_
            }

            if score > best_score:
                best_score = score
                best_k = k

            print(f"  k={k}: silhouette={score:.3f}, inertia={kmeans.inertia_:.1f}")

        print(f"  -> Best k={best_k} (silhouette={best_score:.3f})")
        return best_k, results

    # =========================================================================
    # Ensemble Methods
    # =========================================================================

    def build_consensus_families(
        self,
        methods: Optional[List[str]] = None,
        min_agreement: int = 2,
        use_strict: bool = True
    ) -> List[ColorFamily]:
        """
        Build consensus families from multiple clustering methods.

        When use_strict=True, uses voting to pick the best clustering rather than
        transitively merging all co-occurring pairs.
        """
        if methods is None:
            methods = [m for m in self.families.keys() if m != 'consensus']

        n_methods = len(methods)
        print(f"Building consensus from {n_methods} methods...")

        if n_methods == 0:
            print("  No methods to build consensus from")
            return []

        if use_strict:
            return self._build_consensus_voting(methods)
        else:
            return self._build_consensus_union_find(methods, min_agreement)

    def _build_consensus_voting(
        self,
        methods: List[str]
    ) -> List[ColorFamily]:
        """
        Build consensus by voting: use the clustering that best represents
        the consensus of all methods.

        For each pair of clusters (one from each method), compute overlap.
        Pick the clustering with highest average agreement with others.
        """
        # Get all families from all methods
        method_families = {m: self.families.get(m, []) for m in methods}

        # Score each method by how well its families agree with other methods
        method_scores = {}

        for method1 in methods:
            families1 = method_families[method1]
            if not families1:
                method_scores[method1] = 0.0
                continue

            # For each family in method1, find best matching family in other methods
            total_agreement = 0.0
            n_comparisons = 0

            for fam1 in families1:
                members1 = set(fam1.members)

                for method2 in methods:
                    if method2 == method1:
                        continue

                    families2 = method_families[method2]
                    if not families2:
                        continue

                    # Find best matching family in method2
                    best_overlap = 0.0
                    for fam2 in families2:
                        members2 = set(fam2.members)
                        intersection = len(members1 & members2)
                        union = len(members1 | members2)
                        if union > 0:
                            jaccard = intersection / union
                            best_overlap = max(best_overlap, jaccard)

                    total_agreement += best_overlap
                    n_comparisons += 1

            if n_comparisons > 0:
                method_scores[method1] = total_agreement / n_comparisons
            else:
                method_scores[method1] = 0.0

        # Pick the best method
        best_method = max(method_scores, key=lambda m: method_scores[m])
        best_score = method_scores[best_method]

        print(f"  Method scores: {method_scores}")
        print(f"  Best method: {best_method} (score={best_score:.3f})")

        # Use the best method's families as consensus, with adjusted confidence
        consensus_families = []
        for i, family in enumerate(self.families[best_method]):
            # Boost confidence by agreement score
            adjusted_confidence = family.confidence * (0.5 + 0.5 * best_score)

            consensus_family = ColorFamily(
                id=i,
                name=family.name,
                members=family.members.copy(),
                centroid_rgb=family.centroid_rgb.copy() if family.centroid_rgb is not None else None,
                method=f"consensus_{best_method}",
                confidence=adjusted_confidence
            )
            consensus_families.append(consensus_family)

        self.families["consensus"] = consensus_families
        print(f"  -> Created {len(consensus_families)} consensus families (from {best_method})")

        return consensus_families

    def _build_consensus_union_find(
        self,
        methods: List[str],
        min_agreement: int = 2
    ) -> List[ColorFamily]:
        """
        Original union-find based consensus (may create very large families).
        """
        # For each color, track which family it belongs to in each method
        color_family_map: Dict[str, Dict[str, int]] = defaultdict(dict)

        for method in methods:
            if method not in self.families:
                continue
            for family in self.families[method]:
                for member in family.members:
                    color_family_map[member][method] = family.id

        # Build co-occurrence matrix: how often do pairs cluster together?
        color_names = list(color_family_map.keys())
        n_colors = len(color_names)

        print(f"  Computing co-occurrence for {n_colors:,} colors...")

        # For efficiency, use sparse counting
        co_occurrence: Dict[Tuple[str, str], int] = defaultdict(int)

        for method in methods:
            if method not in self.families:
                continue
            for family in self.families[method]:
                members = family.members
                for i, m1 in enumerate(members):
                    for m2 in members[i+1:]:
                        key = tuple(sorted([m1, m2]))
                        co_occurrence[key] += 1

        # Cluster based on co-occurrence
        # Two colors are in same family if they co-occur in >= min_agreement methods

        # Union-Find for clustering
        parent = {name: name for name in color_names}

        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x, y):
            px, py = find(x), find(y)
            if px != py:
                parent[py] = px

        # Union colors that agree in multiple methods
        merged = 0
        for (c1, c2), count in co_occurrence.items():
            if count >= min_agreement:
                union(c1, c2)
                merged += 1

        print(f"  Merged {merged:,} color pairs")

        # Build families from clusters
        cluster_map: Dict[str, List[str]] = defaultdict(list)
        for name in color_names:
            root = find(name)
            cluster_map[root].append(name)

        # Convert to ColorFamily objects
        consensus_families = []
        for i, (root, members) in enumerate(sorted(
            cluster_map.items(),
            key=lambda x: -len(x[1])  # Largest first
        )):
            if len(members) < 2:
                continue  # Skip singletons

            # Representative: highest confidence
            rep_name = max(members, key=lambda n: self.colors[n].confidence)

            # Compute average RGB
            rgb_coords = np.array([self.colors[n].rgb_array for n in members])
            centroid = np.mean(rgb_coords, axis=0)

            # Confidence based on size and member confidence
            conf = np.mean([self.colors[n].confidence for n in members])

            family = ColorFamily(
                id=i,
                name=rep_name,
                members=members,
                centroid_rgb=centroid,
                method="consensus",
                confidence=conf
            )
            consensus_families.append(family)

        self.families["consensus"] = consensus_families
        print(f"  -> Created {len(consensus_families)} consensus families")

        return consensus_families

    # =========================================================================
    # Output Methods
    # =========================================================================

    def save_families(self, method: str, output_path: Optional[Path] = None):
        """Save families from a method to JSON."""
        if method not in self.families:
            print(f"No families for method: {method}")
            return

        if output_path is None:
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            output_path = OUTPUT_DIR / f"families_{method}.json"

        families = self.families[method]

        data = {
            'method': method,
            'n_families': len(families),
            'n_colors': sum(f.size for f in families),
            'families': []
        }

        for family in families:
            family_data = {
                'id': int(family.id),  # Ensure native int
                'name': family.name,
                'size': family.size,
                'confidence': round(float(family.confidence), 4),
                'members': family.members[:100],  # Limit for readability
                'total_members': family.size
            }
            if family.centroid_rgb is not None:
                family_data['centroid_rgb'] = [round(float(x), 1) for x in family.centroid_rgb]
                family_data['centroid_hex'] = '#{:02x}{:02x}{:02x}'.format(
                    int(family.centroid_rgb[0]),
                    int(family.centroid_rgb[1]),
                    int(family.centroid_rgb[2])
                )
            data['families'].append(family_data)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        print(f"Saved {len(families)} families to {output_path.name}")

    def print_family_summary(self, method: str, top_n: int = 20):
        """Print summary of families from a method."""
        if method not in self.families:
            print(f"No families for method: {method}")
            return

        families = sorted(
            self.families[method],
            key=lambda f: -f.size
        )

        print(f"\n{'='*60}")
        print(f"FAMILY SUMMARY: {method}")
        print(f"{'='*60}")
        print(f"Total families: {len(families)}")
        print(f"Total colors: {sum(f.size for f in families):,}")
        print(f"\nTop {top_n} families by size:")

        for i, family in enumerate(families[:top_n], 1):
            hex_str = ""
            if family.centroid_rgb is not None:
                hex_str = ' #{:02x}{:02x}{:02x}'.format(
                    int(family.centroid_rgb[0]),
                    int(family.centroid_rgb[1]),
                    int(family.centroid_rgb[2])
                )

            members_preview = ', '.join(family.members[:5])
            if len(family.members) > 5:
                members_preview += f", ... (+{len(family.members)-5} more)"

            print(f"{i:2}. {family.name:<25} {family.size:>5} members{hex_str}")
            print(f"    [{members_preview}]")


def main():
    """Run the full multi-method clustering pipeline."""
    import argparse

    parser = argparse.ArgumentParser(description="Multi-method color family clustering")
    parser.add_argument('--limit', type=int, default=None,
                       help='Limit number of colors to process')
    parser.add_argument('--k', type=int, default=30,
                       help='Number of clusters for K-means/GMM')
    parser.add_argument('--find-k', action='store_true',
                       help='Run silhouette analysis to find optimal k')
    parser.add_argument('--skip-munsell', action='store_true',
                       help='Skip Munsell conversion')
    parser.add_argument('--skip-sbert', action='store_true',
                       help='Skip SBERT embeddings')
    parser.add_argument('--methods', type=str, default='all',
                       help='Clustering methods to run (comma-separated)')
    args = parser.parse_args()

    print("=" * 60)
    print("PHASE C: MULTI-METHOD FAMILY CLUSTERING")
    print("=" * 60)
    print()

    # Initialize
    clustering = FamilyClustering()

    # Load data
    clustering.load_consolidated_data(limit=args.limit)

    # Convert to Munsell
    if not args.skip_munsell:
        clustering.convert_to_munsell()

    # Compute SBERT embeddings
    if not args.skip_sbert:
        clustering.compute_sbert_embeddings()

    # Find optimal k if requested
    if args.find_k:
        print("\n" + "-" * 40)
        k_rgb, _ = clustering.find_optimal_k("rgb", range(15, 50, 5))
        if not args.skip_sbert:
            k_sbert, _ = clustering.find_optimal_k("sbert", range(15, 50, 5))
        print("-" * 40)
    else:
        k_rgb = args.k

    # Run clustering methods
    methods = args.methods.split(',') if args.methods != 'all' else [
        'kmeans_rgb', 'kmeans_munsell', 'dbscan_rgb', 'gmm_rgb', 'sbert', 'hierarchical_rgb'
    ]

    print("\n" + "-" * 40)
    print("Running clustering methods...")
    print("-" * 40 + "\n")

    if 'kmeans_rgb' in methods:
        clustering.cluster_kmeans_rgb(n_clusters=k_rgb)

    if 'kmeans_munsell' in methods and not args.skip_munsell:
        clustering.cluster_kmeans_munsell(n_clusters=k_rgb)

    if 'dbscan_rgb' in methods:
        # Use lower percentile for densely packed color data
        # Note: DBSCAN finds density-based clusters - useful for outlier detection
        clustering.cluster_dbscan_rgb(eps=None, min_samples=10, auto_eps_percentile=30.0)

    if 'gmm_rgb' in methods:
        clustering.cluster_gmm_rgb(n_components=k_rgb)

    if 'sbert' in methods and not args.skip_sbert:
        clustering.cluster_sbert(n_clusters=k_rgb)

    if 'hierarchical_rgb' in methods:
        clustering.cluster_hierarchical_rgb(n_clusters=k_rgb)

    # Build consensus
    print("\n" + "-" * 40)
    clustering.build_consensus_families(min_agreement=2)
    print("-" * 40)

    # Show closest family pairs
    print("\n" + "-" * 40)
    print("Most similar family pairs (consensus):")
    closest = clustering.get_closest_families("consensus", top_n=10)
    for fam1, fam2, dist in closest:
        print(f"  {fam1} <-> {fam2}: {dist:.1f}")
    print("-" * 40)

    # Save results
    print("\n" + "-" * 40)
    print("Saving results...")
    print("-" * 40 + "\n")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for method in clustering.families.keys():
        clustering.save_families(method)
        clustering.print_family_summary(method, top_n=10)

    print("\n" + "=" * 60)
    print("CLUSTERING COMPLETE")
    print("=" * 60)
    print(f"Output directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
