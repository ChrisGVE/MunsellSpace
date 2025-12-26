//! Color modifier enum for ISCC-NBS descriptor construction
//!
//! The modifier (e.g., "vivid", "pale", "dark grayish") applies uniformly
//! across all color naming systems: ISCC-NBS standard, extended, and semantic.

use super::registry::get_ish_form;

/// ISCC-NBS color modifier.
///
/// Modifiers describe the saturation, lightness, and character of a color.
/// The same modifier applies to all naming systems (standard ISCC-NBS,
/// extended/alt names, and Centore semantic overlays).
///
/// # Example
///
/// ```rust
/// use munsellspace::color_names::ColorModifier;
///
/// let modifier = ColorModifier::Vivid;
/// assert_eq!(modifier.format("red"), "vivid red");
/// assert_eq!(modifier.format("coral"), "vivid coral");
/// ```
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum ColorModifier {
    // ─── High saturation ───
    /// Vivid: maximum saturation
    Vivid,
    /// Brilliant: high saturation with high lightness
    Brilliant,
    /// Strong: high saturation
    Strong,
    /// Deep: high saturation with low lightness
    Deep,
    /// Very deep: maximum saturation with very low lightness
    VeryDeep,

    // ─── Medium ───
    /// Light: medium saturation with high lightness
    Light,
    /// Moderate: medium saturation
    Moderate,
    /// Medium: synonym for moderate (rare usage)
    Medium,
    /// Dark: medium saturation with low lightness
    Dark,
    /// Very dark: medium saturation with very low lightness
    VeryDark,
    /// Very light: medium saturation with very high lightness
    VeryLight,

    // ─── Low saturation ───
    /// Pale: low saturation with high lightness
    Pale,
    /// Very pale: very low saturation with high lightness
    VeryPale,
    /// Grayish: low saturation
    Grayish,
    /// Dark grayish: low saturation with low lightness
    DarkGrayish,
    /// Blackish: very low saturation approaching black
    Blackish,
    /// Brownish: modified toward brown
    Brownish,

    // ─── Compound modifiers (use -ish form of base color) ───
    /// {color}ish white: e.g., "pinkish white", "yellowish white"
    IshWhite,
    /// {color}ish gray: e.g., "reddish gray", "bluish gray"
    IshGray,
    /// {color}ish black: e.g., "reddish black", "purplish black"
    IshBlack,
    /// Light {color}ish gray: e.g., "light brownish gray"
    LightIshGray,
    /// Dark {color}ish gray: e.g., "dark reddish gray"
    DarkIshGray,

    // ─── No modifier ───
    /// No modifier (for pure white, black, gray)
    None,
}

impl ColorModifier {
    /// Parse a ColorModifier from an ISCC-NBS formatter string.
    ///
    /// The formatter string comes from the ISCC-NBS data and contains
    /// placeholders like `{0}` (base name) and `{1}` (-ish form).
    ///
    /// # Example
    ///
    /// ```rust
    /// use munsellspace::color_names::ColorModifier;
    ///
    /// assert_eq!(ColorModifier::from_formatter("vivid {0}"), ColorModifier::Vivid);
    /// assert_eq!(ColorModifier::from_formatter("{1} gray"), ColorModifier::IshGray);
    /// ```
    pub fn from_formatter(formatter: &str) -> Self {
        match formatter {
            // High saturation
            "vivid {0}" => Self::Vivid,
            "brilliant {0}" => Self::Brilliant,
            "strong {0}" => Self::Strong,
            "deep {0}" => Self::Deep,
            "very deep {0}" => Self::VeryDeep,

            // Medium
            "light {0}" => Self::Light,
            "moderate {0}" => Self::Moderate,
            "medium {0}" => Self::Medium,
            "dark {0}" => Self::Dark,
            "very dark {0}" => Self::VeryDark,
            "very light {0}" => Self::VeryLight,

            // Low saturation
            "pale {0}" => Self::Pale,
            "very pale {0}" => Self::VeryPale,
            "grayish {0}" => Self::Grayish,
            "dark grayish {0}" => Self::DarkGrayish,
            "blackish {0}" => Self::Blackish,
            "brownish {0}" => Self::Brownish,

            // Compound (use -ish form)
            "{1} white" => Self::IshWhite,
            "{1} gray" => Self::IshGray,
            "{1} black" => Self::IshBlack,
            "light {1} gray" => Self::LightIshGray,
            "dark {1} gray" => Self::DarkIshGray,

            // No modifier or unrecognized
            "{0}" | "" => Self::None,
            _ => Self::None,
        }
    }

