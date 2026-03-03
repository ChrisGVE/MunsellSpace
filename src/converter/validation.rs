//! Accuracy validation and regression testing for the converter.

use crate::error::Result;
use crate::types::MunsellColor;

use super::{AccuracyStats, MunsellConverter};

impl MunsellConverter {
    /// Regression test: verify the full conversion pipeline reproduces reference data.
    ///
    /// Because reference colors are cached in a HashMap, this method will always
    /// return 100% exact matches for the lookup path. Its value is as a regression
    /// guard: if someone breaks the reference dataset or the HashMap, this fails.
    ///
    /// For algorithmic accuracy measurement, use [`validate_algorithmic_accuracy`].
    pub fn validate_regression(&self) -> Result<AccuracyStats> {
        let mut exact_matches = 0;
        let mut close_matches = 0;
        let total = self.reference_data.len();

        for entry in self.reference_data.iter() {
            match self.srgb_to_munsell(entry.rgb) {
                Ok(converted) => {
                    if converted.notation == entry.munsell {
                        exact_matches += 1;
                    } else if self.is_close_match(&converted.notation, &entry.munsell) {
                        close_matches += 1;
                    }
                }
                Err(_) => {}
            }
        }

        Ok(AccuracyStats {
            total_colors: total,
            exact_matches,
            close_matches,
            accuracy_percentage: (exact_matches as f64 / total as f64) * 100.0,
            close_match_percentage: ((exact_matches + close_matches) as f64 / total as f64) * 100.0,
        })
    }

    /// Measure algorithmic conversion accuracy against the reference dataset.
    ///
    /// Bypasses the HashMap lookup and tests only the mathematical conversion
    /// pipeline, giving a true measurement of algorithmic accuracy.
    pub fn validate_algorithmic_accuracy(&self) -> Result<AccuracyStats> {
        let mut exact_matches = 0;
        let mut close_matches = 0;
        let total = self.reference_data.len();

        for entry in self.reference_data.iter() {
            match self.algorithmic_srgb_to_munsell(entry.rgb) {
                Ok(converted) => {
                    if converted.notation == entry.munsell {
                        exact_matches += 1;
                    } else if self.is_close_match(&converted.notation, &entry.munsell) {
                        close_matches += 1;
                    }
                }
                Err(_) => {}
            }
        }

        Ok(AccuracyStats {
            total_colors: total,
            exact_matches,
            close_matches,
            accuracy_percentage: (exact_matches as f64 / total as f64) * 100.0,
            close_match_percentage: ((exact_matches + close_matches) as f64 / total as f64) * 100.0,
        })
    }

    /// Validate converter accuracy against the reference dataset.
    ///
    /// # Deprecated
    /// Use [`validate_regression`] for regression testing or
    /// [`validate_algorithmic_accuracy`] for true accuracy measurement.
    #[deprecated(
        since = "1.2.3",
        note = "Use validate_regression() or validate_algorithmic_accuracy() instead."
    )]
    pub fn validate_accuracy(&self) -> Result<AccuracyStats> {
        self.validate_regression()
    }

    /// Validate RGB color values.
    #[inline]
    pub(crate) fn validate_rgb(&self, _rgb: [u8; 3]) -> Result<()> {
        // RGB values are already constrained to 0-255 by u8 type
        Ok(())
    }

    /// Check if two Munsell notations are close matches.
    pub(crate) fn is_close_match(&self, notation1: &str, notation2: &str) -> bool {
        if let (Ok(color1), Ok(color2)) = (
            MunsellColor::from_notation(notation1),
            MunsellColor::from_notation(notation2)
        ) {
            if color1.is_neutral() && color2.is_neutral() {
                (color1.value - color2.value).abs() < 0.5
            } else if let (Some(_hue1), Some(_hue2)) = (&color1.hue, &color2.hue) {
                color1.hue_family() == color2.hue_family()
                    && (color1.value - color2.value).abs() < 1.0
                    && color1.chroma.zip(color2.chroma)
                        .map(|(c1, c2)| (c1 - c2).abs() < 2.0)
                        .unwrap_or(false)
            } else {
                false
            }
        } else {
            false
        }
    }
}
