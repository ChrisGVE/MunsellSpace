/// Comprehensive conversion dataset generator for all 260 colors
/// 
/// This script processes all 260 colors from MUNSELL_COLOR_SCIENCE_COMPLETE.csv and generates
/// a comprehensive comparison table showing:
/// 1. RGB hex values
/// 2. Expected ISCC-NBS names
/// 3. Actual Rust conversion to Munsell coordinates  
/// 4. Method 1 (IncludeStartExcludeEnd) classification result
/// 5. Method 2 (ExcludeStartIncludeEnd) classification result
/// 6. Match status for each method

use munsellspace::{MunsellConverter, ISCC_NBS_Classifier, HueRangeMethod, MunsellColor};
use std::fs::File;
use std::io::{BufRead, BufReader, Write};

/// Complete color analysis result for a single color
#[derive(Debug, Clone)]
struct ColorAnalysisResult {
    /// Color number from dataset
    number: u32,
    /// RGB values
    rgb: [u8; 3],
    /// RGB as hex string
    rgb_hex: String,
    /// Expected ISCC-NBS name from dataset
    expected_name: String,
    /// Munsell coordinates from conversion
    munsell_coordinates: Option<MunsellColor>,
    /// Method 1 classification result
    method1_result: Option<String>,
    /// Method 1 match status
    method1_match: bool,
    /// Method 2 classification result  
    method2_result: Option<String>,
    /// Method 2 match status
    method2_match: bool,
    /// Any error message from conversion or classification
    error_message: Option<String>,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🎨 Comprehensive Conversion Dataset Generator");
    println!("===========================================\n");
    
    // Initialize converters
    let munsell_converter = MunsellConverter::new()?;
    let method1_classifier = ISCC_NBS_Classifier::new_with_hue_range_method(HueRangeMethod::IncludeStartExcludeEnd)?;
    let method2_classifier = ISCC_NBS_Classifier::new_with_hue_range_method(HueRangeMethod::ExcludeStartIncludeEnd)?;
    
    println!("📊 Processing all 260 colors from complete dataset...");
    
    // Load and process dataset
    let dataset_path = "tests/data/MUNSELL_COLOR_SCIENCE_COMPLETE.csv";
    let file = File::open(dataset_path)?;
    let reader = BufReader::new(file);
    
    let mut results = Vec::new();
    let mut total_processed = 0;
    let mut method1_correct = 0;
    let mut method2_correct = 0;
    let mut conversion_failures = 0;
    
    for (line_num, line) in reader.lines().enumerate() {
        let line = line?;
        
        // Skip header line
        if line_num == 0 && line.starts_with("number,") {
            continue;
        }
        
        let parts: Vec<&str> = line.split(',').collect();
        if parts.len() < 5 {
            continue; // Skip invalid lines
        }
        
        // Parse CSV: number,name,r,g,b
        let number: u32 = parts[0].trim().parse().unwrap_or(0);
        let expected_name = parts[1].trim().trim_matches('"').to_string();
        let r: u8 = parts[2].trim().parse().unwrap_or(0);
        let g: u8 = parts[3].trim().parse().unwrap_or(0);
        let b: u8 = parts[4].trim().parse().unwrap_or(0);
        
        let rgb = [r, g, b];
        let rgb_hex = format!("#{:02X}{:02X}{:02X}", r, g, b);
        
        total_processed += 1;
        
        // Convert RGB to Munsell coordinates
        let munsell_result = munsell_converter.srgb_to_munsell(rgb);
        let munsell_coordinates = match munsell_result {
            Ok(color) => Some(color),
            Err(_) => {
                conversion_failures += 1;
                None
            }
        };
        
        // Test Method 1 classification
        let method1_result = match method1_classifier.classify_srgb(rgb) {
            Ok(Some(result)) => Some(result.full_iscc_nbs_name()),
            _ => None,
        };
        
        // Test Method 2 classification
        let method2_result = match method2_classifier.classify_srgb(rgb) {
            Ok(Some(result)) => Some(result.full_iscc_nbs_name()),
            _ => None,
        };
        
        // Check matches
        let method1_match = method1_result.as_ref()
            .map_or(false, |result| result.to_lowercase() == expected_name.to_lowercase());
        let method2_match = method2_result.as_ref()
            .map_or(false, |result| result.to_lowercase() == expected_name.to_lowercase());
            
        if method1_match { method1_correct += 1; }
        if method2_match { method2_correct += 1; }
        
        let error_message = if munsell_coordinates.is_none() {
            Some("RGB to Munsell conversion failed".to_string())
        } else if method1_result.is_none() && method2_result.is_none() {
            Some("Both classification methods failed".to_string())
        } else {
            None
        };
        
        results.push(ColorAnalysisResult {
            number,
            rgb,
            rgb_hex,
            expected_name,
            munsell_coordinates,
            method1_result,
            method1_match,
            method2_result,
            method2_match,
            error_message,
        });
        
        if total_processed % 50 == 0 {
            println!("   Processed {} colors...", total_processed);
        }
    }
    
