//! String parsing and formatting functions - exact 1:1 port from Python colour-science
//! Line-by-line port with exact behavior matching

use crate::error::{MunsellError, Result};
use regex::Regex;
use std::collections::HashMap;
use lazy_static::lazy_static;

// Python: MUNSELL_GRAY_PATTERN = r'N(?P<value>[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)'
lazy_static! {
    static ref MUNSELL_GRAY_PATTERN: Regex = Regex::new(
        r"(?i)N(?P<value>[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)"
    ).unwrap();
}

// Python: MUNSELL_COLOUR_PATTERN with all hue families
lazy_static! {
    static ref MUNSELL_COLOUR_PATTERN: Regex = Regex::new(
        r"(?i)(?P<hue>[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)\s*(?P<letter>BG|GY|YR|RP|PB|B|G|Y|R|P)\s*(?P<value>[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)\s*/\s*(?P<chroma>[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)"
    ).unwrap();
}

// Python: MUNSELL_HUE_LETTER_CODES = {'BG': 2, 'GY': 4, 'YR': 6, 'RP': 8, 'PB': 10, 'B': 1, 'G': 3, 'Y': 5, 'R': 7, 'P': 9}
lazy_static! {
    static ref MUNSELL_HUE_LETTER_CODES: HashMap<&'static str, u8> = {
        let mut m = HashMap::new();
        m.insert("BG", 2);
        m.insert("GY", 4);
        m.insert("YR", 6);
        m.insert("RP", 8);
        m.insert("PB", 10);
        m.insert("B", 1);
        m.insert("G", 3);
        m.insert("Y", 5);
        m.insert("R", 7);
        m.insert("P", 9);
        m
    };
}

// Reverse mapping for code to letter
lazy_static! {
    static ref CODE_TO_HUE_LETTER: HashMap<u8, &'static str> = {
        let mut m = HashMap::new();
        m.insert(1, "B");
        m.insert(2, "BG");
        m.insert(3, "G");
        m.insert(4, "GY");
        m.insert(5, "Y");
        m.insert(6, "YR");
        m.insert(7, "R");
        m.insert(8, "RP");
        m.insert(9, "P");
        m.insert(10, "PB");
        m
    };
}

/// Parse given Munsell colour and return intermediate Munsell Colorlab specification
/// Exact 1:1 port from Python colour-science parse_munsell_colour
/// 
/// Returns [hue, value, chroma, code] where NaN indicates grey/neutral
pub fn parse_munsell_colour(munsell_colour: &str) -> Result<[f64; 4]> {
    // Python line: match = re.match(MUNSELL_GRAY_PATTERN, munsell_colour, flags=re.IGNORECASE)
    if let Some(captures) = MUNSELL_GRAY_PATTERN.captures(munsell_colour) {
        // Python: return tstack([np.nan, match.group("value"), np.nan, np.nan])
        let value = captures.name("value")
            .ok_or_else(|| MunsellError::InvalidNotation { notation: munsell_colour.to_string(), reason: "Invalid format".to_string() })?
            .as_str()
            .parse::<f64>()
            .map_err(|_| MunsellError::InvalidNotation { notation: munsell_colour.to_string(), reason: "Invalid format".to_string() })?;
        
        return Ok([f64::NAN, value, f64::NAN, f64::NAN]);
    }
    
    // Python line: match = re.match(MUNSELL_COLOUR_PATTERN, munsell_colour, flags=re.IGNORECASE)
    if let Some(captures) = MUNSELL_COLOUR_PATTERN.captures(munsell_colour) {
        // Python: return tstack([
        //     match.group("hue"),
        //     match.group("value"),
        //     match.group("chroma"),
        //     MUNSELL_HUE_LETTER_CODES[match.group("letter").upper()]
        // ])
        
        let hue = captures.name("hue")
            .ok_or_else(|| MunsellError::InvalidNotation { notation: munsell_colour.to_string(), reason: "Invalid format".to_string() })?
            .as_str()
            .parse::<f64>()
            .map_err(|_| MunsellError::InvalidNotation { notation: munsell_colour.to_string(), reason: "Invalid format".to_string() })?;
            
        let value = captures.name("value")
            .ok_or_else(|| MunsellError::InvalidNotation { notation: munsell_colour.to_string(), reason: "Invalid format".to_string() })?
            .as_str()
            .parse::<f64>()
            .map_err(|_| MunsellError::InvalidNotation { notation: munsell_colour.to_string(), reason: "Invalid format".to_string() })?;
            
        let chroma = captures.name("chroma")
            .ok_or_else(|| MunsellError::InvalidNotation { notation: munsell_colour.to_string(), reason: "Invalid format".to_string() })?
            .as_str()
            .parse::<f64>()
            .map_err(|_| MunsellError::InvalidNotation { notation: munsell_colour.to_string(), reason: "Invalid format".to_string() })?;
            
        let letter = captures.name("letter")
            .ok_or_else(|| MunsellError::InvalidNotation { notation: munsell_colour.to_string(), reason: "Invalid format".to_string() })?
            .as_str()
            .to_uppercase();
            
        let code = *MUNSELL_HUE_LETTER_CODES.get(letter.as_str())
            .ok_or_else(|| MunsellError::InvalidNotation { notation: munsell_colour.to_string(), reason: "Invalid format".to_string() })?;
        
        return Ok([hue, value, chroma, code as f64]);
    }
    
    // Python: raise ValueError(f'"{munsell_colour}" is not a valid "Munsell Renotation System" colour specification!')
    Err(MunsellError::InvalidNotation {
        notation: munsell_colour.to_string(),
        reason: "Does not match Munsell notation pattern".to_string()
    })
}

