/// Debug script to check hue sequence
use munsellspace::MechanicalWedgeSystem;

fn main() {
    let wedge_system = MechanicalWedgeSystem::new();
    let stats = wedge_system.get_wedge_statistics();
    println!("Wedge system has {} wedges", stats.total_wedges);
    
    // Print the first few and last few hue wedge keys to see the pattern
    let mut wedge_keys: Vec<_> = stats.wedge_counts.keys().collect();
    wedge_keys.sort();
    
    println!("First 10 wedge keys:");
    for key in wedge_keys.iter().take(10) {
        println!("  {}", key);
    }
    
    println!("Last 10 wedge keys:");
    for key in wedge_keys.iter().skip(wedge_keys.len() - 10) {
        println!("  {}", key);
    }
    
    // Check if specific RP hues are present
    let rp_wedges: Vec<_> = wedge_keys.iter().filter(|k| k.contains("RP")).collect();
    println!("RP family wedges ({}):", rp_wedges.len());
    for key in rp_wedges {
        println!("  {}", key);
    }
}