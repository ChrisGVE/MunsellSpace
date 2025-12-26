//! Color name registry with base and -ish forms
//!
//! This module contains the internal mapping from base color names to their
//! adjectival (-ish) variants used in ISCC-NBS descriptor construction.
//!
//! The -ish forms are internal implementation details; only base names are public.

/// Internal: color name entry with base and -ish forms
#[derive(Debug, Clone, PartialEq)]
pub(crate) struct ColorNameEntry {
    /// Base form: "red", "navy", "yellowish pink"
    pub base: &'static str,
    /// Adjectival (-ish) form: "reddish", "navyish", "yellowish pinkish"
    pub ish: &'static str,
}

impl ColorNameEntry {
    const fn new(base: &'static str, ish: &'static str) -> Self {
        Self { base, ish }
    }
}

/// Complete color name registry covering ISCC-NBS, extended, and semantic names.
///
/// To add a new color: append to this array.
pub(crate) const COLOR_NAMES: &[ColorNameEntry] = &[
    // ═══════════════════════════════════════════════════════════════════════════
    // ISCC-NBS Standard Base Colors (used with {1} compound modifiers)
    // ═══════════════════════════════════════════════════════════════════════════
    ColorNameEntry::new("red", "reddish"),
    ColorNameEntry::new("blue", "bluish"),
    ColorNameEntry::new("green", "greenish"),
    ColorNameEntry::new("yellow", "yellowish"),
    ColorNameEntry::new("brown", "brownish"),
    ColorNameEntry::new("purple", "purplish"),
    ColorNameEntry::new("pink", "pinkish"),
    ColorNameEntry::new("orange", "orangish"),
    ColorNameEntry::new("olive", "olive"),      // Exception: unchanged per ISCC-NBS
    ColorNameEntry::new("violet", "violetish"),
    ColorNameEntry::new("gray", "grayish"),
    ColorNameEntry::new("grey", "greyish"),     // British spelling variant
    ColorNameEntry::new("white", "whitish"),
    ColorNameEntry::new("black", "blackish"),

    // ═══════════════════════════════════════════════════════════════════════════
    // ISCC-NBS Compound Standard Names
    // ═══════════════════════════════════════════════════════════════════════════
    ColorNameEntry::new("yellowish pink", "yellowish pinkish"),
    ColorNameEntry::new("reddish orange", "reddish orangish"),
    ColorNameEntry::new("reddish brown", "reddish brownish"),
    ColorNameEntry::new("orange yellow", "orange yellowish"),
    ColorNameEntry::new("yellowish brown", "yellowish brownish"),
    ColorNameEntry::new("olive brown", "olive brownish"),
    ColorNameEntry::new("greenish yellow", "greenish yellowish"),
    ColorNameEntry::new("yellow green", "yellow greenish"),
    ColorNameEntry::new("olive green", "olive greenish"),
    ColorNameEntry::new("yellowish green", "yellowish greenish"),
    ColorNameEntry::new("bluish green", "bluish greenish"),
    ColorNameEntry::new("greenish blue", "greenish bluish"),
    ColorNameEntry::new("purplish blue", "purplish bluish"),
    ColorNameEntry::new("reddish purple", "reddish purplish"),
    ColorNameEntry::new("purplish pink", "purplish pinkish"),
    ColorNameEntry::new("purplish red", "purplish reddish"),

    // ═══════════════════════════════════════════════════════════════════════════
    // Extended/Alt Color Names (ISCC-NBS alternates)
    // ═══════════════════════════════════════════════════════════════════════════
    ColorNameEntry::new("chartreuse", "chartreusish"),
    ColorNameEntry::new("teal", "tealish"),
    ColorNameEntry::new("turquoise", "turquoisish"),

    // ═══════════════════════════════════════════════════════════════════════════
    // Semantic Overlay Names (Centore 2020) - non-basic only
    // Basic colors (blue, brown, gray, green, orange, pink, purple, red, white,
    // yellow) are already in the ISCC-NBS section above
    // ═══════════════════════════════════════════════════════════════════════════
    ColorNameEntry::new("aqua", "aquaish"),
    ColorNameEntry::new("beige", "beigeish"),
    ColorNameEntry::new("coral", "coralish"),
    ColorNameEntry::new("fuchsia", "fuchsiaish"),
    ColorNameEntry::new("gold", "goldish"),
    ColorNameEntry::new("lavender", "lavenderish"),
    ColorNameEntry::new("lilac", "lilacish"),
    ColorNameEntry::new("magenta", "magentaish"),
    ColorNameEntry::new("mauve", "mauvish"),
    ColorNameEntry::new("navy", "navyish"),
    ColorNameEntry::new("peach", "peachish"),
    ColorNameEntry::new("rose", "roseish"),
    ColorNameEntry::new("rust", "rustish"),
    ColorNameEntry::new("sand", "sandish"),
    ColorNameEntry::new("tan", "tannish"),
    ColorNameEntry::new("taupe", "taupish"),
    ColorNameEntry::new("wine", "winish"),
];

