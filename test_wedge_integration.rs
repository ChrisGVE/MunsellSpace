/// Test script to verify the integration of MechanicalWedgeSystem with ISCC_NBS_Classifier
use munsellspace::{ISCC_NBS_Classifier, MechanicalWedgeSystem};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("Testing MechanicalWedgeSystem integration with ISCC_NBS_Classifier...");

    // Test 1: Create the classifier (this should work without errors)
    println!("\n1. Creating ISCC_NBS_Classifier...");
    let classifier = match ISCC_NBS_Classifier::new() {
        Ok(c) => {
            println!("✅ Classifier created successfully");
            c
        },
        Err(e) => {
            println!("❌ Failed to create classifier: {}", e);
            return Err(e.into());
        }
    };

    // Test 2: Try to classify some sample colors
    println!("\n2. Testing color classifications...");
    
    let test_colors = vec![
        ("5R", 4.0, 14.0, "vivid red"),
        ("10YR", 6.0, 8.0, "moderate yellowish brown"),
        ("5B", 3.0, 12.0, "deep blue"),
        ("2.5G", 5.0, 6.0, "grayish green"),
        ("7.5P", 7.0, 10.0, "light purple"),
    ];

    for (hue, value, chroma, expected_description) in test_colors {
        println!("\nTesting: {} {:.1}/{:.1} (expecting: {})", hue, value, chroma, expected_description);
        
        match classifier.classify_munsell(hue, value, chroma) {
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
                println!("❌ Classification failed: {}", e);
            }
        }
    }

    // Test 3: Create a standalone mechanical wedge system
    println!("\n3. Testing standalone MechanicalWedgeSystem...");
    let wedge_system = MechanicalWedgeSystem::new();
    let stats = wedge_system.get_wedge_statistics();
    println!("✅ Wedge system created with {} wedges containing {} total polygons", 
             stats.total_wedges, stats.total_polygons);

    // Test 4: Validate wedge system
    println!("\n4. Validating wedge system...");
    let validation = wedge_system.validate_all_wedges();
    println!("✅ Validation completed for {} wedges", validation.wedge_results.len());

    println!("\n🎉 All tests completed!");
    Ok(())
}