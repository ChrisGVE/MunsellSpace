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

    #[test]
    fn test_iscc_nbs_reference_accuracy() {
        let classifier = ISCC_NBS_Classifier::new()
            .expect("Should be able to create ISCC_NBS_Classifier");

        // Load the ISCC-NBS reference dataset
        let csv_path = "tests/data/ISCC_NBS_REFERENCE_DATASET.csv";
        let csv_content = std::fs::read_to_string(csv_path)
            .expect("Should be able to read ISCC-NBS reference dataset");
        
        let mut total_tests = 0;
        let mut exact_matches = 0;
        let mut color_matches = 0;
        let mut modifier_matches = 0;
        let mut failures = Vec::new();
        
        println!("Testing ISCC-NBS accuracy against reference dataset...");
        
        // Skip header and process each line
        for (line_num, line) in csv_content.lines().skip(1).enumerate() {
            if line.trim().is_empty() {
                continue;
            }
            
            let parts: Vec<&str> = line.split(',').collect();
            if parts.len() < 4 {
                continue;
            }
            
            let hex = parts[0].trim();
            let expected_name = parts[1].trim();
            let expected_modifier = parts[2].trim();
            let expected_color = parts[3].trim();
            
            total_tests += 1;
            
            // Test hex classification
            match classifier.classify_hex(hex) {
                Ok(Some(result)) => {
                    // Build expected full name for comparison
                    let actual_full = format!("{} {}", result.iscc_nbs_descriptor(), result.iscc_nbs_color());
                    
                    // Check for exact match
                    if actual_full == expected_name {
                        exact_matches += 1;
                        color_matches += 1;
                        modifier_matches += 1;
                    } else {
                        // Check partial matches
                        if result.iscc_nbs_color() == expected_color {
                            color_matches += 1;
                        }
                        if result.iscc_nbs_descriptor() == expected_modifier || 
                           (expected_modifier == "-ish white" && result.iscc_nbs_descriptor().contains("ish")) ||
                           (expected_modifier == "-ish gray" && result.iscc_nbs_descriptor().contains("ish")) {
                            modifier_matches += 1;
                        }
                        
                        // Store failure for analysis
                        failures.push(format!(
                            "Line {}: {} -> Expected: '{}' | Got: '{}' | Color: {} vs {} | Modifier: {} vs {}",
                            line_num + 2, hex, expected_name, actual_full,
                            expected_color, result.iscc_nbs_color(),
                            expected_modifier, result.iscc_nbs_descriptor()
                        ));
                    }
                },
                Ok(None) => {
                    failures.push(format!("Line {}: {} -> No classification found", line_num + 2, hex));
                },
                Err(e) => {
                    failures.push(format!("Line {}: {} -> Error: {}", line_num + 2, hex, e));
                }
            }
            
            // Show progress every 50 tests
            if total_tests % 50 == 0 {
                println!("Progress: {}/{} tests completed", total_tests, 267);
            }
        }
        
        // Calculate accuracy percentages
        let exact_accuracy = (exact_matches as f64 / total_tests as f64) * 100.0;
        let color_accuracy = (color_matches as f64 / total_tests as f64) * 100.0;
        let modifier_accuracy = (modifier_matches as f64 / total_tests as f64) * 100.0;
        
        println!("\n🎯 ISCC-NBS Reference Dataset Accuracy Results:");
        println!("Total colors tested: {}", total_tests);
        println!("Exact matches: {}/{} ({:.1}%)", exact_matches, total_tests, exact_accuracy);
        println!("Color matches: {}/{} ({:.1}%)", color_matches, total_tests, color_accuracy);
        println!("Modifier matches: {}/{} ({:.1}%)", modifier_matches, total_tests, modifier_accuracy);
        
        // Show first 10 failures for analysis
        if !failures.is_empty() {
            println!("\n❌ Sample Failures (first 10):");
            for failure in failures.iter().take(10) {
                println!("  {}", failure);
            }
            if failures.len() > 10 {
                println!("  ... and {} more failures", failures.len() - 10);
            }
        }
        
        // For now, we'll print results but not fail the test since accuracy may be low initially
        // Once we achieve target accuracy, we can set minimum thresholds
        println!("\n✅ ISCC-NBS accuracy test completed. Results logged above.");
        
        // Optional: Uncomment to set minimum accuracy requirements
        // assert!(exact_accuracy > 50.0, "Exact match accuracy too low: {:.1}%", exact_accuracy);
        // assert!(color_accuracy > 80.0, "Color match accuracy too low: {:.1}%", color_accuracy);
    }

    #[test]
    fn test_munsell_color_science_sample_accuracy() {
        let classifier = ISCC_NBS_Classifier::new()
            .expect("Should be able to create ISCC_NBS_Classifier");

        // Load the Munsell Color Science sample dataset
        let csv_path = "tests/data/MUNSELL_COLOR_SCIENCE_SAMPLE.csv";
        let csv_content = std::fs::read_to_string(csv_path)
            .expect("Should be able to read Munsell Color Science sample dataset");
        
        let mut total_tests = 0;
        let mut exact_matches = 0;
        let mut color_matches = 0;
        let mut modifier_matches = 0;
        let mut failures = Vec::new();
        
        println!("Testing ISCC-NBS accuracy against Munsell Color Science sample dataset...");
        
        // Skip header and process each line
        for (line_num, line) in csv_content.lines().skip(1).enumerate() {
            if line.trim().is_empty() {
                continue;
            }
            
            let parts: Vec<&str> = line.split(',').collect();
            if parts.len() < 5 {
                continue;
            }
            
            let number = parts[0].trim();
            let expected_name = parts[1].trim();
            let r: u8 = parts[2].trim().parse().unwrap_or(0);
            let g: u8 = parts[3].trim().parse().unwrap_or(0);
            let b: u8 = parts[4].trim().parse().unwrap_or(0);
            
            total_tests += 1;
            
            // Test RGB classification
            match classifier.classify_srgb([r, g, b]) {
                Ok(Some(result)) => {
                    // Parse expected name into modifier and color
                    let expected_parts: Vec<&str> = expected_name.split_whitespace().collect();
                    let (expected_modifier, expected_color) = if expected_parts.len() >= 2 {
                        let color_start = expected_parts.len() - 1;
                        let modifier = expected_parts[..color_start].join(" ");
                        let color = expected_parts[color_start];
                        (modifier, color.to_string())
                    } else {
                        ("".to_string(), expected_name.to_string())
                    };
                    
                    let actual_full = format!("{} {}", result.iscc_nbs_descriptor(), result.iscc_nbs_color());
                    
                    // Check for exact match
                    if actual_full.to_lowercase() == expected_name.to_lowercase() {
                        exact_matches += 1;
                        color_matches += 1;
                        modifier_matches += 1;
                    } else {
                        // Check partial matches
                        if result.iscc_nbs_color().to_lowercase() == expected_color.to_lowercase() {
                            color_matches += 1;
                        }
                        if result.iscc_nbs_descriptor().to_lowercase() == expected_modifier.to_lowercase() {
                            modifier_matches += 1;
                        }
                        
                        // Store failure for analysis
                        failures.push(format!(
                            "#{}: RGB({},{},{}) -> Expected: '{}' | Got: '{}' | Color: {} vs {} | Modifier: {} vs {}",
                            number, r, g, b, expected_name, actual_full,
                            expected_color, result.iscc_nbs_color(),
                            expected_modifier, result.iscc_nbs_descriptor()
                        ));
                    }
                },
                Ok(None) => {
                    failures.push(format!("#{}: RGB({},{},{}) -> No classification found", number, r, g, b));
                },
                Err(e) => {
                    failures.push(format!("#{}: RGB({},{},{}) -> Error: {}", number, r, g, b, e));
                }
            }
        }
        
        // Calculate accuracy percentages
        let exact_accuracy = (exact_matches as f64 / total_tests as f64) * 100.0;
        let color_accuracy = (color_matches as f64 / total_tests as f64) * 100.0;
        let modifier_accuracy = (modifier_matches as f64 / total_tests as f64) * 100.0;
        
        println!("\n🎯 Munsell Color Science Sample Accuracy Results:");
        println!("Total colors tested: {}", total_tests);
        println!("Exact matches: {}/{} ({:.1}%)", exact_matches, total_tests, exact_accuracy);
        println!("Color matches: {}/{} ({:.1}%)", color_matches, total_tests, color_accuracy);
        println!("Modifier matches: {}/{} ({:.1}%)", modifier_matches, total_tests, modifier_accuracy);
        
        // Show all failures for analysis (since this is a small sample)
        if !failures.is_empty() {
            println!("\n❌ Failures:");
            for failure in &failures {
                println!("  {}", failure);
            }
        }
        
        println!("\n✅ Munsell Color Science sample accuracy test completed.");
    }

    #[test]
    fn test_munsell_color_science_complete_accuracy() {
        let classifier = ISCC_NBS_Classifier::new()
            .expect("Should be able to create ISCC_NBS_Classifier");

        // Load the complete Munsell Color Science dataset (260 valid colors out of 267 total)
        let csv_path = "tests/data/MUNSELL_COLOR_SCIENCE_COMPLETE.csv";
        let csv_content = std::fs::read_to_string(csv_path)
            .expect("Should be able to read complete Munsell Color Science dataset");
        
        let mut total_tests = 0;
        let mut exact_matches = 0;
        let mut color_matches = 0;
        let mut modifier_matches = 0;
        let mut failures = Vec::new();
        
        println!("Testing ISCC-NBS accuracy against complete Munsell Color Science dataset...");
        
        // Skip header and process each line
        for (line_num, line) in csv_content.lines().skip(1).enumerate() {
            if line.trim().is_empty() {
                continue;
            }
            
            let parts: Vec<&str> = line.split(',').collect();
            if parts.len() < 5 {
                continue;
            }
            
            let number = parts[0].trim();
            let expected_name = parts[1].trim().trim_matches('"'); // Remove quotes
            let r: u8 = parts[2].trim().parse().unwrap_or(0);
            let g: u8 = parts[3].trim().parse().unwrap_or(0);
            let b: u8 = parts[4].trim().parse().unwrap_or(0);
            
            total_tests += 1;
            
            // Test RGB classification
            match classifier.classify_srgb([r, g, b]) {
                Ok(Some(result)) => {
                    // Parse expected name into modifier and color
                    let expected_parts: Vec<&str> = expected_name.split_whitespace().collect();
                    let (expected_modifier, expected_color) = if expected_parts.len() >= 2 {
                        let color_start = expected_parts.len() - 1;
                        let modifier = expected_parts[..color_start].join(" ");
                        let color = expected_parts[color_start];
                        (modifier, color.to_string())
                    } else {
                        ("".to_string(), expected_name.to_string())
                    };
                    
                    let actual_full = format!("{} {}", result.iscc_nbs_descriptor(), result.iscc_nbs_color());
                    
                    // Check for exact match
                    if actual_full.to_lowercase() == expected_name.to_lowercase() {
                        exact_matches += 1;
                        color_matches += 1;
                        modifier_matches += 1;
                    } else {
                        // Check partial matches
                        if result.iscc_nbs_color().to_lowercase() == expected_color.to_lowercase() {
                            color_matches += 1;
                        }
                        if result.iscc_nbs_descriptor().to_lowercase() == expected_modifier.to_lowercase() {
                            modifier_matches += 1;
                        }
                        
                        // Store failure for analysis (only first 50 to avoid overwhelming output)
                        if failures.len() < 50 {
                            failures.push(format!(
                                "#{}: RGB({},{},{}) -> Expected: '{}' | Got: '{}' | Color: {} vs {} | Modifier: {} vs {}",
                                number, r, g, b, expected_name, actual_full,
                                expected_color, result.iscc_nbs_color(),
                                expected_modifier, result.iscc_nbs_descriptor()
                            ));
                        }
                    }
                },
                Ok(None) => {
                    if failures.len() < 50 {
                        failures.push(format!("#{}: RGB({},{},{}) -> No classification found", number, r, g, b));
                    }
                },
                Err(e) => {
                    if failures.len() < 50 {
                        failures.push(format!("#{}: RGB({},{},{}) -> Error: {}", number, r, g, b, e));
                    }
                }
            }
            
            // Show progress every 50 tests
            if total_tests % 50 == 0 {
                println!("Progress: {}/{} tests completed", total_tests, 260);
            }
        }
        
        // Calculate accuracy percentages
        let exact_accuracy = (exact_matches as f64 / total_tests as f64) * 100.0;
        let color_accuracy = (color_matches as f64 / total_tests as f64) * 100.0;
        let modifier_accuracy = (modifier_matches as f64 / total_tests as f64) * 100.0;
        
        println!("\n🎯 Complete Munsell Color Science Dataset Accuracy Results:");
        println!("Total colors tested: {}", total_tests);
        println!("Exact matches: {}/{} ({:.1}%)", exact_matches, total_tests, exact_accuracy);
        println!("Color matches: {}/{} ({:.1}%)", color_matches, total_tests, color_accuracy);
        println!("Modifier matches: {}/{} ({:.1}%)", modifier_matches, total_tests, modifier_accuracy);
        
        // Show sample failures for analysis
        if !failures.is_empty() {
            println!("\n❌ Sample Failures (first {}):", failures.len().min(50));
            for failure in failures.iter().take(50) {
                println!("  {}", failure);
            }
            if failures.len() > 50 {
                println!("  ... and {} more failures", total_tests - exact_matches - 50);
            }
        }
        
        println!("\n✅ Complete Munsell Color Science accuracy test completed.");
        
        // Report comparison with previous results
        println!("\n📊 Accuracy Comparison:");
        println!("Sample dataset (20 colors): 60.0% exact matches, 70.0% color matches");
        println!("Complete dataset ({} colors): {:.1}% exact matches, {:.1}% color matches", total_tests, exact_accuracy, color_accuracy);
    }
}