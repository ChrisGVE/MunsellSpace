/// Comprehensive hue range method comparison tool for ISCC-NBS classification
/// 
/// This script compares Method 1 vs Method 2 hue range interpretation for polygon
/// assignments to determine which provides better classification accuracy.

use munsellspace::{MunsellConverter, ISCC_NBS_Classifier, HueRangeMethod, MunsellColor};
use std::fs::File;
use std::io::{BufRead, BufReader, Write};
use std::collections::HashMap;

/// Represents the results of testing a single hue range method
#[derive(Debug, Clone)]
struct MethodTestResults {
    /// Method being tested
    method: HueRangeMethod,
    /// Total colors tested
    total_tests: usize,
    /// Number of successful classifications
    successful_classifications: usize,
    /// Accuracy percentage
    accuracy_percentage: f64,
    /// Classification failures with details
    failures: Vec<ClassificationFailure>,
    /// Error category distribution
    error_categories: HashMap<ErrorCategory, usize>,
}

/// Detailed classification failure information
#[derive(Debug, Clone)]
struct ClassificationFailure {
    rgb: [u8; 3],
    expected_name: String,
    actual_name: Option<String>,
    munsell_coordinates: Option<MunsellColor>,
    error_message: Option<String>,
    line_number: usize,
    error_category: ErrorCategory,
}

/// Error categories for classification failures
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
enum ErrorCategory {
    RedPurpleConfusion,
    BrownClassificationGaps,
    ModifierInconsistencies,
    HueFamilyError,
    ValueClassificationError,
    ChromaClassificationError,
    NoClassificationFound,
    ConversionError,
    Other,
}

impl ErrorCategory {
    /// Categorize a failure based on expected and actual names
    fn categorize_failure(expected: &str, actual: &Option<String>) -> Self {
        let expected_lower = expected.to_lowercase();
        
        match actual {
            None => ErrorCategory::NoClassificationFound,
            Some(actual_name) => {
                let actual_lower = actual_name.to_lowercase();
                
                // Red/Purple confusion patterns
                if (expected_lower.contains("red") && actual_lower.contains("purple")) ||
                   (expected_lower.contains("purple") && actual_lower.contains("red")) {
                    return ErrorCategory::RedPurpleConfusion;
                }
                
                // Brown classification gaps
                if expected_lower.contains("brown") && !actual_lower.contains("brown") {
                    return ErrorCategory::BrownClassificationGaps;
                }
                
                // Modifier inconsistencies
                if Self::has_modifier_inconsistency(&expected_lower, &actual_lower) {
                    return ErrorCategory::ModifierInconsistencies;
                }
                
                // Hue family errors
                if Self::has_hue_family_error(&expected_lower, &actual_lower) {
                    return ErrorCategory::HueFamilyError;
                }
                
                // Value classification errors
                if Self::has_value_error(&expected_lower, &actual_lower) {
                    return ErrorCategory::ValueClassificationError;
                }
                
                // Chroma classification errors
                if Self::has_chroma_error(&expected_lower, &actual_lower) {
                    return ErrorCategory::ChromaClassificationError;
                }
                
                ErrorCategory::Other
            }
        }
    }
    
    fn has_modifier_inconsistency(expected: &str, actual: &str) -> bool {
        let modifiers = ["ish", "very", "deep", "light", "dark", "pale", "grayish", "vivid", "strong", "moderate"];
        
        for modifier in &modifiers {
            let exp_has = expected.contains(modifier);
            let act_has = actual.contains(modifier);
            if exp_has != act_has {
                return true;
            }
        }
        false
    }
    
    fn has_hue_family_error(expected: &str, actual: &str) -> bool {
        let hue_families = ["red", "yellow", "green", "blue", "purple", "pink", "orange", "brown"];
        
        for family in &hue_families {
            let exp_has = expected.contains(family);
            let act_has = actual.contains(family);
            if exp_has && !act_has {
                return true;
            }
        }
        false
    }
    
