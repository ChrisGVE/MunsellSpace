//! Internal ISCC-NBS color polygon representation.

use geo::Polygon;

/// Internal representation of an ISCC-NBS color category with its polygonal region.
///
/// Each ISCC-NBS color is defined by a polygon in Munsell value-chroma space,
/// bounded by specific hue ranges. This struct represents one such color region.
///
/// # Fields
/// - `color_number`: Unique ISCC-NBS identifier (1-267)
/// - `polygon_group`: Group number for colors with multiple disconnected regions
/// - `hue_range`: Start and end hues defining the applicable hue range
/// - `polygon`: Geometric polygon defining the valid value-chroma region
#[derive(Debug, Clone)]
pub struct IsccNbsColor {
    /// Color number from ISCC-NBS standard (1-267).
    ///
    /// This unique identifier corresponds to specific color names
    /// in the ISCC-NBS system and is used for metadata lookup.
    pub color_number: u16,

    /// Polygon group number for colors with multiple disconnected regions.
    ///
    /// Some ISCC-NBS colors are defined by multiple separate polygons.
    /// This field groups polygons belonging to the same color category.
    pub polygon_group: u8,

    /// Hue range defining the applicable Munsell hue span.
    ///
    /// Tuple containing (start_hue, end_hue) such as ("1R", "7R"),
    /// indicating this color definition applies to hues from 1R through 7R.
    pub hue_range: (String, String),

    /// Geometric polygon defining the color region in Munsell value-chroma space.
    ///
    /// Points in this polygon represent valid (value, chroma) coordinates
    /// for this color within the specified hue range.
    pub polygon: Polygon<f64>,
}
