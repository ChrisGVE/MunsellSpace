//! Exact 1:1 port of Python colour-science munsell functions.
//!
//! This module contains exact implementations matching Python's behaviour,
//! organized into focused submodules.

mod hue_conversions;
mod specification;
mod interpolation_methods;
mod renotation_lookup;
mod ovoid;
mod xyy_to_munsell;
mod spec_to_xy;
#[cfg(test)]
mod tests;

pub use hue_conversions::{
    hue_to_astm_hue, astm_hue_to_hue, hue_to_hue_angle,
    hue_angle_to_hue, bounding_hues_from_renotation,
};
pub use specification::{
    is_grey_munsell_colour, normalise_munsell_specification,
    luminance_astmd1535, munsell_value_astmd1535,
    cartesian_to_cylindrical, polar_to_cartesian,
};
pub use interpolation_methods::interpolation_method_from_renotation_ovoid;
pub use renotation_lookup::{xyy_from_renotation, maximum_chroma_from_renotation};
pub use ovoid::{xy_from_renotation_ovoid_interpolated, xy_from_renotation_ovoid};
pub use xyy_to_munsell::xyy_to_munsell_specification;
pub use spec_to_xy::{munsell_specification_to_xy, munsell_specification_to_xyy};

/// Linear interpolation helper used across submodules.
pub(crate) fn lerp(x1: f64, x2: f64, y1: f64, y2: f64, x: f64) -> f64 {
    if (x2 - x1).abs() < 1e-10 {
        return y1;
    }
    y1 + (x - x1) * (y2 - y1) / (x2 - x1)
}
