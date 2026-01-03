//! Color characterization types for separating objective facts from formatting preferences.
//!
//! This module provides a clean separation between:
//! - **Characterization**: Objective facts about a color (ISCC-NBS category, semantic matches)
//! - **Formatting**: User preferences for how to describe the color
//!
//! The ISCC-NBS modifier (e.g., "dark", "vivid", "pale") is ALWAYS applied regardless
//! of whether Standard or Extended base colors are selected.
//!
//! # Example
//!
//! ```rust
//! use munsellspace::color_names::{ColorClassifier, FormatOptions, BaseColorSet, OverlayMode};
//!
//! # fn main() -> Result<(), Box<dyn std::error::Error>> {
//! let classifier = ColorClassifier::new()?;
//! let char = classifier.characterize_srgb([0, 0, 128])?;
//!
//! // Different formatting options produce different descriptions
//! let standard = FormatOptions::new(BaseColorSet::Standard, OverlayMode::Ignore);
//! let with_overlay = FormatOptions::new(BaseColorSet::Extended, OverlayMode::Include);
//!
//! println!("Standard: {}", char.describe(&standard));      // "dark blue"
//! println!("With overlay: {}", char.describe(&with_overlay));  // "dark navy" (if navy available)
//! # Ok(())
//! # }
//! ```

use super::modifier::ColorModifier;
use crate::semantic_overlay::MunsellSpec;

// ═══════════════════════════════════════════════════════════════════════════════
// Formatting Options
// ═══════════════════════════════════════════════════════════════════════════════

/// Base color naming system to use.
///
/// Determines whether to use standard ISCC-NBS color names or the
/// extended alternate names. Modifiers are always applied.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Default)]
pub enum BaseColorSet {
    /// Use the 29 official ISCC-NBS base color names with modifiers.
    ///
    /// Output examples: "vivid red", "dark greenish blue", "pale yellow green"
    Standard,

    /// Use extended names: lime, teal, turquoise instead of compound forms.
    ///
    /// Output examples: "vivid red", "dark teal", "pale lime"
    #[default]
    Extended,
}

/// How to handle semantic overlay names (e.g., "navy", "coral", "rust").
///
/// Semantic overlays are the 30 color names from Centore (2020) that
/// represent commonly-used color terms beyond the basic ISCC-NBS set.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Default)]
pub enum OverlayMode {
    /// Ignore semantic overlays; always use ISCC-NBS base colors.
    ///
    /// A color near "navy" would still be called "dark blue".
    Ignore,

    /// Include the nearest semantic overlay when available.
    ///
    /// Uses the overlay with the closest centroid distance to the color point.
    /// Falls back to ISCC-NBS if no overlay data is available.
    #[default]
    Include,
}

/// User preferences for color description formatting.
///
/// Controls how [`ColorCharacterization::describe()`] generates the output string.
///
/// # Example
///
/// ```rust
/// use munsellspace::color_names::{FormatOptions, BaseColorSet, OverlayMode};
///
/// // Standard ISCC-NBS without overlays
/// let opts = FormatOptions::new(BaseColorSet::Standard, OverlayMode::Ignore);
///
/// // Extended with overlays (default)
/// let default_opts = FormatOptions::default();
/// ```
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct FormatOptions {
    /// Which base color naming system to use.
    pub base_colors: BaseColorSet,

    /// How to handle semantic overlay names.
    pub overlay_mode: OverlayMode,
}

impl FormatOptions {
    /// Create new format options with specified settings.
    pub fn new(base_colors: BaseColorSet, overlay_mode: OverlayMode) -> Self {
        Self {
            base_colors,
            overlay_mode,
        }
    }

    /// Standard ISCC-NBS base colors with modifiers, no overlays.
    ///
    /// Output: "vivid red", "dark blue", "pale green", etc.
    pub fn standard() -> Self {
        Self {
            base_colors: BaseColorSet::Standard,
            overlay_mode: OverlayMode::Ignore,
        }
    }

    /// Extended ISCC-NBS alternate names with modifiers, no overlays.
    ///
    /// Output: "vivid red", "dark navy", "pale lime", etc.
    pub fn extended() -> Self {
        Self {
            base_colors: BaseColorSet::Extended,
            overlay_mode: OverlayMode::Ignore,
        }
    }

