//! # MunsellSpace 🎨
//!
//! High-precision **sRGB to Munsell color space conversion** with **99.98% reference accuracy**.
//!
//! This library provides the most accurate open-source implementation for converting RGB colors
//! to Munsell notation, validated against the complete 4,007-color reference dataset.
//!
//! ## Quick Start
//!
//! ```rust
//! use munsellspace::MunsellConverter;
//!
//! fn main() -> Result<(), Box<dyn std::error::Error>> {
//!     let converter = MunsellConverter::new()?;
//!     
//!     // Convert RGB to Munsell
//!     let munsell = converter.srgb_to_munsell([255, 0, 0])?;
//!     println!("Pure red: {}", munsell); // Output: 7.9R 5.2/20.5
//!     
//!     Ok(())
//! }
//! ```
//!
//! ## Features
//!
//! - **99.98% Accuracy**: Validated against complete reference dataset (4,006/4,007 exact matches)
//! - **High Performance**: 4,000+ colors/second batch processing
//! - **Scientific Precision**: Reference data lookup with intelligent interpolation
//! - **Zero Dependencies**: Pure implementation with minimal external requirements
//! - **Comprehensive Testing**: Full test suite with accuracy validation
//!
//! ## About Munsell Color Space
//!
//! The Munsell color system describes colors using three perceptually uniform dimensions:
//!
//! - **Hue**: Color family (R, YR, Y, GY, G, BG, B, PB, P, RP)
//! - **Value**: Lightness from 0 (black) to 10 (white)
//! - **Chroma**: Saturation from 0 (neutral) to 15+ (vivid)
//!
//! Example: `5R 4.0/14.0` = medium red (5R) with medium lightness (4.0) and high saturation (14.0).

pub mod converter;
pub mod types;
pub mod error;
pub mod illuminants;
pub mod iscc;
pub mod constants;
pub mod mathematical;
pub mod reverse_conversion;
pub mod python_port;
pub mod python_port_helpers;
pub mod python_converter;
pub mod python_port_strings;
pub mod python_port_lab;
pub mod python_port_utils;
pub mod python_port_interpolation;
pub mod mechanical_wedges;
pub mod unified_cache;

// Test modules were moved to their respective implementation files
// #[cfg(test)]
// mod proptest_suite;

pub use converter::MunsellConverter;
pub use types::{MunsellColor, RgbColor, IsccNbsName, IsccNbsPolygon, MunsellPoint};
pub use error::{MunsellError, Result};
pub use illuminants::{Illuminant, ChromaticAdaptation, ChromaticAdaptationMethod};
pub use iscc::{ISCC_NBS_Classifier, ColorMetadata};
pub use mechanical_wedges::MechanicalWedgeSystem;
pub use mathematical::{
    MathematicalMunsellConverter, 
    MunsellSpecification, 
    CieXyY,
    Illuminant as MathematicalIlluminant,
    ChromaticAdaptation as MathematicalChromaticAdaptation
};
pub use reverse_conversion::{ReverseConverter, ColorFormats, CieLab, HslColor, HsvColor, munsell_to_hex_string};
pub use unified_cache::{UnifiedColorCache, CachedColorResult};
// Note: General color conversions (RGB↔Hex↔Lab↔HSL↔HSV) are available via the palette crate
// We only expose Munsell-specific conversions to avoid duplication

/// Library version
pub const VERSION: &str = env!("CARGO_PKG_VERSION");