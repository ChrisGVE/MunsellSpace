//! Color -ish transformation constants for ISCC-NBS descriptor construction
//!
//! This module contains the mapping from base color names to their "-ish" variants
//! used in ISCC-NBS color descriptor construction and semantic overlay naming.

/// Static array mapping basic color names to their -ish variants
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

/// Static array mapping semantic overlay names (Centore 2020) to their -ish variants.
/// These follow English language conventions for color adjectives.
///
/// Most overlay names don't have natural "-ish" forms in standard English,
/// so they typically stay unchanged or use a hyphenated form.
pub const OVERLAY_TO_ISH_MAPPINGS: &[(&str, &str)] = &[
    // Colors with natural -ish forms
    ("gold", "goldish"),
    ("peach", "peachy"),      // "peachy" is more natural than "peachish"
    ("rose", "rosy"),         // "rosy" is more natural than "roseish"
    ("rust", "rusty"),        // "rusty" is more natural than "rustish"
    ("violet", "violetish"),

    // Colors that stay unchanged (no natural -ish form in English)
    ("aqua", "aqua"),
    ("beige", "beige"),
    ("coral", "coral"),
    ("fuchsia", "fuchsia"),
    ("lavender", "lavender"),
    ("lilac", "lilac"),
    ("magenta", "magenta"),
    ("mauve", "mauve"),
    ("navy", "navy"),
    ("sand", "sandy"),        // "sandy" is more natural
    ("tan", "tannish"),
    ("taupe", "taupe"),
    ("teal", "teal"),
    ("turquoise", "turquoise"),
    ("wine", "wine"),
];

/// Get the -ish variant of a color name, or return the original if no mapping exists.
/// Checks both basic color mappings and semantic overlay mappings.
pub fn get_color_ish(color_name: &str) -> &str {
    // First check basic color mappings
    if let Some((_, ish)) = COLOR_TO_ISH_MAPPINGS
        .iter()
        .find(|(base, _)| *base == color_name)
    {
        return ish;
    }

    // Then check overlay mappings
    if let Some((_, ish)) = OVERLAY_TO_ISH_MAPPINGS
        .iter()
        .find(|(base, _)| base.eq_ignore_ascii_case(color_name))
    {
        return ish;
    }

    // Return original if no mapping found
    color_name
}

/// Get the -ish variant specifically for semantic overlay names.
/// Returns None if the color is not a known overlay name.
pub fn get_overlay_ish(overlay_name: &str) -> Option<&'static str> {
    OVERLAY_TO_ISH_MAPPINGS
        .iter()
        .find(|(base, _)| base.eq_ignore_ascii_case(overlay_name))
        .map(|(_, ish)| *ish)
}

/// Check if a color name is a semantic overlay name.
pub fn is_overlay_name(name: &str) -> bool {
    OVERLAY_TO_ISH_MAPPINGS
        .iter()
        .any(|(base, _)| base.eq_ignore_ascii_case(name))
}