    /// Format a color name with this modifier.
    ///
    /// For simple modifiers, prepends the modifier to the color name.
    /// For compound modifiers (IshWhite, IshGray, etc.), uses the -ish
    /// form of the color name from the internal registry.
    ///
    /// # Example
    ///
    /// ```rust
    /// use munsellspace::color_names::ColorModifier;
    ///
    /// assert_eq!(ColorModifier::Vivid.format("red"), "vivid red");
    /// assert_eq!(ColorModifier::DarkGrayish.format("blue"), "dark grayish blue");
    /// assert_eq!(ColorModifier::IshGray.format("red"), "reddish gray");
    /// assert_eq!(ColorModifier::LightIshGray.format("brown"), "light brownish gray");
    /// assert_eq!(ColorModifier::None.format("white"), "white");
    /// ```
    pub fn format(&self, color_name: &str) -> String {
        match self {
            // High saturation
            Self::Vivid => format!("vivid {}", color_name),
            Self::Brilliant => format!("brilliant {}", color_name),
            Self::Strong => format!("strong {}", color_name),
            Self::Deep => format!("deep {}", color_name),
            Self::VeryDeep => format!("very deep {}", color_name),

            // Medium
            Self::Light => format!("light {}", color_name),
            Self::Moderate => format!("moderate {}", color_name),
            Self::Medium => format!("medium {}", color_name),
            Self::Dark => format!("dark {}", color_name),
            Self::VeryDark => format!("very dark {}", color_name),
            Self::VeryLight => format!("very light {}", color_name),

            // Low saturation
            Self::Pale => format!("pale {}", color_name),
            Self::VeryPale => format!("very pale {}", color_name),
            Self::Grayish => format!("grayish {}", color_name),
            Self::DarkGrayish => format!("dark grayish {}", color_name),
            Self::Blackish => format!("blackish {}", color_name),
            Self::Brownish => format!("brownish {}", color_name),

            // Compound (use -ish form)
            Self::IshWhite => format!("{} white", get_ish_form(color_name)),
            Self::IshGray => format!("{} gray", get_ish_form(color_name)),
            Self::IshBlack => format!("{} black", get_ish_form(color_name)),
            Self::LightIshGray => format!("light {} gray", get_ish_form(color_name)),
            Self::DarkIshGray => format!("dark {} gray", get_ish_form(color_name)),

            // No modifier
            Self::None => color_name.to_string(),
        }
    }

