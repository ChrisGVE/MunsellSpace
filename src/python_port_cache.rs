//! Caching mechanisms - exact 1:1 port behavior from Python colour-science
//! Python uses LRU caching and memoization, we'll implement equivalent behavior

use std::collections::HashMap;
use std::hash::{Hash, Hasher};
use ordered_float::OrderedFloat;

/// Cache key for floating point values
/// Handles f64 hashing for cache keys
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct CacheKey {
    values: Vec<OrderedFloat<f64>>,
}

impl CacheKey {
    /// Create a cache key from f64 values
    pub fn from_floats(values: &[f64]) -> Self {
        Self {
            values: values.iter().map(|&v| OrderedFloat(v)).collect(),
        }
    }
    
    /// Create a cache key from a single f64
    pub fn from_float(value: f64) -> Self {
        Self {
            values: vec![OrderedFloat(value)],
        }
    }
    
    /// Create a cache key from specification [hue, value, chroma, code]
    pub fn from_specification(spec: &[f64; 4]) -> Self {
        Self::from_floats(spec)
    }
    
    /// Create a cache key from xyY coordinates
    pub fn from_xyy(xyy: &[f64; 3]) -> Self {
        Self::from_floats(xyy)
    }
}

/// Simple LRU cache implementation
/// Matches Python's functools.lru_cache behavior
pub struct LRUCache<K: Hash + Eq + Clone, V: Clone> {
    capacity: usize,
    cache: HashMap<K, V>,
    access_order: Vec<K>,
}

impl<K: Hash + Eq + Clone, V: Clone> LRUCache<K, V> {
    /// Create a new LRU cache with specified capacity
    pub fn new(capacity: usize) -> Self {
        Self {
            capacity,
            cache: HashMap::with_capacity(capacity),
            access_order: Vec::with_capacity(capacity),
        }
    }
    
    /// Get a value from the cache
    pub fn get(&mut self, key: &K) -> Option<V> {
        if let Some(value) = self.cache.get(key) {
            // Move to end of access order (most recently used)
            self.access_order.retain(|k| k != key);
            self.access_order.push(key.clone());
            Some(value.clone())
        } else {
            None
        }
    }
    
    /// Insert a value into the cache
    pub fn insert(&mut self, key: K, value: V) {
        // If key exists, update and move to end
        if self.cache.contains_key(&key) {
            self.cache.insert(key.clone(), value);
            self.access_order.retain(|k| k != &key);
            self.access_order.push(key);
            return;
        }
        
        // If at capacity, remove least recently used
        if self.cache.len() >= self.capacity {
            if let Some(lru_key) = self.access_order.first() {
                let lru_key = lru_key.clone();
                self.cache.remove(&lru_key);
                self.access_order.remove(0);
            }
        }
        
        // Insert new entry
        self.cache.insert(key.clone(), value);
        self.access_order.push(key);
    }
    
    /// Clear the cache
    pub fn clear(&mut self) {
        self.cache.clear();
        self.access_order.clear();
    }
    
    /// Get cache size
    pub fn len(&self) -> usize {
        self.cache.len()
    }
    
    /// Check if cache is empty
    pub fn is_empty(&self) -> bool {
        self.cache.is_empty()
    }
}

/// Global cache for Munsell conversions
/// This matches Python's module-level caching
pub struct MunsellCache {
    xyy_to_munsell: LRUCache<CacheKey, [f64; 4]>,
    munsell_to_xyy: LRUCache<CacheKey, [f64; 3]>,
    interpolation_results: LRUCache<CacheKey, f64>,
}

impl MunsellCache {
    /// Create a new Munsell cache
    pub fn new(capacity: usize) -> Self {
        Self {
            xyy_to_munsell: LRUCache::new(capacity),
            munsell_to_xyy: LRUCache::new(capacity),
            interpolation_results: LRUCache::new(capacity),
        }
    }
    
    /// Get cached xyY to Munsell result
    pub fn get_xyy_to_munsell(&mut self, xyy: &[f64; 3]) -> Option<[f64; 4]> {
        let key = CacheKey::from_xyy(xyy);
        self.xyy_to_munsell.get(&key)
    }
    
    /// Cache xyY to Munsell result
    pub fn cache_xyy_to_munsell(&mut self, xyy: &[f64; 3], result: [f64; 4]) {
        let key = CacheKey::from_xyy(xyy);
        self.xyy_to_munsell.insert(key, result);
    }
    
    /// Get cached Munsell to xyY result
    pub fn get_munsell_to_xyy(&mut self, spec: &[f64; 4]) -> Option<[f64; 3]> {
        let key = CacheKey::from_specification(spec);
        self.munsell_to_xyy.get(&key)
    }
    
    /// Cache Munsell to xyY result
    pub fn cache_munsell_to_xyy(&mut self, spec: &[f64; 4], result: [f64; 3]) {
        let key = CacheKey::from_specification(spec);
        self.munsell_to_xyy.insert(key, result);
    }
    
    /// Get cached interpolation result
    pub fn get_interpolation(&mut self, values: &[f64]) -> Option<f64> {
        let key = CacheKey::from_floats(values);
        self.interpolation_results.get(&key)
    }
    
