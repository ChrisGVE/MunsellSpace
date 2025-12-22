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

// ============================================================================
// Semantic Overlay Data Structures
// ============================================================================

/// A semantic overlay representing a non-basic color name region.
///
/// Based on Centore (2020): Each overlay is defined by a convex polyhedron
/// in 3D Munsell Cartesian space. The polyhedron encloses all colors that
/// can be called by this name.
#[derive(Debug, Clone)]
pub struct SemanticOverlay {
    /// The color name (e.g., "aqua", "beige", "coral")
    pub name: &'static str,
    /// The polyhedron defining the color region
    pub polyhedron: ConvexPolyhedron,
    /// Centroid (focal color) from Centore's Table 1
    pub centroid: MunsellSpec,
    /// Number of samples used to define this region in Centore's study
    pub sample_count: u32,
}

impl SemanticOverlay {
    /// Create a new semantic overlay.
    pub fn new(
        name: &'static str,
        vertices: &[(f64, f64, f64)],
        faces: &[(usize, usize, usize)],
        centroid: MunsellSpec,
        sample_count: u32,
    ) -> Self {
        Self {
            name,
            polyhedron: ConvexPolyhedron::from_arrays(vertices, faces),
            centroid,
            sample_count,
        }
    }

    /// Test if a Munsell color matches this overlay.
    pub fn contains(&self, color: &MunsellSpec) -> bool {
        let point = color.to_cartesian();
        self.polyhedron.contains_point(&point)
    }

    /// Test if a Munsell color matches with tolerance.
    pub fn contains_with_tolerance(&self, color: &MunsellSpec, tolerance: f64) -> bool {
        let point = color.to_cartesian();
        self.polyhedron.contains_point_with_tolerance(&point, tolerance)
    }

    /// Calculate distance from color to centroid.
    pub fn distance_to_centroid(&self, color: &MunsellSpec) -> f64 {
        color.distance_from(&self.centroid)
    }

    /// Get the centroid as a notation string.
    pub fn centroid_notation(&self) -> String {
        self.centroid.to_notation()
    }
}

/// Registry of all semantic overlays.
///
/// This struct holds all 20 non-basic color name overlays from Centore (2020).
#[derive(Debug, Clone)]
pub struct SemanticOverlayRegistry {
    overlays: Vec<SemanticOverlay>,
}

impl SemanticOverlayRegistry {
    /// Create a new registry with the given overlays.
    pub fn new(overlays: Vec<SemanticOverlay>) -> Self {
        Self { overlays }
    }

    /// Get all overlays.
    pub fn all(&self) -> &[SemanticOverlay] {
        &self.overlays
    }

    /// Find an overlay by name (case-insensitive).
    pub fn get(&self, name: &str) -> Option<&SemanticOverlay> {
        let name_lower = name.to_lowercase();
        self.overlays.iter().find(|o| o.name.to_lowercase() == name_lower)
    }

    /// Test if a color matches a specific overlay by name.
    pub fn matches(&self, color: &MunsellSpec, overlay_name: &str) -> bool {
        self.get(overlay_name)
            .map(|o| o.contains(color))
            .unwrap_or(false)
    }

    /// Find all overlays that contain the given color.
    pub fn matching_overlays(&self, color: &MunsellSpec) -> Vec<&SemanticOverlay> {
        self.overlays
            .iter()
            .filter(|o| o.contains(color))
            .collect()
    }

    /// Find the best matching overlay for a color.
    ///
    /// If the color is inside multiple overlays, returns the one with
    /// the closest centroid. If the color is not inside any overlay,
    /// returns None.
    pub fn best_match(&self, color: &MunsellSpec) -> Option<&SemanticOverlay> {
        let matches = self.matching_overlays(color);
        if matches.is_empty() {
            return None;
        }

        matches
            .into_iter()
            .min_by(|a, b| {
                let dist_a = a.distance_to_centroid(color);
                let dist_b = b.distance_to_centroid(color);
                dist_a.partial_cmp(&dist_b).unwrap_or(std::cmp::Ordering::Equal)
            })
    }

    /// Find the closest overlay by centroid distance (even if color is outside).
    pub fn closest_overlay(&self, color: &MunsellSpec) -> Option<(&SemanticOverlay, f64)> {
        self.overlays
            .iter()
            .map(|o| (o, o.distance_to_centroid(color)))
            .min_by(|a, b| a.1.partial_cmp(&b.1).unwrap_or(std::cmp::Ordering::Equal))
    }

