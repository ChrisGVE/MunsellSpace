/// Thread-safe unified color conversion cache with FIFO eviction
/// 
/// This module provides a centralized caching system for color conversions
/// that normalizes all inputs to RGB [u8; 3] format to ensure cache hits
/// regardless of input format (hex, RGB, Lab, HSL, HSV).

use std::collections::VecDeque;
use std::sync::{Arc, Mutex};
use crate::{MunsellColor, ISCC_NBS_Result, MunsellError};

/// Maximum number of cached entries (FIFO eviction when exceeded)
const CACHE_SIZE: usize = 500;

/// Complete cached result for a color conversion
#[derive(Clone, Debug)]
pub struct CachedColorResult {
    /// The RGB value (canonical form)
    pub rgb: [u8; 3],
    /// Munsell notation result
    pub munsell: MunsellColor,
    /// ISCC-NBS classification result (if applicable)
    pub iscc_nbs: Option<ISCC_NBS_Result>,
}

/// Thread-safe FIFO cache for color conversions
#[derive(Clone)]
pub struct UnifiedColorCache {
    /// Internal cache storage - Vec of (key, value) pairs maintained in FIFO order
    cache: Arc<Mutex<VecDeque<([u8; 3], CachedColorResult)>>>,
    /// Maximum cache size
    max_size: usize,
}

impl UnifiedColorCache {
    /// Create a new cache with default size (500 entries)
    pub fn new() -> Self {
        Self::with_capacity(CACHE_SIZE)
    }
    
    /// Create a new cache with specified capacity
    pub fn with_capacity(capacity: usize) -> Self {
        Self {
            cache: Arc::new(Mutex::new(VecDeque::with_capacity(capacity))),
            max_size: capacity,
        }
    }
    
    /// Look up a color by RGB value
    pub fn get(&self, rgb: &[u8; 3]) -> Option<CachedColorResult> {
        let cache = self.cache.lock().unwrap();
        
        // Linear search from back (most recent) to front (oldest)
        // This gives us LRU-like behavior without the complexity
        for (cached_rgb, result) in cache.iter().rev() {
            if cached_rgb == rgb {
                return Some(result.clone());
            }
        }
        None
    }
    
    /// Store a color conversion result
    pub fn insert(&self, rgb: [u8; 3], result: CachedColorResult) {
        let mut cache = self.cache.lock().unwrap();
        
        // First check if it already exists and remove it
        // (we'll re-add it at the back for LRU-like behavior)
        cache.retain(|(cached_rgb, _)| cached_rgb != &rgb);
        
        // Add to the back (most recent)
        cache.push_back((rgb, result));
        
        // If we exceed capacity, remove from the front (oldest)
        if cache.len() > self.max_size {
            cache.pop_front();
        }
    }
    
    /// Clear all cached entries
    pub fn clear(&self) {
        let mut cache = self.cache.lock().unwrap();
        cache.clear();
    }
    
    /// Get the current number of cached entries
    pub fn len(&self) -> usize {
        let cache = self.cache.lock().unwrap();
        cache.len()
    }
    
    /// Check if the cache is empty
    pub fn is_empty(&self) -> bool {
        let cache = self.cache.lock().unwrap();
        cache.is_empty()
    }
    
    /// Get cache statistics
    pub fn stats(&self) -> CacheStats {
        let cache = self.cache.lock().unwrap();
        CacheStats {
            current_size: cache.len(),
            max_size: self.max_size,
            capacity: cache.capacity(),
        }
    }
}

impl Default for UnifiedColorCache {
    fn default() -> Self {
        Self::new()
    }
}

/// Cache statistics
#[derive(Debug, Clone)]
pub struct CacheStats {
    /// Current number of entries in cache
    pub current_size: usize,
    /// Maximum allowed entries
    pub max_size: usize,
    /// Current allocated capacity
    pub capacity: usize,
}

/// Normalize hex color string to RGB
/// Handles formats: #RGB, #RRGGBB, RGB, RRGGBB (case insensitive)
pub fn normalize_hex_to_rgb(hex: &str) -> Result<[u8; 3], MunsellError> {
    let hex = hex.trim().trim_start_matches('#').to_uppercase();
    
    let rgb = if hex.len() == 3 {
        // Short form: "F00" -> [255, 0, 0]
        let r = u8::from_str_radix(&hex[0..1].repeat(2), 16)
            .map_err(|_| MunsellError::ConversionError { 
                message: format!("Invalid hex color: {}", hex) 
            })?;
        let g = u8::from_str_radix(&hex[1..2].repeat(2), 16)
            .map_err(|_| MunsellError::ConversionError { 
                message: format!("Invalid hex color: {}", hex) 
            })?;
        let b = u8::from_str_radix(&hex[2..3].repeat(2), 16)
            .map_err(|_| MunsellError::ConversionError { 
                message: format!("Invalid hex color: {}", hex) 
            })?;
        [r, g, b]
    } else if hex.len() == 6 {
        // Long form: "FF0000" -> [255, 0, 0]
        let r = u8::from_str_radix(&hex[0..2], 16)
            .map_err(|_| MunsellError::ConversionError { 
                message: format!("Invalid hex color: {}", hex) 
            })?;
        let g = u8::from_str_radix(&hex[2..4], 16)
            .map_err(|_| MunsellError::ConversionError { 
                message: format!("Invalid hex color: {}", hex) 
            })?;
        let b = u8::from_str_radix(&hex[4..6], 16)
            .map_err(|_| MunsellError::ConversionError { 
                message: format!("Invalid hex color: {}", hex) 
            })?;
        [r, g, b]
    } else {
        return Err(MunsellError::ConversionError { 
            message: format!("Invalid hex color length: expected 3 or 6 characters, got {}", hex.len()) 
        });
    };
    
    Ok(rgb)
}

