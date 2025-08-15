# MunsellSpace API Documentation

Complete API reference for the MunsellSpace Rust library.

## Table of Contents

- [Core Types](#core-types)
- [Conversion Functions](#conversion-functions)
- [ISCC-NBS Classification](#iscc-nbs-classification)
- [Illuminants and Adaptation](#illuminants-and-adaptation)
- [Error Handling](#error-handling)
- [Advanced Features](#advanced-features)
- [Examples](#examples)

## Core Types

### `MunsellColor`

Represents a color in Munsell notation.

```rust
pub struct MunsellColor {
    pub hue: Option<String>,     // e.g., "5R", "2.5YR", "N" for neutral
    pub value: f64,               // 0.0 to 10.0
    pub chroma: Option<f64>,      // 0.0 to maximum (varies by hue/value)
    pub notation: String,         // Full notation, e.g., "5R 4.0/14.0"
}
```

#### Methods

```rust
impl MunsellColor {
    /// Create a new Munsell color
    pub fn new(hue: Option<String>, value: f64, chroma: Option<f64>) -> Result<Self>
    
    /// Parse from notation string
    pub fn from_notation(notation: &str) -> Result<Self>
    
    /// Check if color is achromatic (neutral)
    pub fn is_achromatic(&self) -> bool
    
    /// Get hue family (R, YR, Y, GY, G, BG, B, PB, P, RP)
    pub fn hue_family(&self) -> Option<String>
    
    /// Validate color is within gamut
    pub fn validate(&self) -> Result<()>
}
```

### `RgbColor`

RGB color representation with validation.

```rust
pub struct RgbColor {
    pub r: u8,  // Red (0-255)
    pub g: u8,  // Green (0-255)
    pub b: u8,  // Blue (0-255)
}
```

#### Methods

```rust
impl RgbColor {
    /// Create from array
    pub fn from_array(rgb: [u8; 3]) -> Self
    
    /// Create from individual components
    pub fn new(r: u8, g: u8, b: u8) -> Self
    
    /// Convert to array
    pub fn to_array(&self) -> [u8; 3]
    
    /// Convert to normalized floats (0.0-1.0)
    pub fn to_normalized(&self) -> [f64; 3]
}
```

## Conversion Functions

### `MunsellConverter`

Main converter for RGB to Munsell transformations.

```rust
pub struct MunsellConverter {
    // Internal fields
}
```

#### Methods

```rust
impl MunsellConverter {
    /// Create a new converter with default settings
    pub fn new() -> Result<Self>
    
    /// Create with specific configuration
    pub fn with_config(config: ConverterConfig) -> Result<Self>
    
    /// Convert sRGB to Munsell
    pub fn srgb_to_munsell(&self, rgb: [u8; 3]) -> Result<MunsellColor>
    
    /// Convert Lab to Munsell
    pub fn lab_to_munsell(&self, lab: [f64; 3]) -> Result<MunsellColor>
    
    /// Convert hex to Munsell
    pub fn hex_to_munsell(&self, hex: &str) -> Result<MunsellColor>
    
    /// Batch conversion
    pub fn convert_batch(&self, colors: &[[u8; 3]]) -> Result<Vec<MunsellColor>>
    
    /// Parallel batch conversion
    pub fn convert_batch_parallel(&self, colors: &[[u8; 3]]) -> Result<Vec<MunsellColor>>
}
```

#### Configuration

```rust
pub struct ConverterConfig {
    pub illuminant: Illuminant,
    pub adaptation: ChromaticAdaptation,
    pub cache_size: usize,
    pub parallel_threshold: usize,
}

impl Default for ConverterConfig {
    fn default() -> Self {
        Self {
            illuminant: Illuminant::D65,
            adaptation: ChromaticAdaptation::Bradford,
            cache_size: 1000,
            parallel_threshold: 100,
        }
    }
}
```

## ISCC-NBS Classification

### `ISCC_NBS_Classifier`

Classifies colors into ISCC-NBS standardized color names.

```rust
pub struct ISCC_NBS_Classifier {
    // Internal fields
}
```

#### Methods

```rust
impl ISCC_NBS_Classifier {
    /// Create a new classifier
    pub fn new() -> Result<Self>
    
    /// Classify RGB color
    pub fn classify_rgb(&self, rgb: [u8; 3]) -> Result<IsccNbsColor>
    
    /// Classify Lab color
    pub fn classify_lab(&self, lab: [f64; 3]) -> Result<IsccNbsColor>
    
    /// Classify hex color
    pub fn classify_hex(&self, hex: &str) -> Result<IsccNbsColor>
    
    /// Classify Munsell color
    pub fn classify_munsell(
        &self, 
        hue: &str, 
        value: f64, 
        chroma: f64
    ) -> Result<IsccNbsColor>
    
    /// Get all color definitions
    pub fn get_all_colors(&self) -> Vec<IsccNbsColor>
    
    /// Find color by ID
    pub fn get_color_by_id(&self, id: u32) -> Option<IsccNbsColor>
    
    /// Find color by name
    pub fn get_color_by_name(&self, name: &str) -> Option<IsccNbsColor>
}
```

### `IsccNbsColor`

ISCC-NBS color representation.

```rust
pub struct IsccNbsColor {
    pub id: u32,                    // 1-267
    pub name: String,               // e.g., "vivid red"
    pub alternate_name: Option<String>,
    pub munsell_ranges: Vec<MunsellRange>,
}

pub struct MunsellRange {
    pub hue_start: String,
    pub hue_end: String,
    pub value_min: f64,
    pub value_max: f64,
    pub chroma_min: f64,
    pub chroma_max: f64,
}
```

## Illuminants and Adaptation

### `Illuminant`

Supported standard illuminants.

```rust
pub enum Illuminant {
    /// CIE Standard Illuminant C (average daylight)
    C,
    /// CIE Standard Illuminant D65 (noon daylight)
    D65,
    /// CIE Standard Illuminant F7 (broadband fluorescent)
    F7,
}

impl Illuminant {
    /// Get XYZ tristimulus values
    pub fn xyz(&self) -> [f64; 3]
    
    /// Get xy chromaticity coordinates
    pub fn xy(&self) -> [f64; 2]
    
    /// Get correlated color temperature
    pub fn cct(&self) -> Option<f64>
}
```

### `ChromaticAdaptation`

Chromatic adaptation transforms.

```rust
pub enum ChromaticAdaptation {
    /// Simple XYZ scaling (von Kries)
    XYZScaling,
    /// Bradford transform
    Bradford,
    /// CAT02 transform
    CAT02,
    /// No adaptation
    None,
}

impl ChromaticAdaptation {
    /// Adapt XYZ values between illuminants
    pub fn adapt(
        &self,
        xyz: [f64; 3],
        from: Illuminant,
        to: Illuminant
    ) -> [f64; 3]
}
```

## Error Handling

### `MunsellError`

Custom error type for all operations.

```rust
#[derive(Debug, thiserror::Error)]
pub enum MunsellError {
    #[error("Invalid RGB values: {0}")]
    InvalidRgb(String),
    
    #[error("Invalid Munsell notation: {0}")]
    InvalidNotation(String),
    
    #[error("Color out of gamut: {0}")]
    OutOfGamut(String),
    
    #[error("Invalid hex color: {0}")]
    InvalidHex(String),
    
    #[error("ISCC-NBS classification failed: {0}")]
    ClassificationError(String),
    
    #[error("IO error: {0}")]
    IoError(#[from] std::io::Error),
    
    #[error("Parse error: {0}")]
    ParseError(String),
}

pub type Result<T> = std::result::Result<T, MunsellError>;
```

## Advanced Features

### Thread Safety

All public types implement `Send + Sync`:

```rust
use std::sync::Arc;
use std::thread;

let converter = Arc::new(MunsellConverter::new()?);
let mut handles = vec![];

for i in 0..4 {
    let conv = Arc::clone(&converter);
    handles.push(thread::spawn(move || {
        conv.srgb_to_munsell([255, 0, 0])
    }));
}
```

### Caching

Automatic caching of conversion results:

```rust
let converter = MunsellConverter::with_config(ConverterConfig {
    cache_size: 5000,  // Cache up to 5000 colors
    ..Default::default()
})?;

// First call computes
let color1 = converter.srgb_to_munsell([255, 0, 0])?;

// Second call uses cache
let color2 = converter.srgb_to_munsell([255, 0, 0])?;
```

### Parallel Processing

```rust
use rayon::prelude::*;

let colors: Vec<[u8; 3]> = generate_colors();

// Automatic parallel processing for large batches
let results = converter.convert_batch_parallel(&colors)?;

// Manual parallel processing
let results: Vec<MunsellColor> = colors
    .par_iter()
    .map(|rgb| converter.srgb_to_munsell(*rgb))
    .collect::<Result<Vec<_>>>()?;
```

## Examples

### Basic Color Conversion

```rust
use munsellspace::MunsellConverter;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let converter = MunsellConverter::new()?;
    
    // Pure colors
    let red = converter.srgb_to_munsell([255, 0, 0])?;
    println!("Red: {}", red);  // 7.9R 5.2/20.5
    
    let green = converter.srgb_to_munsell([0, 255, 0])?;
    println!("Green: {}", green);  // 7.5GY 8.7/11.1
    
    let blue = converter.srgb_to_munsell([0, 0, 255])?;
    println!("Blue: {}", blue);  // 6.7PB 3.1/12.5
    
    // Neutral colors
    let gray = converter.srgb_to_munsell([128, 128, 128])?;
    println!("Gray: {}", gray);  // N 5.0/
    
    Ok(())
}
```

### ISCC-NBS Classification

```rust
use munsellspace::ISCC_NBS_Classifier;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let classifier = ISCC_NBS_Classifier::new()?;
    
    // Classify colors
    let red_name = classifier.classify_rgb([255, 0, 0])?;
    println!("Red: {} (ID: {})", red_name.name, red_name.id);
    
    let navy_name = classifier.classify_rgb([0, 0, 128])?;
    println!("Navy: {} (ID: {})", navy_name.name, navy_name.id);
    
    // Find specific color
    if let Some(color) = classifier.get_color_by_name("vivid red") {
        println!("Vivid red ID: {}", color.id);
    }
    
    Ok(())
}
```

### Working with Different Illuminants

```rust
use munsellspace::{MunsellConverter, ConverterConfig, Illuminant, ChromaticAdaptation};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Illuminant C (traditional)
    let conv_c = MunsellConverter::with_config(ConverterConfig {
        illuminant: Illuminant::C,
        adaptation: ChromaticAdaptation::Bradford,
        ..Default::default()
    })?;
    
    // Illuminant F7 (fluorescent)
    let conv_f7 = MunsellConverter::with_config(ConverterConfig {
        illuminant: Illuminant::F7,
        adaptation: ChromaticAdaptation::CAT02,
        ..Default::default()
    })?;
    
    let rgb = [200, 150, 100];
    
    let munsell_c = conv_c.srgb_to_munsell(rgb)?;
    let munsell_f7 = conv_f7.srgb_to_munsell(rgb)?;
    
    println!("Under C: {}", munsell_c);
    println!("Under F7: {}", munsell_f7);
    
    Ok(())
}
```

### Batch Processing

```rust
use munsellspace::MunsellConverter;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let converter = MunsellConverter::new()?;
    
    // Generate color palette
    let palette: Vec<[u8; 3]> = (0..256).step_by(32)
        .flat_map(|r| (0..256).step_by(32)
            .flat_map(move |g| (0..256).step_by(32)
                .map(move |b| [r as u8, g as u8, b as u8])))
        .collect();
    
    // Convert all at once (uses parallel processing automatically)
    let munsell_colors = converter.convert_batch_parallel(&palette)?;
    
    for (rgb, munsell) in palette.iter().zip(munsell_colors.iter()) {
        println!("RGB{:?} -> {}", rgb, munsell);
    }
    
    Ok(())
}
```

### Error Handling

```rust
use munsellspace::{MunsellConverter, MunsellError};

fn convert_color(rgb: [u8; 3]) -> Result<String, MunsellError> {
    let converter = MunsellConverter::new()?;
    let munsell = converter.srgb_to_munsell(rgb)?;
    Ok(munsell.notation)
}

fn main() {
    match convert_color([255, 0, 0]) {
        Ok(notation) => println!("Success: {}", notation),
        Err(MunsellError::InvalidRgb(msg)) => eprintln!("Invalid RGB: {}", msg),
        Err(MunsellError::OutOfGamut(msg)) => eprintln!("Out of gamut: {}", msg),
        Err(e) => eprintln!("Error: {}", e),
    }
}
```

### Custom Types Integration

```rust
use munsellspace::{MunsellConverter, MunsellColor};

// Your custom color type
struct MyColor {
    r: f32,
    g: f32,
    b: f32,
}

impl MyColor {
    fn to_munsell(&self) -> Result<MunsellColor, Box<dyn std::error::Error>> {
        let converter = MunsellConverter::new()?;
        let rgb = [
            (self.r * 255.0) as u8,
            (self.g * 255.0) as u8,
            (self.b * 255.0) as u8,
        ];
        Ok(converter.srgb_to_munsell(rgb)?)
    }
}
```

## Performance Tips

1. **Reuse Converters**: Create once, use many times
2. **Batch Processing**: Use `convert_batch_parallel()` for large datasets
3. **Configure Cache**: Adjust cache size based on your usage patterns
4. **Thread Sharing**: Use `Arc<T>` for multi-threaded scenarios
5. **Illuminant Choice**: D65 is fastest (native sRGB), C and F7 require adaptation

## Further Reading

- [Munsell Color System](https://en.wikipedia.org/wiki/Munsell_color_system)
- [ISCC-NBS System](https://en.wikipedia.org/wiki/ISCC%E2%80%93NBS_system)
- [CIE Color Spaces](https://en.wikipedia.org/wiki/CIE_1931_color_space)
- [Python Colour Science](https://github.com/colour-science/colour)

---

This API documentation is based on the MunsellSpace library implementation, which derives its mathematical algorithms from the Python Colour Science library.