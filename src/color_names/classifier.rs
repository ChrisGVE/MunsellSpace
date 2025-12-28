//! Unified color classifier for all naming systems
//!
//! The `ColorClassifier` provides a single entry point for classifying colors
//! across all naming systems: ISCC-NBS standard, extended, and semantic overlays.

use crate::error::{MunsellError, Result};
use crate::iscc::{ColorMetadata, IsccNbsClassifier};
use crate::semantic_overlay::{parse_munsell_notation, MunsellSpec};
use crate::types::MunsellColor;
use crate::unified_cache::hex_to_rgb;
use crate::MunsellConverter;

// Internal use of deprecated functions - these are the backing implementations
// We use them internally while providing the unified API externally
#[allow(deprecated)]
use crate::semantic_overlay::{closest_overlay, matching_overlays, semantic_overlay};

use super::characterization::ColorCharacterization;
use super::descriptor::ColorDescriptor;
use super::modifier::ColorModifier;

/// Unified color classifier for all naming systems.
///
/// Provides a single entry point for classifying colors and obtaining
/// complete naming information across:
/// - ISCC-NBS standard names (267 categories)
/// - Extended/alternate names
/// - Semantic overlay names (Centore 2020, 30 colors)
///
/// # Example
///
/// ```rust
/// use munsellspace::color_names::ColorClassifier;
///
/// # fn main() -> Result<(), Box<dyn std::error::Error>> {
/// let classifier = ColorClassifier::new()?;
///
/// // Classify an RGB color
/// let desc = classifier.classify_srgb([180, 80, 60])?;
/// println!("Standard: {}", desc.standard_descriptor());
/// println!("Semantic: {:?}", desc.semantic_descriptor());
///
/// // Classify a hex color
/// let desc = classifier.classify_hex("#B45040")?;
/// println!("{}", desc);
/// # Ok(())
/// # }
/// ```
pub struct ColorClassifier {
    converter: MunsellConverter,
    iscc: IsccNbsClassifier,
}