    /// Standard base colors with modifiers and semantic overlays.
    ///
    /// Output: "dark navy", "vivid coral" (overlay when available), else "dark blue", "vivid red"
    pub fn standard_with_overlays() -> Self {
        Self {
            base_colors: BaseColorSet::Standard,
            overlay_mode: OverlayMode::Include,
        }
    }

    /// Extended alternate names with modifiers and semantic overlays.
    ///
    /// Output: "dark navy", "vivid coral" (overlay when available), else "dark sapphire", "vivid crimson"
    pub fn extended_with_overlays() -> Self {
        Self {
            base_colors: BaseColorSet::Extended,
            overlay_mode: OverlayMode::Include,
        }
    }
}

impl Default for FormatOptions {
    fn default() -> Self {
        Self {
            base_colors: BaseColorSet::Extended,
            overlay_mode: OverlayMode::Include,
        }
    }
}

// ═══════════════════════════════════════════════════════════════════════════════
// Color Characterization
// ═══════════════════════════════════════════════════════════════════════════════

/// Objective characterization of a color in Munsell space.
///
/// Contains all factual information about a color's classification across
/// multiple naming systems. The actual description string is generated
/// by [`describe()`](Self::describe) based on user preferences.
///
/// # Fields
///
/// - **ISCC-NBS data**: Category number (1-267), base color name, extended name, modifier
/// - **Semantic overlay data**: Matching overlays (sorted by centroid distance), nearest overlay
///
/// # Example
///
/// ```rust
/// use munsellspace::color_names::{ColorClassifier, FormatOptions, BaseColorSet, OverlayMode};
///
/// # fn main() -> Result<(), Box<dyn std::error::Error>> {
/// let classifier = ColorClassifier::new()?;
/// let char = classifier.characterize_srgb([0, 0, 128])?;
///
/// // Access raw characterization data
/// println!("ISCC-NBS #{}: {}", char.iscc_nbs_number, char.iscc_base_color);
/// println!("Modifier: {:?}", char.modifier);
/// println!("Semantic matches: {:?}", char.semantic_matches);
///
/// // Generate formatted description
/// let opts = FormatOptions::extended_with_overlays();
/// println!("Description: {}", char.describe(&opts));
/// # Ok(())
/// # }
/// ```
#[derive(Debug, Clone)]
pub struct ColorCharacterization {
    /// The Munsell specification (hue_number, value, chroma).
    pub munsell: MunsellSpec,

    // ─── ISCC-NBS Data ───

    /// ISCC-NBS category number (1-267).
    pub iscc_nbs_number: u16,

    /// Base color name from ISCC-NBS (one of 13: red, blue, green, etc.).
    pub iscc_base_color: String,

    /// Extended/alternate color name (e.g., "crimson" instead of "red").
    pub iscc_extended_name: String,

    /// Color modifier derived from ISCC-NBS classification.
    pub modifier: ColorModifier,

    // ─── Semantic Overlay Data ───

    /// All semantic overlays that contain this color (may be empty).
    ///
    /// Ordered by distance from centroid (closest first). The first element
    /// is used when `OverlayMode::Include` is selected.
    pub semantic_matches: Vec<String>,

    /// Nearest semantic overlay and distance, even if not matching.
    ///
    /// Always populated unless classification failed.
    pub nearest_semantic: Option<(String, f64)>,

    // ─── Shade Category ───

    /// Color shade category (e.g., "red", "brown", "pink").
    ///
    /// Groups similar colors into broader categories.
    pub shade: String,
}

