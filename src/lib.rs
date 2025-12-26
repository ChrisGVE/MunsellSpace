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
//! - **Thread Safety**: Full support for concurrent usage with `Send + Sync` implementations
//! - **Semantic Color Names**: 30 color name overlays from Centore (2020) research
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
//!
//! ## Thread Safety
//!
//! All public types in MunsellSpace are thread-safe and implement `Send + Sync`. You can
//! safely share converters across multiple threads using `Arc<T>`:
//!
//! ```rust
//! use munsellspace::{MunsellConverter, IsccNbsClassifier};
//! use std::sync::Arc;
//! use std::thread;
//!
//! fn main() -> Result<(), Box<dyn std::error::Error>> {
//!     // Create shared instances
//!     let converter = Arc::new(MunsellConverter::new()?);
//!     let classifier = Arc::new(IsccNbsClassifier::new()?);
//!     
//!     let mut handles = vec![];
//!     
//!     // Spawn multiple threads for concurrent processing
//!     for thread_id in 0..4 {
//!         let converter_clone = Arc::clone(&converter);
//!         let classifier_clone = Arc::clone(&classifier);
//!         
//!         let handle = thread::spawn(move || {
//!             // Each thread can safely use the converters concurrently
//!             let munsell = converter_clone.srgb_to_munsell([255, 0, 0]).unwrap();
//!             
//!             if let (Some(hue), Some(chroma)) = (&munsell.hue, munsell.chroma) {
//!                 if let Ok(Some(iscc_color)) = classifier_clone.classify_munsell(hue, munsell.value, chroma) {
//!                     println!("Thread {}: {} -> {:?}", thread_id, munsell, iscc_color);
//!                 }
//!             }
//!         });
//!         
//!         handles.push(handle);
//!     }
//!     
//!     // Wait for all threads to complete
//!     for handle in handles {
//!         handle.join().unwrap();
//!     }
//!     
//!     Ok(())
//! }
//! ```
//!
//! Internal caches use `Arc<RwLock<T>>` for safe concurrent access, allowing multiple
//! readers or exclusive writers without data races.
//!
//! ## Semantic Color Names (v1.2.0+)
//!
//! MunsellSpace includes 30 semantic color name overlays derived from Paul Centore's
//! 2020 research paper "Beige, aqua, fuchsia, etc.: Definitions for some non-basic
//! surface colour names" (JAIC, 25, 24-54). These overlays define convex polyhedra
//! in Munsell space for each color name, allowing you to determine which color names
//! apply to any given Munsell color.
//!
//! ```rust
//! use munsellspace::{MunsellSpec, semantic_overlay, matching_overlays, get_registry};
//!
//! fn main() {
//!     // Parse a Munsell color and find matching color names
//!     let color = MunsellSpec::new(7.4, 6.2, 3.4); // Near aqua centroid
//!
//!     // Get the best-matching color name
//!     if let Some(name) = semantic_overlay(&color) {
//!         println!("Best match: {}", name);  // "aqua"
//!     }
//!
//!     // Get all matching color names (colors can match multiple names)
//!     let matches = matching_overlays(&color);
//!     println!("All matches: {:?}", matches);
//!
//!     // Access the complete registry for advanced use
//!     let registry = get_registry();
//!     println!("Registry has {} overlays", registry.len()); // 30
//! }
//! ```
//!
//! **Available color names (30 total):**
//! - **Non-basic (20)**: aqua, beige, coral, fuchsia, gold, lavender, lilac, magenta,
//!   mauve, navy, peach, rose, rust, sand, tan, taupe, teal, turquoise, violet, wine
//! - **Basic (10)**: blue, brown, gray, green, orange, pink, purple, red, white, yellow
//!
//! ## Unified Color Naming API (v1.2.0+)
//!
//! The [`ColorClassifier`] provides a unified interface for all color naming systems.
//! From any color input, get complete naming information with consistent modifiers
//! across ISCC-NBS standard, extended, and semantic names.
//!
//! ```rust
//! use munsellspace::{ColorClassifier, ColorModifier};
//!
//! fn main() -> Result<(), Box<dyn std::error::Error>> {
//!     let classifier = ColorClassifier::new()?;
//!
//!     // Classify any color format
//!     let desc = classifier.classify_srgb([180, 80, 60])?;
//!
//!     // Get descriptors from all naming systems
//!     println!("Standard: {}", desc.standard_descriptor());   // "moderate reddish brown"
//!     println!("Extended: {}", desc.extended_descriptor());   // "moderate rust"
//!     if let Some(semantic) = desc.semantic_descriptor() {
//!         println!("Semantic: {}", semantic);                 // "moderate rust"
//!     }
//!
//!     // The same modifier applies across all systems
//!     println!("Modifier: {:?}", desc.modifier);              // Moderate
//!
//!     // Format any modifier + color combination
//!     let formatted = ColorModifier::Vivid.format("coral");
//!     println!("{}", formatted);                              // "vivid coral"
//!
//!     Ok(())
//! }
//! ```
//!
//! ## Flexible Color Characterization (v1.2.1+)
//!
//! The new characterization API separates objective color facts from formatting preferences,
//! giving you complete control over how colors are described.
//!
//! ```rust
//! use munsellspace::{ColorClassifier, ColorCharacterization, FormatOptions, BaseColorSet, OverlayMode};
//!
//! fn main() -> Result<(), Box<dyn std::error::Error>> {
//!     let classifier = ColorClassifier::new()?;
//!
//!     // Get objective characterization
//!     let char = classifier.characterize_srgb([0, 0, 128])?;
//!
//!     // Access raw data
//!     println!("ISCC-NBS #{}: {}", char.iscc_nbs_number, char.iscc_base_color);
//!     println!("Semantic matches: {:?}", char.semantic_matches);
//!
//!     // Format with different preferences
//!     let standard = FormatOptions::new(BaseColorSet::Standard, OverlayMode::Never);
//!     let extended = FormatOptions::new(BaseColorSet::Extended, OverlayMode::WhenMatching);
//!
//!     println!("Standard: {}", char.describe(&standard));  // "blue"
//!     println!("Extended: {}", char.describe(&extended));  // "dark navy" (if inside navy)
//!
//!     // Preset options for common cases
//!     println!("{}", char.describe(&FormatOptions::standard()));           // "blue"
//!     println!("{}", char.describe(&FormatOptions::extended()));           // "dark blue"
//!     println!("{}", char.describe(&FormatOptions::standard_with_overlays())); // "navy"
//!     println!("{}", char.describe(&FormatOptions::extended_with_overlays())); // "dark navy"
//!
//!     Ok(())
//! }
//! ```
//!
//! **`BaseColorSet`**: Controls which ISCC-NBS names to use
//! - `Standard`: 13 basic colors without modifiers ("blue", "red", "green")
//! - `Extended`: Full 267-category system with modifiers ("dark blue", "vivid red")
//!
//! **`OverlayMode`**: Controls semantic overlay behavior
//! - `Never`: Always use ISCC-NBS names
//! - `WhenMatching`: Use overlay if color is inside the polyhedron
//! - `Nearest`: Always use nearest overlay, even if outside

