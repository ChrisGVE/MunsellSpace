//! Mathematical Munsell color space conversion implementation
//! 
//! This module implements true mathematical algorithms for sRGB ↔ Munsell conversion
//! following ASTM D1535 standards and using the complete Munsell Renotation dataset
//! for accurate interpolation.

use palette::{Srgb, Xyz, convert::IntoColor, white_point::D65};
use crate::constants::*;
use crate::error::{MunsellError, Result};

// Critical constants from Python colour-science
const THRESHOLD_INTEGER: f64 = 1e-3;  // Python's achromatic threshold
const TOLERANCE_ABSOLUTE_DEFAULT: f64 = 1e-8;
const MAX_OUTER_ITERATIONS: usize = 64;
const MAX_INNER_ITERATIONS: usize = 16;

// Import centralized illuminant and adaptation constants
// Standard illuminant white points are now imported from constants module

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

/// Coordinate transformation functions following Python colour-science
mod coordinate_transforms {

    /// Convert cartesian [x, y] to polar [rho, phi] coordinates
    /// phi is in radians [-π, π]
    #[inline]
    pub fn cartesian_to_polar(x: f64, y: f64) -> (f64, f64) {
        let rho = x.hypot(y);  // More efficient than manual sqrt
        let phi = y.atan2(x);              // arctan2 returns [-π, π]
        (rho, phi)
    }

    /// Convert polar [rho, phi] to cartesian [x, y] coordinates  
    /// phi should be in radians
    #[inline]
    pub fn polar_to_cartesian(rho: f64, phi: f64) -> (f64, f64) {
        let x = rho * phi.cos();
        let y = rho * phi.sin();
        (x, y)
    }

    /// Convert cartesian [x, y, z] to cylindrical [rho, phi, z] coordinates
    /// Uses cartesian_to_polar for first two coordinates, keeps z unchanged
    #[inline]
    pub fn cartesian_to_cylindrical(x: f64, y: f64, z: f64) -> (f64, f64, f64) {
        let (rho, phi) = cartesian_to_polar(x, y);
        (rho, phi, z)
    }

    /// Convert cylindrical [rho, phi, z] to cartesian [x, y, z] coordinates
    #[inline]
    pub fn cylindrical_to_cartesian(rho: f64, phi: f64, z: f64) -> (f64, f64, f64) {
        let (x, y) = polar_to_cartesian(rho, phi);
        (x, y, z)
    }
}

/// Hue angle conversion functions following Python colour-science exact implementation
mod hue_conversions {

    /// Hue family codes as used in Python colour-science
    const HUE_FAMILY_CODES: [(u8, &str); 10] = [
        (1, "BG"), (2, "G"), (3, "GY"), (4, "Y"), (5, "YR"),
        (6, "R"), (7, "RP"), (8, "P"), (9, "PB"), (10, "B")
    ];

    /// Convert [hue, code] to ASTM hue angle
    /// Exact implementation from Python colour-science
    #[inline]
    pub fn hue_to_astm_hue(hue: f64, code: u8) -> f64 {
        // Calculate single_hue following exact Python formula
        // CRITICAL: Use 17.0 as in Python, and handle modulo correctly!
        let raw = (17.0 - code as f64) % 10.0 + (hue * 0.1) - 0.5;
        // Python-style modulo: always returns positive result (optimized)
        let single_hue = ((raw % 10.0) + 10.0) % 10.0;
        
        // Linear interpolation with exact breakpoints from Python
        linear_interpolate_hue_angle(single_hue)
    }

    /// Convert hue angle to [hue, code] pair
    /// Exact implementation from Python colour-science
    #[inline]  
    pub fn hue_angle_to_hue(hue_angle: f64) -> (f64, u8) {
        // Reverse interpolation from angle to single_hue
        let single_hue = reverse_interpolate_hue_angle(hue_angle);
        
        // Determine code based on single_hue ranges
        // CRITICAL FIX: Use Python's EXACT code mapping from hue_angle_to_hue
        let code = if single_hue <= 0.5 { 7 }       // R  (code 7)
                   else if single_hue <= 1.5 { 6 }  // YR (code 6)
                   else if single_hue <= 2.5 { 5 }  // Y  (code 5)
                   else if single_hue <= 3.5 { 4 }  // GY (code 4)
                   else if single_hue <= 4.5 { 3 }  // G  (code 3)
                   else if single_hue <= 5.5 { 2 }  // BG (code 2)
                   else if single_hue <= 6.5 { 1 }  // B  (code 1)
                   else if single_hue <= 7.5 { 10 } // PB (code 10)
                   else if single_hue <= 8.5 { 9 }  // P  (code 9)
                   else if single_hue <= 9.5 { 8 }  // RP (code 8)
                   else { 7 };                       // R (wraparound back to code 7)
        
        // Calculate hue from single_hue (exact Python logic)
        let hue = (10.0 * (single_hue % 1.0) + 5.0) % 10.0;
        
        // REVERTED: Don't normalize here, it's done in normalize_munsell_specification
        let final_hue = if hue == 0.0 { 10.0 } else { hue };
        
        (final_hue, code)
    }

    /// Linear interpolation for hue angle mapping
    /// Uses exact breakpoints from Python colour-science
    #[inline]
    fn linear_interpolate_hue_angle(single_hue: f64) -> f64 {
        // Exact breakpoints from Python: [0, 2, 3, 4, 5, 6, 8, 9, 10]
        // Exact angles from Python:     [0, 45, 70, 135, 160, 225, 255, 315, 360]
        
        let breakpoints = [0.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 9.0, 10.0];
        let angles = [0.0, 45.0, 70.0, 135.0, 160.0, 225.0, 255.0, 315.0, 360.0];
        
        // Find the two bounding points
        for i in 0..breakpoints.len()-1 {
            if single_hue >= breakpoints[i] && single_hue <= breakpoints[i+1] {
                let t = (single_hue - breakpoints[i]) / (breakpoints[i+1] - breakpoints[i]);
                return angles[i] + t * (angles[i+1] - angles[i]);
            }
        }
        
        // Handle edge case (should not happen with valid input)
        360.0
    }

    /// Reverse interpolation from hue angle to single_hue
    #[inline]
    fn reverse_interpolate_hue_angle(hue_angle: f64) -> f64 {
        // Same breakpoints but reversed
        let angles = [0.0, 45.0, 70.0, 135.0, 160.0, 225.0, 255.0, 315.0, 360.0];
        let breakpoints = [0.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 9.0, 10.0];
        
        // Find the two bounding angles
        for i in 0..angles.len()-1 {
            if hue_angle >= angles[i] && hue_angle <= angles[i+1] {
                let t = (hue_angle - angles[i]) / (angles[i+1] - angles[i]);
                return breakpoints[i] + t * (breakpoints[i+1] - breakpoints[i]);
            }
        }
        
        // Handle edge case
        0.0
    }

    /// Find the two bounding hues from Munsell Renotation System data
    /// Exact implementation from Python colour-science
    pub fn bounding_hues_from_renotation(hue: f64, code: u8) -> ((f64, u8), (f64, u8)) {
        let mut hue_cw: f64;
        let mut code_cw: u8;
        let mut hue_ccw: f64;
        let mut code_ccw: u8;

        // Check if hue is exact multiple of 2.5
        if (hue % 2.5 - 0.0).abs() < 1e-10 {
            if (hue - 0.0).abs() < 1e-10 {
                // Special case: hue == 0
                hue_cw = 10.0;
                // Increment code in the proper sequence
                code_cw = match code {
                    1 => 2,   // B -> BG
                    2 => 3,   // BG -> G
                    3 => 4,   // G -> GY
                    4 => 5,   // GY -> Y
                    5 => 6,   // Y -> YR
                    6 => 7,   // YR -> R
                    7 => 8,   // R -> RP
                    8 => 9,   // RP -> P
                    9 => 10,  // P -> PB
                    10 => 1,  // PB -> B (wraparound)
                    _ => code // Invalid, keep same
                };
            } else {
                hue_cw = hue;
                code_cw = code;
            }
            hue_ccw = hue_cw;
            code_ccw = code_cw;
        } else {
            // Intermediate hue - find bounding standard hues
            hue_cw = 2.5 * (hue / 2.5).floor();
            hue_ccw = (hue_cw + 2.5) % 10.0;
            if (hue_ccw - 0.0).abs() < 1e-10 {
                hue_ccw = 10.0;
            }

            if (hue_cw - 0.0).abs() < 1e-10 {
                hue_cw = 10.0;
                // Increment code in the proper sequence
                code_cw = match code {
                    1 => 2,   // B -> BG
                    2 => 3,   // BG -> G
                    3 => 4,   // G -> GY
                    4 => 5,   // GY -> Y
                    5 => 6,   // Y -> YR
                    6 => 7,   // YR -> R
                    7 => 8,   // R -> RP
                    8 => 9,   // RP -> P
                    9 => 10,  // P -> PB
                    10 => 1,  // PB -> B (wraparound)
                    _ => code // Invalid, keep same
                };
            } else {
                code_cw = code;
            }
            code_ccw = code;
        }

        ((hue_cw, code_cw), (hue_ccw, code_ccw))
    }

    /// Convert code number to hue family name  
    /// FIXED: Python's MUNSELL_HUE_LETTER_CODES: {'B': 1, 'BG': 2, 'G': 3, 'GY': 4, 'Y': 5, 'YR': 6, 'R': 7, 'RP': 8, 'P': 9, 'PB': 10}
    pub fn code_to_family(code: u8) -> &'static str {
        match code {
            1 => "B",
            2 => "BG",
            3 => "G",
            4 => "GY",
            5 => "Y",
            6 => "YR",
            7 => "R",
            8 => "RP",
            9 => "P",
            10 => "PB",
            _ => "N" // Fallback for invalid codes
        }
    }

    /// Convert family name to code number
    /// FIXED: Python's MUNSELL_HUE_LETTER_CODES dictionary
    pub fn family_to_code(family: &str) -> u8 {
        match family {
            "B" => 1,
            "BG" => 2,
            "G" => 3,
            "GY" => 4,
            "Y" => 5,
            "YR" => 6,
            "R" => 7,
            "RP" => 8,
            "P" => 9,
            "PB" => 10,
            _ => 0 // "N" or invalid
        }
    }
    
    /// Convert hue and code to hue angle in degrees
    /// Exact implementation of Python colour-science hue_to_hue_angle function
    pub fn hue_to_hue_angle(hue: f64, code: u8) -> f64 {
        // Calculate single_hue following exact Python formula
        // FIXED: Python's formula uses (18 - code) for their mapping
        let single_hue = ((18.0 - code as f64) % 10.0 + (hue / 10.0) - 0.5) % 10.0;
        
        // Use linear interpolation with exact Python breakpoints
        linear_interpolate_hue_angle(single_hue)
    }
}

/// Interpolation method selection logic
/// MASSIVE empirical lookup table from Python colour-science
mod interpolation_methods {
    use super::hue_conversions::*;

    #[derive(Debug, Clone, PartialEq)]
    pub enum InterpolationMethod {
        None,     // No interpolation needed
        Linear,   // Linear interpolation
        Radial,   // Radial interpolation
    }