    /// Get overlay names.
    pub fn names(&self) -> Vec<&'static str> {
        self.overlays.iter().map(|o| o.name).collect()
    }

    /// Number of overlays in the registry.
    pub fn len(&self) -> usize {
        self.overlays.len()
    }

    /// Check if registry is empty.
    pub fn is_empty(&self) -> bool {
        self.overlays.is_empty()
    }
}

/// The 20 non-basic color names defined by Centore (2020).
pub const OVERLAY_NAMES: [&str; 20] = [
    "aqua", "beige", "coral", "fuchsia", "gold",
    "lavender", "lilac", "magenta", "mauve", "navy",
    "peach", "rose", "rust", "sand", "tan",
    "taupe", "teal", "turquoise", "violet", "wine",
];

/// Centroid specifications from Centore (2020) Table 1.
///
/// These are the focal colors for each semantic overlay.
pub mod centroids {
    use super::MunsellSpec;

    /// Parse a Munsell notation to MunsellSpec, panicking on error.
    fn spec(notation: &str) -> MunsellSpec {
        super::parse_munsell_notation(notation)
            .unwrap_or_else(|| panic!("Invalid centroid notation: {}", notation))
    }

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
            _ => None,
        }
    }
}

// ============================================================================
// Point-in-Polyhedron Algorithm
// ============================================================================

/// A triangular face of a polyhedron, defined by vertex indices.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct TriFace {
    /// Index of first vertex
    pub v0: usize,
    /// Index of second vertex
    pub v1: usize,
    /// Index of third vertex
    pub v2: usize,
}

impl TriFace {
    /// Create a new triangular face from vertex indices.
    pub fn new(v0: usize, v1: usize, v2: usize) -> Self {
        Self { v0, v1, v2 }
    }
}

/// Represents a convex polyhedron defined by vertices and triangular faces.
#[derive(Debug, Clone)]
pub struct ConvexPolyhedron {
    /// Vertices as 3D Cartesian coordinates
    pub vertices: Vec<MunsellCartesian>,
    /// Triangular faces as vertex indices (counter-clockwise when viewed from outside)
    pub faces: Vec<TriFace>,
}

impl ConvexPolyhedron {
    /// Create a new convex polyhedron.
    pub fn new(vertices: Vec<MunsellCartesian>, faces: Vec<TriFace>) -> Self {
        Self { vertices, faces }
    }

    /// Create from arrays of vertex coordinates and face indices.
    ///
    /// # Arguments
    /// * `vertices` - Array of (x, y, z) coordinate tuples
    /// * `faces` - Array of (v0, v1, v2) face index tuples
    pub fn from_arrays(vertices: &[(f64, f64, f64)], faces: &[(usize, usize, usize)]) -> Self {
        let verts: Vec<MunsellCartesian> = vertices
            .iter()
            .map(|(x, y, z)| MunsellCartesian::new(*x, *y, *z))
            .collect();

        let face_list: Vec<TriFace> = faces
            .iter()
            .map(|(v0, v1, v2)| TriFace::new(*v0, *v1, *v2))
            .collect();

        Self::new(verts, face_list)
    }

    /// Calculate the centroid (geometric center) of the polyhedron.
    pub fn centroid(&self) -> MunsellCartesian {
        if self.vertices.is_empty() {
            return MunsellCartesian::new(0.0, 0.0, 0.0);
        }

        let n = self.vertices.len() as f64;
        let sum_x: f64 = self.vertices.iter().map(|v| v.x).sum();
        let sum_y: f64 = self.vertices.iter().map(|v| v.y).sum();
        let sum_z: f64 = self.vertices.iter().map(|v| v.z).sum();

        MunsellCartesian::new(sum_x / n, sum_y / n, sum_z / n)
    }