/// Convert Lab to sRGB [0-255]
/// Uses D65 white point
pub fn lab_to_rgb(lab: [f64; 3]) -> Result<[u8; 3], MunsellError> {
    // Lab → XYZ → RGB conversion
    let [l, a, b] = lab;
    
    // D65 white point
    const XN: f64 = 0.95047;
    const YN: f64 = 1.00000;
    const ZN: f64 = 1.08883;
    
    // Lab to XYZ
    let fy = (l + 16.0) / 116.0;
    let fx = a / 500.0 + fy;
    let fz = fy - b / 200.0;
    
    let delta = 6.0 / 29.0;
    let delta_cubed = delta * delta * delta;
    
    let x = if fx * fx * fx > delta_cubed {
        fx * fx * fx
    } else {
        (116.0 * fx - 16.0) / 903.3
    } * XN;
    
    let y = if l > 7.9996 {
        fy * fy * fy
    } else {
        l / 903.3
    } * YN;
    
    let z = if fz * fz * fz > delta_cubed {
        fz * fz * fz
    } else {
        (116.0 * fz - 16.0) / 903.3
    } * ZN;
    
    // XYZ to linear RGB (using sRGB matrix)
    let r_linear =  3.2406 * x - 1.5372 * y - 0.4986 * z;
    let g_linear = -0.9689 * x + 1.8758 * y + 0.0415 * z;
    let b_linear =  0.0557 * x - 0.2040 * y + 1.0570 * z;
    
    // Apply gamma correction (linear RGB to sRGB)
    let gamma_correct = |linear: f64| -> u8 {
        let srgb = if linear <= 0.0031308 {
            12.92 * linear
        } else {
            1.055 * linear.powf(1.0 / 2.4) - 0.055
        };
        (srgb * 255.0).round().clamp(0.0, 255.0) as u8
    };
    
    Ok([
        gamma_correct(r_linear),
        gamma_correct(g_linear),
        gamma_correct(b_linear),
    ])
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_hex_normalization() {
        // All these should produce the same RGB
        assert_eq!(normalize_hex_to_rgb("#FF0000").unwrap(), [255, 0, 0]);
        assert_eq!(normalize_hex_to_rgb("#ff0000").unwrap(), [255, 0, 0]);
        assert_eq!(normalize_hex_to_rgb("FF0000").unwrap(), [255, 0, 0]);
        assert_eq!(normalize_hex_to_rgb("ff0000").unwrap(), [255, 0, 0]);
        assert_eq!(normalize_hex_to_rgb("#F00").unwrap(), [255, 0, 0]);
        assert_eq!(normalize_hex_to_rgb("#f00").unwrap(), [255, 0, 0]);
        assert_eq!(normalize_hex_to_rgb("F00").unwrap(), [255, 0, 0]);
        assert_eq!(normalize_hex_to_rgb("f00").unwrap(), [255, 0, 0]);
    }
    
    #[test]
    fn test_cache_fifo_eviction() {
        let cache = UnifiedColorCache::with_capacity(3);
        
        // Create dummy results
        let result1 = CachedColorResult {
            rgb: [255, 0, 0],
            munsell: MunsellColor {
                hue: Some("5R".to_string()),
                value: 5.0,
                chroma: Some(10.0),
                notation: "5R 5.0/10.0".to_string(),
            },
            iscc_nbs: None,
        };
        
        let result2 = result1.clone();
        let result3 = result1.clone();
        let result4 = result1.clone();
        
        // Fill cache to capacity
        cache.insert([1, 0, 0], result1.clone());
        cache.insert([2, 0, 0], result2.clone());
        cache.insert([3, 0, 0], result3.clone());
        assert_eq!(cache.len(), 3);
        
        // Add one more - should evict the first
        cache.insert([4, 0, 0], result4.clone());
        assert_eq!(cache.len(), 3);
        
        // First entry should be gone
        assert!(cache.get(&[1, 0, 0]).is_none());
        // Others should still be there
        assert!(cache.get(&[2, 0, 0]).is_some());
        assert!(cache.get(&[3, 0, 0]).is_some());
        assert!(cache.get(&[4, 0, 0]).is_some());
    }
    
    #[test]
    fn test_cache_thread_safety() {
        use std::thread;
        
        let cache = Arc::new(UnifiedColorCache::with_capacity(100));
        let mut handles = vec![];
        
        // Spawn multiple threads that write to cache
        for i in 0..10 {
            let cache_clone = Arc::clone(&cache);
            let handle = thread::spawn(move || {
                let result = CachedColorResult {
                    rgb: [i as u8, 0, 0],
                    munsell: MunsellColor {
                        hue: Some(format!("{}R", i)),
                        value: i as f64,
                        chroma: Some(i as f64),
                        notation: format!("{}R {}.0/{}.0", i, i, i),
                    },
                    iscc_nbs: None,
                };
                
                for j in 0..10 {
                    let rgb = [(i * 10 + j) as u8, 0, 0];
                    cache_clone.insert(rgb, result.clone());
                }
            });
            handles.push(handle);
        }
        
        // Wait for all threads to complete
        for handle in handles {
            handle.join().unwrap();
        }
        
        // Cache should have entries (exact count depends on timing)
        assert!(cache.len() > 0);
        assert!(cache.len() <= 100);
    }
}