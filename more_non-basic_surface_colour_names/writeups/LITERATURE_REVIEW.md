# Literature Review: Color-Semantic Embeddings

## Research Notes for Color Embedding Fine-Tuning Project
**Date**: 2025-12-30
**Purpose**: Academic context for semantic color pipeline publication

---

## 1. Foundational Color Science

### Berlin & Kay Color Universals (1969)

The foundational theory of cross-cultural color naming by Berlin and Kay established:
- Languages share a common stock of color concepts
- Terms evolve in a constrained order (7 evolutionary stages)
- 11 basic English color terms: red, yellow, green, blue, black, white, gray, orange, brown, pink, purple
- Slavic languages have 12 (separate light/dark blue)

**World Color Survey (1976)**:
- 110 unwritten languages from 45 language families
- 25 monolingual speakers per language
- 320 Munsell color chips named
- Privileged anchor points in color space

**Key Reference**: [Berlin & Kay Theory](https://link.springer.com/referenceworkentry/10.1007/978-3-642-27851-8_62-2)

### Modern Computational Extensions

- [Regier et al.](https://www.pnas.org/doi/10.1073/pnas.1619666114): "Color naming across languages reflects optimal or near-optimal divisions of an irregularly shaped perceptual color space"
- Expression-induction models simulate BCT evolution with Bayesian inference
- Agent-based models reproduce typological patterns from learning biases

---

## 2. Color-Emotion Associations

### Cross-Cultural Studies

**Jonauskaite et al. (2020)** - [Psychological Science](https://journals.sagepub.com/doi/10.1177/0956797620948810)
- 4,598 participants, 30 nations, 22 languages
- Universal similarity coefficient r = 0.88
- Key associations: red→love (69.2%), yellow→joy (55.7%), black→sadness (53.7%)
- Cultural variations: white = mourning in China

**Adams & Osgood (1973)** - [Journal of Cross-Cultural Psychology](https://journals.sagepub.com/doi/10.1177/002202217300400201)
- 23-culture semantic differential study
- Cross-cultural similarities in feelings about colors

**Machine Learning Approach** - [Royal Society Open Science](https://royalsocietypublishing.org/doi/10.1098/rsos.190741)
- SVM classifier predicted colors from emotion ratings (AUC 0.830)
- Country-specific patterns detectable above universal baseline

### Cultural Color-Valence

[PMC Study on Implicit Associations](https://pmc.ncbi.nlm.nih.gov/articles/PMC10017663/):
- BLACK/GREY = bad, WHITE/BLUE/GREEN = good (Western)
- RED = strong, active; YELLOW/WHITE/GREY = weak
- Chinese: white carries negative connotations (mourning)

---

## 3. Sentence Embeddings & Domain Adaptation

### SBERT Architecture

[Sentence-BERT (Reimers & Gurevych, 2019)](https://sbert.net/):
- Siamese network architecture with BERT encoder
- Fixed-length sentence embeddings
- Contrastive training objectives

### Domain Adaptation Strategies

1. **TSDAE** - [Domain Adaptation Docs](https://sbert.net/examples/domain_adaptation/README.html)
   - Up to 8-point improvement with domain pre-training
   - 10-point improvement for semantic search

2. **GPL (Generative Pseudo Labeling)**
   - Overcomes computational overhead of adaptive pre-training
   - Can be applied on top of fine-tuned models

3. **LoRA (Low-Rank Adaptation)** - [arXiv:2106.09685](https://arxiv.org/abs/2106.09685)
   - Freeze pretrained weights, inject trainable rank decomposition matrices
   - 10,000x fewer trainable parameters than full fine-tuning
   - 3x lower GPU memory requirement
   - [Practical Guide](https://magazine.sebastianraschka.com/p/practical-tips-for-finetuning-llms)

4. **Bottleneck Adapters**
   - Small trainable modules inside frozen pretrained layers
   - Alternative to LoRA with similar efficiency gains

---

## 4. Metaphor & Synesthesia Processing

### Linguistic Synesthesia

[Cambridge Core Study](https://www.cambridge.org/core/product/37BF69837C0EE4B490F82D9FD178A386/core-reader):
- Linguistic synesthesia: words from one modality describe another
- Examples: "loud colors", "cold smell", "itching tunes"
- Differs from metaphor (concrete→concrete vs concrete→abstract)

### Computational Metaphor Processing

[ACL Anthology - Recent Advances](https://aclanthology.org/2021.naacl-main.372.pdf):
- Metaphor is highly frequent, indispensable for semantic NLP
- Lack of common task definition hinders comparison
- Context vectors show metaphor structures semantic space

[MIT Press - Multilingual Metaphor Processing](https://direct.mit.edu/coli/article/43/1/71/1565/Multilingual-Metaphor-Processing-Experiments-with):
- Weakly supervised and unsupervised techniques
- Generalize metaphor mechanisms from distributional properties

### Cross-Modal Similarity Model

[ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0885230818301086):
- Synesthetic metaphor bridges five perceptual modalities
- Key: discover similarity between source domain and target perceptual features

---

## 5. Vision-Language Models & Color

### CLIP Architecture

[Wikipedia - CLIP](https://en.wikipedia.org/wiki/Contrastive_Language-Image_Pre-training):
- Contrastive training aligns images and text in shared vector space
- Modality-specific encoders mapped to similar embeddings for matching pairs

### Visual-Semantic Grounding

[OpenReview - VG-BERT](https://openreview.net/forum?id=ljOg2HIBDGH):
- Cross-modal contrastive learning grounds language in vision
- Produces "visually grounded semantic space"
- Embeddings predictive of human semantic feature norms

### CLIP Limitations for Color

Research shows CLIP fails on fine-grained color semantics:
- Similar distributions for opposite descriptions ("red car" vs "not red car")
- Rotations in embedding space correspond to color transformations

---

## 6. Text-to-Color Prediction

### Compositional Color from Text

[Maheshwari et al.](https://3dvar.com/Maheshwari2021Generating.pdf):
- Handles abstract concepts ("hot") and explicit color indicators ("pink")
- Learns composition: "young leaves" → green, "fallen leaves" → brown-red
- **Zero-shot learning** for unseen (attribute, object) pairs

### Emergent Color Categorization in CNNs

[eLife](https://elifesciences.org/articles/76472):
- Color categories emerge from object recognition training
- No explicit color supervision needed

### Neural Network Color Naming

[PNAS](https://www.pnas.org/doi/10.1073/pnas.2016569118):
- Communicating neural networks develop efficient color-naming systems
- Maximize accuracy while minimizing complexity

---

## 7. Cross-Cultural Perception in ML

### Globalization Study (2024)

[eScholarship/PSyArXiv](https://osf.io/preprints/psyarxiv/3jvxw):
- 2,280 participants, 22 languages
- Color naming maps differ structurally across languages (even among internet users)
- LLMs have language-specific color representations
- "Globalization has not removed cultural distinctions in color concepts"

### Cultural Diversity in Vision Models

[arXiv:2310.14356](https://arxiv.org/html/2310.14356):
- 7 languages compared for same images
- Multilingual descriptions: 29.9% more objects, 24.5% more relations, 46.0% more attributes
- Computer vision often treats perception as homogeneous (incorrectly)

### Japanese Pumpkin Example

- Japanese speakers say pumpkins are "green" (local reality)
- English speakers say "orange" (Western variety)
- GPT-4o in Japanese responds "orange" (English pattern leakage)

---

## 8. Relevant Datasets

| Dataset | Size | Languages | Content | Citation |
|---------|------|-----------|---------|----------|
| Free Association DB | 223,786 responses | 7 (EN, FR, DE, ES, IT, ET, LT) | Color→concept associations | [OSF](https://osf.io/xzcbg/) |
| Jonauskaite Survey | 4,598 participants | 22 | Color-emotion ratings | [OSF](https://osf.io/873df/) |
| World Color Survey | 110 languages | 110 | Munsell chip naming | WCS |
| 128-Year Review | Meta-analysis | Multi | Color-emotion research | [OSF](https://osf.io/g5srf/) |
| Our Wikipedia Harvest | 1,062 articles | 180+ | Color families, descriptions | This project |

---

## 9. Gaps in Literature & Our Contribution

### Identified Gaps

1. **No unified color embedding model**: Existing work fragments across vision, language, psychology
2. **Limited metaphor→color inference**: Most work is metaphor detection, not color prediction
3. **Cross-lingual color semantics underexplored**: Few multilingual color embedding studies
4. **No systematic comparison of fine-tuning strategies for color domain**

### Our Contributions

1. **First comprehensive color embedding arena**: Compare 4 architectures on same data
2. **Unified training data**: Wikipedia families + emotion associations + free associations
3. **Multilingual from the start**: 180+ languages in training data
4. **Metaphor-to-color pipeline**: Novel application of semantic embeddings
5. **Publication-ready evaluation**: Standardized benchmarks across architectures

---

## 10. Key Papers to Cite

### Must-Cite (Foundational)
- Berlin, B., & Kay, P. (1969). Basic Color Terms
- Reimers, N., & Gurevych, I. (2019). Sentence-BERT
- Jonauskaite, D., et al. (2020). Universal Patterns in Color-Emotion Associations

### Should-Cite (Methodological)
- Hu, E.J., et al. (2021). LoRA: Low-Rank Adaptation
- Maheshwari, P., et al. (2021). Generating Compositional Color from Text
- Adams, F.M., & Osgood, C.E. (1973). Cross-Cultural Affective Meanings of Color

### May-Cite (Context)
- Zhang, Y., & Choi, Y. (2021). Explainable Semantic Space by Grounding Language to Vision
- Regier, T., Kay, P., & Khetarpal, N. (2007). Color Naming Reflects Optimal Partitions

---

## Notes for Paper Writing

### Potential Titles
1. "ColorSBERT: Domain-Adapted Sentence Embeddings for Semantic Color Inference"
2. "From Metaphor to Color: Fine-Tuning Language Models for Cross-Modal Perception"
3. "A Comparative Study of Embedding Architectures for Multilingual Color Semantics"

### Key Claims to Support
1. Base SBERT lacks color family knowledge (our baseline experiment shows this)
2. Fine-tuning restores/creates color relationships (arena results)
3. Cross-lingual consistency is achievable (multilingual training data)
4. Emotional/cultural associations can be learned (Jonauskaite data integration)

### Experimental Contributions
- Arena comparison of 4 architectures (first systematic comparison)
- 66,307 training pairs across 180+ languages
- Evaluation on family accuracy, emotion accuracy, cross-lingual consistency, poetic inference
