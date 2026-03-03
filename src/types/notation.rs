//! Munsell notation parsing and validation helpers.

/// Format a Munsell value, dropping the trailing `.0` when the value is an integer.
pub(crate) fn format_value(v: f64) -> String {
    if v.fract() == 0.0 {
        format!("{:.1}", v)
    } else {
        format!("{}", v)
    }
}

/// Split a compact notation like "5R4.0/14.0" into ("5R", "4.0/14.0").
///
/// Finds the boundary where hue-family letters end and the value digits begin.
pub(crate) fn split_hue_from_value(s: &str) -> Option<(String, String)> {
    let upper = s.to_uppercase();
    // Try matching each family (longest first) after a numeric prefix
    let mut families = ["BG", "GY", "YR", "RP", "PB", "B", "G", "Y", "R", "P"];
    families.sort_by_key(|f| std::cmp::Reverse(f.len()));

    for family in &families {
        // Find all occurrences of the family in the string
        if let Some(pos) = upper.find(family) {
            let after_family = pos + family.len();
            // The part before family+letters must be a number (the hue number)
            let numeric_part = &upper[..pos];
            if numeric_part.is_empty() {
                continue;
            }
            if numeric_part.parse::<f64>().is_err() {
                continue;
            }
            // The part after the family must start a value/chroma like "4.0/14.0"
            if after_family < upper.len() {
                let hue = s[..after_family].to_string();
                let rest = s[after_family..].to_string();
                return Some((hue, rest));
            }
        }
    }
    None
}

/// Validates that a hue string has the correct format (number + valid hue family).
pub(crate) fn is_valid_hue_format(hue: &str) -> bool {
    // Valid hue families - order by length (longest first) to avoid matching "B" when we want "PB"
    let mut valid_families = ["R", "YR", "Y", "GY", "G", "BG", "B", "PB", "P", "RP"];
    valid_families.sort_by_key(|s| std::cmp::Reverse(s.len()));

    // Find which family it ends with (checking longest first)
    let family = valid_families.iter()
        .find(|&&family| hue.ends_with(family));

    let family = match family {
        Some(f) => f,
        None => return false,
    };

    // Extract the numeric part
    let numeric_part = hue.strip_suffix(family).unwrap_or("");

    // Check if numeric part is empty or invalid
    if numeric_part.is_empty() {
        return false;
    }

    // Parse numeric part - should be a valid float in range 0.0-10.0 (inclusive)
    match numeric_part.parse::<f64>() {
        Ok(num) => num >= 0.0 && num <= 10.0,
        Err(_) => false,
    }
}