    fn has_value_error(expected: &str, actual: &str) -> bool {
        let value_modifiers = ["light", "dark", "very dark", "very light", "blackish"];
        
        for modifier in &value_modifiers {
            let exp_has = expected.contains(modifier);
            let act_has = actual.contains(modifier);
            if exp_has != act_has {
                return true;
            }
        }
        false
    }
    
    fn has_chroma_error(expected: &str, actual: &str) -> bool {
        let chroma_modifiers = ["vivid", "strong", "moderate", "grayish", "pale"];
        
        for modifier in &chroma_modifiers {
            let exp_has = expected.contains(modifier);
            let act_has = actual.contains(modifier);
            if exp_has != act_has {
                return true;
            }
        }
        false
    }
    
    fn description(&self) -> &'static str {
        match self {
            ErrorCategory::RedPurpleConfusion => "Red/Purple Confusion",
            ErrorCategory::BrownClassificationGaps => "Brown Classification Gaps",
            ErrorCategory::ModifierInconsistencies => "Modifier Inconsistencies",
            ErrorCategory::HueFamilyError => "Hue Family Errors",
            ErrorCategory::ValueClassificationError => "Value Classification Errors",
            ErrorCategory::ChromaClassificationError => "Chroma Classification Errors",
            ErrorCategory::NoClassificationFound => "No Classification Found",
            ErrorCategory::ConversionError => "RGB->Munsell Conversion Error",
            ErrorCategory::Other => "Other Classification Errors",
        }
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🎨 Hue Range Method Comparison for ISCC-NBS Classification");
    println!("========================================================\n");
    
    // Test both methods
    println!("📊 Testing Method 1: IncludeStartExcludeEnd...");
    let method1_results = test_hue_range_method(HueRangeMethod::IncludeStartExcludeEnd)?;
    
    println!("📊 Testing Method 2: ExcludeStartIncludeEnd...");
    let method2_results = test_hue_range_method(HueRangeMethod::ExcludeStartIncludeEnd)?;
    
    // Generate comparison report
    generate_comparison_report(&method1_results, &method2_results)?;
    
    // Determine and display the recommended method
    let recommended_method = determine_best_method(&method1_results, &method2_results);
    display_recommendation(&recommended_method, &method1_results, &method2_results);
    
    println!("✅ Hue range method comparison completed!");
    println!("📄 Detailed report saved as: HRUE_RANGE_METHOD_COMPARISON.md");
    
    Ok(())
}