    /// Returns the modifier as a standalone string (without color name).
    ///
    /// For compound modifiers, returns a placeholder form.
    ///
    /// # Example
    ///
    /// ```rust
    /// use munsellspace::color_names::ColorModifier;
    ///
    /// assert_eq!(ColorModifier::Vivid.as_str(), "vivid");
    /// assert_eq!(ColorModifier::DarkGrayish.as_str(), "dark grayish");
    /// assert_eq!(ColorModifier::None.as_str(), "");
    /// ```
    pub fn as_str(&self) -> &'static str {
        match self {
            Self::Vivid => "vivid",
            Self::Brilliant => "brilliant",
            Self::Strong => "strong",
            Self::Deep => "deep",
            Self::VeryDeep => "very deep",
            Self::Light => "light",
            Self::Moderate => "moderate",
            Self::Medium => "medium",
            Self::Dark => "dark",
            Self::VeryDark => "very dark",
            Self::VeryLight => "very light",
            Self::Pale => "pale",
            Self::VeryPale => "very pale",
            Self::Grayish => "grayish",
            Self::DarkGrayish => "dark grayish",
            Self::Blackish => "blackish",
            Self::Brownish => "brownish",
            Self::IshWhite => "-ish white",
            Self::IshGray => "-ish gray",
            Self::IshBlack => "-ish black",
            Self::LightIshGray => "light -ish gray",
            Self::DarkIshGray => "dark -ish gray",
            Self::None => "",
        }
    }

    /// Returns true if this is a compound modifier that uses the -ish form.
    pub fn is_compound(&self) -> bool {
        matches!(
            self,
            Self::IshWhite | Self::IshGray | Self::IshBlack | Self::LightIshGray | Self::DarkIshGray
        )
    }

    /// Returns true if this modifier indicates high saturation.
    pub fn is_vivid(&self) -> bool {
        matches!(
            self,
            Self::Vivid | Self::Brilliant | Self::Strong | Self::Deep | Self::VeryDeep
        )
    }

    /// Returns true if this modifier indicates low saturation (grayish tones).
    pub fn is_grayish(&self) -> bool {
        matches!(
            self,
            Self::Grayish
                | Self::DarkGrayish
                | Self::IshGray
                | Self::LightIshGray
                | Self::DarkIshGray
        )
    }
}

impl Default for ColorModifier {
    fn default() -> Self {
        Self::None
    }
}

