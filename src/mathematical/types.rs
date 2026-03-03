//! Public types for the mathematical Munsell converter.
//!
//! Contains `Illuminant` (re-exported from `crate::illuminants`),
//! `ChromaticAdaptation`, `MunsellSpecification`, and `CieXyY`.

/// Standard illuminants — re-exported from the canonical `illuminants` module.
///
/// Each illuminant represents a specific light source with defined spectral
/// characteristics, affecting how colors appear and are measured.
///
/// # Usage in Munsell Conversion
///
/// Different ISCC-NBS datasets were created under different illuminant assumptions:
/// - **W3 Dataset**: Performs best with Illuminant C (46-52% accuracy)
/// - **Centore Dataset**: Performs best with Illuminant F7 (57-63% accuracy)
///
/// # Examples
///
/// ```rust
/// use munsellspace::mathematical::Illuminant;
///
/// let illuminant = Illuminant::D65;
/// let white_point = illuminant.white_point();
/// println!("D65 white point: {:?}", white_point);
/// ```
pub use crate::illuminants::Illuminant;

/// Chromatic adaptation methods for illuminant changes.
///
/// Chromatic adaptation transforms handle the change in color appearance
/// when moving between different illuminants. Each method uses different
/// mathematical models to predict how colors should appear under the new
/// illuminant conditions.
///
/// # Performance in Munsell Conversion
///
/// For ISCC-NBS classification accuracy:
/// - **XYZScaling**: Often performs slightly better (1-2% improvement)
/// - **Bradford**: Close second, more theoretically robust
/// - **CAT02**: Generally similar to Bradford
///
/// # Examples
///
/// ```rust
/// use munsellspace::mathematical::ChromaticAdaptation;
///
/// let bradford = ChromaticAdaptation::Bradford;
/// let xyz_scaling = ChromaticAdaptation::XYZScaling;
/// let cat02 = ChromaticAdaptation::CAT02;
/// ```
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum ChromaticAdaptation {
    /// Bradford chromatic adaptation transform - industry standard method
    Bradford,
    /// XYZ scaling adaptation - simple but often effective method
    XYZScaling,
    /// CAT02 chromatic adaptation from CIECAM02 - modern appearance model
    CAT02,
}

/// Mathematical Munsell color specification with precise component values.
///
/// Represents a color in the Munsell color system using continuous numeric values
/// rather than discrete notation strings.
///
/// # Examples
///
/// ```rust
/// use munsellspace::mathematical::MunsellSpecification;
///
/// let red = MunsellSpecification {
///     hue: 5.0,
///     family: "R".to_string(),
///     value: 4.0,
///     chroma: 14.0,
/// };
/// ```
#[derive(Debug, Clone, PartialEq)]
pub struct MunsellSpecification {
    /// Hue number within family (0.0-10.0)
    pub hue: f64,
    /// Hue family designation: R, YR, Y, GY, G, BG, B, PB, P, RP, or N (neutral)
    pub family: String,
    /// Value (lightness): 0.0 (black) to 10.0 (white)
    pub value: f64,
    /// Chroma (saturation): 0.0 (neutral) to 20.0+ (vivid)
    pub chroma: f64,
}

/// CIE xyY color space representation for chromaticity calculations.
///
/// The CIE xyY color space separates chromaticity (x, y) from luminance (Y).
///
/// # Examples
///
/// ```rust
/// use munsellspace::mathematical::CieXyY;
///
/// let color = CieXyY {
///     x: 0.3127,
///     y: 0.3290,
///     y_luminance: 0.5,
/// };
/// ```
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct CieXyY {
    /// Chromaticity x coordinate derived from CIE XYZ
    pub x: f64,
    /// Chromaticity y coordinate derived from CIE XYZ
    pub y: f64,
    /// Luminance Y component (identical to Y in CIE XYZ)
    pub y_luminance: f64,
}