/// Test a specific hue range method and return detailed results
fn test_hue_range_method(method: HueRangeMethod) -> Result<MethodTestResults, Box<dyn std::error::Error>> {
    println!("   Creating classifier with {:?}...", method);
    
    // Initialize converters with the specified method
    let munsell_converter = MunsellConverter::new()?;
    let iscc_classifier = ISCC_NBS_Classifier::new_with_hue_range_method(method)?;
    
    // Load test dataset
    let dataset_path = "tests/data/MUNSELL_COLOR_SCIENCE_COMPLETE.csv";
    let file = File::open(dataset_path)?;
    let reader = BufReader::new(file);
    
    let mut total_tests = 0;
    let mut successful_classifications = 0;
    let mut failures = Vec::new();
    let mut error_categories: HashMap<ErrorCategory, usize> = HashMap::new();
    
    println!("   Processing test dataset...");
    
    for (line_num, line) in reader.lines().enumerate() {
        let line = line?;
        
        // Skip header line
        if line_num == 0 && line.starts_with("number,") {
            continue;
        }
        
        let parts: Vec<&str> = line.split(',').collect();
        if parts.len() < 4 {
            continue; // Skip invalid lines
        }
        
        // Parse CSV: number,name,r,g,b
        let expected_name = parts[1].trim().trim_matches('"').to_string();
        let r: u8 = parts[2].trim().parse().unwrap_or(0);
        let g: u8 = parts[3].trim().parse().unwrap_or(0);
        let b: u8 = parts[4].trim().parse().unwrap_or(0);
        
        let rgb = [r, g, b];
        total_tests += 1;
        
        // Convert RGB to Munsell coordinates
        let munsell_result = munsell_converter.srgb_to_munsell(rgb);
        
        let munsell_color = match munsell_result {
            Ok(color) => Some(color),
            Err(e) => {
                let category = ErrorCategory::ConversionError;
                *error_categories.entry(category.clone()).or_insert(0) += 1;
                failures.push(ClassificationFailure {
                    rgb,
                    expected_name: expected_name.clone(),
                    actual_name: None,
                    munsell_coordinates: None,
                    error_message: Some(format!("Munsell conversion failed: {}", e)),
                    line_number: line_num + 1,
                    error_category: category,
                });
                continue;
            }
        };
        
        // Classify using ISCC-NBS
        let classification_result = iscc_classifier.classify_srgb(rgb);
        
        match classification_result {
            Ok(Some(result)) => {
                let actual_name = result.full_iscc_nbs_name();
                
                if actual_name.to_lowercase() == expected_name.to_lowercase() {
                    successful_classifications += 1;
                } else {
                    let category = ErrorCategory::categorize_failure(&expected_name, &Some(actual_name.clone()));
                    *error_categories.entry(category.clone()).or_insert(0) += 1;
                    failures.push(ClassificationFailure {
                        rgb,
                        expected_name: expected_name.clone(),
                        actual_name: Some(actual_name),
                        munsell_coordinates: munsell_color,
                        error_message: None,
                        line_number: line_num + 1,
                        error_category: category,
                    });
                }
            }
            Ok(None) => {
                let category = ErrorCategory::NoClassificationFound;
                *error_categories.entry(category.clone()).or_insert(0) += 1;
                failures.push(ClassificationFailure {
                    rgb,
                    expected_name: expected_name.clone(),
                    actual_name: None,
                    munsell_coordinates: munsell_color,
                    error_message: Some("No ISCC-NBS classification found".to_string()),
                    line_number: line_num + 1,
                    error_category: category,
                });
            }
            Err(e) => {
                let category = ErrorCategory::ConversionError;
                *error_categories.entry(category.clone()).or_insert(0) += 1;
                failures.push(ClassificationFailure {
                    rgb,
                    expected_name: expected_name.clone(),
                    actual_name: None,
                    munsell_coordinates: munsell_color,
                    error_message: Some(format!("Classification error: {}", e)),
                    line_number: line_num + 1,
                    error_category: category,
                });
            }
        }
    }
    
    let accuracy_percentage = (successful_classifications as f64 / total_tests as f64) * 100.0;
    
    println!("   Results: {}/{} correct ({:.2}%)", successful_classifications, total_tests, accuracy_percentage);
    
    Ok(MethodTestResults {
        method,
        total_tests,
        successful_classifications,
        accuracy_percentage,
        failures,
        error_categories,
    })
}