    /// Test if a point is inside this convex polyhedron.
    ///
    /// Uses the half-space test: for a convex polyhedron, a point is inside
    /// if and only if it is on the interior side of every face plane.
    ///
    /// # Arguments
    /// * `point` - The point to test
    ///
    /// # Returns
    /// `true` if the point is inside the polyhedron, `false` otherwise.
    ///
    /// # Note
    /// Points exactly on the boundary may return either true or false
    /// due to floating-point precision.
    pub fn contains_point(&self, point: &MunsellCartesian) -> bool {
        if self.faces.is_empty() || self.vertices.len() < 4 {
            return false;
        }

        // Calculate centroid to determine which side is "inside"
        let centroid = self.centroid();

        for face in &self.faces {
            let v0 = &self.vertices[face.v0];
            let v1 = &self.vertices[face.v1];
            let v2 = &self.vertices[face.v2];

            // Calculate face normal using cross product of two edges
            let edge1 = (v1.x - v0.x, v1.y - v0.y, v1.z - v0.z);
            let edge2 = (v2.x - v0.x, v2.y - v0.y, v2.z - v0.z);

            let normal = cross_product(edge1, edge2);

            // Calculate plane equation: ax + by + cz + d = 0
            // where (a, b, c) is the normal
            let d = -(normal.0 * v0.x + normal.1 * v0.y + normal.2 * v0.z);

            // Calculate signed distance for the test point and centroid
            let point_side = normal.0 * point.x + normal.1 * point.y + normal.2 * point.z + d;
            let centroid_side = normal.0 * centroid.x + normal.1 * centroid.y + normal.2 * centroid.z + d;

            // Point must be on the same side as centroid (with small epsilon for boundary)
            const EPSILON: f64 = 1e-10;
            if centroid_side > EPSILON {
                // Centroid is on positive side, point should also be positive or nearly zero
                if point_side < -EPSILON {
                    return false;
                }
            } else if centroid_side < -EPSILON {
                // Centroid is on negative side, point should also be negative or nearly zero
                if point_side > EPSILON {
                    return false;
                }
            }
            // If centroid is on the plane (shouldn't happen for valid polyhedra), skip this face
        }

        true
    }

    /// Test if a point is inside with a tolerance for near-boundary points.
    ///
    /// This is useful when testing colors that might be slightly outside
    /// due to measurement or conversion errors.
    ///
    /// # Arguments
    /// * `point` - The point to test
    /// * `tolerance` - Distance tolerance (in Munsell Cartesian units)
    ///
    /// # Returns
    /// `true` if the point is inside or within tolerance of the boundary.
    pub fn contains_point_with_tolerance(&self, point: &MunsellCartesian, tolerance: f64) -> bool {
        if self.contains_point(point) {
            return true;
        }

        // Check if point is within tolerance distance of any vertex
        for vertex in &self.vertices {
            if point.distance(vertex) <= tolerance {
                return true;
            }
        }

        false
    }
}

/// Calculate cross product of two 3D vectors.
fn cross_product(a: (f64, f64, f64), b: (f64, f64, f64)) -> (f64, f64, f64) {
    (
        a.1 * b.2 - a.2 * b.1,
        a.2 * b.0 - a.0 * b.2,
        a.0 * b.1 - a.1 * b.0,
    )
}

/// Test if a point is inside a convex polyhedron (standalone function).
///
/// This is a convenience wrapper around `ConvexPolyhedron::contains_point`.
///
/// # Arguments
/// * `point` - The test point in Cartesian coordinates
/// * `vertices` - Polyhedron vertices as (x, y, z) tuples
/// * `faces` - Triangular faces as (v0, v1, v2) vertex index tuples
///
/// # Returns
/// `true` if the point is inside the polyhedron.
pub fn point_in_polyhedron(
    point: &MunsellCartesian,
    vertices: &[(f64, f64, f64)],
    faces: &[(usize, usize, usize)],
) -> bool {
    let poly = ConvexPolyhedron::from_arrays(vertices, faces);
    poly.contains_point(point)
}

/// Test if a Munsell color is inside a polyhedron (convenience function).
///
/// # Arguments
/// * `color` - The Munsell specification to test
/// * `vertices` - Polyhedron vertices as (x, y, z) tuples
/// * `faces` - Triangular faces as (v0, v1, v2) vertex index tuples
///
/// # Returns
/// `true` if the color is inside the polyhedron.
pub fn munsell_in_polyhedron(
    color: &MunsellSpec,
    vertices: &[(f64, f64, f64)],
    faces: &[(usize, usize, usize)],
) -> bool {
    let point = color.to_cartesian();
    point_in_polyhedron(&point, vertices, faces)
}

#[cfg(test)]
mod tests {
    use super::*;

    // ========================================================================
    // Point-in-Polyhedron Tests
    // ========================================================================

    /// Create a unit cube centered at origin for testing.
    fn unit_cube() -> ConvexPolyhedron {
        let vertices = vec![
            (-0.5, -0.5, -0.5),
            (0.5, -0.5, -0.5),
            (0.5, 0.5, -0.5),
            (-0.5, 0.5, -0.5),
            (-0.5, -0.5, 0.5),
            (0.5, -0.5, 0.5),
            (0.5, 0.5, 0.5),
            (-0.5, 0.5, 0.5),
        ];

        // Faces defined counter-clockwise when viewed from outside
        let faces = vec![
            // Bottom (z = -0.5)
            (0, 2, 1),
            (0, 3, 2),
            // Top (z = 0.5)
            (4, 5, 6),
            (4, 6, 7),
            // Front (y = -0.5)
            (0, 1, 5),
            (0, 5, 4),
            // Back (y = 0.5)
            (2, 3, 7),
            (2, 7, 6),
            // Left (x = -0.5)
            (0, 4, 7),
            (0, 7, 3),
            // Right (x = 0.5)
            (1, 2, 6),
            (1, 6, 5),
        ];

        ConvexPolyhedron::from_arrays(&vertices, &faces)
    }

