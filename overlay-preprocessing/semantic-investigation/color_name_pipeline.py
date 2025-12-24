#!/usr/bin/env python3
"""
Robust Color Name Processing Pipeline

Based on semantic investigation findings, this pipeline:
1. Preprocesses names (strips noise, decodes hex)
2. Validates against master vocabulary (33K+ names from 6 sources)
3. Uses SBERT semantic similarity for unknown names
4. Groups similar names for consolidation

Usage:
    pipeline = ColorNamePipeline()
    result = pipeline.process("fedex purple")
    # Returns: {'valid': True, 'cleaned': 'fedex purple', 'similarity': 0.594, ...}
"""

import csv
import re
import json
from pathlib import Path
from typing import Optional, Dict, List, Tuple, Set
import numpy as np


class ColorNamePipeline:
    """
    Pipeline for validating and processing color names.

    Uses a two-tier validation approach:
    1. Direct lookup in master vocabulary (33K+ names from 6 authoritative sources)
    2. SBERT semantic similarity for names not in vocabulary
    """

    # Similarity threshold - names below this are filtered
    SIMILARITY_THRESHOLD = 0.35

    # Minimum sample count for XKCD quality filtering
    # Set to 0 to disable (semantic validation is sufficient)
    MIN_SAMPLE_COUNT = 0

    # Maximum words for a valid color name (filters sentences)
    MAX_WORDS = 6

    # Paths
    VOCAB_DIR = Path(__file__).parent.parent / "color-vocabularies"
    CACHE_DIR = Path(__file__).parent

    def __init__(self, load_model: bool = True, use_cache: bool = True):
        """
        Initialize the pipeline.

        Args:
            load_model: If True, loads SBERT model for similarity computation
            use_cache: If True, uses cached similarities when available
        """
        self.model = None
        self.master_vocab: Set[str] = set()
        self.core_vocab: List[str] = []
        self.core_embeddings = None
        self._cached_similarities = None

        # Load master vocabulary (always)
        self._load_master_vocabulary()

        # Load SBERT model or cache
        if load_model:
            self._load_model()
        elif use_cache:
            self._load_cached_similarities()

    def _load_master_vocabulary(self):
        """Load the master vocabulary from CSV."""
        vocab_path = self.VOCAB_DIR / "master_vocabulary.csv"

        if not vocab_path.exists():
            print(f"Warning: Master vocabulary not found at {vocab_path}")
            print("Run collect_vocabularies.py first")
            return

        with open(vocab_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                if row:
                    self.master_vocab.add(row[0].lower().strip())

        print(f"Loaded master vocabulary: {len(self.master_vocab):,} names")

    def _load_model(self):
        """Load SBERT model and build core vocabulary embeddings."""
        try:
            from sentence_transformers import SentenceTransformer
            print("Loading SBERT model...")
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            self._build_core_vocabulary()
            print("Model loaded successfully")
        except ImportError:
            print("Warning: sentence-transformers not available, using cached results")
            self._load_cached_similarities()

    def _build_core_vocabulary(self):
        """
        Build a core vocabulary for SBERT similarity.

        Uses a representative subset of ~2000 terms covering:
        - Basic color names
        - Modified colors (light/dark/etc.)
        - Compound colors
        - Common specific colors from sources
        """
        core = set()

        # Basic colors
        basic = {
            'red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'brown',
            'black', 'white', 'gray', 'grey', 'cyan', 'magenta', 'violet', 'indigo',
            'teal', 'turquoise', 'maroon', 'navy', 'olive', 'lime', 'aqua', 'coral',
            'salmon', 'crimson', 'scarlet', 'burgundy', 'fuchsia', 'lavender',
            'lilac', 'mauve', 'beige', 'tan', 'cream', 'ivory', 'gold', 'silver',
            'bronze', 'copper', 'rose', 'peach', 'apricot', 'amber', 'ochre',
            'sienna', 'umber', 'khaki', 'chartreuse', 'mint', 'sage', 'forest',
            'emerald', 'jade', 'azure', 'cobalt', 'cerulean', 'sapphire', 'plum',
            'grape', 'wine', 'rust', 'terracotta', 'taupe', 'charcoal', 'slate',
            'periwinkle', 'mocha', 'camel', 'mustard', 'mahogany', 'vermilion',
            'carnation', 'tangerine', 'lemon', 'goldenrod', 'saffron', 'pistachio',
            'avocado', 'seafoam', 'denim', 'cornflower', 'wisteria', 'amethyst',
            'orchid', 'heather', 'mulberry', 'eggplant', 'raspberry', 'strawberry',
            'blush', 'brick', 'cinnamon', 'caramel', 'chocolate', 'coffee', 'espresso',
            'walnut', 'chestnut', 'hazelnut', 'almond', 'sand', 'wheat', 'oatmeal',
            'stone', 'pewter', 'steel', 'ash', 'smoke', 'fog', 'mist', 'cloud',
            'snow', 'pearl', 'bone', 'sky', 'sea', 'grass', 'leaf', 'moss'
        }
        core.update(basic)

        # Modifiers
        modifiers = ['light', 'dark', 'bright', 'pale', 'deep', 'vivid', 'dull',
                     'muted', 'pastel', 'neon', 'dusty', 'dirty', 'soft', 'rich',
                     'royal', 'baby', 'hot', 'cool', 'warm', 'electric', 'burnt']

        # Add modified versions of basic colors
        for mod in modifiers:
            for color in list(basic)[:30]:  # Top 30 basic colors
                core.add(f"{mod} {color}")

        # Compound colors
        primaries = ['blue', 'green', 'red', 'yellow', 'purple', 'orange', 'pink', 'brown']
        for c1 in primaries:
            for c2 in primaries:
                if c1 != c2:
                    core.add(f"{c1}ish {c2}")
                    core.add(f"{c1} {c2}")
                    core.add(f"{c1}y {c2}")

        # Add high-frequency names from master vocabulary
        # (Sample from vocabulary to cover more semantic space)
        vocab_sample = list(self.master_vocab)[:1000]  # First 1000 (alphabetically sorted)
        core.update(vocab_sample)

        self.core_vocab = sorted(core)
        print(f"Building core vocabulary embeddings ({len(self.core_vocab):,} terms)...")
        self.core_embeddings = self.model.encode(self.core_vocab, show_progress_bar=True)

    def _load_cached_similarities(self):
        """Load pre-computed similarities from experiment results."""
        cache_path = self.CACHE_DIR / "exp1_sbert_full_results.json"
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

        # Step 3: Strip leading/trailing noise (preserve balanced parentheses)
        # Only strip truly noisy punctuation, not parentheses which may contain transliterations
        stripped = re.sub(r'^[!?.,;:*#@&%^~`]+', '', name)
        stripped = re.sub(r'[!?.,;:*#@&%^~`]+$', '', stripped)
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

    def is_in_vocabulary(self, name: str) -> bool:
        """Check if name is in the master vocabulary."""
        return name.lower().strip() in self.master_vocab

    def compute_similarity(self, name: str) -> Tuple[float, str]:
        """
        Compute semantic similarity to color vocabulary.

        Returns:
            Tuple of (similarity_score, best_matching_color)
        """
        name_lower = name.lower().strip()

        # Tier 1: Direct vocabulary lookup
        if name_lower in self.master_vocab:
            return 1.0, name_lower

        # Tier 2: Check cache
        if self._cached_similarities and name_lower in self._cached_similarities:
            cached = self._cached_similarities[name_lower]
            return cached['similarity'], cached['best_match']

        # Tier 3: Compute with SBERT
        if self.model is not None and self.core_embeddings is not None:
            from sklearn.metrics.pairwise import cosine_similarity
            embedding = self.model.encode([name])
            sims = cosine_similarity(embedding, self.core_embeddings)[0]
            best_idx = np.argmax(sims)
            return float(sims[best_idx]), self.core_vocab[best_idx]

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

        # Check 4: Vocabulary lookup or semantic similarity
        similarity, best_match = self.compute_similarity(name)
        info['similarity'] = similarity
        info['best_match'] = best_match
        info['in_vocabulary'] = similarity == 1.0

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
            'in_vocabulary': False,
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
        result['in_vocabulary'] = validation_info.get('in_vocabulary', False)

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
    print("Color Name Pipeline Demo (with Master Vocabulary)")
    print("=" * 70)

    # Test cases including previously problematic ones
    test_cases = [
        # Previously problematic (should now work)
        "periwinkle",          # Was filtered, now in vocabulary
        "mocha",               # Was filtered, now in vocabulary
        "camel",               # Was filtered, now in vocabulary
        # Edge cases
        "!!! green",
        "!!! purple",
        "#0000FF",
        "#FF5733",
        "bluish fuchsia",
        "teal purple",
        "fedex purple",
        "warm lavender",
        "army grey",
        # Should be filtered
        "this test is probably measuring how long people take",
        "asdfgh",
        "123456",
        "???",
        # Should pass
        "light blue",
        "sky blue",
        "forest green",
        "海老茶 (ebicha)",     # Japanese color name (in vocabulary)
    ]

    # Use cached mode for demo (faster)
    pipeline = ColorNamePipeline(load_model=False, use_cache=True)

    print("\nProcessing test cases:\n")
    for name in test_cases:
        result = pipeline.process(name)
        status = "VALID" if result['valid'] else "INVALID"
        vocab_tag = " [in vocab]" if result['in_vocabulary'] else ""
        print(f"'{name}'")
        print(f"  → cleaned: '{result['cleaned']}'")
        print(f"  → {status} (sim={result['similarity']:.3f}, match='{result['best_match']}'){vocab_tag}")
        if result['reason']:
            print(f"  → reason: {result['reason']}")
        print()


if __name__ == "__main__":
    main()
