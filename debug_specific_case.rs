use munsellspace::{ISCC_NBS_Classifier, MunsellConverter};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🐛 Debugging specific case: #886648 -> 9.5R 4.5/6.0");
    
    // Step 1: Convert RGB to Munsell (this should work)
    let converter = MunsellConverter::new()?;
    let rgb = [0x88, 0x66, 0x48]; // #886648
    let munsell = converter.srgb_to_munsell(rgb)?;
    
    println!("✅ RGB to Munsell conversion: {:?}", munsell);
    println!("   Hue: {:?}, Value: {}, Chroma: {:?}", munsell.hue, munsell.value, munsell.chroma);
    
    // Step 2: Try ISCC-NBS classification with detailed debugging
    let classifier = ISCC_NBS_Classifier::new()?;
    
    // Test the specific coordinates
    let hue = "9.5R";
    let value = 4.5;
    let chroma = 6.0;
    
    println!("\n🔍 Testing classification with exact coordinates:");
    println!("   Hue: {}, Value: {}, Chroma: {}", hue, value, chroma);
    
    // Add debug tracing for the wedge system
    println!("\n🔍 Debug tracing wedge system:");
    
    // First, let me check what wedge this should map to
    println!("   Expected: 9.5R should map to wedge 10R→1YR");
    
    let result = classifier.classify_munsell(hue, value, chroma)?;
    
    match result {
        Some(classification) => {
            println!("✅ Classification found: {} {}", 
                     classification.iscc_nbs_descriptor, 
                     classification.iscc_nbs_color);
            println!("   ISCC-NBS color ID: {}", classification.iscc_nbs_color_id);
        }
        None => {
            println!("❌ No classification found!");
            println!("\n🔍 This indicates either:");
            println!("   1. Wedge key '10R→1YR' doesn't exist");
            println!("   2. Polygon color 43 not found in that wedge");
            println!("   3. Point-in-polygon test failing");
            
            // Let's debug this step by step
            println!("\n🔧 Starting systematic debugging...");
            
            // Step 1: Check where color 43 is located in the system
            let color_43_wedges = classifier.debug_find_all_color_43();
            println!("🔍 Color 43 found in wedges: {:?}", color_43_wedges);
            
            // Step 2: Check if the expected wedge exists
            let expected_wedge = "10R→1YR";
            if let Some(contents) = classifier.debug_wedge_contents(expected_wedge) {
                println!("✅ Wedge {} exists with {} colors:", expected_wedge, contents.len());
                for (i, content) in contents.iter().take(5).enumerate() {
                    println!("   {}: {}", i+1, content);
                }
                if contents.len() > 5 {
                    println!("   ... and {} more", contents.len() - 5);
                }
                
                // Step 3: Test point-in-polygon for color 43 specifically
                if let Some(detailed_info) = classifier.debug_test_point_detailed(expected_wedge, 43, value, chroma) {
                    println!("🔍 Detailed point-in-polygon analysis:");
                    println!("{}", detailed_info);
                    
                    // Test a point clearly inside the polygon to verify the issue
                    println!("\n🔧 Testing boundary condition:");
                    println!("   Original point (6, 4.5) is on the TOP EDGE of polygon");
                    println!("   Testing point clearly inside: (5, 3.5)");
                    if let Some(inside_result) = classifier.debug_test_point(expected_wedge, 43, 3.5, 5.0) {
                        println!("   Point (3.5, 5.0) inside polygon: {}", inside_result);
                    }
                    
                    println!("   Testing point just below edge: (4.4, 6.0)");  
                    if let Some(below_edge) = classifier.debug_test_point(expected_wedge, 43, 4.4, 6.0) {
                        println!("   Point (4.4, 6.0) inside polygon: {}", below_edge);
                    }
                } else {
                    println!("❌ Color 43 not found in wedge {}", expected_wedge);
                }
            } else {
                println!("❌ Expected wedge {} does NOT exist", expected_wedge);
                
                // Check what wedges do exist around this area
                println!("🔍 Checking for similar wedge keys...");
                let wedge_stats = classifier.wedge_system.get_wedge_statistics();
                for wedge_key in wedge_stats.wedge_counts.keys() {
                    if wedge_key.contains("10R") || wedge_key.contains("1YR") {
                        println!("   Found related wedge: {}", wedge_key);
                    }
                }
            }
        }
    }
    
    // Step 3: Test with the full RGB path
    println!("\n🔍 Testing with full RGB classification:");
    let rgb_result = classifier.classify_srgb(rgb)?;
    
    match rgb_result {
        Some(classification) => {
            println!("✅ RGB classification: {} {}", 
                     classification.iscc_nbs_descriptor, 
                     classification.iscc_nbs_color);
        }
        None => {
            println!("❌ RGB classification failed!");
        }
    }
    
    println!("\n📋 Expected result: 'moderate yellowish brown' (color 43)");
    
    Ok(())
}