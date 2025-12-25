# Active References: Actually Used in Research

This document lists only the references actively cited and used in the MunsellSpace color research project.

---

## Primary Methodology

### Centore, Paul (2020)
**Title**: "Beige, aqua, fuchsia, etc.: Definitions for some non-basic surface colour names"

**Journal**: Journal of the International Colour Association (JAIC)

**Details**: Volume 25, pp. 24-54

**URL**: https://www.munsellcolourscienceforpainters.com/ColourSciencePapers/BeigeAquaFuchsiaEtc.pdf

**Usage in project**:
- Primary methodology for inner convex hull polyhedron construction
- Reference dataset: 9,261 CAUS fabric samples, 30 color categories
- Outlier removal algorithm (single-layer vertex removal)
- Centroid calculation methodology
- Reference centroids for bias detection (Phase 4)

**Key equations used**:
- Munsell to Cartesian: x = C·cos(H·π/50), y = C·sin(H·π/50), z = V
- Convex hull vertex removal for outlier detection
- Filled-solid centroid calculation (equations 6-8)

**Cited in**:
- Phase 6: Convex Hull Construction
- Phase 4: Calibration Analysis
- POLYHEDRON_METHODOLOGY.md

**BibTeX**:
```bibtex
@article{centore2020beige,
  title={Beige, aqua, fuchsia, etc.: Definitions for some non-basic surface colour names},
  author={Centore, Paul},
  journal={Journal of the International Colour Association},
  volume={25},
  pages={24--54},
  year={2020},
  url={https://www.munsellcolourscienceforpainters.com/ColourSciencePapers/BeigeAquaFuchsiaEtc.pdf}
}
```

---

## Primary Dataset

### Munroe, Randall (2010)
**Title**: "XKCD Color Survey Results"

**Published**: XKCD Blog, May 3, 2010

**URL**: https://blog.xkcd.com/2010/05/03/color-survey-results/

**Dataset download**: https://xkcd.com/color/rgb.txt

**Dataset size**:
- 3.4 million color naming responses
- 175,844 unique color names
- 954 most common colors in public dataset

**Usage in project**:
- Primary crowdsourced dataset (Phase 1)
- Source for all screen color data
- Semantic validation input (Phase 2)
- RGB to Munsell conversion input (Phase 3)

**Characteristics**:
- Screen colors (RGB, uncalibrated monitors)
- Freeform naming (crowd-sourced)
- Long-tail distribution (common colors have 10,000+ samples)

**Cited in**:
- Phase 1: Data Collection
- Phase 2: Entity Matching
- DATA_PIPELINE_RATIONALE.md

**BibTeX**:
```bibtex
@misc{munroe2010xkcd,
  title={XKCD Color Survey Results},
  author={Munroe, Randall},
  year={2010},
  month={May},
  howpublished={XKCD Blog},
  url={https://blog.xkcd.com/2010/05/03/color-survey-results/}
}
```

---

## Supporting Theory

### Lay, Steven R. (2007)
**Title**: "Convex Sets and Their Applications"

**Publisher**: Dover Publications, Mineola, NY

**ISBN**: 978-0486458038

**Usage in project**:
- Mathematical foundation for minimal generating sets
- Definition: "Points a rubber band would touch if stretched around all points in 2D"
- Convex hull vertex theory

**Referenced by**: Centore (2020) as citation [4]

**Cited in**:
- POLYHEDRON_METHODOLOGY.md
- Phase 6 documentation

**BibTeX**:
```bibtex
@book{lay2007convex,
  title={Convex Sets and Their Applications},
  author={Lay, Steven R.},
  year={2007},
  publisher={Dover Publications},
  address={Mineola, NY},
  isbn={978-0486458038}
}
```

---

## Computational Methods

### Reimers, Nils and Gurevych, Iryna (2019)
**Title**: "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks"

**Conference**: EMNLP-IJCNLP 2019

**URL**: https://arxiv.org/abs/1908.10084

**Code**: https://github.com/UKPLab/sentence-transformers

