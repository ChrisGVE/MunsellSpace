use munsellspace::IsccNbsClassifier;
use std::collections::HashMap;

#[test]
fn test_hue_wedge_distribution_analysis() {
    println!("=== HUE WEDGE DISTRIBUTION ANALYSIS ===");
    println!("Analyzing how ISCC-NBS polygons are distributed across adjacent hue planes");
    println!();
    
    let classifier = IsccNbsClassifier::new().expect("Failed to create classifier");
    
    // Test a comprehensive set of Munsell hues to understand wedge coverage
    let test_hues = vec![
        // Red family
        "1R", "2R", "3R", "4R", "5R", "6R", "7R", "8R", "9R", "10R",
        // Yellow-Red family  
        "1YR", "2YR", "3YR", "4YR", "5YR", "6YR", "7YR", "8YR", "9YR", "10YR",
        // Yellow family
        "1Y", "2Y", "3Y", "4Y", "5Y", "6Y", "7Y", "8Y", "9Y", "10Y",
        // Green-Yellow family
        "1GY", "2GY", "3GY", "4GY", "5GY", "6GY", "7GY", "8GY", "9GY", "10GY",
        // Green family
        "1G", "2G", "3G", "4G", "5G", "6G", "7G", "8G", "9G", "10G",
        // Blue-Green family
        "1BG", "2BG", "3BG", "4BG", "5BG", "6BG", "7BG", "8BG", "9BG", "10BG",
        // Blue family
        "1B", "2B", "3B", "4B", "5B", "6B", "7B", "8B", "9B", "10B",
        // Purple-Blue family
        "1PB", "2PB", "3PB", "4PB", "5PB", "6PB", "7PB", "8PB", "9PB", "10PB",
        // Purple family
        "1P", "2P", "3P", "4P", "5P", "6P", "7P", "8P", "9P", "10P",
        // Red-Purple family
        "1RP", "2RP", "3RP", "4RP", "5RP", "6RP", "7RP", "8RP", "9RP", "10RP",
    ];
    
    // Test various value/chroma combinations
    let test_values = vec![1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0];
    let test_chromas = vec![1.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0];
    
    let mut hue_family_stats: HashMap<String, HueFamilyStats> = HashMap::new();
    let mut total_tests = 0;
    let mut total_found = 0;
    
    println!("Testing coverage across all hue families...");
    
    for hue in &test_hues {
        let family = extract_hue_family(hue);
        let stats = hue_family_stats.entry(family.clone()).or_insert_with(|| HueFamilyStats::new(&family));
        
        for &value in &test_values {
            for &chroma in &test_chromas {
                total_tests += 1;
                
                match classifier.classify_munsell(hue, value, chroma) {
                    Ok(Some(_result)) => {
                        stats.found += 1;
                        total_found += 1;
                    }
                    Ok(None) => {
                        stats.not_found += 1;
                        stats.missing_points.push(format!("{} {:.1}/{:.1}", hue, value, chroma));
                    }
                    Err(_) => {
                        stats.errors += 1;
                    }
                }
                stats.total += 1;
            }
        }
    }
    
    println!();
    println!("=== HUE FAMILY COVERAGE ANALYSIS ===");
    
    // Sort families for consistent output
    let mut families: Vec<_> = hue_family_stats.keys().collect();
    families.sort();
    
    for family in families {
        let stats = &hue_family_stats[family];
        let coverage_pct = (stats.found as f64 / stats.total as f64) * 100.0;
        
        println!("{}:", family);
        println!("  Coverage: {}/{} ({:.1}%)", stats.found, stats.total, coverage_pct);
        println!("  Not found: {} ({:.1}%)", stats.not_found, (stats.not_found as f64 / stats.total as f64) * 100.0);
        println!("  Errors: {}", stats.errors);
        
        if coverage_pct < 50.0 {
            println!("  ❌ POOR COVERAGE - Potential wedge distribution issue");
            // Show some missing points for analysis
            println!("  Sample missing points:");
            for point in stats.missing_points.iter().take(3) {
                println!("    - {}", point);
            }
        } else if coverage_pct < 80.0 {
            println!("  ⚠️  MODERATE COVERAGE - Some gaps exist");
        } else {
            println!("  ✅ GOOD COVERAGE");
        }
        println!();
    }
    
    let overall_coverage = (total_found as f64 / total_tests as f64) * 100.0;
    println!("=== OVERALL ANALYSIS ===");
    println!("Total tests: {}", total_tests);
    println!("Total found: {} ({:.1}%)", total_found, overall_coverage);
    println!("Total missing: {} ({:.1}%)", total_tests - total_found, 100.0 - overall_coverage);
    
    // Identify problematic hue families
    let mut poor_families = Vec::new();
    let mut good_families = Vec::new();
    
    for (family, stats) in &hue_family_stats {
        let coverage = (stats.found as f64 / stats.total as f64) * 100.0;
        if coverage < 50.0 {
            poor_families.push((family.clone(), coverage));
        } else if coverage > 80.0 {
            good_families.push((family.clone(), coverage));
        }
    }
    
    if !poor_families.is_empty() {
        println!();
        println!("🔍 FAMILIES WITH POOR COVERAGE (likely wedge distribution issues):");
        for (family, coverage) in poor_families {
            println!("  - {}: {:.1}% coverage", family, coverage);
        }
    }
    
    if !good_families.is_empty() {
        println!();
        println!("✅ FAMILIES WITH GOOD COVERAGE (wedge distribution working):");
        for (family, coverage) in good_families {
            println!("  - {}: {:.1}% coverage", family, coverage);
        }
    }
    
    println!();
    println!("=== DIAGNOSTIC RECOMMENDATIONS ===");
    if overall_coverage < 30.0 {
        println!("❌ CRITICAL: Overall coverage too low. Likely fundamental wedge distribution issue.");
        println!("   Recommendation: Check adjacent plane splitting algorithm");
    } else if overall_coverage < 60.0 {
        println!("⚠️  MODERATE: Coverage gaps in specific hue families.");
        println!("   Recommendation: Analyze specific family wedge assignments");
    } else {
        println!("✅ GOOD: Overall coverage acceptable, may have isolated issues.");
    }
}

