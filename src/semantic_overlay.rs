//! Semantic overlay functionality for non-basic color names.
//!
//! This module implements semantic color naming based on Paul Centore's 2020 paper
//! "Beige, aqua, fuchsia, etc.: Definitions for some non-basic surface colour names"
//! (Journal of the American Institute for Conservation, 25:3, 37-56).
//!
//! The methodology uses convex polyhedra in 3D Munsell space to define color name regions,
//! with point-in-polyhedron tests for membership determination.

use std::f64::consts::PI;

/// Munsell hue families in clockwise order starting from R.
/// Each family spans 4 hue steps (0-10 within family maps to 0-4 in absolute numbering).
pub const HUE_FAMILIES: [&str; 10] = ["R", "YR", "Y", "GY", "G", "BG", "B", "PB", "P", "RP"];

/// Represents a point in 3D Munsell Cartesian space.
///
/// Coordinates are derived from cylindrical Munsell (H, V, C) where:
/// - x = chroma * cos(theta)
/// - y = chroma * sin(theta)
/// - z = value
///
/// Theta is calculated from hue number: theta = hue_number * 9 degrees
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct MunsellCartesian {
    /// X coordinate (chroma * cos(hue_angle))
    pub x: f64,
    /// Y coordinate (chroma * sin(hue_angle))
    pub y: f64,
    /// Z coordinate (value, 0-10)
    pub z: f64,
}

impl MunsellCartesian {
    /// Create a new Cartesian coordinate.
    pub fn new(x: f64, y: f64, z: f64) -> Self {
        Self { x, y, z }
    }

    /// Calculate Euclidean distance to another point.
    pub fn distance(&self, other: &MunsellCartesian) -> f64 {
        let dx = self.x - other.x;
        let dy = self.y - other.y;
        let dz = self.z - other.z;
        (dx * dx + dy * dy + dz * dz).sqrt()
    }
}

/// Represents a Munsell color specification with numeric hue.
///
/// This is used internally for polyhedron calculations where we need
/// the hue as a continuous number (0-40) rather than a string.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct MunsellSpec {
    /// Hue as a number from 0-40 (continuous around the hue circle).
    /// 0 = 10RP, 4 = 10R, 8 = 10YR, etc.
    /// Each integer step represents 2.5 hue units.
    pub hue_number: f64,
    /// Value (lightness) from 0-10.
    pub value: f64,
    /// Chroma (saturation) from 0+.
    pub chroma: f64,
}

impl MunsellSpec {
    /// Create a new Munsell specification.
    pub fn new(hue_number: f64, value: f64, chroma: f64) -> Self {
        Self {
            hue_number,
            value,
            chroma,
        }
    }

    /// Create a neutral (achromatic) Munsell specification.
    pub fn neutral(value: f64) -> Self {
        Self {
            hue_number: 0.0,
            value,
            chroma: 0.0,
        }
    }

    /// Convert to 3D Cartesian coordinates for polyhedron math.
    ///
    /// The conversion follows Centore's methodology:
    /// - Hue angle: theta = hue_number * 9 degrees (40 steps = 360 degrees)
    /// - x = chroma * cos(theta)
    /// - y = chroma * sin(theta)
    /// - z = value
    pub fn to_cartesian(&self) -> MunsellCartesian {
        let theta = self.hue_number * 9.0 * PI / 180.0;
        MunsellCartesian {
            x: self.chroma * theta.cos(),
            y: self.chroma * theta.sin(),
            z: self.value,
        }
    }

    /// Create from 3D Cartesian coordinates.
    ///
    /// This is the inverse of `to_cartesian()`.
    pub fn from_cartesian(cart: &MunsellCartesian) -> Self {
        let chroma = (cart.x * cart.x + cart.y * cart.y).sqrt();

        // Handle achromatic case
        if chroma < 1e-10 {
            return Self::neutral(cart.z);
        }

        // Calculate hue angle from x, y
        let mut theta = cart.y.atan2(cart.x);
        if theta < 0.0 {
            theta += 2.0 * PI;
        }

        // Convert radians to hue number (0-40)
        let hue_number = theta * 180.0 / PI / 9.0;

        Self {
            hue_number: hue_number % 40.0,
            value: cart.z,
            chroma,
        }
    }

