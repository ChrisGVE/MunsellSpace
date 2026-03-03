//! Core mechanical wedge system for hue-based color classification.

use std::collections::HashMap;
use crate::{MunsellError, Result};
use crate::iscc::IsccNbsColor;

/// Mechanical hue wedge distribution system for deterministic ISCC-NBS classification.
///
/// This system partitions the complete Munsell hue circle into 100 wedge containers,
/// each responsible for a specific hue range. It implements deterministic boundary
/// handling to ensure consistent color classification.
///
/// # Architecture
///
/// The system maintains three key data structures:
/// - **Wedge containers**: 100 HashMap entries, each containing color polygons for a hue range
/// - **Hue sequence**: Ordered list of all 100 Munsell hues (1R through 10RP)
/// - **Position lookup**: Fast mapping from hue strings to sequence positions
///
/// # Boundary Rules
///
/// Uses "exclude start, include end" rule for deterministic classification:
/// - Hue exactly at wedge start: belongs to *previous* wedge
/// - Hue exactly at wedge end: belongs to *current* wedge
pub struct MechanicalWedgeSystem {
    /// Map of wedge identifiers to color polygon containers.
    pub(super) wedge_containers: HashMap<String, Vec<IsccNbsColor>>,

    /// Complete ordered sequence of Munsell hue references.
    pub(super) hue_sequence: Vec<String>,

    /// Fast lookup table mapping hue strings to sequence positions.
    pub(super) hue_to_position: HashMap<String, usize>,
}

impl MechanicalWedgeSystem {
    /// Create a new mechanical wedge system with all 100 wedge containers.
    pub fn new() -> Self {
        let hue_sequence = Self::create_reference_hue_sequence();
        let hue_to_position = Self::create_position_lookup(&hue_sequence);
        let wedge_containers = Self::create_all_wedge_containers(&hue_sequence);

        Self {
            wedge_containers,
            hue_sequence,
            hue_to_position,
        }
    }

    /// Create the complete ordered sequence of Munsell hue references.
    pub(super) fn create_reference_hue_sequence() -> Vec<String> {
        let families = ["R", "YR", "Y", "GY", "G", "BG", "B", "PB", "P", "RP"];
        let mut sequence = Vec::with_capacity(100);

        for family in &families {
            for hue_num in 1..=10 {
                sequence.push(format!("{}{}", hue_num, family));
            }
        }

        sequence
    }

    /// Create quick lookup from hue string to sequence position.
    fn create_position_lookup(sequence: &[String]) -> HashMap<String, usize> {
        sequence
            .iter()
            .enumerate()
            .map(|(pos, hue)| (hue.clone(), pos))
            .collect()
    }

    /// Create all 100 wedge containers (empty initially).
    fn create_all_wedge_containers(sequence: &[String]) -> HashMap<String, Vec<IsccNbsColor>> {
        let mut containers = HashMap::new();

        for i in 0..sequence.len() {
            let start_hue = &sequence[i];
            let end_hue = &sequence[(i + 1) % sequence.len()];
            let wedge_key = format!("{}→{}", start_hue, end_hue);
            containers.insert(wedge_key, Vec::new());
        }

        containers
    }

    /// Distribute a color polygon into appropriate wedge containers.
    pub fn distribute_polygon(&mut self, polygon: IsccNbsColor) -> Result<()> {
        let (start_hue, end_hue) = Self::parse_polygon_hue_range(&polygon)?;
        let wedge_keys = self.find_wedges_in_range(&start_hue, &end_hue)?;

        for wedge_key in wedge_keys {
            if let Some(container) = self.wedge_containers.get_mut(&wedge_key) {
                container.push(polygon.clone());
            }
        }

        Ok(())
    }

    /// Parse polygon hue range from ISCC-NBS data.
    fn parse_polygon_hue_range(polygon: &IsccNbsColor) -> Result<(String, String)> {
        Ok((polygon.hue_range.0.clone(), polygon.hue_range.1.clone()))
    }

    /// Find all wedge keys that span from start_hue to end_hue.
    fn find_wedges_in_range(&self, start_hue: &str, end_hue: &str) -> Result<Vec<String>> {
        let start_pos = self.hue_to_position.get(start_hue).ok_or_else(|| {
            MunsellError::ConversionError {
                message: format!("Unknown start hue: {}", start_hue),
            }
        })?;

        let end_pos = self.hue_to_position.get(end_hue).ok_or_else(|| {
            MunsellError::ConversionError {
                message: format!("Unknown end hue: {}", end_hue),
            }
        })?;

        let mut wedge_keys = Vec::new();
        let mut current_pos = (*start_pos + 1) % self.hue_sequence.len();

        loop {
            let next_pos = (current_pos + 1) % self.hue_sequence.len();
            let start_hue_at_pos = &self.hue_sequence[current_pos];
            let end_hue_at_pos = &self.hue_sequence[next_pos];

            wedge_keys.push(format!("{}→{}", start_hue_at_pos, end_hue_at_pos));

            if current_pos == *end_pos {
                break;
            }

            current_pos = next_pos;
        }

        Ok(wedge_keys)
    }