#[test]
fn test_adjacent_plane_mapping_direct() {
    println!("=== ADJACENT PLANE MAPPING VALIDATION ===");
    println!("Testing specific hue → adjacent plane mapping logic");
    println!();
    
    let classifier = IsccNbsClassifier::new().expect("Failed to create classifier");
    
    // Test specific hues that should have classifications
    let critical_test_cases = vec![
        ("5R", 5.0, 10.0, "Should be in red family planes"),
        ("2.5YR", 4.0, 8.0, "Should be in yellow-red family planes"),
        ("10B", 3.0, 6.0, "Should be in blue family planes"),
        ("7.5P", 6.0, 12.0, "Should be in purple family planes"),
        ("1G", 5.0, 8.0, "Should be in green family planes"),
    ];
    
    for (hue, value, chroma, description) in critical_test_cases {
        println!("Testing: {} {:.1}/{:.1} ({})", hue, value, chroma, description);
        
        match classifier.classify_munsell(hue, value, chroma) {
            Ok(Some(result)) => {
                println!("  ✅ FOUND: {} {}", result.iscc_nbs_descriptor(), result.iscc_nbs_color());
                println!("     Revised: {}", result.revised_descriptor());
            }
            Ok(None) => {
                println!("  ❌ NOT FOUND: No classification in any wedge");
                println!("     Issue: Hue {} may not be properly mapped to adjacent planes", hue);
            }
            Err(e) => {
                println!("  ❌ ERROR: {}", e);
            }
        }
        println!();
    }
}

#[test]
fn test_wedge_intersection_and_gaps() {
    println!("=== WEDGE INTERSECTION AND GAP ANALYSIS ===");
    println!("Analyzing potential issues with wedge boundaries and overlaps");
    println!();
    
    // Test boundary conditions between adjacent hues
    let boundary_tests = vec![
        ("9R", "10R", "1YR", 5.0, 8.0),   // Red to Yellow-Red boundary
        ("9YR", "10YR", "1Y", 4.0, 6.0),  // Yellow-Red to Yellow boundary  
        ("9Y", "10Y", "1GY", 6.0, 10.0),  // Yellow to Green-Yellow boundary
        ("9G", "10G", "1BG", 3.0, 4.0),   // Green to Blue-Green boundary
        ("9B", "10B", "1PB", 5.0, 12.0),  // Blue to Purple-Blue boundary
        ("9P", "10P", "1RP", 7.0, 14.0),  // Purple to Red-Purple boundary
        ("9RP", "10RP", "1R", 4.0, 8.0),  // Red-Purple to Red boundary
    ];
    
    for (hue1, hue2, hue3, value, chroma) in boundary_tests {
        println!("Boundary test: {} → {} → {} at {:.1}/{:.1}", hue1, hue2, hue3, value, chroma);
        
        let classifier = IsccNbsClassifier::new().expect("Failed to create classifier");
        
        let result1 = classifier.classify_munsell(hue1, value, chroma);
        let result2 = classifier.classify_munsell(hue2, value, chroma);  
        let result3 = classifier.classify_munsell(hue3, value, chroma);
        
        let found1 = result1.as_ref().map(|r| r.is_some()).unwrap_or(false);
        let found2 = result2.as_ref().map(|r| r.is_some()).unwrap_or(false);
        let found3 = result3.as_ref().map(|r| r.is_some()).unwrap_or(false);
        
        println!("  Results: {} {} {}", 
            if found1 { "✅" } else { "❌" },
            if found2 { "✅" } else { "❌" },
            if found3 { "✅" } else { "❌" }
        );
        
        // Analyze patterns
        if !found1 && !found2 && !found3 {
            println!("  ❌ CRITICAL: Complete boundary gap - no wedge coverage");
        } else if found1 && found2 && found3 {
            println!("  ⚠️  POTENTIAL OVERLAP: All three hues found (check for duplicate wedges)");
        } else {
            println!("  ✅ NORMAL: Partial coverage at boundary");
        }
        println!();
    }
}

// Helper structures and functions

#[derive(Debug)]
struct HueFamilyStats {
    family: String,
    total: usize,
    found: usize,
    not_found: usize,
    errors: usize,
    missing_points: Vec<String>,
}

impl HueFamilyStats {
    fn new(family: &str) -> Self {
        Self {
            family: family.to_string(),
            total: 0,
            found: 0,
            not_found: 0,
            errors: 0,
            missing_points: Vec::new(),
        }
    }
}

fn extract_hue_family(hue: &str) -> String {
    // Extract the hue family letters (e.g., "5R" → "R", "2.5YR" → "YR")
    hue.chars().filter(|c| c.is_alphabetic()).collect()
}