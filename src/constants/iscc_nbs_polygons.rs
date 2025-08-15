// Auto-generated from ISCC-NBS-Definitions.csv
// Contains embedded polygon definitions for ISCC-NBS color classification
// Each polygon is defined by its color_number, polygon_group, hue_range, and points

/// A single polygon point in value-chroma space
#[derive(Debug, Clone)]
pub struct PolygonPoint {
    pub chroma: f64,
    pub value: f64,
}

/// A complete polygon definition for an ISCC-NBS color region
#[derive(Debug, Clone)]
pub struct PolygonDefinition {
    pub color_number: u16,
    pub polygon_group: u8,
    pub hue1: &'static str,
    pub hue2: &'static str,
    pub points: &'static [PolygonPoint],
}

// Embedded polygon data - generated from ISCC-NBS-Definitions.csv
// This eliminates the need to read CSV files at runtime

pub const POLYGON_DEFINITIONS: &[PolygonDefinition] = &[
    // Color 1: polygon 1
    PolygonDefinition {
        color_number: 1,
        polygon_group: 1,
        hue1: "9RP",
        hue2: "4R",
        points: &[
            PolygonPoint { chroma: 11.0, value: 6.5 },
            PolygonPoint { chroma: 11.0, value: 10.0 },
            PolygonPoint { chroma: 50.0, value: 10.0 },
            PolygonPoint { chroma: 50.0, value: 6.5 },
        ],
    },
    // Color 2: polygon 1
    PolygonDefinition {
        color_number: 2,
        polygon_group: 1,
        hue1: "9RP",
        hue2: "4R",
        points: &[
            PolygonPoint { chroma: 7.0, value: 6.5 },
            PolygonPoint { chroma: 7.0, value: 10.0 },
            PolygonPoint { chroma: 11.0, value: 10.0 },
            PolygonPoint { chroma: 11.0, value: 6.5 },
        ],
    },
    // Color 3: polygon 1
    PolygonDefinition {
        color_number: 3,
        polygon_group: 1,
        hue1: "9RP",
        hue2: "4R",
        points: &[
            PolygonPoint { chroma: 7.0, value: 5.5 },
            PolygonPoint { chroma: 7.0, value: 6.5 },
            PolygonPoint { chroma: 15.0, value: 6.5 },
            PolygonPoint { chroma: 15.0, value: 5.5 },
        ],
    },
    // Color 3: polygon 2
    PolygonDefinition {
        color_number: 3,
        polygon_group: 2,
        hue1: "4R",
        hue2: "6R",
        points: &[
            PolygonPoint { chroma: 7.0, value: 5.5 },
            PolygonPoint { chroma: 7.0, value: 6.5 },
            PolygonPoint { chroma: 11.0, value: 6.5 },
            PolygonPoint { chroma: 11.0, value: 5.5 },
        ],
    },
    // Color 4: polygon 1
    PolygonDefinition {
        color_number: 4,
        polygon_group: 1,
        hue1: "9RP",
        hue2: "6R",
        points: &[
            PolygonPoint { chroma: 3.0, value: 8.0 },
            PolygonPoint { chroma: 3.0, value: 10.0 },
            PolygonPoint { chroma: 7.0, value: 10.0 },
            PolygonPoint { chroma: 7.0, value: 8.0 },
        ],
    },
    // Color 5: polygon 1
    PolygonDefinition {
        color_number: 5,
        polygon_group: 1,
        hue1: "9RP",
        hue2: "6R",
        points: &[
            PolygonPoint { chroma: 3.0, value: 6.5 },
            PolygonPoint { chroma: 3.0, value: 8.0 },
            PolygonPoint { chroma: 7.0, value: 8.0 },
            PolygonPoint { chroma: 7.0, value: 6.5 },
        ],
    },
    // Color 6: polygon 1
    PolygonDefinition {
        color_number: 6,
        polygon_group: 1,
        hue1: "9RP",
        hue2: "6R",
        points: &[
            PolygonPoint { chroma: 5.0, value: 5.5 },
            PolygonPoint { chroma: 5.0, value: 6.5 },
            PolygonPoint { chroma: 7.0, value: 6.5 },
            PolygonPoint { chroma: 7.0, value: 5.5 },
        ],
    },
    // Color 7: polygon 1
    PolygonDefinition {
        color_number: 7,
        polygon_group: 1,
        hue1: "9RP",
        hue2: "6R",
        points: &[
            PolygonPoint { chroma: 1.5, value: 8.0 },
            PolygonPoint { chroma: 1.5, value: 10.0 },
            PolygonPoint { chroma: 3.0, value: 10.0 },
            PolygonPoint { chroma: 3.0, value: 8.0 },
        ],
    },
    // Color 8: polygon 1
    PolygonDefinition {
        color_number: 8,
        polygon_group: 1,
        hue1: "9RP",
        hue2: "6R",
        points: &[
            PolygonPoint { chroma: 1.5, value: 6.5 },
            PolygonPoint { chroma: 1.5, value: 8.0 },
            PolygonPoint { chroma: 3.0, value: 8.0 },
            PolygonPoint { chroma: 3.0, value: 6.5 },
        ],
    },
    // Color 9: polygon 1
    PolygonDefinition {
        color_number: 9,
        polygon_group: 1,
        hue1: "9RP",
        hue2: "5YR",
        points: &[
            PolygonPoint { chroma: 0.5, value: 8.5 },
            PolygonPoint { chroma: 0.5, value: 10.0 },
            PolygonPoint { chroma: 1.5, value: 10.0 },
            PolygonPoint { chroma: 1.5, value: 8.5 },
        ],
    },
    // Color 9: polygon 2
    PolygonDefinition {
        color_number: 9,
        polygon_group: 2,
        hue1: "5YR",
        hue2: "7YR",
        points: &[
            PolygonPoint { chroma: 0.5, value: 8.5 },
            PolygonPoint { chroma: 0.5, value: 10.0 },
            PolygonPoint { chroma: 1.2, value: 10.0 },
            PolygonPoint { chroma: 1.2, value: 8.5 },
        ],
    },
    // Color 10: polygon 1
    PolygonDefinition {
        color_number: 10,
        polygon_group: 1,
        hue1: "9RP",
        hue2: "5YR",
        points: &[
            PolygonPoint { chroma: 0.5, value: 6.5 },
            PolygonPoint { chroma: 0.5, value: 8.5 },
            PolygonPoint { chroma: 1.5, value: 8.5 },
            PolygonPoint { chroma: 1.5, value: 6.5 },
        ],
    },
    // Color 10: polygon 2
    PolygonDefinition {
        color_number: 10,
        polygon_group: 2,
        hue1: "5YR",
        hue2: "7YR",
        points: &[
            PolygonPoint { chroma: 0.5, value: 6.5 },
            PolygonPoint { chroma: 0.5, value: 8.5 },
            PolygonPoint { chroma: 1.2, value: 8.5 },
            PolygonPoint { chroma: 1.2, value: 6.5 },
        ],
    },
    // Color 11: polygon 1
    PolygonDefinition {
        color_number: 11,
        polygon_group: 1,
        hue1: "1R",
        hue2: "7R",
        points: &[
            PolygonPoint { chroma: 11.0, value: 0.0 },
            PolygonPoint { chroma: 11.0, value: 3.5 },
            PolygonPoint { chroma: 13.0, value: 3.5 },
            PolygonPoint { chroma: 13.0, value: 5.5 },
            PolygonPoint { chroma: 15.0, value: 5.5 },
            PolygonPoint { chroma: 15.0, value: 6.5 },
            PolygonPoint { chroma: 50.0, value: 6.5 },
            PolygonPoint { chroma: 50.0, value: 0.0 },
        ],
    },
    // Color 11: polygon 2
    PolygonDefinition {
        color_number: 11,
        polygon_group: 2,
        hue1: "7R",
        hue2: "9R",
        points: &[
            PolygonPoint { chroma: 11.0, value: 0.0 },
            PolygonPoint { chroma: 11.0, value: 3.5 },
            PolygonPoint { chroma: 13.0, value: 3.5 },
            PolygonPoint { chroma: 13.0, value: 4.5 },
            PolygonPoint { chroma: 50.0, value: 4.5 },
            PolygonPoint { chroma: 50.0, value: 0.0 },
        ],
    },
    // Color 12: polygon 1
    PolygonDefinition {
        color_number: 12,
        polygon_group: 1,
        hue1: "1R",
        hue2: "7R",
        points: &[
            PolygonPoint { chroma: 11.0, value: 3.5 },
            PolygonPoint { chroma: 11.0, value: 5.5 },
            PolygonPoint { chroma: 13.0, value: 5.5 },
            PolygonPoint { chroma: 13.0, value: 3.5 },
        ],
    },
    // Color 13: polygon 1
    PolygonDefinition {
        color_number: 13,
        polygon_group: 1,
        hue1: "1R",
        hue2: "9R",
        points: &[
            PolygonPoint { chroma: 9.0, value: 2.0 },
            PolygonPoint { chroma: 9.0, value: 3.5 },
            PolygonPoint { chroma: 11.0, value: 3.5 },
            PolygonPoint { chroma: 11.0, value: 2.0 },
        ],
    },
    // Color 14: polygon 1
    PolygonDefinition {
        color_number: 14,
        polygon_group: 1,
        hue1: "1R",
        hue2: "9R",
        points: &[
            PolygonPoint { chroma: 7.0, value: 0.0 },
            PolygonPoint { chroma: 7.0, value: 2.0 },
            PolygonPoint { chroma: 11.0, value: 2.0 },
            PolygonPoint { chroma: 11.0, value: 0.0 },
        ],
    },
    // Color 15: polygon 1
    PolygonDefinition {
        color_number: 15,
        polygon_group: 1,
        hue1: "1R",
        hue2: "7R",
        points: &[
            PolygonPoint { chroma: 7.0, value: 3.5 },
            PolygonPoint { chroma: 7.0, value: 5.5 },
            PolygonPoint { chroma: 11.0, value: 5.5 },
            PolygonPoint { chroma: 11.0, value: 3.5 },
        ],
    },
    // Color 16: polygon 1
    PolygonDefinition {
        color_number: 16,
        polygon_group: 1,
        hue1: "1R",
        hue2: "6R",
        points: &[
            PolygonPoint { chroma: 3.0, value: 2.0 },
            PolygonPoint { chroma: 3.0, value: 3.5 },
            PolygonPoint { chroma: 9.0, value: 3.5 },
            PolygonPoint { chroma: 9.0, value: 2.0 },
        ],
    },
    // Color 16: polygon 2
    PolygonDefinition {
        color_number: 16,
        polygon_group: 2,
        hue1: "6R",
        hue2: "9R",
        points: &[
            PolygonPoint { chroma: 7.0, value: 2.0 },
            PolygonPoint { chroma: 7.0, value: 3.5 },
            PolygonPoint { chroma: 9.0, value: 3.5 },
            PolygonPoint { chroma: 9.0, value: 2.0 },
        ],
    },
    // Color 17: polygon 1
    PolygonDefinition {
        color_number: 17,
        polygon_group: 1,
        hue1: "1R",
        hue2: "6R",
        points: &[
            PolygonPoint { chroma: 2.0, value: 0.0 },
            PolygonPoint { chroma: 2.0, value: 2.0 },
            PolygonPoint { chroma: 7.0, value: 2.0 },
            PolygonPoint { chroma: 7.0, value: 0.0 },
        ],
    },
    // Color 18: polygon 1
    PolygonDefinition {
        color_number: 18,
        polygon_group: 1,
        hue1: "1R",
        hue2: "8R",
        points: &[
            PolygonPoint { chroma: 1.5, value: 5.5 },
            PolygonPoint { chroma: 1.5, value: 6.5 },
            PolygonPoint { chroma: 5.0, value: 6.5 },
            PolygonPoint { chroma: 5.0, value: 5.5 },
        ],
    },
    // Color 18: polygon 2
    PolygonDefinition {
        color_number: 18,
        polygon_group: 2,
        hue1: "8R",
        hue2: "1YR",
        points: &[
            PolygonPoint { chroma: 1.5, value: 5.5 },
            PolygonPoint { chroma: 1.5, value: 6.5 },
            PolygonPoint { chroma: 3.0, value: 6.5 },
            PolygonPoint { chroma: 3.0, value: 5.5 },
        ],
    },
    // Color 19: polygon 1
    PolygonDefinition {
        color_number: 19,
        polygon_group: 1,
        hue1: "1R",
        hue2: "8R",
        points: &[
            PolygonPoint { chroma: 1.5, value: 3.5 },
            PolygonPoint { chroma: 1.5, value: 5.5 },
            PolygonPoint { chroma: 7.0, value: 5.5 },
            PolygonPoint { chroma: 7.0, value: 3.5 },
        ],
    },
    // Color 19: polygon 2
    PolygonDefinition {
        color_number: 19,
        polygon_group: 2,
        hue1: "8R",
        hue2: "1YR",
        points: &[
            PolygonPoint { chroma: 1.5, value: 4.5 },
            PolygonPoint { chroma: 1.5, value: 5.5 },
            PolygonPoint { chroma: 3.0, value: 5.5 },
            PolygonPoint { chroma: 3.0, value: 4.5 },
        ],
    },
    // Color 20: polygon 1
    PolygonDefinition {
        color_number: 20,
        polygon_group: 1,
        hue1: "1R",
        hue2: "6R",
        points: &[
            PolygonPoint { chroma: 0.5, value: 2.0 },
            PolygonPoint { chroma: 0.5, value: 2.5 },
            PolygonPoint { chroma: 1.5, value: 2.5 },
            PolygonPoint { chroma: 1.5, value: 3.5 },
            PolygonPoint { chroma: 3.0, value: 3.5 },
            PolygonPoint { chroma: 3.0, value: 2.0 },
        ],
    },
    // Color 21: polygon 1
    PolygonDefinition {
        color_number: 21,
        polygon_group: 1,
        hue1: "1R",
        hue2: "6R",
        points: &[
            PolygonPoint { chroma: 1.0, value: 0.0 },
            PolygonPoint { chroma: 1.0, value: 2.0 },
            PolygonPoint { chroma: 2.0, value: 2.0 },
            PolygonPoint { chroma: 2.0, value: 0.0 },
        ],
    },
    // Color 22: polygon 1
    PolygonDefinition {
        color_number: 22,
        polygon_group: 1,
        hue1: "1R",
        hue2: "2YR",
        points: &[
            PolygonPoint { chroma: 0.5, value: 4.5 },
            PolygonPoint { chroma: 0.5, value: 6.5 },
            PolygonPoint { chroma: 1.5, value: 6.5 },
            PolygonPoint { chroma: 1.5, value: 4.5 },
        ],
    },
    // Color 23: polygon 1
    PolygonDefinition {
        color_number: 23,
        polygon_group: 1,
        hue1: "1R",
        hue2: "1YR",
        points: &[
            PolygonPoint { chroma: 0.5, value: 2.5 },
            PolygonPoint { chroma: 0.5, value: 4.5 },
            PolygonPoint { chroma: 1.5, value: 4.5 },
            PolygonPoint { chroma: 1.5, value: 2.5 },
        ],
    },
    // Color 24: polygon 1
    PolygonDefinition {
        color_number: 24,
        polygon_group: 1,
        hue1: "1R",
        hue2: "6R",
        points: &[
            PolygonPoint { chroma: 0.5, value: 0.0 },
            PolygonPoint { chroma: 0.5, value: 2.0 },
            PolygonPoint { chroma: 1.0, value: 2.0 },
            PolygonPoint { chroma: 1.0, value: 0.0 },
        ],
    },
    // Color 24: polygon 2
    PolygonDefinition {
        color_number: 24,
        polygon_group: 2,
        hue1: "6R",
        hue2: "1YR",
        points: &[
            PolygonPoint { chroma: 0.5, value: 0.0 },
            PolygonPoint { chroma: 0.5, value: 1.5 },
            PolygonPoint { chroma: 1.0, value: 1.5 },
            PolygonPoint { chroma: 1.0, value: 0.0 },
        ],
    },
    // Color 25: polygon 1
    PolygonDefinition {
        color_number: 25,
        polygon_group: 1,
        hue1: "4R",
        hue2: "2YR",
        points: &[
            PolygonPoint { chroma: 11.0, value: 6.5 },
            PolygonPoint { chroma: 11.0, value: 10.0 },
            PolygonPoint { chroma: 50.0, value: 10.0 },
            PolygonPoint { chroma: 50.0, value: 6.5 },
        ],
    },
    // Color 26: polygon 1
    PolygonDefinition {
        color_number: 26,
        polygon_group: 1,
        hue1: "4R",
        hue2: "2YR",
        points: &[
            PolygonPoint { chroma: 7.0, value: 6.5 },
            PolygonPoint { chroma: 7.0, value: 10.0 },
            PolygonPoint { chroma: 11.0, value: 10.0 },
            PolygonPoint { chroma: 11.0, value: 6.5 },
        ],
    },
    // Color 27: polygon 1
    PolygonDefinition {
        color_number: 27,
        polygon_group: 1,
        hue1: "4R",
        hue2: "6R",
        points: &[
            PolygonPoint { chroma: 11.0, value: 5.5 },
            PolygonPoint { chroma: 11.0, value: 6.5 },
            PolygonPoint { chroma: 15.0, value: 6.5 },
            PolygonPoint { chroma: 15.0, value: 5.5 },
        ],
    },
    // Color 27: polygon 2
    PolygonDefinition {
        color_number: 27,
        polygon_group: 2,
        hue1: "6R",
        hue2: "7R",
        points: &[
            PolygonPoint { chroma: 7.0, value: 5.5 },
            PolygonPoint { chroma: 7.0, value: 6.5 },
            PolygonPoint { chroma: 15.0, value: 6.5 },
            PolygonPoint { chroma: 15.0, value: 5.5 },
        ],
    },
    // Color 28: polygon 1
    PolygonDefinition {
        color_number: 28,
        polygon_group: 1,
        hue1: "6R",
        hue2: "2YR",
        points: &[
            PolygonPoint { chroma: 3.0, value: 8.0 },
            PolygonPoint { chroma: 3.0, value: 10.0 },
            PolygonPoint { chroma: 7.0, value: 10.0 },
            PolygonPoint { chroma: 7.0, value: 8.0 },
        ],
    },
    // Color 28: polygon 2
    PolygonDefinition {
        color_number: 28,
        polygon_group: 2,
        hue1: "2YR",
        hue2: "7YR",
        points: &[
            PolygonPoint { chroma: 3.0, value: 8.0 },
            PolygonPoint { chroma: 3.0, value: 10.0 },
            PolygonPoint { chroma: 6.0, value: 10.0 },
            PolygonPoint { chroma: 6.0, value: 8.0 },
        ],
    },
    // Color 29: polygon 1
    PolygonDefinition {
        color_number: 29,
        polygon_group: 1,
        hue1: "6R",
        hue2: "2YR",
        points: &[
            PolygonPoint { chroma: 3.0, value: 6.5 },
            PolygonPoint { chroma: 3.0, value: 8.0 },
            PolygonPoint { chroma: 7.0, value: 8.0 },
            PolygonPoint { chroma: 7.0, value: 6.5 },
        ],
    },
    // Color 29: polygon 2
    PolygonDefinition {
        color_number: 29,
        polygon_group: 2,
        hue1: "2YR",
        hue2: "7YR",
        points: &[
            PolygonPoint { chroma: 3.0, value: 6.5 },
            PolygonPoint { chroma: 3.0, value: 8.0 },
            PolygonPoint { chroma: 6.0, value: 8.0 },
            PolygonPoint { chroma: 6.0, value: 6.5 },
        ],
    },
    // Color 30: polygon 1
    PolygonDefinition {
        color_number: 30,
        polygon_group: 1,
        hue1: "6R",
        hue2: "8R",
        points: &[
            PolygonPoint { chroma: 5.0, value: 5.5 },
            PolygonPoint { chroma: 5.0, value: 6.5 },
            PolygonPoint { chroma: 7.0, value: 6.5 },
            PolygonPoint { chroma: 7.0, value: 5.5 },
        ],
    },
    // Color 31: polygon 1
    PolygonDefinition {
        color_number: 31,
        polygon_group: 1,
        hue1: "6R",
        hue2: "5YR",
        points: &[
            PolygonPoint { chroma: 1.5, value: 8.0 },
            PolygonPoint { chroma: 1.5, value: 10.0 },
            PolygonPoint { chroma: 3.0, value: 10.0 },
            PolygonPoint { chroma: 3.0, value: 8.0 },
        ],
    },
    // Color 31: polygon 2
    PolygonDefinition {
        color_number: 31,
        polygon_group: 2,
        hue1: "5YR",
        hue2: "8YR",
        points: &[
            PolygonPoint { chroma: 1.2, value: 8.0 },
            PolygonPoint { chroma: 1.2, value: 10.0 },
            PolygonPoint { chroma: 3.0, value: 10.0 },
            PolygonPoint { chroma: 3.0, value: 8.0 },
        ],
    },
    // Color 32: polygon 1
    PolygonDefinition {
        color_number: 32,
        polygon_group: 1,
        hue1: "6R",
        hue2: "5YR",
        points: &[
            PolygonPoint { chroma: 1.5, value: 6.5 },
            PolygonPoint { chroma: 1.5, value: 8.0 },
            PolygonPoint { chroma: 3.0, value: 8.0 },
            PolygonPoint { chroma: 3.0, value: 6.5 },
        ],
    },
    // Color 33: polygon 1
    PolygonDefinition {
        color_number: 33,
        polygon_group: 1,
        hue1: "5YR",
        hue2: "8YR",
        points: &[
            PolygonPoint { chroma: 1.2, value: 6.5 },
            PolygonPoint { chroma: 1.2, value: 8.0 },
            PolygonPoint { chroma: 3.0, value: 8.0 },
            PolygonPoint { chroma: 3.0, value: 6.5 },
        ],
    },
    // Color 34: polygon 1
    PolygonDefinition {
        color_number: 34,
        polygon_group: 1,
        hue1: "7R",
        hue2: "9R",
        points: &[
            PolygonPoint { chroma: 13.0, value: 4.5 },
            PolygonPoint { chroma: 13.0, value: 6.5 },
            PolygonPoint { chroma: 50.0, value: 6.5 },
            PolygonPoint { chroma: 50.0, value: 4.5 },
        ],
    },
    // Color 34: polygon 2
    PolygonDefinition {
        color_number: 34,
        polygon_group: 2,
        hue1: "9R",
        hue2: "2YR",
        points: &[
            PolygonPoint { chroma: 13.0, value: 3.5 },
            PolygonPoint { chroma: 13.0, value: 6.5 },
            PolygonPoint { chroma: 50.0, value: 6.5 },
            PolygonPoint { chroma: 50.0, value: 3.5 },
        ],
    },
    // Color 35: polygon 1
    PolygonDefinition {
        color_number: 35,
        polygon_group: 1,
        hue1: "7R",
        hue2: "2YR",
        points: &[
            PolygonPoint { chroma: 11.0, value: 4.5 },
            PolygonPoint { chroma: 11.0, value: 6.5 },
            PolygonPoint { chroma: 13.0, value: 6.5 },
            PolygonPoint { chroma: 13.0, value: 4.5 },
        ],
    },
    // Color 36: polygon 1
    PolygonDefinition {
        color_number: 36,
        polygon_group: 1,
        hue1: "7R",
        hue2: "2YR",
        points: &[
            PolygonPoint { chroma: 11.0, value: 3.5 },
            PolygonPoint { chroma: 11.0, value: 4.5 },
            PolygonPoint { chroma: 13.0, value: 4.5 },
            PolygonPoint { chroma: 13.0, value: 3.5 },
        ],
    },
    // Color 37: polygon 1
    PolygonDefinition {
        color_number: 37,
        polygon_group: 1,
        hue1: "7R",
        hue2: "2YR",
        points: &[
            PolygonPoint { chroma: 7.0, value: 4.5 },
            PolygonPoint { chroma: 7.0, value: 6.5 },
            PolygonPoint { chroma: 11.0, value: 6.5 },
            PolygonPoint { chroma: 11.0, value: 4.5 },
        ],
    },
    // Color 38: polygon 1
    PolygonDefinition {
        color_number: 38,
        polygon_group: 1,
        hue1: "7R",
        hue2: "2YR",
        points: &[
            PolygonPoint { chroma: 7.0, value: 3.5 },
            PolygonPoint { chroma: 7.0, value: 4.5 },
            PolygonPoint { chroma: 11.0, value: 4.5 },
            PolygonPoint { chroma: 11.0, value: 3.5 },
        ],
    },
    // Color 39: polygon 1
    PolygonDefinition {
        color_number: 39,
        polygon_group: 1,
        hue1: "8R",
        hue2: "3YR",
        points: &[
            PolygonPoint { chroma: 5.0, value: 4.5 },
            PolygonPoint { chroma: 5.0, value: 6.5 },
            PolygonPoint { chroma: 7.0, value: 6.5 },
            PolygonPoint { chroma: 7.0, value: 4.5 },
        ],
    },
    // Color 40: polygon 1
    PolygonDefinition {
        color_number: 40,
        polygon_group: 1,
        hue1: "9R",
        hue2: "2YR",
        points: &[
            PolygonPoint { chroma: 7.0, value: 2.5 },
            PolygonPoint { chroma: 7.0, value: 3.5 },
            PolygonPoint { chroma: 50.0, value: 3.5 },
            PolygonPoint { chroma: 50.0, value: 2.5 },
        ],
    },
    // Color 41: polygon 1
    PolygonDefinition {
        color_number: 41,
        polygon_group: 1,
        hue1: "6R",
        hue2: "9R",
        points: &[
            PolygonPoint { chroma: 5.0, value: 0.0 },
            PolygonPoint { chroma: 5.0, value: 2.5 },
            PolygonPoint { chroma: 7.0, value: 2.5 },
            PolygonPoint { chroma: 7.0, value: 0.0 },
        ],
    },
    // Color 41: polygon 2
    PolygonDefinition {
        color_number: 41,
        polygon_group: 2,
        hue1: "9R",
        hue2: "2YR",
        points: &[
            PolygonPoint { chroma: 5.0, value: 0.0 },
            PolygonPoint { chroma: 5.0, value: 2.5 },
            PolygonPoint { chroma: 50.0, value: 2.5 },
            PolygonPoint { chroma: 50.0, value: 0.0 },
        ],
    },
    // Color 42: polygon 1
    PolygonDefinition {
        color_number: 42,
        polygon_group: 1,
        hue1: "8R",
        hue2: "3YR",
        points: &[
            PolygonPoint { chroma: 3.0, value: 4.5 },
            PolygonPoint { chroma: 3.0, value: 6.5 },
            PolygonPoint { chroma: 5.0, value: 6.5 },
            PolygonPoint { chroma: 5.0, value: 4.5 },
        ],
    },
    // Color 43: polygon 1
    PolygonDefinition {
        color_number: 43,
        polygon_group: 1,
        hue1: "6R",
        hue2: "8R",
        points: &[
            PolygonPoint { chroma: 3.0, value: 2.5 },
            PolygonPoint { chroma: 3.0, value: 3.5 },
            PolygonPoint { chroma: 7.0, value: 3.5 },
            PolygonPoint { chroma: 7.0, value: 2.5 },
        ],
    },
    // Color 43: polygon 2
    PolygonDefinition {
        color_number: 43,
        polygon_group: 2,
        hue1: "8R",
        hue2: "2YR",
        points: &[
            PolygonPoint { chroma: 3.0, value: 2.5 },
            PolygonPoint { chroma: 3.0, value: 4.5 },
            PolygonPoint { chroma: 7.0, value: 4.5 },
            PolygonPoint { chroma: 7.0, value: 2.5 },
        ],
    },
    // Color 43: polygon 3
    PolygonDefinition {
        color_number: 43,
        polygon_group: 3,
        hue1: "2YR",
        hue2: "3YR",
        points: &[
            PolygonPoint { chroma: 3.0, value: 2.5 },
            PolygonPoint { chroma: 3.0, value: 4.5 },
            PolygonPoint { chroma: 5.0, value: 4.5 },
            PolygonPoint { chroma: 5.0, value: 2.5 },
        ],
    },
    // Color 44: polygon 1
    PolygonDefinition {
        color_number: 44,
        polygon_group: 1,
        hue1: "6R",
        hue2: "3YR",
        points: &[
            PolygonPoint { chroma: 1.0, value: 0.0 },
            PolygonPoint { chroma: 1.0, value: 1.5 },
            PolygonPoint { chroma: 3.0, value: 1.5 },
            PolygonPoint { chroma: 3.0, value: 2.5 },
            PolygonPoint { chroma: 5.0, value: 2.5 },
            PolygonPoint { chroma: 5.0, value: 0.0 },
        ],
    },
    // Color 45: polygon 1
    PolygonDefinition {
        color_number: 45,
        polygon_group: 1,
        hue1: "1YR",
        hue2: "5YR",
        points: &[
            PolygonPoint { chroma: 1.5, value: 4.5 },
            PolygonPoint { chroma: 1.5, value: 6.5 },
            PolygonPoint { chroma: 3.0, value: 6.5 },
            PolygonPoint { chroma: 3.0, value: 4.5 },
        ],
    },
    // Color 46: polygon 1
    PolygonDefinition {
        color_number: 46,
        polygon_group: 1,
        hue1: "6R",
        hue2: "8R",
        points: &[
            PolygonPoint { chroma: 1.5, value: 2.5 },
            PolygonPoint { chroma: 1.5, value: 3.5 },
            PolygonPoint { chroma: 3.0, value: 3.5 },
            PolygonPoint { chroma: 3.0, value: 2.5 },
        ],
    },
    // Color 46: polygon 2
    PolygonDefinition {
        color_number: 46,
        polygon_group: 2,
        hue1: "8R",
        hue2: "3YR",
        points: &[
            PolygonPoint { chroma: 1.5, value: 2.5 },
            PolygonPoint { chroma: 1.5, value: 4.5 },
            PolygonPoint { chroma: 3.0, value: 4.5 },
            PolygonPoint { chroma: 3.0, value: 2.5 },
        ],
    },
    // Color 47: polygon 1
    PolygonDefinition {
        color_number: 47,
        polygon_group: 1,
        hue1: "6R",
        hue2: "3YR",
        points: &[
            PolygonPoint { chroma: 0.5, value: 1.5 },
            PolygonPoint { chroma: 0.5, value: 2.5 },
            PolygonPoint { chroma: 3.0, value: 2.5 },
            PolygonPoint { chroma: 3.0, value: 1.5 },
        ],
    },
    // Color 48: polygon 1
    PolygonDefinition {
        color_number: 48,
        polygon_group: 1,
        hue1: "2YR",
        hue2: "7YR",
        points: &[
            PolygonPoint { chroma: 14.0, value: 4.5 },
            PolygonPoint { chroma: 14.0, value: 10.0 },
            PolygonPoint { chroma: 50.0, value: 10.0 },
            PolygonPoint { chroma: 50.0, value: 4.5 },
        ],
    },
    // Color 49: polygon 1
    PolygonDefinition {
        color_number: 49,
        polygon_group: 1,
        hue1: "2YR",
        hue2: "7YR",
        points: &[
            PolygonPoint { chroma: 10.0, value: 7.5 },
            PolygonPoint { chroma: 10.0, value: 10.0 },
            PolygonPoint { chroma: 14.0, value: 10.0 },
            PolygonPoint { chroma: 14.0, value: 7.5 },
        ],
    },
    // Color 50: polygon 1
    PolygonDefinition {
        color_number: 50,
        polygon_group: 1,
        hue1: "2YR",
        hue2: "7YR",
        points: &[
            PolygonPoint { chroma: 10.0, value: 5.5 },
            PolygonPoint { chroma: 10.0, value: 7.5 },
            PolygonPoint { chroma: 14.0, value: 7.5 },
            PolygonPoint { chroma: 14.0, value: 5.5 },
        ],
    },
    // Color 51: polygon 1
    PolygonDefinition {
        color_number: 51,
        polygon_group: 1,
        hue1: "2YR",
        hue2: "7YR",
        points: &[
            PolygonPoint { chroma: 10.0, value: 4.5 },
            PolygonPoint { chroma: 10.0, value: 5.5 },
            PolygonPoint { chroma: 14.0, value: 5.5 },
            PolygonPoint { chroma: 14.0, value: 4.5 },
        ],
    },
    // Color 52: polygon 1
    PolygonDefinition {
        color_number: 52,
        polygon_group: 1,
        hue1: "2YR",
        hue2: "7YR",
        points: &[
            PolygonPoint { chroma: 6.0, value: 7.5 },
            PolygonPoint { chroma: 6.0, value: 10.0 },
            PolygonPoint { chroma: 10.0, value: 10.0 },
            PolygonPoint { chroma: 10.0, value: 7.5 },
        ],
    },
    // Color 53: polygon 1
    PolygonDefinition {
        color_number: 53,
        polygon_group: 1,
        hue1: "2YR",
        hue2: "3YR",
        points: &[
            PolygonPoint { chroma: 7.0, value: 5.5 },
            PolygonPoint { chroma: 7.0, value: 6.5 },
            PolygonPoint { chroma: 6.0, value: 6.5 },
            PolygonPoint { chroma: 6.0, value: 7.5 },
            PolygonPoint { chroma: 10.0, value: 7.5 },
            PolygonPoint { chroma: 10.0, value: 5.5 },
        ],
    },
    // Color 53: polygon 2
    PolygonDefinition {
        color_number: 53,
        polygon_group: 2,
        hue1: "3YR",
        hue2: "7YR",
        points: &[
            PolygonPoint { chroma: 6.0, value: 5.5 },
            PolygonPoint { chroma: 6.0, value: 7.5 },
            PolygonPoint { chroma: 10.0, value: 7.5 },
            PolygonPoint { chroma: 10.0, value: 5.5 },
        ],
    },
    // Color 54: polygon 1
    PolygonDefinition {
        color_number: 54,
        polygon_group: 1,
        hue1: "2YR",
        hue2: "3YR",
        points: &[
            PolygonPoint { chroma: 7.0, value: 4.5 },
            PolygonPoint { chroma: 7.0, value: 5.5 },
            PolygonPoint { chroma: 10.0, value: 5.5 },
            PolygonPoint { chroma: 10.0, value: 4.5 },
        ],
    },
    // Color 54: polygon 2
    PolygonDefinition {
        color_number: 54,
        polygon_group: 2,
        hue1: "3YR",
        hue2: "7YR",
        points: &[
            PolygonPoint { chroma: 6.0, value: 4.5 },
            PolygonPoint { chroma: 6.0, value: 5.5 },
            PolygonPoint { chroma: 10.0, value: 5.5 },
            PolygonPoint { chroma: 10.0, value: 4.5 },
        ],
    },
    // Color 55: polygon 1
    PolygonDefinition {
        color_number: 55,
        polygon_group: 1,
        hue1: "2YR",
        hue2: "8YR",
        points: &[
            PolygonPoint { chroma: 5.0, value: 2.5 },
            PolygonPoint { chroma: 5.0, value: 4.5 },
            PolygonPoint { chroma: 50.0, value: 4.5 },
            PolygonPoint { chroma: 50.0, value: 2.5 },
        ],
    },
    // Color 56: polygon 1
    PolygonDefinition {
        color_number: 56,
        polygon_group: 1,
        hue1: "2YR",
        hue2: "8YR",
        points: &[
            PolygonPoint { chroma: 5.0, value: 0.0 },
            PolygonPoint { chroma: 5.0, value: 2.5 },
            PolygonPoint { chroma: 50.0, value: 2.5 },
            PolygonPoint { chroma: 50.0, value: 0.0 },
        ],
    },
    // Color 57: polygon 1
    PolygonDefinition {
        color_number: 57,
        polygon_group: 1,
        hue1: "3YR",
        hue2: "8YR",
        points: &[
            PolygonPoint { chroma: 3.0, value: 4.5 },
            PolygonPoint { chroma: 3.0, value: 6.5 },
            PolygonPoint { chroma: 6.0, value: 6.5 },
            PolygonPoint { chroma: 6.0, value: 4.5 },
        ],
    },
    // Color 58: polygon 1
    PolygonDefinition {
        color_number: 58,
        polygon_group: 1,
        hue1: "3YR",
        hue2: "8YR",
        points: &[
            PolygonPoint { chroma: 2.5, value: 2.5 },
            PolygonPoint { chroma: 2.5, value: 4.5 },
            PolygonPoint { chroma: 5.0, value: 4.5 },
            PolygonPoint { chroma: 5.0, value: 2.5 },
        ],
    },
    // Color 59: polygon 1
    PolygonDefinition {
        color_number: 59,
        polygon_group: 1,
        hue1: "3YR",
        hue2: "8YR",
        points: &[
            PolygonPoint { chroma: 1.0, value: 0.0 },
            PolygonPoint { chroma: 1.0, value: 1.5 },
            PolygonPoint { chroma: 2.5, value: 1.5 },
            PolygonPoint { chroma: 2.5, value: 2.5 },
            PolygonPoint { chroma: 5.0, value: 2.5 },
            PolygonPoint { chroma: 5.0, value: 0.0 },
        ],
    },
    // Color 60: polygon 1
    PolygonDefinition {
        color_number: 60,
        polygon_group: 1,
        hue1: "5YR",
        hue2: "8YR",
        points: &[
            PolygonPoint { chroma: 1.2, value: 4.5 },
            PolygonPoint { chroma: 1.2, value: 6.5 },
            PolygonPoint { chroma: 3.0, value: 6.5 },
            PolygonPoint { chroma: 3.0, value: 4.5 },
        ],
    },
    // Color 61: polygon 1
    PolygonDefinition {
        color_number: 61,
        polygon_group: 1,
        hue1: "3YR",
        hue2: "5YR",
        points: &[
            PolygonPoint { chroma: 1.5, value: 2.5 },
            PolygonPoint { chroma: 1.5, value: 4.5 },
            PolygonPoint { chroma: 2.5, value: 4.5 },
            PolygonPoint { chroma: 2.5, value: 2.5 },
        ],
    },
    // Color 61: polygon 2
    PolygonDefinition {
        color_number: 61,
        polygon_group: 2,
        hue1: "5YR",
        hue2: "8YR",
        points: &[
            PolygonPoint { chroma: 1.2, value: 2.5 },
            PolygonPoint { chroma: 1.2, value: 4.5 },
            PolygonPoint { chroma: 2.5, value: 4.5 },
            PolygonPoint { chroma: 2.5, value: 2.5 },
        ],
    },
    // Color 62: polygon 1
    PolygonDefinition {
        color_number: 62,
        polygon_group: 1,
        hue1: "3YR",
        hue2: "8YR",
        points: &[
            PolygonPoint { chroma: 0.5, value: 1.5 },
            PolygonPoint { chroma: 0.5, value: 2.5 },
            PolygonPoint { chroma: 2.5, value: 2.5 },
            PolygonPoint { chroma: 2.5, value: 1.5 },
        ],
    },
    // Color 63: polygon 1
    PolygonDefinition {
        color_number: 63,
        polygon_group: 1,
        hue1: "2YR",
        hue2: "5YR",
        points: &[
            PolygonPoint { chroma: 0.5, value: 4.5 },
            PolygonPoint { chroma: 0.5, value: 6.5 },
            PolygonPoint { chroma: 1.5, value: 6.5 },
            PolygonPoint { chroma: 1.5, value: 4.5 },
        ],
    },
    // Color 63: polygon 2
    PolygonDefinition {
        color_number: 63,
        polygon_group: 2,
        hue1: "5YR",
        hue2: "7YR",
        points: &[
            PolygonPoint { chroma: 0.5, value: 4.5 },
            PolygonPoint { chroma: 0.5, value: 6.5 },
            PolygonPoint { chroma: 1.2, value: 6.5 },
            PolygonPoint { chroma: 1.2, value: 4.5 },
        ],
    },
    // Color 63: polygon 3
    PolygonDefinition {
        color_number: 63,
        polygon_group: 3,
        hue1: "7YR",
        hue2: "4Y",
        points: &[
            PolygonPoint { chroma: 0.7, value: 4.5 },
            PolygonPoint { chroma: 0.7, value: 6.5 },
            PolygonPoint { chroma: 1.2, value: 6.5 },
            PolygonPoint { chroma: 1.2, value: 4.5 },
        ],
    },
    // Color 64: polygon 1
    PolygonDefinition {
        color_number: 64,
        polygon_group: 1,
        hue1: "1YR",
        hue2: "5YR",
        points: &[
            PolygonPoint { chroma: 0.5, value: 2.5 },
            PolygonPoint { chroma: 0.5, value: 4.5 },
            PolygonPoint { chroma: 1.5, value: 4.5 },
            PolygonPoint { chroma: 1.5, value: 2.5 },
        ],
    },
    // Color 64: polygon 2
    PolygonDefinition {
        color_number: 64,
        polygon_group: 2,
        hue1: "5YR",
        hue2: "4Y",
        points: &[
            PolygonPoint { chroma: 0.5, value: 2.5 },
            PolygonPoint { chroma: 0.5, value: 4.5 },
            PolygonPoint { chroma: 1.2, value: 4.5 },
            PolygonPoint { chroma: 1.2, value: 2.5 },
        ],
    },
    // Color 65: polygon 1
    PolygonDefinition {
        color_number: 65,
        polygon_group: 1,
        hue1: "1YR",
        hue2: "4Y",
        points: &[
            PolygonPoint { chroma: 0.5, value: 0.0 },
            PolygonPoint { chroma: 0.5, value: 1.5 },
            PolygonPoint { chroma: 1.0, value: 1.5 },
            PolygonPoint { chroma: 1.0, value: 0.0 },
        ],
    },
    // Color 66: polygon 1
    PolygonDefinition {
        color_number: 66,
        polygon_group: 1,
        hue1: "7YR",
        hue2: "1Y",
        points: &[
            PolygonPoint { chroma: 14.0, value: 5.5 },
            PolygonPoint { chroma: 14.0, value: 10.0 },
            PolygonPoint { chroma: 50.0, value: 10.0 },
            PolygonPoint { chroma: 50.0, value: 5.5 },
        ],
    },
    // Color 67: polygon 1
    PolygonDefinition {
        color_number: 67,
        polygon_group: 1,
        hue1: "7YR",
        hue2: "1Y",
        points: &[
            PolygonPoint { chroma: 10.0, value: 8.0 },
            PolygonPoint { chroma: 10.0, value: 10.0 },
            PolygonPoint { chroma: 14.0, value: 10.0 },
            PolygonPoint { chroma: 14.0, value: 8.0 },
        ],
    },
    // Color 68: polygon 1
    PolygonDefinition {
        color_number: 68,
        polygon_group: 1,
        hue1: "7YR",
        hue2: "1Y",
        points: &[
            PolygonPoint { chroma: 10.0, value: 6.5 },
            PolygonPoint { chroma: 10.0, value: 8.0 },
            PolygonPoint { chroma: 14.0, value: 8.0 },
            PolygonPoint { chroma: 14.0, value: 6.5 },
        ],
    },
    // Color 69: polygon 1
    PolygonDefinition {
        color_number: 69,
        polygon_group: 1,
        hue1: "7YR",
        hue2: "1Y",
        points: &[
            PolygonPoint { chroma: 10.0, value: 5.5 },
            PolygonPoint { chroma: 10.0, value: 6.5 },
            PolygonPoint { chroma: 14.0, value: 6.5 },
            PolygonPoint { chroma: 14.0, value: 5.5 },
        ],
    },
    // Color 70: polygon 1
    PolygonDefinition {
        color_number: 70,
        polygon_group: 1,
        hue1: "7YR",
        hue2: "1Y",
        points: &[
            PolygonPoint { chroma: 6.0, value: 8.0 },
            PolygonPoint { chroma: 6.0, value: 10.0 },
            PolygonPoint { chroma: 10.0, value: 10.0 },
            PolygonPoint { chroma: 10.0, value: 8.0 },
        ],
    },
    // Color 71: polygon 1
    PolygonDefinition {
        color_number: 71,
        polygon_group: 1,
        hue1: "7YR",
        hue2: "1Y",
        points: &[
            PolygonPoint { chroma: 6.0, value: 6.5 },
            PolygonPoint { chroma: 6.0, value: 8.0 },
            PolygonPoint { chroma: 10.0, value: 8.0 },
            PolygonPoint { chroma: 10.0, value: 6.5 },
        ],
    },
    // Color 72: polygon 1
    PolygonDefinition {
        color_number: 72,
        polygon_group: 1,
        hue1: "7YR",
        hue2: "1Y",
        points: &[
            PolygonPoint { chroma: 6.0, value: 5.5 },
            PolygonPoint { chroma: 6.0, value: 6.5 },
            PolygonPoint { chroma: 10.0, value: 6.5 },
            PolygonPoint { chroma: 10.0, value: 5.5 },
        ],
    },
    // Color 73: polygon 1
    PolygonDefinition {
        color_number: 73,
        polygon_group: 1,
        hue1: "7YR",
        hue2: "8YR",
        points: &[
            PolygonPoint { chroma: 3.0, value: 7.5 },
            PolygonPoint { chroma: 3.0, value: 10.0 },
            PolygonPoint { chroma: 6.0, value: 10.0 },
            PolygonPoint { chroma: 6.0, value: 7.5 },
        ],
    },
    // Color 73: polygon 2
    PolygonDefinition {
        color_number: 73,
        polygon_group: 2,
        hue1: "8YR",
        hue2: "1Y",
        points: &[
            PolygonPoint { chroma: 2.0, value: 7.5 },
            PolygonPoint { chroma: 2.0, value: 10.0 },
            PolygonPoint { chroma: 6.0, value: 10.0 },
            PolygonPoint { chroma: 6.0, value: 7.5 },
        ],
    },
    // Color 74: polygon 1
    PolygonDefinition {
        color_number: 74,
        polygon_group: 1,
        hue1: "7YR",
        hue2: "8YR",
        points: &[
            PolygonPoint { chroma: 6.0, value: 4.5 },
            PolygonPoint { chroma: 6.0, value: 5.5 },
            PolygonPoint { chroma: 50.0, value: 5.5 },
            PolygonPoint { chroma: 50.0, value: 4.5 },
        ],
    },
    // Color 74: polygon 2
    PolygonDefinition {
        color_number: 74,
        polygon_group: 2,
        hue1: "8YR",
        hue2: "1Y",
        points: &[
            PolygonPoint { chroma: 5.0, value: 3.5 },
            PolygonPoint { chroma: 5.0, value: 5.5 },
            PolygonPoint { chroma: 50.0, value: 5.5 },
            PolygonPoint { chroma: 50.0, value: 3.5 },
        ],
    },
    // Color 75: polygon 1
    PolygonDefinition {
        color_number: 75,
        polygon_group: 1,
        hue1: "8YR",
        hue2: "1Y",
        points: &[
            PolygonPoint { chroma: 5.0, value: 0.0 },
            PolygonPoint { chroma: 5.0, value: 3.5 },
            PolygonPoint { chroma: 50.0, value: 3.5 },
            PolygonPoint { chroma: 50.0, value: 0.0 },
        ],
    },
    // Color 76: polygon 1
    PolygonDefinition {
        color_number: 76,
        polygon_group: 1,
        hue1: "7YR",
        hue2: "8YR",
        points: &[
            PolygonPoint { chroma: 3.0, value: 6.5 },
            PolygonPoint { chroma: 3.0, value: 7.5 },
            PolygonPoint { chroma: 6.0, value: 7.5 },
            PolygonPoint { chroma: 6.0, value: 6.5 },
        ],
    },
    // Color 76: polygon 2
    PolygonDefinition {
        color_number: 76,
        polygon_group: 2,
        hue1: "8YR",
        hue2: "1Y",
        points: &[
            PolygonPoint { chroma: 3.0, value: 5.5 },
            PolygonPoint { chroma: 3.0, value: 7.5 },
            PolygonPoint { chroma: 6.0, value: 7.5 },
            PolygonPoint { chroma: 6.0, value: 5.5 },
        ],
    },
    // Color 77: polygon 1
    PolygonDefinition {
        color_number: 77,
        polygon_group: 1,
        hue1: "8YR",
        hue2: "1Y",
        points: &[
            PolygonPoint { chroma: 2.5, value: 3.5 },
            PolygonPoint { chroma: 2.5, value: 4.5 },
            PolygonPoint { chroma: 3.0, value: 4.5 },
            PolygonPoint { chroma: 3.0, value: 5.5 },
            PolygonPoint { chroma: 5.0, value: 5.5 },
            PolygonPoint { chroma: 5.0, value: 3.5 },
        ],
    },
    // Color 78: polygon 1
    PolygonDefinition {
        color_number: 78,
        polygon_group: 1,
        hue1: "8YR",
        hue2: "1Y",
        points: &[
            PolygonPoint { chroma: 1.0, value: 0.0 },
            PolygonPoint { chroma: 1.0, value: 1.5 },
            PolygonPoint { chroma: 2.5, value: 1.5 },
            PolygonPoint { chroma: 2.5, value: 3.5 },
            PolygonPoint { chroma: 5.0, value: 3.5 },
            PolygonPoint { chroma: 5.0, value: 0.0 },
        ],
    },
    // Color 79: polygon 1
    PolygonDefinition {
        color_number: 79,
        polygon_group: 1,
        hue1: "8YR",
        hue2: "1Y",
        points: &[
            PolygonPoint { chroma: 1.2, value: 5.5 },
            PolygonPoint { chroma: 1.2, value: 6.5 },
            PolygonPoint { chroma: 2.0, value: 6.5 },
            PolygonPoint { chroma: 2.0, value: 7.5 },
            PolygonPoint { chroma: 3.0, value: 7.5 },
            PolygonPoint { chroma: 3.0, value: 5.5 },
        ],
    },
    // Color 80: polygon 1
    PolygonDefinition {
        color_number: 80,
        polygon_group: 1,
        hue1: "8YR",
        hue2: "1Y",
        points: &[
            PolygonPoint { chroma: 1.2, value: 3.5 },
            PolygonPoint { chroma: 1.2, value: 5.5 },
            PolygonPoint { chroma: 3.0, value: 5.5 },
            PolygonPoint { chroma: 3.0, value: 4.5 },
            PolygonPoint { chroma: 2.5, value: 4.5 },
            PolygonPoint { chroma: 2.5, value: 3.5 },
        ],
    },
    // Color 81: polygon 1
    PolygonDefinition {
        color_number: 81,
        polygon_group: 1,
        hue1: "8YR",
        hue2: "1Y",
        points: &[
            PolygonPoint { chroma: 0.5, value: 1.5 },
            PolygonPoint { chroma: 0.5, value: 2.5 },
            PolygonPoint { chroma: 1.2, value: 2.5 },
            PolygonPoint { chroma: 1.2, value: 3.5 },
            PolygonPoint { chroma: 2.5, value: 3.5 },
            PolygonPoint { chroma: 2.5, value: 1.5 },
        ],
    },
    // Color 82: polygon 1
    PolygonDefinition {
        color_number: 82,
        polygon_group: 1,
        hue1: "1Y",
        hue2: "7Y",
        points: &[
            PolygonPoint { chroma: 11.0, value: 5.5 },
            PolygonPoint { chroma: 11.0, value: 10.0 },
            PolygonPoint { chroma: 50.0, value: 10.0 },
            PolygonPoint { chroma: 50.0, value: 5.5 },
        ],
    },
    // Color 83: polygon 1
    PolygonDefinition {
        color_number: 83,
        polygon_group: 1,
        hue1: "1Y",
        hue2: "7Y",
        points: &[
            PolygonPoint { chroma: 8.0, value: 8.0 },
            PolygonPoint { chroma: 8.0, value: 10.0 },
            PolygonPoint { chroma: 11.0, value: 10.0 },
            PolygonPoint { chroma: 11.0, value: 8.0 },
        ],
    },
    // Color 84: polygon 1
    PolygonDefinition {
        color_number: 84,
        polygon_group: 1,
        hue1: "1Y",
        hue2: "7Y",
        points: &[
            PolygonPoint { chroma: 8.0, value: 6.5 },
            PolygonPoint { chroma: 8.0, value: 8.0 },
            PolygonPoint { chroma: 11.0, value: 8.0 },
            PolygonPoint { chroma: 11.0, value: 6.5 },
        ],
    },
    // Color 85: polygon 1
    PolygonDefinition {
        color_number: 85,
        polygon_group: 1,
        hue1: "1Y",
        hue2: "7Y",
        points: &[
            PolygonPoint { chroma: 8.0, value: 5.5 },
            PolygonPoint { chroma: 8.0, value: 6.5 },
            PolygonPoint { chroma: 11.0, value: 6.5 },
            PolygonPoint { chroma: 11.0, value: 5.5 },
        ],
    },
    // Color 86: polygon 1
    PolygonDefinition {
        color_number: 86,
        polygon_group: 1,
        hue1: "1Y",
        hue2: "7Y",
        points: &[
            PolygonPoint { chroma: 5.0, value: 8.0 },
            PolygonPoint { chroma: 5.0, value: 10.0 },
            PolygonPoint { chroma: 8.0, value: 10.0 },
            PolygonPoint { chroma: 8.0, value: 8.0 },
        ],
    },
    // Color 87: polygon 1
    PolygonDefinition {
        color_number: 87,
        polygon_group: 1,
        hue1: "1Y",
        hue2: "7Y",
        points: &[
            PolygonPoint { chroma: 5.0, value: 6.5 },
            PolygonPoint { chroma: 5.0, value: 8.0 },
            PolygonPoint { chroma: 8.0, value: 8.0 },
            PolygonPoint { chroma: 8.0, value: 6.5 },
        ],
    },
    // Color 88: polygon 1
    PolygonDefinition {
        color_number: 88,
        polygon_group: 1,
        hue1: "1Y",
        hue2: "7Y",
        points: &[
            PolygonPoint { chroma: 5.0, value: 5.5 },
            PolygonPoint { chroma: 5.0, value: 6.5 },
            PolygonPoint { chroma: 8.0, value: 6.5 },
            PolygonPoint { chroma: 8.0, value: 5.5 },
        ],
    },
    // Color 89: polygon 1
    PolygonDefinition {
        color_number: 89,
        polygon_group: 1,
        hue1: "1Y",
        hue2: "7Y",
        points: &[
            PolygonPoint { chroma: 2.0, value: 8.0 },
            PolygonPoint { chroma: 2.0, value: 10.0 },
            PolygonPoint { chroma: 5.0, value: 10.0 },
            PolygonPoint { chroma: 5.0, value: 8.0 },
        ],
    },
    // Color 89: polygon 2
    PolygonDefinition {
        color_number: 89,
        polygon_group: 2,
        hue1: "7Y",
        hue2: "9Y",
        points: &[
            PolygonPoint { chroma: 2.0, value: 8.0 },
            PolygonPoint { chroma: 2.0, value: 10.0 },
            PolygonPoint { chroma: 3.0, value: 10.0 },
            PolygonPoint { chroma: 3.0, value: 8.0 },
        ],
    },
    // Color 90: polygon 1
    PolygonDefinition {
        color_number: 90,
        polygon_group: 1,
        hue1: "1Y",
        hue2: "7Y",
        points: &[
            PolygonPoint { chroma: 2.0, value: 6.5 },
            PolygonPoint { chroma: 2.0, value: 8.0 },
            PolygonPoint { chroma: 5.0, value: 8.0 },
            PolygonPoint { chroma: 5.0, value: 6.5 },
        ],
    },
    // Color 90: polygon 2
    PolygonDefinition {
        color_number: 90,
        polygon_group: 2,
        hue1: "7Y",
        hue2: "9Y",
        points: &[
            PolygonPoint { chroma: 2.0, value: 6.5 },
            PolygonPoint { chroma: 2.0, value: 8.0 },
            PolygonPoint { chroma: 3.0, value: 8.0 },
            PolygonPoint { chroma: 3.0, value: 6.5 },
        ],
    },
    // Color 91: polygon 1
    PolygonDefinition {
        color_number: 91,
        polygon_group: 1,
        hue1: "1Y",
        hue2: "7Y",
        points: &[
            PolygonPoint { chroma: 3.0, value: 5.5 },
            PolygonPoint { chroma: 3.0, value: 6.5 },
            PolygonPoint { chroma: 5.0, value: 6.5 },
            PolygonPoint { chroma: 5.0, value: 5.5 },
        ],
    },
    // Color 92: polygon 1
    PolygonDefinition {
        color_number: 92,
        polygon_group: 1,
        hue1: "7YR",
        hue2: "8YR",
        points: &[
            PolygonPoint { chroma: 0.7, value: 8.5 },
            PolygonPoint { chroma: 0.7, value: 10.0 },
            PolygonPoint { chroma: 1.2, value: 10.0 },
            PolygonPoint { chroma: 1.2, value: 8.5 },
        ],
    },
    // Color 92: polygon 2
    PolygonDefinition {
        color_number: 92,
        polygon_group: 2,
        hue1: "8YR",
        hue2: "9Y",
        points: &[
            PolygonPoint { chroma: 0.7, value: 8.5 },
            PolygonPoint { chroma: 0.7, value: 10.0 },
            PolygonPoint { chroma: 2.0, value: 10.0 },
            PolygonPoint { chroma: 2.0, value: 8.5 },
        ],
    },
    // Color 92: polygon 3
    PolygonDefinition {
        color_number: 92,
        polygon_group: 3,
        hue1: "9Y",
        hue2: "4GY",
        points: &[
            PolygonPoint { chroma: 0.5, value: 8.5 },
            PolygonPoint { chroma: 0.5, value: 10.0 },
            PolygonPoint { chroma: 1.2, value: 10.0 },
            PolygonPoint { chroma: 1.2, value: 8.5 },
        ],
    },
    // Color 93: polygon 1
    PolygonDefinition {
        color_number: 93,
        polygon_group: 1,
        hue1: "7YR",
        hue2: "8YR",
        points: &[
            PolygonPoint { chroma: 0.7, value: 6.5 },
            PolygonPoint { chroma: 0.7, value: 8.5 },
            PolygonPoint { chroma: 1.2, value: 8.5 },
            PolygonPoint { chroma: 1.2, value: 6.5 },
        ],
    },
    // Color 93: polygon 2
    PolygonDefinition {
        color_number: 93,
        polygon_group: 2,
        hue1: "8YR",
        hue2: "9Y",
        points: &[
            PolygonPoint { chroma: 0.7, value: 6.5 },
            PolygonPoint { chroma: 0.7, value: 8.5 },
            PolygonPoint { chroma: 2.0, value: 8.5 },
            PolygonPoint { chroma: 2.0, value: 6.5 },
        ],
    },
    // Color 93: polygon 3
    PolygonDefinition {
        color_number: 93,
        polygon_group: 3,
        hue1: "9Y",
        hue2: "4GY",
        points: &[
            PolygonPoint { chroma: 0.5, value: 6.5 },
            PolygonPoint { chroma: 0.5, value: 8.5 },
            PolygonPoint { chroma: 1.2, value: 8.5 },
            PolygonPoint { chroma: 1.2, value: 6.5 },
        ],
    },
    // Color 94: polygon 1
    PolygonDefinition {
        color_number: 94,
        polygon_group: 1,
        hue1: "1Y",
        hue2: "4Y",
        points: &[
            PolygonPoint { chroma: 1.2, value: 4.5 },
            PolygonPoint { chroma: 1.2, value: 6.5 },
            PolygonPoint { chroma: 3.0, value: 6.5 },
            PolygonPoint { chroma: 3.0, value: 5.5 },
            PolygonPoint { chroma: 50.0, value: 5.5 },
            PolygonPoint { chroma: 50.0, value: 4.5 },
        ],
    },
    // Color 95: polygon 1
    PolygonDefinition {
        color_number: 95,
        polygon_group: 1,
        hue1: "1Y",
        hue2: "4Y",
        points: &[
            PolygonPoint { chroma: 1.2, value: 2.5 },
            PolygonPoint { chroma: 1.2, value: 4.5 },
            PolygonPoint { chroma: 50.0, value: 4.5 },
            PolygonPoint { chroma: 50.0, value: 2.5 },
        ],
    },
    // Color 96: polygon 1
    PolygonDefinition {
        color_number: 96,
        polygon_group: 1,
        hue1: "1Y",
        hue2: "4Y",
        points: &[
            PolygonPoint { chroma: 1.0, value: 0.0 },
            PolygonPoint { chroma: 1.0, value: 1.5 },
            PolygonPoint { chroma: 0.5, value: 1.5 },
            PolygonPoint { chroma: 0.5, value: 2.5 },
            PolygonPoint { chroma: 50.0, value: 2.5 },
            PolygonPoint { chroma: 50.0, value: 0.0 },
        ],
    },
    // Color 97: polygon 1
    PolygonDefinition {
        color_number: 97,
        polygon_group: 1,
        hue1: "7Y",
        hue2: "2GY",
        points: &[
            PolygonPoint { chroma: 11.0, value: 5.5 },
            PolygonPoint { chroma: 11.0, value: 10.0 },
            PolygonPoint { chroma: 50.0, value: 10.0 },
            PolygonPoint { chroma: 50.0, value: 5.5 },
        ],
    },
    // Color 98: polygon 1
    PolygonDefinition {
        color_number: 98,
        polygon_group: 1,
        hue1: "7Y",
        hue2: "2GY",
        points: &[
            PolygonPoint { chroma: 8.0, value: 8.0 },
            PolygonPoint { chroma: 8.0, value: 10.0 },
            PolygonPoint { chroma: 11.0, value: 10.0 },
            PolygonPoint { chroma: 11.0, value: 8.0 },
        ],
    },
    // Color 99: polygon 1
    PolygonDefinition {
        color_number: 99,
        polygon_group: 1,
        hue1: "7Y",
        hue2: "2GY",
        points: &[
            PolygonPoint { chroma: 8.0, value: 6.5 },
            PolygonPoint { chroma: 8.0, value: 8.0 },
            PolygonPoint { chroma: 11.0, value: 8.0 },
            PolygonPoint { chroma: 11.0, value: 6.5 },
        ],
    },
    // Color 100: polygon 1
    PolygonDefinition {
        color_number: 100,
        polygon_group: 1,
        hue1: "7Y",
        hue2: "2GY",
        points: &[
            PolygonPoint { chroma: 8.0, value: 5.5 },
            PolygonPoint { chroma: 8.0, value: 6.5 },
            PolygonPoint { chroma: 11.0, value: 6.5 },
            PolygonPoint { chroma: 11.0, value: 5.5 },
        ],
    },
    // Color 101: polygon 1
    PolygonDefinition {
        color_number: 101,
        polygon_group: 1,
        hue1: "7Y",
        hue2: "2GY",
        points: &[
            PolygonPoint { chroma: 5.0, value: 8.0 },
            PolygonPoint { chroma: 5.0, value: 10.0 },
            PolygonPoint { chroma: 8.0, value: 10.0 },
            PolygonPoint { chroma: 8.0, value: 8.0 },
        ],
    },
    // Color 102: polygon 1
    PolygonDefinition {
        color_number: 102,
        polygon_group: 1,
        hue1: "7Y",
        hue2: "2GY",
        points: &[
            PolygonPoint { chroma: 5.0, value: 6.5 },
            PolygonPoint { chroma: 5.0, value: 8.0 },
            PolygonPoint { chroma: 8.0, value: 8.0 },
            PolygonPoint { chroma: 8.0, value: 6.5 },
        ],
    },
    // Color 103: polygon 1
    PolygonDefinition {
        color_number: 103,
        polygon_group: 1,
        hue1: "7Y",
        hue2: "2GY",
        points: &[
            PolygonPoint { chroma: 5.0, value: 5.5 },
            PolygonPoint { chroma: 5.0, value: 6.5 },
            PolygonPoint { chroma: 8.0, value: 6.5 },
            PolygonPoint { chroma: 8.0, value: 5.5 },
        ],
    },
    // Color 104: polygon 1
    PolygonDefinition {
        color_number: 104,
        polygon_group: 1,
        hue1: "7Y",
        hue2: "2GY",
        points: &[
            PolygonPoint { chroma: 3.0, value: 8.0 },
            PolygonPoint { chroma: 3.0, value: 10.0 },
            PolygonPoint { chroma: 5.0, value: 10.0 },
            PolygonPoint { chroma: 5.0, value: 8.0 },
        ],
    },
    // Color 105: polygon 1
    PolygonDefinition {
        color_number: 105,
        polygon_group: 1,
        hue1: "7Y",
        hue2: "2GY",
        points: &[
            PolygonPoint { chroma: 3.0, value: 6.5 },
            PolygonPoint { chroma: 3.0, value: 8.0 },
            PolygonPoint { chroma: 5.0, value: 8.0 },
            PolygonPoint { chroma: 5.0, value: 6.5 },
        ],
    },
    // Color 106: polygon 1
    PolygonDefinition {
        color_number: 106,
        polygon_group: 1,
        hue1: "4Y",
        hue2: "7Y",
        points: &[
            PolygonPoint { chroma: 3.0, value: 4.5 },
            PolygonPoint { chroma: 3.0, value: 5.5 },
            PolygonPoint { chroma: 50.0, value: 5.5 },
            PolygonPoint { chroma: 50.0, value: 4.5 },
        ],
    },
    // Color 106: polygon 2
    PolygonDefinition {
        color_number: 106,
        polygon_group: 2,
        hue1: "7Y",
        hue2: "2GY",
        points: &[
            PolygonPoint { chroma: 3.0, value: 4.5 },
            PolygonPoint { chroma: 3.0, value: 6.5 },
            PolygonPoint { chroma: 5.0, value: 6.5 },
            PolygonPoint { chroma: 5.0, value: 5.5 },
            PolygonPoint { chroma: 50.0, value: 5.5 },
            PolygonPoint { chroma: 50.0, value: 4.5 },
        ],
    },
    // Color 107: polygon 1
    PolygonDefinition {
        color_number: 107,
        polygon_group: 1,
        hue1: "4Y",
        hue2: "2GY",
        points: &[
            PolygonPoint { chroma: 3.0, value: 2.5 },
            PolygonPoint { chroma: 3.0, value: 4.5 },
            PolygonPoint { chroma: 50.0, value: 4.5 },
            PolygonPoint { chroma: 50.0, value: 2.5 },
        ],
    },
    // Color 108: polygon 1
    PolygonDefinition {
        color_number: 108,
        polygon_group: 1,
        hue1: "4Y",
        hue2: "2GY",
        points: &[
            PolygonPoint { chroma: 1.0, value: 0.0 },
            PolygonPoint { chroma: 1.0, value: 1.5 },
            PolygonPoint { chroma: 3.0, value: 1.5 },
            PolygonPoint { chroma: 3.0, value: 2.5 },
            PolygonPoint { chroma: 50.0, value: 2.5 },
            PolygonPoint { chroma: 50.0, value: 0.0 },
        ],
    },
    // Color 109: polygon 1
    PolygonDefinition {
        color_number: 109,
        polygon_group: 1,
        hue1: "4Y",
        hue2: "9Y",
        points: &[
            PolygonPoint { chroma: 2.0, value: 4.5 },
            PolygonPoint { chroma: 2.0, value: 6.5 },
            PolygonPoint { chroma: 3.0, value: 6.5 },
            PolygonPoint { chroma: 3.0, value: 4.5 },
        ],
    },
    // Color 109: polygon 2
    PolygonDefinition {
        color_number: 109,
        polygon_group: 2,
        hue1: "9Y",
        hue2: "2GY",
        points: &[
            PolygonPoint { chroma: 1.2, value: 4.5 },
            PolygonPoint { chroma: 1.2, value: 6.5 },
            PolygonPoint { chroma: 3.0, value: 6.5 },
            PolygonPoint { chroma: 3.0, value: 4.5 },
        ],
    },
    // Color 110: polygon 1
    PolygonDefinition {
        color_number: 110,
        polygon_group: 1,
        hue1: "4Y",
        hue2: "9Y",
        points: &[
            PolygonPoint { chroma: 1.5, value: 2.5 },
            PolygonPoint { chroma: 1.5, value: 4.5 },
            PolygonPoint { chroma: 3.0, value: 4.5 },
            PolygonPoint { chroma: 3.0, value: 2.5 },
        ],
    },
    // Color 110: polygon 2
    PolygonDefinition {
        color_number: 110,
        polygon_group: 2,
        hue1: "9Y",
        hue2: "2GY",
        points: &[
            PolygonPoint { chroma: 1.2, value: 2.5 },
            PolygonPoint { chroma: 1.2, value: 4.5 },
            PolygonPoint { chroma: 3.0, value: 4.5 },
            PolygonPoint { chroma: 3.0, value: 2.5 },
        ],
    },
    // Color 111: polygon 1
    PolygonDefinition {
        color_number: 111,
        polygon_group: 1,
        hue1: "4Y",
        hue2: "2GY",
        points: &[
            PolygonPoint { chroma: 0.5, value: 1.5 },
            PolygonPoint { chroma: 0.5, value: 2.5 },
            PolygonPoint { chroma: 3.0, value: 2.5 },
            PolygonPoint { chroma: 3.0, value: 1.5 },
        ],
    },
    // Color 112: polygon 1
    PolygonDefinition {
        color_number: 112,
        polygon_group: 1,
        hue1: "4Y",
        hue2: "9Y",
        points: &[
            PolygonPoint { chroma: 0.7, value: 4.5 },
            PolygonPoint { chroma: 0.7, value: 6.5 },
            PolygonPoint { chroma: 2.0, value: 6.5 },
            PolygonPoint { chroma: 2.0, value: 4.5 },
        ],
    },
    // Color 112: polygon 2
    PolygonDefinition {
        color_number: 112,
        polygon_group: 2,
        hue1: "9Y",
        hue2: "4GY",
        points: &[
            PolygonPoint { chroma: 0.5, value: 4.5 },
            PolygonPoint { chroma: 0.5, value: 6.5 },
            PolygonPoint { chroma: 1.2, value: 6.5 },
            PolygonPoint { chroma: 1.2, value: 4.5 },
        ],
    },
    // Color 113: polygon 1
    PolygonDefinition {
        color_number: 113,
        polygon_group: 1,
        hue1: "4Y",
        hue2: "9Y",
        points: &[
            PolygonPoint { chroma: 0.5, value: 2.5 },
            PolygonPoint { chroma: 0.5, value: 4.5 },
            PolygonPoint { chroma: 1.5, value: 4.5 },
            PolygonPoint { chroma: 1.5, value: 2.5 },
        ],
    },
    // Color 113: polygon 2
    PolygonDefinition {
        color_number: 113,
        polygon_group: 2,
        hue1: "9Y",
        hue2: "4GY",
        points: &[
            PolygonPoint { chroma: 0.5, value: 2.5 },
            PolygonPoint { chroma: 0.5, value: 4.5 },
            PolygonPoint { chroma: 1.2, value: 4.5 },
            PolygonPoint { chroma: 1.2, value: 2.5 },
        ],
    },
    // Color 114: polygon 1
    PolygonDefinition {
        color_number: 114,
        polygon_group: 1,
        hue1: "4Y",
        hue2: "4GY",
        points: &[
            PolygonPoint { chroma: 0.5, value: 0.0 },
            PolygonPoint { chroma: 0.5, value: 1.5 },
            PolygonPoint { chroma: 1.0, value: 1.5 },
            PolygonPoint { chroma: 1.0, value: 0.0 },
        ],
    },
    // Color 115: polygon 1
    PolygonDefinition {
        color_number: 115,
        polygon_group: 1,
        hue1: "2GY",
        hue2: "8GY",
        points: &[
            PolygonPoint { chroma: 11.0, value: 3.5 },
            PolygonPoint { chroma: 11.0, value: 10.0 },
            PolygonPoint { chroma: 50.0, value: 10.0 },
            PolygonPoint { chroma: 50.0, value: 3.5 },
        ],
    },
    // Color 116: polygon 1
    PolygonDefinition {
        color_number: 116,
        polygon_group: 1,
        hue1: "2GY",
        hue2: "8GY",
        points: &[
            PolygonPoint { chroma: 7.0, value: 7.5 },
            PolygonPoint { chroma: 7.0, value: 10.0 },
            PolygonPoint { chroma: 11.0, value: 10.0 },
            PolygonPoint { chroma: 11.0, value: 7.5 },
        ],
    },
    // Color 117: polygon 1
    PolygonDefinition {
        color_number: 117,
        polygon_group: 1,
        hue1: "2GY",
        hue2: "8GY",
        points: &[
            PolygonPoint { chroma: 7.0, value: 4.5 },
            PolygonPoint { chroma: 7.0, value: 7.5 },
            PolygonPoint { chroma: 11.0, value: 7.5 },
            PolygonPoint { chroma: 11.0, value: 4.5 },
        ],
    },
    // Color 118: polygon 1
    PolygonDefinition {
        color_number: 118,
        polygon_group: 1,
        hue1: "2GY",
        hue2: "8GY",
        points: &[
            PolygonPoint { chroma: 7.0, value: 3.5 },
            PolygonPoint { chroma: 7.0, value: 4.5 },
            PolygonPoint { chroma: 11.0, value: 4.5 },
            PolygonPoint { chroma: 11.0, value: 3.5 },
        ],
    },
    // Color 119: polygon 1
    PolygonDefinition {
        color_number: 119,
        polygon_group: 1,
        hue1: "2GY",
        hue2: "8GY",
        points: &[
            PolygonPoint { chroma: 3.0, value: 7.5 },
            PolygonPoint { chroma: 3.0, value: 10.0 },
            PolygonPoint { chroma: 7.0, value: 10.0 },
            PolygonPoint { chroma: 7.0, value: 7.5 },
        ],
    },
    // Color 120: polygon 1
    PolygonDefinition {
        color_number: 120,
        polygon_group: 1,
        hue1: "2GY",
        hue2: "8GY",
        points: &[
            PolygonPoint { chroma: 3.0, value: 4.5 },
            PolygonPoint { chroma: 3.0, value: 7.5 },
            PolygonPoint { chroma: 7.0, value: 7.5 },
            PolygonPoint { chroma: 7.0, value: 4.5 },
        ],
    },
    // Color 121: polygon 1
    PolygonDefinition {
        color_number: 121,
        polygon_group: 1,
        hue1: "9Y",
        hue2: "8GY",
        points: &[
            PolygonPoint { chroma: 1.2, value: 7.5 },
            PolygonPoint { chroma: 1.2, value: 10.0 },
            PolygonPoint { chroma: 3.0, value: 10.0 },
            PolygonPoint { chroma: 3.0, value: 7.5 },
        ],
    },
    // Color 122: polygon 1
    PolygonDefinition {
        color_number: 122,
        polygon_group: 1,
        hue1: "9Y",
        hue2: "2GY",
        points: &[
            PolygonPoint { chroma: 1.2, value: 6.5 },
            PolygonPoint { chroma: 1.2, value: 7.5 },
            PolygonPoint { chroma: 3.0, value: 7.5 },
            PolygonPoint { chroma: 3.0, value: 6.5 },
        ],
    },
    // Color 122: polygon 2
    PolygonDefinition {
        color_number: 122,
        polygon_group: 2,
        hue1: "2GY",
        hue2: "8GY",
        points: &[
            PolygonPoint { chroma: 1.2, value: 4.5 },
            PolygonPoint { chroma: 1.2, value: 7.5 },
            PolygonPoint { chroma: 3.0, value: 7.5 },
            PolygonPoint { chroma: 3.0, value: 4.5 },
        ],
    },
    // Color 123: polygon 1
    PolygonDefinition {
        color_number: 123,
        polygon_group: 1,
        hue1: "2GY",
        hue2: "8GY",
        points: &[
            PolygonPoint { chroma: 7.0, value: 2.5 },
            PolygonPoint { chroma: 7.0, value: 3.5 },
            PolygonPoint { chroma: 50.0, value: 3.5 },
            PolygonPoint { chroma: 50.0, value: 2.5 },
        ],
    },
    // Color 124: polygon 1
    PolygonDefinition {
        color_number: 124,
        polygon_group: 1,
        hue1: "2GY",
        hue2: "8GY",
        points: &[
            PolygonPoint { chroma: 7.0, value: 0.0 },
            PolygonPoint { chroma: 7.0, value: 2.5 },
            PolygonPoint { chroma: 50.0, value: 2.5 },
            PolygonPoint { chroma: 50.0, value: 0.0 },
        ],
    },
    // Color 125: polygon 1
    PolygonDefinition {
        color_number: 125,
        polygon_group: 1,
        hue1: "2GY",
        hue2: "8GY",
        points: &[
            PolygonPoint { chroma: 3.0, value: 2.5 },
            PolygonPoint { chroma: 3.0, value: 4.5 },
            PolygonPoint { chroma: 7.0, value: 4.5 },
            PolygonPoint { chroma: 7.0, value: 2.5 },
        ],
    },
    // Color 126: polygon 1
    PolygonDefinition {
        color_number: 126,
        polygon_group: 1,
        hue1: "2GY",
        hue2: "8GY",
        points: &[
            PolygonPoint { chroma: 1.0, value: 0.0 },
            PolygonPoint { chroma: 1.0, value: 1.5 },
            PolygonPoint { chroma: 3.0, value: 1.5 },
            PolygonPoint { chroma: 3.0, value: 2.5 },
            PolygonPoint { chroma: 7.0, value: 2.5 },
            PolygonPoint { chroma: 7.0, value: 0.0 },
        ],
    },
    // Color 127: polygon 1
    PolygonDefinition {
        color_number: 127,
        polygon_group: 1,
        hue1: "2GY",
        hue2: "8GY",
        points: &[
            PolygonPoint { chroma: 1.2, value: 2.5 },
            PolygonPoint { chroma: 1.2, value: 4.5 },
            PolygonPoint { chroma: 3.0, value: 4.5 },
            PolygonPoint { chroma: 3.0, value: 2.5 },
        ],
    },
    // Color 128: polygon 1
    PolygonDefinition {
        color_number: 128,
        polygon_group: 1,
        hue1: "2GY",
        hue2: "8GY",
        points: &[
            PolygonPoint { chroma: 0.5, value: 1.5 },
            PolygonPoint { chroma: 0.5, value: 2.5 },
            PolygonPoint { chroma: 3.0, value: 2.5 },
            PolygonPoint { chroma: 3.0, value: 1.5 },
        ],
    },
    // Color 129: polygon 1
    PolygonDefinition {
        color_number: 129,
        polygon_group: 1,
        hue1: "8GY",
        hue2: "3G",
        points: &[
            PolygonPoint { chroma: 11.0, value: 4.5 },
            PolygonPoint { chroma: 11.0, value: 10.0 },
            PolygonPoint { chroma: 50.0, value: 10.0 },
            PolygonPoint { chroma: 50.0, value: 4.5 },
        ],
    },
    // Color 130: polygon 1
    PolygonDefinition {
        color_number: 130,
        polygon_group: 1,
        hue1: "8GY",
        hue2: "3G",
        points: &[
            PolygonPoint { chroma: 7.0, value: 6.5 },
            PolygonPoint { chroma: 7.0, value: 10.0 },
            PolygonPoint { chroma: 11.0, value: 10.0 },
            PolygonPoint { chroma: 11.0, value: 6.5 },
        ],
    },
    // Color 131: polygon 1
    PolygonDefinition {
        color_number: 131,
        polygon_group: 1,
        hue1: "8GY",
        hue2: "3G",
        points: &[
            PolygonPoint { chroma: 7.0, value: 4.5 },
            PolygonPoint { chroma: 7.0, value: 6.5 },
            PolygonPoint { chroma: 11.0, value: 6.5 },
            PolygonPoint { chroma: 11.0, value: 4.5 },
        ],
    },
    // Color 132: polygon 1
    PolygonDefinition {
        color_number: 132,
        polygon_group: 1,
        hue1: "8GY",
        hue2: "3G",
        points: &[
            PolygonPoint { chroma: 7.0, value: 2.5 },
            PolygonPoint { chroma: 7.0, value: 4.5 },
            PolygonPoint { chroma: 50.0, value: 4.5 },
            PolygonPoint { chroma: 50.0, value: 2.5 },
        ],
    },
    // Color 133: polygon 1
    PolygonDefinition {
        color_number: 133,
        polygon_group: 1,
        hue1: "8GY",
        hue2: "3G",
        points: &[
            PolygonPoint { chroma: 7.0, value: 0.0 },
            PolygonPoint { chroma: 7.0, value: 2.5 },
            PolygonPoint { chroma: 50.0, value: 2.5 },
            PolygonPoint { chroma: 50.0, value: 0.0 },
        ],
    },
    // Color 134: polygon 1
    PolygonDefinition {
        color_number: 134,
        polygon_group: 1,
        hue1: "8GY",
        hue2: "3G",
        points: &[
            PolygonPoint { chroma: 2.5, value: 8.5 },
            PolygonPoint { chroma: 2.5, value: 10.0 },
            PolygonPoint { chroma: 7.0, value: 10.0 },
            PolygonPoint { chroma: 7.0, value: 8.5 },
        ],
    },
    // Color 135: polygon 1
    PolygonDefinition {
        color_number: 135,
        polygon_group: 1,
        hue1: "8GY",
        hue2: "3G",
        points: &[
            PolygonPoint { chroma: 2.5, value: 6.5 },
            PolygonPoint { chroma: 2.5, value: 8.5 },
            PolygonPoint { chroma: 7.0, value: 8.5 },
            PolygonPoint { chroma: 7.0, value: 6.5 },
        ],
    },
    // Color 136: polygon 1
    PolygonDefinition {
        color_number: 136,
        polygon_group: 1,
        hue1: "8GY",
        hue2: "3G",
        points: &[
            PolygonPoint { chroma: 2.5, value: 4.5 },
            PolygonPoint { chroma: 2.5, value: 6.5 },
            PolygonPoint { chroma: 7.0, value: 6.5 },
            PolygonPoint { chroma: 7.0, value: 4.5 },
        ],
    },
    // Color 137: polygon 1
    PolygonDefinition {
        color_number: 137,
        polygon_group: 1,
        hue1: "8GY",
        hue2: "3G",
        points: &[
            PolygonPoint { chroma: 2.5, value: 2.5 },
            PolygonPoint { chroma: 2.5, value: 4.5 },
            PolygonPoint { chroma: 7.0, value: 4.5 },
            PolygonPoint { chroma: 7.0, value: 2.5 },
        ],
    },
    // Color 138: polygon 1
    PolygonDefinition {
        color_number: 138,
        polygon_group: 1,
        hue1: "8GY",
        hue2: "3G",
        points: &[
            PolygonPoint { chroma: 2.0, value: 0.0 },
            PolygonPoint { chroma: 2.0, value: 2.5 },
            PolygonPoint { chroma: 7.0, value: 2.5 },
            PolygonPoint { chroma: 7.0, value: 0.0 },
        ],
    },
    // Color 139: polygon 1
    PolygonDefinition {
        color_number: 139,
        polygon_group: 1,
        hue1: "3G",
        hue2: "9G",
        points: &[
            PolygonPoint { chroma: 11.0, value: 0.0 },
            PolygonPoint { chroma: 11.0, value: 10.0 },
            PolygonPoint { chroma: 50.0, value: 10.0 },
            PolygonPoint { chroma: 50.0, value: 0.0 },
        ],
    },
    // Color 140: polygon 1
    PolygonDefinition {
        color_number: 140,
        polygon_group: 1,
        hue1: "3G",
        hue2: "9G",
        points: &[
            PolygonPoint { chroma: 7.0, value: 5.5 },
            PolygonPoint { chroma: 7.0, value: 10.0 },
            PolygonPoint { chroma: 11.0, value: 10.0 },
            PolygonPoint { chroma: 11.0, value: 5.5 },
        ],
    },
    // Color 141: polygon 1
    PolygonDefinition {
        color_number: 141,
        polygon_group: 1,
        hue1: "3G",
        hue2: "9G",
        points: &[
            PolygonPoint { chroma: 7.0, value: 3.5 },
            PolygonPoint { chroma: 7.0, value: 5.5 },
            PolygonPoint { chroma: 11.0, value: 5.5 },
            PolygonPoint { chroma: 11.0, value: 3.5 },
        ],
    },
    // Color 142: polygon 1
    PolygonDefinition {
        color_number: 142,
        polygon_group: 1,
        hue1: "3G",
        hue2: "9G",
        points: &[
            PolygonPoint { chroma: 7.0, value: 0.0 },
            PolygonPoint { chroma: 7.0, value: 3.5 },
            PolygonPoint { chroma: 11.0, value: 3.5 },
            PolygonPoint { chroma: 11.0, value: 0.0 },
        ],
    },
    // Color 143: polygon 1
    PolygonDefinition {
        color_number: 143,
        polygon_group: 1,
        hue1: "3G",
        hue2: "9G",
        points: &[
            PolygonPoint { chroma: 2.5, value: 7.5 },
            PolygonPoint { chroma: 2.5, value: 10.0 },
            PolygonPoint { chroma: 7.0, value: 10.0 },
            PolygonPoint { chroma: 7.0, value: 7.5 },
        ],
    },
    // Color 144: polygon 1
    PolygonDefinition {
        color_number: 144,
        polygon_group: 1,
        hue1: "3G",
        hue2: "9G",
        points: &[
            PolygonPoint { chroma: 2.5, value: 5.5 },
            PolygonPoint { chroma: 2.5, value: 7.5 },
            PolygonPoint { chroma: 7.0, value: 7.5 },
            PolygonPoint { chroma: 7.0, value: 5.5 },
        ],
    },
    // Color 145: polygon 1
    PolygonDefinition {
        color_number: 145,
        polygon_group: 1,
        hue1: "3G",
        hue2: "9G",
        points: &[
            PolygonPoint { chroma: 2.5, value: 3.5 },
            PolygonPoint { chroma: 2.5, value: 5.5 },
            PolygonPoint { chroma: 7.0, value: 5.5 },
            PolygonPoint { chroma: 7.0, value: 3.5 },
        ],
    },
    // Color 146: polygon 1
    PolygonDefinition {
        color_number: 146,
        polygon_group: 1,
        hue1: "3G",
        hue2: "9G",
        points: &[
            PolygonPoint { chroma: 2.0, value: 2.0 },
            PolygonPoint { chroma: 2.0, value: 2.5 },
            PolygonPoint { chroma: 2.5, value: 2.5 },
            PolygonPoint { chroma: 2.5, value: 3.5 },
            PolygonPoint { chroma: 7.0, value: 3.5 },
            PolygonPoint { chroma: 7.0, value: 2.0 },
        ],
    },
    // Color 147: polygon 1
    PolygonDefinition {
        color_number: 147,
        polygon_group: 1,
        hue1: "3G",
        hue2: "9G",
        points: &[
            PolygonPoint { chroma: 2.0, value: 0.0 },
            PolygonPoint { chroma: 2.0, value: 2.0 },
            PolygonPoint { chroma: 7.0, value: 2.0 },
            PolygonPoint { chroma: 7.0, value: 0.0 },
        ],
    },
    // Color 148: polygon 1
    PolygonDefinition {
        color_number: 148,
        polygon_group: 1,
        hue1: "8GY",
        hue2: "10BG",
        points: &[
            PolygonPoint { chroma: 1.2, value: 7.5 },
            PolygonPoint { chroma: 1.2, value: 10.0 },
            PolygonPoint { chroma: 2.5, value: 10.0 },
            PolygonPoint { chroma: 2.5, value: 7.5 },
        ],
    },
    // Color 149: polygon 1
    PolygonDefinition {
        color_number: 149,
        polygon_group: 1,
        hue1: "8GY",
        hue2: "10BG",
        points: &[
            PolygonPoint { chroma: 1.2, value: 5.5 },
            PolygonPoint { chroma: 1.2, value: 7.5 },
            PolygonPoint { chroma: 2.5, value: 7.5 },
            PolygonPoint { chroma: 2.5, value: 5.5 },
        ],
    },
    // Color 150: polygon 1
    PolygonDefinition {
        color_number: 150,
        polygon_group: 1,
        hue1: "8GY",
        hue2: "10BG",
        points: &[
            PolygonPoint { chroma: 1.2, value: 3.5 },
            PolygonPoint { chroma: 1.2, value: 5.5 },
            PolygonPoint { chroma: 2.5, value: 5.5 },
            PolygonPoint { chroma: 2.5, value: 3.5 },
        ],
    },
    // Color 151: polygon 1
    PolygonDefinition {
        color_number: 151,
        polygon_group: 1,
        hue1: "8GY",
        hue2: "10BG",
        points: &[
            PolygonPoint { chroma: 0.5, value: 2.0 },
            PolygonPoint { chroma: 0.5, value: 2.5 },
            PolygonPoint { chroma: 1.2, value: 2.5 },
            PolygonPoint { chroma: 1.2, value: 3.5 },
            PolygonPoint { chroma: 2.5, value: 3.5 },
            PolygonPoint { chroma: 2.5, value: 2.5 },
            PolygonPoint { chroma: 2.0, value: 2.5 },
            PolygonPoint { chroma: 2.0, value: 2.0 },
        ],
    },
    // Color 152: polygon 1
    PolygonDefinition {
        color_number: 152,
        polygon_group: 1,
        hue1: "8GY",
        hue2: "10BG",
        points: &[
            PolygonPoint { chroma: 1.0, value: 0.0 },
            PolygonPoint { chroma: 1.0, value: 2.0 },
            PolygonPoint { chroma: 2.0, value: 2.0 },
            PolygonPoint { chroma: 2.0, value: 0.0 },
        ],
    },
    // Color 153: polygon 1
    PolygonDefinition {
        color_number: 153,
        polygon_group: 1,
        hue1: "4GY",
        hue2: "10BG",
        points: &[
            PolygonPoint { chroma: 0.5, value: 8.5 },
            PolygonPoint { chroma: 0.5, value: 10.0 },
            PolygonPoint { chroma: 1.2, value: 10.0 },
            PolygonPoint { chroma: 1.2, value: 8.5 },
        ],
    },
    // Color 154: polygon 1
    PolygonDefinition {
        color_number: 154,
        polygon_group: 1,
        hue1: "4GY",
        hue2: "10BG",
        points: &[
            PolygonPoint { chroma: 0.5, value: 6.5 },
            PolygonPoint { chroma: 0.5, value: 8.5 },
            PolygonPoint { chroma: 1.2, value: 8.5 },
            PolygonPoint { chroma: 1.2, value: 6.5 },
        ],
    },
    // Color 155: polygon 1
    PolygonDefinition {
        color_number: 155,
        polygon_group: 1,
        hue1: "4GY",
        hue2: "10BG",
        points: &[
            PolygonPoint { chroma: 0.5, value: 4.5 },
            PolygonPoint { chroma: 0.5, value: 6.5 },
            PolygonPoint { chroma: 1.2, value: 6.5 },
            PolygonPoint { chroma: 1.2, value: 4.5 },
        ],
    },
    // Color 156: polygon 1
    PolygonDefinition {
        color_number: 156,
        polygon_group: 1,
        hue1: "4GY",
        hue2: "10BG",
        points: &[
            PolygonPoint { chroma: 0.5, value: 2.5 },
            PolygonPoint { chroma: 0.5, value: 4.5 },
            PolygonPoint { chroma: 1.2, value: 4.5 },
            PolygonPoint { chroma: 1.2, value: 2.5 },
        ],
    },
    // Color 157: polygon 1
    PolygonDefinition {
        color_number: 157,
        polygon_group: 1,
        hue1: "4GY",
        hue2: "8GY",
        points: &[
            PolygonPoint { chroma: 0.5, value: 0.0 },
            PolygonPoint { chroma: 0.5, value: 1.5 },
            PolygonPoint { chroma: 1.0, value: 1.5 },
            PolygonPoint { chroma: 1.0, value: 0.0 },
        ],
    },
    // Color 157: polygon 2
    PolygonDefinition {
        color_number: 157,
        polygon_group: 2,
        hue1: "8GY",
        hue2: "10BG",
        points: &[
            PolygonPoint { chroma: 0.5, value: 0.0 },
            PolygonPoint { chroma: 0.5, value: 2.0 },
            PolygonPoint { chroma: 1.0, value: 2.0 },
            PolygonPoint { chroma: 1.0, value: 0.0 },
        ],
    },
    // Color 158: polygon 1
    PolygonDefinition {
        color_number: 158,
        polygon_group: 1,
        hue1: "9G",
        hue2: "10BG",
        points: &[
            PolygonPoint { chroma: 11.0, value: 0.0 },
            PolygonPoint { chroma: 11.0, value: 10.0 },
            PolygonPoint { chroma: 50.0, value: 10.0 },
            PolygonPoint { chroma: 50.0, value: 0.0 },
        ],
    },
    // Color 159: polygon 1
    PolygonDefinition {
        color_number: 159,
        polygon_group: 1,
        hue1: "9G",
        hue2: "10BG",
        points: &[
            PolygonPoint { chroma: 7.0, value: 5.5 },
            PolygonPoint { chroma: 7.0, value: 10.0 },
            PolygonPoint { chroma: 11.0, value: 10.0 },
            PolygonPoint { chroma: 11.0, value: 5.5 },
        ],
    },
    // Color 160: polygon 1
    PolygonDefinition {
        color_number: 160,
        polygon_group: 1,
        hue1: "9G",
        hue2: "10BG",
        points: &[
            PolygonPoint { chroma: 7.0, value: 3.5 },
            PolygonPoint { chroma: 7.0, value: 5.5 },
            PolygonPoint { chroma: 11.0, value: 5.5 },
            PolygonPoint { chroma: 11.0, value: 3.5 },
        ],
    },
    // Color 161: polygon 1
    PolygonDefinition {
        color_number: 161,
        polygon_group: 1,
        hue1: "9G",
        hue2: "10BG",
        points: &[
            PolygonPoint { chroma: 7.0, value: 0.0 },
            PolygonPoint { chroma: 7.0, value: 3.5 },
            PolygonPoint { chroma: 11.0, value: 3.5 },
            PolygonPoint { chroma: 11.0, value: 0.0 },
        ],
    },
    // Color 162: polygon 1
    PolygonDefinition {
        color_number: 162,
        polygon_group: 1,
        hue1: "9G",
        hue2: "10BG",
        points: &[
            PolygonPoint { chroma: 2.5, value: 7.5 },
            PolygonPoint { chroma: 2.5, value: 10.0 },
            PolygonPoint { chroma: 7.0, value: 10.0 },
            PolygonPoint { chroma: 7.0, value: 7.5 },
        ],
    },
    // Color 163: polygon 1
    PolygonDefinition {
        color_number: 163,
        polygon_group: 1,
        hue1: "9G",
        hue2: "10BG",
        points: &[
            PolygonPoint { chroma: 2.5, value: 5.5 },
            PolygonPoint { chroma: 2.5, value: 7.5 },
            PolygonPoint { chroma: 7.0, value: 7.5 },
            PolygonPoint { chroma: 7.0, value: 5.5 },
        ],
    },
    // Color 164: polygon 1
    PolygonDefinition {
        color_number: 164,
        polygon_group: 1,
        hue1: "9G",
        hue2: "10BG",
        points: &[
            PolygonPoint { chroma: 2.5, value: 3.5 },
            PolygonPoint { chroma: 2.5, value: 5.5 },
            PolygonPoint { chroma: 7.0, value: 5.5 },
            PolygonPoint { chroma: 7.0, value: 3.5 },
        ],
    },
    // Color 165: polygon 1
    PolygonDefinition {
        color_number: 165,
        polygon_group: 1,
        hue1: "9G",
        hue2: "10BG",
        points: &[
            PolygonPoint { chroma: 2.0, value: 2.0 },
            PolygonPoint { chroma: 2.0, value: 2.5 },
            PolygonPoint { chroma: 2.5, value: 2.5 },
            PolygonPoint { chroma: 2.5, value: 3.5 },
            PolygonPoint { chroma: 7.0, value: 3.5 },
            PolygonPoint { chroma: 7.0, value: 2.0 },
        ],
    },
    // Color 166: polygon 1
    PolygonDefinition {
        color_number: 166,
        polygon_group: 1,
        hue1: "9G",
        hue2: "10BG",
        points: &[
            PolygonPoint { chroma: 2.0, value: 0.0 },
            PolygonPoint { chroma: 2.0, value: 2.0 },
            PolygonPoint { chroma: 7.0, value: 2.0 },
            PolygonPoint { chroma: 7.0, value: 0.0 },
        ],
    },
    // Color 167: polygon 1
    PolygonDefinition {
        color_number: 167,
        polygon_group: 1,
        hue1: "10BG",
        hue2: "9B",
        points: &[
            PolygonPoint { chroma: 11.0, value: 0.0 },
            PolygonPoint { chroma: 11.0, value: 10.0 },
            PolygonPoint { chroma: 50.0, value: 10.0 },
            PolygonPoint { chroma: 50.0, value: 0.0 },
        ],
    },
    // Color 168: polygon 1
    PolygonDefinition {
        color_number: 168,
        polygon_group: 1,
        hue1: "10BG",
        hue2: "9B",
        points: &[
            PolygonPoint { chroma: 7.0, value: 5.5 },
            PolygonPoint { chroma: 7.0, value: 10.0 },
            PolygonPoint { chroma: 11.0, value: 10.0 },
            PolygonPoint { chroma: 11.0, value: 5.5 },
        ],
    },
    // Color 169: polygon 1
    PolygonDefinition {
        color_number: 169,
        polygon_group: 1,
        hue1: "10BG",
        hue2: "9B",
        points: &[
            PolygonPoint { chroma: 7.0, value: 3.5 },
            PolygonPoint { chroma: 7.0, value: 5.5 },
            PolygonPoint { chroma: 11.0, value: 5.5 },
            PolygonPoint { chroma: 11.0, value: 3.5 },
        ],
    },
    // Color 170: polygon 1
    PolygonDefinition {
        color_number: 170,
        polygon_group: 1,
        hue1: "10BG",
        hue2: "9B",
        points: &[
            PolygonPoint { chroma: 7.0, value: 0.0 },
            PolygonPoint { chroma: 7.0, value: 3.5 },
            PolygonPoint { chroma: 11.0, value: 3.5 },
            PolygonPoint { chroma: 11.0, value: 0.0 },
        ],
    },
    // Color 171: polygon 1
    PolygonDefinition {
        color_number: 171,
        polygon_group: 1,
        hue1: "10BG",
        hue2: "9B",
        points: &[
            PolygonPoint { chroma: 3.0, value: 7.5 },
            PolygonPoint { chroma: 3.0, value: 10.0 },
            PolygonPoint { chroma: 7.0, value: 10.0 },
            PolygonPoint { chroma: 7.0, value: 7.5 },
        ],
    },
    // Color 172: polygon 1
    PolygonDefinition {
        color_number: 172,
        polygon_group: 1,
        hue1: "10BG",
        hue2: "9B",
        points: &[
            PolygonPoint { chroma: 3.0, value: 5.5 },
            PolygonPoint { chroma: 3.0, value: 7.5 },
            PolygonPoint { chroma: 7.0, value: 7.5 },
            PolygonPoint { chroma: 7.0, value: 5.5 },
        ],
    },
    // Color 173: polygon 1
    PolygonDefinition {
        color_number: 173,
        polygon_group: 1,
        hue1: "10BG",
        hue2: "9B",
        points: &[
            PolygonPoint { chroma: 3.0, value: 3.5 },
            PolygonPoint { chroma: 3.0, value: 5.5 },
            PolygonPoint { chroma: 7.0, value: 5.5 },
            PolygonPoint { chroma: 7.0, value: 3.5 },
        ],
    },
    // Color 174: polygon 1
    PolygonDefinition {
        color_number: 174,
        polygon_group: 1,
        hue1: "10BG",
        hue2: "9B",
        points: &[
            PolygonPoint { chroma: 2.0, value: 2.0 },
            PolygonPoint { chroma: 2.0, value: 2.5 },
            PolygonPoint { chroma: 3.0, value: 2.5 },
            PolygonPoint { chroma: 3.0, value: 3.5 },
            PolygonPoint { chroma: 7.0, value: 3.5 },
            PolygonPoint { chroma: 7.0, value: 2.0 },
        ],
    },
    // Color 175: polygon 1
    PolygonDefinition {
        color_number: 175,
        polygon_group: 1,
        hue1: "10BG",
        hue2: "9B",
        points: &[
            PolygonPoint { chroma: 2.0, value: 0.0 },
            PolygonPoint { chroma: 2.0, value: 2.0 },
            PolygonPoint { chroma: 7.0, value: 2.0 },
            PolygonPoint { chroma: 7.0, value: 0.0 },
        ],
    },
    // Color 176: polygon 1
    PolygonDefinition {
        color_number: 176,
        polygon_group: 1,
        hue1: "9B",
        hue2: "7PB",
        points: &[
            PolygonPoint { chroma: 11.0, value: 0.0 },
            PolygonPoint { chroma: 11.0, value: 3.0 },
            PolygonPoint { chroma: 13.0, value: 3.0 },
            PolygonPoint { chroma: 13.0, value: 10.0 },
            PolygonPoint { chroma: 50.0, value: 10.0 },
            PolygonPoint { chroma: 50.0, value: 0.0 },
        ],
    },
    // Color 177: polygon 1
    PolygonDefinition {
        color_number: 177,
        polygon_group: 1,
        hue1: "9B",
        hue2: "7PB",
        points: &[
            PolygonPoint { chroma: 9.0, value: 5.5 },
            PolygonPoint { chroma: 9.0, value: 10.0 },
            PolygonPoint { chroma: 13.0, value: 10.0 },
            PolygonPoint { chroma: 13.0, value: 5.5 },
        ],
    },
    // Color 178: polygon 1
    PolygonDefinition {
        color_number: 178,
        polygon_group: 1,
        hue1: "9B",
        hue2: "7PB",
        points: &[
            PolygonPoint { chroma: 9.0, value: 3.0 },
            PolygonPoint { chroma: 9.0, value: 5.5 },
            PolygonPoint { chroma: 13.0, value: 5.5 },
            PolygonPoint { chroma: 13.0, value: 3.0 },
        ],
    },
    // Color 179: polygon 1
    PolygonDefinition {
        color_number: 179,
        polygon_group: 1,
        hue1: "9B",
        hue2: "7PB",
        points: &[
            PolygonPoint { chroma: 7.0, value: 0.0 },
            PolygonPoint { chroma: 7.0, value: 3.0 },
            PolygonPoint { chroma: 11.0, value: 3.0 },
            PolygonPoint { chroma: 11.0, value: 0.0 },
        ],
    },
    // Color 180: polygon 1
    PolygonDefinition {
        color_number: 180,
        polygon_group: 1,
        hue1: "9B",
        hue2: "5PB",
        points: &[
            PolygonPoint { chroma: 5.0, value: 7.5 },
            PolygonPoint { chroma: 5.0, value: 10.0 },
            PolygonPoint { chroma: 9.0, value: 10.0 },
            PolygonPoint { chroma: 9.0, value: 7.5 },
        ],
    },
    // Color 180: polygon 2
    PolygonDefinition {
        color_number: 180,
        polygon_group: 2,
        hue1: "5PB",
        hue2: "7PB",
        points: &[
            PolygonPoint { chroma: 7.0, value: 7.5 },
            PolygonPoint { chroma: 7.0, value: 10.0 },
            PolygonPoint { chroma: 9.0, value: 10.0 },
            PolygonPoint { chroma: 9.0, value: 7.5 },
        ],
    },
    // Color 181: polygon 1
    PolygonDefinition {
        color_number: 181,
        polygon_group: 1,
        hue1: "9B",
        hue2: "5PB",
        points: &[
            PolygonPoint { chroma: 5.0, value: 5.5 },
            PolygonPoint { chroma: 5.0, value: 7.5 },
            PolygonPoint { chroma: 9.0, value: 7.5 },
            PolygonPoint { chroma: 9.0, value: 5.5 },
        ],
    },
    // Color 181: polygon 2
    PolygonDefinition {
        color_number: 181,
        polygon_group: 2,
        hue1: "5PB",
        hue2: "7PB",
        points: &[
            PolygonPoint { chroma: 7.0, value: 5.5 },
            PolygonPoint { chroma: 7.0, value: 7.5 },
            PolygonPoint { chroma: 9.0, value: 7.5 },
            PolygonPoint { chroma: 9.0, value: 5.5 },
        ],
    },
    // Color 182: polygon 1
    PolygonDefinition {
        color_number: 182,
        polygon_group: 1,
        hue1: "9B",
        hue2: "5PB",
        points: &[
            PolygonPoint { chroma: 5.0, value: 3.0 },
            PolygonPoint { chroma: 5.0, value: 5.5 },
            PolygonPoint { chroma: 9.0, value: 5.5 },
            PolygonPoint { chroma: 9.0, value: 3.0 },
        ],
    },
    // Color 182: polygon 2
    PolygonDefinition {
        color_number: 182,
        polygon_group: 2,
        hue1: "5PB",
        hue2: "7PB",
        points: &[
            PolygonPoint { chroma: 5.0, value: 3.0 },
            PolygonPoint { chroma: 5.0, value: 4.5 },
            PolygonPoint { chroma: 7.0, value: 4.5 },
            PolygonPoint { chroma: 7.0, value: 5.5 },
            PolygonPoint { chroma: 9.0, value: 5.5 },
            PolygonPoint { chroma: 9.0, value: 3.0 },
        ],
    },
    // Color 183: polygon 1
    PolygonDefinition {
        color_number: 183,
        polygon_group: 1,
        hue1: "9B",
        hue2: "6PB",
        points: &[
            PolygonPoint { chroma: 2.0, value: 0.0 },
            PolygonPoint { chroma: 2.0, value: 2.5 },
            PolygonPoint { chroma: 3.0, value: 2.5 },
            PolygonPoint { chroma: 3.0, value: 3.0 },
            PolygonPoint { chroma: 7.0, value: 3.0 },
            PolygonPoint { chroma: 7.0, value: 0.0 },
        ],
    },
    // Color 183: polygon 2
    PolygonDefinition {
        color_number: 183,
        polygon_group: 2,
        hue1: "6PB",
        hue2: "7PB",
        points: &[
            PolygonPoint { chroma: 5.0, value: 0.0 },
            PolygonPoint { chroma: 5.0, value: 3.0 },
            PolygonPoint { chroma: 7.0, value: 3.0 },
            PolygonPoint { chroma: 7.0, value: 0.0 },
        ],
    },
    // Color 184: polygon 1
    PolygonDefinition {
        color_number: 184,
        polygon_group: 1,
        hue1: "10BG",
        hue2: "9B",
        points: &[
            PolygonPoint { chroma: 1.5, value: 7.5 },
            PolygonPoint { chroma: 1.5, value: 10.0 },
            PolygonPoint { chroma: 3.0, value: 10.0 },
            PolygonPoint { chroma: 3.0, value: 7.5 },
        ],
    },
    // Color 184: polygon 2
    PolygonDefinition {
        color_number: 184,
        polygon_group: 2,
        hue1: "9B",
        hue2: "5PB",
        points: &[
            PolygonPoint { chroma: 1.5, value: 7.5 },
            PolygonPoint { chroma: 1.5, value: 10.0 },
            PolygonPoint { chroma: 5.0, value: 10.0 },
            PolygonPoint { chroma: 5.0, value: 7.5 },
        ],
    },
    // Color 184: polygon 3
    PolygonDefinition {
        color_number: 184,
        polygon_group: 3,
        hue1: "5PB",
        hue2: "9PB",
        points: &[
            PolygonPoint { chroma: 1.5, value: 7.5 },
            PolygonPoint { chroma: 1.5, value: 10.0 },
            PolygonPoint { chroma: 3.0, value: 10.0 },
            PolygonPoint { chroma: 3.0, value: 7.5 },
        ],
    },
    // Color 185: polygon 1
    PolygonDefinition {
        color_number: 185,
        polygon_group: 1,
        hue1: "10BG",
        hue2: "9B",
        points: &[
            PolygonPoint { chroma: 1.5, value: 5.5 },
            PolygonPoint { chroma: 1.5, value: 7.5 },
            PolygonPoint { chroma: 3.0, value: 7.5 },
            PolygonPoint { chroma: 3.0, value: 5.5 },
        ],
    },
    // Color 185: polygon 2
    PolygonDefinition {
        color_number: 185,
        polygon_group: 2,
        hue1: "9B",
        hue2: "5PB",
        points: &[
            PolygonPoint { chroma: 1.5, value: 5.5 },
            PolygonPoint { chroma: 1.5, value: 7.5 },
            PolygonPoint { chroma: 5.0, value: 7.5 },
            PolygonPoint { chroma: 5.0, value: 5.5 },
        ],
    },
    // Color 185: polygon 3
    PolygonDefinition {
        color_number: 185,
        polygon_group: 3,
        hue1: "5PB",
        hue2: "9PB",
        points: &[
            PolygonPoint { chroma: 1.5, value: 5.5 },
            PolygonPoint { chroma: 1.5, value: 7.5 },
            PolygonPoint { chroma: 3.0, value: 7.5 },
            PolygonPoint { chroma: 3.0, value: 5.5 },
        ],
    },
    // Color 186: polygon 1
    PolygonDefinition {
        color_number: 186,
        polygon_group: 1,
        hue1: "10BG",
        hue2: "9B",
        points: &[
            PolygonPoint { chroma: 1.5, value: 3.0 },
            PolygonPoint { chroma: 1.5, value: 5.5 },
            PolygonPoint { chroma: 3.0, value: 5.5 },
            PolygonPoint { chroma: 3.0, value: 3.0 },
        ],
    },
    // Color 186: polygon 2
    PolygonDefinition {
        color_number: 186,
        polygon_group: 2,
        hue1: "9B",
        hue2: "5PB",
        points: &[
            PolygonPoint { chroma: 1.5, value: 3.0 },
            PolygonPoint { chroma: 1.5, value: 5.5 },
            PolygonPoint { chroma: 5.0, value: 5.5 },
            PolygonPoint { chroma: 5.0, value: 3.0 },
        ],
    },
    // Color 186: polygon 3
    PolygonDefinition {
        color_number: 186,
        polygon_group: 3,
        hue1: "5PB",
        hue2: "9PB",
        points: &[
            PolygonPoint { chroma: 1.5, value: 3.0 },
            PolygonPoint { chroma: 1.5, value: 5.5 },
            PolygonPoint { chroma: 3.0, value: 5.5 },
            PolygonPoint { chroma: 3.0, value: 3.0 },
        ],
    },
    // Color 187: polygon 1
    PolygonDefinition {
        color_number: 187,
        polygon_group: 1,
        hue1: "10BG",
        hue2: "9PB",
        points: &[
            PolygonPoint { chroma: 0.5, value: 2.0 },
            PolygonPoint { chroma: 0.5, value: 2.5 },
            PolygonPoint { chroma: 1.5, value: 2.5 },
            PolygonPoint { chroma: 1.5, value: 3.0 },
            PolygonPoint { chroma: 3.0, value: 3.0 },
            PolygonPoint { chroma: 3.0, value: 2.5 },
            PolygonPoint { chroma: 2.0, value: 2.5 },
            PolygonPoint { chroma: 2.0, value: 2.0 },
        ],
    },
    // Color 188: polygon 1
    PolygonDefinition {
        color_number: 188,
        polygon_group: 1,
        hue1: "10BG",
        hue2: "9PB",
        points: &[
            PolygonPoint { chroma: 1.0, value: 0.0 },
            PolygonPoint { chroma: 1.0, value: 2.0 },
            PolygonPoint { chroma: 2.0, value: 2.0 },
            PolygonPoint { chroma: 2.0, value: 0.0 },
        ],
    },
    // Color 189: polygon 1
    PolygonDefinition {
        color_number: 189,
        polygon_group: 1,
        hue1: "10BG",
        hue2: "9PB",
        points: &[
            PolygonPoint { chroma: 0.5, value: 8.5 },
            PolygonPoint { chroma: 0.5, value: 10.0 },
            PolygonPoint { chroma: 1.5, value: 10.0 },
            PolygonPoint { chroma: 1.5, value: 8.5 },
        ],
    },
    // Color 190: polygon 1
    PolygonDefinition {
        color_number: 190,
        polygon_group: 1,
        hue1: "10BG",
        hue2: "9PB",
        points: &[
            PolygonPoint { chroma: 0.5, value: 6.5 },
            PolygonPoint { chroma: 0.5, value: 8.5 },
            PolygonPoint { chroma: 1.5, value: 8.5 },
            PolygonPoint { chroma: 1.5, value: 6.5 },
        ],
    },
    // Color 191: polygon 1
    PolygonDefinition {
        color_number: 191,
        polygon_group: 1,
        hue1: "10BG",
        hue2: "9PB",
        points: &[
            PolygonPoint { chroma: 0.5, value: 4.5 },
            PolygonPoint { chroma: 0.5, value: 6.5 },
            PolygonPoint { chroma: 1.5, value: 6.5 },
            PolygonPoint { chroma: 1.5, value: 4.5 },
        ],
    },
    // Color 192: polygon 1
    PolygonDefinition {
        color_number: 192,
        polygon_group: 1,
        hue1: "10BG",
        hue2: "9PB",
        points: &[
            PolygonPoint { chroma: 0.5, value: 2.5 },
            PolygonPoint { chroma: 0.5, value: 4.5 },
            PolygonPoint { chroma: 1.5, value: 4.5 },
            PolygonPoint { chroma: 1.5, value: 2.5 },
        ],
    },
    // Color 193: polygon 1
    PolygonDefinition {
        color_number: 193,
        polygon_group: 1,
        hue1: "10BG",
        hue2: "9PB",
        points: &[
            PolygonPoint { chroma: 0.5, value: 0.0 },
            PolygonPoint { chroma: 0.5, value: 2.0 },
            PolygonPoint { chroma: 1.0, value: 2.0 },
            PolygonPoint { chroma: 1.0, value: 0.0 },
        ],
    },
    // Color 194: polygon 1
    PolygonDefinition {
        color_number: 194,
        polygon_group: 1,
        hue1: "7PB",
        hue2: "9PB",
        points: &[
            PolygonPoint { chroma: 11.0, value: 0.0 },
            PolygonPoint { chroma: 11.0, value: 3.0 },
            PolygonPoint { chroma: 13.0, value: 3.0 },
            PolygonPoint { chroma: 13.0, value: 10.0 },
            PolygonPoint { chroma: 50.0, value: 10.0 },
            PolygonPoint { chroma: 50.0, value: 0.0 },
        ],
    },
    // Color 195: polygon 1
    PolygonDefinition {
        color_number: 195,
        polygon_group: 1,
        hue1: "7PB",
        hue2: "9PB",
        points: &[
            PolygonPoint { chroma: 9.0, value: 4.5 },
            PolygonPoint { chroma: 9.0, value: 10.0 },
            PolygonPoint { chroma: 13.0, value: 10.0 },
            PolygonPoint { chroma: 13.0, value: 5.5 },
            PolygonPoint { chroma: 11.0, value: 5.5 },
            PolygonPoint { chroma: 11.0, value: 4.5 },
        ],
    },
    // Color 196: polygon 1
    PolygonDefinition {
        color_number: 196,
        polygon_group: 1,
        hue1: "7PB",
        hue2: "9PB",
        points: &[
            PolygonPoint { chroma: 9.0, value: 3.0 },
            PolygonPoint { chroma: 9.0, value: 4.5 },
            PolygonPoint { chroma: 11.0, value: 4.5 },
            PolygonPoint { chroma: 11.0, value: 5.5 },
            PolygonPoint { chroma: 13.0, value: 5.5 },
            PolygonPoint { chroma: 13.0, value: 3.0 },
        ],
    },
    // Color 197: polygon 1
    PolygonDefinition {
        color_number: 197,
        polygon_group: 1,
        hue1: "7PB",
        hue2: "9PB",
        points: &[
            PolygonPoint { chroma: 7.0, value: 0.0 },
            PolygonPoint { chroma: 7.0, value: 3.0 },
            PolygonPoint { chroma: 11.0, value: 3.0 },
            PolygonPoint { chroma: 11.0, value: 0.0 },
        ],
    },
    // Color 198: polygon 1
    PolygonDefinition {
        color_number: 198,
        polygon_group: 1,
        hue1: "5PB",
        hue2: "7PB",
        points: &[
            PolygonPoint { chroma: 5.0, value: 7.5 },
            PolygonPoint { chroma: 5.0, value: 10.0 },
            PolygonPoint { chroma: 7.0, value: 10.0 },
            PolygonPoint { chroma: 7.0, value: 7.5 },
        ],
    },
    // Color 198: polygon 2
    PolygonDefinition {
        color_number: 198,
        polygon_group: 2,
        hue1: "7PB",
        hue2: "9PB",
        points: &[
            PolygonPoint { chroma: 5.0, value: 7.5 },
            PolygonPoint { chroma: 5.0, value: 10.0 },
            PolygonPoint { chroma: 9.0, value: 10.0 },
            PolygonPoint { chroma: 9.0, value: 7.5 },
        ],
    },
    // Color 199: polygon 1
    PolygonDefinition {
        color_number: 199,
        polygon_group: 1,
        hue1: "5PB",
        hue2: "7PB",
        points: &[
            PolygonPoint { chroma: 5.0, value: 4.5 },
            PolygonPoint { chroma: 5.0, value: 7.5 },
            PolygonPoint { chroma: 7.0, value: 7.5 },
            PolygonPoint { chroma: 7.0, value: 4.5 },
        ],
    },
    // Color 199: polygon 2
    PolygonDefinition {
        color_number: 199,
        polygon_group: 2,
        hue1: "7PB",
        hue2: "9PB",
        points: &[
            PolygonPoint { chroma: 5.0, value: 4.5 },
            PolygonPoint { chroma: 5.0, value: 7.5 },
            PolygonPoint { chroma: 9.0, value: 7.5 },
            PolygonPoint { chroma: 9.0, value: 4.5 },
        ],
    },
    // Color 200: polygon 1
    PolygonDefinition {
        color_number: 200,
        polygon_group: 1,
        hue1: "7PB",
        hue2: "9PB",
        points: &[
            PolygonPoint { chroma: 5.0, value: 2.0 },
            PolygonPoint { chroma: 5.0, value: 4.5 },
            PolygonPoint { chroma: 9.0, value: 4.5 },
            PolygonPoint { chroma: 9.0, value: 3.0 },
            PolygonPoint { chroma: 7.0, value: 3.0 },
            PolygonPoint { chroma: 7.0, value: 2.0 },
        ],
    },
    // Color 201: polygon 1
    PolygonDefinition {
        color_number: 201,
        polygon_group: 1,
        hue1: "6PB",
        hue2: "7PB",
        points: &[
            PolygonPoint { chroma: 2.0, value: 0.0 },
            PolygonPoint { chroma: 2.0, value: 2.0 },
            PolygonPoint { chroma: 5.0, value: 2.0 },
            PolygonPoint { chroma: 5.0, value: 0.0 },
        ],
    },
    // Color 201: polygon 2
    PolygonDefinition {
        color_number: 201,
        polygon_group: 2,
        hue1: "7PB",
        hue2: "9PB",
        points: &[
            PolygonPoint { chroma: 2.0, value: 0.0 },
            PolygonPoint { chroma: 2.0, value: 2.0 },
            PolygonPoint { chroma: 7.0, value: 2.0 },
            PolygonPoint { chroma: 7.0, value: 0.0 },
        ],
    },
    // Color 202: polygon 1
    PolygonDefinition {
        color_number: 202,
        polygon_group: 1,
        hue1: "5PB",
        hue2: "9PB",
        points: &[
            PolygonPoint { chroma: 3.0, value: 7.5 },
            PolygonPoint { chroma: 3.0, value: 10.0 },
            PolygonPoint { chroma: 5.0, value: 10.0 },
            PolygonPoint { chroma: 5.0, value: 7.5 },
        ],
    },
    // Color 203: polygon 1
    PolygonDefinition {
        color_number: 203,
        polygon_group: 1,
        hue1: "5PB",
        hue2: "9PB",
        points: &[
            PolygonPoint { chroma: 3.0, value: 4.5 },
            PolygonPoint { chroma: 3.0, value: 7.5 },
            PolygonPoint { chroma: 5.0, value: 7.5 },
            PolygonPoint { chroma: 5.0, value: 4.5 },
        ],
    },
    // Color 204: polygon 1
    PolygonDefinition {
        color_number: 204,
        polygon_group: 1,
        hue1: "5PB",
        hue2: "6PB",
        points: &[
            PolygonPoint { chroma: 3.0, value: 3.0 },
            PolygonPoint { chroma: 3.0, value: 4.5 },
            PolygonPoint { chroma: 5.0, value: 4.5 },
            PolygonPoint { chroma: 5.0, value: 3.0 },
        ],
    },
    // Color 204: polygon 2
    PolygonDefinition {
        color_number: 204,
        polygon_group: 2,
        hue1: "6PB",
        hue2: "9PB",
        points: &[
            PolygonPoint { chroma: 2.0, value: 2.0 },
            PolygonPoint { chroma: 2.0, value: 2.5 },
            PolygonPoint { chroma: 3.0, value: 2.5 },
            PolygonPoint { chroma: 3.0, value: 4.5 },
            PolygonPoint { chroma: 5.0, value: 4.5 },
            PolygonPoint { chroma: 5.0, value: 2.0 },
        ],
    },
    // Color 205: polygon 1
    PolygonDefinition {
        color_number: 205,
        polygon_group: 1,
        hue1: "9PB",
        hue2: "3P",
        points: &[
            PolygonPoint { chroma: 13.0, value: 0.0 },
            PolygonPoint { chroma: 13.0, value: 10.0 },
            PolygonPoint { chroma: 50.0, value: 10.0 },
            PolygonPoint { chroma: 50.0, value: 0.0 },
        ],
    },
    // Color 206: polygon 1
    PolygonDefinition {
        color_number: 206,
        polygon_group: 1,
        hue1: "9PB",
        hue2: "3P",
        points: &[
            PolygonPoint { chroma: 9.0, value: 4.5 },
            PolygonPoint { chroma: 9.0, value: 10.0 },
            PolygonPoint { chroma: 13.0, value: 10.0 },
            PolygonPoint { chroma: 13.0, value: 4.5 },
        ],
    },
    // Color 207: polygon 1
    PolygonDefinition {
        color_number: 207,
        polygon_group: 1,
        hue1: "9PB",
        hue2: "3P",
        points: &[
            PolygonPoint { chroma: 9.0, value: 2.5 },
            PolygonPoint { chroma: 9.0, value: 4.5 },
            PolygonPoint { chroma: 13.0, value: 4.5 },
            PolygonPoint { chroma: 13.0, value: 2.5 },
        ],
    },
    // Color 208: polygon 1
    PolygonDefinition {
        color_number: 208,
        polygon_group: 1,
        hue1: "9PB",
        hue2: "3P",
        points: &[
            PolygonPoint { chroma: 7.0, value: 0.0 },
            PolygonPoint { chroma: 7.0, value: 2.5 },
            PolygonPoint { chroma: 13.0, value: 2.5 },
            PolygonPoint { chroma: 13.0, value: 0.0 },
        ],
    },
    // Color 209: polygon 1
    PolygonDefinition {
        color_number: 209,
        polygon_group: 1,
        hue1: "9PB",
        hue2: "3P",
        points: &[
            PolygonPoint { chroma: 5.0, value: 7.5 },
            PolygonPoint { chroma: 5.0, value: 10.0 },
            PolygonPoint { chroma: 9.0, value: 10.0 },
            PolygonPoint { chroma: 9.0, value: 7.5 },
        ],
    },
    // Color 210: polygon 1
    PolygonDefinition {
        color_number: 210,
        polygon_group: 1,
        hue1: "9PB",
        hue2: "3P",
        points: &[
            PolygonPoint { chroma: 5.0, value: 4.5 },
            PolygonPoint { chroma: 5.0, value: 7.5 },
            PolygonPoint { chroma: 9.0, value: 7.5 },
            PolygonPoint { chroma: 9.0, value: 4.5 },
        ],
    },
    // Color 211: polygon 1
    PolygonDefinition {
        color_number: 211,
        polygon_group: 1,
        hue1: "9PB",
        hue2: "3P",
        points: &[
            PolygonPoint { chroma: 5.0, value: 2.5 },
            PolygonPoint { chroma: 5.0, value: 4.5 },
            PolygonPoint { chroma: 9.0, value: 4.5 },
            PolygonPoint { chroma: 9.0, value: 2.5 },
        ],
    },
    // Color 212: polygon 1
    PolygonDefinition {
        color_number: 212,
        polygon_group: 1,
        hue1: "9PB",
        hue2: "3P",
        points: &[
            PolygonPoint { chroma: 2.0, value: 0.0 },
            PolygonPoint { chroma: 2.0, value: 2.5 },
            PolygonPoint { chroma: 7.0, value: 2.5 },
            PolygonPoint { chroma: 7.0, value: 0.0 },
        ],
    },
    // Color 213: polygon 1
    PolygonDefinition {
        color_number: 213,
        polygon_group: 1,
        hue1: "9PB",
        hue2: "3P",
        points: &[
            PolygonPoint { chroma: 3.0, value: 7.5 },
            PolygonPoint { chroma: 3.0, value: 10.0 },
            PolygonPoint { chroma: 5.0, value: 10.0 },
            PolygonPoint { chroma: 5.0, value: 7.5 },
        ],
    },
    // Color 214: polygon 1
    PolygonDefinition {
        color_number: 214,
        polygon_group: 1,
        hue1: "9PB",
        hue2: "3P",
        points: &[
            PolygonPoint { chroma: 3.0, value: 4.5 },
            PolygonPoint { chroma: 3.0, value: 7.5 },
            PolygonPoint { chroma: 5.0, value: 7.5 },
            PolygonPoint { chroma: 5.0, value: 4.5 },
        ],
    },
    // Color 215: polygon 1
    PolygonDefinition {
        color_number: 215,
        polygon_group: 1,
        hue1: "9PB",
        hue2: "3P",
        points: &[
            PolygonPoint { chroma: 3.0, value: 2.5 },
            PolygonPoint { chroma: 3.0, value: 4.5 },
            PolygonPoint { chroma: 5.0, value: 4.5 },
            PolygonPoint { chroma: 5.0, value: 2.5 },
        ],
    },
    // Color 216: polygon 1
    PolygonDefinition {
        color_number: 216,
        polygon_group: 1,
        hue1: "3P",
        hue2: "9P",
        points: &[
            PolygonPoint { chroma: 13.0, value: 0.0 },
            PolygonPoint { chroma: 13.0, value: 10.0 },
            PolygonPoint { chroma: 50.0, value: 10.0 },
            PolygonPoint { chroma: 50.0, value: 0.0 },
        ],
    },
    // Color 217: polygon 1
    PolygonDefinition {
        color_number: 217,
        polygon_group: 1,
        hue1: "3P",
        hue2: "9P",
        points: &[
            PolygonPoint { chroma: 9.0, value: 5.5 },
            PolygonPoint { chroma: 9.0, value: 10.0 },
            PolygonPoint { chroma: 13.0, value: 10.0 },
            PolygonPoint { chroma: 13.0, value: 5.5 },
        ],
    },
    // Color 218: polygon 1
    PolygonDefinition {
        color_number: 218,
        polygon_group: 1,
        hue1: "3P",
        hue2: "9P",
        points: &[
            PolygonPoint { chroma: 9.0, value: 3.5 },
            PolygonPoint { chroma: 9.0, value: 5.5 },
            PolygonPoint { chroma: 13.0, value: 5.5 },
            PolygonPoint { chroma: 13.0, value: 3.5 },
        ],
    },
    // Color 219: polygon 1
    PolygonDefinition {
        color_number: 219,
        polygon_group: 1,
        hue1: "3P",
        hue2: "9P",
        points: &[
            PolygonPoint { chroma: 7.0, value: 2.0 },
            PolygonPoint { chroma: 7.0, value: 3.5 },
            PolygonPoint { chroma: 13.0, value: 3.5 },
            PolygonPoint { chroma: 13.0, value: 2.0 },
        ],
    },
    // Color 220: polygon 1
    PolygonDefinition {
        color_number: 220,
        polygon_group: 1,
        hue1: "3P",
        hue2: "9P",
        points: &[
            PolygonPoint { chroma: 7.0, value: 0.0 },
            PolygonPoint { chroma: 7.0, value: 2.0 },
            PolygonPoint { chroma: 13.0, value: 2.0 },
            PolygonPoint { chroma: 13.0, value: 0.0 },
        ],
    },
    // Color 221: polygon 1
    PolygonDefinition {
        color_number: 221,
        polygon_group: 1,
        hue1: "3P",
        hue2: "9P",
        points: &[
            PolygonPoint { chroma: 5.0, value: 7.5 },
            PolygonPoint { chroma: 5.0, value: 10.0 },
            PolygonPoint { chroma: 9.0, value: 10.0 },
            PolygonPoint { chroma: 9.0, value: 7.5 },
        ],
    },
    // Color 222: polygon 1
    PolygonDefinition {
        color_number: 222,
        polygon_group: 1,
        hue1: "3P",
        hue2: "9P",
        points: &[
            PolygonPoint { chroma: 5.0, value: 5.5 },
            PolygonPoint { chroma: 5.0, value: 7.5 },
            PolygonPoint { chroma: 9.0, value: 7.5 },
            PolygonPoint { chroma: 9.0, value: 5.5 },
        ],
    },
    // Color 223: polygon 1
    PolygonDefinition {
        color_number: 223,
        polygon_group: 1,
        hue1: "3P",
        hue2: "9P",
        points: &[
            PolygonPoint { chroma: 5.0, value: 3.5 },
            PolygonPoint { chroma: 5.0, value: 5.5 },
            PolygonPoint { chroma: 9.0, value: 5.5 },
            PolygonPoint { chroma: 9.0, value: 3.5 },
        ],
    },
    // Color 224: polygon 1
    PolygonDefinition {
        color_number: 224,
        polygon_group: 1,
        hue1: "3P",
        hue2: "9P",
        points: &[
            PolygonPoint { chroma: 2.0, value: 2.0 },
            PolygonPoint { chroma: 2.0, value: 2.5 },
            PolygonPoint { chroma: 3.0, value: 2.5 },
            PolygonPoint { chroma: 3.0, value: 3.5 },
            PolygonPoint { chroma: 7.0, value: 3.5 },
            PolygonPoint { chroma: 7.0, value: 2.0 },
        ],
    },
    // Color 225: polygon 1
    PolygonDefinition {
        color_number: 225,
        polygon_group: 1,
        hue1: "3P",
        hue2: "9P",
        points: &[
            PolygonPoint { chroma: 2.0, value: 0.0 },
            PolygonPoint { chroma: 2.0, value: 2.0 },
            PolygonPoint { chroma: 7.0, value: 2.0 },
            PolygonPoint { chroma: 7.0, value: 0.0 },
        ],
    },
    // Color 226: polygon 1
    PolygonDefinition {
        color_number: 226,
        polygon_group: 1,
        hue1: "9PB",
        hue2: "3P",
        points: &[
            PolygonPoint { chroma: 1.5, value: 7.5 },
            PolygonPoint { chroma: 1.5, value: 10.0 },
            PolygonPoint { chroma: 3.0, value: 10.0 },
            PolygonPoint { chroma: 3.0, value: 7.5 },
        ],
    },
    // Color 226: polygon 2
    PolygonDefinition {
        color_number: 226,
        polygon_group: 2,
        hue1: "3P",
        hue2: "9P",
        points: &[
            PolygonPoint { chroma: 1.5, value: 7.5 },
            PolygonPoint { chroma: 1.5, value: 10.0 },
            PolygonPoint { chroma: 5.0, value: 10.0 },
            PolygonPoint { chroma: 5.0, value: 7.5 },
        ],
    },
    // Color 227: polygon 1
    PolygonDefinition {
        color_number: 227,
        polygon_group: 1,
        hue1: "9PB",
        hue2: "3P",
        points: &[
            PolygonPoint { chroma: 1.5, value: 5.5 },
            PolygonPoint { chroma: 1.5, value: 7.5 },
            PolygonPoint { chroma: 3.0, value: 7.5 },
            PolygonPoint { chroma: 3.0, value: 5.5 },
        ],
    },
    // Color 227: polygon 2
    PolygonDefinition {
        color_number: 227,
        polygon_group: 2,
        hue1: "3P",
        hue2: "9P",
        points: &[
            PolygonPoint { chroma: 1.5, value: 5.5 },
            PolygonPoint { chroma: 1.5, value: 7.5 },
            PolygonPoint { chroma: 5.0, value: 7.5 },
            PolygonPoint { chroma: 5.0, value: 5.5 },
        ],
    },
    // Color 227: polygon 3
    PolygonDefinition {
        color_number: 227,
        polygon_group: 3,
        hue1: "9P",
        hue2: "1R",
        points: &[
            PolygonPoint { chroma: 1.5, value: 5.5 },
            PolygonPoint { chroma: 1.5, value: 6.5 },
            PolygonPoint { chroma: 3.0, value: 6.5 },
            PolygonPoint { chroma: 3.0, value: 5.5 },
        ],
    },
    // Color 228: polygon 1
    PolygonDefinition {
        color_number: 228,
        polygon_group: 1,
        hue1: "9PB",
        hue2: "3P",
        points: &[
            PolygonPoint { chroma: 1.5, value: 3.5 },
            PolygonPoint { chroma: 1.5, value: 5.5 },
            PolygonPoint { chroma: 3.0, value: 5.5 },
            PolygonPoint { chroma: 3.0, value: 3.5 },
        ],
    },
    // Color 228: polygon 2
    PolygonDefinition {
        color_number: 228,
        polygon_group: 2,
        hue1: "3P",
        hue2: "9P",
        points: &[
            PolygonPoint { chroma: 1.5, value: 3.5 },
            PolygonPoint { chroma: 1.5, value: 5.5 },
            PolygonPoint { chroma: 5.0, value: 5.5 },
            PolygonPoint { chroma: 5.0, value: 3.5 },
        ],
    },
    // Color 228: polygon 3
    PolygonDefinition {
        color_number: 228,
        polygon_group: 3,
        hue1: "9P",
        hue2: "1R",
        points: &[
            PolygonPoint { chroma: 1.5, value: 3.5 },
            PolygonPoint { chroma: 1.5, value: 5.5 },
            PolygonPoint { chroma: 3.0, value: 5.5 },
            PolygonPoint { chroma: 3.0, value: 3.5 },
        ],
    },
    // Color 229: polygon 1
    PolygonDefinition {
        color_number: 229,
        polygon_group: 1,
        hue1: "9PB",
        hue2: "1R",
        points: &[
            PolygonPoint { chroma: 0.5, value: 2.0 },
            PolygonPoint { chroma: 0.5, value: 2.5 },
            PolygonPoint { chroma: 1.5, value: 2.5 },
            PolygonPoint { chroma: 1.5, value: 3.5 },
            PolygonPoint { chroma: 3.0, value: 3.5 },
            PolygonPoint { chroma: 3.0, value: 2.5 },
            PolygonPoint { chroma: 2.0, value: 2.5 },
            PolygonPoint { chroma: 2.0, value: 2.0 },
        ],
    },
    // Color 230: polygon 1
    PolygonDefinition {
        color_number: 230,
        polygon_group: 1,
        hue1: "9PB",
        hue2: "1R",
        points: &[
            PolygonPoint { chroma: 1.0, value: 0.0 },
            PolygonPoint { chroma: 1.0, value: 2.0 },
            PolygonPoint { chroma: 2.0, value: 2.0 },
            PolygonPoint { chroma: 2.0, value: 0.0 },
        ],
    },
    // Color 231: polygon 1
    PolygonDefinition {
        color_number: 231,
        polygon_group: 1,
        hue1: "9PB",
        hue2: "9RP",
        points: &[
            PolygonPoint { chroma: 0.5, value: 8.5 },
            PolygonPoint { chroma: 0.5, value: 10.0 },
            PolygonPoint { chroma: 1.5, value: 10.0 },
            PolygonPoint { chroma: 1.5, value: 8.5 },
        ],
    },
    // Color 232: polygon 1
    PolygonDefinition {
        color_number: 232,
        polygon_group: 1,
        hue1: "9PB",
        hue2: "9RP",
        points: &[
            PolygonPoint { chroma: 0.5, value: 6.5 },
            PolygonPoint { chroma: 0.5, value: 8.5 },
            PolygonPoint { chroma: 1.5, value: 8.5 },
            PolygonPoint { chroma: 1.5, value: 6.5 },
        ],
    },
    // Color 233: polygon 1
    PolygonDefinition {
        color_number: 233,
        polygon_group: 1,
        hue1: "9PB",
        hue2: "1R",
        points: &[
            PolygonPoint { chroma: 0.5, value: 4.5 },
            PolygonPoint { chroma: 0.5, value: 6.5 },
            PolygonPoint { chroma: 1.5, value: 6.5 },
            PolygonPoint { chroma: 1.5, value: 4.5 },
        ],
    },
    // Color 234: polygon 1
    PolygonDefinition {
        color_number: 234,
        polygon_group: 1,
        hue1: "9PB",
        hue2: "1R",
        points: &[
            PolygonPoint { chroma: 0.5, value: 2.5 },
            PolygonPoint { chroma: 0.5, value: 4.5 },
            PolygonPoint { chroma: 1.5, value: 4.5 },
            PolygonPoint { chroma: 1.5, value: 2.5 },
        ],
    },
    // Color 235: polygon 1
    PolygonDefinition {
        color_number: 235,
        polygon_group: 1,
        hue1: "9PB",
        hue2: "1R",
        points: &[
            PolygonPoint { chroma: 0.5, value: 0.0 },
            PolygonPoint { chroma: 0.5, value: 2.0 },
            PolygonPoint { chroma: 1.0, value: 2.0 },
            PolygonPoint { chroma: 1.0, value: 0.0 },
        ],
    },
    // Color 236: polygon 1
    PolygonDefinition {
        color_number: 236,
        polygon_group: 1,
        hue1: "9P",
        hue2: "3RP",
        points: &[
            PolygonPoint { chroma: 13.0, value: 0.0 },
            PolygonPoint { chroma: 13.0, value: 5.5 },
            PolygonPoint { chroma: 15.0, value: 5.5 },
            PolygonPoint { chroma: 15.0, value: 6.5 },
            PolygonPoint { chroma: 50.0, value: 6.5 },
            PolygonPoint { chroma: 50.0, value: 0.0 },
        ],
    },
    // Color 237: polygon 1
    PolygonDefinition {
        color_number: 237,
        polygon_group: 1,
        hue1: "9P",
        hue2: "3RP",
        points: &[
            PolygonPoint { chroma: 9.0, value: 3.5 },
            PolygonPoint { chroma: 9.0, value: 5.5 },
            PolygonPoint { chroma: 13.0, value: 5.5 },
            PolygonPoint { chroma: 13.0, value: 3.5 },
        ],
    },
    // Color 238: polygon 1
    PolygonDefinition {
        color_number: 238,
        polygon_group: 1,
        hue1: "9P",
        hue2: "3RP",
        points: &[
            PolygonPoint { chroma: 7.0, value: 2.0 },
            PolygonPoint { chroma: 7.0, value: 3.5 },
            PolygonPoint { chroma: 13.0, value: 3.5 },
            PolygonPoint { chroma: 13.0, value: 2.0 },
        ],
    },
    // Color 239: polygon 1
    PolygonDefinition {
        color_number: 239,
        polygon_group: 1,
        hue1: "9P",
        hue2: "3RP",
        points: &[
            PolygonPoint { chroma: 7.0, value: 0.0 },
            PolygonPoint { chroma: 7.0, value: 2.0 },
            PolygonPoint { chroma: 13.0, value: 2.0 },
            PolygonPoint { chroma: 13.0, value: 0.0 },
        ],
    },
    // Color 240: polygon 1
    PolygonDefinition {
        color_number: 240,
        polygon_group: 1,
        hue1: "9P",
        hue2: "3RP",
        points: &[
            PolygonPoint { chroma: 5.0, value: 5.5 },
            PolygonPoint { chroma: 5.0, value: 6.5 },
            PolygonPoint { chroma: 9.0, value: 6.5 },
            PolygonPoint { chroma: 9.0, value: 5.5 },
        ],
    },
    // Color 241: polygon 1
    PolygonDefinition {
        color_number: 241,
        polygon_group: 1,
        hue1: "9P",
        hue2: "3RP",
        points: &[
            PolygonPoint { chroma: 5.0, value: 3.5 },
            PolygonPoint { chroma: 5.0, value: 5.5 },
            PolygonPoint { chroma: 9.0, value: 5.5 },
            PolygonPoint { chroma: 9.0, value: 3.5 },
        ],
    },
    // Color 242: polygon 1
    PolygonDefinition {
        color_number: 242,
        polygon_group: 1,
        hue1: "9P",
        hue2: "3RP",
        points: &[
            PolygonPoint { chroma: 2.0, value: 2.0 },
            PolygonPoint { chroma: 2.0, value: 2.5 },
            PolygonPoint { chroma: 3.0, value: 2.5 },
            PolygonPoint { chroma: 3.0, value: 3.5 },
            PolygonPoint { chroma: 7.0, value: 3.5 },
            PolygonPoint { chroma: 7.0, value: 2.0 },
        ],
    },
    // Color 243: polygon 1
    PolygonDefinition {
        color_number: 243,
        polygon_group: 1,
        hue1: "9P",
        hue2: "3RP",
        points: &[
            PolygonPoint { chroma: 2.0, value: 0.0 },
            PolygonPoint { chroma: 2.0, value: 2.0 },
            PolygonPoint { chroma: 7.0, value: 2.0 },
            PolygonPoint { chroma: 7.0, value: 0.0 },
        ],
    },
    // Color 244: polygon 1
    PolygonDefinition {
        color_number: 244,
        polygon_group: 1,
        hue1: "9P",
        hue2: "3RP",
        points: &[
            PolygonPoint { chroma: 3.0, value: 5.5 },
            PolygonPoint { chroma: 3.0, value: 6.5 },
            PolygonPoint { chroma: 5.0, value: 6.5 },
            PolygonPoint { chroma: 5.0, value: 5.5 },
        ],
    },
    // Color 245: polygon 1
    PolygonDefinition {
        color_number: 245,
        polygon_group: 1,
        hue1: "9P",
        hue2: "3RP",
        points: &[
            PolygonPoint { chroma: 3.0, value: 3.5 },
            PolygonPoint { chroma: 3.0, value: 5.5 },
            PolygonPoint { chroma: 5.0, value: 5.5 },
            PolygonPoint { chroma: 5.0, value: 3.5 },
        ],
    },
    // Color 246: polygon 1
    PolygonDefinition {
        color_number: 246,
        polygon_group: 1,
        hue1: "9P",
        hue2: "9RP",
        points: &[
            PolygonPoint { chroma: 9.0, value: 7.5 },
            PolygonPoint { chroma: 9.0, value: 10.0 },
            PolygonPoint { chroma: 50.0, value: 10.0 },
            PolygonPoint { chroma: 50.0, value: 7.5 },
        ],
    },
    // Color 247: polygon 1
    PolygonDefinition {
        color_number: 247,
        polygon_group: 1,
        hue1: "9P",
        hue2: "9RP",
        points: &[
            PolygonPoint { chroma: 9.0, value: 6.5 },
            PolygonPoint { chroma: 9.0, value: 7.5 },
            PolygonPoint { chroma: 50.0, value: 7.5 },
            PolygonPoint { chroma: 50.0, value: 6.5 },
        ],
    },
    // Color 248: polygon 1
    PolygonDefinition {
        color_number: 248,
        polygon_group: 1,
        hue1: "9P",
        hue2: "9RP",
        points: &[
            PolygonPoint { chroma: 9.0, value: 5.5 },
            PolygonPoint { chroma: 9.0, value: 6.5 },
            PolygonPoint { chroma: 15.0, value: 6.5 },
            PolygonPoint { chroma: 15.0, value: 5.5 },
        ],
    },
    // Color 249: polygon 1
    PolygonDefinition {
        color_number: 249,
        polygon_group: 1,
        hue1: "9P",
        hue2: "9RP",
        points: &[
            PolygonPoint { chroma: 5.0, value: 7.5 },
            PolygonPoint { chroma: 5.0, value: 10.0 },
            PolygonPoint { chroma: 9.0, value: 10.0 },
            PolygonPoint { chroma: 9.0, value: 7.5 },
        ],
    },
    // Color 250: polygon 1
    PolygonDefinition {
        color_number: 250,
        polygon_group: 1,
        hue1: "9P",
        hue2: "9RP",
        points: &[
            PolygonPoint { chroma: 5.0, value: 6.5 },
            PolygonPoint { chroma: 5.0, value: 7.5 },
            PolygonPoint { chroma: 9.0, value: 7.5 },
            PolygonPoint { chroma: 9.0, value: 6.5 },
        ],
    },
    // Color 251: polygon 1
    PolygonDefinition {
        color_number: 251,
        polygon_group: 1,
        hue1: "3RP",
        hue2: "9RP",
        points: &[
            PolygonPoint { chroma: 5.0, value: 5.5 },
            PolygonPoint { chroma: 5.0, value: 6.5 },
            PolygonPoint { chroma: 9.0, value: 6.5 },
            PolygonPoint { chroma: 9.0, value: 5.5 },
        ],
    },
    // Color 252: polygon 1
    PolygonDefinition {
        color_number: 252,
        polygon_group: 1,
        hue1: "9P",
        hue2: "9RP",
        points: &[
            PolygonPoint { chroma: 1.5, value: 7.5 },
            PolygonPoint { chroma: 1.5, value: 10.0 },
            PolygonPoint { chroma: 5.0, value: 10.0 },
            PolygonPoint { chroma: 5.0, value: 7.5 },
        ],
    },
    // Color 253: polygon 1
    PolygonDefinition {
        color_number: 253,
        polygon_group: 1,
        hue1: "9P",
        hue2: "9RP",
        points: &[
            PolygonPoint { chroma: 1.5, value: 6.5 },
            PolygonPoint { chroma: 1.5, value: 7.5 },
            PolygonPoint { chroma: 5.0, value: 7.5 },
            PolygonPoint { chroma: 5.0, value: 6.5 },
        ],
    },
    // Color 254: polygon 1
    PolygonDefinition {
        color_number: 254,
        polygon_group: 1,
        hue1: "3RP",
        hue2: "1R",
        points: &[
            PolygonPoint { chroma: 11.0, value: 0.0 },
            PolygonPoint { chroma: 11.0, value: 2.0 },
            PolygonPoint { chroma: 13.0, value: 2.0 },
            PolygonPoint { chroma: 13.0, value: 5.5 },
            PolygonPoint { chroma: 15.0, value: 5.5 },
            PolygonPoint { chroma: 15.0, value: 6.5 },
            PolygonPoint { chroma: 50.0, value: 6.5 },
            PolygonPoint { chroma: 50.0, value: 0.0 },
        ],
    },
    // Color 255: polygon 1
    PolygonDefinition {
        color_number: 255,
        polygon_group: 1,
        hue1: "3RP",
        hue2: "1R",
        points: &[
            PolygonPoint { chroma: 11.0, value: 3.5 },
            PolygonPoint { chroma: 11.0, value: 5.5 },
            PolygonPoint { chroma: 13.0, value: 5.5 },
            PolygonPoint { chroma: 13.0, value: 3.5 },
        ],
    },
    // Color 256: polygon 1
    PolygonDefinition {
        color_number: 256,
        polygon_group: 1,
        hue1: "3RP",
        hue2: "1R",
        points: &[
            PolygonPoint { chroma: 9.0, value: 2.0 },
            PolygonPoint { chroma: 9.0, value: 3.5 },
            PolygonPoint { chroma: 13.0, value: 3.5 },
            PolygonPoint { chroma: 13.0, value: 2.0 },
        ],
    },
    // Color 257: polygon 1
    PolygonDefinition {
        color_number: 257,
        polygon_group: 1,
        hue1: "3RP",
        hue2: "1R",
        points: &[
            PolygonPoint { chroma: 7.0, value: 0.0 },
            PolygonPoint { chroma: 7.0, value: 2.0 },
            PolygonPoint { chroma: 11.0, value: 2.0 },
            PolygonPoint { chroma: 11.0, value: 0.0 },
        ],
    },
    // Color 258: polygon 1
    PolygonDefinition {
        color_number: 258,
        polygon_group: 1,
        hue1: "3RP",
        hue2: "1R",
        points: &[
            PolygonPoint { chroma: 7.0, value: 3.5 },
            PolygonPoint { chroma: 7.0, value: 5.5 },
            PolygonPoint { chroma: 11.0, value: 5.5 },
            PolygonPoint { chroma: 11.0, value: 3.5 },
        ],
    },
    // Color 259: polygon 1
    PolygonDefinition {
        color_number: 259,
        polygon_group: 1,
        hue1: "3RP",
        hue2: "1R",
        points: &[
            PolygonPoint { chroma: 2.0, value: 2.0 },
            PolygonPoint { chroma: 2.0, value: 2.5 },
            PolygonPoint { chroma: 3.0, value: 2.5 },
            PolygonPoint { chroma: 3.0, value: 3.5 },
            PolygonPoint { chroma: 9.0, value: 3.5 },
            PolygonPoint { chroma: 9.0, value: 2.0 },
        ],
    },
    // Color 260: polygon 1
    PolygonDefinition {
        color_number: 260,
        polygon_group: 1,
        hue1: "3RP",
        hue2: "1R",
        points: &[
            PolygonPoint { chroma: 2.0, value: 0.0 },
            PolygonPoint { chroma: 2.0, value: 2.0 },
            PolygonPoint { chroma: 7.0, value: 2.0 },
            PolygonPoint { chroma: 7.0, value: 0.0 },
        ],
    },
    // Color 261: polygon 1
    PolygonDefinition {
        color_number: 261,
        polygon_group: 1,
        hue1: "3RP",
        hue2: "1R",
        points: &[
            PolygonPoint { chroma: 3.0, value: 5.5 },
            PolygonPoint { chroma: 3.0, value: 6.5 },
            PolygonPoint { chroma: 5.0, value: 6.5 },
            PolygonPoint { chroma: 5.0, value: 5.5 },
        ],
    },
    // Color 262: polygon 1
    PolygonDefinition {
        color_number: 262,
        polygon_group: 1,
        hue1: "3RP",
        hue2: "1R",
        points: &[
            PolygonPoint { chroma: 3.0, value: 3.5 },
            PolygonPoint { chroma: 3.0, value: 5.5 },
            PolygonPoint { chroma: 7.0, value: 5.5 },
            PolygonPoint { chroma: 7.0, value: 3.5 },
        ],
    },
    // Color 263: polygon 1
    PolygonDefinition {
        color_number: 263,
        polygon_group: 1,
        hue1: "1R",
        hue2: "7YR",
        points: &[
            PolygonPoint { chroma: 0.0, value: 8.5 },
            PolygonPoint { chroma: 0.0, value: 10.0 },
            PolygonPoint { chroma: 0.5, value: 10.0 },
            PolygonPoint { chroma: 0.5, value: 8.5 },
        ],
    },
    // Color 263: polygon 2
    PolygonDefinition {
        color_number: 263,
        polygon_group: 2,
        hue1: "7YR",
        hue2: "9Y",
        points: &[
            PolygonPoint { chroma: 0.0, value: 8.5 },
            PolygonPoint { chroma: 0.0, value: 10.0 },
            PolygonPoint { chroma: 0.7, value: 10.0 },
            PolygonPoint { chroma: 0.7, value: 8.5 },
        ],
    },
    // Color 263: polygon 3
    PolygonDefinition {
        color_number: 263,
        polygon_group: 3,
        hue1: "9Y",
        hue2: "1R",
        points: &[
            PolygonPoint { chroma: 0.0, value: 8.5 },
            PolygonPoint { chroma: 0.0, value: 10.0 },
            PolygonPoint { chroma: 0.5, value: 10.0 },
            PolygonPoint { chroma: 0.5, value: 8.5 },
        ],
    },
    // Color 264: polygon 1
    PolygonDefinition {
        color_number: 264,
        polygon_group: 1,
        hue1: "1R",
        hue2: "7YR",
        points: &[
            PolygonPoint { chroma: 0.0, value: 6.5 },
            PolygonPoint { chroma: 0.0, value: 8.5 },
            PolygonPoint { chroma: 0.5, value: 8.5 },
            PolygonPoint { chroma: 0.5, value: 6.5 },
        ],
    },
    // Color 264: polygon 2
    PolygonDefinition {
        color_number: 264,
        polygon_group: 2,
        hue1: "7YR",
        hue2: "9Y",
        points: &[
            PolygonPoint { chroma: 0.0, value: 6.5 },
            PolygonPoint { chroma: 0.0, value: 8.5 },
            PolygonPoint { chroma: 0.7, value: 8.5 },
            PolygonPoint { chroma: 0.7, value: 6.5 },
        ],
    },
    // Color 264: polygon 3
    PolygonDefinition {
        color_number: 264,
        polygon_group: 3,
        hue1: "9Y",
        hue2: "1R",
        points: &[
            PolygonPoint { chroma: 0.0, value: 6.5 },
            PolygonPoint { chroma: 0.0, value: 8.5 },
            PolygonPoint { chroma: 0.5, value: 8.5 },
            PolygonPoint { chroma: 0.5, value: 6.5 },
        ],
    },
    // Color 265: polygon 1
    PolygonDefinition {
        color_number: 265,
        polygon_group: 1,
        hue1: "1R",
        hue2: "7YR",
        points: &[
            PolygonPoint { chroma: 0.0, value: 4.5 },
            PolygonPoint { chroma: 0.0, value: 6.5 },
            PolygonPoint { chroma: 0.5, value: 6.5 },
            PolygonPoint { chroma: 0.5, value: 4.5 },
        ],
    },
    // Color 265: polygon 2
    PolygonDefinition {
        color_number: 265,
        polygon_group: 2,
        hue1: "7YR",
        hue2: "9Y",
        points: &[
            PolygonPoint { chroma: 0.0, value: 4.5 },
            PolygonPoint { chroma: 0.0, value: 6.5 },
            PolygonPoint { chroma: 0.7, value: 6.5 },
            PolygonPoint { chroma: 0.7, value: 4.5 },
        ],
    },
    // Color 265: polygon 3
    PolygonDefinition {
        color_number: 265,
        polygon_group: 3,
        hue1: "9Y",
        hue2: "1R",
        points: &[
            PolygonPoint { chroma: 0.0, value: 4.5 },
            PolygonPoint { chroma: 0.0, value: 6.5 },
            PolygonPoint { chroma: 0.5, value: 6.5 },
            PolygonPoint { chroma: 0.5, value: 4.5 },
        ],
    },
    // Color 266: polygon 1
    PolygonDefinition {
        color_number: 266,
        polygon_group: 1,
        hue1: "1R",
        hue2: "7YR",
        points: &[
            PolygonPoint { chroma: 0.0, value: 2.5 },
            PolygonPoint { chroma: 0.0, value: 4.5 },
            PolygonPoint { chroma: 0.5, value: 4.5 },
            PolygonPoint { chroma: 0.5, value: 2.5 },
        ],
    },
    // Color 266: polygon 2
    PolygonDefinition {
        color_number: 266,
        polygon_group: 2,
        hue1: "7YR",
        hue2: "9Y",
        points: &[
            PolygonPoint { chroma: 0.0, value: 2.5 },
            PolygonPoint { chroma: 0.0, value: 4.5 },
            PolygonPoint { chroma: 0.5, value: 4.5 },
            PolygonPoint { chroma: 0.5, value: 2.5 },
        ],
    },
    // Color 266: polygon 3
    PolygonDefinition {
        color_number: 266,
        polygon_group: 3,
        hue1: "9Y",
        hue2: "1R",
        points: &[
            PolygonPoint { chroma: 0.0, value: 2.5 },
            PolygonPoint { chroma: 0.0, value: 4.5 },
            PolygonPoint { chroma: 0.5, value: 4.5 },
            PolygonPoint { chroma: 0.5, value: 2.5 },
        ],
    },
    // Color 267: polygon 1
    PolygonDefinition {
        color_number: 267,
        polygon_group: 1,
        hue1: "1R",
        hue2: "7YR",
        points: &[
            PolygonPoint { chroma: 0.0, value: 0.0 },
            PolygonPoint { chroma: 0.0, value: 2.5 },
            PolygonPoint { chroma: 0.5, value: 2.5 },
            PolygonPoint { chroma: 0.5, value: 0.0 },
        ],
    },
    // Color 267: polygon 2
    PolygonDefinition {
        color_number: 267,
        polygon_group: 2,
        hue1: "7YR",
        hue2: "9Y",
        points: &[
            PolygonPoint { chroma: 0.0, value: 0.0 },
            PolygonPoint { chroma: 0.0, value: 2.5 },
            PolygonPoint { chroma: 0.5, value: 2.5 },
            PolygonPoint { chroma: 0.5, value: 0.0 },
        ],
    },
    // Color 267: polygon 3
    PolygonDefinition {
        color_number: 267,
        polygon_group: 3,
        hue1: "9Y",
        hue2: "1R",
        points: &[
            PolygonPoint { chroma: 0.0, value: 0.0 },
            PolygonPoint { chroma: 0.0, value: 2.5 },
            PolygonPoint { chroma: 0.5, value: 2.5 },
            PolygonPoint { chroma: 0.5, value: 0.0 },
        ],
    },
];

/// Get all polygon definitions (for backward compatibility with CSV loading approach)
pub fn get_polygon_definitions() -> &'static [PolygonDefinition] {
    POLYGON_DEFINITIONS
}