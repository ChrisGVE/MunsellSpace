# Phase 2.1: Spelling Variant Detection Report

## 1. Executive Summary

| Metric | Value |
|--------|-------|
| Total names analyzed | 181,637 |
| XKCD unique names | 175,844 |
| Centore unique names | 7,584 |
| Reference dictionary size | 422 |
| Total variants detected | 132,418 |
| Multi-method agreement | 11,993 |
| High confidence (>=0.9) | 17,261 |

## 2. Detection Method Results

| Method | Variants Found |
|--------|---------------|
| Rule-based | 7,638 |
| Phonetic | 127,374 |
| Edit distance | 12,744 |
| Word-level | 60,760 |

## 3. Methodology

### 3.1 Rule-Based Detection
- Predefined mappings for known spelling variants
- US English as canonical form (gray > grey)
- Known color name misspellings (fuschia → fuchsia)
- Confidence: 1.0 (highest)

### 3.2 Phonetic Detection
- Soundex algorithm for consonant-based sound encoding
- Metaphone algorithm for more accurate English phonetics
- Matches against reference dictionary of high-frequency names
- Confidence: 0.8 (both match) or 0.6 (single match)

### 3.3 Edit Distance Detection
- Levenshtein distance via difflib SequenceMatcher
- Threshold: 0.85 similarity ratio
- Finds similar spellings within edit threshold
- Confidence: proportional to similarity score

### 3.4 Word-Level Detection
- Decomposes compound names into words
- Checks each word against reference word set
- Applies rules and edit distance per-word
- Confidence: 0.7

### 3.5 Ensemble Combination
- Multiple methods vote on canonical form
- Multi-hit agreement adds confidence bonus (+0.1 per additional method)
- Final confidence capped at 1.0

## 4. High-Impact Variants (Top 50)

Ranked by confidence and XKCD response count:

| Variant | Canonical | Confidence | Methods | XKCD Count |
|---------|-----------|------------|---------|------------|
| grey | gray | 1.00 | rule, word_level | 36,127 |
| fuschia | fuchsia | 1.00 | rule, word_level | 13,154 |
| lavendar | lavender | 1.00 | rule, word_level | 4,381 |
| grey blue | gray blue | 1.00 | rule, word_level | 3,595 |
| dark grey | dark gray | 1.00 | rule, word_level | 3,163 |
| blue-grey | blue-gray | 1.00 | rule | 2,955 |
| blue grey | blue gray | 1.00 | rule, word_level | 2,872 |
| turqoise | turquoise | 1.00 | rule, word_level | 2,722 |
| fushia | fuchsia | 1.00 | rule, word_level | 2,697 |
| light grey | light gray | 1.00 | rule, word_level | 2,465 |
| grey green | gray green | 1.00 | rule, word_level | 2,428 |
| grey-blue | gray-blue | 1.00 | rule | 2,424 |
| grey-green | gray-green | 1.00 | rule | 2,166 |
| burgandy | burgundy | 1.00 | rule, word_level | 1,404 |
| greenish grey | greenish gray | 1.00 | rule, word_level | 906 |
| turqouise | turquoise | 1.00 | rule, word_level | 810 |
| grey purple | gray purple | 1.00 | rule | 787 |
| turquise | turquoise | 1.00 | rule, word_level | 744 |
| lavander | lavender | 1.00 | rule, word_level | 736 |
| chartruse | chartreuse | 1.00 | rule, word_level | 692 |
| green-grey | green-gray | 1.00 | rule | 692 |
| yello | yellow | 1.00 | rule, word_level | 667 |
| slate grey | slate gray | 1.00 | rule, word_level | 665 |
| bluish grey | bluish gray | 1.00 | rule | 623 |
| grey-brown | gray-brown | 1.00 | rule | 590 |
| green grey | green gray | 1.00 | rule, word_level | 572 |
| grey brown | gray brown | 1.00 | rule, word_level | 544 |
| purple grey | purple gray | 1.00 | rule | 543 |
| grey-purple | gray-purple | 1.00 | rule | 515 |
| purple-grey | purple-gray | 1.00 | rule | 499 |
| muave | mauve | 1.00 | rule, phonetic, word_level | 489 |
| bluish gray | bluish grey | 1.00 | phonetic, edit_distance | 479 |
| fuchia | fuchsia | 1.00 | rule, edit_distance, word_level | 475 |
| fusia | fuchsia | 1.00 | rule, word_level | 471 |
| turquois | turquoise | 1.00 | phonetic, edit_distance, word_level | 457 |
| blu | blue | 1.00 | rule, edit_distance, word_level | 455 |
| gren | green | 1.00 | rule, edit_distance, word_level | 448 |
| yellowy green | yellow green | 1.00 | edit_distance, word_level | 443 |
| puple | purple | 1.00 | edit_distance, word_level | 434 |
| bluish | blueish | 1.00 | edit_distance, word_level | 428 |
| dark blue green | dark blue-green | 1.00 | phonetic, edit_distance | 426 |
| steel grey | steel gray | 1.00 | rule, word_level | 422 |
| slate gray | slate grey | 1.00 | phonetic, edit_distance | 415 |
| purply blue | purpley blue | 1.00 | phonetic, edit_distance, word_level | 415 |
| gray purple | grey purple | 1.00 | phonetic, edit_distance | 404 |
| purpleish blue | purplish blue | 1.00 | phonetic, edit_distance, word_level | 402 |
| chartruese | chartreuse | 1.00 | rule, word_level | 389 |
| purpleish | purplish | 1.00 | edit_distance, word_level | 389 |
| redish | reddish | 1.00 | edit_distance, word_level | 384 |
| fucsia | fuchsia | 1.00 | rule, edit_distance, word_level | 375 |

