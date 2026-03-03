//! Centroid specifications from Centore (2020) Table 1.
//!
//! These are the focal colors for each semantic overlay.

use super::types::MunsellSpec;
use super::parsing::parse_munsell_notation;

/// Parse a Munsell notation to MunsellSpec, panicking on error.
fn spec(notation: &str) -> MunsellSpec {
    parse_munsell_notation(notation)
        .unwrap_or_else(|| panic!("Invalid centroid notation: {}", notation))
}

// ========================================================================
// 20 Non-Basic Color Centroids
// ========================================================================

/// Aqua: 7.4BG 6.2/3.4
pub fn aqua() -> MunsellSpec { spec("7.4BG 6.2/3.4") }
/// Beige: 6.7YR 6.1/3.4
pub fn beige() -> MunsellSpec { spec("6.7YR 6.1/3.4") }
/// Coral: 6.5R 5.8/8.3
pub fn coral() -> MunsellSpec { spec("6.5R 5.8/8.3") }
/// Fuchsia: 4.8RP 4.1/10.3
pub fn fuchsia() -> MunsellSpec { spec("4.8RP 4.1/10.3") }
/// Gold: 9.8YR 6.4/7.4
pub fn gold() -> MunsellSpec { spec("9.8YR 6.4/7.4") }
/// Lavender: 5.6P 5.4/4.8
pub fn lavender() -> MunsellSpec { spec("5.6P 5.4/4.8") }
/// Lilac: 7.8P 5.6/4.8
pub fn lilac() -> MunsellSpec { spec("7.8P 5.6/4.8") }
/// Magenta: 3.8RP 3.4/9.4
pub fn magenta() -> MunsellSpec { spec("3.8RP 3.4/9.4") }
/// Mauve: 1.2RP 5.1/3.9
pub fn mauve() -> MunsellSpec { spec("1.2RP 5.1/3.9") }
/// Navy: 7.3PB 2.1/3.6
pub fn navy() -> MunsellSpec { spec("7.3PB 2.1/3.6") }
/// Peach: 2.9YR 7.0/5.9
pub fn peach() -> MunsellSpec { spec("2.9YR 7.0/5.9") }
/// Rose: 0.5R 5.0/7.7
pub fn rose() -> MunsellSpec { spec("0.5R 5.0/7.7") }
/// Rust: 9.4R 3.9/7.4
pub fn rust() -> MunsellSpec { spec("9.4R 3.9/7.4") }
/// Sand: 7.6YR 6.3/3.2
pub fn sand() -> MunsellSpec { spec("7.6YR 6.3/3.2") }
/// Tan: 6.3YR 5.2/4.1
pub fn tan() -> MunsellSpec { spec("6.3YR 5.2/4.1") }
/// Taupe: 3.2YR 4.7/1.4
pub fn taupe() -> MunsellSpec { spec("3.2YR 4.7/1.4") }
/// Teal: 1.6B 3.3/4.5
pub fn teal() -> MunsellSpec { spec("1.6B 3.3/4.5") }
/// Turquoise: 1.6B 5.5/5.9
pub fn turquoise() -> MunsellSpec { spec("1.6B 5.5/5.9") }
/// Violet: 7.0P 3.8/6.2
pub fn violet() -> MunsellSpec { spec("7.0P 3.8/6.2") }
/// Wine: 2.7R 3.0/4.9
pub fn wine() -> MunsellSpec { spec("2.7R 3.0/4.9") }

// ========================================================================
// 10 Basic Color Centroids (computed from polyhedron vertices)
// ========================================================================

/// Blue: 1.8PB 4.8/5.0 (1673 CAUS samples)
pub fn blue() -> MunsellSpec { spec("1.8PB 4.8/5.0") }
/// Brown: 2.2YR 3.5/3.4 (536 CAUS samples)
pub fn brown() -> MunsellSpec { spec("2.2YR 3.5/3.4") }
/// Gray: 3.2Y 5.0/1.9 (485 CAUS samples) - low chroma yellowish
pub fn gray() -> MunsellSpec { spec("3.2Y 5.0/1.9") }
/// Green: 2.3G 5.0/4.0 (1296 CAUS samples)
pub fn green() -> MunsellSpec { spec("2.3G 5.0/4.0") }
/// Orange: 2.5YR 6.1/10.3 (378 CAUS samples)
pub fn orange() -> MunsellSpec { spec("2.5YR 6.1/10.3") }
/// Pink: 0.7R 6.1/7.2 (594 CAUS samples)
pub fn pink() -> MunsellSpec { spec("0.7R 6.1/7.2") }
/// Purple: 4.3P 3.0/6.5 (226 CAUS samples)
pub fn purple() -> MunsellSpec { spec("4.3P 3.0/6.5") }
/// Red: 5.1R 3.9/9.6 (662 CAUS samples)
pub fn red() -> MunsellSpec { spec("5.1R 3.9/9.6") }
/// White: 2.2Y 8.3/1.6 (152 CAUS samples) - low chroma yellowish
pub fn white() -> MunsellSpec { spec("2.2Y 8.3/1.6") }
/// Yellow: 3.9Y 7.8/8.0 (394 CAUS samples)
pub fn yellow() -> MunsellSpec { spec("3.9Y 7.8/8.0") }

/// Get centroid by name (case-insensitive).
pub fn get(name: &str) -> Option<MunsellSpec> {
    match name.to_lowercase().as_str() {
        "aqua" => Some(aqua()),
        "beige" => Some(beige()),
        "coral" => Some(coral()),
        "fuchsia" => Some(fuchsia()),
        "gold" => Some(gold()),
        "lavender" => Some(lavender()),
        "lilac" => Some(lilac()),
        "magenta" => Some(magenta()),
        "mauve" => Some(mauve()),
        "navy" => Some(navy()),
        "peach" => Some(peach()),
        "rose" => Some(rose()),
        "rust" => Some(rust()),
        "sand" => Some(sand()),
        "tan" => Some(tan()),
        "taupe" => Some(taupe()),
        "teal" => Some(teal()),
        "turquoise" => Some(turquoise()),
        "violet" => Some(violet()),
        "wine" => Some(wine()),
        // Basic colors
        "blue" => Some(blue()),
        "brown" => Some(brown()),
        "gray" | "grey" => Some(gray()),
        "green" => Some(green()),
        "orange" => Some(orange()),
        "pink" => Some(pink()),
        "purple" => Some(purple()),
        "red" => Some(red()),
        "white" => Some(white()),
        "yellow" => Some(yellow()),
        _ => None,
    }
}
