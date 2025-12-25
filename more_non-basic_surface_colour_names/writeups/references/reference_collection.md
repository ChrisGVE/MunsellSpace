# Comprehensive Reference Collection

## Academic Papers

### Primary Methodology Paper

**Centore, Paul (2020)**
- **Title**: "Beige, aqua, fuchsia, etc.: Definitions for some non-basic surface colour names"
- **Journal**: Journal of the International Colour Association (JAIC)
- **Volume**: 25
- **Pages**: 24-54
- **URL**: https://www.munsellcolourscienceforpainters.com/ColourSciencePapers/BeigeAquaFuchsiaEtc.pdf
- **Key contribution**: Inner convex hull methodology for defining color polyhedra from measured fabric samples
- **Dataset**: 9,261 CAUS fabric samples, 30 color categories analyzed
- **Citation relevance**: Primary methodology for polyhedron construction and outlier removal

### Convex Hull Theory

**Lay, Steven R. (2007)**
- **Title**: "Convex Sets and Their Applications"
- **Publisher**: Dover Publications
- **Location**: Mineola, NY
- **Key contribution**: Mathematical foundation for minimal generating sets and convex hull vertices
- **Citation relevance**: Defines "minimal generating set" used in Centore's methodology
- **Referenced by**: Centore (2020) as citation [4]

### Color Naming Studies

**Berlin, Brent and Kay, Paul (1969)**
- **Title**: "Basic Color Terms: Their Universality and Evolution"
- **Publisher**: University of California Press
- **Key contribution**: Cross-cultural study of color naming, identifies 11 basic color terms
- **Relevance**: Theoretical foundation for semantic color categorization
- **Basic terms identified**: white, black, red, green, yellow, blue, brown, purple, pink, orange, grey

**Monroe, Meredith et al. (2016)**
- **Title**: "The names of colors in the laboratory and online"
- **Journal**: Color Research & Application
- **Key contribution**: Comparison of laboratory vs. online color naming
- **Relevance**: Validates crowdsourced color naming approaches like XKCD

### Sentence Embeddings

**Reimers, Nils and Gurevych, Iryna (2019)**
- **Title**: "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks"
- **Conference**: EMNLP-IJCNLP 2019
- **Key contribution**: SBERT model for semantic similarity computation
- **Relevance**: Core methodology for semantic validation (Phase 2.1)
- **Model used**: `all-MiniLM-L6-v2`

### Circular Statistics

**Fisher, Nicholas I. (1993)**
- **Title**: "Statistical Analysis of Circular Data"
- **Publisher**: Cambridge University Press
- **Key contribution**: Circular mean, circular variance, and angular statistics
- **Relevance**: Essential for hue analysis (hue is circular: 0° = 360°)
- **Applications**: Centroid calculation, bias aggregation, model fitting

### Outlier Detection

**Eddy, William F. (1982)**
- **Title**: "Convex Hull Peeling"
- **Chapter in**: COMPSTAT 1982 5th Symposium held at Toulouse 1982
- **Publisher**: Springer
- **URL**: https://link.springer.com/chapter/10.1007/978-3-642-51461-6_4
- **Key contribution**: Iterative convex hull peeling for outlier detection
- **Relevance**: Optional enhancement to Centore's single-layer approach

**Sridhar, Vinesh and Svenning, Alejandro (2024)**
- **Title**: "Fast Area-Weighted Peeling of Convex Hulls for Outlier Detection"
- **Journal**: arXiv preprint
- **URL**: https://arxiv.org/abs/2410.04544
- **Key contribution**: O(n log n) algorithm for area-weighted outlier removal
- **Relevance**: Alternative to Centore's vertex-based approach (not used in current implementation)

### Model Selection

**Tibshirani, Robert (1996)**
- **Title**: "Regression Shrinkage and Selection via the Lasso"
- **Journal**: Journal of the Royal Statistical Society, Series B
- **Volume**: 58, No. 1
- **Pages**: 267-288
- **Key contribution**: Model selection principles, bias-variance tradeoff
- **Relevance**: Justifies Fourier 4 selection over higher-order models