/// Convert Munsell colour string to normalised Munsell specification
/// Exact 1:1 port from Python colour-science munsell_colour_to_munsell_specification
pub fn munsell_colour_to_munsell_specification(munsell_colour: &str) -> Result<[f64; 4]> {
    // Python: return normalise_munsell_specification(parse_munsell_colour(munsell_colour))
    let spec = parse_munsell_colour(munsell_colour)?;
    Ok(crate::python_port::normalise_munsell_specification(&spec))
}

/// Convert Munsell specification to Munsell colour string
/// Exact 1:1 port from Python colour-science munsell_specification_to_munsell_colour
pub fn munsell_specification_to_munsell_colour(
    specification: &[f64; 4],
    hue_decimals: usize,
    value_decimals: usize,
    chroma_decimals: usize,
) -> Result<String> {
    // Python: hue, value, chroma, code = tsplit(normalise_munsell_specification(specification))
    let spec = crate::python_port::normalise_munsell_specification(specification);
    let hue = spec[0];
    let value = spec[1];
    let chroma = spec[2];
    let code = spec[3] as u8;
    
    // Python: if is_grey_munsell_colour(specification):
    if crate::python_port::is_grey_munsell_colour(&spec) {
        // Python: return MUNSELL_GRAY_EXTENDED_FORMAT.format(value, value_decimals)
        // Format: 'N {0:.{1}f}' where {0} is value, {1} is decimals
        // Note: Python uses 'N {value}' with a space after N
        return Ok(format!("N {:.prec$}", value, prec = value_decimals));
    } else {
        // Python: hue = round(hue, hue_decimals)
        let hue = round_to_decimals(hue, hue_decimals);
        
        // Python: attest(0 <= hue <= 10, ...)
        if !(0.0 <= hue && hue <= 10.0) {
            return Err(MunsellError::InvalidNotation {
                notation: format!("{:?}", spec),
                reason: format!("Specification hue must be normalised to domain [0, 10], got {}", hue)
            });
        }
        
        // Python: value = round(value, value_decimals)
        let value = round_to_decimals(value, value_decimals);
        
        // Python: attest(0 <= value <= 10, ...)
        if !(0.0 <= value && value <= 10.0) {
            return Err(MunsellError::InvalidNotation {
                notation: format!("{:?}", spec),
                reason: format!("Specification value must be normalised to domain [0, 10], got {}", value)
            });
        }
        
        // Python: chroma = round(chroma, chroma_decimals)
        let chroma = round_to_decimals(chroma, chroma_decimals);
        
        // Python: attest(2 <= chroma <= 50, ...)
        if !(2.0 <= chroma && chroma <= 50.0) {
            return Err(MunsellError::InvalidNotation {
                notation: format!("{:?}", spec),
                reason: format!("Specification chroma must be normalised to domain [2, 50], got {}", chroma)
            });
        }
        
        // Get hue letter from code
        let hue_letter = CODE_TO_HUE_LETTER.get(&code)
            .ok_or_else(|| MunsellError::InvalidNotation {
                notation: format!("{:?}", spec),
                reason: format!("Invalid hue code: {}", code)
            })?;
        
        // Python format: '{0:.{1}f}{2} {3:.{4}f}/{5:.{6}f}'
        // where: hue, hue_decimals, letter, value, value_decimals, chroma, chroma_decimals
        Ok(format!(
            "{:.h_prec$}{} {:.v_prec$}/{:.c_prec$}",
            hue, hue_letter, value, chroma,
            h_prec = hue_decimals,
            v_prec = value_decimals,
            c_prec = chroma_decimals
        ))
    }
}

