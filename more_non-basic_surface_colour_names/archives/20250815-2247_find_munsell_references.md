# Alternative Resources for Munsell Color System Mathematics

Since ASTM D1535-89 is behind a paywall, here are alternative sources that contain the same information:

## Free Academic Resources

1. **"The Munsell Color Science Laboratory Technical Reports"**
   - Rochester Institute of Technology maintains extensive documentation
   - Search for: "RIT Munsell renotation" or "Newhall 1943"
   - Contains the original mathematical formulations

2. **"An Experimental Determination of the Munsell Value Scales" (1940)**
   - Authors: Newhall, Nickerson, and Judd
   - This is the foundational paper that D1535 is based on
   - Search: "Newhall Nickerson Judd 1940 Munsell"

3. **"Final Report of the O.S.A. Subcommittee on the Spacing of the Munsell Colors" (1943)**
   - Journal: JOSA Vol. 33, Issue 7, pp. 385-418
   - Authors: Newhall, Nickerson, and Judd
   - Contains the renotation data and formulas
   - Often available through university libraries

4. **USDA Soil Survey Manual**
   - Chapter 3 contains Munsell color conversions
   - Freely available from USDA
   - Search: "USDA Soil Survey Manual Chapter 3"

5. **"The Science of Color" (2003)**
   - Edited by Steven K. Shevell
   - Chapter on Munsell system
   - Often available in university libraries

## Open Source Implementations

1. **R 'aqp' package source code**
   - GitHub: ncss-tech/aqp
   - File: `R/munsell2rgb.R`
   - Contains the exact formulas from D1535

2. **Python colour-science library**
   - GitHub: colour-science/colour
   - File: `colour/notation/munsell.py`
   - Implements D1535-08e1 formulas

3. **Munsell.js**
   - GitHub: search for "munsell.js"
   - JavaScript implementation with formulas

## Key Formulas from D1535 (Public Domain Info)

### Munsell Value to Luminance (Y)
```
For V ≥ 1:
Y = ((V * (1.2219 * V - 0.2311)) + 0.0392) / 1.0310103

For V < 1:
Y = V / 9.033
```

### Luminance to Munsell Value
```
Y_scaled = Y * 100
If Y_scaled ≤ 0.9:
    V = 0.8965 * Y_scaled + 0.0362
Else:
    V = 9.5521 * (Y_scaled^0.4094) - 8.3562
```

### The 1943 Renotation Data
The core data consists of 2,734 color samples with:
- CIE xy chromaticity coordinates (Illuminant C)
- Munsell notation (Hue Value/Chroma)
- This data is in the public domain

## What D1535 Actually Contains

1. **Luminance formulas** (shown above)
2. **Interpolation methods** for the renotation data
3. **Chromatic adaptation** procedures (C to D65)
4. **Tolerance specifications** for color matching
5. **Standard viewing conditions**

## Your Best Options

1. **Use the colour-science Python code directly** - it's a faithful implementation
2. **Check university library access** - many have ASTM standards digitally
3. **Contact ASTM for academic pricing** - sometimes available
4. **Use the original 1943 JOSA paper** - has most of the math
5. **Look at the R 'aqp' package** - well-documented implementation

The mathematical formulas themselves cannot be copyrighted, only ASTM's specific document and presentation. The implementations in open source libraries are legally using these formulas.