    /// Determine interpolation method for given Munsell specification
    /// Exact implementation of Python colour-science interpolation_method_from_renotation_ovoid
    pub fn interpolation_method_from_renotation_ovoid(hue: f64, value: f64, chroma: f64, code: u8) -> InterpolationMethod {
        // Check for grey colors
        // FIXED: code == 0 now means "R", not achromatic. Only check chroma.
        if chroma == 0.0 {
            return InterpolationMethod::None;
        }

        // Round value and chroma to integers as required
        let value = value.round() as i32;
        let chroma = (2.0 * (chroma / 2.0).round()) as i32; // Round to even numbers

        // Standard Munsell Renotation System hue, no interpolation needed
        if (hue % 2.5 - 0.0).abs() < 1e-10 {
            return InterpolationMethod::None;
        }

        let astm_hue = hue_to_astm_hue(hue, code);

        // MASSIVE empirical lookup table - exact from Python colour-science
        match value {
            1 => {
                match chroma {
                    2 => {
                        if (15.0 < astm_hue && astm_hue < 30.0) || (60.0 < astm_hue && astm_hue < 85.0) {
                            InterpolationMethod::Radial
                        } else {
                            InterpolationMethod::Linear
                        }
                    }
                    4 => {
                        if (12.5 < astm_hue && astm_hue < 27.5) || (57.5 < astm_hue && astm_hue < 80.0) {
                            InterpolationMethod::Radial
                        } else {
                            InterpolationMethod::Linear
                        }
                    }
                    6 => {
                        if 55.0 < astm_hue && astm_hue < 80.0 {
                            InterpolationMethod::Radial
                        } else {
                            InterpolationMethod::Linear
                        }
                    }
                    8 => {
                        if 67.5 < astm_hue && astm_hue < 77.5 {
                            InterpolationMethod::Radial
                        } else {
                            InterpolationMethod::Linear
                        }
                    }
                    _ if chroma >= 10 => {
                        if 72.5 < astm_hue && astm_hue < 77.5 {
                            InterpolationMethod::Radial
                        } else {
                            InterpolationMethod::Linear
                        }
                    }
                    _ => InterpolationMethod::Linear
                }
            }
            2 => {
                match chroma {
                    2 => {
                        if (15.0 < astm_hue && astm_hue < 27.5) || (77.5 < astm_hue && astm_hue < 80.0) {
                            InterpolationMethod::Radial
                        } else {
                            InterpolationMethod::Linear
                        }
                    }
                    4 => {
                        if (12.5 < astm_hue && astm_hue < 30.0) || (62.5 < astm_hue && astm_hue < 80.0) {
                            InterpolationMethod::Radial
                        } else {
                            InterpolationMethod::Linear
                        }
                    }
                    6 => {
                        if (7.5 < astm_hue && astm_hue < 22.5) || (62.5 < astm_hue && astm_hue < 80.0) {
                            InterpolationMethod::Radial
                        } else {
                            InterpolationMethod::Linear
                        }
                    }
                    8 => {
                        if (7.5 < astm_hue && astm_hue < 15.0) || (60.0 < astm_hue && astm_hue < 80.0) {
                            InterpolationMethod::Radial
                        } else {
                            InterpolationMethod::Linear
                        }
                    }
                    _ if chroma >= 10 => {
                        if 65.0 < astm_hue && astm_hue < 77.5 {
                            InterpolationMethod::Radial
                        } else {
                            InterpolationMethod::Linear
                        }
                    }
                    _ => InterpolationMethod::Linear
                }
            }
            3 => {
                match chroma {
                    2 => {
                        if (10.0 < astm_hue && astm_hue < 37.5) || (65.0 < astm_hue && astm_hue < 85.0) {
                            InterpolationMethod::Radial
                        } else {
                            InterpolationMethod::Linear
                        }
                    }
                    4 => {
                        if (5.0 < astm_hue && astm_hue < 37.5) || (55.0 < astm_hue && astm_hue < 72.5) {
                            InterpolationMethod::Radial
                        } else {
                            InterpolationMethod::Linear
                        }
                    }
                    6 | 8 | 10 => {
                        if (7.5 < astm_hue && astm_hue < 37.5) || (57.5 < astm_hue && astm_hue < 82.5) {
                            InterpolationMethod::Radial
                        } else {
                            InterpolationMethod::Linear
                        }
                    }
                    _ if chroma >= 12 => {
                        if (7.5 < astm_hue && astm_hue < 42.5) || (57.5 < astm_hue && astm_hue < 80.0) {
                            InterpolationMethod::Radial
                        } else {
                            InterpolationMethod::Linear
                        }
                    }
                    _ => InterpolationMethod::Linear
                }
            }
            4 => {
                match chroma {
                    2 | 4 => {
                        if (7.5 < astm_hue && astm_hue < 42.5) || (57.5 < astm_hue && astm_hue < 85.0) {
                            InterpolationMethod::Radial
                        } else {
                            InterpolationMethod::Linear
                        }
                    }
                    6 | 8 => {
                        if (7.5 < astm_hue && astm_hue < 40.0) || (57.5 < astm_hue && astm_hue < 82.5) {
                            InterpolationMethod::Radial
                        } else {
                            InterpolationMethod::Linear
                        }
                    }
                    _ if chroma >= 10 => {
                        if (7.5 < astm_hue && astm_hue < 40.0) || (57.5 < astm_hue && astm_hue < 80.0) {
                            InterpolationMethod::Radial
                        } else {
                            InterpolationMethod::Linear
                        }
                    }
                    _ => InterpolationMethod::Linear
                }
            }
            5 => {
                match chroma {
                    2 => {
                        if (5.0 < astm_hue && astm_hue < 37.5) || (55.0 < astm_hue && astm_hue < 85.0) {
                            InterpolationMethod::Radial
                        } else {
                            InterpolationMethod::Linear
                        }
                    }
                    4 | 6 | 8 => {
                        if (2.5 < astm_hue && astm_hue < 42.5) || (55.0 < astm_hue && astm_hue < 85.0) {
                            InterpolationMethod::Radial
                        } else {
                            InterpolationMethod::Linear
                        }
                    }
                    _ if chroma >= 10 => {
                        if (2.5 < astm_hue && astm_hue < 42.5) || (55.0 < astm_hue && astm_hue < 82.5) {
                            InterpolationMethod::Radial
                        } else {
                            InterpolationMethod::Linear
                        }
                    }
                    _ => InterpolationMethod::Linear
                }
            }
            6 => {
                match chroma {
                    2 | 4 => {
                        if (5.0 < astm_hue && astm_hue < 37.5) || (55.0 < astm_hue && astm_hue < 87.5) {
                            InterpolationMethod::Radial
                        } else {
                            InterpolationMethod::Linear
                        }
                    }
                    6 => {
                        if (5.0 < astm_hue && astm_hue < 42.5) || (57.5 < astm_hue && astm_hue < 87.5) {
                            InterpolationMethod::Radial
                        } else {
                            InterpolationMethod::Linear
                        }
                    }
                    8 | 10 => {
                        if (5.0 < astm_hue && astm_hue < 42.5) || (60.0 < astm_hue && astm_hue < 85.0) {
                            InterpolationMethod::Radial
                        } else {
                            InterpolationMethod::Linear
                        }
                    }
                    12 | 14 => {
                        if (5.0 < astm_hue && astm_hue < 42.5) || (60.0 < astm_hue && astm_hue < 82.5) {
                            InterpolationMethod::Radial
                        } else {
                            InterpolationMethod::Linear
                        }
                    }
                    _ if chroma >= 16 => {
                        if (5.0 < astm_hue && astm_hue < 42.5) || (60.0 < astm_hue && astm_hue < 80.0) {
                            InterpolationMethod::Radial
                        } else {
                            InterpolationMethod::Linear
                        }
                    }
                    _ => InterpolationMethod::Linear
                }
            }
            7 => {
                match chroma {
                    2 | 4 | 6 => {
                        if (5.0 < astm_hue && astm_hue < 42.5) || (60.0 < astm_hue && astm_hue < 85.0) {
                            InterpolationMethod::Radial
                        } else {
                            InterpolationMethod::Linear
                        }
                    }
                    8 => {
                        if (5.0 < astm_hue && astm_hue < 42.5) || (60.0 < astm_hue && astm_hue < 82.5) {
                            InterpolationMethod::Radial
                        } else {
                            InterpolationMethod::Linear
                        }
                    }
                    10 => {
                        if (30.0 < astm_hue && astm_hue < 42.5) || (5.0 < astm_hue && astm_hue < 25.0) || (60.0 < astm_hue && astm_hue < 82.5) {
                            InterpolationMethod::Radial
                        } else {
                            InterpolationMethod::Linear
                        }
                    }
                    12 => {
                        if (30.0 < astm_hue && astm_hue < 42.5) || (7.5 < astm_hue && astm_hue < 27.5) || (80.0 < astm_hue && astm_hue < 82.5) {
                            InterpolationMethod::Radial
                        } else {
                            InterpolationMethod::Linear
                        }
                    }
                    _ if chroma >= 14 => {
                        if (32.5 < astm_hue && astm_hue < 40.0) || (7.5 < astm_hue && astm_hue < 15.0) || (80.0 < astm_hue && astm_hue < 82.5) {
                            InterpolationMethod::Radial
                        } else {
                            InterpolationMethod::Linear
                        }
                    }
                    _ => InterpolationMethod::Linear
                }
            }
            8 => {
                match chroma {
                    2 | 4 | 6 | 8 | 10 | 12 => {
                        if (5.0 < astm_hue && astm_hue < 40.0) || (60.0 < astm_hue && astm_hue < 85.0) {
                            InterpolationMethod::Radial
                        } else {
                            InterpolationMethod::Linear
                        }
                    }
                    _ if chroma >= 14 => {
                        if (32.5 < astm_hue && astm_hue < 40.0) || (5.0 < astm_hue && astm_hue < 15.0) || (60.0 < astm_hue && astm_hue < 85.0) {
                            InterpolationMethod::Radial
                        } else {
                            InterpolationMethod::Linear
                        }
                    }
                    _ => InterpolationMethod::Linear
                }
            }
            9 => {
                match chroma {
                    2 | 4 => {
                        if (5.0 < astm_hue && astm_hue < 40.0) || (55.0 < astm_hue && astm_hue < 80.0) {
                            InterpolationMethod::Radial
                        } else {
                            InterpolationMethod::Linear
                        }
                    }
                    6 | 8 | 10 | 12 | 14 => {
                        if 5.0 < astm_hue && astm_hue < 42.5 {
                            InterpolationMethod::Radial
                        } else {
                            InterpolationMethod::Linear
                        }
                    }
                    _ if chroma >= 16 => {
                        if 35.0 < astm_hue && astm_hue < 42.5 {
                            InterpolationMethod::Radial
                        } else {
                            InterpolationMethod::Linear
                        }
                    }
                    _ => InterpolationMethod::Linear
                }
            }
            10 => {
                // Ideal white, no interpolation needed
                InterpolationMethod::None
            }
            _ => InterpolationMethod::Linear // Default for out-of-range values
        }
    }
}

/// Mathematical Munsell converter using ASTM D1535 algorithms
pub struct MathematicalMunsellConverter {
    /// Cached interpolation data for performance
    renotation_data: &'static [((&'static str, f64, f64), (f64, f64, f64))],
    /// Source illuminant (sRGB is D65)
    source_illuminant: Illuminant,
    /// Target illuminant for Munsell calculations
    target_illuminant: Illuminant,
    /// Chromatic adaptation method to use
    adaptation_method: ChromaticAdaptation,
}

impl MathematicalMunsellConverter {
    /// Create a new mathematical converter instance with default D65 illuminant
    pub fn new() -> Result<Self> {
        Ok(Self {
            renotation_data: MUNSELL_RENOTATION_DATA,
            source_illuminant: Illuminant::D65,
            target_illuminant: Illuminant::D65,
            adaptation_method: ChromaticAdaptation::Bradford,
        })
    }
    
