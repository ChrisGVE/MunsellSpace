use munsellspace::{MunsellConverter, IsccNbsClassifier};

#[test]
fn test_pure_red_conversion_pipeline() {
    // Test what pure red converts to in Munsell space
    let converter = MunsellConverter::new().expect("Failed to create converter");
    let classifier = IsccNbsClassifier::new().expect("Failed to create classifier");
    
    let pure_red = [255, 0, 0];
    
    // First, see what Munsell color pure red becomes
    match converter.srgb_to_munsell(pure_red) {
        Ok(munsell) => {
            println!("Pure red RGB [255, 0, 0] converts to Munsell:");
            println!("  Hue: {:?}", munsell.hue);
            println!("  Value: {:.2}", munsell.value);
            println!("  Chroma: {:?}", munsell.chroma);
            
            // Now try to classify this Munsell color
            if let (Some(hue), Some(chroma)) = (&munsell.hue, munsell.chroma) {
                match classifier.classify_munsell(hue, munsell.value, chroma) {
                    Ok(Some(result)) => {
                        println!("  ISCC-NBS Classification:");
                        println!("    Descriptor: {}", result.iscc_nbs_descriptor());
                        println!("    Color: {}", result.iscc_nbs_color());
                        println!("    Full Name: {} {}", result.iscc_nbs_descriptor(), result.iscc_nbs_color());
                    }
                    Ok(None) => {
                        println!("  No ISCC-NBS classification found for this Munsell color");
                    }
                    Err(e) => {
                        println!("  ISCC-NBS classification error: {}", e);
                    }
                }
            } else {
                println!("  Neutral color (no hue/chroma)");
            }
        }
        Err(e) => {
            println!("Munsell conversion error: {}", e);
        }
    }
}

#[test]
fn test_moderate_colors() {
    // Test some moderate colors that are more likely to be in ISCC-NBS space
    let classifier = IsccNbsClassifier::new().expect("Failed to create classifier");
    
    let test_colors = vec![
        ([128, 64, 64], "brownish red"),
        ([64, 128, 64], "moderate green"),
        ([64, 64, 128], "moderate blue"),
        ([128, 128, 64], "olive"),
    ];
    
    for (rgb, expected_description) in test_colors {
        match classifier.classify_srgb(rgb) {
            Ok(Some(result)) => {
                println!("RGB {:?} ({}):", rgb, expected_description);
                println!("  ISCC-NBS: {} {}", result.iscc_nbs_descriptor(), result.iscc_nbs_color());
                println!("  Revised: {}", result.revised_descriptor());
            }
            Ok(None) => {
                println!("RGB {:?} ({}): No ISCC-NBS classification", rgb, expected_description);
            }
            Err(e) => {
                println!("RGB {:?} ({}): Error - {}", rgb, expected_description, e);
            }
        }
    }
}