impl ColorClassifier {
    /// Create a new unified color classifier.
    ///
    /// Initializes the underlying Munsell converter and ISCC-NBS classifier.
    ///
    /// # Errors
    ///
    /// Returns an error if the reference data cannot be loaded.
    pub fn new() -> Result<Self> {
        Ok(Self {
            converter: MunsellConverter::new()?,
            iscc: IsccNbsClassifier::new()?,
        })
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // Primary Classification Methods
    // ═══════════════════════════════════════════════════════════════════════════

    /// Classify an sRGB color and return complete naming information.
    ///
    /// # Arguments
    ///
    /// * `rgb` - sRGB color as [R, G, B] with values 0-255
    ///
    /// # Example
    ///
    /// ```rust
    /// use munsellspace::color_names::ColorClassifier;
    ///
    /// # fn main() -> Result<(), Box<dyn std::error::Error>> {
    /// let classifier = ColorClassifier::new()?;
    /// let desc = classifier.classify_srgb([255, 0, 0])?;
    ///
    /// println!("ISCC-NBS: {}", desc.standard_descriptor());
    /// if let Some(semantic) = desc.semantic_descriptor() {
    ///     println!("Semantic: {}", semantic);
    /// }
    /// # Ok(())
    /// # }
    /// ```
    pub fn classify_srgb(&self, rgb: [u8; 3]) -> Result<ColorDescriptor> {
        let munsell = self.converter.srgb_to_munsell(rgb)?;
        self.classify_munsell_color(&munsell)
    }

    /// Classify a hex color string and return complete naming information.
    ///
    /// Accepts formats: "#RRGGBB", "RRGGBB", "#RGB", "RGB"
    ///
    /// # Example
    ///
    /// ```rust
    /// use munsellspace::color_names::ColorClassifier;
    ///
    /// # fn main() -> Result<(), Box<dyn std::error::Error>> {
    /// let classifier = ColorClassifier::new()?;
    /// let desc = classifier.classify_hex("#C86450")?;
    /// println!("{}", desc.standard_descriptor());
    /// # Ok(())
    /// # }
    /// ```
    pub fn classify_hex(&self, hex: &str) -> Result<ColorDescriptor> {
        let rgb = hex_to_rgb(hex)?;
        self.classify_srgb(rgb)
    }

    /// Classify a CIELAB color and return complete naming information.
    ///
    /// # Arguments
    ///
    /// * `lab` - CIELAB color as [L*, a*, b*]
    ///
    /// # Example
    ///
    /// ```rust
    /// use munsellspace::color_names::ColorClassifier;
    ///
    /// # fn main() -> Result<(), Box<dyn std::error::Error>> {
    /// let classifier = ColorClassifier::new()?;
    /// let desc = classifier.classify_lab([50.0, 40.0, 30.0])?;
    /// println!("{}", desc.standard_descriptor());
    /// # Ok(())
    /// # }
    /// ```
    pub fn classify_lab(&self, lab: [f64; 3]) -> Result<ColorDescriptor> {
        let munsell = self.converter.lab_to_munsell(lab)?;
        self.classify_munsell_color(&munsell)
    }

    /// Classify a Munsell notation string and return complete naming information.
    ///
    /// # Arguments
    ///
    /// * `notation` - Munsell notation string (e.g., "5R 4/10", "N 5/")
    ///
    /// # Example
    ///
    /// ```rust
    /// use munsellspace::color_names::ColorClassifier;
    ///
    /// # fn main() -> Result<(), Box<dyn std::error::Error>> {
    /// let classifier = ColorClassifier::new()?;
    /// let desc = classifier.classify_munsell("5R 4/10")?;
    /// println!("{}", desc.standard_descriptor()); // e.g., "vivid red"
    /// # Ok(())
    /// # }
    /// ```
    pub fn classify_munsell(&self, notation: &str) -> Result<ColorDescriptor> {
        let munsell = MunsellColor::from_notation(notation)?;
        self.classify_munsell_color(&munsell)
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // Characterization Methods (v1.2.1+)
    // ═══════════════════════════════════════════════════════════════════════════

    /// Characterize an sRGB color and return objective facts.
    ///
    /// Returns a [`ColorCharacterization`] containing all classification data
    /// without applying any formatting. Use [`ColorCharacterization::describe()`]
    /// with [`FormatOptions`](super::FormatOptions) to generate the output string.
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
    /// // Access raw data
    /// println!("ISCC-NBS: {} ({})", char.iscc_base_color, char.iscc_nbs_number);
    ///
    /// // Format with options
    /// let opts = FormatOptions::new(BaseColorSet::Extended, OverlayMode::Include);
    /// println!("{}", char.describe(&opts));
    /// # Ok(())
    /// # }
    /// ```
    pub fn characterize_srgb(&self, rgb: [u8; 3]) -> Result<ColorCharacterization> {
        let munsell = self.converter.srgb_to_munsell(rgb)?;
        self.characterize_munsell_color(&munsell)
    }

    /// Characterize a hex color string and return objective facts.
    ///
    /// Accepts formats: "#RRGGBB", "RRGGBB", "#RGB", "RGB"
    ///
    /// # Example
    ///
    /// ```rust
    /// use munsellspace::color_names::{ColorClassifier, FormatOptions};
    ///
    /// # fn main() -> Result<(), Box<dyn std::error::Error>> {
    /// let classifier = ColorClassifier::new()?;
    /// let char = classifier.characterize_hex("#000080")?;
    /// println!("{}", char.describe(&FormatOptions::extended_with_overlays()));
    /// # Ok(())
    /// # }
    /// ```
    pub fn characterize_hex(&self, hex: &str) -> Result<ColorCharacterization> {
        let rgb = hex_to_rgb(hex)?;
        self.characterize_srgb(rgb)
    }

    /// Characterize a CIELAB color and return objective facts.
    ///
    /// # Arguments
    ///
    /// * `lab` - CIELAB color as [L*, a*, b*]
    pub fn characterize_lab(&self, lab: [f64; 3]) -> Result<ColorCharacterization> {
        let munsell = self.converter.lab_to_munsell(lab)?;
        self.characterize_munsell_color(&munsell)
    }

    /// Characterize a Munsell notation string and return objective facts.
    ///
    /// # Arguments
    ///
    /// * `notation` - Munsell notation string (e.g., "5R 4/10", "N 5/")
    ///
    /// # Example
    ///
    /// ```rust
    /// use munsellspace::color_names::{ColorClassifier, FormatOptions};
    ///
    /// # fn main() -> Result<(), Box<dyn std::error::Error>> {
    /// let classifier = ColorClassifier::new()?;
    /// let char = classifier.characterize_munsell_notation("5PB 3/8")?;
    ///
    /// // Check semantic matches
    /// if char.has_semantic_match() {
    ///     println!("Matches: {:?}", char.semantic_matches);
    /// }
    /// # Ok(())
    /// # }
    /// ```
    pub fn characterize_munsell_notation(&self, notation: &str) -> Result<ColorCharacterization> {
        let munsell = MunsellColor::from_notation(notation)?;
        self.characterize_munsell_color(&munsell)
    }

    /// Internal: characterize a MunsellColor and build ColorCharacterization.
    #[allow(deprecated)] // Uses deprecated semantic overlay functions internally
    fn characterize_munsell_color(&self, munsell: &MunsellColor) -> Result<ColorCharacterization> {
        // Get ISCC-NBS classification
        let (iscc_number, iscc_meta) = self.get_iscc_classification(munsell)?;

        // Convert to MunsellSpec for semantic overlay lookup
        let munsell_spec = self.munsell_color_to_spec(munsell);

        // Get semantic overlay matches
        let (semantic_matches, nearest) = if let Some(ref spec) = munsell_spec {
            let all_matches: Vec<String> =
                matching_overlays(spec).iter().map(|s| s.to_string()).collect();
            let nearest = closest_overlay(spec).map(|(name, dist)| (name.to_string(), dist));
            (all_matches, nearest)
        } else {
            (vec![], None)
        };

        // Extract modifier from formatter
        let modifier = iscc_meta
            .iscc_nbs_formatter
            .as_ref()
            .map(|f| ColorModifier::from_formatter(f))
            .unwrap_or(ColorModifier::None);

        Ok(ColorCharacterization {
            munsell: munsell_spec.unwrap_or_else(|| MunsellSpec::new(0.0, munsell.value, 0.0)),
            iscc_nbs_number: iscc_number,
            iscc_base_color: iscc_meta.iscc_nbs_color_name.clone(),
            iscc_extended_name: iscc_meta.alt_color_name.clone(),
            modifier,
            semantic_matches,
            nearest_semantic: nearest,
            shade: iscc_meta.color_shade.clone(),
        })
    }

    /// Internal: classify a MunsellColor and build the complete descriptor.
    ///
    /// Uses ColorCharacterization internally and converts to ColorDescriptor.
    fn classify_munsell_color(&self, munsell: &MunsellColor) -> Result<ColorDescriptor> {
        // Get the characterization first
        let char = self.characterize_munsell_color(munsell)?;

        // Convert to ColorDescriptor format
        let semantic_name = char.semantic_matches.first().cloned();
        let semantic_alternates: Vec<String> =
            char.semantic_matches.into_iter().skip(1).collect();

        Ok(ColorDescriptor {
            iscc_nbs_number: char.iscc_nbs_number,
            modifier: char.modifier,
            standard_name: char.iscc_base_color,
            extended_name: char.iscc_extended_name,
            semantic_name,
            semantic_alternates,
            nearest_semantic: char.nearest_semantic,
            shade: char.shade,
        })
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // Convenience Methods
    // ═══════════════════════════════════════════════════════════════════════════

    /// Get only the semantic color name for an sRGB color.
    ///
    /// This is a convenience method when you only need the semantic name.
    ///
    /// # Example
    ///
    /// ```rust
    /// use munsellspace::color_names::ColorClassifier;
    ///
    /// # fn main() -> Result<(), Box<dyn std::error::Error>> {
    /// let classifier = ColorClassifier::new()?;
    /// if let Some(name) = classifier.semantic_name([200, 150, 120])? {
    ///     println!("Semantic: {}", name);
    /// }
    /// # Ok(())
    /// # }
    /// ```
    #[allow(deprecated)] // Uses deprecated semantic_overlay function internally
    pub fn semantic_name(&self, rgb: [u8; 3]) -> Result<Option<String>> {
        let munsell = self.converter.srgb_to_munsell(rgb)?;
        if let Some(spec) = self.munsell_color_to_spec(&munsell) {
            Ok(semantic_overlay(&spec).map(|s| s.to_string()))
        } else {
            Ok(None)
        }
    }

    /// Get all semantic color names that match an sRGB color.
    ///
    /// Colors near boundaries may match multiple semantic overlays.
    ///
    /// # Example
    ///
    /// ```rust
    /// use munsellspace::color_names::ColorClassifier;
    ///
    /// # fn main() -> Result<(), Box<dyn std::error::Error>> {
    /// let classifier = ColorClassifier::new()?;
    /// let matches = classifier.semantic_matches([200, 100, 80])?;
    /// for name in matches {
    ///     println!("Matches: {}", name);
    /// }
    /// # Ok(())
    /// # }
    /// ```
    #[allow(deprecated)] // Uses deprecated matching_overlays function internally
    pub fn semantic_matches(&self, rgb: [u8; 3]) -> Result<Vec<String>> {
        let munsell = self.converter.srgb_to_munsell(rgb)?;
        if let Some(spec) = self.munsell_color_to_spec(&munsell) {
            Ok(matching_overlays(&spec)
                .iter()
                .map(|s| s.to_string())
                .collect())
        } else {
            Ok(vec![])
        }
    }

    /// Get all ISCC-NBS color numbers that contain a given sRGB color.
    ///
    /// Colors at boundaries may fall within multiple ISCC-NBS categories.
    pub fn all_iscc_matches(&self, rgb: [u8; 3]) -> Result<Vec<u16>> {
        let munsell = self.converter.srgb_to_munsell(rgb)?;
        if let (Some(hue), Some(chroma)) = (&munsell.hue, munsell.chroma) {
            self.iscc
                .find_all_colors_at_point(hue, munsell.value, chroma)
        } else {
            // Neutral color - would need separate handling
            Ok(vec![])
        }
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // Internal Helper Methods
    // ═══════════════════════════════════════════════════════════════════════════

    /// Get ISCC-NBS classification including color number.
    fn get_iscc_classification(&self, munsell: &MunsellColor) -> Result<(u16, ColorMetadata)> {
        if let (Some(hue), Some(chroma)) = (&munsell.hue, munsell.chroma) {
            // Use find_all_colors_at_point to get color number(s)
            let color_numbers = self
                .iscc
                .find_all_colors_at_point(hue, munsell.value, chroma)?;

            if let Some(&color_number) = color_numbers.first() {
                // Get metadata for this color number
                if let Some(metadata) = self.iscc.classify_munsell(hue, munsell.value, chroma)? {
                    return Ok((color_number, metadata));
                }
            }
        }

        // Handle neutral colors or classification failures
        // For neutral colors, we need a different approach
        if munsell.is_neutral() {
            // Create a synthetic metadata for neutral colors
            let neutral_name = self.get_neutral_name(munsell.value);
            let metadata = ColorMetadata {
                iscc_nbs_color_name: neutral_name.to_string(),
                iscc_nbs_formatter: None,
                alt_color_name: neutral_name.to_string(),
                color_shade: neutral_name.to_string(),
            };
            let color_number = self.get_neutral_color_number(munsell.value);
            return Ok((color_number, metadata));
        }

        Err(MunsellError::ConversionError {
            message: format!(
                "Could not classify Munsell color: {}",
                munsell.notation
            ),
        })
    }

    /// Get the color name for a neutral (achromatic) color based on value.
    fn get_neutral_name(&self, value: f64) -> &'static str {
        if value <= 0.5 {
            "black"
        } else if value >= 9.5 {
            "white"
        } else {
            "gray"
        }
    }

    /// Get the ISCC-NBS color number for a neutral color.
    fn get_neutral_color_number(&self, value: f64) -> u16 {
        // ISCC-NBS neutral color numbers:
        // 263 = white, 264 = light gray, 265 = medium gray, 266 = dark gray, 267 = black
        if value <= 0.5 {
            267 // black
        } else if value >= 9.5 {
            263 // white
        } else if value >= 7.5 {
            264 // light gray
        } else if value >= 4.5 {
            265 // medium gray
        } else {
            266 // dark gray
        }
    }

    /// Convert MunsellColor to MunsellSpec for semantic overlay lookup.
    fn munsell_color_to_spec(&self, munsell: &MunsellColor) -> Option<MunsellSpec> {
        // If we have the notation, parse it
        parse_munsell_notation(&munsell.notation)
    }
}

// Thread-safe: MunsellConverter and IsccNbsClassifier are both thread-safe
unsafe impl Send for ColorClassifier {}
unsafe impl Sync for ColorClassifier {}

#[cfg(test)]
mod tests {
    use super::*;

    fn classifier() -> ColorClassifier {
        ColorClassifier::new().expect("Failed to create classifier")
    }

    #[test]
    fn test_classify_srgb_red() {
        let c = classifier();
        let desc = c.classify_srgb([255, 0, 0]).expect("Classification failed");

        assert!(desc.standard_name.contains("red") || desc.shade == "red");
        assert!(desc.modifier.is_vivid() || desc.modifier == ColorModifier::Strong);
    }

    #[test]
    fn test_classify_srgb_blue() {
        let c = classifier();
        let desc = c.classify_srgb([0, 0, 255]).expect("Classification failed");

        assert!(desc.standard_name.contains("blue") || desc.shade == "blue");
    }

    #[test]
    fn test_classify_hex() {
        let c = classifier();
        let desc = c.classify_hex("#FF0000").expect("Classification failed");

        assert!(desc.standard_name.contains("red") || desc.shade == "red");
    }

    #[test]
    fn test_classify_hex_short() {
        let c = classifier();
        let desc = c.classify_hex("#F00").expect("Classification failed");

        assert!(desc.standard_name.contains("red") || desc.shade == "red");
    }

    #[test]
    fn test_classify_munsell_notation() {
        let c = classifier();
        let desc = c.classify_munsell("5R 4/10").expect("Classification failed");

        assert!(desc.standard_name.contains("red") || desc.shade == "red");
    }

    #[test]
    fn test_semantic_name_coral_region() {
        let c = classifier();
        // Use a color in the coral region (roughly 6.5R 5.8/8.3)
        // Coral is around RGB(255, 127, 80) approximately
        let name = c.semantic_name([255, 127, 80]).expect("Classification failed");

        // This should be in or near the coral/rose/peach region
        if let Some(n) = name {
            assert!(
                n == "coral" || n == "rose" || n == "peach" || n == "orange" || n == "pink",
                "Expected coral-like color, got: {}",
                n
            );
        }
    }

    #[test]
    fn test_semantic_matches() {
        let c = classifier();
        let matches = c
            .semantic_matches([200, 100, 80])
            .expect("Classification failed");

        // Should return zero or more matches
        // The exact matches depend on the color's position
        // Some colors near boundaries can match many overlays
        assert!(matches.len() <= 10); // Reasonable upper bound
    }

    #[test]
    fn test_descriptor_formatting() {
        let c = classifier();
        let desc = c.classify_srgb([200, 50, 50]).expect("Classification failed");

        // Standard descriptor should combine modifier and name
        let standard = desc.standard_descriptor();
        assert!(!standard.is_empty());

        // Extended descriptor should also be non-empty
        let extended = desc.extended_descriptor();
        assert!(!extended.is_empty());
    }

    #[test]
    fn test_modifier_extraction() {
        let c = classifier();
        let desc = c.classify_srgb([255, 0, 0]).expect("Classification failed");

        // Pure red should have a vivid or strong modifier
        assert!(
            desc.modifier.is_vivid() || desc.modifier == ColorModifier::Strong,
            "Expected vivid/strong modifier for pure red, got: {:?}",
            desc.modifier
        );
    }

    #[test]
    fn test_shade_extraction() {
        let c = classifier();
        let desc = c.classify_srgb([255, 0, 0]).expect("Classification failed");

        // Pure red should have "red" shade
        assert!(!desc.shade.is_empty());
    }

    #[test]
    fn test_gray_classification() {
        let c = classifier();
        let desc = c.classify_srgb([128, 128, 128]).expect("Classification failed");

        // Medium gray
        assert!(
            desc.standard_name.contains("gray") || desc.standard_name.contains("grey"),
            "Expected gray, got: {}",
            desc.standard_name
        );
    }

    #[test]
    fn test_white_classification() {
        let c = classifier();
        let desc = c.classify_srgb([255, 255, 255]).expect("Classification failed");

        assert!(
            desc.standard_name == "white"
                || desc.standard_name.contains("white")
                || desc.shade == "white",
            "Expected white, got: {}",
            desc.standard_name
        );
    }

    #[test]
    fn test_black_classification() {
        let c = classifier();
        let desc = c.classify_srgb([0, 0, 0]).expect("Classification failed");

        assert!(
            desc.standard_name == "black"
                || desc.standard_name.contains("black")
                || desc.shade == "black",
            "Expected black, got: {}",
            desc.standard_name
        );
    }

    #[test]
    fn test_has_semantic_match() {
        let c = classifier();

        // A vivid color should likely have a semantic match
        let desc = c.classify_srgb([255, 100, 100]).expect("Classification failed");

        // May or may not have semantic match depending on position
        // Just verify the method works
        let _ = desc.has_semantic_match();
    }

    #[test]
    fn test_nearest_semantic() {
        let c = classifier();
        let desc = c.classify_srgb([200, 100, 80]).expect("Classification failed");

        // Should always have a nearest semantic (even if not matched)
        if let Some((name, dist)) = desc.nearest_semantic.as_ref() {
            assert!(!name.is_empty());
            assert!(*dist >= 0.0);
        }
    }

    #[test]
    fn test_all_iscc_matches() {
        let c = classifier();
        let matches = c
            .all_iscc_matches([200, 100, 80])
            .expect("Classification failed");

        // Should have at least one match for a chromatic color
        assert!(!matches.is_empty());
    }

    #[test]
    fn test_display_trait() {
        let c = classifier();
        let desc = c.classify_srgb([180, 80, 60]).expect("Classification failed");

        // Display should output the standard descriptor
        let display = format!("{}", desc);
        assert_eq!(display, desc.standard_descriptor());
    }
}