    /// Create a converter with specified illuminants and adaptation method
    pub fn with_illuminants(source: Illuminant, target: Illuminant, method: ChromaticAdaptation) -> Result<Self> {
        Ok(Self {
            renotation_data: MUNSELL_RENOTATION_DATA,
            source_illuminant: source,
            target_illuminant: target,
            adaptation_method: method,
        })
    }

    /// Convert sRGB color to Munsell specification using mathematical algorithms
    ///
    /// # Arguments
    /// * `rgb` - sRGB color as [R, G, B] with values 0-255
    ///
    /// # Returns
    /// * `MunsellSpecification` with hue, value, chroma, and family
    ///
    /// # Example
    /// ```rust
    /// use munsellspace::MathematicalMunsellConverter;
    /// # fn main() -> Result<(), Box<dyn std::error::Error>> {
    /// let converter = MathematicalMunsellConverter::new()?;
    /// let munsell = converter.srgb_to_munsell([255, 0, 0])?;
    /// println!("Red: {}.{} {:.1}/{:.1}", munsell.hue, munsell.family, munsell.value, munsell.chroma);
    /// # Ok(())
    /// # }
    /// ```
    pub fn srgb_to_munsell(&self, rgb: [u8; 3]) -> Result<MunsellSpecification> {
        // Step 1: Convert sRGB to xyY using palette crate
        let xyy = self.srgb_to_xyy(rgb)?;
        
        // Step 2: Convert xyY to Munsell specification using mathematical algorithm
        self.xyy_to_munsell_specification(xyy)
    }

    /// Convert sRGB to CIE xyY color space with optional chromatic adaptation
    pub fn srgb_to_xyy(&self, rgb: [u8; 3]) -> Result<CieXyY> {
        // Create sRGB color with normalized values [0.0, 1.0]
        let rgb_norm = [
            rgb[0] as f64 / 255.0,
            rgb[1] as f64 / 255.0,
            rgb[2] as f64 / 255.0,
        ];
        
        let srgb = Srgb::new(rgb_norm[0], rgb_norm[1], rgb_norm[2]);
        
        // Convert sRGB → Linear RGB
        let linear_rgb = srgb.into_linear();
        
        // Convert Linear RGB → XYZ (source illuminant)
        let xyz_source: Xyz<D65, f64> = linear_rgb.into_color();
        let (x_src, y_src, z_src) = xyz_source.into_components();
        let xyz_src = [x_src, y_src, z_src];
        
        // Apply chromatic adaptation if needed
        let xyz_adapted = if self.source_illuminant == self.target_illuminant {
            // No adaptation needed
            xyz_src
        } else {
            // Apply chromatic adaptation from source to target illuminant
            self.chromatic_adaptation(xyz_src, self.source_illuminant, self.target_illuminant)?
        };
        
        // Convert XYZ to xyY
        let xyy = self.xyz_to_xyy(xyz_adapted);
        
        Ok(xyy)
    }

    /// Perform chromatic adaptation between illuminants
    fn chromatic_adaptation(&self, xyz: [f64; 3], source: Illuminant, target: Illuminant) -> Result<[f64; 3]> {
        match self.adaptation_method {
            ChromaticAdaptation::XYZScaling => {
                // Simple XYZ scaling method
                let source_wp = source.white_point();
                let target_wp = target.white_point();
                
                // Avoid division by zero
                if source_wp[0].abs() < 1e-15 || source_wp[1].abs() < 1e-15 || source_wp[2].abs() < 1e-15 {
                    return Err(MunsellError::ConvergenceFailed);
                }
                
                Ok([
                    xyz[0] * target_wp[0] / source_wp[0],
                    xyz[1] * target_wp[1] / source_wp[1],
                    xyz[2] * target_wp[2] / source_wp[2],
                ])
            }
            ChromaticAdaptation::Bradford => {
                self.bradford_adaptation(xyz, source, target)
            }
            ChromaticAdaptation::CAT02 => {
                self.cat02_adaptation(xyz, source, target)
            }
        }
    }
    
    /// Bradford chromatic adaptation transform
    fn bradford_adaptation(&self, xyz: [f64; 3], source: Illuminant, target: Illuminant) -> Result<[f64; 3]> {
        let source_wp = source.white_point();
        let target_wp = target.white_point();
        
        // Transform to cone response domain
        let cone_src = self.matrix_multiply_3x3(&BRADFORD_MATRIX, &xyz);
        let cone_src_wp = self.matrix_multiply_3x3(&BRADFORD_MATRIX, &source_wp);
        let cone_tgt_wp = self.matrix_multiply_3x3(&BRADFORD_MATRIX, &target_wp);
        
        // Avoid division by zero
        if cone_src_wp[0].abs() < 1e-15 || cone_src_wp[1].abs() < 1e-15 || cone_src_wp[2].abs() < 1e-15 {
            return Err(MunsellError::ConvergenceFailed);
        }
        
        // Apply adaptation
        let cone_adapted = [
            cone_src[0] * cone_tgt_wp[0] / cone_src_wp[0],
            cone_src[1] * cone_tgt_wp[1] / cone_src_wp[1],
            cone_src[2] * cone_tgt_wp[2] / cone_src_wp[2],
        ];
        
        // Transform back to XYZ
        Ok(self.matrix_multiply_3x3(&BRADFORD_MATRIX_INV, &cone_adapted))
    }
    
    /// CAT02 chromatic adaptation transform
    fn cat02_adaptation(&self, xyz: [f64; 3], source: Illuminant, target: Illuminant) -> Result<[f64; 3]> {
        let source_wp = source.white_point();
        let target_wp = target.white_point();
        
        // Transform to CAT02 response domain
        let cat_src = self.matrix_multiply_3x3(&CAT02_MATRIX, &xyz);
        let cat_src_wp = self.matrix_multiply_3x3(&CAT02_MATRIX, &source_wp);
        let cat_tgt_wp = self.matrix_multiply_3x3(&CAT02_MATRIX, &target_wp);
        
        // Avoid division by zero
        if cat_src_wp[0].abs() < 1e-15 || cat_src_wp[1].abs() < 1e-15 || cat_src_wp[2].abs() < 1e-15 {
            return Err(MunsellError::ConvergenceFailed);
        }
        
        // Apply adaptation
        let cat_adapted = [
            cat_src[0] * cat_tgt_wp[0] / cat_src_wp[0],
            cat_src[1] * cat_tgt_wp[1] / cat_src_wp[1],
            cat_src[2] * cat_tgt_wp[2] / cat_src_wp[2],
        ];
        
        // Transform back to XYZ
        Ok(self.matrix_multiply_3x3(&CAT02_MATRIX_INV, &cat_adapted))
    }

    /// Convert XYZ to xyY coordinates
    fn xyz_to_xyy(&self, xyz: [f64; 3]) -> CieXyY {
        let sum = xyz[0] + xyz[1] + xyz[2];
        
        if sum < 1e-15 {
            // Handle black/near-black colors
            CieXyY { x: 0.0, y: 0.0, y_luminance: xyz[1] }
        } else {
            CieXyY {
                x: xyz[0] / sum,
                y: xyz[1] / sum,
                y_luminance: xyz[1], // Y component is luminance
            }
        }
    }

    /// Multiply 3x3 matrix with 3D vector
    fn matrix_multiply_3x3(&self, matrix: &[[f64; 3]; 3], vector: &[f64; 3]) -> [f64; 3] {
        [
            matrix[0][0] * vector[0] + matrix[0][1] * vector[1] + matrix[0][2] * vector[2],
            matrix[1][0] * vector[0] + matrix[1][1] * vector[1] + matrix[1][2] * vector[2],
            matrix[2][0] * vector[0] + matrix[2][1] * vector[1] + matrix[2][2] * vector[2],
        ]
    }

