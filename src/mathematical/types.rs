//! Public types for the mathematical Munsell converter.
//!
//! Contains `Illuminant`, `ChromaticAdaptation`, `MunsellSpecification`, and `CieXyY`.

use crate::constants::*;

/// Standard illuminants supported by the mathematical Munsell conversion system.
///
/// Each illuminant represents a specific light source with defined spectral characteristics,
/// affecting how colors appear and are measured. The choice of illuminant significantly
/// impacts conversion accuracy for different datasets.
///
/// # Standard Illuminants
///
/// - **A**: Tungsten filament lamp (2856K) - warm incandescent light
/// - **C**: Average daylight (6774K) - traditional daylight standard
/// - **E**: Equal energy illuminant - theoretical reference
/// - **D50**: Daylight (5003K) - printing and photography standard
/// - **D55**: Daylight (5503K) - intermediate daylight
/// - **D65**: Daylight (6504K) - most common computer display standard
/// - **D75**: Daylight (7504K) - north sky daylight
/// - **F2**: Cool white fluorescent (4230K) - office lighting
/// - **F7**: Daylight fluorescent (6500K) - modern office lighting
/// - **F11**: Narrow-band fluorescent (4000K) - specialized lighting
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
///
/// // For best ISCC-NBS accuracy, choose illuminant based on your dataset
/// let w3_illuminant = Illuminant::C;      // Best for W3 reference dataset
/// let centore_illuminant = Illuminant::F7; // Best for Centore dataset
/// ```
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum Illuminant {
    /// Tungsten filament lamp (2856K) - warm incandescent lighting
    A,
    /// Average daylight (6774K) - traditional daylight standard used by many color systems
    C,
    /// Equal energy illuminant - theoretical reference with flat spectral distribution
    E,
    /// Daylight (5003K) - printing and photography industry standard
    D50,
    /// Daylight (5503K) - intermediate daylight temperature
    D55,
    /// Daylight (6504K) - most common computer display and sRGB standard
    D65,
    /// Daylight (7504K) - north sky daylight, cooler temperature
    D75,
    /// Cool white fluorescent (4230K) - common office lighting
    F2,
    /// Daylight fluorescent (6500K) - modern office and commercial lighting
    F7,
    /// Narrow-band fluorescent (4000K) - specialized fluorescent lighting
    F11,
}

impl Illuminant {
    /// Get the CIE XYZ tristimulus values for this illuminant's white point.
    ///
    /// Returns the white point coordinates in the CIE XYZ color space,
    /// which define the reference "white" color under this illuminant.
    /// These values are essential for chromatic adaptation and color
    /// space transformations.
    ///
    /// # Returns
    /// Array of [X, Y, Z] tristimulus values for the white point
    ///
    /// # Examples
    /// ```rust
    /// use munsellspace::mathematical::Illuminant;
    ///
    /// // Get white points for different illuminants
    /// let d65_white = Illuminant::D65.white_point();
    /// let c_white = Illuminant::C.white_point();
    ///
    /// println!("D65 white point: X={:.3}, Y={:.3}, Z={:.3}",
    ///          d65_white[0], d65_white[1], d65_white[2]);
    ///
    /// // D65 typically has values around [0.95047, 1.0, 1.08883]
    /// // C has different values, affecting color appearance
    /// ```
    pub fn white_point(&self) -> [f64; 3] {
        match self {
            Illuminant::A => ILLUMINANT_A_XYZ,
            Illuminant::C => ILLUMINANT_C_XYZ,
            Illuminant::E => ILLUMINANT_E_XYZ,
            Illuminant::D50 => ILLUMINANT_D50_XYZ,
            Illuminant::D55 => ILLUMINANT_D55_XYZ,
            Illuminant::D65 => ILLUMINANT_D65_XYZ,
            Illuminant::D75 => ILLUMINANT_D75_XYZ,
            Illuminant::F2 => ILLUMINANT_F2_XYZ,
            Illuminant::F7 => ILLUMINANT_F7_XYZ,
            Illuminant::F11 => ILLUMINANT_F11_XYZ,
        }
    }
}

/// Chromatic adaptation methods for illuminant changes.
///
/// Chromatic adaptation transforms handle the change in color appearance
/// when moving between different illuminants. Each method uses different
/// mathematical models to predict how colors should appear under the new
/// illuminant conditions.
///
/// # Adaptation Methods
///
/// - **Bradford**: Industry-standard method with excellent performance across illuminants
/// - **XYZScaling**: Simple scaling method, slightly better than Bradford for some cases
/// - **CAT02**: CIECAM02-based method, part of modern color appearance models
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
/// // Different adaptation methods for comparison
/// let bradford = ChromaticAdaptation::Bradford;
/// let xyz_scaling = ChromaticAdaptation::XYZScaling;
/// let cat02 = ChromaticAdaptation::CAT02;
///
/// // XYZScaling often provides best ISCC-NBS accuracy
/// let recommended = ChromaticAdaptation::XYZScaling;
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
/// rather than discrete notation strings. This format is used internally for
/// mathematical color space calculations and interpolation.
///
/// # Components
///
/// - **hue**: Continuous hue value (0.0-10.0 within each family)
/// - **family**: Hue family designation ("R", "YR", "Y", etc.)
/// - **value**: Lightness from black (0.0) to white (10.0)
/// - **chroma**: Saturation from neutral (0.0) to vivid (20.0+)
///
/// # Examples
///
/// ```rust
/// use munsellspace::mathematical::MunsellSpecification;
///
/// // Create a mathematical Munsell specification
/// let red = MunsellSpecification {
///     hue: 5.0,
///     family: "R".to_string(),
///     value: 4.0,
///     chroma: 14.0,
/// };
///
/// // This represents approximately "5R 4.0/14.0" in Munsell notation
/// println!("Mathematical spec: {}R {:.1}/{:.1}",
///          red.hue, red.value, red.chroma);
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
/// The CIE xyY color space separates chromaticity (x, y) from luminance (Y),
/// making it useful for color analysis and Munsell conversion calculations.
/// The x and y coordinates define the color's chromaticity (hue and saturation
/// properties), while Y represents the luminance (lightness).
///
/// # Coordinate Ranges
///
/// - **x**: Chromaticity coordinate (typically 0.0-1.0)
/// - **y**: Chromaticity coordinate (typically 0.0-1.0)
/// - **Y**: Luminance (0.0-1.0, where 1.0 represents diffuse white)
///
/// # Usage in Munsell Conversion
///
/// CIE xyY serves as an intermediate color space for:
/// - Calculating hue angles from chromaticity coordinates
/// - Determining chroma (saturation) from chromaticity distance
/// - Computing Munsell value from luminance Y
///
/// # Examples
///
/// ```rust
/// use munsellspace::mathematical::CieXyY;
///
/// // Create a color in CIE xyY space
/// let color = CieXyY {
///     x: 0.3127,  // D65 illuminant x chromaticity
///     y: 0.3290,  // D65 illuminant y chromaticity
///     y_luminance: 0.5,     // 50% luminance
/// };
///
/// println!("Chromaticity: x={:.4}, y={:.4}", color.x, color.y);
/// println!("Luminance: Y={:.3}", color.y_luminance);
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
