/// Comprehensive ISCC-NBS classification accuracy analysis tool
/// 
/// This script tests the MunsellSpace library's ISCC-NBS color classification accuracy
/// against the reference dataset and generates detailed error analysis.

use munsellspace::{MunsellConverter, ISCC_NBS_Classifier, MunsellColor};
use std::fs::File;
use std::io::{BufRead, BufReader, Write};
use std::collections::HashMap;

/// Represents a classification failure with complete details
#[derive(Debug, Clone)]
struct ClassificationFailure {
    /// The RGB values that failed
    rgb: [u8; 3],
    /// Expected ISCC-NBS name from reference dataset
    expected_name: String,
    /// Actual ISCC-NBS name from classification (if any)
    actual_name: Option<String>,
    /// Converted Munsell coordinates
    munsell_coordinates: Option<MunsellColor>,
    /// Error message if conversion failed
    error_message: Option<String>,
    /// Line number in the test dataset
    line_number: usize,
}

/// Error category for classification failures
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
enum ErrorCategory {
    /// Confusion between red and purple colors
    RedPurpleConfusion,
    /// Classification gaps in brown color regions  
    BrownClassificationGaps,
    /// Inconsistent modifier handling
    ModifierInconsistencies,
    /// Hue family misclassification
    HueFamilyError,
    /// Value/lightness classification errors
    ValueClassificationError,
    /// Chroma/saturation classification errors  
    ChromaClassificationError,
    /// Complete classification failure (no result)
    NoClassificationFound,
    /// Conversion error (RGB->Munsell failed)
    ConversionError,
    /// Unclassified error type
    Other,
}

impl ErrorCategory {
    /// Categorize a failure based on the expected and actual names
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
                
                // Value classification errors (light/dark modifiers)
                if Self::has_value_error(&expected_lower, &actual_lower) {
                    return ErrorCategory::ValueClassificationError;
                }
                
                // Chroma classification errors (vivid/grayish/pale modifiers)
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
                return true; // Expected a hue family but didn't get it
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

/// Statistics for an error category
#[derive(Debug, Clone)]
struct CategoryStats {
    count: usize,
    percentage: f64,
    examples: Vec<ClassificationFailure>,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🎨 MunsellSpace ISCC-NBS Classification Accuracy Analysis");
    println!("========================================================\n");
    
    // Initialize converters
    let munsell_converter = MunsellConverter::new()?;
    let iscc_classifier = ISCC_NBS_Classifier::new()?;
    
    // Load test dataset
    let dataset_path = "tests/data/MUNSELL_COLOR_SCIENCE_COMPLETE.csv";
    let file = File::open(dataset_path)?;
    let reader = BufReader::new(file);
    
    let mut total_tests = 0;
    let mut successful_classifications = 0;
    let mut failures = Vec::new();
    
    println!("📊 Running classification accuracy test...\n");
    
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
        let _number: u32 = parts[0].trim().parse().unwrap_or(0);
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
                failures.push(ClassificationFailure {
                    rgb,
                    expected_name: expected_name.clone(),
                    actual_name: None,
                    munsell_coordinates: None,
                    error_message: Some(format!("Munsell conversion failed: {}", e)),
                    line_number: line_num + 1,
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
                    failures.push(ClassificationFailure {
                        rgb,
                        expected_name: expected_name.clone(),
                        actual_name: Some(actual_name),
                        munsell_coordinates: munsell_color,
                        error_message: None,
                        line_number: line_num + 1,
                    });
                }
            }
            Ok(None) => {
                failures.push(ClassificationFailure {
                    rgb,
                    expected_name: expected_name.clone(),
                    actual_name: None,
                    munsell_coordinates: munsell_color,
                    error_message: Some("No ISCC-NBS classification found".to_string()),
                    line_number: line_num + 1,
                });
            }
            Err(e) => {
                failures.push(ClassificationFailure {
                    rgb,
                    expected_name: expected_name.clone(),
                    actual_name: None,
                    munsell_coordinates: munsell_color,
                    error_message: Some(format!("Classification error: {}", e)),
                    line_number: line_num + 1,
                });
            }
        }
    }
    
    // Calculate accuracy statistics
    let accuracy_percentage = (successful_classifications as f64 / total_tests as f64) * 100.0;
    let failure_percentage = (failures.len() as f64 / total_tests as f64) * 100.0;
    
    println!("📈 Overall Classification Results:");
    println!("  Total colors tested: {}", total_tests);
    println!("  Successful classifications: {} ({:.2}%)", successful_classifications, accuracy_percentage);
    println!("  Failed classifications: {} ({:.2}%)", failures.len(), failure_percentage);
    println!();
    
    // Categorize failures
    let mut category_counts: HashMap<ErrorCategory, Vec<ClassificationFailure>> = HashMap::new();
    
    for failure in &failures {
        let category = ErrorCategory::categorize_failure(&failure.expected_name, &failure.actual_name);
        category_counts.entry(category).or_insert_with(Vec::new).push(failure.clone());
    }
    
    // Calculate category statistics
    let mut category_stats: HashMap<ErrorCategory, CategoryStats> = HashMap::new();
    for (category, failures_in_category) in &category_counts {
        let count = failures_in_category.len();
        let percentage = (count as f64 / total_tests as f64) * 100.0;
        let examples: Vec<ClassificationFailure> = failures_in_category.iter()
            .take(5) // Take first 5 examples
            .cloned()
            .collect();
            
        category_stats.insert(category.clone(), CategoryStats {
            count,
            percentage,
            examples,
        });
    }
    
    // Generate comprehensive report
    generate_error_analysis_report(&category_stats, &failures, total_tests)?;
    
    println!("✅ Error analysis report generated: CLASSIFICATION_ERRORS_REPORT.md");
    
    Ok(())
}