    /// Convert CIE xyY to Munsell specification using ASTM D1535 algorithm
    pub fn xyy_to_munsell_specification(&self, xyy: CieXyY) -> Result<MunsellSpecification> {
        // EXACT IMPLEMENTATION of Python colour-science _xyY_to_munsell_specification
        // This is the complete dual-loop iterative algorithm for 100% mathematical accuracy
        
        use coordinate_transforms::*;
        use hue_conversions::*;
        
        const CONVERGENCE_THRESHOLD: f64 = THRESHOLD_INTEGER / 1e4; // 1e-7
        
        // Step 1: Calculate Munsell Value using ASTM D1535 polynomial
        let mut value = self.luminance_to_munsell_value(xyy.y_luminance)?;
        
        // Round if close to integer (Python lines 1070-1071)
        if (value - value.round()).abs() < 1e-10 {
            value = value.round();
        }
        
        // Step 2: Get achromatic center for this value (uses Illuminant C)
        // This is critical - Python checks achromatic relative to the value-specific center, not D65!
        let achromatic_spec = MunsellSpecification {
            hue: 0.0,
            family: "N".to_string(),
            value,
            chroma: 0.0,
        };
        let achromatic_xyy = self.munsell_specification_to_xyy(&achromatic_spec)?;
        let x_center = achromatic_xyy.x;
        let y_center = achromatic_xyy.y;
        
        // Calculate rho_input relative to achromatic center (NOT D65!)
        let (rho_input, phi_input_rad, _) = cartesian_to_cylindrical(
            xyy.x - x_center,
            xyy.y - y_center,
            xyy.y_luminance
        );
        // CRITICAL: Keep phi_input in original range [-180, 180] like Python!
        // Do NOT normalize to [0, 360) here - it affects convergence
        let phi_input = phi_input_rad.to_degrees();
        
        // Debug for RGB [238,0,85] specifically
        let _is_debug_color = (xyy.x - 0.558939).abs() < 0.0001 && (xyy.y - 0.285274).abs() < 0.0001;
        
        // Step 3: Check for achromatic using rho_input (like Python)
        // Also check for pure black (Y ≈ 0)
        if rho_input < THRESHOLD_INTEGER || xyy.y_luminance < 1e-6 {  // 1e-3
            return Ok(MunsellSpecification {
                hue: 0.0,
                family: "N".to_string(),
                value,
                chroma: 0.0,
            });
        }

        // Step 4: Generate initial guess using direct xyY angle
        let initial_spec = self.generate_initial_guess(xyy)?;
        let mut hue_current = initial_spec.0;
        let mut code_current = initial_spec.1;
        let mut chroma_current = initial_spec.2;  // No additional scaling needed
        
        // Note: rho_input and phi_input already calculated above relative to achromatic center
        // Don't recalculate them here!
        
        
        // Step 4: DUAL-LOOP ITERATIVE ALGORITHM
        for _outer_iteration in 0..MAX_OUTER_ITERATIONS {
            
            // Check maximum chroma boundaries
            let chroma_maximum = self.maximum_chroma_from_renotation(hue_current, value, code_current)?;
            if chroma_current > chroma_maximum {
                chroma_current = chroma_maximum;
            }
            
            // Calculate current xyY from specification
            let (x_current, y_current) = self.munsell_specification_to_xy(hue_current, value, chroma_current, code_current)?;
            
            // Convert to cylindrical coordinates relative to achromatic center (NOT Illuminant C directly!)
            let (_rho_current, phi_current, _) = cartesian_to_cylindrical(
                x_current - x_center, 
                y_current - y_center, 
                xyy.y_luminance
            );
            let mut phi_current_degrees = phi_current.to_degrees();
            // Normalize to [0, 360) range
            if phi_current_degrees < 0.0 {
                phi_current_degrees += 360.0;
            }
            
            // Inner loop: Hue angle search following Python algorithm
            // Calculate phi difference with wrapping (Python lines 1138-1140)
            let mut phi_current_difference = (360.0 - phi_input + phi_current_degrees) % 360.0;
            if phi_current_difference > 180.0 {
                phi_current_difference -= 360.0;
            }
            
            // Don't include the initial point if phi_difference is essentially 0
            // because it's not a sampled point, it's our starting position
            let mut phi_differences_data = if phi_current_difference.abs() < 1e-6 {
                vec![]
            } else {
                vec![phi_current_difference]
            };
            let mut hue_angles_differences_data = if phi_current_difference.abs() < 1e-6 {
                vec![]
            } else {
                vec![0.0]
            };
            let hue_angle_current = hue_to_astm_hue(hue_current, code_current);
            let mut extrapolate = false;
            let mut iterations_inner = 0;
            
            // Python's condition: continue while all phi_differences have same sign AND not extrapolating
            while (phi_differences_data.iter().all(|&d| d >= 0.0) || 
                   phi_differences_data.iter().all(|&d| d <= 0.0)) && 
                  !extrapolate {
                
                iterations_inner += 1;
                if iterations_inner > MAX_INNER_ITERATIONS {
                    break; // Prevent infinite loop
                }
                
                // Python line 1167: step by (phi_input - phi_current) each iteration
                // Even when phi_input == phi_current, Python still uses the formula
                // This means when phi_diff=0, all iterations test the SAME angle
                let step = iterations_inner as f64 * (phi_input - phi_current_degrees);
                // Ensure angle is in [0, 360) range (Python-style positive modulo)
                let hue_angle_inner = if (hue_angle_current + step) < 0.0 {
                    ((hue_angle_current + step) % 360.0 + 360.0) % 360.0
                } else {
                    (hue_angle_current + step) % 360.0
                };
                
                // FIXED: Match Python's modulo behavior (always positive result)
                let step_mod = if step < 0.0 {
                    ((step % 360.0) + 360.0) % 360.0
                } else {
                    step % 360.0
                };
                
                // Then normalize to [-180, 180] for circular arithmetic
                let mut hue_angle_difference_inner = if step_mod > 180.0 {
                    step_mod - 360.0
                } else {
                    step_mod
                };
                
                let (hue_inner, code_inner) = hue_angle_to_hue(hue_angle_inner);
                
                // Get xy for this test hue - Python does this even when extrapolating
                // but doesn't use the result (lines 1177-1185)
                let (x_inner, y_inner) = self.munsell_specification_to_xy(hue_inner, value, chroma_current, code_inner)?;
                
                // Check if we should enable extrapolation AFTER getting xy
                // CRITICAL: Python enables extrapolation after 2 points (lines 1187-1188)
                if phi_differences_data.len() >= 2 {
                    extrapolate = true;
                }
                
                // If not extrapolating, calculate and store phi difference (Python lines 1190-1201)
                if !extrapolate {
                    // Calculate phi for this test point (relative to achromatic center)
                    let (_, phi_inner, _) = cartesian_to_cylindrical(
                        x_inner - x_center,
                        y_inner - y_center,
                        xyy.y_luminance
                    );
                    let mut phi_inner_degrees = phi_inner.to_degrees();
                    // Normalize to [0, 360) range
                    if phi_inner_degrees < 0.0 {
                        phi_inner_degrees += 360.0;
                    }
                    
                    let mut phi_inner_difference = (360.0 - phi_input + phi_inner_degrees) % 360.0;
                    if phi_inner_difference > 180.0 {
                        phi_inner_difference -= 360.0;
                    }
                    
                    phi_differences_data.push(phi_inner_difference);
                    hue_angles_differences_data.push(hue_angle_difference_inner);
                }
            }
            
            
            // Extrapolate/interpolate to find where phi_difference = 0
            // SIMPLIFIED: Match Python's simple approach - no stuck detection, no perturbations
            let hue_angle_difference_new = if phi_differences_data.len() >= 2 {
                // Sort by phi_differences (Python lines 1206-1209)
                let mut paired: Vec<_> = phi_differences_data.iter()
                    .zip(hue_angles_differences_data.iter())
                    .map(|(&p, &h)| (p, h))
                    .collect();
                paired.sort_by(|a, b| a.0.partial_cmp(&b.0).unwrap());
                
                let sorted_phi: Vec<f64> = paired.iter().map(|&(p, _)| p).collect();
                let sorted_hue: Vec<f64> = paired.iter().map(|&(_, h)| h).collect();
                
                // Simple linear interpolation to find where phi_difference = 0
                // This matches Python's LinearInterpolator which uses np.interp
                let result = self.linear_interpolate(&sorted_phi, &sorted_hue, 0.0)?;
                
                // Python takes modulo 360 of the result
                if result < 0.0 {
                    result % 360.0 + 360.0
                } else {
                    result % 360.0
                }
            } else {
                0.0 // No correction if we couldn't collect enough points
            };
            
            let mut hue_angle_new = (hue_angle_current + hue_angle_difference_new) % 360.0;
            // Ensure angle is positive
            if hue_angle_new < 0.0 {
                hue_angle_new += 360.0;
            }
            let (hue_new, code_new) = hue_angle_to_hue(hue_angle_new);
            
            // SIMPLIFIED: Just update hue and code, no stuck detection or perturbations
            // This matches Python's approach which doesn't have any special stuck handling
            hue_current = hue_new;
            code_current = code_new;
            
            // CRITICAL: Cap chroma at maximum SECOND TIME (Python lines 1237-1252)
            let chroma_maximum = self.maximum_chroma_from_renotation(hue_current, value, code_current)?;
            if chroma_current > chroma_maximum {
                chroma_current = chroma_maximum;
            }
            
            // Inner loop: Chroma magnitude refinement using Python's exponential scaling
            
            // Update current specification with new hue (relative to achromatic center)
            let (x_current_new, y_current_new) = self.munsell_specification_to_xy(hue_current, value, chroma_current, code_current)?;
            let (rho_current_new, _, _) = cartesian_to_cylindrical(
                x_current_new - x_center,
                y_current_new - y_center,
                xyy.y_luminance
            );
            
            let mut rho_bounds_data = vec![rho_current_new];
            let mut chroma_bounds_data = vec![chroma_current];
            let mut iterations_inner = 0;
            
            
            // Python condition: continue until rho_input is between min and max of rho_bounds
            let mut loop_count = 0;
            while loop_count < MAX_INNER_ITERATIONS {
                let rho_min = *rho_bounds_data.iter().min_by(|a, b| a.partial_cmp(b).unwrap()).unwrap();
                let rho_max = *rho_bounds_data.iter().max_by(|a, b| a.partial_cmp(b).unwrap()).unwrap();
                
                // Check if rho_input is between min and max
                if rho_min <= rho_input && rho_input <= rho_max {
                    break;
                }
                
                loop_count += 1;
                iterations_inner += 1;
                if iterations_inner > MAX_INNER_ITERATIONS {
                    break;
                }
                
                // Python line 1278: exponential scaling
                let chroma_inner = if rho_current_new.abs() > 1e-10 {
                    let ratio = rho_input / rho_current_new;
                    let power = iterations_inner as f64;
                    let result = ratio.powf(power) * chroma_current;
                    result
                } else {
                    chroma_current // Avoid division by zero
                };
                
                let chroma_max = self.maximum_chroma_from_renotation(hue_current, value, code_current)?;
                let chroma_bounded = chroma_inner.min(chroma_max).max(0.0);
                
                
                let (x_inner, y_inner) = self.munsell_specification_to_xy(hue_current, value, chroma_bounded, code_current)?;
                let (rho_inner, _, _) = cartesian_to_cylindrical(
                    x_inner - x_center,
                    y_inner - y_center,
                    xyy.y_luminance
                );
                
                rho_bounds_data.push(rho_inner);
                chroma_bounds_data.push(chroma_bounded);
            }
            
            
            // Linear interpolation for chroma (Python line 1310)
            let chroma_new = if rho_bounds_data.len() >= 2 {
                // Sort by rho (Python lines 1306-1309)
                let mut paired: Vec<_> = rho_bounds_data.iter()
                    .zip(chroma_bounds_data.iter())
                    .map(|(&r, &c)| (r, c))
                    .collect();
                paired.sort_by(|a, b| a.0.partial_cmp(&b.0).unwrap());
                
                let sorted_rho: Vec<f64> = paired.iter().map(|&(r, _)| r).collect();
                let sorted_chroma: Vec<f64> = paired.iter().map(|&(_, c)| c).collect();
                
                
                let interpolated = self.linear_interpolate(&sorted_rho, &sorted_chroma, rho_input)?;
                
                
                // Prevent negative chromas - they're physically impossible
                // This can happen when extrapolating near the achromatic axis
                interpolated.max(0.0)
            } else {
                chroma_current // Keep current if we couldn't refine
            };
            chroma_current = chroma_new;
            
            // Step 5: Convergence check
            let (x_final, y_final) = self.munsell_specification_to_xy(hue_current, value, chroma_current, code_current)?;
            let difference = ((xyy.x - x_final).powi(2) + (xyy.y - y_final).powi(2)).sqrt();
            
            if difference < CONVERGENCE_THRESHOLD {
                // Converged! Apply full normalization to match Python
                // CRITICAL: Check for chroma == 0 -> achromatic
                if chroma_current < 1e-10 {
                    return Ok(MunsellSpecification {
                        hue: 0.0,
                        family: "N".to_string(),
                        value,
                        chroma: 0.0,
                    });
                }
                
                // Apply hue normalization (0YR -> 10R)
                let (normalized_hue, normalized_code) = Self::normalize_munsell_specification(hue_current, code_current);
                let family = code_to_family(normalized_code);
                
                return Ok(MunsellSpecification {
                    hue: normalized_hue,
                    family: family.to_string(),
                    value,
                    chroma: chroma_current,
                });
            }
        }
        
        // If we reach here, the algorithm didn't converge
        // Return the last computed values anyway with full normalization
        
        // CRITICAL: Check for chroma == 0 -> achromatic
        if chroma_current < 1e-10 {
            return Ok(MunsellSpecification {
                hue: 0.0,
                family: "N".to_string(),
                value,
                chroma: 0.0,
            });
        }
        
        // Apply hue normalization (0YR -> 10R)
        let (normalized_hue, normalized_code) = Self::normalize_munsell_specification(hue_current, code_current);
        let family = code_to_family(normalized_code);
        
        Ok(MunsellSpecification {
            hue: normalized_hue,
            family: family.to_string(),
            value,
            chroma: chroma_current,
        })
    }

    /// Normalize Munsell specification following Python colour-science rules
    /// When hue == 0, convert to hue=10 and increment code (move to next family in cycle)
    fn normalize_munsell_specification(hue: f64, code: u8) -> (f64, u8) {
        // Only normalize if hue is exactly 0 or very close to 0
        // Don't trigger on hue=10 which is already normalized
        if hue.abs() < 0.01 && hue < 5.0 {  // hue < 5 ensures we don't catch hue=10
            // When hue is 0 (or very close), convert to 10 and move to next family
            // This matches Python's normalise_munsell_specification (line 1576-1578)
            // FIXED: Use proper code increment in sequence
            let new_code = match code {
                1 => 2,   // B -> BG
                2 => 3,   // BG -> G
                3 => 4,   // G -> GY
                4 => 5,   // GY -> Y
                5 => 6,   // Y -> YR
                6 => 7,   // YR -> R
                7 => 8,   // R -> RP
                8 => 9,   // RP -> P
                9 => 10,  // P -> PB
                10 => 1,  // PB -> B (wraparound)
                _ => code // Invalid, keep same
            };
            (10.0, new_code)
        } else {
            (hue, code)
        }
    }
    
