# Changelog

All notable changes to MunsellSpace will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Ready for production publication to crates.io
- Merged feature/true-mathematical-conversion branch to main

## [1.2.2] - 2025-12-28

### Fixed
- **ISCC-NBS modifiers now always applied**: The `describe()` method was incorrectly only applying
  modifiers (vivid, dark, pale, etc.) when `BaseColorSet::Extended` was selected. Modifiers are now
  correctly applied regardless of whether Standard or Extended base colors are used.

### Changed
- **Simplified `OverlayMode` API**: Renamed variants for clarity
  - `Never` → `Ignore`: Always use ISCC-NBS base colors, ignore semantic overlays
  - `WhenMatching`/`Nearest` → `Include`: Use nearest semantic overlay when available
  - The previous three-mode system was confusing; the new two-mode system is clearer
- Updated documentation to reflect correct modifier behavior

### Migration from 1.2.1
- Replace `OverlayMode::Never` with `OverlayMode::Ignore`
- Replace `OverlayMode::WhenMatching` or `OverlayMode::Nearest` with `OverlayMode::Include`
- Note: With the modifier fix, `FormatOptions::standard()` now returns "dark blue" instead of "blue"

## [1.2.1] - 2025-12-26

### Added
- **Flexible Characterization API**: New separation of objective color facts from formatting preferences
  - `ColorCharacterization`: Objective facts about a color (ISCC-NBS category, semantic matches, shade)
  - `FormatOptions`: User preferences for output formatting
  - `BaseColorSet`: Choose between Standard (13 colors) or Extended (267 with modifiers)
  - `OverlayMode`: Control semantic overlay usage (Ignore, Include)
- **New `characterize_*` methods on `ColorClassifier`**:
  - `characterize_srgb()`, `characterize_hex()`, `characterize_lab()`, `characterize_munsell_notation()`
  - Return `ColorCharacterization` for flexible formatting via `describe(&FormatOptions)`

### Changed
- `ColorDescriptor` now uses `ColorCharacterization` internally (backward compatible)
- Reduced code duplication in classifier implementation

## [1.2.0] - 2025-12-25

### Added
- **Unified Color Naming API**: Single entry point for all color naming systems
  - `ColorClassifier`: Unified interface for ISCC-NBS, extended, and semantic names
  - `ColorDescriptor`: Complete naming info with consistent modifiers across systems
  - `ColorModifier`: 22-variant enum for all ISCC-NBS modifiers (vivid, pale, dark, etc.)
- **Semantic Color Overlays**: 30 color names from Centore (2020) research
  - 20 non-basic: aqua, beige, coral, fuchsia, gold, lavender, lilac, magenta, mauve, navy, peach, rose, rust, sand, tan, taupe, teal, turquoise, violet, wine
  - 10 basic: blue, brown, gray, green, orange, pink, purple, red, white, yellow
- Color name registry with `known_color_names()`, `is_known_color()`, `color_name_count()`

### Deprecated
- `IsccNbsClassifier::classify_srgb()`, `classify_lab()`, `classify_hex()` - use `ColorClassifier` instead
- `semantic_overlay()`, `matching_overlays()`, `matching_overlays_ranked()`, `matches_overlay()`, `closest_overlay()` - use `ColorClassifier` and `ColorDescriptor` instead

### Attribution
- Added proper citations for Paul Centore's 2020 JAIC paper on non-basic surface colour names
- Added attribution for ISCC (Inter-Society Color Council) color category definitions

## [1.1.1] - 2025-12-24

### Added
- Attribution for Paul Centore's sRGB-to-Munsell conversion methodology and publications
- Attribution for ISCC (Inter-Society Color Council) color category definitions

## [1.1.0] - 2025-01-15

### Added
- **ISCC-NBS Color Classification System**: Complete implementation with 267 standardized color names
- **Multiple Illuminant Support**: C, D65, and F7 illuminants with chromatic adaptation
- **Chromatic Adaptation Methods**: XYZ Scaling, Bradford, and CAT02 transforms
- **Lab Color Space Support**: Direct Lab to Munsell conversion
- **Hex Color Support**: Convert hex color codes to Munsell notation
- **Thread Safety**: Full `Send + Sync` implementations for concurrent processing
- **Parallel Processing**: Rayon integration for batch operations
- **Caching System**: Automatic result caching for improved performance
- **Mechanical Wedge System**: Accurate ISCC-NBS boundary determination
- **Comprehensive Testing**: Property-based tests, edge cases, and benchmarks

### Changed
- Replaced `RefCell` with `Arc<RwLock>` for thread-safe caching
- Optimized mathematical operations with inline hints
- Enhanced documentation with detailed examples

### Fixed
- Mechanical wedge boundary rule for 1R wraparound case
- Cache method signatures after optimization
- Documentation examples to pass doc tests
- Gray/grey spelling consistency

### Performance Improvements
- Matrix operation optimizations
- Geometric calculation optimizations
- Inline hints for hot code paths
- Efficient caching strategies

## [1.0.0] - 2024-11-01

### Added
- Initial stable release of MunsellSpace library
- Core sRGB to Munsell color space conversion
- High-precision mathematical algorithms based on Python colour-science
- Reference dataset with 4,007 validated color mappings
- Comprehensive error handling with custom error types
- Full documentation with examples
- Integration tests with reference dataset validation
- MIT License

### Features
- **Core Conversion**: RGB to Munsell notation with high accuracy
- **Color Systems**: Support for all Munsell hue families (R, YR, Y, GY, G, BG, B, PB, P, RP)
- **Value Range**: 0 (black) to 10 (white)
- **Chroma Support**: 0 (neutral) to variable maximum
- **Batch Processing**: Efficient conversion of multiple colors
- **Type Safety**: Strong typing with validation

### Technical Implementation
- sRGB gamma correction (ITU-R BT.709)
- Linear RGB to XYZ transformation
- XYZ to xyY chromaticity conversion
- D65 illuminant as default
- Nearest neighbor matching for reference colors

### Performance
- Single conversion: <1ms per color
- Batch processing: 4,000+ colors/second
- Memory usage: <100MB for complete reference dataset

## [0.9.0] - 2024-10-15 (Beta)

### Added
- Beta release for testing and feedback
- Core conversion pipeline implementation
- Basic test suite
- Initial documentation draft

### Known Limitations
- Single-threaded processing only
- Limited to D65 illuminant
- No ISCC-NBS support
- No Lab color space support

---

## Migration Guides

### Upgrading from 1.0.0 to 1.1.0

#### New Features Available
- ISCC-NBS classification: Use `IsccNbsClassifier` for color names
- Multiple illuminants: Configure with `Illuminant::C`, `Illuminant::F7`
- Thread-safe processing: Share converters with `Arc<T>`
- Lab/Hex support: New conversion methods available

#### API Changes
- All types now implement `Send + Sync`
- New methods: `lab_to_munsell()`, `hex_to_munsell()`

### Upgrading from 0.9.0 to 1.0.0

Complete API redesign - please refer to new documentation.

## Credits

This library is based on the mathematical algorithms from the [Python Colour Science library](https://github.com/colour-science/colour). We are grateful for their comprehensive implementation and documentation.

## Contributors

See [GitHub Contributors](https://github.com/chrisgve/MunsellSpace/graphs/contributors) for the complete list.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.