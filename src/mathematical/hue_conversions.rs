//! Hue angle conversion functions following Python colour-science exact implementation.

/// Hue family codes as used in Python colour-science
#[allow(dead_code)]
const HUE_FAMILY_CODES: [(u8, &str); 10] = [
    (1, "BG"), (2, "G"), (3, "GY"), (4, "Y"), (5, "YR"),
    (6, "R"), (7, "RP"), (8, "P"), (9, "PB"), (10, "B")
];

/// Convert [hue, code] to ASTM hue angle.
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

/// Convert hue angle to [hue, code] pair.
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

/// Linear interpolation for hue angle mapping.
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

/// Find the two bounding hues from Munsell Renotation System data.
/// Exact implementation from Python colour-science
pub fn bounding_hues_from_renotation(hue: f64, code: u8) -> ((f64, u8), (f64, u8)) {
    let mut hue_cw: f64;
    let code_cw: u8;
    let mut hue_ccw: f64;
    let code_ccw: u8;

    // Check if hue is exact multiple of 2.5
    if (hue % 2.5 - 0.0).abs() < 1e-10 {
        if (hue - 0.0).abs() < 1e-10 {
            // Special case: hue == 0
            hue_cw = 10.0;
            code_cw = increment_code(code);
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
            code_cw = increment_code(code);
        } else {
            code_cw = code;
        }
        code_ccw = code;
    }

    ((hue_cw, code_cw), (hue_ccw, code_ccw))
}

/// Increment code in the Munsell hue sequence
fn increment_code(code: u8) -> u8 {
    match code {
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
    }
}

/// Convert code number to hue family name.
/// FIXED: Python's MUNSELL_HUE_LETTER_CODES mapping
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

/// Convert family name to code number.
/// FIXED: Python's MUNSELL_HUE_LETTER_CODES dictionary
#[allow(dead_code)]
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

/// Convert hue and code to hue angle in degrees.
/// Exact implementation of Python colour-science hue_to_hue_angle function
pub fn hue_to_hue_angle(hue: f64, code: u8) -> f64 {
    // Calculate single_hue following exact Python formula
    // FIXED: Python's formula uses (18 - code) for their mapping
    let single_hue = ((18.0 - code as f64) % 10.0 + (hue / 10.0) - 0.5) % 10.0;

    // Use linear interpolation with exact Python breakpoints
    linear_interpolate_hue_angle(single_hue)
}
