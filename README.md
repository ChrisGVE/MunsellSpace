# MunsellSpace 🎨

High-precision **sRGB to Munsell color space conversion** library with **ISCC-NBS color naming system** support.

[![Crates.io](https://img.shields.io/crates/v/munsellspace.svg)](https://crates.io/crates/munsellspace)
[![Downloads](https://img.shields.io/crates/d/munsellspace.svg)](https://crates.io/crates/munsellspace)
[![Documentation](https://docs.rs/munsellspace/badge.svg)](https://docs.rs/munsellspace)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Build Status](https://img.shields.io/github/actions/workflow/status/chrisgve/MunsellSpace/ci.yml?branch=main)](https://github.com/chrisgve/MunsellSpace/actions)

## Overview

MunsellSpace is a high-performance Rust library for converting sRGB colors to Munsell color notation and ISCC-NBS color names. This implementation is based on the mathematical algorithms from the [Python Colour Science library](https://github.com/colour-science/colour), providing accurate color space transformations with comprehensive thread safety support.

## ✨ Features

- **High-Precision Conversion**: Multiple mathematical conversion algorithms with configurable illuminants
- **ISCC-NBS Classification**: Convert colors to standardized ISCC-NBS color names (267 categories)
- **Multiple Illuminants**: Support for C, D65, and F7 illuminants with chromatic adaptation
- **Thread-Safe Architecture**: Full `Send + Sync` support for concurrent processing
- **Comprehensive API**: Support for RGB, Lab, and hex color input formats
- **Performance Optimized**: Efficient caching and parallel processing capabilities
- **Scientific Accuracy**: Based on established color science algorithms and standards

## 🚀 Quick Start

### Installation

Add to your `Cargo.toml`:

```toml
[dependencies]
munsellspace = "1.0"
```

### Basic Usage

```rust
use munsellspace::{MunsellConverter, IsccNbsClassifier};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Create converter for Munsell notation
    let converter = MunsellConverter::new()?;
    
    // Convert RGB to Munsell
    let munsell = converter.srgb_to_munsell([255, 0, 0])?;
    println!("Pure red: {}", munsell); // Output: 7.9R 5.2/20.5
    
    // Create ISCC-NBS classifier
    let classifier = IsccNbsClassifier::new()?;
    
    // Classify color to ISCC-NBS name
    let color_name = classifier.classify_rgb([255, 0, 0])?;
    println!("Color name: {:?}", color_name); // Output: vivid red
    
    Ok(())
}
```

## 📊 Color Systems

### Munsell Color System

The [Munsell color system](https://en.wikipedia.org/wiki/Munsell_color_system) describes colors using three perceptually uniform dimensions:

- **Hue**: Color family (R, YR, Y, GY, G, BG, B, PB, P, RP)
- **Value**: Lightness from 0 (black) to 10 (white)
- **Chroma**: Saturation from 0 (neutral) to variable maximum

**Notation Format**: `HUE VALUE/CHROMA` (e.g., `5R 4.0/14.0`)

### ISCC-NBS Color System

The Inter-Society Color Council - National Bureau of Standards (ISCC-NBS) system provides standardized color names for 267 distinct color categories. Each color is defined by:

- Numerical identifier (1-267)
- Descriptive name (e.g., "vivid red", "light grayish blue")
- Polygonal region in Munsell color space

## 🔬 Technical Details

### Mathematical Conversion Pipeline

The library implements a sophisticated color conversion pipeline:

1. **sRGB → Linear RGB**: Gamma correction removal
2. **Linear RGB → XYZ**: Color space transformation (ITU-R BT.709)
3. **XYZ → xyY**: Chromaticity and luminance separation
4. **Chromatic Adaptation**: Optional adaptation between illuminants
5. **xyY → Munsell**: Mathematical transformation to Munsell notation
6. **Munsell → ISCC-NBS**: Geometric point-in-polygon classification

### Supported Illuminants

- **C**: Traditional daylight (used in original Munsell specifications)
- **D65**: Standard daylight (sRGB native illuminant)
- **F7**: Fluorescent light source

### Chromatic Adaptation Methods

- **XYZ Scaling**: Simple von Kries transformation
- **Bradford**: More sophisticated adaptation matrix
- **CAT02**: Advanced chromatic adaptation transform

## 🔒 Thread Safety

All public types implement `Send + Sync` for safe concurrent usage:

```rust
use munsellspace::{MunsellConverter, IsccNbsClassifier};
use std::sync::Arc;
use std::thread;

let converter = Arc::new(MunsellConverter::new()?);
let classifier = Arc::new(IsccNbsClassifier::new()?);

let mut handles = vec![];

for thread_id in 0..4 {
    let conv = Arc::clone(&converter);
    let class = Arc::clone(&classifier);
    
    let handle = thread::spawn(move || {
        let munsell = conv.srgb_to_munsell([255, 0, 0])?;
        let color_name = class.classify_rgb([255, 0, 0])?;
        println!("Thread {}: {} -> {:?}", thread_id, munsell, color_name);
        Ok::<(), Box<dyn std::error::Error + Send + Sync>>(())
    });
    
    handles.push(handle);
}

for handle in handles {
    handle.join().unwrap()?;
}
```

## 📈 Performance

- **Single conversion**: <1ms per color
- **Batch processing**: 4,000+ colors/second
- **Memory usage**: <100MB for complete reference dataset
- **Caching**: Automatic result caching for repeated conversions

## 📚 API Documentation

For detailed API documentation, visit [docs.rs/munsellspace](https://docs.rs/munsellspace).

Key modules:
- `converter`: Core Munsell conversion functionality
- `iscc`: ISCC-NBS classification system
- `types`: Color type definitions and validation
- `illuminants`: Illuminant definitions and adaptation
- `mathematical`: Mathematical conversion algorithms

## 🛠️ Development

### Building from Source

```bash
# Clone repository
git clone https://github.com/chrisgve/MunsellSpace.git
cd MunsellSpace

# Build library
cargo build --release

# Run tests
cargo test

# Run benchmarks
cargo bench

# Generate documentation
cargo doc --open
```

### Testing

```bash
# Run all tests
cargo test

# Run with output
cargo test -- --nocapture

# Run specific test
cargo test test_name

# Run benchmarks
cargo bench
```

## 🙏 Acknowledgments & Credits

This library builds upon decades of color science research and open-source contributions:

### Core Algorithms
- **[Python Colour Science](https://github.com/colour-science/colour)**: This implementation is based on the mathematical algorithms from the Python `colour-science` library, specifically the Munsell color notation conversion functions. We are deeply grateful for their comprehensive and well-documented implementation.
- **[Paul Centore's Munsell Research](http://www.munsellcolorscienceforpainters.com/)**: This library incorporates methodology from Dr. Paul Centore's work on sRGB-to-Munsell conversion, including his chromatic adaptation techniques and validation datasets.

### Scientific References
- **Semantic Color Names**: Centore, P. (2020). [Beige, aqua, fuchsia, etc.: Definitions for some non-basic surface colour names](https://www.jaic-colour.org/). *Journal of the International Colour Association*, 25, 24-54. The 30 semantic color overlays in this library are derived from the convex polyhedra defined in this paper.
- **Munsell Renotation Data**: Based on the original Munsell renotation studies (1943) and subsequent refinements
- **ISCC-NBS Method of Designating Colors**: Kelly, K.L. & Judd, D.B. (1976). Color: Universal Language and Dictionary of Names
- **CIE Standards**: International Commission on Illumination specifications for color spaces and illuminants
- **ITU-R BT.709**: International standard for sRGB color space transformation

### Data Sources
- **Munsell Renotation Dataset**: Original renotation data from the Munsell Color Science Laboratory
- **[ISCC-NBS Definitions](https://iscc.org/)**: The 267 color categories and Munsell-space boundaries are derived from the Inter-Society Color Council (ISCC) and National Bureau of Standards (NBS) publications
- **Reference RGB Values**: Validated sRGB to Munsell mappings from multiple sources

### Community
- The Rust community for excellent tooling and support
- Contributors to the color science field for their research and publications
- Open-source maintainers who make scientific computing accessible

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Repository**: [github.com/chrisgve/MunsellSpace](https://github.com/chrisgve/MunsellSpace)
- **Documentation**: [docs.rs/munsellspace](https://docs.rs/munsellspace)
- **Issue Tracker**: [GitHub Issues](https://github.com/chrisgve/MunsellSpace/issues)
- **Python Colour Science**: [colour-science/colour](https://github.com/colour-science/colour)
- **Munsell Color System**: [munsell.com](https://munsell.com/)

---

**MunsellSpace** - High-precision color space conversion for Rust 🦀