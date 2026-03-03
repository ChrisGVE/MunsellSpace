//! Munsell hue string parsing and formatting.

use super::types::MunsellSpec;
use super::HUE_FAMILIES;

/// Parse a Munsell hue string to a numeric hue value (0-40).
///
/// The Munsell hue circle has 40 steps:
/// - 0 = 10RP (wraps to start)
/// - 4 = 10R
/// - 8 = 10YR
/// - 12 = 10Y
/// - 16 = 10GY
/// - 20 = 10G
/// - 24 = 10BG
/// - 28 = 10B
/// - 32 = 10PB
/// - 36 = 10P
///
/// Each step represents 2.5 hue units within a family.
///
/// # Arguments
/// * `hue` - Munsell hue string like "5R", "2.5YR", "10PB"
///
/// # Returns
/// Hue number from 0-40, or None if parsing fails.
///
/// # Examples
/// ```
/// use munsellspace::semantic_overlay::parse_hue_to_number;
///
/// assert!((parse_hue_to_number("5R").unwrap() - 2.0).abs() < 0.001);
/// assert!((parse_hue_to_number("10R").unwrap() - 4.0).abs() < 0.001);
/// assert!((parse_hue_to_number("2.5YR").unwrap() - 5.0).abs() < 0.001);
/// ```
pub fn parse_hue_to_number(hue: &str) -> Option<f64> {
    // Find which family by checking suffixes (longest first to handle "PB" vs "B")
    let families_by_length: [&str; 10] = ["YR", "GY", "BG", "PB", "RP", "R", "Y", "G", "B", "P"];

    let (family, family_idx) = families_by_length
        .iter()
        .find_map(|&fam| {
            if hue.ends_with(fam) {
                let idx = HUE_FAMILIES.iter().position(|&f| f == fam)?;
                Some((fam, idx))
            } else {
                None
            }
        })?;

    // Extract the numeric part
    let num_str = hue.strip_suffix(family)?;
    let num: f64 = num_str.parse().ok()?;

    // Validate range
    if !(0.0..=10.0).contains(&num) {
        return None;
    }

    // Calculate hue number
    let family_start = family_idx as f64 * 4.0;
    let hue_number = (family_start + num / 2.5) % 40.0;

    Some(hue_number)
}

/// Convert a numeric hue (0-40) back to a Munsell hue string.
///
/// # Arguments
/// * `hue_number` - Hue value from 0-40
///
/// # Returns
/// Tuple of (hue_string, family_letter) like ("5R", "R")
///
/// # Examples
/// ```
/// use munsellspace::semantic_overlay::hue_number_to_string;
///
/// let (hue, family) = hue_number_to_string(2.0);
/// assert_eq!(hue, "5R");
/// assert_eq!(family, "R");
/// ```
pub fn hue_number_to_string(hue_number: f64) -> (String, &'static str) {
    // Normalize to 0-40
    let normalized = ((hue_number % 40.0) + 40.0) % 40.0;

    // Calculate within-family position first (0-10 range, where 10 wraps to next family)
    let within_family = (normalized % 4.0) * 2.5;

    // Handle edge case: if within_family is very close to 0, use 10 of PREVIOUS family
    let (final_family_idx, final_num) = if within_family < 0.001 && normalized > 0.001 {
        // At boundary (e.g., hue 32) - use 10 of previous family (e.g., 10PB not 0P)
        let prev_family_idx = ((normalized / 4.0).floor() as usize + 9) % 10;
        (prev_family_idx, 10.0_f64)
    } else if within_family < 0.001 {
        // At hue 0 (10RP)
        (9, 10.0_f64) // 10RP
    } else {
        // Normal case
        let family_idx = (normalized / 4.0).floor() as usize % 10;
        (family_idx, within_family)
    };

    let final_family = HUE_FAMILIES[final_family_idx % 10];

    // Format the hue string
    let hue_str = if (final_num - final_num.round()).abs() < 0.001 {
        format!("{}{}", final_num.round() as i32, final_family)
    } else {
        format!("{:.1}{}", final_num, final_family)
    };

    (hue_str, final_family)
}

/// Parse a full Munsell notation string to MunsellSpec.
///
/// # Arguments
/// * `notation` - Munsell notation like "5R 4.0/12.0" or "N 5.0/"
///
/// # Returns
/// MunsellSpec or None if parsing fails.
pub fn parse_munsell_notation(notation: &str) -> Option<MunsellSpec> {
    let notation = notation.trim();

    // Handle neutral colors
    if notation.starts_with("N ") {
        let value_str = notation.strip_prefix("N ")?.trim_end_matches('/');
        let value: f64 = value_str.parse().ok()?;
        return Some(MunsellSpec::neutral(value));
    }

    // Parse chromatic: "5R 4.0/12.0"
    let parts: Vec<&str> = notation.split_whitespace().collect();
    if parts.len() != 2 {
        return None;
    }

    let hue_number = parse_hue_to_number(parts[0])?;

    let vc_parts: Vec<&str> = parts[1].split('/').collect();
    if vc_parts.len() != 2 {
        return None;
    }

    let value: f64 = vc_parts[0].parse().ok()?;
    let chroma: f64 = vc_parts[1].parse().ok()?;

    Some(MunsellSpec::new(hue_number, value, chroma))
}