    /// Cache interpolation result
    pub fn cache_interpolation(&mut self, values: &[f64], result: f64) {
        let key = CacheKey::from_floats(values);
        self.interpolation_results.insert(key, result);
    }
    
    /// Clear all caches
    pub fn clear_all(&mut self) {
        self.xyy_to_munsell.clear();
        self.munsell_to_xyy.clear();
        self.interpolation_results.clear();
    }
}

/// Thread-local cache instance
/// This matches Python's module-level caching behavior
thread_local! {
    static CACHE: std::cell::RefCell<MunsellCache> = std::cell::RefCell::new(MunsellCache::new(128));
}

/// Get cached xyY to Munsell conversion result
pub fn get_cached_xyy_to_munsell(xyy: &[f64; 3]) -> Option<[f64; 4]> {
    CACHE.with(|cache| cache.borrow_mut().get_xyy_to_munsell(xyy))
}

/// Cache xyY to Munsell conversion result
pub fn cache_xyy_to_munsell(xyy: &[f64; 3], result: [f64; 4]) {
    CACHE.with(|cache| cache.borrow_mut().cache_xyy_to_munsell(xyy, result));
}

/// Get cached Munsell to xyY conversion result
pub fn get_cached_munsell_to_xyy(spec: &[f64; 4]) -> Option<[f64; 3]> {
    CACHE.with(|cache| cache.borrow_mut().get_munsell_to_xyy(spec))
}

/// Cache Munsell to xyY conversion result
pub fn cache_munsell_to_xyy(spec: &[f64; 4], result: [f64; 3]) {
    CACHE.with(|cache| cache.borrow_mut().cache_munsell_to_xyy(spec, result));
}

/// Clear all caches
pub fn clear_all_caches() {
    CACHE.with(|cache| cache.borrow_mut().clear_all());
}

/// Memoization decorator equivalent
/// For functions that should cache their results
pub struct Memoized<F, K, V> 
where
    K: Hash + Eq + Clone,
    V: Clone,
{
    func: F,
    cache: HashMap<K, V>,
}

impl<F, K, V> Memoized<F, K, V>
where
    F: Fn(&K) -> V,
    K: Hash + Eq + Clone,
    V: Clone,
{
    /// Create a new memoized function
    pub fn new(func: F) -> Self {
        Self {
            func,
            cache: HashMap::new(),
        }
    }
    
    /// Call the memoized function
    pub fn call(&mut self, key: &K) -> V {
        if let Some(value) = self.cache.get(key) {
            value.clone()
        } else {
            let value = (self.func)(key);
            self.cache.insert(key.clone(), value.clone());
            value
        }
    }
    
    /// Clear the memoization cache
    pub fn clear(&mut self) {
        self.cache.clear();
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_cache_key() {
        let key1 = CacheKey::from_float(1.5);
        let key2 = CacheKey::from_float(1.5);
        let key3 = CacheKey::from_float(2.0);
        
        assert_eq!(key1, key2);
        assert_ne!(key1, key3);
        
        let spec_key = CacheKey::from_specification(&[5.0, 4.0, 10.0, 7.0]);
        let xyy_key = CacheKey::from_xyy(&[0.31, 0.35, 0.2]);
        
        assert_ne!(spec_key, xyy_key);
    }
    
    #[test]
    fn test_lru_cache() {
        let mut cache: LRUCache<String, i32> = LRUCache::new(2);
        
        cache.insert("a".to_string(), 1);
        cache.insert("b".to_string(), 2);
        
        assert_eq!(cache.get(&"a".to_string()), Some(1));
        assert_eq!(cache.get(&"b".to_string()), Some(2));
        
        // Insert third item, should evict "a" (least recently used)
        cache.insert("c".to_string(), 3);
        
        assert_eq!(cache.get(&"a".to_string()), None); // Evicted
        assert_eq!(cache.get(&"b".to_string()), Some(2));
        assert_eq!(cache.get(&"c".to_string()), Some(3));
    }
    
    #[test]
    fn test_munsell_cache() {
        let mut cache = MunsellCache::new(10);
        
        let xyy = [0.31, 0.35, 0.2];
        let spec = [5.0, 4.0, 10.0, 7.0];
        
        // Test caching xyY to Munsell
        assert_eq!(cache.get_xyy_to_munsell(&xyy), None);
        cache.cache_xyy_to_munsell(&xyy, spec);
        assert_eq!(cache.get_xyy_to_munsell(&xyy), Some(spec));
        
        // Test caching Munsell to xyY
        assert_eq!(cache.get_munsell_to_xyy(&spec), None);
        cache.cache_munsell_to_xyy(&spec, xyy);
        assert_eq!(cache.get_munsell_to_xyy(&spec), Some(xyy));
    }
    
    #[test]
    fn test_memoization() {
        let mut memoized = Memoized::new(|x: &i32| x * 2);
        
        assert_eq!(memoized.call(&5), 10);
        assert_eq!(memoized.call(&5), 10); // Should use cached value
        assert_eq!(memoized.call(&3), 6);
        
        memoized.clear();
        assert_eq!(memoized.call(&5), 10); // Recalculated after clear
    }
}