impl ColorCharacterization {
    /// Generate a color description based on format options.
    ///
    /// The output string depends on:
    /// - `base_colors`: Whether to use Standard (29 ISCC-NBS names) or Extended (lime/teal/turquoise)
    /// - `overlay_mode`: Whether to include semantic overlay names
    ///
    /// The ISCC-NBS modifier (e.g., "dark", "vivid", "pale") is ALWAYS applied.
    ///
    /// # Examples
    ///
    /// For a dark greenish blue color with "teal" as nearest overlay:
    ///
    /// | BaseColorSet | OverlayMode | Output |
    /// |--------------|-------------|--------|
    /// | Standard | Ignore | "dark greenish blue" |
    /// | Extended | Ignore | "dark teal" |
    /// | Standard | Include | "dark teal" |
    /// | Extended | Include | "dark teal" |
    pub fn describe(&self, options: &FormatOptions) -> String {
        // 1. Determine the color name: overlay takes precedence when included
        let color_name = match options.overlay_mode {
            OverlayMode::Ignore => match options.base_colors {
                BaseColorSet::Standard => &self.iscc_base_color,
                BaseColorSet::Extended => &self.iscc_extended_name,
            },
            OverlayMode::Include => {
                // Use nearest overlay (first in sorted list), fall back to ISCC-NBS
                self.semantic_matches
                    .first()
                    .map(|s| s.as_str())
                    .or_else(|| self.nearest_semantic.as_ref().map(|(name, _)| name.as_str()))
                    .unwrap_or_else(|| match options.base_colors {
                        BaseColorSet::Standard => &self.iscc_base_color,
                        BaseColorSet::Extended => &self.iscc_extended_name,
                    })
            }
        };

        // 2. Always apply modifier
        self.modifier.format(color_name)
    }

    /// Get the base color name without any modifier.
    ///
    /// Returns the semantic overlay name if applicable per options,
    /// otherwise the ISCC-NBS name.
    pub fn base_color(&self, options: &FormatOptions) -> &str {
        match options.overlay_mode {
            OverlayMode::Ignore => match options.base_colors {
                BaseColorSet::Standard => &self.iscc_base_color,
                BaseColorSet::Extended => &self.iscc_extended_name,
            },
            OverlayMode::Include => self
                .semantic_matches
                .first()
                .map(|s| s.as_str())
                .or_else(|| self.nearest_semantic.as_ref().map(|(name, _)| name.as_str()))
                .unwrap_or_else(|| match options.base_colors {
                    BaseColorSet::Standard => &self.iscc_base_color,
                    BaseColorSet::Extended => &self.iscc_extended_name,
                }),
        }
    }

    /// Returns true if any semantic overlay contains this color.
    pub fn has_semantic_match(&self) -> bool {
        !self.semantic_matches.is_empty()
    }

    /// Returns the number of semantic overlays that contain this color.
    pub fn semantic_match_count(&self) -> usize {
        self.semantic_matches.len()
    }

    /// Convenience: describe with default options (Extended + Include overlays).
    pub fn to_string_default(&self) -> String {
        self.describe(&FormatOptions::default())
    }
}

