//! Color descriptor containing complete naming information
//!
//! The `ColorDescriptor` provides unified access to all color naming systems:
//! - ISCC-NBS standard names (267 categories)
//! - Extended ISCC-NBS names (more recognizable alternatives)
//! - Semantic overlay names (Centore 2020)

use super::modifier::ColorModifier;

/// Complete color naming information for any color point.
///
/// This struct provides unified access to all color naming systems,
/// with the same modifier applying across all systems.
///
/// # Example
///
/// ```rust
/// use munsellspace::color_names::{ColorDescriptor, ColorModifier};
///
/// // ColorDescriptor is typically obtained from ColorClassifier
/// // This shows the structure:
/// let desc = ColorDescriptor {
///     iscc_nbs_number: 15,
///     modifier: ColorModifier::Moderate,
///     standard_name: "red".to_string(),
///     extended_name: "red".to_string(),
///     semantic_name: Some("rust".to_string()),
///     semantic_alternates: vec![],
///     nearest_semantic: Some(("rust".to_string(), 0.5)),
///     shade: "red".to_string(),
/// };
///
/// assert_eq!(desc.standard_descriptor(), "moderate red");
/// assert_eq!(desc.semantic_descriptor(), Some("moderate rust".to_string()));
/// ```
#[derive(Debug, Clone)]
pub struct ColorDescriptor {
    // ─── Core identification ───
    /// ISCC-NBS category number (1-267)
    pub iscc_nbs_number: u16,

    // ─── Modifier (shared across ALL naming systems) ───
    /// The color modifier (e.g., Vivid, Pale, Dark)
    pub modifier: ColorModifier,

    // ─── Standard ISCC-NBS ───
    /// Standard ISCC-NBS color name (e.g., "red", "yellowish pink")
    pub standard_name: String,

    // ─── Extended/Alt Name ───
    /// Extended/alternate color name (e.g., "lime" for "yellow green")
    pub extended_name: String,

    // ─── Semantic (Centore 2020) ───
    /// Primary semantic match, if the color is inside a semantic polyhedron
    pub semantic_name: Option<String>,

    /// Additional semantic matches (for colors in overlapping regions)
    pub semantic_alternates: Vec<String>,

    /// Nearest semantic overlay and distance (always computed)
    /// Useful for colors outside all semantic polyhedra
    pub nearest_semantic: Option<(String, f64)>,

    // ─── Shade category ───
    /// Color shade category (e.g., "red", "brown", "pink")
    pub shade: String,
}

impl ColorDescriptor {
    /// Returns the standard ISCC-NBS descriptor.
    ///
    /// Combines the modifier with the standard name.
    ///
    /// # Example
    ///
    /// ```rust
    /// use munsellspace::color_names::{ColorDescriptor, ColorModifier};
    ///
    /// let desc = ColorDescriptor {
    ///     iscc_nbs_number: 11,
    ///     modifier: ColorModifier::Vivid,
    ///     standard_name: "red".to_string(),
    ///     extended_name: "red".to_string(),
    ///     semantic_name: None,
    ///     semantic_alternates: vec![],
    ///     nearest_semantic: None,
    ///     shade: "red".to_string(),
    /// };
    ///
    /// assert_eq!(desc.standard_descriptor(), "vivid red");
    /// ```
    pub fn standard_descriptor(&self) -> String {
        self.modifier.format(&self.standard_name)
    }

    /// Returns the extended/alternate descriptor.
    ///
    /// Combines the modifier with the extended name.
    /// For most colors, this equals the standard descriptor.
    ///
    /// # Example
    ///
    /// ```rust
    /// use munsellspace::color_names::{ColorDescriptor, ColorModifier};
    ///
    /// let desc = ColorDescriptor {
    ///     iscc_nbs_number: 115,
    ///     modifier: ColorModifier::Vivid,
    ///     standard_name: "yellow green".to_string(),
    ///     extended_name: "lime".to_string(),
    ///     semantic_name: None,
    ///     semantic_alternates: vec![],
    ///     nearest_semantic: None,
    ///     shade: "lime".to_string(),
    /// };
    ///
    /// assert_eq!(desc.standard_descriptor(), "vivid yellow green");
    /// assert_eq!(desc.extended_descriptor(), "vivid lime");
    /// ```
    pub fn extended_descriptor(&self) -> String {
        self.modifier.format(&self.extended_name)
    }

    /// Returns the semantic descriptor if a semantic match exists.
    ///
    /// Combines the modifier with the semantic name.
    ///
    /// # Example
    ///
    /// ```rust
    /// use munsellspace::color_names::{ColorDescriptor, ColorModifier};
    ///
    /// let desc = ColorDescriptor {
    ///     iscc_nbs_number: 43,
    ///     modifier: ColorModifier::Moderate,
    ///     standard_name: "reddish brown".to_string(),
    ///     extended_name: "reddish brown".to_string(),
    ///     semantic_name: Some("rust".to_string()),
    ///     semantic_alternates: vec![],
    ///     nearest_semantic: Some(("rust".to_string(), 0.3)),
    ///     shade: "brown".to_string(),
    /// };
    ///
    /// assert_eq!(desc.semantic_descriptor(), Some("moderate rust".to_string()));
    /// ```
    pub fn semantic_descriptor(&self) -> Option<String> {
        self.semantic_name
            .as_ref()
            .map(|name| self.modifier.format(name))
    }

    /// Returns all semantic descriptors including alternates.
    ///
    /// Useful for colors that fall within multiple overlapping semantic regions.
    pub fn all_semantic_descriptors(&self) -> Vec<String> {
        let mut result = Vec::new();
        if let Some(ref name) = self.semantic_name {
            result.push(self.modifier.format(name));
        }
        for alt in &self.semantic_alternates {
            result.push(self.modifier.format(alt));
        }
        result
    }

