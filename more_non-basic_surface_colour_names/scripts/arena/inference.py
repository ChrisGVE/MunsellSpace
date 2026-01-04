#!/usr/bin/env python3
"""
Color Inference Pipeline - D_TwoTower Model

Loads the trained D_TwoTower model and provides inference capabilities
for mapping text to color families.

The model uses 16 core color families:
  pink, red, orange, brown, yellow, olive, green, blue, purple, violet,
  white, gray, black, lime, teal, turquoise

Usage:
    from inference import ColorInference

    ci = ColorInference()
    result = ci.infer("Near the southern sea, a piercing calm...")
    print(result.top_family, result.confidence)
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

import numpy as np
import torch
import torch.nn as nn

from sentence_transformers import SentenceTransformer

# Setup paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent.parent
MODEL_DIR = PROJECT_DIR / "models" / "arena" / "arch_d_final"
DATA_DIR = PROJECT_DIR / "datasets"


# =============================================================================
# MODEL DEFINITION (must match training)
# =============================================================================

class TwoTowerModel(nn.Module):
    """
    Two-tower architecture (must match training definition):
    - Tower 1: Frozen SBERT for general semantics
    - Tower 2: Small trained encoder for color-specific features
    - Fusion layer combines both
    """

    def __init__(self, sbert_model: SentenceTransformer, color_dim: int = 64):
        super().__init__()
        self.sbert = sbert_model
        self.sbert_dim = 384
        self.color_dim = color_dim

        # Freeze SBERT
        for param in self.sbert.parameters():
            param.requires_grad = False

        # Color tower: small encoder
        self.color_encoder = nn.Sequential(
            nn.Linear(self.sbert_dim, 128),
            nn.GELU(),
            nn.Linear(128, color_dim),
            nn.LayerNorm(color_dim)
        )

        # Fusion layer
        self.fusion = nn.Sequential(
            nn.Linear(self.sbert_dim + color_dim, 384),
            nn.GELU(),
            nn.Linear(384, 384)
        )

    def forward(self, texts: List[str]) -> torch.Tensor:
        # Get SBERT embeddings (frozen)
        with torch.no_grad():
            sbert_emb = torch.tensor(self.sbert.encode(texts))

        # Get color embeddings (trainable)
        color_emb = self.color_encoder(sbert_emb)

        # Fuse
        combined = torch.cat([sbert_emb, color_emb], dim=-1)
        output = self.fusion(combined)

        return output

    def encode(self, texts):
        """Encode texts to embeddings."""
        single_input = isinstance(texts, str)
        if single_input:
            texts = [texts]
        with torch.no_grad():
            result = self.forward(texts).cpu().numpy()
            if single_input:
                return result.squeeze(0)
            return result


# =============================================================================
# INFERENCE RESULT
# =============================================================================

@dataclass
class InferenceResult:
    """Result of color inference."""
    text: str
    top_family: str  # Core family (16 categories)
    confidence: float
    all_families: List[Tuple[str, float]]  # (overlay, score) sorted descending
    top_overlay: str = None  # Specific overlay (may be same as family)
    embedding: Optional[np.ndarray] = None

    def __repr__(self):
        top3 = [f"{f}:{s:.2f}" for f, s in self.all_families[:3]]
        overlay_info = f" [{self.top_overlay}]" if self.top_overlay != self.top_family else ""
        return f"InferenceResult({self.top_family}{overlay_info}, conf={self.confidence:.3f}, top3=[{', '.join(top3)}])"


# =============================================================================
# COLOR INFERENCE CLASS
# =============================================================================

class ColorInference:
    """
    Color inference using the trained D_TwoTower model.

    Maps arbitrary text (including metaphorical/poetic descriptions)
    to color families using semantic embeddings.

    Uses a comprehensive set of overlays from seven sources:
    1. Extended ISCC-NBS (29 names)
    2. Centore's semantic overlays (30 names)
    3. Research-identified candidates (28 names)
    4. Jewel domain (11 gemstone names): amethyst, garnet, opal, etc.
    5. Metal domain (3 unique names): gold, old copper, verdigris
    6. Earth domain (5 earth tone names): umber, terracotta, clay, etc.
    7. Flora domain (4 plant-based names): moss, fern, pine, cedar
    8. Fountain Pen Inks (pending data access - placeholder)

    Total: ~95 unique overlay terms after deduplication.
    """

    # Extended ISCC-NBS names (29)
    ISCC_NBS_EXTENDED = [
        "black", "blue", "brown", "gray", "green", "greenish yellow",
        "lime", "olive", "olive brown", "olive green", "orange",
        "orange yellow", "pink", "purple", "purplish blue", "purplish pink",
        "purplish red", "red", "reddish brown", "reddish orange",
        "reddish purple", "teal", "turquoise", "violet", "white",
        "yellow", "yellowish brown", "yellowish green", "yellowish pink"
    ]

    # Centore's 30 overlays (20 non-basic + 10 basic)
    CENTORE_OVERLAYS = [
        # 20 non-basic
        "aqua", "beige", "coral", "fuchsia", "gold", "lavender", "lilac",
        "magenta", "mauve", "navy", "peach", "rose", "rust", "sand", "tan",
        "taupe", "teal", "turquoise", "violet", "wine",
        # 10 basic
        "blue", "brown", "gray", "green", "orange", "pink", "purple",
        "red", "white", "yellow"
    ]

    # Research-identified overlay candidates
    RESEARCH_OVERLAYS = [
        "grey",       # Spelling variant of gray (strong)
        "maroon",     # Dark red-brown (good, 100% consistency)
        "indigo",     # Deep blue-violet (good)
        "silver",     # Metallic gray (good)
        "plum",       # Purple variant (marginal)
        "aquamarine", # Blue-green (marginal)
        "carmine",    # Deep red (marginal)
        "crimson",    # Bright red (common usage)
        "cyan",       # Blue-green (common usage)
        "magenta",    # Already in Centore but important
        "scarlet",    # Bright red
        "amber",      # Orange-yellow
        "bronze",     # Brown-orange metallic
        "copper",     # Red-brown metallic
        "cream",      # Off-white
        "ivory",      # Warm white
        "charcoal",   # Dark gray
        "burgundy",   # Dark red
        "emerald",    # Bright green
        "jade",       # Green
        "sapphire",   # Blue
        "ruby",       # Red
        "pearl",      # White/iridescent
        "mint",       # Light green
        "sage",       # Gray-green
        "khaki",      # Tan/brown
        "ochre",      # Yellow-brown
        "sepia",      # Brown
    ]

    # Jewel domain overlays (11 gemstone terms)
    JEWEL_OVERLAYS = [
        "amethyst",     # Purple-violet gemstone
        "garnet",       # Deep red gemstone
        "opal",         # Iridescent, predominantly light
        "tanzanite",    # Blue-violet gemstone
        "tsavorite",    # Bright green garnet variety
        "malachite",    # Deep green mineral
        "lapis lazuli", # Deep blue with gold flecks
        "hematite",     # Metallic gray-black mineral
        "topaz",        # Golden yellow (common variety)
        "citrine",      # Yellow quartz
        "peridot",      # Yellow-green olivine
    ]

    # Metal domain overlays (non-duplicates only)
    # Note: silver, copper, rust already in other lists
    METAL_OVERLAYS = [
        "gold",         # Metallic yellow
        "old copper",   # Oxidized copper, brownish
        "verdigris",    # Green-blue copper patina
    ]

    # Earth domain overlays (5 earth tone terms)
    EARTH_OVERLAYS = [
        "umber",        # Raw/burnt umber pigment
        "terracotta",   # Orange-brown clay
        "clay",         # Natural clay color
        "mahogany",     # Reddish-brown wood
        "sienna",       # Raw/burnt sienna pigment
    ]

    # Flora domain overlays (4 plant-based terms)
    FLORA_OVERLAYS = [
        "moss",         # Yellow-green moss color
        "fern",         # Mid-green fern fronds
        "pine",         # Dark evergreen color
        "cedar",        # Reddish-brown wood
    ]

    # Fountain Pen Inks (placeholder - pending data access)
    # Data source: inkswatch.com (2854 inks with Hex/HSL/HSV)
    # Pending: User confirmation of data access and licensing
    FOUNTAIN_PEN_OVERLAYS = [
        # TODO: Populate after data access confirmed
        # Will require: data extraction, deduplication, Munsell conversion
    ]

    # Combined and deduplicated overlay set
    ALL_OVERLAYS = sorted(list(set(
        ISCC_NBS_EXTENDED + CENTORE_OVERLAYS + RESEARCH_OVERLAYS +
        JEWEL_OVERLAYS + METAL_OVERLAYS + EARTH_OVERLAYS + FLORA_OVERLAYS
        # Note: FOUNTAIN_PEN_OVERLAYS not included until data available
    )))

    # 16 core families for super-family grouping
    CORE_FAMILIES = [
        "pink", "red", "orange", "brown", "yellow", "olive",
        "green", "blue", "purple", "violet", "white", "gray",
        "black", "lime", "teal", "turquoise"
    ]

    # Map overlays to core families for super-family matching
    OVERLAY_TO_FAMILY = {
        # Direct matches (core families)
        "pink": "pink", "red": "red", "orange": "orange", "brown": "brown",
        "yellow": "yellow", "olive": "olive", "green": "green", "blue": "blue",
        "purple": "purple", "violet": "violet", "white": "white", "gray": "gray",
        "grey": "gray", "black": "black", "lime": "lime", "teal": "teal",
        "turquoise": "turquoise",
        # ISCC-NBS compound names
        "greenish yellow": "yellow", "olive brown": "brown", "olive green": "olive",
        "orange yellow": "orange", "purplish blue": "blue", "purplish pink": "pink",
        "purplish red": "red", "reddish brown": "brown", "reddish orange": "orange",
        "reddish purple": "purple", "yellowish brown": "brown",
        "yellowish green": "green", "yellowish pink": "pink",
        # Centore overlays
        "aqua": "teal", "beige": "brown", "coral": "pink", "fuchsia": "pink",
        "gold": "yellow", "lavender": "violet", "lilac": "violet",
        "magenta": "pink", "mauve": "violet", "navy": "blue", "peach": "orange",
        "rose": "pink", "rust": "brown", "sand": "brown", "tan": "brown",
        "taupe": "gray", "wine": "red",
        # Research overlays
        "maroon": "red", "indigo": "violet", "silver": "gray", "plum": "violet",
        "aquamarine": "teal", "carmine": "red", "crimson": "red", "cyan": "teal",
        "scarlet": "red", "amber": "orange", "bronze": "brown", "copper": "orange",
        "cream": "white", "ivory": "white", "charcoal": "gray", "burgundy": "red",
        "emerald": "green", "jade": "green", "sapphire": "blue", "ruby": "red",
        "pearl": "white", "mint": "green", "sage": "olive", "khaki": "brown",
        "ochre": "brown", "sepia": "brown",
        # Jewel domain mappings
        "amethyst": "violet",     # Purple-violet gemstone
        "garnet": "red",          # Deep red gemstone
        "opal": "white",          # Iridescent, predominantly light
        "tanzanite": "blue",      # Blue-violet gemstone
        "tsavorite": "green",     # Bright green garnet variety
        "malachite": "green",     # Deep green mineral
        "lapis lazuli": "blue",   # Deep blue with gold flecks
        "hematite": "gray",       # Metallic gray-black mineral
        "topaz": "yellow",        # Golden yellow (common variety)
        "citrine": "yellow",      # Yellow quartz
        "peridot": "green",       # Yellow-green olivine
        # Metal domain mappings (non-duplicates)
        "gold": "yellow",         # Metallic yellow
        "old copper": "brown",    # Oxidized copper, brownish
        "verdigris": "teal",      # Green-blue copper patina
        # Earth domain mappings
        "umber": "brown",         # Raw/burnt umber pigment
        "terracotta": "orange",   # Orange-brown clay
        "clay": "brown",          # Natural clay color
        "mahogany": "brown",      # Reddish-brown wood
        "sienna": "orange",       # Raw/burnt sienna pigment
        # Flora domain mappings
        "moss": "olive",          # Yellow-green moss color
        "fern": "green",          # Mid-green fern fronds
        "pine": "green",          # Dark evergreen color
        "cedar": "brown",         # Reddish-brown wood
    }

    # Super-family groupings for relaxed matching
    SUPER_FAMILIES = {
        "pink": ["pink", "red", "purple", "coral", "rose", "fuchsia", "magenta"],
        "red": ["red", "pink", "orange", "brown", "crimson", "scarlet", "maroon", "burgundy", "wine", "carmine", "ruby", "garnet"],
        "orange": ["orange", "red", "yellow", "brown", "peach", "coral", "amber", "copper", "terracotta", "sienna"],
        "brown": ["brown", "orange", "olive", "yellow", "tan", "beige", "rust", "sand", "taupe", "bronze", "khaki", "ochre", "sepia", "umber", "clay", "mahogany", "cedar", "old copper"],
        "yellow": ["yellow", "orange", "lime", "green", "gold", "greenish yellow", "amber", "topaz", "citrine"],
        "olive": ["olive", "green", "brown", "lime", "olive green", "olive brown", "sage", "khaki", "moss"],
        "green": ["green", "lime", "olive", "teal", "emerald", "jade", "mint", "sage", "yellowish green", "tsavorite", "malachite", "fern", "pine", "peridot"],
        "blue": ["blue", "teal", "turquoise", "purple", "navy", "purplish blue", "sapphire", "cyan", "aqua", "indigo", "lapis lazuli", "tanzanite"],
        "purple": ["purple", "violet", "pink", "blue", "magenta", "plum", "mauve", "reddish purple", "purplish pink", "purplish red", "amethyst"],
        "violet": ["violet", "purple", "pink", "blue", "lavender", "lilac", "mauve", "indigo", "plum", "amethyst", "tanzanite"],
        "white": ["white", "gray", "cream", "ivory", "pearl", "opal"],
        "gray": ["gray", "grey", "white", "black", "silver", "charcoal", "taupe", "hematite"],
        "black": ["black", "gray", "charcoal", "hematite"],
        "lime": ["lime", "green", "yellow", "olive", "yellowish green", "peridot"],
        "teal": ["teal", "blue", "turquoise", "green", "cyan", "aqua", "aquamarine", "verdigris"],
        "turquoise": ["turquoise", "teal", "blue", "green", "aqua", "aquamarine", "cyan", "verdigris"],
    }

    def __init__(self, model_path: Path = None, device: str = None):
        """
        Initialize the color inference model.

        Args:
            model_path: Path to the model.pt file (default: arch_d_final)
            device: 'cuda', 'mps', or 'cpu' (auto-detected if None)
        """
        self.model_path = model_path or MODEL_DIR / "model.pt"

        # Auto-detect device
        if device is None:
            if torch.cuda.is_available():
                self.device = "cuda"
            elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                self.device = "mps"
            else:
                self.device = "cpu"
        else:
            self.device = device

        self.model = None
        self.family_embeddings = None

    def load(self, use_all_overlays: bool = True):
        """Load the model and compute overlay embeddings.

        Args:
            use_all_overlays: If True, use all overlays (ISCC-NBS + Centore + Research).
                             If False, use only 16 core families.
        """
        if self.model is not None:
            return  # Already loaded

        print(f"Loading model from {self.model_path}...")

        # Load base SBERT
        base_sbert = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

        # Create model architecture
        self.model = TwoTowerModel(base_sbert, color_dim=64)

        # Load trained weights
        state_dict = torch.load(self.model_path, map_location=self.device)
        self.model.load_state_dict(state_dict)
        self.model.eval()

        # Choose anchor set
        self.use_all_overlays = use_all_overlays
        anchors = self.ALL_OVERLAYS if use_all_overlays else self.CORE_FAMILIES

        # Pre-compute overlay embeddings
        print(f"Computing embeddings for {len(anchors)} overlays...")
        self.overlay_embeddings = {}
        for overlay in anchors:
            emb = self.model.encode(overlay)
            self.overlay_embeddings[overlay] = emb / np.linalg.norm(emb)

        print(f"Model loaded successfully on {self.device}")
        print(f"Using {'ALL' if use_all_overlays else 'CORE'} overlays: {len(anchors)} anchors")

    def infer(self, text: str, include_embedding: bool = False) -> InferenceResult:
        """
        Infer color overlay from text.

        Args:
            text: Input text (can be any length, any language)
            include_embedding: Whether to include the raw embedding in result

        Returns:
            InferenceResult with top overlay, confidence, and all overlay scores
        """
        if self.model is None:
            self.load()

        # Encode input text
        text_emb = self.model.encode(text)
        text_emb = text_emb / np.linalg.norm(text_emb)

        # Compute similarity to all overlays
        scores = []
        for overlay in self.overlay_embeddings:
            sim = np.dot(text_emb, self.overlay_embeddings[overlay])
            scores.append((overlay, float(sim)))

        # Sort by score descending
        scores.sort(key=lambda x: -x[1])

        top_overlay = scores[0][0]
        confidence = scores[0][1]

        # Map to core family for compatibility
        top_family = self.OVERLAY_TO_FAMILY.get(top_overlay, top_overlay)

        return InferenceResult(
            text=text[:100] + "..." if len(text) > 100 else text,
            top_family=top_family,
            top_overlay=top_overlay,
            confidence=confidence,
            all_families=scores,  # Now contains all overlays
            embedding=text_emb if include_embedding else None
        )

    def infer_batch(self, texts: List[str]) -> List[InferenceResult]:
        """Infer color families for multiple texts."""
        return [self.infer(text) for text in texts]

    def is_in_super_family(self, predicted: str, expected: str) -> bool:
        """Check if predicted is in the super-family of expected."""
        return predicted in self.SUPER_FAMILIES.get(expected, [expected])

    def top_k_families(self, text: str, k: int = 3) -> List[Tuple[str, float]]:
        """Get top-k predicted families for text."""
        result = self.infer(text)
        return result.all_families[:k]


# =============================================================================
# DEMO
# =============================================================================

def main():
    """Demo the inference pipeline."""
    print("=" * 70)
    print("COLOR INFERENCE PIPELINE - D_TwoTower Model")
    print("=" * 70)
    print()

    # Initialize
    ci = ColorInference()
    ci.load()
    print()

    # Test cases (from research notes)
    test_cases = [
        # The user's original request - should map to lavender → violet family
        ("Near the southern sea, where light presses hard against the land, "
         "the air carries a piercing calm - an upward scent that seems borrowed "
         "from the sky itself, strong enough to still the heart and leave the "
         "horizon clearer than before.",
         "violet"),  # lavender is in violet family

        # Direct color family tests
        ("The sky is a deep cerulean blue", "blue"),
        ("Fresh lime green leaves in spring", "lime"),
        ("A warm terracotta sunset", "orange"),
        ("Deep violet amethyst crystals", "violet"),
        ("Soft pink cherry blossoms", "pink"),

        # Emotional/abstract tests
        ("Calm, peaceful, serene meditation", "blue"),
        ("Passionate, fiery love", "red"),
        ("Fresh, natural, organic growth", "green"),
        ("Warm, cozy autumn evening", "orange"),
        ("Mysterious, mystical twilight", "purple"),

        # Multilingual tests
        ("Mer bleue, ciel bleu", "blue"),  # French: blue sea, blue sky
        ("Fuoco rosso, passione ardente", "red"),  # Italian: red fire, burning passion
        ("Grüner Wald im Frühling", "green"),  # German: green forest in spring

        # Cherry blossom (sakura) test
        ("Sakura petals falling like pink snow in spring", "pink"),

        # NEW DOMAIN TESTS - Jewel domain
        ("Deep amethyst crystals gleaming in the cave", "violet"),
        ("The garnet ring sparkled like blood", "red"),
        ("Malachite green swirls in the stone", "green"),
        ("Lapis lazuli blue with golden flecks", "blue"),

        # NEW DOMAIN TESTS - Metal domain
        ("Old copper pipes with green verdigris", "teal"),
        ("Golden sunlight at dawn", "yellow"),

        # NEW DOMAIN TESTS - Earth domain
        ("Terracotta pottery in the sun", "orange"),
        ("Rich umber shadows in the painting", "brown"),
        ("Sienna earth tones of the canyon", "orange"),

        # NEW DOMAIN TESTS - Flora domain
        ("Moss-covered stones in the forest", "olive"),
        ("Deep pine green evergreens", "green"),
        ("Cedar wood paneling", "brown"),
    ]

    print(f"Total overlays: {len(ci.ALL_OVERLAYS)}")
    print()
    print("TEST RESULTS")
    print("-" * 80)

    correct = 0
    super_family_correct = 0

    for text, expected in test_cases:
        result = ci.infer(text)

        is_correct = result.top_family == expected
        is_super = ci.is_in_super_family(result.top_family, expected)

        if is_correct:
            correct += 1
            symbol = "✓"
        elif is_super:
            super_family_correct += 1
            symbol = "~"
        else:
            symbol = "✗"

        # Show overlay if different from family
        overlay_info = f" ({result.top_overlay})" if result.top_overlay != result.top_family else ""

        print(f"{symbol} Expected: {expected:10} | Got: {result.top_family:10}{overlay_info:15} | "
              f"Conf: {result.confidence:.3f}")
        print(f"  Text: {text[:55]}...")
        print(f"  Top 5 overlays: {[f'{o}:{s:.2f}' for o, s in result.all_families[:5]]}")
        print()

    total = len(test_cases)
    print("-" * 80)
    print(f"SUMMARY:")
    print(f"  Strict accuracy: {correct}/{total} ({100*correct/total:.1f}%)")
    print(f"  Super-family:    {correct + super_family_correct}/{total} "
          f"({100*(correct + super_family_correct)/total:.1f}%)")


if __name__ == "__main__":
    main()