    /// Convert to Munsell notation string.
    ///
    /// # Returns
    /// String like "5R 4.0/12.0" or "N 5.0/" for neutral colors.
    pub fn to_notation(&self) -> String {
        if self.chroma < 0.5 {
            return format!("N {:.1}/", self.value);
        }

        let (hue_str, _) = hue_number_to_string(self.hue_number);
        format!("{} {:.1}/{:.1}", hue_str, self.value, self.chroma)
    }

    /// Distance from centroid (for finding closest overlay).
    pub fn distance_from(&self, other: &MunsellSpec) -> f64 {
        self.to_cartesian().distance(&other.to_cartesian())
    }
}

/// Parse a Munsell hue string to a numeric hue value (0-40).
///
/// The Munsell hue circle has 40 steps:
/// - 0 = 10RP (wraps to start)
/// - 4 = 10R
/// - 8 = 10YR
/// - 12 = 10Y
/// - 16 = 10GY
/// - 20 = 10G
/// - 24 = 10BG
/// - 28 = 10B
/// - 32 = 10PB
/// - 36 = 10P
///
/// Each step represents 2.5 hue units within a family.
///
/// # Arguments
/// * `hue` - Munsell hue string like "5R", "2.5YR", "10PB"
///
/// # Returns
/// Hue number from 0-40, or None if parsing fails.
///
/// # Examples
/// ```
/// use munsellspace::semantic_overlay::parse_hue_to_number;
///
/// assert!((parse_hue_to_number("5R").unwrap() - 2.0).abs() < 0.001);
/// assert!((parse_hue_to_number("10R").unwrap() - 4.0).abs() < 0.001);
/// assert!((parse_hue_to_number("2.5YR").unwrap() - 5.0).abs() < 0.001);
/// ```
pub fn parse_hue_to_number(hue: &str) -> Option<f64> {
    // Find which family by checking suffixes (longest first to handle "PB" vs "B")
    let families_by_length: [&str; 10] = ["YR", "GY", "BG", "PB", "RP", "R", "Y", "G", "B", "P"];

    let (family, family_idx) = families_by_length
        .iter()
        .find_map(|&fam| {
            if hue.ends_with(fam) {
                let idx = HUE_FAMILIES.iter().position(|&f| f == fam)?;
                Some((fam, idx))
            } else {
                None
            }
        })?;

    // Extract the numeric part
    let num_str = hue.strip_suffix(family)?;
    let num: f64 = num_str.parse().ok()?;

    // Validate range
    if !(0.0..=10.0).contains(&num) {
        return None;
    }

    // Calculate hue number
    // Each family starts at family_idx * 4 (e.g., R=0*4=0, YR=1*4=4, Y=2*4=8, ...)
    // Within each family, 10 = next family start, 0 = previous family end
    // So 5R = 0 + 5/2.5 = 2, 10R = 0 + 10/2.5 = 4
    let family_start = family_idx as f64 * 4.0;
    let hue_number = (family_start + num / 2.5) % 40.0;

    Some(hue_number)
}

/// Convert a numeric hue (0-40) back to a Munsell hue string.
///
/// # Arguments
/// * `hue_number` - Hue value from 0-40
///
/// # Returns
/// Tuple of (hue_string, family_letter) like ("5R", "R")
///
/// # Examples
/// ```
/// use munsellspace::semantic_overlay::hue_number_to_string;
///
/// let (hue, family) = hue_number_to_string(2.0);
/// assert_eq!(hue, "5R");
/// assert_eq!(family, "R");
/// ```
pub fn hue_number_to_string(hue_number: f64) -> (String, &'static str) {
    // Normalize to 0-40
    let normalized = ((hue_number % 40.0) + 40.0) % 40.0;

    // Calculate within-family position first (0-10 range, where 10 wraps to next family)
    let within_family = (normalized % 4.0) * 2.5;

    // Handle edge case: if within_family is very close to 0, use 10 of PREVIOUS family
    let (final_family_idx, final_num) = if within_family < 0.001 && normalized > 0.001 {
        // At boundary (e.g., hue 32) - use 10 of previous family (e.g., 10PB not 0P)
        let prev_family_idx = ((normalized / 4.0).floor() as usize + 9) % 10;
        (prev_family_idx, 10.0_f64)
    } else if within_family < 0.001 {
        // At hue 0 (10RP)
        (9, 10.0_f64) // 10RP
    } else {
        // Normal case
        let family_idx = (normalized / 4.0).floor() as usize % 10;
        (family_idx, within_family)
    };

    let final_family = HUE_FAMILIES[final_family_idx % 10];

    // Format the hue string
    let hue_str = if (final_num - final_num.round()).abs() < 0.001 {
        format!("{}{}", final_num.round() as i32, final_family)
    } else {
        format!("{:.1}{}", final_num, final_family)
    };

    (hue_str, final_family)
}

