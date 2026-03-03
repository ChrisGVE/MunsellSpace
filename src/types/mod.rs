//! Core types for Munsell color space representation.
//!
//! This module provides the fundamental types used throughout the library:
//! - [`RgbColor`] - RGB color with 8-bit components
//! - [`MunsellColor`] - Munsell color with notation parsing and semantic overlay
//! - [`IsccNbsName`] - ISCC-NBS standardized color name metadata
//! - [`IsccNbsPolygon`] - ISCC-NBS color polygon in Munsell space
//! - [`MunsellPoint`] - Point in Munsell space for polygon boundaries

mod rgb;
mod munsell;
pub(crate) mod notation;
mod iscc_types;

// Re-export all public types to preserve the existing API surface.
pub use rgb::RgbColor;
pub use munsell::MunsellColor;
pub use iscc_types::{IsccNbsName, MunsellPoint, IsccNbsPolygon};

