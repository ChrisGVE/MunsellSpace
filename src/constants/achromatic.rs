//! Achromatic (neutral) color constants for ISCC-NBS classification
//! 
//! This module contains the value boundaries and color number mappings
//! for achromatic colors in the ISCC-NBS system.

/// Achromatic color boundaries and corresponding ISCC-NBS color numbers
/// Format: (lower_value_exclusive, upper_value_inclusive, color_number, color_name)
/// Value ranges are: black (0-2.5), dark gray (2.5-4.5), medium gray (4.5-6.5), 
/// light gray (6.5-8.5), white (8.5-10.0)
pub const ACHROMATIC_BOUNDARIES: &[(f64, f64, u16, &str)] = &[
    (0.0, 2.5, 267, "black"),
    (2.5, 4.5, 266, "dark gray"),
    (4.5, 6.5, 265, "medium gray"), 
    (6.5, 8.5, 264, "light gray"),
    (8.5, 10.0, 263, "white"),
];

/// Get the ISCC-NBS color number for an achromatic color based on its Munsell value
/// Returns None if the value is outside the valid range (0-10)
pub fn get_achromatic_color_number(value: f64) -> Option<u16> {
    if value < 0.0 || value > 10.0 {
        return None;
    }
    
    for &(lower, upper, color_number, _) in ACHROMATIC_BOUNDARIES {
        if value > lower && value <= upper {
            return Some(color_number);
        }
    }
    
    None
}

/// Get the ISCC-NBS color name for an achromatic color based on its Munsell value
/// Returns None if the value is outside the valid range (0-10)
pub fn get_achromatic_color_name(value: f64) -> Option<&'static str> {
    if value < 0.0 || value > 10.0 {
        return None;
    }
    
    for &(lower, upper, _, name) in ACHROMATIC_BOUNDARIES {
        if value > lower && value <= upper {
            return Some(name);
        }
    }
    
    None
}

/// Check if a hue represents an achromatic (neutral) color
/// Recognizes various neutral notations: "N", "0N", "0.0N", etc.
pub fn is_achromatic_hue(hue: &str) -> bool {
    let hue = hue.trim().to_uppercase();
    
    // Check for just "N"
    if hue == "N" {
        return true;
    }

    // Check if it ends with N and everything before it is numeric (digits or decimal point)
    if let Some(n_pos) = hue.rfind('N') {
        let prefix = &hue[..n_pos];
        return prefix.is_empty() || prefix.chars().all(|c| c.is_ascii_digit() || c == '.');
    }

    false
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_achromatic_value_boundaries() {
        // Test exact boundary values
        assert_eq!(get_achromatic_color_number(0.0), None); // 0.0 is not > 0.0
        assert_eq!(get_achromatic_color_number(0.1), Some(267)); // black
        assert_eq!(get_achromatic_color_number(2.5), Some(267)); // black (upper boundary)
        assert_eq!(get_achromatic_color_number(2.6), Some(266)); // dark gray
        assert_eq!(get_achromatic_color_number(4.5), Some(266)); // dark gray
        assert_eq!(get_achromatic_color_number(4.6), Some(265)); // medium gray
        assert_eq!(get_achromatic_color_number(6.5), Some(265)); // medium gray
        assert_eq!(get_achromatic_color_number(6.6), Some(264)); // light gray
        assert_eq!(get_achromatic_color_number(8.5), Some(264)); // light gray
        assert_eq!(get_achromatic_color_number(8.6), Some(263)); // white
        assert_eq!(get_achromatic_color_number(10.0), Some(263)); // white
        assert_eq!(get_achromatic_color_number(10.1), None); // out of range
    }

    #[test]
    fn test_achromatic_color_names() {
        assert_eq!(get_achromatic_color_name(1.0), Some("black"));
        assert_eq!(get_achromatic_color_name(3.0), Some("dark gray"));
        assert_eq!(get_achromatic_color_name(5.0), Some("medium gray"));
        assert_eq!(get_achromatic_color_name(7.0), Some("light gray"));
        assert_eq!(get_achromatic_color_name(9.0), Some("white"));
        assert_eq!(get_achromatic_color_name(-1.0), None);
        assert_eq!(get_achromatic_color_name(11.0), None);
    }

    #[test]
    fn test_achromatic_hue_recognition() {
        // Basic neutral notation
        assert!(is_achromatic_hue("N"));
        assert!(is_achromatic_hue("n"));
        assert!(is_achromatic_hue(" N "));

        // Numeric prefixes
        assert!(is_achromatic_hue("0N"));
        assert!(is_achromatic_hue("0.0N"));
        assert!(is_achromatic_hue("5.5N"));
        assert!(is_achromatic_hue("10N"));

        // Non-achromatic hues
        assert!(!is_achromatic_hue("R"));
        assert!(!is_achromatic_hue("5R"));
        assert!(!is_achromatic_hue("5.0R"));
        assert!(!is_achromatic_hue("YR"));
        assert!(!is_achromatic_hue(""));
        assert!(!is_achromatic_hue("5RN")); // N not at end
    }

    #[test]
    fn test_boundary_consistency() {
        // Verify boundaries don't overlap and cover the full 0-10 range
        let mut boundaries = ACHROMATIC_BOUNDARIES.to_vec();
        boundaries.sort_by(|a, b| a.0.partial_cmp(&b.0).unwrap());
        
        // Check first boundary starts at 0.0
        assert_eq!(boundaries[0].0, 0.0);
        
        // Check last boundary ends at 10.0
        assert_eq!(boundaries.last().unwrap().1, 10.0);
        
        // Check boundaries are contiguous
        for i in 1..boundaries.len() {
            assert_eq!(boundaries[i-1].1, boundaries[i].0, 
                "Gap between boundaries {} and {}", i-1, i);
        }
    }

    #[test]
    fn test_all_color_numbers_unique() {
        let mut color_numbers: Vec<u16> = ACHROMATIC_BOUNDARIES.iter().map(|(_, _, num, _)| *num).collect();
        color_numbers.sort();
        color_numbers.dedup();
        
        assert_eq!(color_numbers.len(), ACHROMATIC_BOUNDARIES.len(), 
            "Duplicate color numbers found in achromatic boundaries");
    }
}