---

## Data Sources

### Primary Dataset: XKCD Color Survey

**Munroe, Randall (2010)**
- **Title**: "Color Survey Results"
- **Published**: XKCD Blog
- **Date**: May 3, 2010
- **URL**: https://blog.xkcd.com/2010/05/03/color-survey-results/
- **Dataset size**: ~3.4 million responses, 175,844 unique color names
- **Collection method**: Online survey asking users to name random RGB colors displayed on screen
- **Data format**: Color name → list of RGB hex values
- **Download**: https://xkcd.com/color/rgb.txt (954 most common colors)
- **License**: Publicly available
- **Characteristics**:
  - Crowdsourced (freeform naming)
  - Screen colors (RGB, uncalibrated monitors)
  - Self-luminous (not reflective)
  - High sample counts for common colors
  - Long-tail distribution

### Reference Dataset: Centore Polyhedron Data

**Centore, Paul (2020) - CAUS Dataset**
- **Source**: Color Association of the United States (CAUS) fabric samples
- **Size**: 9,261 fabric samples
- **Measurement**: Spectrophotometer-measured Munsell coordinates
- **Illuminant**: Standard D65 (presumably)
- **Categories analyzed**: 30 color categories (beige, aqua, teal, etc.)
- **Data format**: Polyhedron vertices in Munsell space (H, V, C)
- **Download**: Included in Centore (2020) supplementary materials
- **Characteristics**:
  - Expert-assigned color names
  - Physical colors (reflective, measured)
  - Controlled illumination
  - Smaller sample counts per category

### Additional Vocabulary Sources

**Meodai Color Names**
- **Author**: David Aerne (@meodai)
- **Repository**: https://github.com/meodai/color-names
- **Size**: 33,000+ color names from multiple sources
- **Sources aggregated**:
  - Wikipedia color names
  - Crayola crayon names
  - Pantone names
  - RAL color standard
  - HTML/CSS color names
  - Commercial paint databases
- **License**: MIT
- **Usage**: Reference vocabulary for semantic validation
- **Format**: JSON (name, hex, source)

**ColorHexa**
- **URL**: https://www.colorhexa.com/
- **Description**: Web-based color encyclopedia
- **Size**: 16+ million colors
- **Features**: Color names, conversions, palettes
- **Usage**: Validation reference for common color names
- **Access**: Web scraping (rate-limited)

**Color-name.com**
- **URL**: http://color-name.com/
- **Description**: User-contributed color names
- **Size**: Variable (user-generated)
- **Usage**: Additional vocabulary source
- **Limitation**: Quality varies (user-submitted)

**Wikipedia: List of Colors**
- **URL**: https://en.wikipedia.org/wiki/List_of_colors_(compact)
- **Size**: ~1,500 notable color names
- **Sources**: Multiple (Crayola, Pantone, web colors, etc.)
- **Usage**: High-quality reference vocabulary
- **License**: CC BY-SA

---

## Technical Standards

### Munsell Color System

**ASTM D1535-14**
- **Title**: "Standard Practice for Specifying Color by the Munsell System"
- **Publisher**: ASTM International
- **Year**: 2014 (reapproved 2018)
- **Scope**: Defines Munsell color notation (Hue Value/Chroma)
- **URL**: https://www.astm.org/d1535-14r18.html
- **Relevance**: Standard for RGB to Munsell conversion
- **Key components**:
  - Munsell hue notation (5R, 10YR, etc.)
  - Value scale (0 = black, 10 = white)
  - Chroma scale (0 = gray, 20+ = high saturation)

**Munsell Renotation Data**
- **Source**: Rochester Institute of Technology (RIT)
- **Description**: Empirical CIE XYZ coordinates for Munsell samples
- **URL**: https://www.rit.edu/cos/colorscience/rc_munsell_renotation.php
- **Format**: Munsell notation → CIE xyY coordinates
- **Usage**: Validation reference for Munsell conversions
- **License**: Public domain

### sRGB Standard

