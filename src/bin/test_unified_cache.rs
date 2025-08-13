/// Test that unified cache properly normalizes different input formats
/// to ensure cache hits for equivalent colors

use munsellspace::{UnifiedColorCache, CachedColorResult, MunsellConverter, ISCC_NBS_Classifier};
use munsellspace::unified_cache::{hex_to_rgb, lab_to_rgb};
use std::sync::Arc;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("Testing Unified Color Cache");
    println!("===========================\n");
    
    // Create shared cache
    let cache = Arc::new(UnifiedColorCache::with_capacity(100));
    let converter = MunsellConverter::new()?;
    let classifier = ISCC_NBS_Classifier::new()?;
    
    // Test 1: Same color via different hex formats
    println!("Test 1: Hex format normalization");
    println!("---------------------------------");
    
    let hex_formats = [
        "#FF0000", "#ff0000", "FF0000", "ff0000",
        "#F00", "#f00", "F00", "f00"
    ];
    
    for (i, hex) in hex_formats.iter().enumerate() {
        let rgb = hex_to_rgb(hex)?;
        println!("Format {}: {} → RGB {:?}", i + 1, hex, rgb);
        
        // Check if it's in cache
        if let Some(cached) = cache.get(&rgb) {
            println!("  ✅ Cache HIT! Munsell: {}", cached.munsell.notation);
        } else {
            println!("  ❌ Cache MISS - Computing...");
            // Compute and cache
            let munsell = converter.srgb_to_munsell(rgb)?;
            let iscc_result = classifier.classify_munsell(
                munsell.hue.as_deref().unwrap_or("N"),
                munsell.value,
                munsell.chroma.unwrap_or(0.0)
            )?;
            
            let result = CachedColorResult {
                rgb,
                munsell: munsell.clone(),
                iscc_nbs: iscc_result,
            };
            
            cache.insert(rgb, result);
            println!("  Computed and cached: {}", munsell.notation);
        }
    }
    
    println!("\nCache size after hex tests: {}", cache.len());
    println!("Expected: 1 (all formats should normalize to same RGB)");
    
    // Test 2: RGB vs Hex for same color
    println!("\n\nTest 2: RGB array vs Hex string");
    println!("--------------------------------");
    
    let rgb_direct = [0, 128, 255];  // A blue color
    let hex_equivalent = "#0080FF";
    
    println!("Direct RGB: {:?}", rgb_direct);
    println!("Hex string: {}", hex_equivalent);
    
    // First, insert via RGB
    if cache.get(&rgb_direct).is_none() {
        let munsell = converter.srgb_to_munsell(rgb_direct)?;
        let iscc_result = classifier.classify_munsell(
            munsell.hue.as_deref().unwrap_or("N"),
            munsell.value,
            munsell.chroma.unwrap_or(0.0)
        )?;
        
        let result = CachedColorResult {
            rgb: rgb_direct,
            munsell: munsell.clone(),
            iscc_nbs: iscc_result,
        };
        
        cache.insert(rgb_direct, result);
        println!("Cached via RGB: {}", munsell.notation);
    }
    
    // Now try via hex - should hit cache
    let rgb_from_hex = hex_to_rgb(hex_equivalent)?;
    println!("Hex normalizes to: {:?}", rgb_from_hex);
    
    if rgb_from_hex == rgb_direct {
        println!("✅ RGB values match!");
        
        if let Some(cached) = cache.get(&rgb_from_hex) {
            println!("✅ Cache HIT via hex! Munsell: {}", cached.munsell.notation);
        } else {
            println!("❌ Unexpected cache miss");
        }
    } else {
        println!("❌ RGB values don't match");
    }
    
    // Test 3: Lab to RGB conversion and caching
    println!("\n\nTest 3: Lab color conversion");
    println!("----------------------------");
    
    // A red color in Lab space
    let lab = [53.23, 80.11, 67.22];  // Approximately red
    println!("Lab color: L={:.2}, a={:.2}, b={:.2}", lab[0], lab[1], lab[2]);
    
    let rgb_from_lab = lab_to_rgb(lab)?;
    println!("Converts to RGB: {:?}", rgb_from_lab);
    
    // Check cache
    if let Some(cached) = cache.get(&rgb_from_lab) {
        println!("✅ Found in cache: {}", cached.munsell.notation);
    } else {
        println!("❌ Not in cache (expected for unique Lab color)");
        // Compute and cache
        let munsell = converter.srgb_to_munsell(rgb_from_lab)?;
        let iscc_result = classifier.classify_munsell(
            munsell.hue.as_deref().unwrap_or("N"),
            munsell.value,
            munsell.chroma.unwrap_or(0.0)
        )?;
        
        let result = CachedColorResult {
            rgb: rgb_from_lab,
            munsell: munsell.clone(),
            iscc_nbs: iscc_result,
        };
        
        cache.insert(rgb_from_lab, result);
        println!("Computed and cached: {}", munsell.notation);
    }
    
    // Test 4: FIFO eviction
    println!("\n\nTest 4: FIFO eviction (capacity = 100)");
    println!("---------------------------------------");
    
    let initial_size = cache.len();
    println!("Initial cache size: {}", initial_size);
    
    // Add many colors to trigger eviction
    for i in 0..120 {
        let rgb = [(i % 256) as u8, ((i * 2) % 256) as u8, ((i * 3) % 256) as u8];
        
        if cache.get(&rgb).is_none() {
            // Create dummy result for testing
            let munsell = converter.srgb_to_munsell(rgb)?;
            let result = CachedColorResult {
                rgb,
                munsell,
                iscc_nbs: None,
            };
            cache.insert(rgb, result);
        }
    }
    
    println!("After adding 120 colors: {} entries", cache.len());
    println!("Expected: ≤100 (due to FIFO eviction)");
    
    // Verify first colors were evicted
    let first_color = [0, 0, 0];
    if cache.get(&first_color).is_none() {
        println!("✅ First color was evicted (FIFO working)");
    } else {
        println!("❓ First color still in cache");
    }
    
    // Recent colors should still be there
    let recent_color = [119u8, 238u8, 101u8];  // (119*3) % 256 = 357 % 256 = 101
    if cache.get(&recent_color).is_some() {
        println!("✅ Recent color still in cache");
    } else {
        println!("❌ Recent color was evicted (unexpected)");
    }
    
    // Final statistics
    println!("\n\nFinal Cache Statistics");
    println!("----------------------");
    let stats = cache.stats();
    println!("Current size: {}/{}", stats.current_size, stats.max_size);
    println!("Capacity allocated: {}", stats.capacity);
    
    println!("\n✅ All tests complete!");
    
    Ok(())
}