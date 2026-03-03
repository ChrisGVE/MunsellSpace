//! Deprecated ISCC-NBS naming methods on MunsellConverter.
//!
//! These methods delegate to `IsccNbsClassifier` / `ColorClassifier` and will be
//! removed in v2.0.0.

use crate::error::{MunsellError, Result};
use crate::types::{MunsellColor, IsccNbsName, IsccNbsPolygon};

use super::MunsellConverter;

impl MunsellConverter {
    /// Load ISCC-NBS polygon data.
    pub(super) fn load_iscc_nbs_data() -> Result<Vec<IsccNbsPolygon>> {
        // ISCC-NBS classification has moved to IsccNbsClassifier/ColorClassifier.
        // This field is kept for backward compatibility but is no longer populated.
        Ok(Vec::new())
    }

    /// Convert sRGB color directly to ISCC-NBS color name.
    ///
    /// # Deprecated
    /// Use [`ColorClassifier::classify_srgb()`](crate::ColorClassifier::classify_srgb)
    /// for unified color naming including semantic overlays.
    #[deprecated(
        since = "1.2.3",
        note = "Use ColorClassifier::classify_srgb() for unified color naming. This method will be removed in v2.0.0."
    )]
    pub fn srgb_to_color_name(&self, rgb: [u8; 3]) -> Result<IsccNbsName> {
        let munsell = self.srgb_to_munsell(rgb)?;
        #[allow(deprecated)]
        self.munsell_to_iscc_nbs_name(&munsell)
    }

    /// Convert Munsell color to ISCC-NBS color name.
    ///
    /// # Deprecated
    /// Use [`ColorClassifier::classify_srgb()`](crate::ColorClassifier::classify_srgb)
    /// for unified color naming including semantic overlays.
    #[deprecated(
        since = "1.2.3",
        note = "Use ColorClassifier::classify_srgb() for unified color naming. This method will be removed in v2.0.0."
    )]
    pub fn munsell_to_iscc_nbs_name(&self, munsell: &MunsellColor) -> Result<IsccNbsName> {
        use crate::IsccNbsClassifier;

        let classifier = IsccNbsClassifier::new()?;
        let result = classifier.classify_munsell_color(munsell)?;

        match result {
            Some(metadata) => {
                let descriptor = metadata.iscc_nbs_descriptor();
                Ok(IsccNbsName::new(
                    0,
                    descriptor,
                    metadata.iscc_nbs_color_name.clone(),
                    None,
                    metadata.alt_color_name.clone(),
                ))
            }
            None => Err(MunsellError::ConversionError {
                message: format!(
                    "No ISCC-NBS color name found for Munsell color: {}",
                    munsell.notation
                ),
            }),
        }
    }

    /// Get all ISCC-NBS color categories.
    ///
    /// # Deprecated
    /// This method always returns an empty slice. Use [`ColorClassifier`](crate::ColorClassifier)
    /// for ISCC-NBS classification.
    #[deprecated(
        since = "1.2.3",
        note = "Always returns empty. Use ColorClassifier for ISCC-NBS classification. Will be removed in v2.0.0."
    )]
    pub fn get_iscc_nbs_polygons(&self) -> &[IsccNbsPolygon] {
        &self.iscc_nbs_polygons
    }

    /// Find ISCC-NBS color by name or partial match.
    ///
    /// # Deprecated
    /// This method always returns empty results. Use [`ColorClassifier`](crate::ColorClassifier)
    /// for ISCC-NBS classification.
    #[deprecated(
        since = "1.2.3",
        note = "Always returns empty. Use ColorClassifier for ISCC-NBS classification. Will be removed in v2.0.0."
    )]
    pub fn find_colors_by_name(&self, query: &str) -> Vec<&IsccNbsPolygon> {
        let query_lower = query.to_lowercase();
        self.iscc_nbs_polygons
            .iter()
            .filter(|polygon| {
                polygon.descriptor.to_lowercase().contains(&query_lower)
                    || polygon.color_name.to_lowercase().contains(&query_lower)
                    || polygon.revised_color.to_lowercase().contains(&query_lower)
            })
            .collect()
    }
}
