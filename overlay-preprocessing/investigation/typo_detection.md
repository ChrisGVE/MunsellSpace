# Phase 2.2: Typo Detection and Correction Report

## 1. Executive Summary

| Metric | Value |
|--------|-------|
| Total color names analyzed | 175,844 |
| Established names (>=500 responses) | 422 |
| Rare names (<=10 responses) | 168,615 |
| Potential typos detected | 18,702 |
| High confidence typos | 18,702 |
| False positive flags | 18,702 |

## 2. Methodology

### Frequency-Based Typo Detection

**Assumption**: If a rare name is very similar to an established name,
the rare name is likely a typo of the established name.

**Parameters**:
- Established threshold: >= 500 responses
- Rare threshold: <= 10 responses
- Similarity threshold: 0.8

**Confidence Calculation**:
- Base confidence = edit similarity score
- Frequency ratio bonus = min(0.2, freq_ratio / 500)
- Higher frequency ratio = higher confidence in correction

## 3. Typo Categories

| Category | Count | Description |
|----------|-------|-------------|
| Transposition | 531 | Adjacent letters swapped |
| Substitution | 2,288 | Single letter replaced |
| Insertion | 3,490 | Extra letter added |
| Deletion | 1,350 | Letter missing |
| Multiple | 11,043 | Multiple edits |

## 4. High-Confidence Typos (Top 50)

| Typo | Correction | Similarity | Typo Count | Correct Count | Confidence |
|------|------------|------------|------------|---------------|------------|
| greenie | green | 0.83 | 7 | 314,172 | 1.00 |
| ghreen | green | 0.91 | 5 | 314,172 | 1.00 |
| lgreen | green | 0.91 | 3 | 314,172 | 1.00 |
| grewn | green | 0.80 | 3 | 314,172 | 1.00 |
| greeon | green | 0.91 | 1 | 314,172 | 1.00 |
| greek | green | 0.80 | 8 | 314,172 | 1.00 |
| green; | green | 0.91 | 1 | 314,172 | 1.00 |
| rgeen | green | 0.80 | 6 | 314,172 | 1.00 |
| gree n | green | 0.91 | 5 | 314,172 | 1.00 |
| grteen | green | 0.91 | 6 | 314,172 | 1.00 |
| fgreen | green | 0.91 | 4 | 314,172 | 1.00 |
| creen | green | 0.80 | 2 | 314,172 | 1.00 |
| grern | green | 0.80 | 2 | 314,172 | 1.00 |
| greenay | green | 0.83 | 5 | 314,172 | 1.00 |
| greenkl | green | 0.83 | 1 | 314,172 | 1.00 |
| greenly | green | 0.83 | 8 | 314,172 | 1.00 |
| green!! | green | 0.83 | 4 | 314,172 | 1.00 |
| preen | green | 0.80 | 2 | 314,172 | 1.00 |
| grueen | green | 0.91 | 1 | 314,172 | 1.00 |
| ?green | green | 0.91 | 1 | 314,172 | 1.00 |
| agreen | green | 0.91 | 3 | 314,172 | 1.00 |
| ggeen | green | 0.80 | 1 | 314,172 | 1.00 |
| grein | green | 0.80 | 2 | 314,172 | 1.00 |
| graen | green | 0.80 | 6 | 314,172 | 1.00 |
| gree? | green | 0.80 | 1 | 314,172 | 1.00 |
| grgeen | green | 0.91 | 1 | 314,172 | 1.00 |
| greenth | green | 0.83 | 1 | 314,172 | 1.00 |
| green?? | green | 0.83 | 1 | 314,172 | 1.00 |
| gilreen | green | 0.83 | 1 | 314,172 | 1.00 |
| greens | green | 0.91 | 7 | 314,172 | 1.00 |
| gtreen | green | 0.91 | 5 | 314,172 | 1.00 |
| greyeen | green | 0.83 | 9 | 314,172 | 1.00 |
| goreen | green | 0.91 | 1 | 314,172 | 1.00 |
| greeyn | green | 0.91 | 4 | 314,172 | 1.00 |
| green ? | green | 0.83 | 1 | 314,172 | 1.00 |
| greeh | green | 0.80 | 2 | 314,172 | 1.00 |
| greebn | green | 0.91 | 8 | 314,172 | 1.00 |
| greeb=n | green | 0.83 | 1 | 314,172 | 1.00 |
| rgreenb | green | 0.83 | 1 | 314,172 | 1.00 |
| greemn | green | 0.91 | 4 | 314,172 | 1.00 |
| greee | green | 0.80 | 5 | 314,172 | 1.00 |
| greenb | green | 0.91 | 9 | 314,172 | 1.00 |
| green17 | green | 0.83 | 1 | 314,172 | 1.00 |
| greenw | green | 0.91 | 1 | 314,172 | 1.00 |
| greel | green | 0.80 | 4 | 314,172 | 1.00 |
| treen | green | 0.80 | 2 | 314,172 | 1.00 |
| greend | green | 0.91 | 4 | 314,172 | 1.00 |
| greenj | green | 0.91 | 7 | 314,172 | 1.00 |
| greet | green | 0.80 | 2 | 314,172 | 1.00 |
| ggreen | green | 0.91 | 7 | 314,172 | 1.00 |

