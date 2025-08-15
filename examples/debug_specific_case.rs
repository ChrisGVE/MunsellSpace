use munsellspace::{ISCC_NBS_Classifier, MunsellConverter};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🐛 Debugging specific case: #886648 -> 9.5R 4.5/6.0");
    
    // Step 1: Convert RGB to Munsell (this should work)
    let converter = MunsellConverter::new()?;
    let rgb = [0x88, 0x66, 0x48]; // #886648
    let munsell = converter.srgb_to_munsell(rgb)?;
    
    println!("✅ RGB to Munsell conversion: {:?}", munsell);
    println!("   Hue: {:?}, Value: {}, Chroma: {:?}", munsell.hue, munsell.value, munsell.chroma);
    
    // Step 2: Try ISCC-NBS classification
    let classifier = ISCC_NBS_Classifier::new()?;
    
    // Test the specific coordinates
    let hue = "9.5R";
    let value = 4.5;
    let chroma = 6.0;
    
    println!("\n🔍 Testing classification with exact coordinates:");
    println!("   Hue: {}, Value: {}, Chroma: {}", hue, value, chroma);
    
    let result = classifier.classify_munsell(hue, value, chroma)?;
    
    match result {
        Some(classification) => {
            println!("✅ Classification found: {} {}", 
                     classification.iscc_nbs_descriptor(), 
                     classification.iscc_nbs_color_name);
        }
        None => {
            println!("❌ No classification found!");
            println!("\n🔍 This indicates either:");
            println!("   1. Wedge key '10R→1YR' doesn't exist");
            println!("   2. Polygon color 43 not found in that wedge");
            println!("   3. Point-in-polygon test failing");
        }
    }
    
    // Step 3: Test with the full RGB path
    println!("\n🔍 Testing with full RGB classification:");
    let rgb_result = classifier.classify_srgb(rgb)?;
    
    match rgb_result {
        Some(classification) => {
            println!("✅ RGB classification: {} {}", 
                     classification.iscc_nbs_descriptor(), 
                     classification.iscc_nbs_color_name);
        }
        None => {
            println!("❌ RGB classification failed!");
        }
    }
    
    println!("\n📋 Expected result: 'moderate yellowish brown' (color 43)");
    
    Ok(())
}