/// Generate comprehensive comparison report
fn generate_comparison_report(method1: &MethodTestResults, method2: &MethodTestResults) -> Result<(), Box<dyn std::error::Error>> {
    let mut report = File::create("HUE_RANGE_METHOD_COMPARISON.md")?;
    
    writeln!(report, "# Hue Range Method Comparison Report")?;
    writeln!(report)?;
    writeln!(report, "## Overview")?;
    writeln!(report)?;
    writeln!(report, "This report compares two different hue range interpretation methods for ISCC-NBS polygon assignments:")?;
    writeln!(report)?;
    writeln!(report, "- **Method 1 (IncludeStartExcludeEnd)**: Includes starting boundary, excludes ending boundary")?;
    writeln!(report, "  - Example: \"8R-2YR\" → [8R, 9R, 10R, 1YR]")?;
    writeln!(report, "- **Method 2 (ExcludeStartIncludeEnd)**: Excludes starting boundary, includes ending boundary")?;
    writeln!(report, "  - Example: \"8R-2YR\" → [9R, 10R, 1YR, 2YR]")?;
    writeln!(report)?;
    
    // Overall accuracy comparison
    writeln!(report, "## Overall Accuracy Comparison")?;
    writeln!(report)?;
    writeln!(report, "| Method | Total Tests | Correct Classifications | Accuracy | Failed Classifications |")?;
    writeln!(report, "|--------|-------------|------------------------|----------|----------------------|")?;
    writeln!(report, "| Method 1 (IncludeStartExcludeEnd) | {} | {} | {:.2}% | {} |", 
             method1.total_tests, method1.successful_classifications, method1.accuracy_percentage, method1.failures.len())?;
    writeln!(report, "| Method 2 (ExcludeStartIncludeEnd) | {} | {} | {:.2}% | {} |", 
             method2.total_tests, method2.successful_classifications, method2.accuracy_percentage, method2.failures.len())?;
    writeln!(report)?;
    
    // Accuracy difference analysis
    let accuracy_diff = method2.accuracy_percentage - method1.accuracy_percentage;
    let classification_diff = method2.successful_classifications as i32 - method1.successful_classifications as i32;
    
    writeln!(report, "**Accuracy Difference**: Method 2 is {:.3}% {} than Method 1", 
             accuracy_diff.abs(), if accuracy_diff > 0.0 { "better" } else { "worse" })?;
    writeln!(report, "**Classification Difference**: Method 2 has {} {} correct classifications", 
             classification_diff.abs(), if classification_diff > 0 { "more" } else { "fewer" })?;
    writeln!(report)?;
    
    // Error category comparison
    writeln!(report, "## Error Category Comparison")?;
    writeln!(report)?;
    
    // Get all error categories from both methods
    let mut all_categories: std::collections::HashSet<ErrorCategory> = std::collections::HashSet::new();
    all_categories.extend(method1.error_categories.keys().cloned());
    all_categories.extend(method2.error_categories.keys().cloned());
    
    writeln!(report, "| Error Category | Method 1 Count | Method 1 % | Method 2 Count | Method 2 % | Difference |")?;
    writeln!(report, "|----------------|----------------|------------|----------------|------------|------------|")?;
    
    for category in &all_categories {
        let method1_count = method1.error_categories.get(category).unwrap_or(&0);
        let method2_count = method2.error_categories.get(category).unwrap_or(&0);
        let method1_pct = (*method1_count as f64 / method1.total_tests as f64) * 100.0;
        let method2_pct = (*method2_count as f64 / method2.total_tests as f64) * 100.0;
        let diff = *method2_count as i32 - *method1_count as i32;
        
        writeln!(report, "| {} | {} | {:.2}% | {} | {:.2}% | {} |", 
                 category.description(), method1_count, method1_pct, 
                 method2_count, method2_pct, 
                 if diff > 0 { format!("+{}", diff) } else { diff.to_string() })?;
    }
    writeln!(report)?;
    
    // Detailed analysis for each method
    write_method_details(&mut report, "Method 1 (IncludeStartExcludeEnd)", method1)?;
    write_method_details(&mut report, "Method 2 (ExcludeStartIncludeEnd)", method2)?;
    
    // Recommendations
    writeln!(report, "## Recommendations")?;
    writeln!(report)?;
    
    if method2.accuracy_percentage > method1.accuracy_percentage {
        writeln!(report, "**Recommended Method**: Method 2 (ExcludeStartIncludeEnd)")?;
        writeln!(report, "**Rationale**: Method 2 provides {:.3}% better accuracy with {} fewer classification failures.", 
                 accuracy_diff, method1.failures.len() as i32 - method2.failures.len() as i32)?;
    } else if method1.accuracy_percentage > method2.accuracy_percentage {
        writeln!(report, "**Recommended Method**: Method 1 (IncludeStartExcludeEnd)")?;
        writeln!(report, "**Rationale**: Method 1 provides {:.3}% better accuracy with {} fewer classification failures.", 
                 -accuracy_diff, method2.failures.len() as i32 - method1.failures.len() as i32)?;
    } else {
        writeln!(report, "**Recommended Method**: Either method (equivalent performance)")?;
        writeln!(report, "**Rationale**: Both methods provide identical accuracy ({:.2}%).", method1.accuracy_percentage)?;
    }
    writeln!(report)?;
    
    writeln!(report, "---")?;
    writeln!(report, "Report generated by MunsellSpace Hue Range Method Comparison Tool")?;
    
    Ok(())
}