/// Parse a full Munsell notation string to MunsellSpec.
///
/// # Arguments
/// * `notation` - Munsell notation like "5R 4.0/12.0" or "N 5.0/"
///
/// # Returns
/// MunsellSpec or None if parsing fails.
pub fn parse_munsell_notation(notation: &str) -> Option<MunsellSpec> {
    let notation = notation.trim();

    // Handle neutral colors
    if notation.starts_with("N ") {
        let value_str = notation.strip_prefix("N ")?.trim_end_matches('/');
        let value: f64 = value_str.parse().ok()?;
        return Some(MunsellSpec::neutral(value));
    }

    // Parse chromatic: "5R 4.0/12.0"
    let parts: Vec<&str> = notation.split_whitespace().collect();
    if parts.len() != 2 {
        return None;
    }

    let hue_number = parse_hue_to_number(parts[0])?;

    let vc_parts: Vec<&str> = parts[1].split('/').collect();
    if vc_parts.len() != 2 {
        return None;
    }

    let value: f64 = vc_parts[0].parse().ok()?;
    let chroma: f64 = vc_parts[1].parse().ok()?;

    Some(MunsellSpec::new(hue_number, value, chroma))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_hue_to_number_basic() {
        // Test basic hue families at 5
        assert!((parse_hue_to_number("5R").unwrap() - 2.0).abs() < 0.001);
        assert!((parse_hue_to_number("5YR").unwrap() - 6.0).abs() < 0.001);
        assert!((parse_hue_to_number("5Y").unwrap() - 10.0).abs() < 0.001);
        assert!((parse_hue_to_number("5GY").unwrap() - 14.0).abs() < 0.001);
        assert!((parse_hue_to_number("5G").unwrap() - 18.0).abs() < 0.001);
        assert!((parse_hue_to_number("5BG").unwrap() - 22.0).abs() < 0.001);
        assert!((parse_hue_to_number("5B").unwrap() - 26.0).abs() < 0.001);
        assert!((parse_hue_to_number("5PB").unwrap() - 30.0).abs() < 0.001);
        assert!((parse_hue_to_number("5P").unwrap() - 34.0).abs() < 0.001);
        assert!((parse_hue_to_number("5RP").unwrap() - 38.0).abs() < 0.001);
    }

    #[test]
    fn test_hue_to_number_boundaries() {
        // Test family boundaries (10 of one = 0 of next)
        assert!((parse_hue_to_number("10R").unwrap() - 4.0).abs() < 0.001);
        assert!((parse_hue_to_number("10YR").unwrap() - 8.0).abs() < 0.001);
        assert!((parse_hue_to_number("10RP").unwrap() - 0.0).abs() < 0.001); // Wraps to 0
    }

    #[test]
    fn test_hue_to_number_fractional() {
        assert!((parse_hue_to_number("2.5R").unwrap() - 1.0).abs() < 0.001);
        assert!((parse_hue_to_number("7.5R").unwrap() - 3.0).abs() < 0.001);
        assert!((parse_hue_to_number("2.5YR").unwrap() - 5.0).abs() < 0.001);
    }

    #[test]
    fn test_hue_to_number_invalid() {
        assert!(parse_hue_to_number("").is_none());
        assert!(parse_hue_to_number("R").is_none());
        assert!(parse_hue_to_number("11R").is_none());
        assert!(parse_hue_to_number("-1R").is_none());
        assert!(parse_hue_to_number("5X").is_none());
    }

    #[test]
    fn test_hue_number_to_string() {
        let (hue, _) = hue_number_to_string(2.0);
        assert_eq!(hue, "5R");

        let (hue, _) = hue_number_to_string(6.0);
        assert_eq!(hue, "5YR");

        let (hue, _) = hue_number_to_string(1.0);
        assert!(hue.contains("R")); // 2.5R
    }

    #[test]
    fn test_roundtrip_hue_conversion() {
        // Test that parsing and converting back gives the same result
        let test_hues = ["5R", "2.5YR", "7.5BG", "10PB", "5RP"];

        for hue in &test_hues {
            let num = parse_hue_to_number(hue).unwrap();
            let (back, _) = hue_number_to_string(num);
            let num2 = parse_hue_to_number(&back).unwrap();
            assert!((num - num2).abs() < 0.001, "Roundtrip failed for {}: {} -> {} -> {}", hue, num, back, num2);
        }
    }

    #[test]
    fn test_cartesian_conversion() {
        // Test conversion at known points
        let spec = MunsellSpec::new(0.0, 5.0, 10.0); // 10RP at value 5, chroma 10
        let cart = spec.to_cartesian();

        // At hue 0, angle is 0, so x = chroma, y = 0
        assert!((cart.x - 10.0).abs() < 0.001);
        assert!(cart.y.abs() < 0.001);
        assert!((cart.z - 5.0).abs() < 0.001);

        // Test at 90 degrees (hue 10 = 10Y)
        let spec90 = MunsellSpec::new(10.0, 5.0, 10.0);
        let cart90 = spec90.to_cartesian();
        assert!(cart90.x.abs() < 0.001); // cos(90) = 0
        assert!((cart90.y - 10.0).abs() < 0.001); // sin(90) = 1
    }

    #[test]
    fn test_cartesian_roundtrip() {
        let original = MunsellSpec::new(15.0, 6.0, 8.0);
        let cart = original.to_cartesian();
        let recovered = MunsellSpec::from_cartesian(&cart);

        assert!((original.hue_number - recovered.hue_number).abs() < 0.001);
        assert!((original.value - recovered.value).abs() < 0.001);
        assert!((original.chroma - recovered.chroma).abs() < 0.001);
    }

    #[test]
    fn test_neutral_cartesian() {
        let neutral = MunsellSpec::neutral(5.0);
        let cart = neutral.to_cartesian();

        assert!(cart.x.abs() < 0.001);
        assert!(cart.y.abs() < 0.001);
        assert!((cart.z - 5.0).abs() < 0.001);

        let recovered = MunsellSpec::from_cartesian(&cart);
        assert!(recovered.chroma < 0.001);
    }

    #[test]
    fn test_parse_munsell_notation() {
        let spec = parse_munsell_notation("5R 4.0/12.0").unwrap();
        assert!((spec.hue_number - 2.0).abs() < 0.001);
        assert!((spec.value - 4.0).abs() < 0.001);
        assert!((spec.chroma - 12.0).abs() < 0.001);

        let neutral = parse_munsell_notation("N 5.0/").unwrap();
        assert!(neutral.chroma < 0.001);
        assert!((neutral.value - 5.0).abs() < 0.001);
    }

    #[test]
    fn test_to_notation() {
        let spec = MunsellSpec::new(2.0, 4.0, 12.0);
        let notation = spec.to_notation();
        assert!(notation.contains("R"));
        assert!(notation.contains("4.0"));
        assert!(notation.contains("12.0"));

        let neutral = MunsellSpec::neutral(5.0);
        let n_notation = neutral.to_notation();
        assert!(n_notation.starts_with("N"));
    }

    #[test]
    fn test_distance() {
        let p1 = MunsellCartesian::new(0.0, 0.0, 0.0);
        let p2 = MunsellCartesian::new(3.0, 4.0, 0.0);
        assert!((p1.distance(&p2) - 5.0).abs() < 0.001);

        let p3 = MunsellCartesian::new(0.0, 0.0, 5.0);
        assert!((p1.distance(&p3) - 5.0).abs() < 0.001);
    }

    #[test]
    fn test_centore_centroids() {
        // Test that Centore's centroids can be parsed and converted
        // Aqua: 7.4BG 6.2/3.4
        let aqua = parse_munsell_notation("7.4BG 6.2/3.4").unwrap();
        assert!((aqua.value - 6.2).abs() < 0.001);
        assert!((aqua.chroma - 3.4).abs() < 0.001);

        // Beige: 6.7YR 6.1/3.4
        let beige = parse_munsell_notation("6.7YR 6.1/3.4").unwrap();
        assert!((beige.value - 6.1).abs() < 0.001);

        // Navy: 7.3PB 2.1/3.6
        let navy = parse_munsell_notation("7.3PB 2.1/3.6").unwrap();
        assert!((navy.value - 2.1).abs() < 0.001);
    }
}