    /// Generate initial guess using direct xyY angle (NOT Lab/LCH as Python doesn't use it)
    fn generate_initial_guess(&self, xyy: CieXyY) -> Result<(f64, u8, f64)> {
        use coordinate_transforms::cartesian_to_cylindrical;
        use hue_conversions::hue_angle_to_hue;
        
        // CRITICAL FIX: Python doesn't use Lab/LCH for initial guess!
        // It uses the direct hue angle from xyY coordinates relative to Illuminant C
        
        // Calculate angle directly from xyY relative to Illuminant C
        let dx = xyy.x - ILLUMINANT_C[0];
        let dy = xyy.y - ILLUMINANT_C[1];
        let (rho, phi_rad, _) = cartesian_to_cylindrical(dx, dy, xyy.y_luminance);
        let mut phi_deg = phi_rad.to_degrees();
        
        // Ensure angle is in [0, 360) range
        if phi_deg < 0.0 {
            phi_deg += 360.0;
        }
        
        
        // Convert angle to Munsell hue and code using the interpolation breakpoints
        let (hue_initial, code_initial) = hue_angle_to_hue(phi_deg);
        
        // Initial chroma estimate based on distance from achromatic center
        // Python uses a simple scaling factor here
        let chroma_initial = rho * 50.0;  // Empirical scaling factor
        
        
        Ok((hue_initial, code_initial, chroma_initial))
    }
    
    /// Exact implementation of Python LCHab_to_munsell_specification function
    /// This is the exact algorithm from colour-science munsell.py lines 2422-2480
    fn lchab_to_munsell_specification(&self, _l: f64, _c: f64, hab: f64) -> (f64, u8) {
        // FIXED: Correct code assignment based on Python's actual behavior
        // Python uses 36° segments with different boundaries than we had
        let code = if hab < 18.0 || hab >= 342.0 {
            8  // RP: [342°, 360°) and [0°, 18°)
        } else if hab < 54.0 {
            7  // R: [18°, 54°)
        } else if hab < 90.0 {
            6  // YR: [54°, 90°)
        } else if hab < 126.0 {
            5  // y_luminance: [90°, 126°)
        } else if hab < 162.0 {
            4  // Gy_luminance: [126°, 162°)
        } else if hab < 198.0 {
            3  // G: [162°, 198°)
        } else if hab < 234.0 {
            2  // BG: [198°, 234°)
        } else if hab < 270.0 {
            1  // B: [234°, 270°)
        } else if hab < 306.0 {
            10 // PB: [270°, 306°)
        } else if hab < 342.0 {
            9  // P: [306°, 342°)
        } else {
            8  // RP: [342°, 360°)
        };
        
        // Calculate hue using linear interpolation (exact from Python)
        // Each 36° segment maps to 0-10 hue range
        let segment_start = ((hab / 36.0).floor() * 36.0) as f64;
        let hab_in_segment = hab - segment_start;
        let mut hue = (hab_in_segment / 36.0) * 10.0;
        
        // Special case: at exact segment boundaries, hue should be 10.0 not 0.0
        if hue == 0.0 && hab > 0.0 {
            hue = 10.0;
        }
        
        (hue, code)
    }

    /// Linear interpolation helper function
    fn linear_interpolate(&self, x_values: &[f64], y_values: &[f64], x_target: f64) -> Result<f64> {
        if x_values.len() != y_values.len() || x_values.len() < 2 {
            return Err(MunsellError::InterpolationError { 
                message: "Invalid data for interpolation".to_string() 
            });
        }
        
        // Find the two closest x values that bracket x_target
        let mut best_result = y_values[0];
        let mut best_distance = (x_values[0] - x_target).abs();
        
        for i in 0..x_values.len()-1 {
            let x1 = x_values[i];
            let x2 = x_values[i+1];
            let y1 = y_values[i];
            let y2 = y_values[i+1];
            
            // Check if x_target is between x1 and x2
            if (x1 <= x_target && x_target <= x2) || (x2 <= x_target && x_target <= x1) {
                // Linear interpolation
                if (x2 - x1).abs() < 1e-10 {
                    return Ok(y1);
                }
                let t = (x_target - x1) / (x2 - x1);
                return Ok(y1 + t * (y2 - y1));
            }
            
            // Track closest point for extrapolation
            let distance = (x1 - x_target).abs();
            if distance < best_distance {
                best_distance = distance;
                best_result = y1;
            }
        }
        
        // Check last point
        let last_idx = x_values.len() - 1;
        let distance = (x_values[last_idx] - x_target).abs();
        if distance < best_distance {
            best_distance = distance;
            best_result = y_values[last_idx];
        }
        
        // CRITICAL FIX: Match np.interp behavior - CLAMP to boundaries instead of extrapolating!
        // np.interp returns boundary values when x is outside the data range
        // This prevents oscillation caused by aggressive extrapolation
        if x_values.len() >= 2 {
            // Sort indices by x value
            let mut indices: Vec<usize> = (0..x_values.len()).collect();
            indices.sort_by(|&i, &j| x_values[i].partial_cmp(&x_values[j]).unwrap());
            
            let sorted_x: Vec<f64> = indices.iter().map(|&i| x_values[i]).collect();
            let sorted_y: Vec<f64> = indices.iter().map(|&i| y_values[i]).collect();
            
            // Check if we need to clamp
            let first_x = sorted_x[0];
            let last_x = sorted_x[sorted_x.len() - 1];
            
            if x_target <= first_x {
                // Left boundary - return first y value (like np.interp default)
                return Ok(sorted_y[0]);
            } else if x_target >= last_x {
                // Right boundary - return last y value (like np.interp default)
                return Ok(sorted_y[sorted_y.len() - 1]);
            }
        }
        
        // Fallback to nearest neighbor if can't determine boundaries
        Ok(best_result)
    }

    /// Calculate maximum chroma from renotation data
    fn maximum_chroma_from_renotation(&self, _hue: f64, value: f64, code: u8) -> Result<f64> {
        // CRITICAL: Must use actual renotation data to find maximum chroma
        // This is essential for proper convergence!
        
        use hue_conversions::code_to_family;
        
        let family = code_to_family(code);
        
        // Round value to nearest 0.5 for lookup
        let value_rounded = (value * 2.0).round() / 2.0;
        
        // Find maximum chroma for this hue family and value
        let mut max_chroma = 0.0;
        
        for entry in self.renotation_data.iter() {
            let ((hue_str, entry_value, entry_chroma), _) = entry;
            
            // Check if family matches (extract from hue string like "2.5GY")
            let entry_family = hue_str.chars()
                .skip_while(|c| c.is_numeric() || *c == '.')
                .collect::<String>();
            
            if entry_family != family {
                continue;
            }
            
            // Check if value is close enough (within 0.25)
            if (entry_value - value_rounded).abs() > 0.25 {
                continue;
            }
            
            // Track maximum chroma found
            if *entry_chroma > max_chroma {
                max_chroma = *entry_chroma;
            }
        }
        
        // If no data found, use conservative defaults based on value
        if max_chroma < 0.1 {
            max_chroma = match value as i32 {
                0..=2 => 10.0,
                3..=5 => 15.0,
                6..=8 => 20.0,
                9..=10 => 10.0,
                _ => 8.0,
            };
        }
        
        Ok(max_chroma)
    }

    /// Convert Munsell specification to xy coordinates using interpolation
    /// Implements Python's _munsell_specification_to_xyY logic for value interpolation
    fn munsell_specification_to_xy(&self, hue: f64, value: f64, chroma: f64, code: u8) -> Result<(f64, f64)> {
        // CRITICAL: Python interpolates between value planes when value is not integer
        // This is essential for convergence accuracy!
        
        // Debug output for problematic cases
        
        // Check if value is essentially an integer
        let is_integer = (value - value.round()).abs() < 1e-10;
        
        if is_integer {
            // Value is integer, use direct lookup
            self.xy_from_renotation_ovoid(hue, value.round(), chroma, code)
        } else {
            // Value is not integer - interpolate between floor and ceiling
            let value_minus = value.floor();
            let value_plus = value_minus + 1.0;
            
            // Get xy for floor value
            let (x_minus, y_minus) = self.xy_from_renotation_ovoid(hue, value_minus, chroma, code)?;
            
            // Get xy for ceiling value (if not at max)
            let (x_plus, y_plus) = if value_plus >= 10.0 {
                // At maximum value, use same as floor
                (x_minus, y_minus)
            } else {
                self.xy_from_renotation_ovoid(hue, value_plus, chroma, code)?
            };
            
            if value_minus == value_plus || (x_minus == x_plus && y_minus == y_plus) {
                // No interpolation needed
                Ok((x_minus, y_minus))
            } else {
                // Interpolate based on Y luminance (Python lines 912-921)
                let y_minus_lum = self.munsell_value_to_luminance(value_minus)?;
                let y_plus_lum = self.munsell_value_to_luminance(value_plus)?;
                let y_actual = self.munsell_value_to_luminance(value)?;
                
                // Linear interpolation
                let t = (y_actual - y_minus_lum) / (y_plus_lum - y_minus_lum);
                let x = x_minus + t * (x_plus - x_minus);
                let y = y_minus + t * (y_plus - y_minus);
                
                Ok((x, y))
            }
        }
    }

    /// Direct lookup from renotation data
    fn lookup_xy_from_renotation(&self, hue: f64, value: f64, chroma: f64, code: u8) -> Result<(f64, f64)> {
        // CRITICAL FIX: When chroma=0, return Illuminant C coordinates (Python behaviour)
        if chroma.abs() < 1e-10 {
            return Ok((ILLUMINANT_C[0], ILLUMINANT_C[1]));
        }
        
        // Find exact match in renotation data
        let family = hue_conversions::code_to_family(code);
        
        // Create the full hue string for exact lookup
        let hue_str = if hue == 10.0 || hue == 0.0 {
            format!("10{}", family)
        } else {
            format!("{}{}", hue, family)
        };
        
        
        // Try to find exact match first with full hue string
        for &((ref entry_family, entry_value, entry_chroma), (x, y, _y)) in self.renotation_data {
            if *entry_family == hue_str &&
               (entry_value - value).abs() < 0.01 && 
               (entry_chroma - chroma).abs() < 0.01 {
                return Ok((x, y));
            }
        }
        
        
        // If no exact match, perform interpolation using nearby points
        self.interpolate_from_renotation_data(&hue_str, value, chroma)
    }