**Model used**: `all-MiniLM-L6-v2`

**Usage in project**:
- Core methodology for semantic validation (Phase 2.1)
- Computes semantic similarity between XKCD names and reference vocabulary
- Threshold: 0.35 cosine similarity
- Validated 137,878 / 175,844 XKCD names (78.4%)

**Implementation**:
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
similarity = cosine_similarity(
    model.encode(xkcd_name),
    model.encode(reference_color)
)
```

**Cited in**:
- Phase 2: Entity Matching & Normalization
- `full_scale_validation.py`

**BibTeX**:
```bibtex
@inproceedings{reimers2019sentencebert,
  title={Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks},
  author={Reimers, Nils and Gurevych, Iryna},
  booktitle={Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)},
  year={2019},
  url={https://arxiv.org/abs/1908.10084}
}
```

---

### Fisher, Nicholas I. (1993)
**Title**: "Statistical Analysis of Circular Data"

**Publisher**: Cambridge University Press

**ISBN**: 978-0521568906

**Usage in project**:
- Circular statistics for hue analysis (hue is angular: 0° = 360°)
- Circular mean calculation for hue averaging
- Circular difference for bias computation
- Essential for Phase 4 (Centore comparison) and Phase 7 (Fourier model)

**Key formulas used**:

**Circular mean**:
```
mean_hue = atan2(Σsin(θᵢ), Σcos(θᵢ))
```

**Circular standard deviation**:
```
σ_circular = √(-2 ln(R))  where R = |Σe^(iθ)| / n
```

**Cited in**:
- Phase 3: Coordinate Analysis
- Phase 4: Calibration Analysis
- Phase 7: Bias Correction
- `common.py` (circular statistics functions)

**BibTeX**:
```bibtex
@book{fisher1993circular,
  title={Statistical Analysis of Circular Data},
  author={Fisher, Nicholas I.},
  year={1993},
  publisher={Cambridge University Press},
  isbn={978-0521568906}
}
```

---

## Standards

### ASTM D1535-14
**Title**: "Standard Practice for Specifying Color by the Munsell System"

**Publisher**: ASTM International

**Year**: 2014 (reapproved 2018)

**URL**: https://www.astm.org/d1535-14r18.html

**Usage in project**:
- Standard for RGB to Munsell conversion (Phase 3.3)
- Implemented in MunsellSpace Rust library
- Defines Munsell notation: Hue Value/Chroma
- Conversion pipeline: sRGB → Linear RGB → XYZ → xyY → Munsell

**Key components**:
- Munsell hue scale (0-100, where 100 = 360°)
- Value scale (0 = black, 10 = white)
- Chroma scale (0 = gray, 20+ = high saturation)

**Cited in**:
- Phase 3: RGB to Munsell Conversion
- MunsellSpace library documentation
- METHODOLOGY.md

**BibTeX**:
```bibtex
@techreport{astm2014munsell,
  title={Standard Practice for Specifying Color by the Munsell System},
  author={{ASTM International}},
  year={2014},
  number={D1535-14},
  institution={ASTM International},
  url={https://www.astm.org/d1535-14r18.html}
}
```

---

### ITU-R BT.709
**Title**: "Parameter values for the HDTV standards for production and international programme exchange"

**Publisher**: International Telecommunication Union

**Year**: 2015

**URL**: https://www.itu.int/rec/R-REC-BT.709/

**Usage in project**:
- sRGB standard and gamma correction (Phase 3.3)
- RGB primaries and white point D65
- Color transformation matrices

**Gamma correction formula**:
```
Clinear = (Csrgb / 12.92)                  if Csrgb ≤ 0.04045
Clinear = ((Csrgb + 0.055) / 1.055)^2.4    if Csrgb > 0.04045
```

**RGB to XYZ matrix**:
```
[X]   [0.4124  0.3576  0.1805]   [R]
[Y] = [0.2126  0.7152  0.0722] × [G]
[Z]   [0.0193  0.1192  0.9505]   [B]
```

**Cited in**:
- Phase 3: RGB to Munsell Conversion
- MunsellSpace library implementation
- `examples/simple_rgb_to_munsell.rs`

**BibTeX**:
```bibtex
@techreport{iturbt709,
  title={Parameter values for the HDTV standards for production and international programme exchange},
  author={{ITU-R}},
  year={2015},
  number={BT.709},
  institution={International Telecommunication Union},
  url={https://www.itu.int/rec/R-REC-BT.709/}
}
```

---

## Additional Vocabulary Source

### Meodai Color Names
**Author**: David Aerne (@meodai)

**Repository**: https://github.com/meodai/color-names

**Size**: 33,000+ color names

**License**: MIT

**Usage in project**:
- Expanded reference vocabulary for semantic validation (Phase 2.1)
- Aggregates multiple sources: Wikipedia, Crayola, Pantone, RAL, CSS, etc.
- Used to build comprehensive SBERT reference set

**Format**: JSON (name, hex, source)

**Cited in**:
- Phase 2: Semantic Validation
- `full_scale_validation.py` (reference vocabulary)

**BibTeX**:
```bibtex
@misc{meodai2024colornames,
  title={Color Names: Collection of 33,000+ Curated Color Names},
  author={Aerne, David},
  year={2024},
  howpublished={GitHub repository},
  url={https://github.com/meodai/color-names},
  note={MIT License}
}
```

---

## Reference Summary Table

| Reference | Year | Type | Phase(s) Used | Purpose |
|-----------|------|------|---------------|---------|
| Centore | 2020 | Paper | 4, 6 | Methodology, reference data |
| Munroe (XKCD) | 2010 | Dataset | 1, 2, 3 | Primary crowdsourced data |
| Lay | 2007 | Book | 6 | Convex hull theory |
| Reimers & Gurevych | 2019 | Paper | 2 | Semantic similarity (SBERT) |
| Fisher | 1993 | Book | 3, 4, 7 | Circular statistics |
| ASTM D1535 | 2014 | Standard | 3 | Munsell conversion standard |
| ITU-R BT.709 | 2015 | Standard | 3 | sRGB standard |
| Meodai | 2024 | Dataset | 2 | Reference vocabulary |

---

## Files Where References Are Cited

### Documentation
- `writeups/methodology/pipeline.md` - All references
- `overlay-preprocessing/semantic-investigation/POLYHEDRON_METHODOLOGY.md` - Centore, Lay
- `overlay-preprocessing/semantic-investigation/DATA_PIPELINE_RATIONALE.md` - Munroe, Centore
- `overlay-preprocessing/METHODOLOGY.md` - All references

### Code
- `overlay-preprocessing/semantic-investigation/full_scale_validation.py` - Reimers, Meodai
- `overlay-preprocessing/semantic-investigation/centore_comparison.py` - Centore, Fisher
- `overlay-preprocessing/semantic-investigation/build_convex_hulls.py` - Centore, Lay
- `overlay-preprocessing/semantic-investigation/common.py` - Fisher (circular stats)
- `overlay-preprocessing/semantic-investigation/fit_fourier_correction.py` - Fisher
- `examples/simple_rgb_to_munsell.rs` - ASTM D1535, ITU-R BT.709

---

## Citation Count by Reference

1. **Centore (2020)**: 12 citations (methodology, Phase 4, Phase 6)
2. **Fisher (1993)**: 8 citations (circular stats, Phase 3, 4, 7)
3. **Munroe (2010)**: 6 citations (dataset, Phase 1, 2, 3)
4. **ASTM D1535**: 5 citations (Munsell standard, Phase 3)
5. **ITU-R BT.709**: 4 citations (sRGB standard, Phase 3)
6. **Reimers & Gurevych (2019)**: 3 citations (SBERT, Phase 2)
7. **Lay (2007)**: 3 citations (convex hull theory, Phase 6)
8. **Meodai (2024)**: 2 citations (vocabulary, Phase 2)

---

**Document version**: 1.0
**Last updated**: 2024-12-24
**Purpose**: Track only references actually used in research (not comprehensive bibliography)