/// Internal: get the -ish form of a color name for formatting
pub(crate) fn get_ish_form(color_name: &str) -> &str {
    COLOR_NAMES
        .iter()
        .find(|e| e.base == color_name)
        .map(|e| e.ish)
        .unwrap_or(color_name)  // Fallback: return unchanged
}

/// Internal: get the base form from an -ish form (reverse lookup)
#[allow(dead_code)]
pub(crate) fn get_base_form(ish_name: &str) -> Option<&'static str> {
    COLOR_NAMES
        .iter()
        .find(|e| e.ish == ish_name)
        .map(|e| e.base)
}

// ═══════════════════════════════════════════════════════════════════════════════
// PUBLIC API - only base names exposed
// ═══════════════════════════════════════════════════════════════════════════════

/// Returns an iterator over all known base color names.
///
/// This includes ISCC-NBS standard names, extended/alternate names,
/// and semantic overlay names from Centore (2020).
///
/// # Example
///
/// ```rust
/// use munsellspace::color_names::known_color_names;
///
/// for name in known_color_names() {
///     println!("{}", name);
/// }
/// ```
pub fn known_color_names() -> impl Iterator<Item = &'static str> {
    COLOR_NAMES.iter().map(|e| e.base)
}

/// Check if a color name is in the registry.
///
/// # Example
///
/// ```rust
/// use munsellspace::color_names::is_known_color;
///
/// assert!(is_known_color("red"));
/// assert!(is_known_color("coral"));
/// assert!(!is_known_color("unknown"));
/// ```
pub fn is_known_color(name: &str) -> bool {
    COLOR_NAMES.iter().any(|e| e.base == name)
}

/// Returns the total number of known color names.
pub fn color_name_count() -> usize {
    COLOR_NAMES.len()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_basic_ish_mappings() {
        assert_eq!(get_ish_form("red"), "reddish");
        assert_eq!(get_ish_form("blue"), "bluish");
        assert_eq!(get_ish_form("green"), "greenish");
        assert_eq!(get_ish_form("yellow"), "yellowish");
        assert_eq!(get_ish_form("purple"), "purplish");
        assert_eq!(get_ish_form("pink"), "pinkish");
        assert_eq!(get_ish_form("brown"), "brownish");
    }

    #[test]
    fn test_olive_exception() {
        // Olive stays as "olive" per ISCC-NBS standard
        assert_eq!(get_ish_form("olive"), "olive");
    }

    #[test]
    fn test_gray_variants() {
        assert_eq!(get_ish_form("gray"), "grayish");
        assert_eq!(get_ish_form("grey"), "greyish");
    }

    #[test]
    fn test_semantic_colors() {
        assert_eq!(get_ish_form("coral"), "coralish");
        assert_eq!(get_ish_form("navy"), "navyish");
        assert_eq!(get_ish_form("rust"), "rustish");
        assert_eq!(get_ish_form("tan"), "tannish");
        assert_eq!(get_ish_form("mauve"), "mauvish");
    }

    #[test]
    fn test_compound_colors() {
        assert_eq!(get_ish_form("yellowish pink"), "yellowish pinkish");
        assert_eq!(get_ish_form("reddish brown"), "reddish brownish");
        assert_eq!(get_ish_form("bluish green"), "bluish greenish");
    }

    #[test]
    fn test_unknown_color_fallback() {
        // Unknown colors return themselves
        assert_eq!(get_ish_form("unknown"), "unknown");
        assert_eq!(get_ish_form("imaginary"), "imaginary");
    }

    #[test]
    fn test_reverse_lookup() {
        assert_eq!(get_base_form("reddish"), Some("red"));
        assert_eq!(get_base_form("bluish"), Some("blue"));
        assert_eq!(get_base_form("olive"), Some("olive"));
        assert_eq!(get_base_form("unknown"), None);
    }

    #[test]
    fn test_known_color_names() {
        let names: Vec<_> = known_color_names().collect();
        assert!(names.contains(&"red"));
        assert!(names.contains(&"coral"));
        assert!(names.contains(&"chartreuse"));
        assert!(names.contains(&"yellowish pink"));
    }

    #[test]
    fn test_is_known_color() {
        assert!(is_known_color("red"));
        assert!(is_known_color("coral"));
        assert!(is_known_color("olive"));
        assert!(!is_known_color("unknown"));
        assert!(!is_known_color(""));
    }

    #[test]
    fn test_color_count() {
        // 14 base + 16 compound + 3 extended + 17 semantic = 50
        assert!(color_name_count() >= 50);
    }

    #[test]
    fn test_no_duplicate_base_names() {
        let names: Vec<_> = known_color_names().collect();
        let unique: std::collections::HashSet<_> = names.iter().collect();
        assert_eq!(names.len(), unique.len(), "Duplicate base names found");
    }
}