    println!("\n📈 Processing Summary:");
    println!("  Total colors processed: {}", total_processed);
    println!("  Conversion failures: {}", conversion_failures);
    println!("  Method 1 accuracy: {} / {} ({:.2}%)", method1_correct, total_processed,
             (method1_correct as f64 / total_processed as f64) * 100.0);
    println!("  Method 2 accuracy: {} / {} ({:.2}%)", method2_correct, total_processed,
             (method2_correct as f64 / total_processed as f64) * 100.0);
    
    // Generate comprehensive dataset table
    generate_comprehensive_dataset_table(&results)?;
    
    // Generate analysis summary
    generate_analysis_summary(&results, method1_correct, method2_correct)?;
    
    println!("✅ Comprehensive conversion dataset generated!");
    println!("📄 Dataset saved as: COMPREHENSIVE_CONVERSION_DATASET.md");
    println!("📄 Analysis saved as: CONVERSION_ANALYSIS_SUMMARY.md");
    
    Ok(())
}

/// Generate the comprehensive dataset table with all color details
fn generate_comprehensive_dataset_table(results: &[ColorAnalysisResult]) -> Result<(), Box<dyn std::error::Error>> {
    let mut dataset = File::create("COMPREHENSIVE_CONVERSION_DATASET.md")?;
    
    writeln!(dataset, "# Comprehensive Conversion Dataset - All 260 Colors")?;
    writeln!(dataset)?;
    writeln!(dataset, "This dataset shows the complete analysis of all 260 colors from the MUNSELL_COLOR_SCIENCE_COMPLETE reference dataset.")?;
    writeln!(dataset, "Each color is tested with both hue range interpretation methods for ISCC-NBS classification.")?;
    writeln!(dataset)?;
    
    writeln!(dataset, "## Legend")?;
    writeln!(dataset)?;
    writeln!(dataset, "- **Method 1**: IncludeStartExcludeEnd hue range interpretation")?;
    writeln!(dataset, "- **Method 2**: ExcludeStartIncludeEnd hue range interpretation")?;
    writeln!(dataset, "- **✅**: Classification matches expected ISCC-NBS name")?;
    writeln!(dataset, "- **❌**: Classification does not match expected name")?;
    writeln!(dataset, "- **N/A**: Classification failed or conversion error")?;
    writeln!(dataset)?;
    
    writeln!(dataset, "## Complete Dataset Table")?;
    writeln!(dataset)?;
    writeln!(dataset, "| # | RGB Hex | Expected ISCC-NBS Name | Munsell Coordinates | Method 1 Result | M1 ✓ | Method 2 Result | M2 ✓ | Notes |")?;
    writeln!(dataset, "|---|---------|------------------------|--------------------|-----------------|----|-----------------|----|----|")?;
    
    for result in results {
        let munsell_coords = match &result.munsell_coordinates {
            Some(color) => color.notation.clone(),
            None => "FAILED".to_string(),
        };
        
        let method1_display = result.method1_result.as_deref().unwrap_or("N/A");
        let method2_display = result.method2_result.as_deref().unwrap_or("N/A");
        
        let method1_check = if result.method1_match { "✅" } else { "❌" };
        let method2_check = if result.method2_match { "✅" } else { "❌" };
        
        let notes = result.error_message.as_deref().unwrap_or("");
        
        writeln!(dataset, "| {} | {} | {} | {} | {} | {} | {} | {} | {} |",
                 result.number,
                 result.rgb_hex,
                 result.expected_name,
                 munsell_coords,
                 method1_display,
                 method1_check,
                 method2_display,
                 method2_check,
                 notes)?;
    }
    
    writeln!(dataset)?;
    writeln!(dataset, "---")?;
    writeln!(dataset, "Generated by MunsellSpace Comprehensive Conversion Dataset Tool")?;
    
    Ok(())
}

