//! Property-based tests for MunsellSpace library using proptest.
//!
//! These tests verify that the library maintains consistent behavior
//! across a wide range of inputs and satisfies important invariants.

#[cfg(test)]
mod property_tests {
    use crate::{MunsellConverter, MunsellColor};
    use proptest::prelude::*;
    use std::sync::Arc;

    /// Property: All valid RGB values should convert without error
    proptest! {
        #[test]
        fn prop_all_rgb_values_convert_successfully(
            r in 0u8..=255,
            g in 0u8..=255,
            b in 0u8..=255
        ) {
            let converter = MunsellConverter::new().unwrap();
            let result = converter.srgb_to_munsell([r, g, b]);
            
            // Should never panic or return error for valid RGB values
            prop_assert!(result.is_ok(), "Failed to convert RGB[{}, {}, {}]: {:?}", r, g, b, result);
            
            let munsell = result.unwrap();
            
            // Basic invariants
            prop_assert!(munsell.value >= 0.0 && munsell.value <= 10.0, 
                        "Value out of range: {}", munsell.value);
            
            if let Some(chroma) = munsell.chroma {
                prop_assert!(chroma >= 0.0, "Negative chroma: {}", chroma);
                prop_assert!(chroma <= 50.0, "Unreasonably high chroma: {}", chroma); // Very conservative upper bound
            }
        }
    }

    /// Property: Converting the same RGB value multiple times should always give the same result
    proptest! {
        #[test]
        fn prop_rgb_conversion_deterministic(
            r in 0u8..=255,
            g in 0u8..=255,
            b in 0u8..=255
        ) {
            let converter = MunsellConverter::new().unwrap();
            let rgb = [r, g, b];
            
            let result1 = converter.srgb_to_munsell(rgb).unwrap();
            let result2 = converter.srgb_to_munsell(rgb).unwrap();
            let result3 = converter.srgb_to_munsell(rgb).unwrap();
            
            prop_assert_eq!(&result1.notation, &result2.notation, "Non-deterministic conversion for RGB{:?}", rgb);
            prop_assert_eq!(&result1.notation, &result3.notation, "Non-deterministic conversion for RGB{:?}", rgb);
            prop_assert_eq!(result1.value, result2.value, "Non-deterministic value for RGB{:?}", rgb);
            prop_assert_eq!(result1.chroma, result2.chroma, "Non-deterministic chroma for RGB{:?}", rgb);
        }
    }

    /// Property: Batch conversion should give same results as individual conversions
    proptest! {
        #[test]
        fn prop_batch_conversion_equals_individual(
            colors in prop::collection::vec(
                (0u8..=255, 0u8..=255, 0u8..=255), 1..=10
            )
        ) {
            let converter = MunsellConverter::new().unwrap();
            let rgb_colors: Vec<[u8; 3]> = colors.into_iter()
                .map(|(r, g, b)| [r, g, b])
                .collect();
            
            // Individual conversions
            let individual_results: Result<Vec<_>, _> = rgb_colors.iter()
                .map(|&rgb| converter.srgb_to_munsell(rgb))
                .collect();
            let individual_results = individual_results.unwrap();
            
            // Batch conversion
            let batch_results = converter.convert_batch(&rgb_colors).unwrap();
            
            prop_assert_eq!(individual_results.len(), batch_results.len());
            
            for (i, (individual, batch)) in individual_results.iter().zip(batch_results.iter()).enumerate() {
                prop_assert_eq!(&individual.notation, &batch.notation,
                    "Batch/individual mismatch at index {}: individual='{}', batch='{}'", 
                    i, individual.notation, batch.notation);
            }
        }
    }

    /// Property: Neutral colors (grayscale) should have no hue information
    proptest! {
        #[test]
        fn prop_grayscale_colors_neutral(
            value in 0u8..=255
        ) {
            let converter = MunsellConverter::new().unwrap();
            let gray_rgb = [value, value, value];
            let result = converter.srgb_to_munsell(gray_rgb).unwrap();
            
            if result.is_neutral() {
                prop_assert!(result.hue.is_none(), "Neutral color should have no hue");
                prop_assert!(result.chroma.is_none(), "Neutral color should have no chroma"); 
                prop_assert!(result.notation.starts_with('N'), "Neutral notation should start with 'N'");
            } else {
                // Very dark or very light grays might have slight chromatic artifacts
                // due to numerical precision, but chroma should be very low
                if let Some(chroma) = result.chroma {
                    prop_assert!(chroma < 2.0, 
                        "Grayscale RGB{:?} should have low chroma, got {}", gray_rgb, chroma);
                }
            }
        }
    }

    /// Property: Black should always convert to N 0.0
    #[test]
    fn prop_black_always_neutral_zero() {
        let converter = MunsellConverter::new().unwrap();
        let black = converter.srgb_to_munsell([0, 0, 0]).unwrap();
        
        assert_eq!(black.notation, "N 0.0");
        assert!(black.is_neutral());
        assert_eq!(black.value, 0.0);
        assert!(black.hue.is_none());
        assert!(black.chroma.is_none());
    }

