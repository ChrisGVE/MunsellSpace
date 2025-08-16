# FUTURE development

This document describes future development to this crate, mostly around the description of colors

## 1. Temperature bias (within any hue family)

### 1.1 Space and adaptation

- Pick a perceptual, near uniform space for boundary math: **CAM16-UCCS** (ideal), **CIELAB** (OK), or **Munsell** to stay strictly in that system
- Normalize viewing condition via chromatic adaptation (e.g., **CAT16** or **CAT02**) so deltas are comparable across illuminants.

### 1.2 Canonical family centers

- For each family (e.g. Yellow), define a **canonical center hue** $h_0$ in your chosen space:
  - Munsell: e.g., **5Y** for Yellow, **5BG** for Blue-Green, etc.
  - LAB/CAM16: a canonical **hue angle** $h_0$
- Optionally define a **local warm axis** (toward red/orange) and **cool axis** (toward blue/green) relative to $h_0$.

### 1.3 Signed hue deviation and wrap

- Compute **signed hue deviation** $\Delta h = \text{wrap_angle}(h-h_0)$ in $[-180^o, 180^o]$.
- Define **Temperature score $T$** as a normalized projection on the warm-cool axis:
  - Simple: $T=\Delta h / H_\text{max}$, where $H_\text{max}$ is a family-specific half-span (e.g., the midpoint to the neighboring families).
  - Better: use a **directional dot product** in a*,b* (or J'a'b') onto a unit warm axis vector; sign gives warm/cool, magnitude gives strength

### 1.4 Modulate by chroma (and lightness)

- Temperature judgments collapse near neutral; apply **grating** by chroma $C$:
  - If $C<C_{\epsilon}:T:=0$ (neutral/undetermined).
  - Else: $T:=T \cdot g(C)$, with $g(C)$ rising from 0->1 (e.g., logistic or piecewise linear).
- Optionally damp very dark/very light extremes where hue discrimination is weak (lightness-dependent weight).

### 1.5 Thresholding and labels

- Provide both **continuous** $T$ and **categorical** labels:
  - $\|T\|<\tau_0$ -> **neutral**; $T>=\tau_1$ -> **warm**; $T<=-\tau_1$ -> **cool**; middle band **slightly warm/cool**.
- Calibrate $\tau$s by visual trials or from literature (you can expose them in coding).

### 1.6 Grays (special case)

- In LAB/CAM16, use **axis sign** for near-neutral:
  - $b^{*}>b_{\epsilon}$ (or J'b' > 0) -> **warm gray**, $b^{*}<-b_{\epsilon}$ -> **cool gray**, $\|b^{*}\|<=b_{\epsilon}$ -> **neutral gray**.
- Optionally include the **a\*** axis: project the (**a\***, **b\***) vector onto your family's warm axis for consistency across all hue

## 2. Semantic overlay families (fuchsia, sand, teal, turquoise, chartreuse, ...)

### 2.1 Philosophy

- Keep **ISCC–NBS** as the categorical backbone.
- Add **overlays** as **soft regions** in perceptual space that may **span multiple ISCC boxes**.
- Overlays are **additive**, not replacements; they produce an `alt_color_name`.

### 2.2 Region definition (soft wedges)

For each overlay term, define a **fuzzy region** as constraints on **hue angle**, **chroma**, and **lightness**:

- Example Teal:
  - Hue: between **blue and green** (e.g., CAM16 hue $h \in [190^o, 210^o]$ - pick ranges that match your audience perception).
  - Chroma: moderate ($C \in [C_\text{min},C_\text{max}]$) to exclude dull gray-green and neon cyan.
  - Lightness: mid-range ($J \in [J_\text{min}, J_\text{max}]$) to avoid "deep blue" or "mint".
- Example Turquoise:
  - Hue slightly **greener and lighter** than teal (shift the hue interval and raise lightness window).
- Example Chartreuse:
  - Hue straddling yellow–green, with **higher chroma** and mid–high lightness.
- Example Sand:
  - Hue **yellow->orange**; **low–moderate chroma**; **mid lightness** (avoid tan’s darker band and cream’s lighter band).
- Example Fuchsia:
  - Hue **magenta–purplish pink**; **high chroma**; **mid–high lightness**.

### 2.3 Soft membership functions

- Use **triangular/trapezoidal membership** per dimension:
  - $\mu_h(h), \mu_C(C), \mu_J(J) \in [0,1]$
- Combine by **min** or **product** to yield an overall membership $\mu \in [0,1]$.
- This gives **graded matches** (useful for ranking alternate names and avoiding hard boundary jumps).

### 2.4 Priority and tie-breakers

When multiple overlays match:

- Define a priority order (domain-specific; e.g., “teal” before generic “bluish green”).
- Or pick the $\text{max} \mu$; if ties, choose the **closest exemplar centroid** in J'a'b' Euclidean distance.

### 2.5 Exemplars and data-driven tuning

- Pick a handful of exemplar swatches per term (e.g., Centore’s sRGB centroids near relevant ISCC bins, or curated ink swatches).
- Compute their centroid and covariance in J’a’b’.
- Set initial intervals (or Gaussian radii) from exemplar spread; **expand** slightly for practical coverage.
- Iterate with **user feedback** (ink community!) to nudge boundaries.

### 2.6 Stability across illuminants

- Since you support multiple illuminants, do all overlay tests in the adapted, uniform space (e.g., CAM16-UCS under stated viewing conditions), not raw RGB.
- Document the **default illuminant and surround**; expose them in config.

## 3. Integrating temperature with overlays

- Each overlay can **carry a temperature descriptor** derived from 1.
  - e.g., "**warm teal**" if its local $T>\tau$ (toward cyan-green) or "**cool teal**" if $T<-\tau$ (toward blue/cyan), depending on how you orient the family center.
- For labels, prefer "**slightly warm/cool**" when $\|T\|$ is near threshold to avoid jarring names.

## 4. Decision pipeline (high level)

1. Convert input to chosen space (with adaptation).
2. **Map** to ISCC-NBS (current logic).
3. **Computer temperature $T$** (continuous + categorical)
4. **Evaluate overlay memberships $\mu_k$** for all semantic families.
5. **Choose overlay** by max $\mu$ with priority/tie-breakers; attach as `alt_color_name`.
6. **Compose final descriptor**:

- `[temperature qualifier]* [overlay or ISCC name] [ISCC modifier]`
- Example: "**slightly warm teal, light**", or "**cool light gray**"

## 5. Calibration and QA

- **Unit tests** on handpicked edge cases that sit near multiple families.
- **Round-trip tests** across illuminants to verify label stability (or document expected shifts).
- **Human eval**: small panel ratings for temperature and semantic fit; adjust thresholds.

---

## APPENDIX:

# Future TODO: Warm–Cool Color Axis and Semantic Overlays for `munsellspace`

This document is a cleaned transcript of a ChatGPT conversation with references,
intended as a **future development roadmap** for extending `munsellspace`.

---

## Conversation Notes

### User’s Context

- Built a Rust crate **munsellspace** for RGB/Lab <-> Munsell conversions (with selectable illuminant).
- Has full **ISCC–NBS mapping** (267 descriptors).
- Added `alt_color_name` field for evocative naming (e.g., _Chartreuse_, _Teal_, _Turquoise_).
- Wants to explore adding **temperature bias** (_warm yellow vs. cool yellow; warm gray vs. cool gray_) and **semantic overlay categories** (e.g., _fuchsia_, _sand_) on top of ISCC–NBS.

---

## Key Insights from Chat

### 1. Warm vs. Cool Colors in Color Science

- Not a **physical property**; rather a **perceptual/psychological axis**.
- Still possible to quantify:
  - **Correlated Color Temperature (CCT)** for light sources.
  - **Warm–cool ratings** in perceptual models (Ou et al. 2004; Hård & Sivik 1981).
  - **CIELAB/CAM16 hue angles**: red/orange/yellow perceived as warmer; blue/green/cyan as cooler.

**Within a hue family**:

- A warm yellow tends toward **red/orange**.
- A cool yellow tends toward **green**.
- A warm gray → slight red/yellow bias; cool gray → slight blue/green bias.

---

### 2. Absolute vs. Relative Warmth

- **Relative (artistic practice):** a yellow looks cool only compared to a redder yellow nearby.
- **Absolute (color science):** define neutral family centers and measure hue bias.

Example:

- In **CIELAB**, grays:
  - \(b^\* > 0\) → warm gray,
  - \(b^\* < 0\) → cool gray.

---

### 3. Temperature Bias Algorithm (Conceptual)

1. Convert to uniform space (CIELAB or CAM16-UCS).
2. Define **canonical family centers** (e.g., 5Y for Yellow).
3. Compute signed hue deviation from canonical hue.
4. Normalize to get a continuous **temperature score T**.
5. Gate by chroma (and lightness) so neutrals don’t falsely register warm/cool.
6. Threshold into **categorical labels**: warm / cool / neutral / slightly warm / slightly cool.
7. Special case for **grays** using b\* (yellow–blue axis).

---

### 4. Semantic Overlay Families (Beyond ISCC–NBS)

ISCC–NBS lacks some **artist-recognized categories** (Centore). Useful additions:

- **Fuchsia** – vivid purplish pink.
- **Sand** – low-chroma yellow/orange/brown tone.
- **Teal** – balanced green–blue.
- **Turquoise** – greener, lighter than teal.
- **Chartreuse** – vivid yellow–green.

**Overlay logic:**

- Define fuzzy regions in hue–chroma–lightness space.
- Assign membership score.
- Pick strongest match as `alt_color_name`.
- Overlays are **additive**, not replacements: retain ISCC box _and_ semantic overlay.

---

### 5. Decision Pipeline

1. Convert color to perceptual space.
2. Map to ISCC–NBS category.
3. Compute temperature bias.
4. Evaluate overlay memberships (fuchsia, sand, teal, etc.).
5. Choose overlay (highest membership).
6. Construct final descriptor:

Example outputs:

- _Cool Light Gray_
- _Slightly Warm Teal, Light_
- _Vivid Fuchsia_

---

### 6. Future TODO Items

- [ ] Implement **absolute temperature axis** (warm/cool bias).
- [ ] Define **semantic overlays** for missing categories (fuchsia, sand, teal, turquoise, chartreuse).
- [ ] Keep ISCC–NBS intact, add overlays in `alt_color_name`.
- [ ] Provide both **continuous T score** and categorical labels.
- [ ] Document illuminant & surround assumptions.
- [ ] Validate with user feedback (fountain pen ink community).

---

## 📚 References

### ISCC–NBS & Historical Foundations

1. Kelly, K. L., & Judd, D. B. (1955). _The ISCC–NBS method of designating colors and a dictionary of color names._  
   [NBS Miscellaneous Publication 212 (PDF)](https://nvlpubs.nist.gov/nistpubs/Legacy/MP/nbsmiscpub212.pdf)

2. Nickerson, D. (1949). _History of the Munsell color system and its scientific application._ _JOSA_, 39(12), 968–974.  
   [DOI link](https://doi.org/10.1364/JOSA.39.000968)

### Paul Centore’s Work

3. Centore, P. (2012). _sRGB Centroids for the ISCC–NBS Colour System._  
   [PDF link](https://www.munsellcolourscienceforpainters.com/ColourSciencePapers/sRGBCentroidsForTheISCCNBSColourSystem.pdf)

4. Centore, P. – various writings on Munsell, interpolation, semantic extensions.  
   [Munsell Colour Science for Painters](https://www.munsellcolourscienceforpainters.com/)

### Warm–Cool Perception & Color Emotion

5. Hård, A., & Sivik, L. (1981). _NCS – Natural Color System._

6. Ou, L.-C., Luo, M. R., Woodcock, A., & Wright, A. (2004). _Colour emotions for single colours._ _Color Research & Application_, 29(3), 232–240.  
   [DOI link](https://doi.org/10.1002/col.20010)

7. Ou, L.-C., Luo, M. R., Woodcock, A., & Wright, A. (2004). _Colour combinations._ _Color Research & Application_, 29(4), 292–298.  
   [DOI link](https://doi.org/10.1002/col.20024)

8. Sivik, L., & Taft, C. (1994). _Color naming: A mapping in the NCS colour solid._ _Scandinavian Journal of Psychology_, 35(2), 144–164.

### Color Appearance & Uniform Spaces

9. Luo, M. R., Cui, G., & Li, C. (2006). _Uniform colour spaces based on CIECAM02._ _Color Research & Application_, 31(4), 320–330.

10. Fairchild, M. D. (2013). _Color Appearance Models_ (3rd ed.). Wiley.

### Semantic Gaps & Overlays

11. Berlin, B., & Kay, P. (1969). _Basic Color Terms: Their Universality and Evolution._

12. ISCC–NBS discussion on missing families (archived):  
    [extradomestic58 RSS archive](https://extradomestic58.rssing.com/chan-32772665/latest.php)

---