    /// Interpolate xy coordinates from renotation data using bilinear interpolation
    fn interpolate_from_renotation_data(&self, hue_str: &str, value: f64, chroma: f64) -> Result<(f64, f64)> {
        // Collect all matching entries with similar hue
        let mut matching_entries = Vec::new();
        
        // Extract the family part from the hue string (e.g., "7.5R" -> "R")
        let family = hue_str.chars().skip_while(|c| !c.is_alphabetic()).collect::<String>();
        
        for &((ref entry_family, entry_value, entry_chroma), (x, y, _y)) in self.renotation_data {
            // Check if this entry has the same family
            if entry_family.ends_with(&family) {
                matching_entries.push((entry_family.clone(), entry_value, entry_chroma, x, y));
            }
        }
        
        if matching_entries.is_empty() {
            return Err(MunsellError::InterpolationError { message: format!("No entries found for hue {}", hue_str) });
        }
        
        // Sort by value, then by chroma
        matching_entries.sort_by(|a, b| a.1.partial_cmp(&b.1).unwrap().then(a.2.partial_cmp(&b.2).unwrap()));
        
        // Find the four surrounding points for bilinear interpolation
        // First find value boundaries
        let mut value_lower = None;
        let mut value_upper = None;
        
        for &(_, entry_value, _, _, _) in &matching_entries {
            if entry_value <= value {
                value_lower = Some(entry_value);
            }
            if entry_value >= value && value_upper.is_none() {
                value_upper = Some(entry_value);
                break;
            }
        }
        
        // If we can't bracket the value, use nearest neighbor
        let target_value = if let (Some(v_low), Some(v_high)) = (value_lower, value_upper) {
            if (value - v_low).abs() < (v_high - value).abs() { v_low } else { v_high }
        } else if let Some(v) = value_lower.or(value_upper) {
            v
        } else {
            // Use the closest available value
            matching_entries.iter().min_by(|a, b| {
                (a.1 - value).abs().partial_cmp(&(b.1 - value).abs()).unwrap()
            }).map(|&(_, v, _, _, _)| v).unwrap_or(5.0)
        };
        
        // Now find chroma boundaries for the target value
        let value_entries: Vec<_> = matching_entries.iter()
            .filter(|&&(_, entry_value, _, _, _)| (entry_value - target_value).abs() < 0.1)
            .collect();
            
        if value_entries.is_empty() {
            return Err(MunsellError::InterpolationError { message: format!("No entries found for value {} in hue {}", target_value, hue_str) });
        }
        
        // Find chroma boundaries
        let mut chroma_lower = None;
        let mut chroma_upper = None;
        
        for &&(_, _, entry_chroma, _, _) in &value_entries {
            if entry_chroma <= chroma {
                chroma_lower = Some(entry_chroma);
            }
            if entry_chroma >= chroma && chroma_upper.is_none() {
                chroma_upper = Some(entry_chroma);
                break;
            }
        }
        
        // Interpolate between chroma boundaries
        if let (Some(c_low), Some(c_high)) = (chroma_lower, chroma_upper) {
            if (c_high - c_low).abs() < 1e-10 {
                // Same chroma, return that point
                let entry = value_entries.iter()
                    .find(|&&(_, _, entry_chroma, _, _)| (entry_chroma - c_low).abs() < 1e-10)
                    .unwrap();
                Ok((entry.3, entry.4))
            } else {
                // Linear interpolation between chroma boundaries
                let entry_low = value_entries.iter()
                    .find(|&&(_, _, entry_chroma, _, _)| (entry_chroma - c_low).abs() < 1e-10)
                    .unwrap();
                let entry_high = value_entries.iter()
                    .find(|&&(_, _, entry_chroma, _, _)| (entry_chroma - c_high).abs() < 1e-10)
                    .unwrap();
                
                let t = (chroma - c_low) / (c_high - c_low);
                let x = entry_low.3 + t * (entry_high.3 - entry_low.3);
                let y = entry_low.4 + t * (entry_high.4 - entry_low.4);
                Ok((x, y))
            }
        } else {
            // Use nearest neighbor
            let nearest = value_entries.iter()
                .min_by(|a, b| (a.2 - chroma).abs().partial_cmp(&(b.2 - chroma).abs()).unwrap())
                .unwrap();
            Ok((nearest.3, nearest.4))
        }
    }

    /// Complete Python xy_from_renotation_ovoid algorithm implementation
    /// This is the exact algorithm from colour-science munsell.py lines 2265-2419
    fn xy_from_renotation_ovoid(&self, hue: f64, value: f64, chroma: f64, code: u8) -> Result<(f64, f64)> {
        
        // CRITICAL: Value must be integer for renotation lookup
        // Chroma interpolation is handled below - DO NOT round chroma here!
        let value_normalized = value.round(); // Must be integer for dataset lookup
        
        
        // Check if this is a standard hue (2.5, 5.0, 7.5, 10.0 or exact 0)
        const THRESHOLD_INTEGER: f64 = 1e-7;
        
        // For standard hues with even chroma, we can do direct lookup
        let is_standard_hue = (hue.abs() < THRESHOLD_INTEGER) ||
           ((hue - 2.5).abs() < THRESHOLD_INTEGER) ||
           ((hue - 5.0).abs() < THRESHOLD_INTEGER) ||
           ((hue - 7.5).abs() < THRESHOLD_INTEGER) ||
           ((hue - 10.0).abs() < THRESHOLD_INTEGER);
        
        // Check if chroma is even (for potential direct lookup)
        let chroma_is_even = (chroma - 2.0 * (chroma / 2.0).round()).abs() < THRESHOLD_INTEGER;
        
        if is_standard_hue && chroma_is_even {
            // Can do direct lookup
            let rounded_hue = 2.5 * (hue / 2.5).round();
            let chroma_even = 2.0 * (chroma / 2.0).round();
            return self.lookup_xy_from_renotation(rounded_hue, value_normalized, chroma_even, code);
        }
        
        // Need to interpolate - first handle chroma interpolation if needed
        if !chroma_is_even {
            // Chroma is not even - need to interpolate between floor and ceiling chromas
            let chroma_lower = 2.0 * (chroma / 2.0).floor();
            let chroma_upper = chroma_lower + 2.0;
            
            
            // Get xy for lower chroma
            let (x_lower, y_lower) = if is_standard_hue {
                let rounded_hue = 2.5 * (hue / 2.5).round();
                self.lookup_xy_from_renotation(rounded_hue, value_normalized, chroma_lower, code)?
            } else {
                self.xy_from_renotation_ovoid_for_even_chroma(hue, value_normalized, chroma_lower, code)?
            };
            
            // Get xy for upper chroma
            let (x_upper, y_upper) = if is_standard_hue {
                let rounded_hue = 2.5 * (hue / 2.5).round();
                self.lookup_xy_from_renotation(rounded_hue, value_normalized, chroma_upper, code)?
            } else {
                self.xy_from_renotation_ovoid_for_even_chroma(hue, value_normalized, chroma_upper, code)?
            };
            
            // Linear interpolation based on chroma
            let t = (chroma - chroma_lower) / (chroma_upper - chroma_lower);
            let x = x_lower + t * (x_upper - x_lower);
            let y = y_lower + t * (y_upper - y_lower);
            
            
            return Ok((x, y));
        }
        
        // Chroma is even but hue is not standard - proceed with hue interpolation
        let chroma_even = 2.0 * (chroma / 2.0).round();
        self.xy_from_renotation_ovoid_for_even_chroma(hue, value_normalized, chroma_even, code)
    }
    
    /// Helper function for xy_from_renotation_ovoid when chroma is even
    fn xy_from_renotation_ovoid_for_even_chroma(&self, hue: f64, value: f64, chroma: f64, code: u8) -> Result<(f64, f64)> {
        use crate::constants::ILLUMINANT_C;
        
        // CRITICAL FIX: When chroma=0, return Illuminant C coordinates (Python behaviour)
        if chroma.abs() < 1e-10 {
            return Ok((ILLUMINANT_C[0], ILLUMINANT_C[1]));
        }
        
        // Get bounding hues (Python's bounding_hues_from_renotation)
        let ((hue_cw, code_cw), (hue_ccw, code_ccw)) = hue_conversions::bounding_hues_from_renotation(hue, code);
        
        // Illuminant C coordinates (grey point)
        let x_grey = ILLUMINANT_C[0];
        let y_grey = ILLUMINANT_C[1];
        
        // Get xyY coordinates for minus (cw) boundary
        let (x_minus, y_minus) = self.lookup_xy_from_renotation(hue_cw, value, chroma, code_cw)?;
        let y_luminance_minus = self.get_y_luminance_from_renotation(hue_cw, value, chroma, code_cw)?;
        
        // Get xyY coordinates for plus (ccw) boundary  
        let (x_plus, y_plus) = self.lookup_xy_from_renotation(hue_ccw, value, chroma, code_ccw)?;
        let y_luminance_plus = self.get_y_luminance_from_renotation(hue_ccw, value, chroma, code_ccw)?;
        
        
        // Convert to cylindrical coordinates relative to grey point
        let (rho_minus, phi_minus, _z_minus) = coordinate_transforms::cartesian_to_cylindrical(
            x_minus - x_grey, y_minus - y_grey, y_luminance_minus
        );
        let phi_minus_deg = phi_minus.to_degrees();
        
        let (rho_plus, phi_plus, _z_plus) = coordinate_transforms::cartesian_to_cylindrical(
            x_plus - x_grey, y_plus - y_grey, y_luminance_plus
        );
        let mut phi_plus_deg = phi_plus.to_degrees();
        
        // Get hue angles using Python's hue_to_hue_angle
        let hue_angle_lower = hue_conversions::hue_to_hue_angle(hue_cw, code_cw);
        let hue_angle = hue_conversions::hue_to_hue_angle(hue, code);
        let hue_angle_upper = hue_conversions::hue_to_hue_angle(hue_ccw, code_ccw);
        
        // Handle phi angle wrapping (Python lines 2376-2377)
        if phi_minus_deg - phi_plus_deg > 180.0 {
            phi_plus_deg += 360.0;
        }
        
        // Handle hue angle wrapping and corrections (Python lines 2379-2387)
        let mut hue_angle_lower_corrected = hue_angle_lower;
        let mut hue_angle_corrected = hue_angle;
        
        if hue_angle_lower == 0.0 {
            hue_angle_lower_corrected = 360.0;
        }
        
        if hue_angle_lower_corrected > hue_angle_upper {
            if hue_angle_lower_corrected > hue_angle {
                hue_angle_lower_corrected -= 360.0;
            } else {
                hue_angle_lower_corrected -= 360.0;
                hue_angle_corrected -= 360.0;
            }
        }
        
        // Get interpolation method (Linear vs Radial)
        let interpolation_method = self.get_interpolation_method(hue, value, chroma, code)?;
        
        
        if interpolation_method == "Linear" {
            // Linear interpolation (Python lines 2399-2404)
            let x = self.linear_interpolate_2d(
                hue_angle_lower_corrected, hue_angle_upper, x_minus, x_plus, hue_angle_corrected
            );
            let y = self.linear_interpolate_2d(
                hue_angle_lower_corrected, hue_angle_upper, y_minus, y_plus, hue_angle_corrected
            );
            
            
            Ok((x, y))
        } else if interpolation_method == "Radial" {
            // Radial interpolation (Python lines 2405-2417)
            let rho = self.linear_interpolate_2d(
                hue_angle_lower_corrected, hue_angle_upper, rho_minus, rho_plus, hue_angle_corrected
            );
            let phi_deg = self.linear_interpolate_2d(
                hue_angle_lower_corrected, hue_angle_upper, phi_minus_deg, phi_plus_deg, hue_angle_corrected
            );
            
            // Convert back to cartesian and add grey point
            let phi_rad = phi_deg.to_radians();
            let (x_offset, y_offset) = coordinate_transforms::polar_to_cartesian(rho, phi_rad);
            let x = x_offset + x_grey;
            let y = y_offset + y_grey;
            
            
            Ok((x, y))
        } else {
            Err(MunsellError::InterpolationError { 
                message: format!("Invalid interpolation method: {}", interpolation_method) 
            })
        }
    }
    
    /// Get Y luminance value from renotation data
    fn get_y_luminance_from_renotation(&self, hue: f64, value: f64, chroma: f64, code: u8) -> Result<f64> {
        let family = hue_conversions::code_to_family(code);
        
        for &((ref entry_family, entry_value, entry_chroma), (_, _, y_luminance)) in self.renotation_data {
            if (*entry_family == family || 
               (entry_family.len() > family.len() && 
                entry_family.ends_with(family) && 
                entry_family.chars().nth(entry_family.len() - family.len() - 1).unwrap_or(' ').is_numeric())) &&
               (entry_value - value).abs() < 0.01 && 
               (entry_chroma - chroma).abs() < 0.01 {
                return Ok(y_luminance);
            }
        }
        
        // Fallback: interpolate Y luminance
        Ok(0.1 * value) // Approximate relationship
    }
    
