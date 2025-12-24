# Research Article Structure: Screen Colors to Physical Colors

## Working Title

**"Bridging Screen and Physical Color Perception: Systematic Bias Detection
Between Crowdsourced RGB and Spectrophotometer-Measured Munsell Colors"**

## Abstract Outline

- Problem: Mapping crowdsourced screen color names to physical Munsell space
- Approach: Multi-stage pipeline with semantic validation and bias detection
- Key Finding: Systematic biases in value (+0.81) and chroma (+3.82), but
  hue bias is non-uniform and category-dependent
- Conclusion: Linear correction insufficient; non-linear modeling required

## Article Sections

### 1. Introduction
- File: `01_introduction.md`
- The challenge of semantic color overlays
- Two data sources: XKCD (screen) vs Centore (physical)
- Research questions and goals

### 2. Related Work
- File: `02_related_work.md`
- Color naming studies (Berlin & Kay, Monroe et al.)
- Sentence embeddings for semantic similarity
- RGB to Munsell conversion methods

### 3. Data Sources
- File: `03_data_sources.md`
- XKCD Color Survey (175K names, 3.4M responses)
- Centore Polyhedron Data (30 categories, spectrophotometer-measured)
- Fundamental differences: screen vs physical color perception

### 4. Methodology
- File: `04_methodology.md`
- Stage 1: Semantic validation (SBERT approach)
- Stage 2: Color wheel consistency check
- Stage 3: RGB to Munsell conversion
- Stage 4: Centore comparison and bias detection

### 5. What Didn't Work
- File: `05_failed_approaches.md`
- String matching (semantic loss)
- Sample count filtering (over-conservative)
- Character autoencoder (non-ASCII failure)
- BERT tokenization (spelling variant failure)
- Linear hue correction (non-uniform bias)

### 6. Results
- File: `06_results.md`
- Semantic validation: 137,878 validated names (82.5%)
- Munsell conversion: 133,359 colors (96.7%)
- Bias detection: 101,894 matched colors

### 7. Key Findings
- File: `07_key_findings.md`
- Universal value bias: +0.81 (screen colors appear lighter)
- Universal chroma bias: +3.82 (screen colors appear more saturated)
- Non-uniform hue bias: category-dependent shifts
- Implications for non-linear modeling

### 8. Discussion
- File: `08_discussion.md`
- Why linear correction fails
- Physical explanation of biases
- Proposed non-linear approaches

### 9. Future Work
- File: `09_future_work.md`
- Non-linear modeling approaches
- Hue-dependent correction functions
- Validation strategies

### 10. Conclusion
- File: `10_conclusion.md`
- Summary of contributions
- Practical implications

## Supporting Materials

### Appendices
- `appendix_a_data_pipeline.md` - Complete pipeline architecture
- `appendix_b_statistics.md` - Detailed statistical analysis
- `appendix_c_code_samples.md` - Key implementation code
- `appendix_model_selection.md` - Model selection rationale and overfitting analysis

### Data Files Reference
- `data_files_reference.md` - Location and purpose of all data files

### Figures (to create)
- Pipeline architecture diagram
- Hue bias by category scatter plot
- Value/chroma bias distribution
- Munsell color space visualization

## Status Tracking

| Section | Status | Last Updated |
|---------|--------|--------------|
| 00 Structure | Complete | 2024-12-24 |
| 01 Introduction | Complete | 2024-12-24 |
| 02 Related Work | Complete | 2024-12-24 |
| 03 Data Sources | Complete | 2024-12-24 |
| 04 Methodology | Complete | 2024-12-24 |
| 05 Failed Approaches | Complete | 2024-12-24 |
| 06 Results | Complete | 2024-12-24 |
| 07 Key Findings | Complete | 2024-12-24 |
| 08 Discussion | Complete | 2024-12-24 |
| 09 Future Work | Complete | 2024-12-24 |
| 10 Conclusion | Complete | 2024-12-24 |
