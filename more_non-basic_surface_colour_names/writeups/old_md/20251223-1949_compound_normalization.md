# Phase 2.3: Compound Name Normalization Report

## 1. Executive Summary

| Metric | Value |
|--------|-------|
| Total names analyzed | 175,844 |
| Single-word names | 33,087 |
| Two-word compounds | 62,382 |
| Three+ word compounds | 80,375 |
| Names with hyphens | 16,485 |
| Names with base color | 95,950 |
| Names with lightness modifier | 30,382 |
| Hyphenation variant groups | 4,945 |
| Word order variant groups | 7,525 |
| Canonical mappings generated | 11,103 |

## 2. Methodology

### 2.1 Compound Name Parsing
Each name is parsed into components:
- **Intensity modifier**: very, slightly, almost, etc.
- **Lightness modifier**: light, dark, pale, bright, etc.
- **Hue modifier**: greenish, bluish, etc.
- **Base color**: primary color (blue, red, etc.)
- **Secondary color**: for mixed colors (blue-green)
- **Descriptor**: object descriptors (sky, forest, etc.)

### 2.2 Normalization Methods

**Standard ordering**: [intensity] [lightness] [hue_mod] [base] [secondary]
- Example: 'very light greenish blue' is standard form

**Frequency-based selection**: Most common variant becomes canonical
- Example: If 'dark blue' has 5000 responses and 'blue dark' has 10,
  'dark blue' is canonical

### 2.3 Variant Detection

**Hyphenation variants**: Group names differing only in hyphenation
- 'blue green', 'blue-green', 'bluegreen' → same group

**Word order variants**: Group names with same words, different order
- 'dark blue', 'blue dark' → same group

## 3. Modifier Usage Analysis

### 3.1 Lightness Modifiers

| Modifier | Response Count |
|----------|---------------|
| light | 224,739 |
| dark | 153,281 |
| bright | 52,497 |
| pale | 46,326 |
| hot | 16,731 |
| deep | 16,040 |
| neon | 14,538 |
| pastel | 10,402 |
| dull | 8,374 |
| medium | 8,285 |
| dusty | 7,057 |
| faded | 4,849 |
| dirty | 4,423 |
| electric | 4,375 |
| soft | 2,607 |

### 3.2 Intensity Modifiers

| Modifier | Response Count |
|----------|---------------|
| very | 8,443 |
| slightly | 4,865 |
| almost | 2,202 |
| ultra | 174 |

## 4. Variant Examples

### 4.1 Hyphenation Variant Groups (Top 20)

| Normalized | Variants | Total Responses |
|------------|----------|-----------------|
| green | green, green-, green-- (+1 more) | 314,176 |
| blue | -blue-, __ blue, blue (+1 more) | 288,019 |
| pink | pink-, pink | 131,015 |
| red | red-, red | 69,929 |
| light blue | light - blue, light- blue, light blue (+2 more) | 58,388 |
| light green | light-green, light green, light  green | 49,968 |
| yellow | yellow, ___ yellow, yellow- | 44,075 |
| magenta | magenta --, magenta | 43,725 |
| grey | grey, grey- | 36,128 |
| sky blue | sky-blue, sky  blue, sky blue | 34,736 |
| lime green | lime  green, lime green, lime green (+1 more) | 31,506 |
| light purple | light  purple, light-purple, light purple | 29,734 |
| dark green | dark green, dark  green, dark-green | 24,017 |
| dark blue | dark-blue, dark  blue, dark blue | 23,534 |
| forest green | forest green, forest-green, forest  green (+1 more) | 19,387 |
| bright green | bright  green, bright green, bright-green | 18,861 |
| gray | gray, gray- | 18,242 |
| olive | olive, olive -_- | 17,553 |
| dark purple | dark-purple, dark purple, dark  purple (+1 more) | 16,916 |
| royal blue | royal-blue, royal blue, royal  blue | 15,073 |

### 4.2 Word Order Variant Groups (Top 20)