    /// Returns true if this color has any semantic match.
    pub fn has_semantic_match(&self) -> bool {
        self.semantic_name.is_some()
    }

    /// Returns the nearest semantic descriptor with distance.
    ///
    /// Always available even for colors outside all semantic polyhedra.
    /// Useful for suggesting the closest semantic name.
    pub fn nearest_semantic_descriptor(&self) -> Option<(String, f64)> {
        self.nearest_semantic
            .as_ref()
            .map(|(name, dist)| (self.modifier.format(name), *dist))
    }

    /// Returns the number of semantic matches (primary + alternates).
    pub fn semantic_match_count(&self) -> usize {
        if self.semantic_name.is_some() {
            1 + self.semantic_alternates.len()
        } else {
            0
        }
    }

    /// Returns true if the extended name differs from the standard name.
    pub fn has_alternate_name(&self) -> bool {
        self.extended_name != self.standard_name
    }
}

impl std::fmt::Display for ColorDescriptor {
    /// Displays the standard ISCC-NBS descriptor.
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.standard_descriptor())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn sample_descriptor() -> ColorDescriptor {
        ColorDescriptor {
            iscc_nbs_number: 43,
            modifier: ColorModifier::Moderate,
            standard_name: "reddish brown".to_string(),
            extended_name: "reddish brown".to_string(),
            semantic_name: Some("rust".to_string()),
            semantic_alternates: vec!["brown".to_string()],
            nearest_semantic: Some(("rust".to_string(), 0.25)),
            shade: "brown".to_string(),
        }
    }

    #[test]
    fn test_standard_descriptor() {
        let desc = sample_descriptor();
        assert_eq!(desc.standard_descriptor(), "moderate reddish brown");
    }

    #[test]
    fn test_extended_descriptor_same() {
        let desc = sample_descriptor();
        assert_eq!(desc.extended_descriptor(), "moderate reddish brown");
    }

    #[test]
    fn test_extended_descriptor_different() {
        let mut desc = sample_descriptor();
        desc.standard_name = "yellow green".to_string();
        desc.extended_name = "lime".to_string();
        desc.modifier = ColorModifier::Vivid;

        assert_eq!(desc.standard_descriptor(), "vivid yellow green");
        assert_eq!(desc.extended_descriptor(), "vivid lime");
    }

    #[test]
    fn test_semantic_descriptor() {
        let desc = sample_descriptor();
        assert_eq!(desc.semantic_descriptor(), Some("moderate rust".to_string()));
    }

    #[test]
    fn test_semantic_descriptor_none() {
        let mut desc = sample_descriptor();
        desc.semantic_name = None;
        assert_eq!(desc.semantic_descriptor(), None);
    }

    #[test]
    fn test_all_semantic_descriptors() {
        let desc = sample_descriptor();
        let all = desc.all_semantic_descriptors();
        assert_eq!(all.len(), 2);
        assert_eq!(all[0], "moderate rust");
        assert_eq!(all[1], "moderate brown");
    }

    #[test]
    fn test_has_semantic_match() {
        let desc = sample_descriptor();
        assert!(desc.has_semantic_match());

        let mut no_semantic = sample_descriptor();
        no_semantic.semantic_name = None;
        assert!(!no_semantic.has_semantic_match());
    }

    #[test]
    fn test_nearest_semantic_descriptor() {
        let desc = sample_descriptor();
        let (name, dist) = desc.nearest_semantic_descriptor().unwrap();
        assert_eq!(name, "moderate rust");
        assert!((dist - 0.25).abs() < 0.001);
    }

    #[test]
    fn test_semantic_match_count() {
        let desc = sample_descriptor();
        assert_eq!(desc.semantic_match_count(), 2); // rust + brown

        let mut no_semantic = sample_descriptor();
        no_semantic.semantic_name = None;
        no_semantic.semantic_alternates.clear();
        assert_eq!(no_semantic.semantic_match_count(), 0);
    }

    #[test]
    fn test_has_alternate_name() {
        let desc = sample_descriptor();
        assert!(!desc.has_alternate_name()); // same name

        let mut with_alt = sample_descriptor();
        with_alt.extended_name = "rust".to_string();
        assert!(with_alt.has_alternate_name());
    }

    #[test]
    fn test_display() {
        let desc = sample_descriptor();
        assert_eq!(format!("{}", desc), "moderate reddish brown");
    }

    #[test]
    fn test_compound_modifier_in_descriptor() {
        let desc = ColorDescriptor {
            iscc_nbs_number: 22,
            modifier: ColorModifier::IshGray,
            standard_name: "red".to_string(),
            extended_name: "red".to_string(),
            semantic_name: None,
            semantic_alternates: vec![],
            nearest_semantic: None,
            shade: "gray".to_string(),
        };

        assert_eq!(desc.standard_descriptor(), "reddish gray");
    }

    #[test]
    fn test_no_modifier() {
        let desc = ColorDescriptor {
            iscc_nbs_number: 263,
            modifier: ColorModifier::None,
            standard_name: "white".to_string(),
            extended_name: "white".to_string(),
            semantic_name: Some("white".to_string()),
            semantic_alternates: vec![],
            nearest_semantic: Some(("white".to_string(), 0.0)),
            shade: "white".to_string(),
        };

        assert_eq!(desc.standard_descriptor(), "white");
        assert_eq!(desc.semantic_descriptor(), Some("white".to_string()));
    }
}
