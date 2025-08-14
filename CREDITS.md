# Credits and Acknowledgments

## Primary Attribution

### Python Colour Science Library

This Rust implementation of Munsell color space conversion is based on the mathematical algorithms from the **[Python Colour Science library](https://github.com/colour-science/colour)**.

The Python Colour library is a comprehensive color science package that provides:
- Munsell color notation conversion algorithms
- Color space transformations
- Chromatic adaptation methods
- Illuminant definitions

We are deeply grateful to the Colour Science team for their:
- Comprehensive and well-documented implementation
- Rigorous scientific approach to color science
- Open-source contribution to the community
- Extensive test data and validation methods

**Original Python Implementation:**
- Repository: https://github.com/colour-science/colour
- Documentation: https://colour.readthedocs.io/
- License: BSD-3-Clause
- Authors: Colour Developers

**Specific Algorithms Used:**
- `colour.notation.munsell` module for Munsell conversion
- XYZ to Munsell mathematical transformations
- Chromatic adaptation matrices (Bradford, CAT02)
- Illuminant specifications (C, D65, F7)

## Scientific References

### Munsell Color System

1. **Munsell Renotation System (1943)**
   - Newhall, S. M., Nickerson, D., & Judd, D. B. (1943)
   - "Final Report of the OSA Subcommittee on the Spacing of the Munsell Colors"
   - *Journal of the Optical Society of America*, 33(7), 385-418

2. **Munsell Color Science Laboratory**
   - Rochester Institute of Technology
   - Original renotation data and color specifications
   - https://www.rit.edu/cos/colorscience/

### ISCC-NBS Color System

1. **ISCC-NBS Method of Designating Colors**
   - Kelly, Kenneth L. & Judd, Deane B. (1976)
   - *Color: Universal Language and Dictionary of Names*
   - National Bureau of Standards Special Publication 440
   - U.S. Government Printing Office, Washington, D.C.

2. **Inter-Society Color Council**
   - Original color boundary definitions
   - Standardized color naming system
   - https://iscc.org/

### Color Space Standards

1. **CIE Standards**
   - International Commission on Illumination (CIE)
   - CIE 1931 XYZ color space
   - Standard illuminants (C, D65)
   - https://cie.co.at/

2. **ITU-R BT.709**
   - International Telecommunication Union
   - sRGB color space specification
   - Gamma correction standards

3. **IEC 61966-2-1:1999**
   - sRGB color space standard
   - Default RGB color space for the Internet

## Data Sources

### Reference Datasets

1. **Munsell Renotation Data**
   - 4,007 color samples with validated RGB-Munsell mappings
   - Based on spectrophotometric measurements
   - Validated through multiple studies

2. **ISCC-NBS Color Boundaries**
   - 267 color categories with polygon definitions
   - Munsell notation ranges for each color name
   - Validated perceptual groupings

3. **Test Data**
   - W3 Schools color dataset
   - Centore Munsell dataset
   - Various validation datasets from color science literature

## Contributors

### Project Maintainers
- Chris G. - Project lead and primary implementation

### Community Contributors
- See [GitHub Contributors](https://github.com/chrisgve/MunsellSpace/graphs/contributors)

### Special Thanks

We extend special thanks to:

1. **The Rust Community**
   - For excellent tooling and documentation
   - Cargo ecosystem and crates.io
   - Helpful community support

2. **Color Science Researchers**
   - Decades of research in color perception
   - Published papers and datasets
   - Open scientific collaboration

3. **Open Source Community**
   - For making scientific computing accessible
   - Sharing knowledge and implementations
   - Collaborative development model

## License Compatibility

This project is released under the MIT License, which is compatible with the BSD-3-Clause license of the Python Colour library. We have:

- Properly attributed the original work
- Maintained scientific accuracy
- Contributed back to the open-source community
- Respected all licensing requirements

## How to Cite

If you use MunsellSpace in your research or project, please cite both this library and the Python Colour library:

### MunsellSpace (This Library)
```bibtex
@software{munsellspace2025,
  author = {MunsellSpace Contributors},
  title = {MunsellSpace: High-precision sRGB to Munsell color space conversion for Rust},
  year = {2025},
  url = {https://github.com/chrisgve/MunsellSpace}
}
```

### Python Colour (Original Implementation)
```bibtex
@software{colour2024,
  author = {Colour Developers},
  title = {Colour: A comprehensive Python package for color science},
  year = {2024},
  url = {https://github.com/colour-science/colour}
}
```

## Contact

For questions about the implementation or to report issues:
- GitHub Issues: https://github.com/chrisgve/MunsellSpace/issues
- Discussions: https://github.com/chrisgve/MunsellSpace/discussions

---

Thank you to everyone who has contributed to making color science more accessible!