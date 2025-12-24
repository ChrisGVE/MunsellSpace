#!/usr/bin/env python3
"""
Robust Color Name Processing Pipeline

Based on semantic investigation findings, this pipeline:
1. Preprocesses names (strips noise, decodes hex)
2. Filters using SBERT semantic similarity
3. Groups similar names for consolidation

Usage:
    pipeline = ColorNamePipeline()
    result = pipeline.process("fedex purple")
    # Returns: {'valid': True, 'cleaned': 'fedex purple', 'similarity': 0.594, ...}
"""

import re
import json
from pathlib import Path
from typing import Optional, Dict, List, Tuple
import numpy as np


class ColorNamePipeline:
    """
    Pipeline for validating and processing color names.

    Uses SBERT semantic similarity to determine if a name
    has color meaning, without making incorrect string-matching
    assumptions.
    """

    # Similarity threshold - names below this are filtered
    SIMILARITY_THRESHOLD = 0.35

    # Minimum sample count for XKCD quality filtering
    MIN_SAMPLE_COUNT = 10

    # Maximum words for a valid color name (filters sentences)
    MAX_WORDS = 6

    def __init__(self, load_model: bool = True):
        """
        Initialize the pipeline.

        Args:
            load_model: If True, loads SBERT model (slower but enables
                        similarity computation). If False, uses cached
                        results only.
        """
        self.model = None
        self.vocab = None
        self.vocab_embeddings = None
        self._cached_similarities = None

        if load_model:
            self._load_model()
        else:
            self._load_cached_similarities()

    def _load_model(self):
        """Load SBERT model and color vocabulary."""
        try:
            from sentence_transformers import SentenceTransformer
            print("Loading SBERT model...")
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            self._build_vocabulary()
            print("Model loaded successfully")
        except ImportError:
            print("Warning: sentence-transformers not available, using cached results")
            self._load_cached_similarities()

    def _build_vocabulary(self):
        """Build color vocabulary for similarity comparison."""
        from common import BASIC_COLORS

        vocab = set()
        vocab.update(BASIC_COLORS)

        # Add modified colors
        for modifier in ['light', 'dark', 'bright', 'pale', 'deep', 'vivid',
                         'soft', 'muted', 'dusty', 'pastel']:
            for color in list(BASIC_COLORS)[:20]:
                vocab.add(f"{modifier} {color}")

        # Add compound colors
        for c1 in ['blue', 'green', 'red', 'yellow', 'purple', 'orange']:
            for c2 in ['blue', 'green', 'red', 'yellow', 'purple', 'orange']:
                if c1 != c2:
                    vocab.add(f"{c1}ish {c2}")
                    vocab.add(f"{c1} {c2}")

        self.vocab = sorted(vocab)
        self.vocab_embeddings = self.model.encode(self.vocab)

    def _load_cached_similarities(self):
        """Load pre-computed similarities from experiment results."""
        cache_path = Path(__file__).parent / "exp1_sbert_full_results.json"
        if cache_path.exists():
            with open(cache_path) as f:
                data = json.load(f)
                self._cached_similarities = data.get('all_similarities', {})
            print(f"Loaded {len(self._cached_similarities):,} cached similarities")

    def preprocess(self, name: str) -> Tuple[str, Dict]:
        """
        Preprocess a color name.

        Returns:
            Tuple of (cleaned_name, preprocessing_info)
        """
        original = name
        info = {'original': original, 'steps': []}

        # Step 1: Handle hex codes
        hex_match = re.match(r'^#?([0-9a-fA-F]{6})$', name.strip())
        if hex_match:
            rgb = self._hex_to_rgb(hex_match.group(1))
            color_name = self._rgb_to_color_name(rgb)
            info['steps'].append(f'hex:{name}→{color_name}')
            return color_name, info

        # Step 2: Lowercase
        name = name.lower()
        if name != original.lower():
            info['steps'].append('lowercase')

        # Step 3: Strip leading/trailing noise
        stripped = re.sub(r'^[^\w\s]+', '', name)
        stripped = re.sub(r'[^\w\s]+$', '', stripped)
        if stripped != name:
            info['steps'].append(f'strip_noise:{name}→{stripped}')
            name = stripped

        # Step 4: Normalize whitespace
        normalized = re.sub(r'\s+', ' ', name).strip()
        if normalized != name:
            info['steps'].append('normalize_ws')
            name = normalized

        # Step 5: Normalize quotes
        name = re.sub(r"[''`]", "'", name)

        return name, info

    def _hex_to_rgb(self, hex_str: str) -> Tuple[int, int, int]:
        """Convert hex string to RGB tuple."""
        return (
            int(hex_str[0:2], 16),
            int(hex_str[2:4], 16),
            int(hex_str[4:6], 16)
        )

    def _rgb_to_color_name(self, rgb: Tuple[int, int, int]) -> str:
        """Convert RGB to approximate color name."""
        r, g, b = rgb

        # Simple heuristic based on dominant channel
        if r > 200 and g < 100 and b < 100:
            return "red"
        elif r < 100 and g > 200 and b < 100:
            return "green"
        elif r < 100 and g < 100 and b > 200:
            return "blue"
        elif r > 200 and g > 200 and b < 100:
            return "yellow"
        elif r > 200 and g < 100 and b > 200:
            return "magenta"
        elif r < 100 and g > 200 and b > 200:
            return "cyan"
        elif r > 200 and g > 200 and b > 200:
            return "white"
        elif r < 50 and g < 50 and b < 50:
            return "black"
        elif abs(r - g) < 30 and abs(g - b) < 30:
            return "light gray" if r > 150 else "dark gray"
        elif r > g and r > b:
            return "orange" if g > b else "pink"
        elif g > r and g > b:
            return "green"
        elif b > r and b > g:
            return "purple" if r > g else "blue"
        else:
            return "gray"

    def compute_similarity(self, name: str) -> Tuple[float, str]:
        """
        Compute semantic similarity to color vocabulary.

        Returns:
            Tuple of (similarity_score, best_matching_color)
        """
        # Check cache first
        if self._cached_similarities and name.lower() in self._cached_similarities:
            cached = self._cached_similarities[name.lower()]
            return cached['similarity'], cached['best_match']

        # Compute if model available
        if self.model is not None:
            from sklearn.metrics.pairwise import cosine_similarity
            embedding = self.model.encode([name])
            sims = cosine_similarity(embedding, self.vocab_embeddings)[0]
            best_idx = np.argmax(sims)
            return float(sims[best_idx]), self.vocab[best_idx]

        # No way to compute
        return 0.0, "unknown"

    def is_valid_color_name(self, name: str) -> Tuple[bool, Dict]:
        """
        Determine if a name is a valid color name.

        Returns:
            Tuple of (is_valid, validation_info)
        """
        info = {'checks': []}

        # Check 1: Not too long (filters sentences)
        word_count = len(name.split())
        if word_count > self.MAX_WORDS:
            info['checks'].append(f'too_long:{word_count}_words')
            return False, info

        # Check 2: Not pure numbers
        if re.match(r'^[\d\s\-\.]+$', name):
            info['checks'].append('pure_numbers')
            return False, info

        # Check 3: Not pure punctuation
        if re.match(r'^[^\w\s]+$', name):
            info['checks'].append('pure_punctuation')
            return False, info

        # Check 4: Semantic similarity
        similarity, best_match = self.compute_similarity(name)
        info['similarity'] = similarity
        info['best_match'] = best_match

        if similarity < self.SIMILARITY_THRESHOLD:
            info['checks'].append(f'low_similarity:{similarity:.3f}')
            return False, info

        info['checks'].append('passed')
        return True, info

    def process(self, name: str, sample_count: int = None) -> Dict:
        """
        Process a color name through the full pipeline.

        Args:
            name: The color name to process
            sample_count: Optional sample count for quality filtering

        Returns:
            Dictionary with processing results
        """
        result = {
            'original': name,
            'valid': False,
            'cleaned': None,
            'similarity': 0.0,
            'best_match': None,
            'reason': None
        }

        # Preprocess
        cleaned, preprocess_info = self.preprocess(name)
        result['cleaned'] = cleaned
        result['preprocessing'] = preprocess_info

        # Validate
        is_valid, validation_info = self.is_valid_color_name(cleaned)
        result['valid'] = is_valid
        result['similarity'] = validation_info.get('similarity', 0.0)
        result['best_match'] = validation_info.get('best_match')

        if not is_valid:
            result['reason'] = validation_info['checks'][-1]
        elif sample_count is not None and sample_count < self.MIN_SAMPLE_COUNT:
            result['valid'] = False
            result['reason'] = f'low_sample_count:{sample_count}'

        return result

    def process_batch(self, names: List[str],
                      sample_counts: Dict[str, int] = None) -> List[Dict]:
        """Process multiple names."""
        results = []
        for name in names:
            count = sample_counts.get(name) if sample_counts else None
            results.append(self.process(name, count))
        return results


def main():
    """Demo the pipeline."""
    print("=" * 70)
    print("Color Name Pipeline Demo")
    print("=" * 70)

    # Test cases from the problematic mappings
    test_cases = [
        "!!! green",
        "!!! purple",
        "#0000FF",
        "#FF5733",
        "bluish fuchsia",
        "teal purple",
        "fedex purple",
        "warm lavender",
        "army grey",
        "this test is probably measuring how long people take",
        "asdfgh",
        "123456",
        "???",
        "light blue",
        "sky blue",
        "forest green",
    ]

    pipeline = ColorNamePipeline(load_model=False)  # Use cached for demo

    print("\nProcessing test cases:\n")
    for name in test_cases:
        result = pipeline.process(name)
        status = "VALID" if result['valid'] else "INVALID"
        print(f"'{name}'")
        print(f"  → cleaned: '{result['cleaned']}'")
        print(f"  → {status} (sim={result['similarity']:.3f}, match='{result['best_match']}')")
        if result['reason']:
            print(f"  → reason: {result['reason']}")
        print()


if __name__ == "__main__":
    main()
