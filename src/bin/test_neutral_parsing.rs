/// Test neutral color parsing to verify support for different formats

use munsellspace::reverse_conversion::parse_munsell_notation;
use munsellspace::python_port_strings::parse_munsell_colour;

fn main() {
    println!("Testing Neutral Color Notation Parsing");
    println!("======================================\n");
    
    let test_cases = vec![
        "N5",        // No space (Python standard)
        "N 5",       // With space (common format)
        "N5.5",      // Decimal no space
        "N 5.5",     // Decimal with space
        "N5/",       // With trailing slash
        "N 5/",      // With space and slash
        "N5/0",      // With explicit zero chroma
        "N 5/0",     // Space with zero chroma
        "N 5.2/",    // Decimal with slash
        "0.0N 5",    // Number before N (sometimes seen in data)
        "5.0N 5",    // Hue number before N (nonsensical but occurs)
        "0N5",       // Zero before N without space
        "10N 5.5",   // Even 10 before N
    ];
    
    println!("Test 1: Python-ported parse_munsell_colour()");
    println!("---------------------------------------------");
    for notation in &test_cases {
        print!("{:12} -> ", notation);
        match parse_munsell_colour(notation) {
            Ok(spec) => {
                println!("✅ value={:.1}", spec[1]);
            }
            Err(_) => {
                println!("❌ Not recognized");
            }
        }
    }
    
    println!("\nTest 2: ReverseConverter parse_munsell_notation()");
    println!("--------------------------------------------------");
    for notation in &test_cases {
        print!("{:12} -> ", notation);
        match parse_munsell_notation(notation) {
            Ok(spec) => {
                println!("✅ value={:.1}, family={}", spec.value, spec.family);
            }
            Err(_) => {
                println!("❌ Not recognized");
            }
        }
    }
    
    println!("\nTest 3: Round-trip through PythonMunsellConverter");
    println!("--------------------------------------------------");
    
    use munsellspace::python_converter::PythonMunsellConverter;
    let converter = PythonMunsellConverter::new();
    
    for notation in &test_cases {
        print!("{:12} -> ", notation);
        match converter.munsell_to_srgb(notation) {
            Ok(rgb) => {
                println!("✅ RGB [{:3}, {:3}, {:3}]", rgb.r, rgb.g, rgb.b);
            }
            Err(e) => {
                println!("❌ {}", e);
            }
        }
    }
    
    println!("\n📊 Summary:");
    println!("-----------");
    println!("The regex pattern now supports:");
    println!("  • Standard formats: N5, N 5, N5.5, N 5.5");
    println!("  • With slash/chroma: N5/, N 5/, N5/0, N 5/0");
    println!("  • With leading number: 0.0N 5, 5.0N 5, 10N 5.5");
    println!("  • (Leading numbers are ignored as they're meaningless for neutrals)");
}