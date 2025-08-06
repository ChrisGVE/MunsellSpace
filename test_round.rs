fn main() {
    let chroma: f64 = 22.595;
    let rounded = 2.0 * (chroma / 2.0).round();
    println!("chroma={}, rounded={}", chroma, rounded);
    
    // Check if it's even
    let is_even = (2.0 * (chroma / 2.0 - (chroma / 2.0).round())).abs() > 1e-10;
    println!("Is {} even? {}", chroma, !is_even);
}