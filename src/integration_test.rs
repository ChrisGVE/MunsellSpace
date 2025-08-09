/// Test module to verify the integration of MechanicalWedgeSystem with ISCC_NBS_Classifier

#[cfg(test)]
mod tests {
    use crate::{ISCC_NBS_Classifier, MechanicalWedgeSystem};

    #[test]
    fn test_classifier_creation() {
        // Test 1: Create the classifier (this should work without errors)
        println!("Creating ISCC_NBS_Classifier...");
        let classifier = ISCC_NBS_Classifier::new()
            .expect("Should be able to create ISCC_NBS_Classifier");
        println!("✅ Classifier created successfully");

        // Test 2: Try to classify a sample color
        println!("Testing color classification...");
        match classifier.classify_munsell("5R", 4.0, 14.0) {
            Ok(Some(result)) => {
                println!("✅ Classification successful:");
                println!("   ISCC-NBS: {} {}", result.iscc_nbs_descriptor(), result.iscc_nbs_color());
                println!("   Revised: {}", result.revised_descriptor());
                println!("   Color ID: {}", result.iscc_nbs_color_id());
            },
            Ok(None) => {
                println!("⚠️  No classification found (color may be outside defined regions)");
            },
            Err(e) => {
                panic!("Classification failed: {}", e);
            }
        }
    }

    #[test]
    fn test_mechanical_wedge_system() {
        // Test 3: Create a standalone mechanical wedge system
        println!("Testing standalone MechanicalWedgeSystem...");
        let wedge_system = MechanicalWedgeSystem::new();
        let stats = wedge_system.get_wedge_statistics();
        println!("✅ Wedge system created with {} wedges containing {} total polygons", 
                 stats.total_wedges, stats.total_polygons);

        assert_eq!(stats.total_wedges, 100, "Should have exactly 100 wedges");
    }

    #[test]
    fn test_multiple_classifications() {
        let classifier = ISCC_NBS_Classifier::new()
            .expect("Should be able to create ISCC_NBS_Classifier");

        let test_colors = vec![
            ("5R", 4.0, 14.0),
            ("10YR", 6.0, 8.0), 
            ("5B", 3.0, 12.0),
            ("2.5G", 5.0, 6.0),
        ];

        let mut successful_classifications = 0;
        let mut total_tests = 0;

        for (hue, value, chroma) in test_colors {
            total_tests += 1;
            println!("Testing: {} {:.1}/{:.1}", hue, value, chroma);
            
            match classifier.classify_munsell(hue, value, chroma) {
                Ok(Some(result)) => {
                    successful_classifications += 1;
                    println!("✅ Classification: {} {}", result.iscc_nbs_descriptor(), result.iscc_nbs_color());
                },
                Ok(None) => {
                    println!("⚠️  No classification found");
                },
                Err(e) => {
                    println!("❌ Classification failed: {}", e);
                }
            }
        }

        println!("Successful classifications: {}/{}", successful_classifications, total_tests);
    }

    #[test]
    fn test_direct_entry_points() {
        let classifier = ISCC_NBS_Classifier::new()
            .expect("Should be able to create ISCC_NBS_Classifier");

        // Test hex classification
        println!("Testing hex classification...");
        match classifier.classify_hex("#FF0000") {
            Ok(Some(result)) => {
                println!("✅ Hex #FF0000: {} {}", result.iscc_nbs_descriptor(), result.iscc_nbs_color());
            },
            Ok(None) => {
                println!("⚠️  No classification for #FF0000");
            },
            Err(e) => {
                panic!("Hex classification failed: {}", e);
            }
        }

        // Test short hex format
        match classifier.classify_hex("f00") {
            Ok(Some(result)) => {
                println!("✅ Hex f00: {} {}", result.iscc_nbs_descriptor(), result.iscc_nbs_color());
            },
            Ok(None) => {
                println!("⚠️  No classification for f00");
            },
            Err(e) => {
                panic!("Short hex classification failed: {}", e);
            }
        }

        // Test Lab classification  
        println!("Testing Lab classification...");
        match classifier.classify_lab([53.23, 80.11, 67.22]) {
            Ok(Some(result)) => {
                println!("✅ Lab bright red: {} {}", result.iscc_nbs_descriptor(), result.iscc_nbs_color());
            },
            Ok(None) => {
                println!("⚠️  No classification for Lab bright red");
            },
            Err(e) => {
                panic!("Lab classification failed: {}", e);
            }
        }

        println!("✅ All direct entry point tests completed successfully");
    }
}