pub mod converter;
pub mod types;
pub mod error;
pub mod illuminants;
pub mod iscc;
pub mod constants;
pub mod mathematical;
pub mod reverse_conversion;
pub mod munsell_color_science;
pub mod conversion_helpers;
pub mod munsell_converter_core;
pub mod color_notation_parser;
pub mod lab_color_space;
pub mod color_math_utils;
pub mod color_interpolation;
pub mod mechanical_wedges;
pub mod unified_cache;
pub mod semantic_overlay;
pub mod semantic_overlay_data;
pub mod color_names;

// Test modules were moved to their respective implementation files
#[cfg(test)]
mod property_tests;
#[cfg(test)]
mod edge_case_tests;
#[cfg(test)]
mod types_tests;
// #[cfg(test)]
// mod comprehensive_unit_tests;

pub use converter::MunsellConverter;
pub use types::{MunsellColor, RgbColor, IsccNbsName, IsccNbsPolygon, MunsellPoint};
pub use error::{MunsellError, Result};
pub use illuminants::{Illuminant, ChromaticAdaptation, ChromaticAdaptationMethod};
pub use iscc::{IsccNbsClassifier, ColorMetadata};
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
pub use semantic_overlay::{
    MunsellSpec, MunsellCartesian, SemanticOverlay, SemanticOverlayRegistry,
    parse_hue_to_number, hue_number_to_string, parse_munsell_notation,
};

// Deprecated semantic overlay functions (v1.2.0) - Use ColorClassifier instead
// These are re-exported for backward compatibility and will be removed in v2.0.0
#[allow(deprecated)]
pub use semantic_overlay::{
    semantic_overlay, matching_overlays, matching_overlays_ranked, matches_overlay, closest_overlay,
};
pub use semantic_overlay_data::{create_overlay_registry, get_registry};

// Unified color naming API (v1.2.0+)
pub use color_names::{
    ColorClassifier, ColorDescriptor, ColorModifier,
    known_color_names, is_known_color, color_name_count,
    // New in v1.2.1: Flexible characterization API
    ColorCharacterization, FormatOptions, BaseColorSet, OverlayMode,
};

// Note: General color conversions (RGB↔Hex↔Lab↔HSL↔HSV) are available via the palette crate
// We only expose Munsell-specific conversions to avoid duplication

/// Library version
pub const VERSION: &str = env!("CARGO_PKG_VERSION");