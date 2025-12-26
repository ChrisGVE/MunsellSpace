//! Unified color naming API for MunsellSpace
//!
//! This module provides a unified interface for all color naming systems:
//!
//! - **ISCC-NBS standard names**: 267 standardized color categories
//! - **Extended/alternate names**: Alternative naming conventions
//! - **Semantic overlays**: 30 color names from Centore (2020) research
//!
//! # Overview
//!
//! The [`ColorClassifier`] is the primary entry point. It accepts colors in
//! various formats (RGB, hex, Lab, Munsell notation) and returns a
//! [`ColorDescriptor`] containing complete naming information.
//!
//! The same [`ColorModifier`] (e.g., "vivid", "pale", "dark grayish") applies
//! across all naming systems, providing consistent descriptors like:
//! - Standard: "vivid red"
//! - Extended: "vivid crimson"
//! - Semantic: "vivid rust"
//!
//! # Example
//!
//! ```rust
//! use munsellspace::color_names::{ColorClassifier, ColorModifier};
//!
//! # fn main() -> Result<(), Box<dyn std::error::Error>> {
//! let classifier = ColorClassifier::new()?;
//!
//! // Classify any color format
//! let desc = classifier.classify_srgb([180, 80, 60])?;
//!
//! println!("ISCC-NBS #{}", desc.iscc_nbs_number);
//! println!("Standard: {}", desc.standard_descriptor());
//! println!("Extended: {}", desc.extended_descriptor());
//!
//! if let Some(semantic) = desc.semantic_descriptor() {
//!     println!("Semantic: {}", semantic);
//! }
//!
//! // Check modifier properties
//! if desc.modifier.is_vivid() {
//!     println!("This is a vivid color!");
//! }
//!
//! // Format any modifier + color combination
//! let formatted = ColorModifier::Deep.format("coral");
//! println!("{}", formatted); // "deep coral"
//! # Ok(())
//! # }
//! ```
//!
//! # Registry
//!
//! The module maintains an internal registry of all known color names across
//! systems. Use [`known_color_names()`] to iterate over them or
//! [`is_known_color()`] to check if a name exists.
//!
//! ```rust
//! use munsellspace::color_names::{known_color_names, is_known_color};
//!
//! assert!(is_known_color("red"));
//! assert!(is_known_color("coral"));
//! assert!(is_known_color("chartreuse"));
//! assert!(!is_known_color("unknown"));
//!
//! // List all known colors
//! for name in known_color_names() {
//!     println!("{}", name);
//! }
//! ```

mod classifier;
mod descriptor;
mod modifier;
mod registry;

// ═══════════════════════════════════════════════════════════════════════════════
// Public API
// ═══════════════════════════════════════════════════════════════════════════════

// Primary types
pub use classifier::ColorClassifier;
pub use descriptor::ColorDescriptor;
pub use modifier::ColorModifier;

// Registry functions (only base names, not internal -ish forms)
pub use registry::{color_name_count, is_known_color, known_color_names};