## 5. Multi-Method Agreement Examples

Variants detected by 2+ methods (higher confidence):

| Variant | Canonical | Methods | Confidence |
|---------|-----------|---------|------------|
| grey | gray | rule, word_level | 1.00 |
| fuschia | fuchsia | rule, word_level | 1.00 |
| lavendar | lavender | rule, word_level | 1.00 |
| grey blue | gray blue | rule, word_level | 1.00 |
| dark grey | dark gray | rule, word_level | 1.00 |
| blue grey | blue gray | rule, word_level | 1.00 |
| turqoise | turquoise | rule, word_level | 1.00 |
| fushia | fuchsia | rule, word_level | 1.00 |
| light grey | light gray | rule, word_level | 1.00 |
| grey green | gray green | rule, word_level | 1.00 |
| burgandy | burgundy | rule, word_level | 1.00 |
| greenish grey | greenish gray | rule, word_level | 1.00 |
| turqouise | turquoise | rule, word_level | 1.00 |
| turquise | turquoise | rule, word_level | 1.00 |
| lavander | lavender | rule, word_level | 1.00 |
| chartruse | chartreuse | rule, word_level | 1.00 |
| yello | yellow | rule, word_level | 1.00 |
| slate grey | slate gray | rule, word_level | 1.00 |
| green grey | green gray | rule, word_level | 1.00 |
| grey brown | gray brown | rule, word_level | 1.00 |
| muave | mauve | rule, phonetic, word_level | 1.00 |
| bluish gray | bluish grey | phonetic, edit_distance | 1.00 |
| fuchia | fuchsia | rule, edit_distance, word_level | 1.00 |
| fusia | fuchsia | rule, word_level | 1.00 |
| turquois | turquoise | phonetic, edit_distance, word_level | 1.00 |
| blu | blue | rule, edit_distance, word_level | 1.00 |
| gren | green | rule, edit_distance, word_level | 1.00 |
| yellowy green | yellow green | edit_distance, word_level | 1.00 |
| puple | purple | edit_distance, word_level | 1.00 |
| bluish | blueish | edit_distance, word_level | 1.00 |

## 6. Dataset-Specific Analysis

### 6.1 XKCD Variants
- Total XKCD variants: 127,468
- Total affected responses: 1,350,001

### 6.2 Centore Variants
- Total Centore variants: 6,521

### 6.3 Overlapping Variants
- Names appearing as variants in both datasets: 1,571

## 7. Uncertainty Considerations

### 7.1 False Positive Risks
- Edit distance may match unrelated color names (e.g., 'rust' vs 'rose')
- Phonetic matching may be too aggressive for short words
- Word-level detection may over-correct compound names

### 7.2 False Negative Risks
- Novel misspellings not in rule database
- Edit threshold 0.85 may miss some typos
- Phonetic algorithms may miss some sound-alike variants

### 7.3 Recommendations
1. High-confidence variants (>=0.9) can be applied automatically
2. Multi-method variants are more reliable than single-method
3. High-response-count variants should be prioritized
4. Consider manual review for edge cases

---

*Generated by Phase 2.1: Spelling Variant Detection*