**ITU-R BT.709**
- **Title**: "Parameter values for the HDTV standards for production and international programme exchange"
- **Publisher**: International Telecommunication Union
- **Year**: 2015
- **Scope**: Defines sRGB color space and transformation matrices
- **URL**: https://www.itu.int/rec/R-REC-BT.709/
- **Key components**:
  - RGB primaries (chromaticity coordinates)
  - White point D65 (x=0.3127, y=0.3290)
  - Gamma correction formula
  - RGB to XYZ matrix

**IEC 61966-2-1**
- **Title**: "Multimedia systems and equipment - Colour measurement and management - Part 2-1: Colour management - Default RGB colour space - sRGB"
- **Publisher**: International Electrotechnical Commission
- **Year**: 1999
- **Scope**: sRGB standard for multimedia
- **Relevance**: Defines sRGB gamma curve and transfer function

### CIE Color Spaces

**CIE 1931 XYZ**
- **Source**: Commission Internationale de l'Éclairage (CIE)
- **Title**: "CIE 1931 Standard Colorimetric Observer"
- **Description**: Device-independent color space based on human vision
- **Components**: X (red-like), Y (luminance), Z (blue-like)
- **Usage**: Intermediate step in RGB to Munsell conversion

**CIE xyY**
- **Source**: CIE
- **Description**: Chromaticity coordinates (x, y) + luminance (Y)
- **Derivation**: x = X/(X+Y+Z), y = Y/(X+Y+Z)
- **Usage**: Simplifies hue/chroma calculations from XYZ

---

## Color Science References

### ISCC-NBS Color System

**Kelly, Kenneth L. and Judd, Deane B. (1976)**
- **Title**: "Color: Universal Language and Dictionary of Names"
- **Publisher**: National Bureau of Standards (NBS)
- **NBS Special Publication**: 440
- **URL**: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nbsspecialpublication440.pdf
- **Key contribution**: ISCC-NBS color naming system with 267 color categories
- **Relevance**: Alternative systematic color naming approach
- **Components**:
  - 13 hue names
  - 8 lightness modifiers
  - 4 saturation modifiers
  - Systematic combination rules

### Munsell Book of Color

**Munsell, Albert H. (1905, reissued)**
- **Title**: "A Color Notation"
- **Publisher**: Various editions
- **Description**: Original Munsell color theory and notation system
- **Historical significance**: First perceptually uniform color space
- **Modern version**: Munsell Book of Color (physical swatches)

---

## Computational Tools & Libraries

### Python Libraries

**Sentence-Transformers**
- **Authors**: Nils Reimers et al.
- **Repository**: https://github.com/UKPLab/sentence-transformers
- **Version used**: 2.2.0+
- **License**: Apache 2.0
- **Usage**: Semantic similarity (Phase 2.1)
- **Model**: `all-MiniLM-L6-v2`

**NumPy**
- **Version**: 1.24+
- **License**: BSD
- **Usage**: Numerical computations, array operations

**SciPy**
- **Version**: 1.10+
- **License**: BSD
- **Usage**: ConvexHull computation, spatial operations

**scikit-learn** (optional)
- **Version**: 1.2+
- **License**: BSD
- **Usage**: Alternative ML methods, statistical tools

### Rust Libraries

**MunsellSpace**
- **Repository**: https://github.com/[username]/MunsellSpace
- **License**: MIT
- **Usage**: ASTM D1535 compliant RGB to Munsell conversion
- **Implementation**: Mathematical conversion (no lookup tables)
- **Dependencies**: serde, csv, thiserror

**PyO3** (Python bindings)
- **Version**: 0.19+
- **License**: Apache 2.0 / MIT
- **Usage**: Rust-Python interoperability

---

## Related Research

### Color Perception

**Palmer, Stephen E. (1999)**
- **Title**: "Vision Science: Photons to Phenomenology"
- **Publisher**: MIT Press
- **Relevance**: Theoretical foundation for color perception
- **Key topics**: Trichromacy, opponent processing, color constancy

**Wandell, Brian A. (1995)**
- **Title**: "Foundations of Vision"
- **Publisher**: Sinauer Associates
- **Relevance**: Computational color vision
- **Key topics**: Photoreceptor responses, color matching functions

