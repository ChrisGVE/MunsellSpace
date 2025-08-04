
fn main() {
    eprintln!("Starting program...");
    let r = 128u8;
    let g = 128u8;
    let b = 128u8;
    eprintln!("RGB: {}, {}, {}", r, g, b);
    eprintln!("Creating converter...");
    let converter = munsellspace::mathematical::MathematicalMunsellConverter::new().unwrap();
    eprintln!("Converter created. Converting...");
    let spec = converter.srgb_to_munsell([r, g, b]).unwrap();
    eprintln!("Conversion complete.");
    println!("Result: {:.1}{} {:.1}/{:.1}", spec.hue, spec.family, spec.value, spec.chroma);
}

