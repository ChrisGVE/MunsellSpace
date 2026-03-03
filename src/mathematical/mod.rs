//! Mathematical Munsell color space conversion implementation.
//!
//! This module implements true mathematical algorithms for sRGB ↔ Munsell conversion
//! following ASTM D1535 standards and using the complete Munsell Renotation dataset
//! for accurate interpolation.

use crate::constants::*;
use crate::error::Result;

mod types;
pub(crate) mod coordinate_transforms;
pub(crate) mod hue_conversions;
#[allow(dead_code)]
pub(crate) mod interpolation_methods;
mod color_space;
mod xyy_to_munsell;
mod renotation;
mod value_computation;
mod unused_methods;
#[cfg(test)]
mod tests;

pub use types::{Illuminant, ChromaticAdaptation, MunsellSpecification, CieXyY};

// Critical constants from Python colour-science
#[allow(dead_code)]
const TOLERANCE_ABSOLUTE_DEFAULT: f64 = 1e-8;
const MAX_OUTER_ITERATIONS: usize = 64;

/// Mathematical Munsell converter using ASTM D1535 algorithms.
pub struct MathematicalMunsellConverter {
    /// Cached interpolation data for performance
    pub(crate) renotation_data: &'static [((&'static str, f64, f64), (f64, f64, f64))],
    /// Source illuminant (sRGB is D65)
    source_illuminant: Illuminant,
    /// Target illuminant for Munsell calculations
    target_illuminant: Illuminant,
    /// Chromatic adaptation method to use
    adaptation_method: ChromaticAdaptation,
}

impl MathematicalMunsellConverter {
    /// Create a new mathematical converter instance with default D65 illuminant.
    pub fn new() -> Result<Self> {
        Ok(Self {
            renotation_data: MUNSELL_RENOTATION_DATA,
            source_illuminant: Illuminant::D65,
            target_illuminant: Illuminant::D65,
            adaptation_method: ChromaticAdaptation::Bradford,
        })
    }

    /// Create a converter with specified illuminants and adaptation method.
    pub fn with_illuminants(
        source: Illuminant, target: Illuminant, method: ChromaticAdaptation,
    ) -> Result<Self> {
        Ok(Self {
            renotation_data: MUNSELL_RENOTATION_DATA,
            source_illuminant: source,
            target_illuminant: target,
            adaptation_method: method,
        })
    }
}
