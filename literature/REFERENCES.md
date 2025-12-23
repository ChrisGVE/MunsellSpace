# Literature References

This document contains citations and links to academic papers and resources used in the development of MunsellSpace's semantic overlay functionality.

## Primary References

### Semantic Overlay Methodology

**Centore, P. (2020)**
"Beige, aqua, fuchsia, etc.: Definitions for some non-basic surface colour names"
*Journal of the International Colour Association*, 25, 24-54.

- **DOI:** Not publicly available
- **Abstract:** Defines convex hull polyhedra in Munsell space for 20 non-basic color names using CAUS fabric samples.
- **Supplementary Data:** PolyhedronFiles.zip (convex hull vertex/face data)
- **License:** Academic use - NOT redistributable without journal permission

### Color Naming Survey Data

**Munroe, R. (2010)**
"Color Survey Results"
*XKCD Blog*

- **URL:** https://blog.xkcd.com/2010/05/03/color-survey-results/
- **Data URL:** https://xkcd.com/color/rgb/
- **License:** CC0 Public Domain
- **Notes:** ~3.4 million color naming responses, freely redistributable

### ISCC-NBS Color System

**Kelly, K.L. & Judd, D.B. (1976)**
*Color: Universal Language and Dictionary of Names*
National Bureau of Standards Special Publication 440.
U.S. Government Printing Office, Washington, D.C.

- **License:** Public Domain (U.S. Government work)
- **Notes:** Defines 267 color categories with Munsell boundaries

### Munsell Color System

**Newhall, S.M., Nickerson, D., & Judd, D.B. (1943)**
"Final Report of the OSA Subcommittee on the Spacing of the Munsell Colors"
*Journal of the Optical Society of America*, 33(7), 385-418.

- **DOI:** 10.1364/JOSA.33.000385
- **License:** Available through OSA

### Color Space Standards

**IEC 61966-2-1:1999**
"Multimedia systems and equipment - Colour measurement and management - Part 2-1: Colour management - Default RGB colour space - sRGB"

- **Publisher:** International Electrotechnical Commission
- **License:** Proprietary standard (purchase required)

**ITU-R BT.709-6 (2015)**
"Parameter values for the HDTV standards for production and international programme exchange"

- **URL:** https://www.itu.int/rec/R-REC-BT.709
- **License:** Freely available from ITU

## Software References

### Python Colour Science Library

**Colour Developers (2015-present)**
*Colour: A comprehensive Python package for color science*

- **Repository:** https://github.com/colour-science/colour
- **Documentation:** https://colour.readthedocs.io/
- **License:** BSD-3-Clause
- **Notes:** Reference implementation for Munsell conversion algorithms

## Licensing Notes

### Papers That Cannot Be Redistributed

Most academic journal articles are protected by copyright and cannot be included directly in this repository, even if freely accessible online. This includes:

- Centore (2020) - Copyright held by Journal of the International Colour Association
- Newhall et al. (1943) - Copyright held by Optical Society of America

### Freely Redistributable Resources

The following can be included:
- XKCD color survey data (CC0)
- U.S. Government publications (Public Domain)
- Open-source software (per their licenses)

## How to Cite MunsellSpace

If using MunsellSpace in academic work, please cite:

```bibtex
@software{munsellspace2025,
  author = {MunsellSpace Contributors},
  title = {MunsellSpace: High-precision sRGB to Munsell color space conversion},
  year = {2025},
  url = {https://github.com/chrisgve/MunsellSpace},
  note = {Rust library with Python bindings}
}
```

And acknowledge the underlying references as appropriate.