/// Generate comprehensive error analysis report
fn generate_error_analysis_report(
    category_stats: &HashMap<ErrorCategory, CategoryStats>,
    all_failures: &[ClassificationFailure], 
    total_tests: usize
) -> Result<(), Box<dyn std::error::Error>> {
    let mut report = File::create("CLASSIFICATION_ERRORS_REPORT.md")?;
    
    writeln!(report, "# ISCC-NBS Classification Error Analysis Report")?;
    writeln!(report)?;
    writeln!(report, "## Overview")?;
    writeln!(report)?;
    writeln!(report, "This report analyzes classification failures in the MunsellSpace library's ISCC-NBS color naming system.")?;
    writeln!(report, "The analysis is based on the complete MUNSELL_COLOR_SCIENCE dataset containing {} reference colors.", total_tests)?;
    writeln!(report)?;
    
    let accuracy = ((total_tests - all_failures.len()) as f64 / total_tests as f64) * 100.0;
    writeln!(report, "**Overall Accuracy**: {:.2}% ({}/{} colors classified correctly)", 
             accuracy, total_tests - all_failures.len(), total_tests)?;
    writeln!(report, "**Total Failures**: {} colors ({:.2}%)", all_failures.len(), 
             (all_failures.len() as f64 / total_tests as f64) * 100.0)?;
    writeln!(report)?;
    
    // Error category summary
    writeln!(report, "## Error Categories Summary")?;
    writeln!(report)?;
    writeln!(report, "| Category | Count | Percentage | Description |")?;
    writeln!(report, "|----------|-------|------------|-------------|")?;
    
    let mut sorted_categories: Vec<_> = category_stats.iter().collect();
    sorted_categories.sort_by(|a, b| b.1.count.cmp(&a.1.count));
    
    for (category, stats) in &sorted_categories {
        writeln!(report, "| {} | {} | {:.2}% | {} |", 
                 category.description(), stats.count, stats.percentage, category.description())?;
    }
    writeln!(report)?;
    
    // Detailed analysis for each category
    writeln!(report, "## Detailed Error Analysis")?;
    writeln!(report)?;
    
    for (category, stats) in &sorted_categories {
        writeln!(report, "### {}", category.description())?;
        writeln!(report)?;
        writeln!(report, "**Count**: {} failures ({:.2}% of total tests)", stats.count, stats.percentage)?;
        writeln!(report)?;
        
        if !stats.examples.is_empty() {
            writeln!(report, "**Examples**:")?;
            writeln!(report)?;
            writeln!(report, "| RGB | Expected Name | Actual Name | Munsell Coordinates | Line |")?;
            writeln!(report, "|-----|---------------|-------------|-------------------|------|")?;
            
            for example in &stats.examples {
                let munsell_coords = match &example.munsell_coordinates {
                    Some(color) => color.notation.clone(),
                    None => "Conversion failed".to_string(),
                };
                
                let actual_name = example.actual_name.as_deref().unwrap_or("No classification");
                
                writeln!(report, "| #{:02X}{:02X}{:02X} | {} | {} | {} | {} |",
                         example.rgb[0], example.rgb[1], example.rgb[2],
                         example.expected_name,
                         actual_name,
                         munsell_coords,
                         example.line_number)?;
            }
            writeln!(report)?;
            
            // Analysis of patterns for this category
            writeln!(report, "**Pattern Analysis**:")?;
            analyze_category_patterns(category, stats, &mut report)?;
            writeln!(report)?;
        }
    }
    
    // Complete failure list
    writeln!(report, "## Complete Failure List")?;
    writeln!(report)?;
    writeln!(report, "All {} classification failures with complete details:", all_failures.len())?;
    writeln!(report)?;
    writeln!(report, "| # | RGB | Expected | Actual | Munsell | Error | Category |")?;
    writeln!(report, "|---|-----|----------|--------|---------|--------|----------|")?;
    
    for (i, failure) in all_failures.iter().enumerate() {
        let munsell_coords = match &failure.munsell_coordinates {
            Some(color) => color.notation.clone(),
            None => "Failed".to_string(),
        };
        
        let actual_name = failure.actual_name.as_deref().unwrap_or("None");
        let error_msg = failure.error_message.as_deref().unwrap_or("Classification mismatch");
        let category = ErrorCategory::categorize_failure(&failure.expected_name, &failure.actual_name);
        
        writeln!(report, "| {} | #{:02X}{:02X}{:02X} | {} | {} | {} | {} | {} |",
                 i + 1, failure.rgb[0], failure.rgb[1], failure.rgb[2],
                 failure.expected_name, actual_name, munsell_coords,
                 error_msg, category.description())?;
    }
    
    writeln!(report)?;
    writeln!(report, "## Recommendations")?;
    writeln!(report)?;
    
    // Generate recommendations based on error patterns
    for (category, stats) in &sorted_categories {
        if stats.count > 5 { // Only recommend for significant categories
            writeln!(report, "### {} ({} failures)", category.description(), stats.count)?;
            generate_category_recommendations(category, &mut report)?;
            writeln!(report)?;
        }
    }
    
    writeln!(report, "---")?;
    writeln!(report, "Report generated by MunsellSpace Classification Accuracy Analysis Tool")?;
    
    Ok(())
}

