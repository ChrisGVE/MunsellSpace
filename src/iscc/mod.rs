//! ISCC-NBS Color Name System Implementation
//!
//! This module provides implementation of the Inter-Society Color Council -
//! National Bureau of Standards (ISCC-NBS) color naming system. It translates
//! Munsell color specifications into standardized color names.
//!
//! The ISCC-NBS system defines 267 color categories, each represented by:
//! - A numerical identifier (1-267)
//! - A descriptive name (e.g., "vivid red", "light grayish blue")
//! - A polygonal region in Munsell color space
//!
//! ## Examples
//!
//! ```rust
//! use munsellspace::iscc::IsccNbsClassifier;
//! use munsellspace::MunsellConverter;
//!
//! # fn main() -> Result<(), Box<dyn std::error::Error>> {
//! // Create classifier and converter
//! let classifier = IsccNbsClassifier::new()?;
//! let converter = MunsellConverter::new()?;
//!
//! // Convert RGB to Munsell, then to ISCC-NBS color name
//! let munsell = converter.srgb_to_munsell([255, 0, 0])?;
//! if let (Some(hue), Some(chroma)) = (&munsell.hue, munsell.chroma) {
//!     println!("Munsell notation: {}", munsell.notation);
//!     // ISCC-NBS classification would use internal methods
//! }
//! # Ok(())
//! # }
//! ```

mod metadata;
mod color;
mod classifier;
mod data_loader;
pub mod validation;

#[cfg(test)]
mod tests;

// Re-export public types
pub use metadata::ColorMetadata;
pub use color::IsccNbsColor;
pub use classifier::IsccNbsClassifier;
pub use validation::ValidationError;