| Sorted Form | Variants | Total Responses |
|-------------|----------|-----------------|
| blue light | blue-light, light - blue, light- blue (+4 more) | 58,397 |
| green light | green light, green - light, light-green (+2 more) | 49,988 |
| blue sky | blue-sky, sky-blue, sky  blue (+2 more) | 34,802 |
| green lime | green lime, lime  green, lime green (+4 more) | 31,525 |
| light purple | purple light, light  purple, purple - light (+2 more) | 29,756 |
| dark green | green dark, dark green, dark  green (+2 more) | 24,027 |
| blue dark | blue - dark, blue dark, dark-blue (+3 more) | 23,541 |
| forest green | forest green, green forest, forest-green (+2 more) | 19,393 |
| bright green | bright  green, bright green, bright-green (+1 more) | 18,864 |
| dark purple | dark-purple, purple-dark, dark purple (+3 more) | 16,925 |
| green yellow | yellow_green, green-yellow, green -yellow (+12 more) | 16,515 |
| blue royal | blue - royal, royal-blue, blue royal (+2 more) | 15,078 |
| hot pink | pink hot, hot-pink, hot  pink (+1 more) | 14,172 |
| blue navy | navy-blue, blue navy, navy - blue (+3 more) | 13,656 |
| blue green | green -blue, green - blue, blue green (+8 more) | 13,524 |
| green pale | pale green, pale-green, pale  green (+3 more) | 13,496 |
| green olive | green-olive, olive green, olive green (+4 more) | 12,616 |
| brown light | light brown, light-brown, light  brown (+1 more) | 12,505 |
| blue grey | grey -blue, blue - grey, blue_grey (+9 more) | 11,881 |
| dark pink | dark  pink, pink-dark, pink dark (+2 more) | 11,847 |

## 5. Canonical Form Examples

| Variant | Canonical | Variant Count | Canonical Count |
|---------|-----------|---------------|-----------------|
| blue-light | light blue | 1 | 58,129 |
| light - blue | light blue | 3 | 58,129 |
| light- blue | light blue | 2 | 58,129 |
| blue light | light blue | 8 | 58,129 |
| light  blue | light blue | 38 | 58,129 |
| light-blue | light blue | 216 | 58,129 |
| green light | light green | 19 | 49,763 |
| green - light | light green | 1 | 49,763 |
| light-green | light green | 194 | 49,763 |
| light  green | light green | 11 | 49,763 |
| blue-sky | sky blue | 1 | 34,503 |
| sky-blue | sky blue | 206 | 34,503 |
| sky  blue | sky blue | 27 | 34,503 |
| blue sky | sky blue | 65 | 34,503 |
| green lime | lime green | 16 | 31,315 |
| lime  green | lime green | 13 | 31,315 |
| green - lime | lime green | 1 | 31,315 |
| lime green | lime green | 1 | 31,315 |
| lime-green | lime green | 177 | 31,315 |
| green-lime | lime green | 2 | 31,315 |
| purple light | light purple | 21 | 29,648 |
| light  purple | light purple | 11 | 29,648 |
| purple - light | light purple | 1 | 29,648 |
| light-purple | light purple | 75 | 29,648 |
| green dark | dark green | 9 | 23,932 |
| dark  green | dark green | 5 | 23,932 |
| dark-green | dark green | 80 | 23,932 |
| green - dark | dark green | 1 | 23,932 |
| blue - dark | dark blue | 1 | 23,443 |
| blue dark | dark blue | 5 | 23,443 |

## 6. Normalization Recommendations

### 6.1 Hyphenation Convention
- **Recommendation**: Use space-separated form for mixed colors
- Rationale: More common in XKCD data
- Example: 'blue green' not 'blue-green'

### 6.2 Word Order Convention
- **Recommendation**: [modifier] [color] order
- Rationale: English convention, more natural
- Example: 'dark blue' not 'blue dark'

### 6.3 Modifier Normalization
- Normalize synonyms: 'really' → 'very', 'lite' → 'light'
- Keep distinct modifiers: 'dark' ≠ 'deep' ≠ 'dim'

## 7. Uncertainty Considerations

### 7.1 Semantic Differences
Some word orders may carry different meanings:
- 'green blue' (green with blue tint) vs 'blue green' (blue with green tint)
- Need human validation for semantic equivalence

### 7.2 Missing Hyphens in Data
Some compound colors may be semantically different:
- 'hot pink' (the color) vs 'hot-pink' (very pink)
- Context and coordinate data can help disambiguate

---

*Generated by Phase 2.3: Compound Name Normalization*