/// Convert xyY to Munsell colour string
/// Exact 1:1 port from Python colour-science xyY_to_munsell_colour
pub fn xyy_to_munsell_colour(
    xyy: [f64; 3],
    hue_decimals: usize,
    value_decimals: usize,
    chroma_decimals: usize,
) -> Result<String> {
    // Python: specification = xyY_to_munsell_specification(xyY)
    let specification = crate::python_port::xyy_to_munsell_specification(xyy)?;
    
    // Python: return munsell_specification_to_munsell_colour(
    //     specification, hue_decimals, value_decimals, chroma_decimals)
    munsell_specification_to_munsell_colour(
        &specification,
        hue_decimals,
        value_decimals,
        chroma_decimals
    )
}

/// Convert Munsell colour string to xyY
/// Exact 1:1 port from Python colour-science munsell_colour_to_xyY
pub fn munsell_colour_to_xyy(munsell_colour: &str) -> Result<[f64; 3]> {
    // Python: specification = munsell_colour_to_munsell_specification(munsell_colour)
    let specification = munsell_colour_to_munsell_specification(munsell_colour)?;
    
    // Python: return munsell_specification_to_xyY(specification)
    crate::python_port::munsell_specification_to_xyy(&specification)
}

// Helper function for rounding to specific decimal places
fn round_to_decimals(value: f64, decimals: usize) -> f64 {
    let multiplier = 10_f64.powi(decimals as i32);
    (value * multiplier).round() / multiplier
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_parse_munsell_colour() {
        // Test grey notation
        let grey = parse_munsell_colour("N5.5").unwrap();
        assert!(grey[0].is_nan());
        assert_eq!(grey[1], 5.5);
        assert!(grey[2].is_nan());
        assert!(grey[3].is_nan());
        
        // Test color notation
        let red = parse_munsell_colour("5R 4/10").unwrap();
        assert_eq!(red[0], 5.0);
        assert_eq!(red[1], 4.0);
        assert_eq!(red[2], 10.0);
        assert_eq!(red[3], 7.0); // R = code 7
        
        // Test with decimals
        let yellow_red = parse_munsell_colour("2.5YR 6.5/8.2").unwrap();
        assert_eq!(yellow_red[0], 2.5);
        assert_eq!(yellow_red[1], 6.5);
        assert_eq!(yellow_red[2], 8.2);
        assert_eq!(yellow_red[3], 6.0); // YR = code 6
    }
    
    #[test]
    fn test_munsell_specification_to_munsell_colour() {
        // Test grey
        let grey_spec = [f64::NAN, 5.2, f64::NAN, f64::NAN];
        let grey_str = munsell_specification_to_munsell_colour(&grey_spec, 1, 1, 1).unwrap();
        assert_eq!(grey_str, "N5.2");
        
        // Test color
        let red_spec = [10.0, 2.0, 4.0, 7.0];
        let red_str = munsell_specification_to_munsell_colour(&red_spec, 1, 1, 1).unwrap();
        assert_eq!(red_str, "10.0R 2.0/4.0");
    }
}