### Color Naming Linguistics

**Regier, Terry and Kay, Paul (2009)**
- **Title**: "Language, thought, and color: Whorf was half right"
- **Journal**: Trends in Cognitive Sciences
- **Volume**: 13, No. 10
- **Relevance**: Relationship between language and color perception

### Machine Learning for Color

**van de Weijer, Joost et al. (2009)**
- **Title**: "Learning Color Names for Real-World Applications"
- **Journal**: IEEE Transactions on Image Processing
- **Relevance**: ML approaches to color naming

---

## Software & Tools

### Color Conversion Tools

**Colour**
- **Repository**: https://github.com/colour-science/colour
- **Language**: Python
- **License**: BSD-3-Clause
- **Description**: Comprehensive color science library
- **Relevance**: Alternative implementation reference for conversions

**Colorspacious**
- **Repository**: https://github.com/njsmith/colorspacious
- **Language**: Python
- **License**: MIT
- **Description**: CIECAM02, CAM16, and other advanced color spaces
- **Relevance**: Perceptual color space alternatives

### Statistical Tools

**R (circular package)**
- **Package**: circular
- **Description**: Circular statistics in R
- **Relevance**: Validation reference for circular mean/variance

---

## Datasets Not Used (For Reference)

### OSF Color Survey
- **URL**: https://osf.io/g8zjy/
- **Size**: 330K color naming responses
- **Limitation**: Smaller than XKCD, less comprehensive

### Lindsey & Brown (2014) World Color Survey
- **Description**: Cross-linguistic color naming
- **Limitation**: Focuses on basic terms, not extended vocabulary

### CIELAB Gamut Data
- **Source**: ICC profiles
- **Limitation**: Device-specific, not semantic

---

## Citation Format

### BibTeX Entry for This Project

```bibtex
@misc{munsellspace-color-research-2024,
  title={Screen Colors to Physical Color Space: A Data Pipeline for Semantic Color Overlays},
  author={MunsellSpace Research Team},
  year={2024},
  howpublished={Research project documentation},
  url={https://github.com/[username]/MunsellSpace}
}
```

### Primary Citation (Centore)

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

### Primary Dataset (XKCD)

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

## Reference Organization

### By Research Phase

**Phase 1: Data Collection**
- Munroe (2010) - XKCD dataset
- Centore (2020) - CAUS dataset
- Meodai - Additional vocabulary

**Phase 2: Entity Matching**
- Reimers & Gurevych (2019) - SBERT
- Berlin & Kay (1969) - Basic color terms

**Phase 3: Coordinate Analysis**
- ASTM D1535 - Munsell standard
- ITU-R BT.709 - sRGB standard

**Phase 4: Calibration**
- Fisher (1993) - Circular statistics
- Centore (2020) - Reference centroids

**Phase 6: Convex Hull**
- Lay (2007) - Convex hull theory
- Centore (2020) - Inner hull methodology
- Eddy (1982) - Hull peeling (optional)

**Phase 7: Bias Correction**
- Tibshirani (1996) - Model selection
- Fisher (1993) - Circular statistics

---

## Accessibility

All references are categorized by:
- **Open Access**: Freely available online
- **Paywalled**: Requires institutional access
- **Book**: Available for purchase
- **Standard**: ASTM/ISO/IEC (may require purchase)

### Open Access References
- Centore (2020) - PDF freely available
- Munroe (2010) - Blog post, public
- Meodai - GitHub, MIT license
- Sridhar & Svenning (2024) - arXiv preprint

### Paywalled/Restricted
- Berlin & Kay (1969) - Book (university libraries)
- ASTM D1535 - Standard (purchase required)
- Regier & Kay (2009) - Journal article

### Purchase Recommended
- Lay (2007) - Dover edition (~$20)
- Fisher (1993) - Cambridge University Press
- Palmer (1999) - MIT Press

---

**Document version**: 1.0
**Last updated**: 2024-12-24
**Maintained by**: MunsellSpace Color Research Project
