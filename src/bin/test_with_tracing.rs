//! Test program with automatic tracing enabled

use munsellspace::python_converter::PythonMunsellConverter;
use tracing::{info, Level};
use tracing_subscriber::FmtSubscriber;

fn main() {
    // Set up tracing subscriber with detailed output
    let subscriber = FmtSubscriber::builder()
        .with_max_level(Level::TRACE)
        .with_target(false)
        .with_thread_ids(false)
        .with_thread_names(false)
        .with_file(true)
        .with_line_number(true)
        .pretty()
        .finish();
    
    tracing::subscriber::set_global_default(subscriber)
        .expect("setting default subscriber failed");
    
    info!("Starting Munsell conversion test with automatic tracing");
    
    // Test RGB(221, 238, 238)
    let rgb = [221u8, 238u8, 238u8];
    info!("Testing RGB({}, {}, {})", rgb[0], rgb[1], rgb[2]);
    
    let converter = PythonMunsellConverter::new();
    
    match converter.srgb_to_munsell(rgb) {
        Ok(munsell) => {
            info!("Result: {}", munsell.notation);
            info!("Components: hue={:?}, value={:.2}, chroma={:?}", 
                  munsell.hue, munsell.value, munsell.chroma);
        }
        Err(e) => {
            eprintln!("Error: {:?}", e);
        }
    }
}