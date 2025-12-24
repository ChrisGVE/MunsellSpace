# What Didn't Work: Failed Approaches and Lessons Learned

This document chronicles approaches that were attempted but ultimately failed or
proved insufficient. Understanding these failures informed the successful approach.

## 1. String Matching for Color Name Normalization

### Approach
Initial investigation (Phase 2) used edit distance and phonetic matching
(Soundex, Metaphone) to normalize color names.

### The Problem
String matching ignores color semantics entirely:

| Input | String Match Output | Correct Handling |
|-------|---------------------|------------------|
| "bluish fuchsia" | "bluish green" | Keep as-is (valid compound) |
| "fedex purple" | "faded purple" | Keep as-is (brand color) |
| "#0000FF" | "pastel blue" | Decode to blue RGB |

### Why It Failed
- Edit distance matched "fuchsia" to "green" (both 6 letters, similar structure)
- Brand names were treated as misspellings
- Hex codes were matched to phonetically similar words

### Lesson Learned
**Color name validation requires semantic understanding, not string similarity.**

### Evidence
- Git commit: `aad5422` - "Reset investigation approach to use semantic NLP methods"
- File: `semantic-investigation/research_summary.md` lines 1-9

---

## 2. Sample Count Filtering (n ≥ 10 or n ≥ 100)

### Approach
Filter out XKCD color names with low sample counts, assuming low-count names
are noise or one-off entries.

### The Problem
This was far too conservative:

| Threshold | Names Retained | Names Discarded | Response Coverage |
|-----------|---------------|-----------------|-------------------|
| n ≥ 100 | 1,369 | 174,475 (99.2%) | ~40% |
| n ≥ 10 | 7,339 | 168,505 (95.8%) | 92.3% |
| n ≥ 1 | 145,042 | 30,802 (17.5%) | 98.3% |

### Why It Failed
- Unique, valid color descriptions often have n=1 (e.g., "dusty lavender mist")
- Semantic validation (SBERT similarity ≥ 0.35) is sufficient to filter noise
- Sample count correlates weakly with validity

### Validation Analysis
Names that passed semantic validation by sample count:

| Sample Count | Semantic Pass Rate |
|--------------|-------------------|
| n = 1 | 79.7% (108K names) |
| n = 2-10 | 91.6% |
| n > 10 | 94-100% |

### Lesson Learned
**Semantic validity is orthogonal to frequency. Low-count names can be valid;
high-count names can be spam if many users entered the same nonsense.**

### Evidence
- Git commit: `c381522` - "feat(validation): remove sample count filter, 20x more validated names"
- Before: 7,339 names; After: 145,042 names

---

## 3. Character-Level Autoencoder

### Approach (Experiment 3)
Train a character-level autoencoder on known color vocabulary. Names with high
reconstruction loss would indicate non-color terms.

### The Problem
The autoencoder failed catastrophically on non-ASCII characters:

| Input | Reconstruction Loss | Expected |
|-------|---------------------|----------|
| "red" | 0.023 | Low (valid) |
| "asdfgh" | 0.891 | High (invalid) |
| "синий" (Russian "blue") | 0.000 | High (invalid) |
| "海老茶" (Japanese color) | 0.000 | High (invalid) |

### Why It Failed
- Character vocabulary was ASCII-only
- Non-ASCII characters were mapped to UNK token
- Reconstruction of UNK→UNK has zero loss
- Result: All non-ASCII names scored as "valid"

### F1 Score
- Overall: 0.845
- On ASCII names: 0.92
- On non-ASCII names: 0.00

### Lesson Learned
**Character-level models trained on English vocabulary cannot validate
international color names. Need multilingual semantic approach.**

### Evidence
- File: `semantic-investigation/exp3_autoencoder_output.log`
- Git commit: `e263651` - notes "Autoencoder fails on non-ASCII (gives 0 loss for Cyrillic)"

---

## 4. BERT Token Overlap

### Approach (Experiment 2)
Use BERT tokenizer to check if color names contain color-related tokens.
Compare token overlap with known color vocabulary.

### The Problem
BERT tokenization fails on spelling variants:

| Name | BERT Tokens | Issue |
|------|-------------|-------|
| "gray" | ["gray"] | OK |
| "grey" | ["grey"] | Different token! |
| "colour" | ["colour"] | Different from "color" |
| "lightblue" | ["light", "##blue"] | Subword split |

### Why It Failed
- BERT treats "gray" and "grey" as completely different tokens
- No semantic similarity between spelling variants at token level
- Compound words split unpredictably