    /// Create a tetrahedron for testing.
    fn tetrahedron() -> ConvexPolyhedron {
        let vertices = vec![
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
            (0.5, 0.866, 0.0),
            (0.5, 0.289, 0.816),
        ];

        let faces = vec![
            (0, 2, 1), // Bottom
            (0, 1, 3), // Front
            (1, 2, 3), // Right
            (2, 0, 3), // Left
        ];

        ConvexPolyhedron::from_arrays(&vertices, &faces)
    }

    #[test]
    fn test_cube_contains_center() {
        let cube = unit_cube();
        let center = MunsellCartesian::new(0.0, 0.0, 0.0);
        assert!(cube.contains_point(&center));
    }

    #[test]
    fn test_cube_contains_interior_points() {
        let cube = unit_cube();

        // Various interior points
        let points = vec![
            MunsellCartesian::new(0.1, 0.1, 0.1),
            MunsellCartesian::new(-0.2, 0.3, -0.1),
            MunsellCartesian::new(0.4, -0.4, 0.4),
        ];

        for point in &points {
            assert!(cube.contains_point(point), "Point {:?} should be inside cube", point);
        }
    }

    #[test]
    fn test_cube_excludes_exterior_points() {
        let cube = unit_cube();

        // Points clearly outside
        let points = vec![
            MunsellCartesian::new(1.0, 0.0, 0.0),
            MunsellCartesian::new(0.0, 1.0, 0.0),
            MunsellCartesian::new(0.0, 0.0, 1.0),
            MunsellCartesian::new(-1.0, -1.0, -1.0),
        ];

        for point in &points {
            assert!(!cube.contains_point(point), "Point {:?} should be outside cube", point);
        }
    }

    #[test]
    fn test_tetrahedron_contains_centroid() {
        let tet = tetrahedron();
        let centroid = tet.centroid();
        assert!(tet.contains_point(&centroid));
    }

    #[test]
    fn test_tetrahedron_excludes_exterior() {
        let tet = tetrahedron();

        // Point clearly outside
        let outside = MunsellCartesian::new(2.0, 2.0, 2.0);
        assert!(!tet.contains_point(&outside));
    }

    #[test]
    fn test_centroid_calculation() {
        let cube = unit_cube();
        let centroid = cube.centroid();

        // Cube centered at origin should have centroid at (0, 0, 0)
        assert!(centroid.x.abs() < 0.001);
        assert!(centroid.y.abs() < 0.001);
        assert!(centroid.z.abs() < 0.001);
    }

    #[test]
    fn test_point_in_polyhedron_function() {
        let vertices = vec![
            (-1.0, -1.0, -1.0),
            (1.0, -1.0, -1.0),
            (1.0, 1.0, -1.0),
            (-1.0, 1.0, -1.0),
            (-1.0, -1.0, 1.0),
            (1.0, -1.0, 1.0),
            (1.0, 1.0, 1.0),
            (-1.0, 1.0, 1.0),
        ];

        let faces = vec![
            (0, 2, 1), (0, 3, 2),
            (4, 5, 6), (4, 6, 7),
            (0, 1, 5), (0, 5, 4),
            (2, 3, 7), (2, 7, 6),
            (0, 4, 7), (0, 7, 3),
            (1, 2, 6), (1, 6, 5),
        ];

        let inside = MunsellCartesian::new(0.0, 0.0, 0.0);
        let outside = MunsellCartesian::new(5.0, 5.0, 5.0);

        assert!(point_in_polyhedron(&inside, &vertices, &faces));
        assert!(!point_in_polyhedron(&outside, &vertices, &faces));
    }