impl std::fmt::Display for ColorCharacterization {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.to_string_default())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn make_test_characterization(
        base: &str,
        extended: &str,
        modifier: ColorModifier,
        semantic_matches: Vec<&str>,
        nearest: Option<(&str, f64)>,
    ) -> ColorCharacterization {
        ColorCharacterization {
            munsell: MunsellSpec::new(28.0, 3.0, 8.0), // A blue-ish hue
            iscc_nbs_number: 182,
            iscc_base_color: base.to_string(),
            iscc_extended_name: extended.to_string(),
            modifier,
            semantic_matches: semantic_matches.into_iter().map(String::from).collect(),
            nearest_semantic: nearest.map(|(n, d)| (n.to_string(), d)),
            shade: base.to_string(), // Use base as default shade for tests
        }
    }

    #[test]
    fn test_standard_ignore_overlay() {
        let char = make_test_characterization(
            "blue",
            "sapphire",
            ColorModifier::Dark,
            vec!["navy"],
            Some(("navy", 1.5)),
        );

        let opts = FormatOptions::new(BaseColorSet::Standard, OverlayMode::Ignore);
        assert_eq!(char.describe(&opts), "dark blue"); // Uses base, modifier applied
    }

    #[test]
    fn test_extended_ignore_overlay() {
        let char = make_test_characterization(
            "blue",
            "sapphire",
            ColorModifier::Dark,
            vec!["navy"],
            Some(("navy", 1.5)),
        );

        let opts = FormatOptions::new(BaseColorSet::Extended, OverlayMode::Ignore);
        assert_eq!(char.describe(&opts), "dark sapphire"); // Uses extended, modifier applied
    }

    #[test]
    fn test_standard_include_overlay() {
        let char = make_test_characterization(
            "blue",
            "sapphire",
            ColorModifier::Dark,
            vec!["navy"],
            Some(("navy", 1.5)),
        );

        let opts = FormatOptions::new(BaseColorSet::Standard, OverlayMode::Include);
        assert_eq!(char.describe(&opts), "dark navy"); // Uses overlay, modifier applied
    }

    #[test]
    fn test_extended_include_overlay() {
        let char = make_test_characterization(
            "blue",
            "sapphire",
            ColorModifier::Dark,
            vec!["navy"],
            Some(("navy", 1.5)),
        );

        let opts = FormatOptions::new(BaseColorSet::Extended, OverlayMode::Include);
        assert_eq!(char.describe(&opts), "dark navy"); // Uses overlay, modifier applied
    }

    #[test]
    fn test_include_falls_back_to_nearest() {
        let char = make_test_characterization(
            "blue",
            "sapphire",
            ColorModifier::Vivid,
            vec![], // No direct matches
            Some(("navy", 5.0)), // But we have nearest
        );

        let opts = FormatOptions::new(BaseColorSet::Extended, OverlayMode::Include);
        assert_eq!(char.describe(&opts), "vivid navy"); // Uses nearest overlay
    }

    #[test]
    fn test_include_falls_back_to_iscc_nbs() {
        let char = make_test_characterization(
            "blue",
            "sapphire",
            ColorModifier::Vivid,
            vec![],  // No direct matches
            None,    // No nearest either
        );

        let opts = FormatOptions::new(BaseColorSet::Extended, OverlayMode::Include);
        assert_eq!(char.describe(&opts), "vivid sapphire"); // Falls back to extended
    }

    #[test]
    fn test_format_options_presets() {
        // Use different base and extended names to show the difference
        let char = make_test_characterization(
            "blue",        // Standard: official ISCC-NBS name
            "sapphire",    // Extended: alternate name (example for test)
            ColorModifier::Dark,
            vec!["navy"],
            Some(("navy", 1.5)),
        );

        // Modifiers are always applied regardless of Standard vs Extended
        assert_eq!(char.describe(&FormatOptions::standard()), "dark blue");      // Uses base
        assert_eq!(char.describe(&FormatOptions::extended()), "dark sapphire");  // Uses extended
        assert_eq!(char.describe(&FormatOptions::standard_with_overlays()), "dark navy"); // Overlay wins
        assert_eq!(char.describe(&FormatOptions::extended_with_overlays()), "dark navy"); // Overlay wins
    }

    #[test]
    fn test_has_semantic_match() {
        let with_match = make_test_characterization(
            "blue", "blue", ColorModifier::Dark,
            vec!["navy"], Some(("navy", 1.5)),
        );
        assert!(with_match.has_semantic_match());
        assert_eq!(with_match.semantic_match_count(), 1);

        let without_match = make_test_characterization(
            "blue", "blue", ColorModifier::Vivid,
            vec![], Some(("navy", 5.0)),
        );
        assert!(!without_match.has_semantic_match());
        assert_eq!(without_match.semantic_match_count(), 0);
    }

    #[test]
    fn test_display_uses_default() {
        let char = make_test_characterization(
            "blue", "blue", ColorModifier::Dark,
            vec!["navy"], Some(("navy", 1.5)),
        );

        // Default is Extended + Include
        assert_eq!(format!("{}", char), "dark navy");
    }

    #[test]
    fn test_base_color_method() {
        let char = make_test_characterization(
            "blue", "sapphire", ColorModifier::Dark,
            vec!["navy"], Some(("navy", 1.5)),
        );

        assert_eq!(char.base_color(&FormatOptions::standard()), "blue");
        assert_eq!(char.base_color(&FormatOptions::extended()), "sapphire");
        assert_eq!(char.base_color(&FormatOptions::standard_with_overlays()), "navy");
        assert_eq!(char.base_color(&FormatOptions::extended_with_overlays()), "navy");
    }
}
