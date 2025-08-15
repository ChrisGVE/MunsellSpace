//! Color -ish transformation constants for ISCC-NBS descriptor construction
//! 
//! This module contains the mapping from base color names to their "-ish" variants
//! used in ISCC-NBS color descriptor construction.

/// Static array mapping color names to their -ish variants
/// Used for constructing ISCC-NBS descriptors with proper color modifiers
pub const COLOR_TO_ISH_MAPPINGS: &[(&str, &str)] = &[
    ("brown", "brownish"),
    ("blue", "bluish"),
    ("red", "reddish"),
    ("green", "greenish"),
    ("yellow", "yellowish"),
    ("purple", "purplish"),
    ("pink", "pinkish"),
    ("orange", "orangish"),
    ("gray", "grayish"),
    ("grey", "greyish"),
    ("olive", "olive"),  // Special case - stays as "olive"
    ("white", "whitish"),
    ("black", "blackish"),
];

/// Get the -ish variant of a color name, or return the original if no mapping exists
pub fn get_color_ish(color_name: &str) -> &str {
    COLOR_TO_ISH_MAPPINGS
        .iter()
        .find(|(base, _)| *base == color_name)
        .map(|(_, ish)| *ish)
        .unwrap_or(color_name)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_basic_color_ish_mappings() {
        assert_eq!(get_color_ish("red"), "reddish");
        assert_eq!(get_color_ish("blue"), "bluish");
        assert_eq!(get_color_ish("green"), "greenish");
        assert_eq!(get_color_ish("yellow"), "yellowish");
        assert_eq!(get_color_ish("purple"), "purplish");
    }

    #[test]
    fn test_special_cases() {
        // olive stays as olive (special case)
        assert_eq!(get_color_ish("olive"), "olive");
        
        // Both gray and grey are supported
        assert_eq!(get_color_ish("gray"), "grayish");
        assert_eq!(get_color_ish("grey"), "greyish");
    }

    #[test]
    fn test_unknown_color() {
        // Unknown colors return themselves
        assert_eq!(get_color_ish("magenta"), "magenta");
        assert_eq!(get_color_ish("unknown"), "unknown");
    }

    #[test]
    fn test_all_mappings_present() {
        let expected_count = 13;
        assert_eq!(COLOR_TO_ISH_MAPPINGS.len(), expected_count);
        
        // Verify all expected colors are present
        let expected_colors = [
            "brown", "blue", "red", "green", "yellow", "purple", 
            "pink", "orange", "gray", "grey", "olive", "white", "black"
        ];
        
        for &color in &expected_colors {
            assert!(
                COLOR_TO_ISH_MAPPINGS.iter().any(|(base, _)| *base == color),
                "Color '{}' not found in mappings", color
            );
        }
    }
}