    /// Find all ISCC-NBS colors that contain the given Munsell point.
    pub fn find_all_colors_at_point(&self, hue: &str, value: f64, chroma: f64) -> Vec<u16> {
        let wedge_key = match self.find_containing_wedge(hue) {
            Some(key) => key,
            None => return vec![],
        };

        let container = match self.wedge_containers.get(&wedge_key) {
            Some(c) => c,
            None => return vec![],
        };

        let mut matching_colors = Vec::new();

        for polygon in container {
            if self.point_in_polygon(value, chroma, polygon) {
                matching_colors.push(polygon.color_number);
            }
        }

        matching_colors.sort_unstable();
        matching_colors.dedup();

        matching_colors
    }

    /// Classify a Munsell color by finding the first matching ISCC-NBS color polygon.
    #[inline]
    pub fn classify_color(&self, hue: &str, value: f64, chroma: f64) -> Option<&IsccNbsColor> {
        let wedge_key = self.find_containing_wedge(hue)?;
        let container = self.wedge_containers.get(&wedge_key)?;

        container
            .iter()
            .find(|polygon| self.point_in_polygon(value, chroma, polygon))
    }

    /// Find which wedge contains the given hue using correct range interpretation.
    #[inline]
    pub(super) fn find_containing_wedge(&self, hue: &str) -> Option<String> {
        let (hue_number, hue_family) = self.parse_hue(hue).ok()?;

        let wedge_number = if hue_number <= 0.0 || hue_number > 10.0 {
            let normalized = if hue_number <= 0.0 {
                (hue_number % 10.0 + 10.0) % 10.0
            } else {
                hue_number % 10.0
            };
            if normalized == 0.0 || normalized <= 1.0 {
                1
            } else {
                (normalized.ceil() as u8).min(10)
            }
        } else {
            (hue_number.ceil() as u8).max(1).min(10)
        };

        let wedge_hue = format!("{}{}", wedge_number, hue_family);
        let wedge_pos = self.hue_to_position.get(&wedge_hue)?;
        let wedge_end_pos = (*wedge_pos + 1) % self.hue_sequence.len();

        let start_hue = &self.hue_sequence[*wedge_pos];
        let end_hue = &self.hue_sequence[wedge_end_pos];

        Some(format!("{}→{}", start_hue, end_hue))
    }

    /// Parse Munsell hue notation (e.g., "4.5R", "7YR").
    #[inline]
    pub(super) fn parse_hue(&self, hue: &str) -> Result<(f64, String)> {
        let hue = hue.trim();

        let mut split_pos = 0;
        for (i, c) in hue.char_indices() {
            if c.is_alphabetic() {
                split_pos = i;
                break;
            }
        }

        if split_pos == 0 {
            return Err(MunsellError::ConversionError {
                message: format!("Invalid hue format: {}", hue),
            });
        }

        let number_str = &hue[..split_pos];
        let family_str = &hue[split_pos..];

        let number: f64 = number_str
            .parse()
            .map_err(|_| MunsellError::ConversionError {
                message: format!("Invalid hue number: {}", number_str),
            })?;

        Ok((number, family_str.to_string()))
    }

    /// Find which wedge contains a given hue (public API).
    pub fn find_wedge_for_hue(&self, hue: &str) -> Option<String> {
        let (hue_num, family) = self.parse_hue(hue).ok()?;
        let (start_ref, end_ref) = self.find_bracketing_hues(hue_num, &family)?;
        Some(format!("{}→{}", start_ref, end_ref))
    }

    /// Get all color polygons in a specific wedge container.
    pub fn get_wedge_polygons(&self, wedge_key: &str) -> Option<&Vec<IsccNbsColor>> {
        self.wedge_containers.get(wedge_key)
    }

    /// Get the total number of wedge containers.
    pub fn wedge_count(&self) -> usize {
        self.wedge_containers.len()
    }

    /// Find the reference hues that bracket a given hue value.
    fn find_bracketing_hues(&self, hue_num: f64, family: &str) -> Option<(String, String)> {
        let start_num = hue_num.floor() as u32;
        let end_num = if start_num == 10 { 1 } else { start_num + 1 };

        if start_num == 10 {
            let next_family = self.get_next_family(family)?;
            Some((
                format!("{}{}", start_num, family),
                format!("{}{}", end_num, next_family),
            ))
        } else {
            Some((
                format!("{}{}", start_num, family),
                format!("{}{}", end_num, family),
            ))
        }
    }

    /// Get the next family in the sequence.
    #[inline]
    fn get_next_family(&self, family: &str) -> Option<String> {
        match family {
            "R" => Some("YR".to_string()),
            "YR" => Some("Y".to_string()),
            "Y" => Some("GY".to_string()),
            "GY" => Some("G".to_string()),
            "G" => Some("BG".to_string()),
            "BG" => Some("B".to_string()),
            "B" => Some("PB".to_string()),
            "PB" => Some("P".to_string()),
            "P" => Some("RP".to_string()),
            "RP" => Some("R".to_string()),
            _ => None,
        }
    }
}