/// Construct a color descriptor by combining a modifier template with a color name.
///
/// The template uses placeholders:
/// - `{0}` is replaced with the base color name
/// - `{1}` is replaced with the "-ish" variant
///
/// # Examples
/// ```
/// use munsellspace::constants::color_ish::construct_overlay_descriptor;
///
/// assert_eq!(construct_overlay_descriptor("light {0}", "beige"), "light beige");
/// assert_eq!(construct_overlay_descriptor("vivid {0}", "coral"), "vivid coral");
/// assert_eq!(construct_overlay_descriptor("{1} gray", "rose"), "rosy gray");
/// ```
pub fn construct_overlay_descriptor(template: &str, overlay_name: &str) -> String {
    let ish_form = get_color_ish(overlay_name);
    template
        .replace("{0}", overlay_name)
        .replace("{1}", ish_form)
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
        assert_eq!(get_color_ish("unknown"), "unknown");
        assert_eq!(get_color_ish("chartreuse"), "chartreuse");
    }

    #[test]
    fn test_all_basic_mappings_present() {
        let expected_count = 13;
        assert_eq!(COLOR_TO_ISH_MAPPINGS.len(), expected_count);

        // Verify all expected basic colors are present
        let expected_colors = [
            "brown", "blue", "red", "green", "yellow", "purple",
            "pink", "orange", "gray", "grey", "olive", "white", "black"
        ];

        for &color in &expected_colors {
            assert!(
                COLOR_TO_ISH_MAPPINGS.iter().any(|(base, _)| *base == color),
                "Color '{}' not found in basic mappings", color
            );
        }
    }

    // ========================================================================
    // Semantic Overlay -ish Tests
    // ========================================================================

    #[test]
    fn test_overlay_ish_mappings() {
        // Colors with natural -ish forms
        assert_eq!(get_color_ish("gold"), "goldish");
        assert_eq!(get_color_ish("peach"), "peachy");
        assert_eq!(get_color_ish("rose"), "rosy");
        assert_eq!(get_color_ish("rust"), "rusty");
        assert_eq!(get_color_ish("sand"), "sandy");
        assert_eq!(get_color_ish("tan"), "tannish");
    }

    #[test]
    fn test_overlay_names_stay_unchanged() {
        // Many overlay names don't have natural -ish forms
        assert_eq!(get_color_ish("beige"), "beige");
        assert_eq!(get_color_ish("aqua"), "aqua");
        assert_eq!(get_color_ish("coral"), "coral");
        assert_eq!(get_color_ish("fuchsia"), "fuchsia");
        assert_eq!(get_color_ish("lavender"), "lavender");
        assert_eq!(get_color_ish("magenta"), "magenta");
        assert_eq!(get_color_ish("navy"), "navy");
        assert_eq!(get_color_ish("teal"), "teal");
        assert_eq!(get_color_ish("wine"), "wine");
    }

    #[test]
    fn test_overlay_ish_case_insensitive() {
        assert_eq!(get_color_ish("BEIGE"), "beige");
        assert_eq!(get_color_ish("Coral"), "coral");
        assert_eq!(get_color_ish("ROSE"), "rosy");
    }

    #[test]
    fn test_get_overlay_ish() {
        assert_eq!(get_overlay_ish("beige"), Some("beige"));
        assert_eq!(get_overlay_ish("rose"), Some("rosy"));
        assert_eq!(get_overlay_ish("unknown"), None);
        assert_eq!(get_overlay_ish("red"), None); // basic color, not overlay
    }

    #[test]
    fn test_is_overlay_name() {
        assert!(is_overlay_name("beige"));
        assert!(is_overlay_name("CORAL"));
        assert!(is_overlay_name("navy"));
        assert!(!is_overlay_name("red")); // basic color
        assert!(!is_overlay_name("unknown"));
    }

    #[test]
    fn test_all_overlay_mappings_present() {
        let expected_overlays = [
            "aqua", "beige", "coral", "fuchsia", "gold",
            "lavender", "lilac", "magenta", "mauve", "navy",
            "peach", "rose", "rust", "sand", "tan",
            "taupe", "teal", "turquoise", "violet", "wine",
        ];

        assert_eq!(OVERLAY_TO_ISH_MAPPINGS.len(), expected_overlays.len(),
            "Expected {} overlay mappings, found {}",
            expected_overlays.len(), OVERLAY_TO_ISH_MAPPINGS.len());

        for &overlay in &expected_overlays {
            assert!(
                is_overlay_name(overlay),
                "Overlay '{}' not found in mappings", overlay
            );
        }
    }

    // ========================================================================
    // Descriptor Construction Tests
    // ========================================================================

    #[test]
    fn test_construct_overlay_descriptor_simple() {
        assert_eq!(construct_overlay_descriptor("light {0}", "beige"), "light beige");
        assert_eq!(construct_overlay_descriptor("dark {0}", "navy"), "dark navy");
        assert_eq!(construct_overlay_descriptor("vivid {0}", "coral"), "vivid coral");
        assert_eq!(construct_overlay_descriptor("pale {0}", "lavender"), "pale lavender");
    }

    #[test]
    fn test_construct_overlay_descriptor_with_ish() {
        // Test {1} placeholder for -ish form
        assert_eq!(construct_overlay_descriptor("{1} gray", "rose"), "rosy gray");
        assert_eq!(construct_overlay_descriptor("{1} brown", "rust"), "rusty brown");
        assert_eq!(construct_overlay_descriptor("light {1} gray", "peach"), "light peachy gray");
    }

    #[test]
    fn test_construct_overlay_descriptor_no_ish_form() {
        // Overlay names without natural -ish forms use themselves
        assert_eq!(construct_overlay_descriptor("{1} gray", "beige"), "beige gray");
        assert_eq!(construct_overlay_descriptor("{1} white", "aqua"), "aqua white");
    }

    #[test]
    fn test_construct_overlay_descriptor_both_placeholders() {
        assert_eq!(
            construct_overlay_descriptor("deep {1} {0}", "rose"),
            "deep rosy rose"
        );
    }

    #[test]
    fn test_construct_overlay_descriptor_no_placeholders() {
        assert_eq!(construct_overlay_descriptor("neutral", "beige"), "neutral");
    }
}