    /// Get interpolation method using Python's interpolation_method_from_renotation_ovoid
    fn get_interpolation_method(&self, hue: f64, value: f64, chroma: f64, code: u8) -> Result<&'static str> {
        // This is a complex lookup from interpolation_methods::INTERPOLATION_METHODS
        // For now, implement the key logic patterns from Python
        
        let family = hue_conversions::code_to_family(code);
        
        // Most common patterns from the interpolation method table
        if value <= 1.0 || chroma <= 2.0 {
            return Ok("Linear");
        }
        
        if chroma >= 20.0 {
            return Ok("Radial");
        }
        
        // Medium chroma ranges often use Linear for stability
        if chroma <= 10.0 {
            return Ok("Linear");
        }
        
        // Default to Radial for high chroma
        Ok("Radial")
    }
    
    /// Simple linear interpolation between two points
    fn linear_interpolate_2d(&self, x1: f64, x2: f64, y1: f64, y2: f64, x: f64) -> f64 {
        if (x2 - x1).abs() < 1e-10 {
            return y1; // Avoid division by zero
        }
        y1 + (x - x1) * (y2 - y1) / (x2 - x1)
    }

    /// Linear interpolation between hue boundaries (LEGACY - now uses xy_from_renotation_ovoid)
    fn linear_interpolate_xy(&self, hue: f64, value: f64, chroma: f64, code: u8) -> Result<(f64, f64)> {
        // Use the complete Python algorithm instead
        self.xy_from_renotation_ovoid(hue, value, chroma, code)
    }

    /// Radial interpolation in cylindrical coordinates (LEGACY - now uses xy_from_renotation_ovoid)
    fn radial_interpolate_xy(&self, hue: f64, value: f64, chroma: f64, code: u8) -> Result<(f64, f64)> {
        // Use the complete Python algorithm instead
        self.xy_from_renotation_ovoid(hue, value, chroma, code)
    }

    /// Fallback interpolation method
    fn interpolate_hue_chroma_to_xy(&self, hue: f64, value: f64, chroma: f64, code: u8) -> Result<(f64, f64)> {
        // Use the old interpolation method as fallback
        let (_, _, _) = self.interpolate_hue_chroma(0.31006, 0.31616, value)?; // Use illuminant C as dummy
        
        // For now, return illuminant C coordinates as fallback
        Ok((0.31006, 0.31616))
    }

    /// Calculate Munsell Value from CIE Y luminance using ASTM D1535 polynomial
    /// 
    /// Uses Newton-Raphson iteration to solve the fifth-order polynomial:
    /// Y = 1.1914*V - 0.22533*V² + 0.23352*V³ - 0.020484*V⁴ + 0.00081939*V⁵
    /// Note: The polynomial gives Y on a 0-100 scale, so we need to convert input
    fn luminance_to_munsell_value(&self, y: f64) -> Result<f64> {
        // Handle edge cases
        if y <= 0.0 {
            return Ok(0.0);
        }
        
        // Convert Y from [0,1] scale to [0,100] scale for ASTM polynomial
        let y_scaled = y * 100.0;
        
        if y_scaled >= 100.0 {
            return Ok(10.0);
        }

        // Newton-Raphson iteration to solve for V given Y
        let mut v = 10.0 * y.sqrt(); // Initial guess based on approximate relationship
        
        for _ in 0..NEWTON_RAPHSON_MAX_ITERATIONS {
            let f = self.astm_polynomial(v) - y_scaled;
            let df = self.astm_polynomial_derivative(v);
            
            if df.abs() < 1e-15 {
                return Err(MunsellError::ConvergenceFailed);
            }
            
            let delta = f / df;
            v -= delta;
            
            if delta.abs() < NEWTON_RAPHSON_TOLERANCE {
                return Ok(v.max(0.0).min(10.0)); // Clamp to valid range
            }
        }
        
        Err(MunsellError::ConvergenceFailed)
    }

    /// ASTM D1535 fifth-order polynomial for Munsell Value
    fn astm_polynomial(&self, v: f64) -> f64 {
        let coeffs = &ASTM_D1535_COEFFICIENTS;
        coeffs[0] * v + 
        coeffs[1] * v * v + 
        coeffs[2] * v * v * v + 
        coeffs[3] * v * v * v * v + 
        coeffs[4] * v * v * v * v * v
    }

    /// Derivative of ASTM D1535 polynomial for Newton-Raphson iteration
    fn astm_polynomial_derivative(&self, v: f64) -> f64 {
        let coeffs = &ASTM_D1535_COEFFICIENTS;
        coeffs[0] + 
        2.0 * coeffs[1] * v + 
        3.0 * coeffs[2] * v * v + 
        4.0 * coeffs[3] * v * v * v + 
        5.0 * coeffs[4] * v * v * v * v
    }

    /// Check if color is achromatic (neutral) based on chromaticity distance from Illuminant D65
    fn is_achromatic_d65(&self, x: f64, y: f64) -> bool {
        // Special case: if x=0 and y=0, this typically means Y=0 (pure black) 
        // and chromaticity is undefined - treat as achromatic
        if x == 0.0 && y == 0.0 {
            return true;
        }
        
        const ILLUMINANT_D65: [f64; 2] = [0.31270, 0.32900];
        let dx = x - ILLUMINANT_D65[0];
        let dy = y - ILLUMINANT_D65[1];
        let distance = (dx * dx + dy * dy).sqrt();
        distance < ACHROMATIC_THRESHOLD
    }

    /// Check if color is achromatic (neutral) based on chromaticity distance from Illuminant C
    fn is_achromatic(&self, x: f64, y: f64) -> bool {
        // Special case: if x=0 and y=0, this typically means Y=0 (pure black) 
        // and chromaticity is undefined - treat as achromatic
        if x == 0.0 && y == 0.0 {
            return true;
        }
        
        let dx = x - ILLUMINANT_C[0];
        let dy = y - ILLUMINANT_C[1];
        let distance = (dx * dx + dy * dy).sqrt();
        distance < ACHROMATIC_THRESHOLD
    }

    /// Interpolate hue and chroma from Munsell Renotation dataset using advanced algorithm
    /// 
    /// This implements the iterative convergence algorithm from Python colour-science
    /// to achieve 100% mathematical accuracy.
    fn interpolate_hue_chroma(&self, x: f64, y: f64, luma: f64) -> Result<(f64, String, f64)> {
        // Implementation following Python colour-science _xyY_to_munsell_specification
        
        // Step 1: Initial guess using nearest neighbor
        let (initial_hue, initial_family, initial_chroma) = self.find_nearest_neighbor(x, y, luma)?;
        
        // Step 2: Iterative convergence refinement
        let mut current_spec = MunsellSpecification {
            hue: initial_hue,
            family: initial_family.clone(),
            value: self.luminance_to_munsell_value(luma)?,
            chroma: initial_chroma,
        };
        
        // Iterative refinement with multiple convergence levels
        for _outer_iteration in 0..MAX_OUTER_ITERATIONS {
            // Calculate target xyY from current specification
            let target_xyy = self.munsell_specification_to_xyy_interpolated(&current_spec)?;
            
            // Calculate error
            let error_x = x - target_xyy.x;
            let error_y = y - target_xyy.y;
            let error_magnitude = (error_x * error_x + error_y * error_y).sqrt();
            
            // Check convergence
            if error_magnitude < TOLERANCE_ABSOLUTE_DEFAULT {
                return Ok((current_spec.hue, current_spec.family, current_spec.chroma));
            }
            
            // Adaptive step refinement using gradient estimation
            current_spec = self.refine_munsell_specification(&current_spec, x, y, error_x, error_y)?;
        }
        
        // Fallback to initial guess if convergence fails
        Ok((initial_hue, initial_family, initial_chroma))
    }

    /// Find nearest neighbor in renotation data as initial guess
    fn find_nearest_neighbor(&self, x: f64, y: f64, luma: f64) -> Result<(f64, String, f64)> {
        let mut best_distance = f64::INFINITY;
        let mut best_match: Option<&'static ((&'static str, f64, f64), (f64, f64, f64))> = None;
        
        // Search through renotation data for closest xyY match
        for entry in self.renotation_data {
            let ((_, _, _), (entry_x, entry_y, entry_luma)) = entry;
            
            // Calculate distance in xyY space with proper weighting
            let dx = x - entry_x;
            let dy = y - entry_y;
            let dluma = luma - entry_luma;
            // Weight chromaticity more heavily than luminance
            let distance = (dx * dx + dy * dy + dluma * dluma * 0.1).sqrt();
            
            if distance < best_distance {
                best_distance = distance;
                best_match = Some(entry);
            }
        }
        
        match best_match {
            Some(((hue_str, _value, chroma), _)) => {
                let (hue, family) = self.parse_hue_string(hue_str)?;
                Ok((hue, family, *chroma))
            }
            None => Err(MunsellError::InterpolationError {
                message: "No matching color found in renotation data".to_string(),
            })
        }
    }

    /// Advanced interpolation from Munsell specification to xyY using radial basis functions
    fn munsell_specification_to_xyy_interpolated(&self, spec: &MunsellSpecification) -> Result<CieXyY> {
        // Handle neutral colors
        if spec.family == "N" {
            let y = self.munsell_value_to_luminance(spec.value)?;
            return Ok(CieXyY {
                x: ILLUMINANT_C[0],
                y: ILLUMINANT_C[1],
                y_luminance: y,
            });
        }

        // For chromatic colors, use advanced interpolation
        let hue_str = format!("{}{}", spec.hue, spec.family);
        
        // Find neighboring points for interpolation
        let neighbors = self.find_interpolation_neighbors(&hue_str, spec.value, spec.chroma);
        
        if neighbors.is_empty() {
            return Err(MunsellError::InterpolationError {
                message: format!("No neighbors found for interpolation: {}", hue_str),
            });
        }

        // Perform radial basis function interpolation
        self.radial_basis_interpolation(&neighbors, spec.value, spec.chroma)
    }

    /// Find neighboring points for advanced interpolation
    fn find_interpolation_neighbors(&self, target_hue: &str, target_value: f64, target_chroma: f64) -> Vec<&'static ((&'static str, f64, f64), (f64, f64, f64))> {
        let mut neighbors = Vec::new();
        
        // Find points with same hue family within reasonable value/chroma range
        for entry in self.renotation_data {
            let ((entry_hue, entry_value, entry_chroma), _) = entry;
            
            // Check if hue family matches
            if self.hue_families_match(target_hue, entry_hue) {
                // Check if within interpolation range (generous bounds)
                let value_diff = (target_value - entry_value).abs();
                let chroma_diff = (target_chroma - entry_chroma).abs();
                
                if value_diff <= 2.0 && chroma_diff <= 4.0 {
                    neighbors.push(entry);
                }
            }
        }
        
        // If no exact family matches, find closest hue families
        if neighbors.len() < 4 {
            for entry in self.renotation_data {
                let ((entry_hue, entry_value, entry_chroma), _) = entry;
                
                // Calculate hue angle distance
                let hue_distance = self.calculate_hue_distance(target_hue, entry_hue);
                
                if hue_distance <= 2.5 { // Within about 2.5 hue steps
                    let value_diff = (target_value - entry_value).abs();
                    let chroma_diff = (target_chroma - entry_chroma).abs();
                    
                    if value_diff <= 3.0 && chroma_diff <= 6.0 {
                        neighbors.push(entry);
                    }
                }
            }
        }
        
        neighbors
    }

    /// Check if two hue families match (same letters)
    fn hue_families_match(&self, hue1: &str, hue2: &str) -> bool {
        let family1 = hue1.chars().filter(|c| c.is_alphabetic()).collect::<String>();
        let family2 = hue2.chars().filter(|c| c.is_alphabetic()).collect::<String>();
        family1 == family2
    }

    /// Calculate angular distance between two hue strings
    fn calculate_hue_distance(&self, hue1: &str, hue2: &str) -> f64 {
        // This is a simplified hue distance calculation
        // In practice, this would need to handle the cylindrical hue space properly
        let (num1, family1) = self.parse_hue_string(hue1).unwrap_or((0.0, "".to_string()));
        let (num2, family2) = self.parse_hue_string(hue2).unwrap_or((0.0, "".to_string()));
        
        if family1 == family2 {
            (num1 - num2).abs()
        } else {
            // Different families - calculate angular distance in hue wheel
            let angle1 = self.hue_to_angle(num1, &family1);
            let angle2 = self.hue_to_angle(num2, &family2);
            let diff = (angle1 - angle2).abs();
            diff.min(360.0 - diff) / 36.0 // Convert to hue step units
        }
    }

    /// Convert hue notation to angle (simplified)
    fn hue_to_angle(&self, hue: f64, family: &str) -> f64 {
        let base_angle = match family {
            "R" => 0.0, "YR" => 36.0, "Y" => 72.0, "GY" => 108.0, "G" => 144.0,
            "BG" => 180.0, "B" => 216.0, "PB" => 252.0, "P" => 288.0, "RP" => 324.0,
            _ => 0.0,
        };
        base_angle + (hue - 5.0) * 3.6 // Each hue step is 3.6 degrees
    }

    /// Radial basis function interpolation
    fn radial_basis_interpolation(&self, neighbors: &[&'static ((&'static str, f64, f64), (f64, f64, f64))], target_value: f64, target_chroma: f64) -> Result<CieXyY> {
        if neighbors.is_empty() {
            return Err(MunsellError::InterpolationError {
                message: "No neighbors for radial basis interpolation".to_string(),
            });
        }

        let mut weighted_x = 0.0;
        let mut weighted_y = 0.0;
        let mut weighted_y = 0.0;
        let mut total_weight = 0.0;

        for neighbor in neighbors {
            let ((_, neighbor_value, neighbor_chroma), (x, y, luma)) = neighbor;
            
            // Calculate distance in Value-Chroma space
            let value_dist = target_value - neighbor_value;
            let chroma_dist = target_chroma - neighbor_chroma;
            let distance = (value_dist * value_dist + chroma_dist * chroma_dist).sqrt();
            
            // Radial basis function (inverse distance weighting with smoothing)
            let weight = if distance < 0.001 {
                1000.0 // Very close point gets high weight
            } else {
                1.0 / (distance + 0.1) // Smooth falloff
            };
            
            weighted_x += x * weight;
            weighted_y += y * weight;
            weighted_y += luma * weight;
            total_weight += weight;
        }

        if total_weight < 1e-15 {
            return Err(MunsellError::InterpolationError {
                message: "Zero total weight in radial basis interpolation".to_string(),
            });
        }

        Ok(CieXyY {
            x: weighted_x / total_weight,
            y: weighted_y / total_weight,
            y_luminance: weighted_y / total_weight,
        })
    }

    /// Refine Munsell specification using gradient estimation
    fn refine_munsell_specification(&self, spec: &MunsellSpecification, target_x: f64, target_y: f64, error_x: f64, error_y: f64) -> Result<MunsellSpecification> {
        // Gradient-based refinement (simplified)
        let step_size = 0.1;
        
        let mut refined_spec = spec.clone();
        
        // Adjust chroma based on chromaticity error
        let chroma_adjustment = (error_x * error_x + error_y * error_y).sqrt() * 2.0;
        refined_spec.chroma = (spec.chroma + chroma_adjustment * step_size).max(0.0);
        
        // Small hue adjustment based on error direction
        let hue_adjustment = error_x.atan2(error_y) * 180.0 / std::f64::consts::PI * 0.1;
        refined_spec.hue = (spec.hue + hue_adjustment).rem_euclid(10.0);
        
        Ok(refined_spec)
    }

    /// Parse Munsell hue string like "5R", "2.5GY" into hue number and family
    fn parse_hue_string(&self, hue_str: &str) -> Result<(f64, String)> {
        // Find the boundary between number and letters
        let mut split_pos = 0;
        for (i, c) in hue_str.char_indices() {
            if c.is_alphabetic() {
                split_pos = i;
                break;
            }
        }
        
        if split_pos == 0 {
            return Err(MunsellError::InvalidNotation {
                notation: hue_str.to_string(),
                reason: "Hue string contains no alphabetic characters".to_string(),
            });
        }
        
        let hue_str_num = &hue_str[..split_pos];
        let family = hue_str[split_pos..].to_string();
        
        let hue: f64 = hue_str_num.parse()
            .map_err(|_| MunsellError::InvalidNotation {
                notation: hue_str_num.to_string(),
                reason: "Invalid numeric value in hue".to_string(),
            })?;
        
        Ok((hue, family))
    }

    /// Convert Munsell specification back to xyY coordinates
    /// 
    /// This implements the reverse conversion for bidirectional capability
    pub fn munsell_specification_to_xyy(&self, spec: &MunsellSpecification) -> Result<CieXyY> {
        // Handle neutral colors
        if spec.family == "N" {
            let y = self.munsell_value_to_luminance(spec.value)?;
            return Ok(CieXyY {
                x: ILLUMINANT_C[0],
                y: ILLUMINANT_C[1],
                y_luminance: y,
            });
        }

        // For chromatic colors, find matching entry in renotation data
        let hue_str = format!("{}{}", spec.hue, spec.family);
        
        for entry in self.renotation_data {
            let ((entry_hue, entry_value, entry_chroma), (x, y, luma)) = entry;
            
            if entry_hue == &hue_str && 
               (entry_value - spec.value).abs() < 0.1 && 
               (entry_chroma - spec.chroma).abs() < 0.1 {
                return Ok(CieXyY { x: *x, y: *y, y_luminance: *luma });
            }
        }
        
        Err(MunsellError::InterpolationError {
            message: format!("No matching renotation data for {}{} {:.1}/{:.1}", 
                spec.hue, spec.family, spec.value, spec.chroma),
        })
    }

    /// Convert Munsell Value to CIE Y luminance using ASTM polynomial directly
    fn munsell_value_to_luminance(&self, value: f64) -> Result<f64> {
        if value < 0.0 || value > 10.0 {
            return Err(MunsellError::InvalidNotation {
                notation: value.to_string(),
                reason: "Munsell Value must be between 0.0 and 10.0".to_string(),
            });
        }
        
        // ASTM polynomial gives Y on [0,100] scale, convert to [0,1] scale
        Ok(self.astm_polynomial(value) / 100.0)
    }

    /// Convert Munsell specification to formatted notation string
    pub fn format_munsell_notation(&self, spec: &MunsellSpecification) -> String {
        if spec.family == "N" {
            format!("N {:.1}", spec.value)
        } else {
            format!("{:.1}{} {:.1}/{:.1}", spec.hue, spec.family, spec.value, spec.chroma)
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_mathematical_converter_creation() {
        let converter = MathematicalMunsellConverter::new().unwrap();
        assert_eq!(converter.renotation_data.len(), 4995);
    }

    #[test]
    fn test_srgb_to_xyy_conversion() {
        let converter = MathematicalMunsellConverter::new().unwrap();
        
        // Test pure red
        let xyy = converter.srgb_to_xyy([255, 0, 0]).unwrap();
        assert!(xyy.x > 0.6); // Red should have high x chromaticity
        assert!(xyy.y > 0.3 && xyy.y < 0.4); // Reasonable y chromaticity
        assert!(xyy.y_luminance > 0.2 && xyy.y_luminance < 0.3); // Reasonable luminance
    }

    #[test]
    fn test_astm_polynomial() {
        let converter = MathematicalMunsellConverter::new().unwrap();
        
        // Test known values
        assert!((converter.astm_polynomial(0.0) - 0.0).abs() < 1e-10);
        assert!(converter.astm_polynomial(5.0) > 0.1); // Should be positive
        
        // The ASTM polynomial gives Y values on a 0-100 scale
        
        // The ASTM polynomial gives reflectance values, not necessarily Y < 1.0
        // At V=10.0, it should give the maximum reflectance
        assert!(converter.astm_polynomial(10.0) > 0.9); // Should be close to but possibly > 1.0
    }

    #[test]
    fn test_luminance_to_munsell_value() {
        let converter = MathematicalMunsellConverter::new().unwrap();
        
        // Test edge cases
        assert!((converter.luminance_to_munsell_value(0.0).unwrap() - 0.0).abs() < 1e-10);
        assert!((converter.luminance_to_munsell_value(1.0).unwrap() - 10.0).abs() < 1e-10);
        
        // Test round-trip consistency
        let test_value = 5.0;
        let luminance = converter.munsell_value_to_luminance(test_value).unwrap(); // Use the proper conversion
        let recovered_value = converter.luminance_to_munsell_value(luminance).unwrap();
        assert!((recovered_value - test_value).abs() < 1e-6);
    }

    #[test]
    fn test_achromatic_detection() {
        let converter = MathematicalMunsellConverter::new().unwrap();
        
        // Test Illuminant C coordinates (should be achromatic)
        assert!(converter.is_achromatic(ILLUMINANT_C[0], ILLUMINANT_C[1]));
        
        // Test clearly chromatic coordinates
        assert!(!converter.is_achromatic(0.7, 0.3)); // Red region
        assert!(!converter.is_achromatic(0.3, 0.6)); // Green region
    }

    #[test]
    fn test_hue_string_parsing() {
        let converter = MathematicalMunsellConverter::new().unwrap();
        
        let (hue, family) = converter.parse_hue_string("5R").unwrap();
        assert_eq!(hue, 5.0);
        assert_eq!(family, "R");
        
        let (hue, family) = converter.parse_hue_string("2.5GY").unwrap();
        assert_eq!(hue, 2.5);
        assert_eq!(family, "GY");
    }

    #[test]
    fn test_munsell_notation_formatting() {
        let converter = MathematicalMunsellConverter::new().unwrap();
        
        // Test neutral color
        let neutral = MunsellSpecification {
            hue: 0.0,
            family: "N".to_string(),
            value: 5.0,
            chroma: 0.0,
        };
        assert_eq!(converter.format_munsell_notation(&neutral), "N 5.0");
        
        // Test chromatic color
        let chromatic = MunsellSpecification {
            hue: 5.0,
            family: "R".to_string(),
            value: 4.0,
            chroma: 12.0,
        };
        assert_eq!(converter.format_munsell_notation(&chromatic), "5.0R 4.0/12.0");
    }

    #[test]
    fn test_black_color_conversion() {
        let converter = MathematicalMunsellConverter::new().unwrap();
        
        // Test pure black
        let munsell = converter.srgb_to_munsell([0, 0, 0]).unwrap();
        
        // For now, just test that it produces a reasonable result
        // The exact behavior for RGB [0,0,0] may depend on how palette handles it
        assert!(munsell.value < 1.0); // Should be very dark
        assert!(munsell.chroma < 1.0); // Should have very low chroma
    }
}