/// Generate analysis summary with statistics and insights
fn generate_analysis_summary(results: &[ColorAnalysisResult], method1_correct: usize, method2_correct: usize) -> Result<(), Box<dyn std::error::Error>> {
    let mut summary = File::create("CONVERSION_ANALYSIS_SUMMARY.md")?;
    
    writeln!(summary, "# Conversion Analysis Summary")?;
    writeln!(summary)?;
    writeln!(summary, "## Overall Performance Comparison")?;
    writeln!(summary)?;
    
    let total = results.len();
    let method1_accuracy = (method1_correct as f64 / total as f64) * 100.0;
    let method2_accuracy = (method2_correct as f64 / total as f64) * 100.0;
    let accuracy_difference = method2_accuracy - method1_accuracy;
    
    writeln!(summary, "| Method | Correct Classifications | Total Colors | Accuracy |")?;
    writeln!(summary, "|--------|-------------------------|-------------|----------|")?;
    writeln!(summary, "| Method 1 (IncludeStartExcludeEnd) | {} | {} | {:.2}% |", method1_correct, total, method1_accuracy)?;
    writeln!(summary, "| Method 2 (ExcludeStartIncludeEnd) | {} | {} | {:.2}% |", method2_correct, total, method2_accuracy)?;
    writeln!(summary)?;
    
    writeln!(summary, "**Performance Difference**: Method 2 is {:.3}% {} than Method 1", 
             accuracy_difference.abs(), 
             if accuracy_difference > 0.0 { "better" } else { "worse" })?;
    writeln!(summary)?;
    
    // Count conversion failures
    let conversion_failures = results.iter().filter(|r| r.munsell_coordinates.is_none()).count();
    let conversion_success_rate = ((total - conversion_failures) as f64 / total as f64) * 100.0;
    
    writeln!(summary, "## Conversion Statistics")?;
    writeln!(summary)?;
    writeln!(summary, "- **Total Colors**: {}", total)?;
    writeln!(summary, "- **Successful RGB→Munsell Conversions**: {} ({:.2}%)", total - conversion_failures, conversion_success_rate)?;
    writeln!(summary, "- **Failed Conversions**: {} ({:.2}%)", conversion_failures, 
             (conversion_failures as f64 / total as f64) * 100.0)?;
    writeln!(summary)?;
    
    // Analyze colors where both methods failed
    let both_failed = results.iter().filter(|r| !r.method1_match && !r.method2_match).count();
    let only_method1_correct = results.iter().filter(|r| r.method1_match && !r.method2_match).count();
    let only_method2_correct = results.iter().filter(|r| !r.method1_match && r.method2_match).count();
    let both_correct = results.iter().filter(|r| r.method1_match && r.method2_match).count();
    
    writeln!(summary, "## Classification Agreement Analysis")?;
    writeln!(summary)?;
    writeln!(summary, "- **Both methods correct**: {} colors ({:.2}%)", both_correct,
             (both_correct as f64 / total as f64) * 100.0)?;
    writeln!(summary, "- **Only Method 1 correct**: {} colors ({:.2}%)", only_method1_correct,
             (only_method1_correct as f64 / total as f64) * 100.0)?;
    writeln!(summary, "- **Only Method 2 correct**: {} colors ({:.2}%)", only_method2_correct,
             (only_method2_correct as f64 / total as f64) * 100.0)?;
    writeln!(summary, "- **Both methods incorrect**: {} colors ({:.2}%)", both_failed,
             (both_failed as f64 / total as f64) * 100.0)?;
    writeln!(summary)?;
    
    // Find problematic colors where both methods fail
    if both_failed > 0 {
        writeln!(summary, "## Colors Where Both Methods Failed")?;
        writeln!(summary)?;
        writeln!(summary, "These colors may indicate gaps in the ISCC-NBS polygon definitions or issues with the conversion:")?;
        writeln!(summary)?;
        writeln!(summary, "| RGB Hex | Expected Name | Munsell Coords | Method 1 Result | Method 2 Result |")?;
        writeln!(summary, "|---------|---------------|----------------|-----------------|-----------------|")?;
        
        for result in results.iter().filter(|r| !r.method1_match && !r.method2_match) {
            let munsell_coords = match &result.munsell_coordinates {
                Some(color) => color.notation.clone(),
                None => "FAILED".to_string(),
            };
            
            writeln!(summary, "| {} | {} | {} | {} | {} |",
                     result.rgb_hex,
                     result.expected_name,
                     munsell_coords,
                     result.method1_result.as_deref().unwrap_or("N/A"),
                     result.method2_result.as_deref().unwrap_or("N/A"))?;
        }
        writeln!(summary)?;
    }
    
    // Colors where methods disagree (one correct, one wrong)
    let disagreement_colors = only_method1_correct + only_method2_correct;
    if disagreement_colors > 0 {
        writeln!(summary, "## Colors Where Methods Disagree ({} colors)", disagreement_colors)?;
        writeln!(summary)?;
        writeln!(summary, "These colors show the difference between hue range interpretation methods:")?;
        writeln!(summary)?;
        writeln!(summary, "| RGB Hex | Expected Name | Munsell Coords | Method 1 Result | M1✓ | Method 2 Result | M2✓ |")?;
        writeln!(summary, "|---------|---------------|----------------|-----------------|-----|-----------------|-----|")?;
        
        for result in results.iter().filter(|r| r.method1_match != r.method2_match) {
            let munsell_coords = match &result.munsell_coordinates {
                Some(color) => color.notation.clone(),
                None => "FAILED".to_string(),
            };
            
            let m1_check = if result.method1_match { "✅" } else { "❌" };
            let m2_check = if result.method2_match { "✅" } else { "❌" };
            
            writeln!(summary, "| {} | {} | {} | {} | {} | {} | {} |",
                     result.rgb_hex,
                     result.expected_name,
                     munsell_coords,
                     result.method1_result.as_deref().unwrap_or("N/A"),
                     m1_check,
                     result.method2_result.as_deref().unwrap_or("N/A"),
                     m2_check)?;
        }
        writeln!(summary)?;
    }
    
    // Recommendations
    writeln!(summary, "## Recommendations")?;
    writeln!(summary)?;
    
    if method2_accuracy > method1_accuracy {
        writeln!(summary, "**Recommended Method**: Method 2 (ExcludeStartIncludeEnd)")?;
        writeln!(summary, "- Provides {:.3}% better accuracy", accuracy_difference)?;
        writeln!(summary, "- {} more colors classified correctly", method2_correct - method1_correct)?;
    } else if method1_accuracy > method2_accuracy {
        writeln!(summary, "**Recommended Method**: Method 1 (IncludeStartExcludeEnd)")?;
        writeln!(summary, "- Provides {:.3}% better accuracy", -accuracy_difference)?;
        writeln!(summary, "- {} more colors classified correctly", method1_correct - method2_correct)?;
    } else {
        writeln!(summary, "**Recommended Method**: Either method (equivalent performance)")?;
        writeln!(summary, "- Both methods provide identical {:.2}% accuracy", method1_accuracy)?;
    }
    
    if conversion_failures > 0 {
        writeln!(summary)?;
        writeln!(summary, "**Conversion Issues**: {} colors failed RGB→Munsell conversion", conversion_failures)?;
        writeln!(summary, "- This may indicate issues with the mathematical conversion algorithm")?;
        writeln!(summary, "- Consider investigating these specific colors for edge cases")?;
    }
    
    writeln!(summary)?;
    writeln!(summary, "---")?;
    writeln!(summary, "Analysis generated by MunsellSpace Comprehensive Conversion Dataset Tool")?;
    
    Ok(())
}