    #[test]
    fn test_munsell_in_polyhedron() {
        // Create a simple polyhedron around a known color region (high chroma, mid value)
        // This cube spans chroma 5-10 (in x-y plane) and value 4-6 (z axis)
        let vertices = vec![
            (5.0, 0.0, 4.0),
            (10.0, 0.0, 4.0),
            (10.0, 5.0, 4.0),
            (5.0, 5.0, 4.0),
            (5.0, 0.0, 6.0),
            (10.0, 0.0, 6.0),
            (10.0, 5.0, 6.0),
            (5.0, 5.0, 6.0),
        ];

        let faces = vec![
            (0, 2, 1), (0, 3, 2),
            (4, 5, 6), (4, 6, 7),
            (0, 1, 5), (0, 5, 4),
            (2, 3, 7), (2, 7, 6),
            (0, 4, 7), (0, 7, 3),
            (1, 2, 6), (1, 6, 5),
        ];

        // A color that should be inside (chroma ~7, value 5, positive x,y quadrant)
        // 5R (hue 2.0) -> theta = 18 degrees, so x = 7*cos(18) ≈ 6.66, y = 7*sin(18) ≈ 2.16
        let inside_color = MunsellSpec::new(2.0, 5.0, 7.0); // 5R 5.0/7.0
        assert!(munsell_in_polyhedron(&inside_color, &vertices, &faces));

        // A color that should be outside (low chroma - Cartesian coords near origin)
        // x = 1*cos(18) ≈ 0.95, y = 1*sin(18) ≈ 0.31 - outside the x range [5,10]
        let outside_color = MunsellSpec::new(2.0, 5.0, 1.0); // 5R 5.0/1.0
        assert!(!munsell_in_polyhedron(&outside_color, &vertices, &faces));

        // A color outside due to wrong value
        let wrong_value = MunsellSpec::new(2.0, 8.0, 7.0); // 5R 8.0/7.0 - z=8 is outside [4,6]
        assert!(!munsell_in_polyhedron(&wrong_value, &vertices, &faces));
    }

    // ========================================================================
    // SemanticOverlay Data Structure Tests
    // ========================================================================

    #[test]
    fn test_centroid_functions() {
        // Test all centroids can be retrieved
        for name in &super::OVERLAY_NAMES {
            let centroid = super::centroids::get(name);
            assert!(centroid.is_some(), "Centroid for '{}' should exist", name);
        }

        // Test specific centroids
        let aqua = super::centroids::aqua();
        assert!((aqua.value - 6.2).abs() < 0.01);

        let navy = super::centroids::navy();
        assert!((navy.value - 2.1).abs() < 0.01);
    }

    #[test]
    fn test_centroid_get_case_insensitive() {
        assert!(super::centroids::get("AQUA").is_some());
        assert!(super::centroids::get("Aqua").is_some());
        assert!(super::centroids::get("aqua").is_some());
        assert!(super::centroids::get("invalid").is_none());
    }

    #[test]
    fn test_overlay_names_count() {
        assert_eq!(super::OVERLAY_NAMES.len(), 20);
    }

    #[test]
    fn test_semantic_overlay_creation() {
        // Create a simple test overlay
        let vertices = vec![
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
            (0.5, 0.866, 0.0),
            (0.5, 0.289, 0.816),
        ];

        let faces = vec![
            (0, 2, 1),
            (0, 1, 3),
            (1, 2, 3),
            (2, 0, 3),
        ];

        let centroid = MunsellSpec::new(2.0, 5.0, 8.0);
        let overlay = SemanticOverlay::new("test", &vertices, &faces, centroid, 100);

        assert_eq!(overlay.name, "test");
        assert_eq!(overlay.sample_count, 100);
    }

    #[test]
    fn test_registry_basic_operations() {
        // Create a simple test registry
        let vertices = vec![
            (-1.0, -1.0, -1.0),
            (1.0, -1.0, -1.0),
            (1.0, 1.0, -1.0),
            (-1.0, 1.0, -1.0),
            (-1.0, -1.0, 1.0),
            (1.0, -1.0, 1.0),
            (1.0, 1.0, 1.0),
            (-1.0, 1.0, 1.0),
        ];

        let faces = vec![
            (0, 2, 1), (0, 3, 2),
            (4, 5, 6), (4, 6, 7),
            (0, 1, 5), (0, 5, 4),
            (2, 3, 7), (2, 7, 6),
            (0, 4, 7), (0, 7, 3),
            (1, 2, 6), (1, 6, 5),
        ];

        let overlay1 = SemanticOverlay::new(
            "test1",
            &vertices,
            &faces,
            MunsellSpec::new(0.0, 0.0, 0.0),
            50,
        );

        let registry = SemanticOverlayRegistry::new(vec![overlay1]);

        assert_eq!(registry.len(), 1);
        assert!(!registry.is_empty());
        assert!(registry.get("test1").is_some());
        assert!(registry.get("TEST1").is_some()); // Case insensitive
        assert!(registry.get("nonexistent").is_none());
    }

    // ========================================================================
    // Coordinate Conversion Tests
    // ========================================================================

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