/// Write detailed analysis for a specific method
fn write_method_details(report: &mut File, title: &str, results: &MethodTestResults) -> Result<(), Box<dyn std::error::Error>> {
    writeln!(report, "## {} - Detailed Analysis", title)?;
    writeln!(report)?;
    writeln!(report, "**Total Tests**: {}", results.total_tests)?;
    writeln!(report, "**Successful Classifications**: {} ({:.2}%)", results.successful_classifications, results.accuracy_percentage)?;
    writeln!(report, "**Failed Classifications**: {} ({:.2}%)", results.failures.len(), 
             (results.failures.len() as f64 / results.total_tests as f64) * 100.0)?;
    writeln!(report)?;
    
    if !results.failures.is_empty() {
        writeln!(report, "### Top 10 Classification Failures")?;
        writeln!(report)?;
        writeln!(report, "| RGB | Expected Name | Actual Name | Error Category | Munsell Coords |")?;
        writeln!(report, "|-----|---------------|-------------|----------------|----------------|")?;
        
        for (i, failure) in results.failures.iter().take(10).enumerate() {
            let munsell_coords = match &failure.munsell_coordinates {
                Some(color) => color.notation.clone(),
                None => "N/A".to_string(),
            };
            let actual_name = failure.actual_name.as_deref().unwrap_or("None");
            
            writeln!(report, "| #{:02X}{:02X}{:02X} | {} | {} | {} | {} |",
                     failure.rgb[0], failure.rgb[1], failure.rgb[2],
                     failure.expected_name,
                     actual_name,
                     failure.error_category.description(),
                     munsell_coords)?;
        }
        writeln!(report)?;
    }
    
    Ok(())
}

/// Determine which method provides better performance
fn determine_best_method(method1: &MethodTestResults, method2: &MethodTestResults) -> HueRangeMethod {
    if method2.accuracy_percentage > method1.accuracy_percentage {
        method2.method
    } else if method1.accuracy_percentage > method2.accuracy_percentage {
        method1.method
    } else {
        // If equal accuracy, prefer the one with fewer "No Classification Found" errors
        let method1_no_class = method1.error_categories.get(&ErrorCategory::NoClassificationFound).unwrap_or(&0);
        let method2_no_class = method2.error_categories.get(&ErrorCategory::NoClassificationFound).unwrap_or(&0);
        
        if method2_no_class < method1_no_class {
            method2.method
        } else {
            method1.method
        }
    }
}

/// Display final recommendation
fn display_recommendation(recommended: &HueRangeMethod, method1: &MethodTestResults, method2: &MethodTestResults) {
    println!("\n🏆 Final Recommendation");
    println!("========================");
    
    match recommended {
        HueRangeMethod::IncludeStartExcludeEnd => {
            println!("**Recommended Method**: Method 1 (IncludeStartExcludeEnd)");
            println!("**Accuracy**: {:.2}% ({}/{} correct)", method1.accuracy_percentage, method1.successful_classifications, method1.total_tests);
            println!("**Advantage over Method 2**: {:.3}% better accuracy", 
                     method1.accuracy_percentage - method2.accuracy_percentage);
        }
        HueRangeMethod::ExcludeStartIncludeEnd => {
            println!("**Recommended Method**: Method 2 (ExcludeStartIncludeEnd)");
            println!("**Accuracy**: {:.2}% ({}/{} correct)", method2.accuracy_percentage, method2.successful_classifications, method2.total_tests);
            println!("**Advantage over Method 1**: {:.3}% better accuracy", 
                     method2.accuracy_percentage - method1.accuracy_percentage);
        }
    }
    println!();
}