/// Analyze patterns within a specific error category
fn analyze_category_patterns(
    category: &ErrorCategory,
    stats: &CategoryStats,
    report: &mut File
) -> Result<(), Box<dyn std::error::Error>> {
    match category {
        ErrorCategory::RedPurpleConfusion => {
            writeln!(report, "- Common in colors at hue boundary between red and purple families")?;
            writeln!(report, "- May indicate incorrect hue boundary definitions in ISCC-NBS polygons")?;
        }
        ErrorCategory::BrownClassificationGaps => {
            writeln!(report, "- Brown colors often misclassified as orange, red, or yellow")?;
            writeln!(report, "- Suggests insufficient brown polygon coverage in certain value/chroma ranges")?;
        }
        ErrorCategory::ModifierInconsistencies => {
            writeln!(report, "- Inconsistent handling of modifiers like 'vivid', 'deep', 'grayish'")?;
            writeln!(report, "- May indicate incorrect polygon boundaries or modifier logic")?;
        }
        ErrorCategory::NoClassificationFound => {
            writeln!(report, "- Colors fall outside all defined ISCC-NBS polygon regions")?;
            writeln!(report, "- Indicates gaps in color space coverage")?;
        }
        _ => {
            writeln!(report, "- Requires further investigation to identify specific patterns")?;
        }
    }
    
    Ok(())
}

/// Generate recommendations for fixing specific error categories
fn generate_category_recommendations(
    category: &ErrorCategory,
    report: &mut File
) -> Result<(), Box<dyn std::error::Error>> {
    match category {
        ErrorCategory::RedPurpleConfusion => {
            writeln!(report, "1. Review hue boundary definitions between R, RP, and P families")?;
            writeln!(report, "2. Check polygon overlap at red-purple transition zones")?;
            writeln!(report, "3. Verify mechanical wedge system hue angle calculations")?;
        }
        ErrorCategory::BrownClassificationGaps => {
            writeln!(report, "1. Expand brown polygon coverage in low-chroma, medium-value regions")?;
            writeln!(report, "2. Review brown vs orange/yellow boundary definitions")?;
            writeln!(report, "3. Add more brown polygon regions for comprehensive coverage")?;
        }
        ErrorCategory::ModifierInconsistencies => {
            writeln!(report, "1. Standardize modifier application logic")?;
            writeln!(report, "2. Review value/chroma thresholds for modifiers like 'vivid', 'deep'")?;
            writeln!(report, "3. Ensure consistent polygon boundary rules")?;
        }
        ErrorCategory::NoClassificationFound => {
            writeln!(report, "1. Identify gaps in ISCC-NBS color space coverage")?;
            writeln!(report, "2. Add missing polygon regions for unclassified colors")?;
            writeln!(report, "3. Review if gaps are intentional or require new definitions")?;
        }
        _ => {
            writeln!(report, "1. Investigate specific failure patterns")?;
            writeln!(report, "2. Review relevant polygon definitions and boundaries")?;
            writeln!(report, "3. Consider algorithm improvements for this category")?;
        }
    }
    
    Ok(())
}