impl std::fmt::Display for ColorModifier {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.as_str())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_simple_modifiers() {
        assert_eq!(ColorModifier::Vivid.format("red"), "vivid red");
        assert_eq!(ColorModifier::Brilliant.format("orange"), "brilliant orange");
        assert_eq!(ColorModifier::Strong.format("blue"), "strong blue");
        assert_eq!(ColorModifier::Deep.format("purple"), "deep purple");
        assert_eq!(ColorModifier::Light.format("green"), "light green");
        assert_eq!(ColorModifier::Moderate.format("pink"), "moderate pink");
        assert_eq!(ColorModifier::Dark.format("brown"), "dark brown");
        assert_eq!(ColorModifier::Pale.format("yellow"), "pale yellow");
        assert_eq!(ColorModifier::Grayish.format("olive"), "grayish olive");
    }

    #[test]
    fn test_compound_modifiers_with_ish() {
        assert_eq!(ColorModifier::IshGray.format("red"), "reddish gray");
        assert_eq!(ColorModifier::IshGray.format("blue"), "bluish gray");
        assert_eq!(ColorModifier::IshBlack.format("purple"), "purplish black");
        assert_eq!(ColorModifier::IshWhite.format("pink"), "pinkish white");
        assert_eq!(ColorModifier::IshWhite.format("yellow"), "yellowish white");
    }

    #[test]
    fn test_light_dark_ish_gray() {
        assert_eq!(
            ColorModifier::LightIshGray.format("brown"),
            "light brownish gray"
        );
        assert_eq!(
            ColorModifier::DarkIshGray.format("red"),
            "dark reddish gray"
        );
        assert_eq!(
            ColorModifier::LightIshGray.format("olive"),
            "light olive gray"
        );
    }

    #[test]
    fn test_olive_exception() {
        // Olive stays as "olive" not "olivish"
        assert_eq!(ColorModifier::IshGray.format("olive"), "olive gray");
    }

    #[test]
    fn test_none_modifier() {
        assert_eq!(ColorModifier::None.format("white"), "white");
        assert_eq!(ColorModifier::None.format("black"), "black");
        assert_eq!(ColorModifier::None.format("gray"), "gray");
    }

    #[test]
    fn test_from_formatter() {
        assert_eq!(ColorModifier::from_formatter("vivid {0}"), ColorModifier::Vivid);
        assert_eq!(ColorModifier::from_formatter("brilliant {0}"), ColorModifier::Brilliant);
        assert_eq!(ColorModifier::from_formatter("strong {0}"), ColorModifier::Strong);
        assert_eq!(ColorModifier::from_formatter("deep {0}"), ColorModifier::Deep);
        assert_eq!(ColorModifier::from_formatter("very deep {0}"), ColorModifier::VeryDeep);
        assert_eq!(ColorModifier::from_formatter("light {0}"), ColorModifier::Light);
        assert_eq!(ColorModifier::from_formatter("moderate {0}"), ColorModifier::Moderate);
        assert_eq!(ColorModifier::from_formatter("dark {0}"), ColorModifier::Dark);
        assert_eq!(ColorModifier::from_formatter("very dark {0}"), ColorModifier::VeryDark);
        assert_eq!(ColorModifier::from_formatter("pale {0}"), ColorModifier::Pale);
        assert_eq!(ColorModifier::from_formatter("grayish {0}"), ColorModifier::Grayish);
        assert_eq!(ColorModifier::from_formatter("dark grayish {0}"), ColorModifier::DarkGrayish);
        assert_eq!(ColorModifier::from_formatter("{1} gray"), ColorModifier::IshGray);
        assert_eq!(ColorModifier::from_formatter("{1} black"), ColorModifier::IshBlack);
        assert_eq!(ColorModifier::from_formatter("{1} white"), ColorModifier::IshWhite);
        assert_eq!(ColorModifier::from_formatter("light {1} gray"), ColorModifier::LightIshGray);
        assert_eq!(ColorModifier::from_formatter("dark {1} gray"), ColorModifier::DarkIshGray);
        assert_eq!(ColorModifier::from_formatter("{0}"), ColorModifier::None);
        assert_eq!(ColorModifier::from_formatter(""), ColorModifier::None);
    }

    #[test]
    fn test_as_str() {
        assert_eq!(ColorModifier::Vivid.as_str(), "vivid");
        assert_eq!(ColorModifier::DarkGrayish.as_str(), "dark grayish");
        assert_eq!(ColorModifier::None.as_str(), "");
    }

    #[test]
    fn test_is_compound() {
        assert!(ColorModifier::IshGray.is_compound());
        assert!(ColorModifier::IshBlack.is_compound());
        assert!(ColorModifier::IshWhite.is_compound());
        assert!(ColorModifier::LightIshGray.is_compound());
        assert!(ColorModifier::DarkIshGray.is_compound());
        assert!(!ColorModifier::Vivid.is_compound());
        assert!(!ColorModifier::Dark.is_compound());
    }

    #[test]
    fn test_is_vivid() {
        assert!(ColorModifier::Vivid.is_vivid());
        assert!(ColorModifier::Brilliant.is_vivid());
        assert!(ColorModifier::Strong.is_vivid());
        assert!(!ColorModifier::Pale.is_vivid());
        assert!(!ColorModifier::Grayish.is_vivid());
    }

    #[test]
    fn test_is_grayish() {
        assert!(ColorModifier::Grayish.is_grayish());
        assert!(ColorModifier::DarkGrayish.is_grayish());
        assert!(ColorModifier::IshGray.is_grayish());
        assert!(!ColorModifier::Vivid.is_grayish());
        assert!(!ColorModifier::Pale.is_grayish());
    }

    #[test]
    fn test_semantic_colors_with_modifiers() {
        // Semantic overlay names should work with all modifiers
        assert_eq!(ColorModifier::Vivid.format("coral"), "vivid coral");
        assert_eq!(ColorModifier::Moderate.format("rust"), "moderate rust");
        assert_eq!(ColorModifier::Pale.format("lavender"), "pale lavender");
        assert_eq!(ColorModifier::Deep.format("navy"), "deep navy");
        assert_eq!(ColorModifier::Light.format("peach"), "light peach");
    }

    #[test]
    fn test_display() {
        assert_eq!(format!("{}", ColorModifier::Vivid), "vivid");
        assert_eq!(format!("{}", ColorModifier::None), "");
    }
}