    /// Property: Colors with higher luminance should have higher Munsell value
    proptest! {
        #[test]
        fn prop_luminance_correlates_with_value(
            base_value in 10u8..=200, // Avoid very dark/bright to ensure clear ordering
            increment in 10u8..=50
        ) {
            let converter = MunsellConverter::new().unwrap();
            let darker_rgb = [base_value, base_value, base_value];
            let lighter_rgb = [
                (base_value.saturating_add(increment)).min(255),
                (base_value.saturating_add(increment)).min(255), 
                (base_value.saturating_add(increment)).min(255)
            ];
            
            let darker_result = converter.srgb_to_munsell(darker_rgb).unwrap();
            let lighter_result = converter.srgb_to_munsell(lighter_rgb).unwrap();
            
            // Lighter color should have higher Munsell value
            prop_assert!(lighter_result.value >= darker_result.value,
                "Lighter RGB{:?} (value={}) should have higher value than darker RGB{:?} (value={})",
                lighter_rgb, lighter_result.value, darker_rgb, darker_result.value);
        }
    }

    /// Property: Thread safety - multiple threads should produce consistent results
    proptest! {
        #[test]
        fn prop_thread_safety(
            colors in prop::collection::vec(
                (0u8..=255, 0u8..=255, 0u8..=255), 5..=15
            )
        ) {
            let converter = Arc::new(MunsellConverter::new().unwrap());
            let rgb_colors: Vec<[u8; 3]> = colors.into_iter()
                .map(|(r, g, b)| [r, g, b])
                .collect();
            
            // Convert on main thread
            let main_results: Vec<_> = rgb_colors.iter()
                .map(|&rgb| converter.srgb_to_munsell(rgb).unwrap().notation)
                .collect();
            
            // Convert on separate threads
            let converter_clone = Arc::clone(&converter);
            let colors_clone = rgb_colors.clone();
            let handle = std::thread::spawn(move || {
                colors_clone.iter()
                    .map(|&rgb| converter_clone.srgb_to_munsell(rgb).unwrap().notation)
                    .collect::<Vec<_>>()
            });
            
            let thread_results = handle.join().unwrap();
            
            prop_assert_eq!(main_results, thread_results, 
                "Thread safety violation: results differ between threads");
        }
    }

    /// Property: Valid Munsell notation parsing should be invertible
    proptest! {
        #[test]
        fn prop_munsell_notation_parsing_roundtrip(
            r in 0u8..=255,
            g in 0u8..=255,
            b in 0u8..=255
        ) {
            let converter = MunsellConverter::new().unwrap();
            let rgb = [r, g, b];
            
            let munsell = converter.srgb_to_munsell(rgb).unwrap();
            let notation = munsell.notation.clone();
            
            // Parse the notation back
            let parsed = MunsellColor::from_notation(&notation);
            
            prop_assert!(parsed.is_ok(), "Failed to parse generated notation '{}' for RGB{:?}", notation, rgb);
            
            let parsed_munsell = parsed.unwrap();
            
            // Should match original
            prop_assert_eq!(&munsell.notation, &parsed_munsell.notation);
            prop_assert_eq!(munsell.is_neutral(), parsed_munsell.is_neutral());
            
            // Values should be very close (allow for formatting precision)
            prop_assert!((munsell.value - parsed_munsell.value).abs() < 0.01,
                "Value mismatch: original={}, parsed={}", munsell.value, parsed_munsell.value);
        }
    }

    /// Property: Extreme RGB values should convert without overflow/underflow
    proptest! {
        #[test]
        fn prop_extreme_rgb_values_safe(
            extreme_pattern in 0u8..=7 // 3 bits for R, G, B extreme patterns
        ) {
            let converter = MunsellConverter::new().unwrap();
            
            // Generate extreme combinations
            let extreme_values = [0, 255];
            let r = extreme_values[(extreme_pattern & 1) as usize];
            let g = extreme_values[((extreme_pattern >> 1) & 1) as usize];
            let b = extreme_values[((extreme_pattern >> 2) & 1) as usize];
            
            let rgb = [r, g, b];
            let result = converter.srgb_to_munsell(rgb);
            
            prop_assert!(result.is_ok(), "Failed to convert extreme RGB{:?}: {:?}", rgb, result);
            
            let munsell = result.unwrap();
            
            // Check for reasonable bounds (no overflow/underflow)
            prop_assert!(munsell.value >= 0.0 && munsell.value <= 10.0);
            if let Some(chroma) = munsell.chroma {
                prop_assert!(chroma >= 0.0 && chroma.is_finite());
            }
            
            // Notation should be valid
            prop_assert!(!munsell.notation.is_empty());
            prop_assert!(munsell.notation.len() < 20); // Reasonable length bound
        }
    }
}