## 5. Category Examples

### Transposition Examples

| Typo | Correction | Count |
|------|------------|-------|
| rgeen | green | 6 |
| rbown | brown | 1 |
| lgiht blue | light blue | 8 |
| light bule | light blue | 10 |
| lihgt blue | light blue | 2 |
| ilght blue | light blue | 1 |
| light lbue | light blue | 8 |
| ligh tblue | light blue | 1 |
| roange | orange | 2 |
| light geren | light green | 3 |

### Substitution Examples

| Typo | Correction | Count |
|------|------------|-------|
| grewn | green | 3 |
| greek | green | 8 |
| creen | green | 2 |
| grern | green | 2 |
| preen | green | 2 |
| ggeen | green | 1 |
| grein | green | 2 |
| graen | green | 6 |
| gree? | green | 1 |
| greeh | green | 2 |

### Insertion Examples

| Typo | Correction | Count |
|------|------------|-------|
| ghreen | green | 5 |
| lgreen | green | 3 |
| greeon | green | 1 |
| green; | green | 1 |
| gree n | green | 5 |
| grteen | green | 6 |
| fgreen | green | 4 |
| grueen | green | 1 |
| ?green | green | 1 |
| agreen | green | 3 |

### Deletion Examples

| Typo | Correction | Count |
|------|------------|-------|
| rown | brown | 8 |
| ight blue | light blue | 4 |
| light lue | light blue | 8 |
| liht blue | light blue | 6 |
| lght blue | light blue | 10 |
| eal | teal | 4 |
| tal | teal | 10 |
| range | orange | 10 |
| oange | orange | 10 |
| ligt green | light green | 10 |

## 6. False Positive Analysis

Potential false positives are rare but valid color names flagged as typos.

### Risk Indicators
- Has color words: Contains known color vocabulary
- In canonical: Already mapped in Phase 2.1
- Low similarity: Edit distance < 0.85 suggests different name, not typo
- Contains object: Has object descriptor (chocolate, wine, etc.)

### High-Risk False Positives (Sample)

| Flagged | Suggested | Risk Score |
|---------|-----------|------------|
| dark iron | dark brown | 0.75 |
| teal purple | pastel purple | 0.75 |
| light  brown | light brown | 0.50 |
| pidgin purple | pink purple | 0.75 |
| paint green | mint green | 0.50 |
| fedex purple | faded purple | 0.75 |
| false blue | pale blue | 0.75 |
| licht blue | light blue | 0.50 |
| sky light blue | very light blue | 1.00 |
| limp green | lime green | 0.50 |
| dark terquise | dark turquoise | 0.50 |
| green-gray? | green-grey | 0.50 |
| html green | teal green | 0.75 |
| orange-y red | orange-red | 0.50 |
| electric pruple | electric purple | 0.50 |
| warm lavender | dark lavender | 0.75 |
| army grey | army green | 0.75 |
| might be purple | light purple | 0.75 |
| green marble | green blue | 0.75 |
| light grean | light green | 0.50 |

## 7. Recommendations

1. **High-confidence typos** (>=0.9) can be auto-corrected
2. **Medium-confidence typos** (0.8-0.9) should be reviewed
3. **False positive flags** require manual verification
4. **Single-edit typos** (transposition, substitution) are most reliable
5. **Multiple-edit corrections** have higher false positive risk

## 8. Integration with Phase 2.1

This analysis complements Phase 2.1 spelling variant detection:
- Phase 2.1: Rule-based and phonetic matching for known variants
- Phase 2.2: Frequency-based detection for unknown typos
- Combined: More comprehensive coverage of spelling errors

---

*Generated by Phase 2.2: Typo Detection and Correction*