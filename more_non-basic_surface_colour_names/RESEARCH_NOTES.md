# Research Notes: Semantic Color Pipeline

## Project: MunsellSpace Color Overlays Extension

**Primary Goal**: Train embeddings that infer colors from metaphorical/poetic text
**Location**: `/more_non-basic_surface_colour_names/`
**Started**: December 2024
**Status**: Active research - Inference pipeline complete, integration next

---

## Table of Contents

1. [Research Objectives](#1-research-objectives)
2. [Key Findings & Results](#2-key-findings--results)
3. [Dead Ends & Failed Approaches](#3-dead-ends--failed-approaches)
4. [Data Sources](#4-data-sources)
5. [Methodology](#5-methodology)
6. [Scripts Reference](#6-scripts-reference)
7. [Literature](#7-literature)
8. [Folder Structure](#8-folder-structure)
9. [Replication Instructions](#9-replication-instructions)
10. [Publication Notes](#10-publication-notes)

---

## 1. Research Objectives

### Primary Goals (Priority Order)

1. **Semantic Color Inference**: Build pipeline that maps abstract concepts/metaphors to colors
   - Example: "Near the southern sea, piercing calm, upward scent" → lavender
   - Chain: Mediterranean → Provence → lavender flowers → lavender color

2. **Extend MunsellSpace Overlays**: Add new color family polyhedra beyond Centore's 30

3. **Firm Up Existing Overlays**: Validate/improve Centore's original 30 overlays

4. **Academic Paper**: Document methodology and findings for publication

### Key Constraints

- Must be **multilingual** (180+ languages)
- Must handle **metaphorical/poetic** input (not just explicit color names)
- Must be **replicable** (all steps documented, data sources cited)

---

## 2. Key Findings & Results

### 2.1 SBERT Baseline Experiment (2025-12-30)

**Script**: `scripts/arena/train_arena.py` (baseline test section)
**Model**: `paraphrase-multilingual-MiniLM-L12-v2` (384-dim)

**Results**:

| Test | Expected | Got | Verdict |
|------|----------|-----|---------|
| blau (DE) ↔ blue (EN) | high | 0.987 | Cross-lingual alignment excellent |
| cerulean → blue family | blue | yellow (0.308) | FAIL - Color families broken |
| calm → blue/lavender | blue | black (0.272) | FAIL - Emotional associations wrong |
| Poetic text → lavender | lavender | blue (0.271) | Weak but correct direction |

**Conclusion**: Base SBERT has excellent multilingual word alignment but lacks:
- Color family structure knowledge (cerulean ≠ blue variant)
- Color-emotion associations (calm ≠ black)
- Fine-grained color semantics

**Implication**: Fine-tuning required. Family structure is the crux.

### 2.2 Wikipedia Color Harvest (2025-12-29/30)

**Scripts**: `scripts/harvest_wikipedia_colors.py`, `scripts/parse_wikipedia_colors.py`

**Results**:
- 1,062 color articles successfully harvested from English Wikipedia
- 1,081 description pairs extracted
- 656 color → family mappings
- 7,254 related color pairs (co-mentioned colors)
- 14,586 cross-lingual translation pairs
- 13 color families identified

**Storage**: `datasets/wikipedia/`

### 2.3 Clustering Validation (2025-12-28)

**Scripts**: `scripts/src/family_clustering.py`, `scripts/src/validate_centore.py`

**Methods Compared**:

| Method | Purity | Recall | Notes |
|--------|--------|--------|-------|
| SBERT semantic | 57.6% | 69.4% | Best preserves human categories |
| K-means RGB | 40.2% | 44.8% | Fragments blue/green |
| K-means Munsell | 38.7% | 42.1% | Similar to RGB |
| GMM RGB | 37.3% | 40.5% | Soft clustering helps slightly |
| DBSCAN RGB | N/A | N/A | Finds outliers well |

**Conclusion**: Semantic (SBERT) clustering aligns best with Centore's 30 reference families.

### 2.4 Arena Training (2025-12-30 → 2026-01-01, COMPLETE)

**Script**: `scripts/arena/train_arena.py`
**Data**: 66,307 training pairs, 21,510 triplets

**Architectures Compared**:
- A: Standard Fine-Tuning (staged epochs)
- B: Multi-Task Training (simultaneous objectives)
- C: Adapter Layers (frozen base + trainable adapter)
- D: Two-Tower (frozen SBERT + small color encoder)

**Final Results**:

| Architecture | Family Acc | Emotion Acc | Cross-lingual | Training Time |
|--------------|------------|-------------|---------------|---------------|
| Baseline | 18.8% | 100%* | 90.9% | - |
| A_Standard | 34.4% | 70% | 92.1% | 55 min |
| B_MultiTask | 40.6% | 60% | 95.3% | 5.2 hours |
| C_Adapter | 37.5% | 50% | 98.0% | 56 min |
| **D_TwoTower** | **46.9%** | **80%** | 96.5% | 36 min |

*Baseline emotion accuracy is artificially 100% due to random alignment with limited test cases.

**Winner: D_TwoTower** 🏆

**Analysis**:
- D_TwoTower achieved best family accuracy (46.9%) and emotion accuracy (80%)
- Hypothesis confirmed: keeping SBERT frozen while learning color-specific features works best
- B_MultiTask's 5+ hour training time didn't pay off (only 40.6% family acc)
- C_Adapter had best cross-lingual retention (98%) but worst emotion accuracy (50%)
- All trained models improved family accuracy 2-2.5x over baseline (18.8%)

**Model Location**: `models/arena/arch_d_final/`

### 2.5 Anchor Family Evaluation (2026-01-01)

**Objective**: Determine optimal anchor families for color name classification

Tested D_TwoTower with different anchor family sets on 200 color names per family
(names containing that family word, e.g., "sky blue" for blue).

#### Test 1: 29 ISCC-NBS Extended Families (includes compound names)

Families: black, blue, brown, gray, green, greenish yellow, lime, olive, olive brown,
olive green, orange, orange yellow, pink, purple, purplish blue, purplish pink,
purplish red, red, reddish brown, reddish orange, reddish purple, teal, turquoise,
violet, white, yellow, yellowish brown, yellowish green, yellowish pink

**Result**: Poor performance due to compound name confusion

| Family | Strict | Super-family | Issue |
|--------|--------|--------------|-------|
| blue | 3.0% | 11.5% | Predicts "violet" (65/200) |
| yellow | 1.0% | 23.0% | Predicts "yellowish pink" |
| white | 1.5% | 1.5% | Predicts "gray" (95/200) |
| violet | 58.5% | 96.5% | Good |
| lime | 71.5% | 74.0% | Good |
| brown | 20.5% | 94.0% | Super-family works |

**Conclusion**: Too many overlapping compound categories confuse the model.

#### Test 2: 16 Core Families (simple names only)

Families: pink, red, orange, brown, yellow, olive, green, blue, purple, violet,
white, gray, black, lime, teal, turquoise

**Result**: Excellent performance

| Family | Strict | Super-family | Top 3 |
|--------|--------|--------------|-------|
| violet | **97.0%** | 98.5% | 99.5% |
| olive | **91.0%** | 91.0% | 100% |
| brown | 91.0% | 92.5% | 96.5% |
| orange | 88.5% | 97.0% | 100% |
| purple | 87.0% | 97.0% | 99.0% |
| pink | 86.0% | 86.0% | 98.5% |
| white | 84.0% | 85.0% | 91.5% |
| lime | 73.0% | 73.0% | 81.0% |
| red | 61.0% | 70.0% | 90.0% |
| yellow | 60.0% | 85.0% | 93.5% |
| gray | 59.5% | 60.5% | 77.0% |
| teal | 57.0% | 64.0% | 83.0% |
| blue | 46.0% | 79.5% | 94.0% |
| black | 42.5% | 67.5% | 72.0% |
| green | 26.0% | 96.0% | 55.5% |

**Key Insights**:
- Violet and olive (extended ISCC-NBS names) work excellently: 97% and 91%
- Green spreads across lime/teal/olive but 96% super-family accuracy
- Blue often → teal (reasonable), 79.5% super-family
- 16 simple anchors is the sweet spot for inference

**Selected for Production**: 16 core families

### 2.6 Full Color Name Classification (2026-01-01)

**Input**: 184,296 color names from consolidated dataset
**Model**: D_TwoTower with 16 core family anchors
**Runtime**: 672.9 seconds (274 names/sec)
**Output**: `datasets/consolidated/color_names_with_families.csv`

#### Family Distribution

| Family | Count | Percentage |
|--------|-------|------------|
| lime | 20,935 | 11.4% |
| orange | 17,807 | 9.7% |
| violet | 16,659 | 9.0% |
| brown | 15,503 | 8.4% |
| olive | 15,419 | 8.4% |
| teal | 15,073 | 8.2% |
| pink | 13,758 | 7.5% |
| purple | 10,027 | 5.4% |
| gray | 9,674 | 5.2% |
| turquoise | 8,485 | 4.6% |
| blue | 8,419 | 4.6% |
| red | 7,416 | 4.0% |
| black | 7,200 | 3.9% |
| yellow | 6,606 | 3.6% |
| green | 6,550 | 3.6% |
| white | 4,765 | 2.6% |

#### Confidence Statistics

- Mean: 0.740 ± 0.133
- Range: -0.034 to 1.000
- Highest confidence families: purple (0.831), blue (0.799), pink (0.796)
- Lowest confidence families: turquoise (0.635), black (0.667), white (0.673)

#### Sample High-Confidence Assignments

| Color Name | Predicted Family | Confidence |
|------------|-----------------|------------|
| green | green | 1.000 |
| blue | blue | 1.000 |
| light blue | teal | 0.928 |
| magenta | pink | 0.836 |
| cyan | teal | 0.852 |
| lime green | lime | 0.932 |
| tan | brown | 0.878 |
| fuchsia | pink | 0.852 |

**Observations**:
- Distribution is reasonably balanced across 16 families
- Lime/orange/violet are most common (crowdsourced color names skew toward vivid colors)
- White is least common (2.6%) - few white variants in crowdsourced data
- Model correctly handles common aliases (cyan→teal, magenta→pink, fuchsia→pink)

### 2.7 Non-Basic Color Evaluation (2026-01-01)

**Objective**: Test model on Centore's 30 families and new overlay candidates

#### Test 1: Centore's 30 → Our 16 Mapping

| Centore Family | → Our Family | Conf | Notes |
|----------------|--------------|------|-------|
| blue | blue | 1.00 | ✓ Direct match |
| brown | brown | 1.00 | ✓ Direct match |
| gray | gray | 1.00 | ✓ Direct match |
| green | green | 1.00 | ✓ Direct match |
| orange | orange | 1.00 | ✓ Direct match |
| pink | pink | 1.00 | ✓ Direct match |
| purple | purple | 1.00 | ✓ Direct match |
| red | red | 1.00 | ✓ Direct match |
| teal | teal | 1.00 | ✓ Direct match |
| turquoise | turquoise | 1.00 | ✓ Direct match |
| violet | violet | 1.00 | ✓ Direct match |
| white | white | 1.00 | ✓ Direct match |
| yellow | yellow | 1.00 | ✓ Direct match |
| aqua | teal | 0.92 | Reasonable (blue-green) |
| beige | brown | 0.77 | Reasonable (tan family) |
| coral | pink | 0.84 | Reasonable (pink-orange) |
| fuchsia | pink | 0.85 | Correct (bright pink) |
| gold | yellow | 0.79 | Reasonable |
| lavender | violet | 0.86 | Correct (light purple) |
| lilac | violet | 0.87 | Correct (light purple) |
| magenta | pink | 0.84 | Correct (pink/red) |
| mauve | violet | 0.84 | Correct (grayish purple) |
| navy | turquoise | 0.75 | **Unexpected** - should be blue |
| peach | yellow | 0.74 | Reasonable (yellow-orange) |
| rose | pink | 0.90 | Correct |
| rust | brown | 0.87 | Correct (brown-orange) |
| sand | brown | 0.86 | Correct |
| tan | brown | 0.88 | Correct |
| taupe | gray | 0.71 | Reasonable (gray-brown) |
| wine | red | 0.82 | Correct (dark red) |

**Mapping summary**: 13 direct matches, 16 reasonable mappings, 1 unexpected (navy→turquoise)

#### Test 2: New Overlay Candidates

| Candidate | Tier | → Our Family | Conf | Variant Consistency |
|-----------|------|--------------|------|---------------------|
| grey | strong | gray | 0.96 | 80% ✓ |
| silver | good | gray | 0.83 | 40% ⚠ |
| indigo | good | violet | 0.85 | 60% |
| maroon | good | brown | 0.86 | 100% ✓ |
| black | good | black | 1.00 | 60% |
| lime | marginal | lime | 1.00 | 100% ✓ |
| carmine | marginal | red | 0.83 | 40% ⚠ |
| aquamarine | marginal | teal | 0.85 | 40% ⚠ |
| plum | marginal | violet | 0.84 | 60% |

**Strong performers**: grey, maroon, lime, black (high consistency)
**Weak performers**: silver, carmine, aquamarine (variants scatter)

#### Test 3: Self-Match Rates in 184K Dataset

Colors containing a family name - what % classify to that family?

| Family | Count | Self-Match | Notes |
|--------|-------|------------|-------|
| violet | 2,005 | **85%** | Best performer |
| pink | 10,049 | 78% | Strong |
| orange | 4,504 | 75% | Strong |
| brown | 7,284 | 74% | Strong |
| purple | 12,159 | 73% | Strong |
| turquoise | 1,148 | 59% | Good |
| white | 1,843 | 56% | Good |
| teal | 2,145 | 54% | Good |
| gray | 6,909 | 50% | Moderate |
| yellow | 7,013 | 40% | Spreads to lime (44%) |
| red | 9,404 | 34% | Spreads to pink/brown |
| blue | 23,045 | 28% | Spreads to teal (36%) |
| green | 28,353 | **8%** | Spreads to lime (39%), olive (29%) |

**Key insight**: Basic colors (green, blue, yellow, red) spread across sub-families.
This is expected - "light green" → lime, "dark blue" → teal, etc.

### 2.8 Inference Pipeline (2026-01-01)

**Scripts**: `scripts/arena/inference.py`, `scripts/semantic_color_pipeline.py`

**Architecture**: Hybrid Rule+ML approach

1. **Rule-based component**: Hand-crafted concept→color associations
   - Visual (sky→blue, fire→red)
   - Emotional (calm→blue/lavender, passionate→red)
   - Cultural (Provence→lavender, Mediterranean→blue)
   - Sensory (scent→lavender, warmth→orange)

2. **ML component**: D_TwoTower model with 16 core family anchors
   - Loads trained model from `models/arena/arch_d_final/model.pt`
   - Computes cosine similarity to family embeddings
   - Provides broader coverage for novel/abstract text

3. **Hybrid fusion**: Weighted combination (default 50/50)
   - Boosts ML weight when rules have no matches
   - Maps rule colors to families using COLOR_TO_FAMILY dict

**Test Results** (6 poetic/metaphorical texts):
- Strict accuracy: 33.3% (2/6)
- Super-family accuracy: 100% (6/6)

**Usage**:
```python
from scripts.semantic_color_pipeline import SemanticColorPipeline

pipeline = SemanticColorPipeline(use_ml=True, ml_weight=0.5)
family, confidence, all_families = pipeline.infer_family(
    "Near the southern sea, a piercing calm..."
)
# → ('blue', 8.26, [('blue', 8.26), ('violet', 4.92), ...])
```

**Standalone ML inference**:
```python
from scripts.arena.inference import ColorInference

ci = ColorInference()
ci.load()
result = ci.infer("The sky is cerulean blue")
# → InferenceResult(teal, conf=0.645, top3=[teal:0.65, blue:0.60, violet:0.60])
```

### 2.9 Overlay Taxonomy & Theoretical Framework (2026-01-01)

#### 2.9.1 Color Domain Categorization

Following Centore's modifier pattern, all non-basic colors follow the structure: `[modifier] + [base]`
(e.g., "purplish blue", "light red"). We categorize overlays into semantic domains:

**Core Overlays** (30 Centore families with polyhedra):
- Basic: blue, brown, gray, green, orange, pink, purple, red, white, yellow
- Non-basic: aqua, beige, coral, fuchsia, gold, lavender, lilac, magenta, mauve, navy,
  peach, rose, rust, sand, tan, taupe, teal, turquoise, violet, wine

**Extended ISCC-NBS** (16 unique, using modifier pattern):
- Compound: greenish yellow, olive brown, olive green, orange yellow, purplish blue,
  purplish pink, purplish red, reddish brown, reddish orange, reddish purple,
  yellowish brown, yellowish green, yellowish pink
- Simple: black, lime, olive (exist in extended Munsell system)

**Jewel Tones Domain** (gemstone-inspired):
- Current: emerald, jade, sapphire, ruby, amber, aquamarine
- Candidates: amethyst, garnet, opal, obsidian, jet, tanzanite, tsavorite,
  malachite, lapis lazuli, hematite, topaz, citrine, peridot

**Metal Domain** (metallic colors):
- Base metals: silver, gold, bronze, copper, brass, iron, tin, platinum, steel
- Oxidation states: rust (iron), verdigris/patina (copper), tarnish (silver)

**Earth Tones Domain**:
- Current: ochre, sepia, khaki, sienna
- Candidates: umber, terracotta, clay, mahogany

**Flora Domain** (plant-inspired):
- Current: mint, sage, coral (also animal), cream, ivory
- Candidates: moss, fern, olive (also ISCC-NBS), pine, cedar

#### 2.9.2 Overlay Superposition Theory

Key theoretical insight from Centore's framework:

**Overlays exist in superposition with base colors, not in isolation.**

1. **Base Color Background**: Every point in Munsell space has a well-defined base color
   (from ISCC-NBS 13 or extended). Overlays add semantic meaning on top.

2. **Bidirectional Fuzziness**: The perception boundary between colors is fuzzy in both directions:
   - A lavender can be perceived as "light purple" or "purplish"
   - A teal can be perceived as "blue-green" or "greenish blue"
   - The overlay captures this ambiguity explicitly

3. **Containment vs Extension**:
   - If an overlay is **fully contained** within its base color → adds nothing geometrically
     (but may add semantic/cultural value)
   - If an overlay **extends beyond** its base color → appropriates regions from adjacent colors
     (this is where overlays provide value for color naming)

4. **Negative Definition Problem**: Saying "what is not [overlay] is [base]" is a negative way
   to describe fuzziness. Instead, overlays should be understood as **positive regions** that
   may overlap with multiple base colors.

#### 2.9.3 Polyhedra Requirements

A color family requires **sufficient data points** to define a polyhedron:

| Points | Geometric Possibility |
|--------|----------------------|
| 1 | Point only (no polyhedron) |
| 2 | Line segment |
| 3 | Triangle (2D) |
| 4 | Tetrahedron (minimum 3D polyhedron) |
| n≥4 | Convex hull possible |

**Significance criteria** (for overlay acceptance):
- Minimum exemplars needed (Centore uses ~20-50 per family)
- Geographic/cultural distribution requirements
- Cross-linguistic consistency
- Temporal stability (not just a trend)

Colors without sufficient exemplars may exist linguistically but are not relevant for
geometric color space partitioning.

#### 2.9.4 Extended Munsell Colors (No Polyhedra Needed)

These exist in the extended Munsell notation and don't require separate polyhedra:

| Color | Munsell Location | Notes |
|-------|------------------|-------|
| black | N0/ to N1/ | Achromatic, neutral axis |
| gray/grey | N4/ to N6/ | Achromatic, neutral axis |
| olive | ~2.5Y 4/4 | Low-chroma yellow-green |
| lime | ~5GY 7/10 | High-chroma yellow-green |
| teal | ~5BG 5/6 | Blue-green |
| turquoise | ~7.5BG 6/8 | Blue-green (more blue than teal) |
| violet | ~7.5P 4/12 | Already in ISCC-NBS |

The downside: we don't capture perception fuzziness at boundaries. But these are
well-defined in the Munsell system already.

#### 2.9.5 Family Mapping Conventions (Following Centore)

These mappings follow Centore's published family assignments:

| Overlay | → Family | Rationale |
|---------|----------|-----------|
| coral | orange | Orange with pink influence, more orange than pink |
| peach | orange | Coral with less pink, yellow-orange family |
| lavender | purple | Light violet, canonical ISCC-NBS purple |
| teal | blue | Blue-green, more green than blue; mapped to blue by convention |
| turquoise | blue | Blue-green, more blue than green; mapped to blue by convention |

These are not "questionable" - they follow established color science conventions.

---

## 3. Dead Ends & Failed Approaches

### 3.1 Direct RGB Clustering for Family Assignment

**What**: Cluster colors by RGB coordinates, assign families by cluster centroid
**Why it failed**: RGB space doesn't match human perception. Blue-greens and blue-purples scatter across clusters.
**Evidence**: Purity 37-40% vs 57.6% for semantic clustering
**Scripts**: `scripts/src/family_clustering.py`

### 3.2 Fourier 4 Correction Model

**What**: Fit Fourier series to correct systematic hue bias in RGB→Munsell conversion
**Status**: Jury still out - not definitively failed but unconfirmed
**Issue**: May be overfitting to calibration artifacts rather than real bias
**Scripts**: `archives/scripts/fit_fourier_correction.py`, `archives/scripts/correction_model.py`

### 3.3 Earlier Phase 1-6 Pipeline (December 2024)

**What**: Multi-phase pipeline for color name processing
**Status**: Archived - methodology was haphazard
**Issue**: No rigorous Centore replication before extending
**Scripts**: `archives/scripts/phase1_*.py` through `phase6_*.py`
**Lesson**: Must replicate Centore exactly first, then extend

### 3.4 BERT Token-Level Features

**What**: Use BERT subword token embeddings for color classification
**Why it failed**: Subword tokens don't preserve color semantics ("cer" + "ule" + "an")
**Scripts**: `archives/scripts/exp2_bert_tokens.py`

---

## 4. Data Sources

### 4.1 Wikipedia Color Articles (Our Collection)

**Collected**: 2025-12-29/30
**Location**: `datasets/wikipedia/en/`
**Format**: JSON (one file per article)
**Size**: 1,062 articles
**License**: CC-BY-SA

### 4.2 Free Association Database (7 Languages)

**Citation**: Journal of Open Psychology Data, DOI: 10.5334/jopd.140
**URL**: https://osf.io/xzcbg/
**Downloaded**: 2025-12-30
**Location**: `datasets/connotations/free_association/`
**Contents**: 223,786 free association responses across 7 languages
**License**: CC-BY 4.0

### 4.3 Jonauskaite Color-Emotion Survey

**Citation**: Psychological Science 31(10), DOI: 10.1177/0956797620948810
**URL**: https://osf.io/873df/
**Downloaded**: 2025-12-30
**Location**: `datasets/connotations/jonauskaite/`
**Contents**: 4,598 participants, 30 nations, 12 colors × 20 emotions
**License**: Open access

### 4.4 128-Year Systematic Review

**URL**: https://osf.io/g5srf/
**Downloaded**: 2025-12-30
**Location**: `datasets/connotations/systematic_review/`
**Contents**: Meta-analysis of color-emotion research since 1896

### 4.5 XKCD Color Survey

**Location**: Main repo `assets/xkcd/` (not duplicated here)
**Contents**: 954 curated colors + 157K raw survey responses

### 4.6 World Color Survey (WCS)

**Location**: `datasets/wcs/`
**Contents**: 110 unwritten languages, 320 Munsell chips
**Purpose**: Cross-cultural color naming validation

### 4.7 Centore Reference Data

**Source**: Centore (2020) JAIC paper supplementary materials
**Location**: `datasets/phase6/polyhedra/`
**Contents**: 30 reference color family polyhedra

---

## 5. Methodology

### 5.1 Overall Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    SEMANTIC COLOR PIPELINE                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │ PHASE A:     │    │ PHASE B:     │    │ PHASE C:     │       │
│  │ Data Harvest │ -> │ Preprocessing │ -> │ Clustering   │       │
│  │              │    │              │    │              │       │
│  │ - Wikipedia  │    │ - Pair gen   │    │ - K-means    │       │
│  │ - Jonauskaite│    │ - Triplets   │    │ - DBSCAN     │       │
│  │ - Free Assoc │    │ - Splits     │    │ - SBERT      │       │
│  └──────────────┘    └──────────────┘    │ - Consensus  │       │
│                                           └──────────────┘       │
│                                                  │               │
│                                                  v               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │ PHASE F:     │    │ PHASE E:     │    │ PHASE D:     │       │
│  │ Integration  │ <- │ Evaluation   │ <- │ Embedding    │       │
│  │              │    │              │    │ Training     │       │
│  │ - Polyhedra  │    │ - Family acc │    │              │       │
│  │ - MunsellSpace│   │ - Emotion acc│    │ - SBERT      │       │
│  │              │    │ - Poetic test│    │ - Arena      │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Training Data Composition

| Type | Count | Source | Purpose |
|------|-------|--------|---------|
| family_sibling | 36,216 | Wikipedia | Color → family structure |
| cross_lingual | 14,586 | Wikipedia | Multilingual alignment |
| related | 7,254 | Wikipedia | Color co-occurrence |
| emotion | 5,033 | Jonauskaite | Color-emotion mapping |
| free_association | 1,499 | OSF DB | Cultural associations |
| description | 1,081 | Wikipedia | Color semantics |
| family | 638 | Wikipedia | Base family pairs |
| **TOTAL** | **66,307** | | |

### 5.3 Evaluation Framework

1. **Color Family Accuracy**: % of color variants correctly grouped
   - Ground truth: Centore's 30 families
   - Test: cerulean→blue, crimson→red, emerald→green

2. **Emotion Accuracy**: % of emotion→color predictions matching Jonauskaite
   - Ground truth: Top associations per emotion
   - Test: calm→blue/lavender, anger→red

3. **Cross-lingual Consistency**: Same concept → same colors across languages
   - Test: "calm" (EN) = "calme" (FR) = "ruhig" (DE)

4. **Poetic Inference**: Free-form text → color
   - User test case: Southern sea/piercing calm → lavender

---

## 6. Scripts Reference

### 6.1 Active Scripts (`scripts/`)

| Script | Purpose | Status |
|--------|---------|--------|
| `arena/train_arena.py` | 4-architecture comparison training | Complete |
| `arena/inference.py` | D_TwoTower model inference | Complete |
| `arena/data_preprocessing.py` | Generate 66K training pairs | Complete |
| `harvest_wikipedia_colors.py` | Fetch Wikipedia color articles | Complete |
| `parse_wikipedia_colors.py` | Extract training data from Wikipedia | Complete |
| `semantic_color_pipeline.py` | Hybrid rule+ML inference pipeline | Complete |
| `src/family_clustering.py` | Multi-method clustering module | Complete |
| `src/validate_centore.py` | Validate against Centore families | Complete |

### 6.2 Archived Scripts (`archives/scripts/`)

47 scripts from earlier pipeline phases. Key ones:

| Script | Purpose | Status |
|--------|---------|--------|
| `phase1_data_inventory.py` | Initial data survey | Archived |
| `phase2_*_*.py` | Spelling/typo/compound handling | Archived |
| `phase3_coordinate_analysis.py` | Munsell coordinate analysis | Archived |
| `centore_comparison.py` | Compare with Centore polyhedra | Archived |
| `exp1_sbert_similarity.py` | SBERT experiments | Archived |
| `correction_model.py` | Fourier correction (uncertain) | Archived |

Full inventory: `archives/scripts/INVENTORY.md`

---

## 7. Literature

### 7.1 Foundational

- **Berlin & Kay (1969)**: Basic Color Terms - 11 universal color terms
- **World Color Survey (1976)**: 110 languages, privileged color anchors
- **Centore (2020)**: JAIC paper on 30 color family polyhedra

### 7.2 Color-Emotion

- **Jonauskaite et al. (2020)**: Universal color-emotion patterns (30 nations)
- **Adams & Osgood (1973)**: 23-culture semantic differential study

### 7.3 Embeddings & Domain Adaptation

- **Reimers & Gurevych (2019)**: Sentence-BERT architecture
- **Hu et al. (2021)**: LoRA - Low-rank adaptation
- **TSDAE**: Domain adaptation for SBERT (8-10 point improvement)

### 7.4 Full Literature Review

See: `writeups/LITERATURE_REVIEW.md`

---

## 8. Folder Structure

```
more_non-basic_surface_colour_names/
├── RESEARCH_NOTES.md          # THIS FILE - Master reference
├── inventory.md               # Auto-generated file listing
│
├── archives/                  # Superseded work
│   ├── scripts/               # 47 archived scripts
│   ├── article_drafts/        # Early paper drafts
│   └── MANIFEST.md            # Archive index
│
├── datasets/                  # All data
│   ├── arena_training/        # Preprocessed training data (66K pairs)
│   ├── clustered/             # Clustering results
│   ├── connotations/          # Jonauskaite, Free Assoc, 128-year
│   ├── parsed/                # Processed Wikipedia data
│   ├── phase6/                # Centore polyhedra
│   ├── wcs/                   # World Color Survey
│   └── wikipedia/             # Raw Wikipedia articles
│
├── literature/                # References (URLs, not PDFs)
│   └── SOURCES.md
│
├── logs/                      # Training logs
│   └── arena/
│
├── memory/                    # Session context files
│   └── critical_decisions.md
│
├── models/                    # Trained model checkpoints
│   └── arena/
│
├── scripts/                   # Active code
│   ├── arena/                 # Training scripts
│   ├── src/                   # Shared modules
│   └── *.py                   # Pipeline scripts
│
├── tmp/                       # Temporary files
│
└── writeups/                  # Documentation
    ├── drafts/                # In-progress articles
    ├── methodology/           # Pipeline documentation
    ├── old_md/                # Superseded writeups
    ├── references/            # Bibliography
    ├── results/               # Experiment results
    └── LITERATURE_REVIEW.md   # Academic context
```

---

## 9. Replication Instructions

### 9.1 Environment Setup

```bash
cd more_non-basic_surface_colour_names
python3.12 -m venv .venv
source .venv/bin/activate
pip install sentence-transformers torch "numpy<2" pandas scikit-learn datasets accelerate
```

### 9.2 Data Preparation

```bash
# 1. Wikipedia harvest (already done, ~30 min)
python scripts/harvest_wikipedia_colors.py
python scripts/parse_wikipedia_colors.py

# 2. Download academic datasets (manual from OSF)
# - https://osf.io/xzcbg/ → datasets/connotations/free_association/
# - https://osf.io/873df/ → datasets/connotations/jonauskaite/

# 3. Preprocess for training
python scripts/arena/data_preprocessing.py
```

### 9.3 Training

```bash
# Run arena training (~6-12 hours)
source .venv/bin/activate
python scripts/arena/train_arena.py 2>&1 | tee logs/arena/training.log &
```

### 9.4 Evaluation

```bash
# After training completes
python scripts/arena/evaluate_arena.py  # TODO: Create this script
```

---

## 10. Publication Notes

### 10.1 Potential Titles

1. "ColorSBERT: Domain-Adapted Sentence Embeddings for Semantic Color Inference"
2. "From Metaphor to Color: Fine-Tuning Language Models for Cross-Modal Perception"
3. "A Comparative Study of Embedding Architectures for Multilingual Color Semantics"

### 10.2 Key Claims to Support

1. Base SBERT lacks color family knowledge (baseline experiment)
2. Fine-tuning restores/creates color relationships (arena results)
3. Cross-lingual consistency is achievable (multilingual training)
4. Emotional/cultural associations can be learned (Jonauskaite integration)

### 10.3 Experimental Contributions

- First systematic comparison of 4 architectures for color embeddings
- 66,307 training pairs across 180+ languages
- Novel evaluation on family accuracy, emotion accuracy, cross-lingual consistency
- Real-world test: poetic/metaphorical text → color inference

### 10.4 Target Venues

- Journal of Open Psychology Data (methodology paper)
- Color Research and Application (application paper)
- ACL/EMNLP (NLP methodology paper)
- AIC (Association Internationale de la Couleur) conference

---

## 11. Color Space Transformation Analysis (2026-01-04)

### 11.1 The Screen-Surface Gap Problem

**Core Question**: How do we transform between Munsell (surface colors) and RGB monitor profiles (self-luminous colors)?

**Empirical Findings from Track B Phase 3 Calibration**:
- Value bias: +2.06 (screen appears ~2 units lighter, uniformly positive)
- Chroma bias: +0.80 (screen slightly more saturated, variable by family)
- Hue bias: -31.8° mean, 21.0° std (NON-UNIFORM, category-dependent)

### 11.2 Reference System: CIE XYZ

All color systems are defined relative to CIE XYZ:

```
Munsell HVC ←→ XYZ (via Renotation Data, Illuminant C)
sRGB ←→ XYZ (via 3×3 matrix, D65, γ=2.4)
P3 ←→ XYZ (via different 3×3 matrix, D65)
Adobe RGB ←→ XYZ (via different matrix, D65, γ=2.2)
```

### 11.3 Key Insight: Surface vs Self-Luminous Appearance

Even when surface and screen colors have **identical XYZ tristimulus values**, they don't look the same:

| Surface Color | Screen Color |
|---------------|--------------|
| Illumination × Reflectance → Eye | Emission → Eye |
| Ambient light affects perception | Self-luminous, no ambient needed |
| MacAdam limits apply | Can exceed MacAdam limits |
| Munsell defined under Illuminant C | sRGB defined under D65 |

### 11.4 Mathematical Framework

#### Known Transformations (Closed-Form)

**RGB → XYZ** (profile-dependent):
```
XYZ = M_profile × linearRGB
where linearRGB = degamma(RGB)
```

For sRGB:
```
M_sRGB = [0.4124  0.3576  0.1805]
         [0.2126  0.7152  0.0722]
         [0.0193  0.1192  0.9505]
```

**Illuminant Adaptation** (D65 → C):
```
XYZ_C = M_Bradford⁻¹ × diag(ρ_C/ρ_D65) × M_Bradford × XYZ_D65
```

#### Non-Symbolic Part

**XYZ ↔ Munsell HVC** cannot be expressed symbolically because:
- Munsell is defined empirically (1943 Renotation Data)
- The space is perceptually uniform but geometrically irregular
- Conversion requires interpolation in lookup tables
- ASTM D1535 specifies an algorithmic procedure, not closed-form

#### Screen-Surface Correction Function

Based on calibration data:
```
M_surface = f(M_screen)

where:
  V_surface = V_screen - β_V(family)     # Value correction (~2.06)
  C_surface = C_screen - β_C(family)     # Chroma correction (~0.80)
  H_surface = H_screen + Δh(H_screen)    # Hue rotation (non-uniform!)
```

### 11.5 Gamut Relationships

**Gamut Mismatch** (from Centore literature):
- sRGB gamut extends BEYOND MacAdam limits in some areas
- sRGB fails to fill all volume INSIDE MacAdam limits
- Complete exemplification of either system in the other is impossible

**MacAdam Limits**:
- Theoretical boundary of surface colors (object-color solid)
- Defined by "optimal colors" with reflectance spectra ∈ {0, 1} with ≤2 transitions
- Apply only to surface colors, not to coloured lights

**Key Literature Quotes**:
> "the sRGB gamut both extends beyond the MacAdam limits, and fails to fill all the volume inside the MacAdam limits" - Centore

> "It lies outside the MacAdam limits, so it is in the sRGB gamut, but not in the Munsell gamut. Likewise, many Munsell colours, especially highly chromatic ones, cannot be produced on an sRGB monitor" - Centore

### 11.6 Proposed Paper Figure

Multi-panel gamut visualization:

1. **xy Chromaticity Diagram**: Spectrum locus, sRGB triangle, P3 triangle, MacAdam limit at Y=0.5

2. **Munsell Value Slices** (V=3, 5, 7): Munsell chroma limits, sRGB/P3 intersections

3. **Calibration Visualization**: Hue wheel with Δh rotation, value/chroma shift vectors by family

### 11.7 Research Questions

1. Can we derive a parameterized transformation that captures the screen-surface gap?
2. Is the hue-dependent, non-uniform nature amenable to symbolic solution?
3. Can we extend to arbitrary RGB profiles (sRGB, P3, Adobe RGB, etc.)?
4. What is the theoretical basis for the observed biases?

### 11.8 Mathematical Formalism (Task #116 Complete)

**Document**: `writeups/methodology/COLOR_SPACE_TRANSFORMATIONS.md` (Section 10)

Key formalizations completed:
- **Profile-independent RGB definition**: Primaries, white point, transfer function
- **RGB↔XYZ matrix derivation**: Full algebraic derivation from primaries
- **Bradford chromatic adaptation**: Complete D65↔C transformation with numerical matrices
- **Screen-surface gap model**: Value/chroma/hue correction functions
- **Gamut intersection algorithms**: Forward-backward test, GJK method
- **Profile-independent API specification**: Proposed Rust API for MunsellSpace v1.4+

Open questions identified:
- Can Δh(H) be derived from first principles?
- Is the gap constant across illuminants?
- Does transformation have closed-form inverse?

**Task #119 Redirection**: Originally planned as Rust implementation in MunsellSpace crate, now redirected to **Python implementation** in research pipeline (`scripts/`). Rationale: The Rust crate contains pre-calculated polyhedra and sRGB support is sufficient; profile-independent transformations and screen-surface corrections are research-specific and belong in the Python data pipeline.

### 11.9 Gamut Comparison Visualization (Task #117 Complete)

**Script**: `scripts/visualize_gamut_comparison.py`
**Output**: `writeups/figures/gamut_comparison.{png,svg,pdf}`

Three-panel publication figure:
- **Panel A**: CIE 1931 xy chromaticity diagram with spectrum locus, sRGB/P3/Adobe RGB gamut triangles, D65 and Illuminant C white points
- **Panel B**: Munsell value slices (V=3, 5, 7) showing chroma limits vs approximated sRGB gamut boundaries
- **Panel C**: Screen-surface hue rotation wheel with per-family bias visualization and summary statistics

---

## 12. Literature Review: Gamut Mapping & Color Transformations (2026-01-04)

*Task #118: Deep dive into ingested Centore papers for mathematical foundations*

### 12.1 The Munsell-sRGB Conversion Chain

**Source**: ConversionsBetweenMunsellAndsRGBsystems.pdf, sRGBCentroidsForTheISCCNBSColourSystem.pdf, OpenSourceInverseRenotationArticle.pdf

The conversion between Munsell and sRGB follows a well-defined chain through CIE XYZ:

```
Munsell HVC → xyY (1943 Renotation) → XYZ → linear RGB → sRGB
sRGB → linear RGB → XYZ → xyY → Munsell HVC (Inverse Renotation)
```

**Key Centore Quotes:**

> "To convert from Munsell to sRGB, first use the Munsell renotation to find the corresponding CIE coordinates for that Munsell colour. Then use the sRGB standard to convert from those CIE coordinates to sRGB coordinates."

> "The sRGB standard defines sRGB colours by tristimulus coordinates, and the 1943 renotation defines the Munsell system by tristimulus coordinates, so Munsell coordinates can be calculated for sRGB coordinates, and vice versa."

**The Renotation Interpolation Method:**

Centore's algorithm uses a two-step approach for non-tabulated Munsell values:
1. **For integer Munsell Value**: Construct "ovoids" (constant chroma curves) and "radials" (constant hue lines) in xy chromaticity space, then interpolate
2. **For non-integer Value**: Interpolate between adjacent integer value planes

> "Curves of constant chroma [ovoids]... Curves of constant hue will be drawn by linear interpolation between data points of the same hue, but consecutive chromas."

**Renotation Data Structure:**
- 2,734 Munsell specifications with xyY coordinates
- Values 1-9 (integer), hues at 2.5, 5.0, 7.5, 10.0 prefixes
- Chromas in even steps from 2 to MacAdam limits
- Neutral point (grey): x = 0.31006, y = 0.31616 (Illuminant C)

### 12.2 The Illuminant C vs D65 Problem

**Source**: ConversionsBetweenMunsellAndsRGBsystems.pdf, sRGBCentroidsForTheISCCNBSColourSystem.pdf

A critical subtlety: **Munsell is defined under Illuminant C, but sRGB under D65**.

**Key Quotes:**

> "The Munsell renotation, however, was standardized on Illuminant C, so physical samples should be viewed under that illuminant."

> "In the sRGB standard, the CIE coordinates for triple [255, 255, 255] were chosen to match what a physical white patch would produce, when the ambient illumination is D65."

**Centore's Practical Solution:**

> "If those same sRGB values were viewed under D65, they would not match the colours seen under Illuminant C—but we finesse this situation, by substituting Illuminant C lighting for D65 lighting. Historically, Illuminant C was chosen as an average daylight chromaticity, so in practice it should be adequate to view the tables' sRGB specifications in a room lit solely with indirect daylight."

**Viewing Conditions for Valid Conversion:**
1. Diffuse Illuminant C lighting (or indirect daylight)
2. Intensity levels characteristic of indirect daylight
3. sRGB [255, 255, 255] has same chromaticity as D65

### 12.3 The Fundamental Surface vs Screen Distinction

**Source**: sRGBCentroidsForTheISCCNBSColourSystem.pdf, OptimalSpectraForDoubleObjectColourSolids.pdf

This is the core theoretical foundation for our screen-surface gap:

**Key Quotes:**

> "Colour translation from a monitor to the physical world is difficult because the sRGB system used for the screen applies to coloured **light sources**, while the ISCC-NBS or Munsell system used for the product applies to coloured **objects**."

> "The standard red-green-blue (sRGB) specification... applies only to light sources, and defines a display device's colour behavior in device-independent terms."

> "Surface colours are defined by their reflectance properties, which are independent of any light source. Light sources, such as traffic signals, can also be perceived directly by the human eye, without reflecting off any surfaces."

**The Physics:**
- **Surface color**: Light source → surface reflection → eye (subtractive)
- **Screen color**: Direct light emission → eye (additive)
- Screen monitors combine red, green, blue light of different intensities
- Objects reflect light according to wavelength-dependent reflectance spectra

### 12.4 Gamut Mismatch: The Irreducible Problem

**Source**: ConversionsBetweenMunsellAndsRGBsystems.pdf, sRGBCentroidsForTheISCCNBSColourSystem.pdf

**The Key Finding:**

> "Conversion is not always possible, however, because the sRGB gamut both extends beyond the MacAdam limits, and fails to fill all the volume inside the MacAdam limits."

**Specific Examples:**

> "For example, any sRGB triple of the form [0, 0, positive integer] is beyond the MacAdam limits." (Pure blues exceed surface color possibilities)

> "It lies outside the MacAdam limits, so it is in the sRGB gamut, but not in the Munsell gamut. Likewise, many Munsell colours, especially highly chromatic ones, cannot be produced on an sRGB monitor."

**Consequence:**

> "One consequence of this mismatch is that it is impossible to produce a complete exemplification of the Munsell system on an sRGB monitor; likewise, it is impossible to print a complete exemplification of all the colours of an sRGB monitor."

**Gamut Clipping:**

> "When the cells in the table are shaded grey, clipping was needed to produce the sRGB triple. In that case, the sRGB triple agrees with the standard, but will not match the Munsell colour."

### 12.5 MacAdam Limits and Optimal Colors

**Source**: FourTransition01FunctionsForReflectanceSpectra.pdf, AZonohedralApproachToOptimalColours.pdf, OptimalSpectraForDoubleObjectColourSolids.pdf

**The Optimal Colour Theorem (Schrödinger 1920, MacAdam 1935):**

> "The reflectance spectrum for an optimal colour must have **Schrödinger form**: it takes on only the values 0 and 1, with at most two transitions between those values."

**Physical Meaning:**
- Optimal colors are the theoretical boundary of the object-colour solid
- They represent maximum possible chroma for any given hue and value
- Real pigments/dyes fall short of these limits

**Schrödinger's Four Forms:**
1. All zeros (black)
2. All ones (ideal white)
3. One transition: 0→1 or 1→0 (passband or stopband)
4. Two transitions: 0→1→0 or 1→0→1 (bandpass or bandstop)

**Key Insight from Centore:**

> "For a fixed hue and value, the chromas extend from 0, corresponding to the grey of that value, to a maximum, called the MacAdam limit. A colour at a MacAdam limit is an optimal colour. The MacAdam limits are theoretical bounds; in practice, the Munsell system extends only as far as actual colorants allow, stopping well short of the MacAdam limits."

### 12.6 Chromatic Adaptation: Von Kries Transform

**Source**: TheTotalChromaticityDiagram.pdf

**Von Kries Model:**

> "In everyday life, chromatic adaptation insures that the prevailing illumination is perceived as a neutral, achromatic 'white.' As a side effect of neutralizing the illuminant, all colours are shifted somewhat."

**Mathematical Formulation:**
The von Kries transform scales LMS cone responses:
```
L' = k_L × L
M' = k_M × M
S' = k_S × S
```

Where k_L, k_M, k_S are chosen so the illuminant maps to D65 (neutral white).

**Key Insight:**

> "What we call *the* chromaticity diagram is really just *a* chromaticity diagram, that corresponds to a neutral state of adaptation. Every state of adaptation has its own chromaticity diagram."

> "By multiplying L, M, and S by various coefficients, the von Kries transform has, for practical purposes, changed the cone response functions, so that previously impossible colours can be produced."

**Implication for Our Work:**
Different viewing conditions (screen vs physical, ambient lighting) create different effective adaptation states, contributing to the observed biases.

### 12.7 Zonohedral Gamut Structure

**Source**: AZonohedralApproachToOptimalColours.pdf, ZonohedralGamutsForColourConstancy.pdf, NonMetamerismOfBoundaryColours.pdf

**Object-Colour Solids are Zonohedra:**

> "Geometrically, an object-colour solid is the zonohedron generated from the spectrum locus vectors for an illuminant."

**Zonohedron Properties:**
- Convex hull of 2^n vertices (n = number of spectral samples)
- Centrally symmetric
- Every face is a parallelogram (or higher-order zonogon)
- Optimal colors lie on the boundary

**Construction:**

> "A zonohedron has a vertex at the origin, when every α is 0, and its terminal vertex occurs when every α in Equation (24) is 1; the terminal vertex is simply the sum of all the generators."

**Unique Boundary Colors:**

> "By applying the methods of Theorem 1 to object-colour solids, and using the empirical finding that no three vectors in the spectrum locus are linearly dependent, it follows that there is a **unique** reflectance function for each optimal colour."

### 12.8 Implications for Screen-Surface Transformation

**Synthesis of Literature Findings:**

1. **The gap is fundamental**: Screen (emissive) and surface (reflective) colors are physically different phenomena. Even with identical XYZ coordinates, they won't appear identical.

2. **Illuminant matters**: Munsell→C, sRGB→D65. Chromatic adaptation creates perceptual shifts beyond simple colorimetric matching.

3. **Gamut mismatch is bidirectional**: Some screen colors exceed MacAdam limits (no Munsell equivalent), some Munsell colors exceed sRGB gamut (no screen equivalent).

4. **No closed-form Munsell formula**: The renotation is empirical data requiring interpolation. This limits purely symbolic approaches.

5. **Viewing conditions critical**: Centore's conversions assume specific ambient lighting (Illuminant C, indirect daylight levels). Real-world conditions vary.

**What the Literature Does NOT Address:**
- Quantitative models for the screen-surface appearance gap
- Correction functions beyond gamut clipping
- The perceptual mechanisms underlying our observed biases (+2.06 value, +0.80 chroma, hue rotation)

This gap in the literature validates our empirical calibration approach.

### 12.9 Key Papers Summary

| Paper | Key Contribution |
|-------|-----------------|
| ConversionsBetweenMunsellAndsRGBsystems | Conversion methodology, illuminant C/D65 finesse |
| sRGBCentroidsForTheISCCNBSColourSystem | Gamut mismatch, ISCC-NBS centroids |
| OpenSourceInverseRenotationArticle | Ovoid/radial interpolation algorithm |
| FourTransition01FunctionsForReflectanceSpectra | Optimal color theorem, Schrödinger form |
| AZonohedralApproachToOptimalColours | Zonohedral structure, MacAdam limits |
| TheTotalChromaticityDiagram | Von Kries, chromatic adaptation |
| NonMetamerismOfBoundaryColours | Unique boundary reflectances |
| OptimalSpectraForDoubleObjectColourSolids | Multi-illuminant optimal colors |
| srgb.pdf | sRGB standard specification |

### 12.10 Additional Findings from Comprehensive Literature Survey

#### Shadow Series in Munsell Space

**Source**: ShadowSeriesInTheMunsellSystem.pdf

A color's shadow series (how it appears as illumination decreases) forms approximately a straight line in Munsell space:

> "This paper calculates that a colour's shadow series is approximately a straight line in the Munsell system. The line starts at the colour's Munsell specification and ends about one value step below N0, on the neutral axis."

**Key finding**: As colors are seen in deeper shadow:
- Value decreases
- Chroma decreases proportionally
- Hue shifts slightly toward yellow

> "Though hues are approximately constant in a shadow series, the calculations do identify a slight, systematic tendency towards the yellow part of the spectrum as a colour is seen more deeply in shadow."

**Implication**: Shadow series linearity in Munsell validates the perceptual uniformity of the Munsell system.

#### Metamer Mismatch Bodies

**Source**: AnOpenSourceAlgorithmForMetamerMismatchBodies.pdf

When the same object is imaged under different illuminants or by different devices, metameric colors can produce different outputs:

> "A metamer mismatch occurs when two colours are identical in one image, but different in the other image."

**Types of metamer mismatching:**
- **Illuminant-induced**: Same sensor, different illuminants
- **Observer-induced**: Different sensors, same illuminant
- **Combined**: Different sensors and illuminants

> "Metamer mismatching results when two reflectance spectra x and y are metameric under Φ, i.e. they give the same colour signal under Φ, but give different colour signals under Ψ"

**Relevance to screen-surface gap**: Screen RGB values that appear identical could map to different Munsell colors depending on assumptions about the reflectance spectrum.

#### Spectrophotometric Measurement Accuracy

**Source**: CoefficientOfVariationInSpectrophotometry.pdf, CommentsOnJoensuuData.pdf

Measurement accuracy varies significantly with reflectance level:

> "The most important result is the dramatically increased variability of spectrophotometric measurements when reflectance is low, less than about 5%."

**Munsell chip accuracy** (Joensuu measurements vs 1943 renotation):
- Median ΔE₀₀ accuracy: ~1.6
- No consistent bias in hue, value, or chroma
- Some variation between spectrophotometers (Perkin-Elmer vs AOTF)

**Implication**: Dark colors (low value) have inherently higher measurement uncertainty.

#### GJK Algorithm for Color Problems

**Source**: GJKinConstrainedLeastSquares.pdf, EnforcingKubelkaMunkConstraintsForOpaquePaints.pdf

The Gilbert-Johnson-Keerthi algorithm efficiently finds the minimum distance between convex polytopes:

> "The GJK algorithm is a fast, iterative method that finds the minimum distance between two convex polytopes."

**Applications in color science:**
- Finding nearest in-gamut color
- Kubelka-Munk paint mixing optimization
- Constrained least-squares color matching

This algorithm could be useful for our gamut clipping and boundary detection work.

#### Color Constancy and Illuminant Estimation

**Source**: ZonohedralGamutsForColourConstancy.pdf

Forsyth's gamut-based illuminant estimation (GBIE) uses the zonohedral structure of illuminant gamuts:

> "Illuminant gamuts are zonohedra, and they are generated by the device's spectrum locus vectors, which are the RGB outputs for monochromatic reflectance spectra."

**Key insight**: One illuminant gamut is almost never a linear transformation of another:

> "A linear image of one illuminant gamut is almost never another illuminant gamut."

This validates that screen-surface transformation cannot be a simple linear/affine operation.

#### Geometric Invariants Under Illuminant Changes

**Source**: GeometricInvariantsUnderIlluminantTransformations.pdf

Some properties remain constant regardless of illuminant:

> "Despite these changes, some properties are invariant under illuminant transformations."

**Invariants:**
- Spectrum cone shape
- Optimal reflectance functions (Schrödinger form)
- Relationships between spectrum locus vectors (directions, not magnitudes)

> "The ith spectrum locus vectors, for any two nowhere-zero illuminants, differ only in magnitude."

---

## 13. Active Reference List for Paper Citation

### Primary Sources (Directly Cited)

1. **Centore, P. (2020)**. Beige, aqua, fuchsia, etc.: Definitions for some non-basic surface colour names. *Journal of the International Colour Association*, 25, 24-54.
   - **Local file**: `jaic_v25_03.pdf`
   - **Use for**: Non-basic color definitions, CAUS data, polyhedra methodology

2. **Centore, P. (2012)**. An Open-Source Inversion Algorithm for the Munsell Renotation. *Color Research & Application*, 37(6), 455-464.
   - **Local file**: `OpenSourceInverseRenotationArticle.pdf`
   - **Use for**: Munsell↔XYZ conversion, ovoid/radial interpolation

3. **Centore, P. (2014)**. Conversions Between the Munsell and sRGB Colour Systems. *Color Research & Application*.
   - **Local file**: `ConversionsBetweenMunsellAndsRGBsystems.pdf`
   - **Use for**: sRGB-Munsell conversion, illuminant C vs D65, gamut mismatch

4. **Centore, P. (2016)**. sRGB Centroids for the ISCC-NBS Colour System. *Color Research & Application*.
   - **Local file**: `sRGBCentroidsForTheISCCNBSColourSystem.pdf`
   - **Use for**: Surface vs light source distinction, ISCC-NBS centroids

5. **Centore, P. (2012)**. A Zonohedral Approach to Optimal Colours. *Color Research & Application*.
   - **Local file**: `AZonohedralApproachToOptimalColours.pdf`
   - **Use for**: MacAdam limits, object-color solid structure

6. **Centore, P. (2020)**. The Total Chromaticity Diagram. *Color Research & Application*.
   - **Local file**: `TheTotalChromaticityDiagram.pdf`
   - **Use for**: Von Kries transforms, chromatic adaptation

7. **IEC 61966-2-1:1999**. Multimedia systems and equipment - Colour measurement and management - Part 2-1: Colour management - Default RGB colour space - sRGB.
   - **Local file**: `srgb.pdf`
   - **Use for**: sRGB standard specification

### Secondary Sources (Background/Methods)

8. **Centore, P. (2011)**. Shadow Series in the Munsell System. *Color Research & Application*.
   - **Local file**: `ShadowSeriesInTheMunsellSystem.pdf`

9. **Centore, P. (2017)**. An Open-Source Algorithm for Metamer Mismatch Bodies. *Color Research & Application*.
   - **Local file**: `AnOpenSourceAlgorithmForMetamerMismatchBodies.pdf`

10. **Centore, P. (2016)**. Zonohedral Gamuts For Colour Constancy. *Color Research & Application*.
    - **Local file**: `ZonohedralGamutsForColourConstancy.pdf`

11. **Centore, P. (2012)**. Geometric Invariants Under Illuminant Transformations. *Color Research & Application*.
    - **Local file**: `GeometricInvariantsUnderIlluminantTransformations.pdf`

12. **Centore, P. (2018)**. Four-Transition 0-1 Functions for Reflectance Spectra.
    - **Local file**: `FourTransition01FunctionsForReflectanceSpectra.pdf`

13. **Centore, P. (2013)**. Comments on the University of Joensuu's Matte Munsell Measurements.
    - **Local file**: `CommentsOnJoensuuData.pdf`

14. **Centore, P.** Coefficient of Variation in Spectrophotometry.
    - **Local file**: `CoefficientOfVariationInSpectrophotometry.pdf`

15. **Centore, P. (2016)**. Enforcing Kubelka-Munk Constraints for Opaque Paints.
    - **Local file**: `EnforcingKubelkaMunkConstraintsForOpaquePaints.pdf`

16. **Centore, P.** A GJK-Based Algorithm for Constrained Least Squares.
    - **Local file**: `GJKinConstrainedLeastSquares.pdf`

17. **Lay, S. R. (2007)**. *Convex Sets and Their Applications*. Dover Publications.
    - **Local file**: `convex-sets-and-their-applications.pdf`
    - **Use for**: Mathematical foundations of convex set theory

### Classic References (from papers)

18. **Newhall, S. M., Nickerson, D., & Judd, D. B. (1943)**. Final report of the O.S.A. subcommittee on the spacing of the Munsell colors. *Journal of the Optical Society of America*, 33(7), 385-418.
    - **The 1943 Munsell Renotation**

19. **Berlin, B., & Kay, P. (1969/1999)**. *Basic Color Terms: Their Universality and Evolution*. CSLI Publications.
    - **Basic color term theory**

20. **Schrödinger, E. (1920)**. Theorie der Pigmente von größter Leuchtkraft. *Annalen der Physik*, 367(15), 603-622.
    - **Optimal color theorem**

21. **MacAdam, D. L. (1935)**. The theory of the maximum visual efficiency of colored materials. *Journal of the Optical Society of America*, 25(8), 249-252.
    - **MacAdam limits**

---

## Changelog

| Date | Update |
|------|--------|
| 2026-01-04 | **Profile-independent conversions (Task #119)**: Python modules `rgb_profiles.py` and `calibrated_conversions.py` with multi-profile RGB-Munsell conversions, screen-surface calibration, gamut detection; 38 unit tests |
| 2026-01-04 | **Gamut visualization (Task #117)**: Three-panel figure (chromaticity, Munsell slices, calibration wheel) in PNG/SVG/PDF |
| 2026-01-04 | **Mathematical formalism (Task #116)**: Complete transformation chain RGB↔XYZ↔Munsell, Bradford adaptation, screen-surface gap model, profile-independent API spec |
| 2026-01-04 | **Comprehensive literature review**: Added shadow series, metamer mismatch, spectrophotometer accuracy, GJK algorithm, color constancy, geometric invariants; created active reference list for citations |
| 2026-01-04 | **Literature review**: Deep dive into Centore papers - conversion methodology, gamut mismatch, optimal colors, chromatic adaptation |
| 2026-01-04 | **Color space transformation analysis**: Screen-surface gap, mathematical framework, gamut relationships |
| 2026-01-01 | **Overlay taxonomy**: Domain categorizations (Jewels, Metals, Earth, Flora) and superposition theory |
| 2026-01-01 | **Inconsistency analysis**: 73 overlays vs 30 polyhedra, documented gaps |
| 2026-01-01 | **Inference pipeline complete**: Hybrid rule+ML approach, 100% super-family accuracy |
| 2026-01-01 | Non-basic color eval: Centore 30 + new candidates tested |
| 2026-01-01 | **Full classification**: 184K color names assigned to 16 families |
| 2026-01-01 | Anchor evaluation: 16 core families optimal (29 ISCC-NBS too granular) |
| 2026-01-01 | **Arena complete**: D_TwoTower wins with 46.9% family accuracy |
| 2025-12-30 | Created master research notes document |
| 2025-12-30 | Arena training launched (4 architectures) |
| 2025-12-30 | SBERT baseline experiment completed |
| 2025-12-30 | Academic datasets downloaded (Jonauskaite, Free Assoc) |
| 2025-12-30 | 66,307 training pairs preprocessed |
| 2025-12-29 | Wikipedia color harvest complete (1,062 articles) |
| 2025-12-28 | Clustering validation complete (SBERT best at 57.6% purity) |
| 2025-12-25 | Project goals clarified |

---

*Last updated: 2026-01-04*
