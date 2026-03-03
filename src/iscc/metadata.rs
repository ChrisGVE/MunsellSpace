//! Color metadata types for the ISCC-NBS system.

use crate::constants::get_color_ish;

/// Color metadata with on-the-fly descriptor construction.
///
/// This struct contains the raw data components for ISCC-NBS color descriptions
/// and provides methods to construct formatted descriptors dynamically.
///
/// # Examples
///
/// ```rust
/// use munsellspace::iscc::ColorMetadata;
///
/// # fn example() -> Result<(), Box<dyn std::error::Error>> {
/// // Color metadata would typically be loaded from internal data
/// let metadata = ColorMetadata {
///     iscc_nbs_color_name: "red".to_string(),
///     iscc_nbs_formatter: Some("vivid {0}".to_string()),
///     alt_color_name: "red".to_string(),
///     color_shade: "medium".to_string(),
/// };
///
/// // Generate formatted descriptor
/// let descriptor = metadata.iscc_nbs_descriptor();
/// println!("Descriptor: {}", descriptor); // "vivid red"
/// # Ok(())
/// # }
/// ```
#[derive(Debug, Clone)]
pub struct ColorMetadata {
    /// Base color name from ISCC-NBS data (e.g., "red", "blue", "yellow").
    ///
    /// This is the core color term that gets formatted with modifiers
    /// like "vivid", "dark", "light", etc.
    pub iscc_nbs_color_name: String,

    /// Formatter template with placeholders for dynamic descriptor construction.
    ///
    /// Contains templates like "vivid {0}", "light {1}", where:
    /// - `{0}` is replaced with the base color name
    /// - `{1}` is replaced with the "-ish" variant (e.g., "reddish")
    pub iscc_nbs_formatter: Option<String>,

    /// Alternative color name for variations in nomenclature.
    ///
    /// Provides alternative names for the same color concept,
    /// allowing for different naming conventions or regional preferences.
    pub alt_color_name: String,

    /// Color shade information describing lightness/darkness characteristics.
    ///
    /// Indicates the relative brightness category such as "light", "dark",
    /// "medium", or other shade descriptors.
    pub color_shade: String,
}

impl ColorMetadata {
    /// Construct the primary ISCC-NBS descriptor using the formatter and color name.
    ///
    /// Applies the formatter template to the primary color name, creating
    /// standardized ISCC-NBS color descriptions.
    ///
    /// # Returns
    /// Formatted color descriptor string (e.g., "vivid red", "light blue")
    ///
    /// # Examples
    /// ```rust
    /// use munsellspace::iscc::ColorMetadata;
    ///
    /// let metadata = ColorMetadata {
    ///     iscc_nbs_color_name: "red".to_string(),
    ///     iscc_nbs_formatter: Some("vivid {0}".to_string()),
    ///     alt_color_name: "red".to_string(),
    ///     color_shade: "bright".to_string(),
    /// };
    ///
    /// assert_eq!(metadata.iscc_nbs_descriptor(), "vivid red");
    /// ```
    pub fn iscc_nbs_descriptor(&self) -> String {
        if let Some(formatter) = &self.iscc_nbs_formatter {
            Self::construct_descriptor(formatter, &self.iscc_nbs_color_name)
        } else {
            self.iscc_nbs_color_name.clone()
        }
    }

    /// Construct the alternative color descriptor using the formatter and alternative name.
    ///
    /// Similar to [`iscc_nbs_descriptor`](Self::iscc_nbs_descriptor) but uses the
    /// alternative color name, providing variant naming options.
    ///
    /// # Returns
    /// Formatted alternative color descriptor string
    ///
    /// # Examples
    /// ```rust
    /// use munsellspace::iscc::ColorMetadata;
    ///
    /// let metadata = ColorMetadata {
    ///     iscc_nbs_color_name: "red".to_string(),
    ///     iscc_nbs_formatter: Some("deep {0}".to_string()),
    ///     alt_color_name: "crimson".to_string(),
    ///     color_shade: "dark".to_string(),
    /// };
    ///
    /// assert_eq!(metadata.alt_color_descriptor(), "deep crimson");
    /// ```
    pub fn alt_color_descriptor(&self) -> String {
        if let Some(formatter) = &self.iscc_nbs_formatter {
            Self::construct_descriptor(formatter, &self.alt_color_name)
        } else {
            self.alt_color_name.clone()
        }
    }

    /// Get the color shade information.
    ///
    /// Returns the shade descriptor indicating the relative lightness/darkness
    /// characteristics of the color.
    ///
    /// # Returns
    /// Reference to the shade descriptor string
    ///
    /// # Examples
    /// ```rust
    /// use munsellspace::iscc::ColorMetadata;
    ///
    /// let metadata = ColorMetadata {
    ///     iscc_nbs_color_name: "blue".to_string(),
    ///     iscc_nbs_formatter: None,
    ///     alt_color_name: "blue".to_string(),
    ///     color_shade: "light".to_string(),
    /// };
    ///
    /// assert_eq!(metadata.shade(), "light");
    /// ```
    pub fn shade(&self) -> &str {
        &self.color_shade
    }

    /// Static descriptor construction using formatter templates and color name lookup.
    ///
    /// This method processes formatter templates containing placeholders:
    /// - `{0}` is replaced with the provided color name
    /// - `{1}` is replaced with the "-ish" variant (e.g., "red" -> "reddish")
    ///
    /// # Arguments
    /// * `formatter` - Template string with `{0}` and/or `{1}` placeholders
    /// * `color_name` - Base color name to substitute into template
    ///
    /// # Returns
    /// Formatted descriptor with placeholders replaced
    ///
    /// # Examples
    /// ```rust
    /// use munsellspace::iscc::ColorMetadata;
    ///
    /// let result = ColorMetadata::construct_descriptor("vivid {0}", "red");
    /// assert_eq!(result, "vivid red");
    ///
    /// let result = ColorMetadata::construct_descriptor("light {1}", "blue");
    /// assert_eq!(result, "light bluish");
    /// ```
    pub fn construct_descriptor(formatter: &str, color_name: &str) -> String {
        let color_name_ish = get_color_ish(color_name);

        // Replace {0} with color_name and {1} with color_name_ish
        formatter
            .replace("{0}", color_name)
            .replace("{1}", color_name_ish)
    }
}