### F1 Score
- On canonical spellings: 1.0
- On spelling variants: 0.72
- On compounds: 0.85

### Lesson Learned
**Token-level matching cannot handle the orthographic diversity of color names.
Need embedding-level semantic similarity.**

### Evidence
- File: `semantic-investigation/exp2_bert_tokens_output.log`
- Git commit: `e263651` - notes "BERT tokenization fails on spelling variants (gray≠grey)"

---

## 5. Linear Hue Correction

### Approach
Apply a constant hue offset to correct systematic bias between XKCD screen
colors and Centore physical colors.

### Initial Finding (Phase 4, HSV Approximation)
```
Mean hue bias: -19.3° (XKCD appears bluer)
Proposed correction: hue_corrected = hue + 19.3°
```

### The Problem (Stage 4, Proper Munsell)
After proper Munsell conversion and category-based analysis, we found:

| Category | Hue Shift | Direction |
|----------|-----------|-----------|
| teal | -41.1° | Cooler |
| turquoise | -39.9° | Cooler |
| aqua | -24.7° | Cooler |
| white | +38.2° | Warmer |
| beige | +33.3° | Warmer |
| taupe | +31.2° | Warmer |
| red | +3.2° | Accurate |
| blue | -9.2° | Accurate |

### Why Linear Fails
- Cool colors (teal, aqua, turquoise) shift **toward blue** (-25° to -41°)
- Warm earth tones (beige, tan, sand) shift **toward yellow** (+25° to +38°)
- Core primaries (red, blue, purple) are relatively **accurate** (±10°)

A single offset cannot correct shifts in opposite directions!

### The Non-Linearity
The hue correction function must be:
```
Δhue = f(hue, value, chroma)
```
Where f is non-linear and hue-dependent.

### Lesson Learned
**Screen-to-physical color mapping requires non-linear, hue-dependent
correction. The bias varies across color space in a complex way.**

### Evidence
- Git commit: `2c60d85` - Initial Stage 4 findings (erroneous due to scale bug)
- Git commit: `d96e062` - Corrected Stage 4 with proper hue scale
- Aggregate stats show mean hue shift near zero but ±36° standard deviation

---

## 6. Color Wheel Consistency Filtering

### Approach
Filter out colors where the name semantics don't match the RGB hue position.
For example, filter "blue" names that have cyan hue (180° instead of 240°).

### The Problem
This conflates two different issues:
1. Invalid color names (actual noise)
2. Systematic perception differences (screen vs physical)

### Why We Stopped
The user correctly identified that filtering on color wheel consistency would
remove the very data needed to detect and correct screen-to-physical biases.

**XKCD colors are screen colors** - they may systematically differ from
theoretical color wheel positions because:
- Monitors have different color temperatures
- sRGB gamut differs from physical pigment gamut
- Perception of self-luminous vs reflected colors differs

### Current Approach
Color wheel consistency is now **annotation-only**, not a filter. The
consistency flags are preserved for analysis but all colors proceed to
Munsell conversion and Centore comparison.

### Lesson Learned
**Don't discard data that reveals systematic biases. Annotate for analysis,
but retain for calibration research.**

### Evidence
- File: `DATA_PIPELINE_RATIONALE.md`
- Git commit: `88ebf7a` - Documents "Color wheel consistency is annotation-only (no filtering)"

---

## Summary: The Learning Curve

| Iteration | Approach | Failure Mode | Improved Approach |
|-----------|----------|--------------|-------------------|
| 1 | String matching | Semantic loss | SBERT similarity |
| 2 | High sample threshold | Over-filtering | Semantic validation only |
| 3 | Autoencoder | Non-ASCII failure | SBERT (multilingual) |
| 4 | BERT tokens | Spelling variant failure | SBERT embeddings |
| 5 | Linear hue correction | Non-uniform bias | (Next: Non-linear model) |
| 6 | Color wheel filtering | Bias data loss | Annotation-only |

## Implications for Future Work

The pattern of failures suggests:

1. **Semantic approaches outperform syntactic** - Use meaning, not characters
2. **Preserve data for analysis** - Don't filter what you need to study
3. **Expect non-linearity** - Color perception is complex
4. **Test on edge cases** - Non-ASCII, spelling variants, compounds

The next stage (non-linear modeling) should:
- Model hue correction as a function of position in color space
- Consider piecewise, polynomial, or neural approaches
- Validate on held-out Centore categories
