# Semantic Color Name Processing: Research Summary

## 1. Problem Reframing

The previous investigation failed because it treated color name normalization as a
pure string matching problem, ignoring semantics. This led to nonsensical mappings:
- "bluish fuchsia" → "bluish green" (color semantics completely lost)
- "fedex purple" → "faded purple" (brand name treated as typo)
- "#0000FF" → "pastel blue" (hex code matched by edit distance)

### The Real Problem

Color names exist in a **semantic field** with multiple valid forms:
1. **Descriptive**: "light blue", "dark green", "pale yellow"
2. **Similarity/Metaphor**: "sky blue", "grass green", "lemon yellow"
3. **Artistic/Brand**: "Fedex purple", "Tiffany blue", "Klein blue"
4. **Combinations**: "dusty rose", "burnt sienna", "robin's egg blue"

**Core Requirements:**
1. A valid color name must be **linkable to at least one color concept**
2. We keep original coordinates - validation only filters, doesn't replace
3. Simple preprocessing (special chars, obvious typos) is orthogonal

## 2. Literature Review

### 2.1 Grounded Color Semantics (Stanford NLP)

**Source**: [Monroe et al., "Colors in Context" (2017)](https://ar5iv.labs.arxiv.org/html/1703.10186)

**Key Methodology:**
- LSTM encoder maps color descriptions to Gaussian distributions over color space
- Uses Fourier-transformed RGB representation
- Handles compositional descriptions ("light greenish blue")
- Pragmatic reasoning combines speaker/listener models

**Applicability**: Their architecture maps text → color coordinates. We need the
inverse validation: does this text have color semantics at all?

### 2.2 Sentence Embeddings for Semantic Similarity

**Source**: [Sentence-BERT (Reimers & Gurevych, 2019)](https://arxiv.org/abs/1908.10084)

**Key Methodology:**
- Siamese BERT networks produce sentence embeddings
- Embeddings can be compared via cosine similarity
- 10,000+ pretrained models available on HuggingFace
- Fast similarity computation (5 seconds vs 65 hours for BERT pairs)

**Applicability**:
- Cluster similar color names (grey/gray, light blue/pale blue)
- Compare against known color vocabulary to detect color meaning
- "forest green" and "dark green" will have similar embeddings

### 2.3 Autoencoders for Text Normalization

**Source**: [Denoising Seq2Seq for Spelling (IEEE 2019)](https://ieeexplore.ieee.org/document/8934902/)

**Key Methodology:**
- Encoder compresses noisy input to latent representation
- Decoder reconstructs clean output
- Trained on (noisy, clean) pairs
- High reconstruction loss indicates out-of-vocabulary/noise

**Applicability**:
- Train on known color vocabulary
- Names with high reconstruction loss may lack color semantics
- Can learn to normalize variants to canonical forms

### 2.4 Deep Ensemble Spelling Correction

**Source**: [Robust Automated Spelling Correction (ACM 2024)](https://dl.acm.org/doi/fullHtml/10.1145/3665065.3665070)

**Key Methodology:**
- Ensemble of LSTM models for uncertainty estimation
- Addresses "uncertain predictions where correct words are regenerated incorrectly"
- Combines character-level and context-level features

**Applicability**:
- More robust than single-model approaches
- Can quantify confidence in corrections

## 3. Proposed Experiments

### Experiment 1: SBERT Semantic Clustering

**Hypothesis**: Color names with similar meanings will cluster together in
SBERT embedding space. Names without color meaning will be distant from color clusters.

**Method**:
1. Embed all XKCD color names using SBERT (all-MiniLM-L6-v2)
2. Embed known color vocabulary (basic colors + modifiers)
3. For each XKCD name, compute max similarity to known color terms
4. Names below threshold likely lack color semantics

**Metrics**:
- Similarity distribution analysis
- Precision/recall on manually labeled test set
- Clustering quality (silhouette score)

### Experiment 2: Color Word Detection via BERT

**Hypothesis**: BERT tokenization will reveal whether a name contains
color-related tokens, even with spelling variations.

**Method**:
1. Tokenize all names with BERT tokenizer
2. Build color token vocabulary from training set
3. Score names by presence of color tokens
4. Compare with character-level edit distance

**Metrics**:
- Token overlap with color vocabulary
- Robustness to spelling variations (gray/grey same token?)

### Experiment 3: Semantic Autoencoder

**Hypothesis**: An autoencoder trained on color vocabulary will have high
reconstruction loss for non-color terms.

**Method**:
1. Build training set from known color names
2. Train seq2seq autoencoder (encoder: text → latent, decoder: latent → text)
3. Measure reconstruction loss on XKCD names
4. High loss = likely not a valid color name

**Variants**:
- Character-level vs word-level
- With/without SBERT embeddings as input

### Experiment 4: Hybrid Approach

**Hypothesis**: Combining semantic similarity + autoencoder provides better
filtering than either alone.

**Method**:
1. Compute SBERT similarity score (Exp 1)
2. Compute autoencoder reconstruction loss (Exp 3)
3. Combine scores (weighted, learned, or voting)
4. Compare against individual methods

### Experiment 5: Spelling-First Variant

**Hypothesis**: Light preprocessing before semantic analysis improves results.

**Method**:
1. Strip special characters (!!!, #, @)
2. Normalize whitespace and case
3. Apply lightweight spell correction (hunspell/aspell)
4. Run Experiments 1-4 on cleaned names
5. Compare results

## 4. Evaluation Framework

### Ground Truth
- **Positive**: Names from Centore dataset (spectrophotometer validated)
- **Negative**: Random English words, numbers, spam patterns

### Test Cases (Manually Curated)
| Name | Expected | Rationale |
|------|----------|-----------|
| "light blue" | Valid | Descriptive color |
| "sky blue" | Valid | Metaphorical color |
| "fedex purple" | Valid | Brand color (has purple) |
| "forest green" | Valid | Metaphorical color |
| "john" | Invalid | Person name, no color |
| "!!!green" | Valid→green | Noise prefix, color present |
| "#0000FF" | Valid→blue | Hex code, decodable |
| "asdfgh" | Invalid | Random characters |
| "bluish fuchsia" | Valid | Compound color |

### Metrics
- **Precision**: % of accepted names that are valid colors
- **Recall**: % of valid colors that are accepted
- **F1**: Harmonic mean
- **Manual Review**: Spot-check unexpected classifications

## 5. Implementation Plan

### Phase A: Setup and Small-Scale Testing
1. Install dependencies (sentence-transformers, transformers, torch)
2. Create test set (100 known valid, 100 known invalid)
3. Implement each experiment as standalone script
4. Validate on test set before full-scale run

### Phase B: Full-Scale Experiments
1. Run each experiment on full XKCD dataset (175K names)
2. Collect metrics and timing
3. Save intermediate results for analysis

### Phase C: Analysis and Synthesis
1. Compare experiment results
2. Identify best approach or combination
3. Build production pipeline

## 6. References

1. Monroe, W., et al. (2017). "Colors in Context: A Pragmatic Neural Model for
   Grounded Language Understanding." arXiv:1703.10186.

2. Reimers, N., & Gurevych, I. (2019). "Sentence-BERT: Sentence Embeddings using
   Siamese BERT-Networks." arXiv:1908.10084.

3. Stanford NLP. (2016). "Learning to Generate Compositional Color Descriptions."

4. ACM. (2024). "Robust Automated Spelling Correction with Deep Ensembles."

5. Bhargava, D. (2018). "Grounded Learning of Color Semantics with Autoencoders."
   Stanford CS224N.

---

*Research conducted: 2025-12-23*
