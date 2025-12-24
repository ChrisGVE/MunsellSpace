# Introduction

## The Challenge of Semantic Color Overlays

Color is both a physical phenomenon and a perceptual experience. When we name
colors, we bridge these domains: physical light spectra become semantic
categories like "teal" or "dusty rose." This mapping is not straightforward,
and it becomes even more complex when the colors we name exist only on screens.

This research addresses a fundamental question: **How do crowdsourced screen
color names map to physical color references, and what systematic biases exist
between screen-based and physical color perception?**

---

## Background

### The Rise of Digital Color

Most color interaction today happens on screens. We choose paint colors from
websites, purchase clothing from online catalogs, and communicate color
preferences through digital images. Yet our color vocabulary evolved for
physical objects: the sky, earth, plants, and dyed fabrics.

When someone names a color on a computer screen, they apply physical-world
vocabulary to a fundamentally different phenomenon:

| Aspect | Physical Color | Screen Color |
|--------|----------------|--------------|
| Light source | Reflected (illuminated by ambient) | Emitted (self-luminous) |
| Color space | Continuous spectrum | Discrete RGB primaries |
| Gamut | Physical pigment limits | sRGB display limits |
| Viewing | Adapted to environment | Often dark-adapted |

### Semantic Color Overlays

A **semantic color overlay** is a mapping from human color terms to regions in
a color space. The goal is to answer: "What colors do humans call 'teal'?"

This has applications in:
- **Color search**: Find images by color name
- **Design tools**: Suggest named color palettes
- **Accessibility**: Describe colors for vision-impaired users
- **Cross-cultural color communication**: Standardize color terms

### The Problem

Creating semantic overlays requires color naming data. The largest available
dataset - the XKCD Color Survey - contains 175,844 color names from web users.
However, these are **screen colors**: RGB values displayed on uncalibrated
monitors under uncontrolled viewing conditions.

To use this data for physical color applications (paint matching, textile
selection, print production), we must understand and correct the biases
between screen and physical color perception.

---

## Research Questions

This research addresses three questions:

### RQ1: Data Quality

How much of the crowdsourced color naming data is semantically valid?

The XKCD survey allowed freeform text entry, producing names like:
- Valid: "dusty rose", "ocean blue", "forest green"
- Invalid: "asdfgh", "my ex's favorite color", profanity

**Approach**: Semantic validation using sentence embeddings (SBERT)

### RQ2: Bias Quantification

What are the systematic biases between screen colors and physical color
references?

Comparing XKCD screen colors to Centore spectrophotometer-measured physical
samples should reveal how screen perception differs from physical reality.

**Approach**: Convert screen colors to Munsell space; compare to physical
reference centroids

### RQ3: Correction Modeling

Can we develop a correction model to map screen colors to physical equivalents?

If biases are systematic (not random), they should be predictable and
correctable.

**Approach**: Analyze bias patterns; develop correction model

---

## Two Data Sources

### XKCD Color Survey (Screen Colors)

In 2010, Randall Munroe conducted a large-scale color naming experiment:
- 175,844 unique color names
- ~3.4 million survey responses
- Freeform text entry
- Colors displayed on participants' own monitors

This is the largest publicly available color naming dataset, but it represents
**screen color perception**, not physical color matching.

### Centore Polyhedron Data (Physical Colors)

Paul Centore's "Real Colour Wheel" project provides:
- 30 color categories (red, blue, teal, beige, etc.)
- Spectrophotometer-measured physical samples
- Coordinates in Munsell color space
- Polygon boundaries defining category regions

This is our **ground truth** for physical color categories.

---

## Contributions

This research makes the following contributions:

### 1. Semantic Validation Pipeline

A methodology for filtering crowdsourced color names using sentence embeddings,
retaining 78.4% of names as semantically valid.

### 2. Screen-to-Physical Bias Quantification

Systematic measurement of how screen colors differ from physical references:
- Value bias: +0.81 (screen colors appear lighter)
- Chroma bias: +3.82 (screen colors appear more saturated)
- Hue bias: Non-uniform, category-dependent (±36° variation)

### 3. Key Finding: Non-Linear Hue Bias

The central discovery: **hue bias cannot be corrected with a linear model**.
Cool colors (teal, turquoise) shift toward blue; warm colors (beige, tan)
shift toward yellow. These opposite shifts require non-linear modeling.

### 4. Foundation for Non-Linear Correction

Framework and proposals for non-linear hue correction modeling, enabling
future work to build accurate screen-to-physical color transformations.

---

## Roadmap

The remainder of this article is organized as follows:

- **Section 2: Related Work** - Prior color naming studies and methods
- **Section 3: Data Sources** - Detailed description of XKCD and Centore data
- **Section 4: Methodology** - Four-stage pipeline for bias detection
- **Section 5: What Didn't Work** - Failed approaches and lessons learned
- **Section 6: Results** - Quantitative findings from each pipeline stage
- **Section 7: Key Findings** - Universal and non-uniform biases
- **Section 8: Discussion** - Why linear correction fails
- **Section 9: Future Work** - Non-linear modeling proposals
- **Section 10: Conclusion** - Summary and implications

