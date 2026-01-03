//! ISCC-NBS color constants and metadata
//! 
//! This module contains embedded ISCC-NBS color metadata, eliminating the need
//! for runtime CSV loading. Data converted from assets/iscc-nbs/ISCC-NBS-Colors.csv.

use std::collections::HashMap;

/// ISCC-NBS color metadata entry
#[derive(Debug, Clone, PartialEq)]
pub struct IsccNbsColorEntry {
    /// Color number from ISCC-NBS standard
    pub color_number: u16,
    /// ISCC-NBS color name (e.g., "pink")
    pub iscc_nbs_color_name: &'static str,
    /// Formatter template (e.g., "vivid {0}")
    pub iscc_nbs_formatter: Option<&'static str>,
    /// Alternative color name (e.g., "pink")
    pub alt_color_name: &'static str,
    /// Color shade category
    pub color_shade: &'static str,
}

/// Embedded ISCC-NBS color data - converted from CSV
pub const ISCC_NBS_COLORS: &[IsccNbsColorEntry] = &[
    IsccNbsColorEntry { color_number: 1, iscc_nbs_color_name: "pink", iscc_nbs_formatter: Some("vivid {0}"), alt_color_name: "pink", color_shade: "pink" },
    IsccNbsColorEntry { color_number: 2, iscc_nbs_color_name: "pink", iscc_nbs_formatter: Some("strong {0}"), alt_color_name: "pink", color_shade: "pink" },
    IsccNbsColorEntry { color_number: 3, iscc_nbs_color_name: "pink", iscc_nbs_formatter: Some("deep {0}"), alt_color_name: "pink", color_shade: "pink" },
    IsccNbsColorEntry { color_number: 4, iscc_nbs_color_name: "pink", iscc_nbs_formatter: Some("light {0}"), alt_color_name: "pink", color_shade: "pink" },
    IsccNbsColorEntry { color_number: 5, iscc_nbs_color_name: "pink", iscc_nbs_formatter: Some("moderate {0}"), alt_color_name: "pink", color_shade: "pink" },
    IsccNbsColorEntry { color_number: 6, iscc_nbs_color_name: "pink", iscc_nbs_formatter: Some("dark {0}"), alt_color_name: "pink", color_shade: "pink" },
    IsccNbsColorEntry { color_number: 7, iscc_nbs_color_name: "pink", iscc_nbs_formatter: Some("pale {0}"), alt_color_name: "pink", color_shade: "pink" },
    IsccNbsColorEntry { color_number: 8, iscc_nbs_color_name: "pink", iscc_nbs_formatter: Some("grayish {0}"), alt_color_name: "pink", color_shade: "pink" },
    IsccNbsColorEntry { color_number: 9, iscc_nbs_color_name: "pink", iscc_nbs_formatter: Some("{1} white"), alt_color_name: "pink", color_shade: "pink" },
    IsccNbsColorEntry { color_number: 10, iscc_nbs_color_name: "pink", iscc_nbs_formatter: Some("{1} gray"), alt_color_name: "pink", color_shade: "pink" },
    IsccNbsColorEntry { color_number: 11, iscc_nbs_color_name: "red", iscc_nbs_formatter: Some("vivid {0}"), alt_color_name: "red", color_shade: "red" },
    IsccNbsColorEntry { color_number: 12, iscc_nbs_color_name: "red", iscc_nbs_formatter: Some("strong {0}"), alt_color_name: "red", color_shade: "red" },
    IsccNbsColorEntry { color_number: 13, iscc_nbs_color_name: "red", iscc_nbs_formatter: Some("deep {0}"), alt_color_name: "red", color_shade: "red" },
    IsccNbsColorEntry { color_number: 14, iscc_nbs_color_name: "red", iscc_nbs_formatter: Some("very deep {0}"), alt_color_name: "red", color_shade: "red" },
    IsccNbsColorEntry { color_number: 15, iscc_nbs_color_name: "red", iscc_nbs_formatter: Some("moderate {0}"), alt_color_name: "red", color_shade: "red" },
    IsccNbsColorEntry { color_number: 16, iscc_nbs_color_name: "red", iscc_nbs_formatter: Some("dark {0}"), alt_color_name: "red", color_shade: "red" },
    IsccNbsColorEntry { color_number: 17, iscc_nbs_color_name: "red", iscc_nbs_formatter: Some("very dark {0}"), alt_color_name: "red", color_shade: "red" },
    IsccNbsColorEntry { color_number: 18, iscc_nbs_color_name: "red", iscc_nbs_formatter: Some("pale {0}"), alt_color_name: "red", color_shade: "red" },
    IsccNbsColorEntry { color_number: 19, iscc_nbs_color_name: "red", iscc_nbs_formatter: Some("grayish {0}"), alt_color_name: "red", color_shade: "red" },
    IsccNbsColorEntry { color_number: 20, iscc_nbs_color_name: "red", iscc_nbs_formatter: Some("dark grayish {0}"), alt_color_name: "red", color_shade: "red" },
    IsccNbsColorEntry { color_number: 21, iscc_nbs_color_name: "red", iscc_nbs_formatter: Some("blackish {0}"), alt_color_name: "red", color_shade: "red" },
    IsccNbsColorEntry { color_number: 22, iscc_nbs_color_name: "red", iscc_nbs_formatter: Some("{1} gray"), alt_color_name: "red", color_shade: "red" },
    IsccNbsColorEntry { color_number: 23, iscc_nbs_color_name: "red", iscc_nbs_formatter: Some("dark {1} gray"), alt_color_name: "red", color_shade: "red" },
    IsccNbsColorEntry { color_number: 24, iscc_nbs_color_name: "red", iscc_nbs_formatter: Some("{1} black"), alt_color_name: "red", color_shade: "red" },
    IsccNbsColorEntry { color_number: 25, iscc_nbs_color_name: "yellowish pink", iscc_nbs_formatter: Some("vivid {0}"), alt_color_name: "yellowish pink", color_shade: "pink" },
    IsccNbsColorEntry { color_number: 26, iscc_nbs_color_name: "yellowish pink", iscc_nbs_formatter: Some("strong {0}"), alt_color_name: "yellowish pink", color_shade: "pink" },
    IsccNbsColorEntry { color_number: 27, iscc_nbs_color_name: "yellowish pink", iscc_nbs_formatter: Some("deep {0}"), alt_color_name: "yellowish pink", color_shade: "pink" },
    IsccNbsColorEntry { color_number: 28, iscc_nbs_color_name: "yellowish pink", iscc_nbs_formatter: Some("light {0}"), alt_color_name: "yellowish pink", color_shade: "pink" },
    IsccNbsColorEntry { color_number: 29, iscc_nbs_color_name: "yellowish pink", iscc_nbs_formatter: Some("moderate {0}"), alt_color_name: "yellowish pink", color_shade: "pink" },
    IsccNbsColorEntry { color_number: 30, iscc_nbs_color_name: "yellowish pink", iscc_nbs_formatter: Some("dark {0}"), alt_color_name: "yellowish pink", color_shade: "pink" },
    IsccNbsColorEntry { color_number: 31, iscc_nbs_color_name: "yellowish pink", iscc_nbs_formatter: Some("pale {0}"), alt_color_name: "yellowish pink", color_shade: "pink" },
    IsccNbsColorEntry { color_number: 32, iscc_nbs_color_name: "yellowish pink", iscc_nbs_formatter: Some("grayish {0}"), alt_color_name: "yellowish pink", color_shade: "pink" },
    IsccNbsColorEntry { color_number: 33, iscc_nbs_color_name: "pink", iscc_nbs_formatter: Some("brownish {0}"), alt_color_name: "pink", color_shade: "pink" },
    IsccNbsColorEntry { color_number: 34, iscc_nbs_color_name: "reddish orange", iscc_nbs_formatter: Some("vivid {0}"), alt_color_name: "reddish orange", color_shade: "orange" },
    IsccNbsColorEntry { color_number: 35, iscc_nbs_color_name: "reddish orange", iscc_nbs_formatter: Some("strong {0}"), alt_color_name: "reddish orange", color_shade: "orange" },
    IsccNbsColorEntry { color_number: 36, iscc_nbs_color_name: "reddish orange", iscc_nbs_formatter: Some("deep {0}"), alt_color_name: "reddish orange", color_shade: "orange" },
    IsccNbsColorEntry { color_number: 37, iscc_nbs_color_name: "reddish orange", iscc_nbs_formatter: Some("moderate {0}"), alt_color_name: "reddish orange", color_shade: "orange" },
    IsccNbsColorEntry { color_number: 38, iscc_nbs_color_name: "reddish orange", iscc_nbs_formatter: Some("dark {0}"), alt_color_name: "reddish orange", color_shade: "orange" },
    IsccNbsColorEntry { color_number: 39, iscc_nbs_color_name: "reddish orange", iscc_nbs_formatter: Some("grayish {0}"), alt_color_name: "reddish orange", color_shade: "orange" },
    IsccNbsColorEntry { color_number: 40, iscc_nbs_color_name: "reddish brown", iscc_nbs_formatter: Some("strong {0}"), alt_color_name: "reddish brown", color_shade: "brown" },
    IsccNbsColorEntry { color_number: 41, iscc_nbs_color_name: "reddish brown", iscc_nbs_formatter: Some("deep {0}"), alt_color_name: "reddish brown", color_shade: "brown" },
    IsccNbsColorEntry { color_number: 42, iscc_nbs_color_name: "reddish brown", iscc_nbs_formatter: Some("light {0}"), alt_color_name: "reddish brown", color_shade: "brown" },
    IsccNbsColorEntry { color_number: 43, iscc_nbs_color_name: "reddish brown", iscc_nbs_formatter: Some("moderate {0}"), alt_color_name: "reddish brown", color_shade: "brown" },
    IsccNbsColorEntry { color_number: 44, iscc_nbs_color_name: "reddish brown", iscc_nbs_formatter: Some("dark {0}"), alt_color_name: "reddish brown", color_shade: "brown" },
    IsccNbsColorEntry { color_number: 45, iscc_nbs_color_name: "reddish brown", iscc_nbs_formatter: Some("pale {0}"), alt_color_name: "reddish brown", color_shade: "brown" },
    IsccNbsColorEntry { color_number: 46, iscc_nbs_color_name: "reddish brown", iscc_nbs_formatter: Some("grayish {0}"), alt_color_name: "reddish brown", color_shade: "brown" },
    IsccNbsColorEntry { color_number: 47, iscc_nbs_color_name: "reddish brown", iscc_nbs_formatter: Some("dark grayish {0}"), alt_color_name: "reddish brown", color_shade: "brown" },
    IsccNbsColorEntry { color_number: 48, iscc_nbs_color_name: "orange", iscc_nbs_formatter: Some("vivid {0}"), alt_color_name: "orange", color_shade: "orange" },
    IsccNbsColorEntry { color_number: 49, iscc_nbs_color_name: "orange", iscc_nbs_formatter: Some("brilliant {0}"), alt_color_name: "orange", color_shade: "orange" },
    IsccNbsColorEntry { color_number: 50, iscc_nbs_color_name: "orange", iscc_nbs_formatter: Some("strong {0}"), alt_color_name: "orange", color_shade: "orange" },
    IsccNbsColorEntry { color_number: 51, iscc_nbs_color_name: "orange", iscc_nbs_formatter: Some("deep {0}"), alt_color_name: "orange", color_shade: "orange" },
    IsccNbsColorEntry { color_number: 52, iscc_nbs_color_name: "orange", iscc_nbs_formatter: Some("light {0}"), alt_color_name: "orange", color_shade: "orange" },
    IsccNbsColorEntry { color_number: 53, iscc_nbs_color_name: "orange", iscc_nbs_formatter: Some("moderate {0}"), alt_color_name: "orange", color_shade: "orange" },
    IsccNbsColorEntry { color_number: 54, iscc_nbs_color_name: "orange", iscc_nbs_formatter: Some("brownish {0}"), alt_color_name: "orange", color_shade: "orange" },
    IsccNbsColorEntry { color_number: 55, iscc_nbs_color_name: "brown", iscc_nbs_formatter: Some("strong {0}"), alt_color_name: "brown", color_shade: "brown" },
    IsccNbsColorEntry { color_number: 56, iscc_nbs_color_name: "brown", iscc_nbs_formatter: Some("deep {0}"), alt_color_name: "brown", color_shade: "brown" },
    IsccNbsColorEntry { color_number: 57, iscc_nbs_color_name: "brown", iscc_nbs_formatter: Some("light {0}"), alt_color_name: "brown", color_shade: "brown" },
    IsccNbsColorEntry { color_number: 58, iscc_nbs_color_name: "brown", iscc_nbs_formatter: Some("moderate {0}"), alt_color_name: "brown", color_shade: "brown" },
    IsccNbsColorEntry { color_number: 59, iscc_nbs_color_name: "brown", iscc_nbs_formatter: Some("dark {0}"), alt_color_name: "brown", color_shade: "brown" },
    IsccNbsColorEntry { color_number: 60, iscc_nbs_color_name: "brown", iscc_nbs_formatter: Some("pale {0}"), alt_color_name: "brown", color_shade: "brown" },
    IsccNbsColorEntry { color_number: 61, iscc_nbs_color_name: "brown", iscc_nbs_formatter: Some("grayish {0}"), alt_color_name: "brown", color_shade: "brown" },
    IsccNbsColorEntry { color_number: 62, iscc_nbs_color_name: "brown", iscc_nbs_formatter: Some("dark grayish {0}"), alt_color_name: "brown", color_shade: "brown" },
    IsccNbsColorEntry { color_number: 63, iscc_nbs_color_name: "brown", iscc_nbs_formatter: Some("light {1} gray"), alt_color_name: "brown", color_shade: "brown" },
    IsccNbsColorEntry { color_number: 64, iscc_nbs_color_name: "brown", iscc_nbs_formatter: Some("{1} gray"), alt_color_name: "brown", color_shade: "brown" },
    IsccNbsColorEntry { color_number: 65, iscc_nbs_color_name: "brown", iscc_nbs_formatter: Some("{1} black"), alt_color_name: "brown", color_shade: "brown" },
    IsccNbsColorEntry { color_number: 66, iscc_nbs_color_name: "orange yellow", iscc_nbs_formatter: Some("vivid {0}"), alt_color_name: "orange yellow", color_shade: "yellow" },
    IsccNbsColorEntry { color_number: 67, iscc_nbs_color_name: "orange yellow", iscc_nbs_formatter: Some("brilliant {0}"), alt_color_name: "orange yellow", color_shade: "yellow" },
    IsccNbsColorEntry { color_number: 68, iscc_nbs_color_name: "orange yellow", iscc_nbs_formatter: Some("strong {0}"), alt_color_name: "orange yellow", color_shade: "yellow" },
    IsccNbsColorEntry { color_number: 69, iscc_nbs_color_name: "orange yellow", iscc_nbs_formatter: Some("deep {0}"), alt_color_name: "orange yellow", color_shade: "yellow" },
    IsccNbsColorEntry { color_number: 70, iscc_nbs_color_name: "orange yellow", iscc_nbs_formatter: Some("light {0}"), alt_color_name: "orange yellow", color_shade: "yellow" },
    IsccNbsColorEntry { color_number: 71, iscc_nbs_color_name: "orange yellow", iscc_nbs_formatter: Some("moderate {0}"), alt_color_name: "orange yellow", color_shade: "yellow" },
    IsccNbsColorEntry { color_number: 72, iscc_nbs_color_name: "orange yellow", iscc_nbs_formatter: Some("dark {0}"), alt_color_name: "orange yellow", color_shade: "yellow" },
    IsccNbsColorEntry { color_number: 73, iscc_nbs_color_name: "orange yellow", iscc_nbs_formatter: Some("pale {0}"), alt_color_name: "orange yellow", color_shade: "yellow" },
    IsccNbsColorEntry { color_number: 74, iscc_nbs_color_name: "yellowish brown", iscc_nbs_formatter: Some("strong {0}"), alt_color_name: "yellowish brown", color_shade: "brown" },
    IsccNbsColorEntry { color_number: 75, iscc_nbs_color_name: "yellowish brown", iscc_nbs_formatter: Some("deep {0}"), alt_color_name: "yellowish brown", color_shade: "brown" },
    IsccNbsColorEntry { color_number: 76, iscc_nbs_color_name: "yellowish brown", iscc_nbs_formatter: Some("light {0}"), alt_color_name: "yellowish brown", color_shade: "brown" },
    IsccNbsColorEntry { color_number: 77, iscc_nbs_color_name: "yellowish brown", iscc_nbs_formatter: Some("moderate {0}"), alt_color_name: "yellowish brown", color_shade: "brown" },
    IsccNbsColorEntry { color_number: 78, iscc_nbs_color_name: "yellowish brown", iscc_nbs_formatter: Some("dark {0}"), alt_color_name: "yellowish brown", color_shade: "brown" },
    IsccNbsColorEntry { color_number: 79, iscc_nbs_color_name: "yellowish brown", iscc_nbs_formatter: Some("pale {0}"), alt_color_name: "yellowish brown", color_shade: "brown" },
    IsccNbsColorEntry { color_number: 80, iscc_nbs_color_name: "yellowish brown", iscc_nbs_formatter: Some("grayish {0}"), alt_color_name: "yellowish brown", color_shade: "brown" },
    IsccNbsColorEntry { color_number: 81, iscc_nbs_color_name: "yellowish brown", iscc_nbs_formatter: Some("dark grayish {0}"), alt_color_name: "yellowish brown", color_shade: "brown" },
    IsccNbsColorEntry { color_number: 82, iscc_nbs_color_name: "yellow", iscc_nbs_formatter: Some("vivid {0}"), alt_color_name: "yellow", color_shade: "yellow" },
    IsccNbsColorEntry { color_number: 83, iscc_nbs_color_name: "yellow", iscc_nbs_formatter: Some("brilliant {0}"), alt_color_name: "yellow", color_shade: "yellow" },
    IsccNbsColorEntry { color_number: 84, iscc_nbs_color_name: "yellow", iscc_nbs_formatter: Some("strong {0}"), alt_color_name: "yellow", color_shade: "yellow" },
    IsccNbsColorEntry { color_number: 85, iscc_nbs_color_name: "yellow", iscc_nbs_formatter: Some("deep {0}"), alt_color_name: "yellow", color_shade: "yellow" },
    IsccNbsColorEntry { color_number: 86, iscc_nbs_color_name: "yellow", iscc_nbs_formatter: Some("light {0}"), alt_color_name: "yellow", color_shade: "yellow" },
    IsccNbsColorEntry { color_number: 87, iscc_nbs_color_name: "yellow", iscc_nbs_formatter: Some("moderate {0}"), alt_color_name: "yellow", color_shade: "yellow" },
    IsccNbsColorEntry { color_number: 88, iscc_nbs_color_name: "yellow", iscc_nbs_formatter: Some("dark {0}"), alt_color_name: "yellow", color_shade: "yellow" },
    IsccNbsColorEntry { color_number: 89, iscc_nbs_color_name: "yellow", iscc_nbs_formatter: Some("pale {0}"), alt_color_name: "yellow", color_shade: "yellow" },
    IsccNbsColorEntry { color_number: 90, iscc_nbs_color_name: "yellow", iscc_nbs_formatter: Some("grayish {0}"), alt_color_name: "yellow", color_shade: "yellow" },
    IsccNbsColorEntry { color_number: 91, iscc_nbs_color_name: "yellow", iscc_nbs_formatter: Some("dark grayish {0}"), alt_color_name: "yellow", color_shade: "yellow" },
    IsccNbsColorEntry { color_number: 92, iscc_nbs_color_name: "yellow", iscc_nbs_formatter: Some("{1} white"), alt_color_name: "yellow", color_shade: "yellow" },
    IsccNbsColorEntry { color_number: 93, iscc_nbs_color_name: "yellow", iscc_nbs_formatter: Some("{1} gray"), alt_color_name: "yellow", color_shade: "yellow" },
    IsccNbsColorEntry { color_number: 94, iscc_nbs_color_name: "olive brown", iscc_nbs_formatter: Some("light {0}"), alt_color_name: "olive brown", color_shade: "brown" },
    IsccNbsColorEntry { color_number: 95, iscc_nbs_color_name: "olive brown", iscc_nbs_formatter: Some("moderate {0}"), alt_color_name: "olive brown", color_shade: "brown" },
    IsccNbsColorEntry { color_number: 96, iscc_nbs_color_name: "olive brown", iscc_nbs_formatter: Some("dark {0}"), alt_color_name: "olive brown", color_shade: "brown" },
    IsccNbsColorEntry { color_number: 97, iscc_nbs_color_name: "greenish yellow", iscc_nbs_formatter: Some("vivid {0}"), alt_color_name: "greenish yellow", color_shade: "yellow" },
    IsccNbsColorEntry { color_number: 98, iscc_nbs_color_name: "greenish yellow", iscc_nbs_formatter: Some("brilliant {0}"), alt_color_name: "greenish yellow", color_shade: "yellow" },
    IsccNbsColorEntry { color_number: 99, iscc_nbs_color_name: "greenish yellow", iscc_nbs_formatter: Some("strong {0}"), alt_color_name: "greenish yellow", color_shade: "yellow" },
    IsccNbsColorEntry { color_number: 100, iscc_nbs_color_name: "greenish yellow", iscc_nbs_formatter: Some("deep {0}"), alt_color_name: "greenish yellow", color_shade: "yellow" },
    IsccNbsColorEntry { color_number: 101, iscc_nbs_color_name: "greenish yellow", iscc_nbs_formatter: Some("light {0}"), alt_color_name: "greenish yellow", color_shade: "yellow" },
    IsccNbsColorEntry { color_number: 102, iscc_nbs_color_name: "greenish yellow", iscc_nbs_formatter: Some("moderate {0}"), alt_color_name: "greenish yellow", color_shade: "yellow" },
    IsccNbsColorEntry { color_number: 103, iscc_nbs_color_name: "greenish yellow", iscc_nbs_formatter: Some("dark {0}"), alt_color_name: "greenish yellow", color_shade: "yellow" },
    IsccNbsColorEntry { color_number: 104, iscc_nbs_color_name: "greenish yellow", iscc_nbs_formatter: Some("pale {0}"), alt_color_name: "greenish yellow", color_shade: "yellow" },
    IsccNbsColorEntry { color_number: 105, iscc_nbs_color_name: "greenish yellow", iscc_nbs_formatter: Some("grayish {0}"), alt_color_name: "greenish yellow", color_shade: "yellow" },
    IsccNbsColorEntry { color_number: 106, iscc_nbs_color_name: "olive", iscc_nbs_formatter: Some("light {0}"), alt_color_name: "olive", color_shade: "olive" },
    IsccNbsColorEntry { color_number: 107, iscc_nbs_color_name: "olive", iscc_nbs_formatter: Some("moderate {0}"), alt_color_name: "olive", color_shade: "olive" },
    IsccNbsColorEntry { color_number: 108, iscc_nbs_color_name: "olive", iscc_nbs_formatter: Some("dark {0}"), alt_color_name: "olive", color_shade: "olive" },
    IsccNbsColorEntry { color_number: 109, iscc_nbs_color_name: "olive", iscc_nbs_formatter: Some("pale {0}"), alt_color_name: "olive", color_shade: "olive" },
    IsccNbsColorEntry { color_number: 110, iscc_nbs_color_name: "olive", iscc_nbs_formatter: Some("grayish {0}"), alt_color_name: "olive", color_shade: "olive" },
    IsccNbsColorEntry { color_number: 111, iscc_nbs_color_name: "olive", iscc_nbs_formatter: Some("dark grayish {0}"), alt_color_name: "olive", color_shade: "olive" },
    IsccNbsColorEntry { color_number: 112, iscc_nbs_color_name: "olive", iscc_nbs_formatter: Some("light {1} gray"), alt_color_name: "olive", color_shade: "olive" },
    IsccNbsColorEntry { color_number: 113, iscc_nbs_color_name: "olive", iscc_nbs_formatter: Some("{1} gray"), alt_color_name: "olive", color_shade: "olive" },
    IsccNbsColorEntry { color_number: 114, iscc_nbs_color_name: "olive", iscc_nbs_formatter: Some("{1} black"), alt_color_name: "olive", color_shade: "olive" },
    IsccNbsColorEntry { color_number: 115, iscc_nbs_color_name: "yellow green", iscc_nbs_formatter: Some("vivid {0}"), alt_color_name: "lime", color_shade: "lime" },
    IsccNbsColorEntry { color_number: 116, iscc_nbs_color_name: "yellow green", iscc_nbs_formatter: Some("brilliant {0}"), alt_color_name: "lime", color_shade: "lime" },
    IsccNbsColorEntry { color_number: 117, iscc_nbs_color_name: "yellow green", iscc_nbs_formatter: Some("strong {0}"), alt_color_name: "lime", color_shade: "lime" },
    IsccNbsColorEntry { color_number: 118, iscc_nbs_color_name: "yellow green", iscc_nbs_formatter: Some("deep {0}"), alt_color_name: "lime", color_shade: "lime" },
    IsccNbsColorEntry { color_number: 119, iscc_nbs_color_name: "yellow green", iscc_nbs_formatter: Some("light {0}"), alt_color_name: "lime", color_shade: "lime" },
    IsccNbsColorEntry { color_number: 120, iscc_nbs_color_name: "yellow green", iscc_nbs_formatter: Some("moderate {0}"), alt_color_name: "lime", color_shade: "lime" },
    IsccNbsColorEntry { color_number: 121, iscc_nbs_color_name: "yellow green", iscc_nbs_formatter: Some("pale {0}"), alt_color_name: "lime", color_shade: "lime" },
    IsccNbsColorEntry { color_number: 122, iscc_nbs_color_name: "yellow green", iscc_nbs_formatter: Some("grayish {0}"), alt_color_name: "lime", color_shade: "lime" },
    IsccNbsColorEntry { color_number: 123, iscc_nbs_color_name: "olive green", iscc_nbs_formatter: Some("strong {0}"), alt_color_name: "olive green", color_shade: "green" },
    IsccNbsColorEntry { color_number: 124, iscc_nbs_color_name: "olive green", iscc_nbs_formatter: Some("deep {0}"), alt_color_name: "olive green", color_shade: "green" },
    IsccNbsColorEntry { color_number: 125, iscc_nbs_color_name: "olive green", iscc_nbs_formatter: Some("moderate {0}"), alt_color_name: "olive green", color_shade: "green" },
    IsccNbsColorEntry { color_number: 126, iscc_nbs_color_name: "olive green", iscc_nbs_formatter: Some("dark {0}"), alt_color_name: "olive green", color_shade: "green" },
    IsccNbsColorEntry { color_number: 127, iscc_nbs_color_name: "olive green", iscc_nbs_formatter: Some("grayish {0}"), alt_color_name: "olive green", color_shade: "green" },
    IsccNbsColorEntry { color_number: 128, iscc_nbs_color_name: "olive green", iscc_nbs_formatter: Some("dark grayish {0}"), alt_color_name: "olive green", color_shade: "green" },
    IsccNbsColorEntry { color_number: 129, iscc_nbs_color_name: "yellowish green", iscc_nbs_formatter: Some("vivid {0}"), alt_color_name: "yellowish green", color_shade: "green" },
    IsccNbsColorEntry { color_number: 130, iscc_nbs_color_name: "yellowish green", iscc_nbs_formatter: Some("brilliant {0}"), alt_color_name: "yellowish green", color_shade: "green" },
    IsccNbsColorEntry { color_number: 131, iscc_nbs_color_name: "yellowish green", iscc_nbs_formatter: Some("strong {0}"), alt_color_name: "yellowish green", color_shade: "green" },
    IsccNbsColorEntry { color_number: 132, iscc_nbs_color_name: "yellowish green", iscc_nbs_formatter: Some("deep {0}"), alt_color_name: "yellowish green", color_shade: "green" },
    IsccNbsColorEntry { color_number: 133, iscc_nbs_color_name: "yellowish green", iscc_nbs_formatter: Some("very deep {0}"), alt_color_name: "yellowish green", color_shade: "green" },
    IsccNbsColorEntry { color_number: 134, iscc_nbs_color_name: "yellowish green", iscc_nbs_formatter: Some("very light {0}"), alt_color_name: "yellowish green", color_shade: "green" },
    IsccNbsColorEntry { color_number: 135, iscc_nbs_color_name: "yellowish green", iscc_nbs_formatter: Some("light {0}"), alt_color_name: "yellowish green", color_shade: "green" },
    IsccNbsColorEntry { color_number: 136, iscc_nbs_color_name: "yellowish green", iscc_nbs_formatter: Some("moderate {0}"), alt_color_name: "yellowish green", color_shade: "green" },
    IsccNbsColorEntry { color_number: 137, iscc_nbs_color_name: "yellowish green", iscc_nbs_formatter: Some("dark {0}"), alt_color_name: "yellowish green", color_shade: "green" },
    IsccNbsColorEntry { color_number: 138, iscc_nbs_color_name: "yellowish green", iscc_nbs_formatter: Some("very dark {0}"), alt_color_name: "yellowish green", color_shade: "green" },
    IsccNbsColorEntry { color_number: 139, iscc_nbs_color_name: "green", iscc_nbs_formatter: Some("vivid {0}"), alt_color_name: "green", color_shade: "green" },
    IsccNbsColorEntry { color_number: 140, iscc_nbs_color_name: "green", iscc_nbs_formatter: Some("brilliant {0}"), alt_color_name: "green", color_shade: "green" },
    IsccNbsColorEntry { color_number: 141, iscc_nbs_color_name: "green", iscc_nbs_formatter: Some("strong {0}"), alt_color_name: "green", color_shade: "green" },
    IsccNbsColorEntry { color_number: 142, iscc_nbs_color_name: "green", iscc_nbs_formatter: Some("deep {0}"), alt_color_name: "green", color_shade: "green" },
    IsccNbsColorEntry { color_number: 143, iscc_nbs_color_name: "green", iscc_nbs_formatter: Some("very light {0}"), alt_color_name: "green", color_shade: "green" },
    IsccNbsColorEntry { color_number: 144, iscc_nbs_color_name: "green", iscc_nbs_formatter: Some("light {0}"), alt_color_name: "green", color_shade: "green" },
    IsccNbsColorEntry { color_number: 145, iscc_nbs_color_name: "green", iscc_nbs_formatter: Some("moderate {0}"), alt_color_name: "green", color_shade: "green" },
    IsccNbsColorEntry { color_number: 146, iscc_nbs_color_name: "green", iscc_nbs_formatter: Some("dark {0}"), alt_color_name: "green", color_shade: "green" },
    IsccNbsColorEntry { color_number: 147, iscc_nbs_color_name: "green", iscc_nbs_formatter: Some("very dark {0}"), alt_color_name: "green", color_shade: "green" },
    IsccNbsColorEntry { color_number: 148, iscc_nbs_color_name: "green", iscc_nbs_formatter: Some("very pale {0}"), alt_color_name: "green", color_shade: "green" },
    IsccNbsColorEntry { color_number: 149, iscc_nbs_color_name: "green", iscc_nbs_formatter: Some("pale {0}"), alt_color_name: "green", color_shade: "green" },
    IsccNbsColorEntry { color_number: 150, iscc_nbs_color_name: "green", iscc_nbs_formatter: Some("grayish {0}"), alt_color_name: "green", color_shade: "green" },
    IsccNbsColorEntry { color_number: 151, iscc_nbs_color_name: "green", iscc_nbs_formatter: Some("dark grayish {0}"), alt_color_name: "green", color_shade: "green" },
    IsccNbsColorEntry { color_number: 152, iscc_nbs_color_name: "green", iscc_nbs_formatter: Some("blackish {0}"), alt_color_name: "green", color_shade: "green" },
    IsccNbsColorEntry { color_number: 153, iscc_nbs_color_name: "green", iscc_nbs_formatter: Some("{1} white"), alt_color_name: "green", color_shade: "green" },
    IsccNbsColorEntry { color_number: 154, iscc_nbs_color_name: "green", iscc_nbs_formatter: Some("light {1} gray"), alt_color_name: "green", color_shade: "green" },
    IsccNbsColorEntry { color_number: 155, iscc_nbs_color_name: "green", iscc_nbs_formatter: Some("{1} gray"), alt_color_name: "green", color_shade: "green" },
    IsccNbsColorEntry { color_number: 156, iscc_nbs_color_name: "green", iscc_nbs_formatter: Some("dark {1} gray"), alt_color_name: "green", color_shade: "green" },
    IsccNbsColorEntry { color_number: 157, iscc_nbs_color_name: "green", iscc_nbs_formatter: Some("{1} black"), alt_color_name: "green", color_shade: "green" },
    IsccNbsColorEntry { color_number: 158, iscc_nbs_color_name: "bluish green", iscc_nbs_formatter: Some("vivid {0}"), alt_color_name: "turquoise", color_shade: "turquoise" },
    IsccNbsColorEntry { color_number: 159, iscc_nbs_color_name: "bluish green", iscc_nbs_formatter: Some("brilliant {0}"), alt_color_name: "turquoise", color_shade: "turquoise" },
    IsccNbsColorEntry { color_number: 160, iscc_nbs_color_name: "bluish green", iscc_nbs_formatter: Some("strong {0}"), alt_color_name: "turquoise", color_shade: "turquoise" },
    IsccNbsColorEntry { color_number: 161, iscc_nbs_color_name: "bluish green", iscc_nbs_formatter: Some("deep {0}"), alt_color_name: "turquoise", color_shade: "turquoise" },
    IsccNbsColorEntry { color_number: 162, iscc_nbs_color_name: "bluish green", iscc_nbs_formatter: Some("very light {0}"), alt_color_name: "turquoise", color_shade: "turquoise" },
    IsccNbsColorEntry { color_number: 163, iscc_nbs_color_name: "bluish green", iscc_nbs_formatter: Some("light {0}"), alt_color_name: "turquoise", color_shade: "turquoise" },
    IsccNbsColorEntry { color_number: 164, iscc_nbs_color_name: "bluish green", iscc_nbs_formatter: Some("moderate {0}"), alt_color_name: "turquoise", color_shade: "turquoise" },
    IsccNbsColorEntry { color_number: 165, iscc_nbs_color_name: "bluish green", iscc_nbs_formatter: Some("dark {0}"), alt_color_name: "turquoise", color_shade: "turquoise" },
    IsccNbsColorEntry { color_number: 166, iscc_nbs_color_name: "bluish green", iscc_nbs_formatter: Some("very dark {0}"), alt_color_name: "turquoise", color_shade: "turquoise" },
    IsccNbsColorEntry { color_number: 167, iscc_nbs_color_name: "greenish blue", iscc_nbs_formatter: Some("vivid {0}"), alt_color_name: "teal", color_shade: "teal" },
    IsccNbsColorEntry { color_number: 168, iscc_nbs_color_name: "greenish blue", iscc_nbs_formatter: Some("brilliant {0}"), alt_color_name: "teal", color_shade: "teal" },
    IsccNbsColorEntry { color_number: 169, iscc_nbs_color_name: "greenish blue", iscc_nbs_formatter: Some("strong {0}"), alt_color_name: "teal", color_shade: "teal" },
    IsccNbsColorEntry { color_number: 170, iscc_nbs_color_name: "greenish blue", iscc_nbs_formatter: Some("deep {0}"), alt_color_name: "teal", color_shade: "teal" },
    IsccNbsColorEntry { color_number: 171, iscc_nbs_color_name: "greenish blue", iscc_nbs_formatter: Some("very light {0}"), alt_color_name: "teal", color_shade: "teal" },
    IsccNbsColorEntry { color_number: 172, iscc_nbs_color_name: "greenish blue", iscc_nbs_formatter: Some("light {0}"), alt_color_name: "teal", color_shade: "teal" },
    IsccNbsColorEntry { color_number: 173, iscc_nbs_color_name: "greenish blue", iscc_nbs_formatter: Some("moderate {0}"), alt_color_name: "teal", color_shade: "teal" },
    IsccNbsColorEntry { color_number: 174, iscc_nbs_color_name: "greenish blue", iscc_nbs_formatter: Some("dark {0}"), alt_color_name: "teal", color_shade: "teal" },
    IsccNbsColorEntry { color_number: 175, iscc_nbs_color_name: "greenish blue", iscc_nbs_formatter: Some("very dark {0}"), alt_color_name: "teal", color_shade: "teal" },
    IsccNbsColorEntry { color_number: 176, iscc_nbs_color_name: "blue", iscc_nbs_formatter: Some("vivid {0}"), alt_color_name: "blue", color_shade: "blue" },
    IsccNbsColorEntry { color_number: 177, iscc_nbs_color_name: "blue", iscc_nbs_formatter: Some("brilliant {0}"), alt_color_name: "blue", color_shade: "blue" },
    IsccNbsColorEntry { color_number: 178, iscc_nbs_color_name: "blue", iscc_nbs_formatter: Some("strong {0}"), alt_color_name: "blue", color_shade: "blue" },
    IsccNbsColorEntry { color_number: 179, iscc_nbs_color_name: "blue", iscc_nbs_formatter: Some("deep {0}"), alt_color_name: "blue", color_shade: "blue" },
    IsccNbsColorEntry { color_number: 180, iscc_nbs_color_name: "blue", iscc_nbs_formatter: Some("very light {0}"), alt_color_name: "blue", color_shade: "blue" },
    IsccNbsColorEntry { color_number: 181, iscc_nbs_color_name: "blue", iscc_nbs_formatter: Some("light {0}"), alt_color_name: "blue", color_shade: "blue" },
    IsccNbsColorEntry { color_number: 182, iscc_nbs_color_name: "blue", iscc_nbs_formatter: Some("moderate {0}"), alt_color_name: "blue", color_shade: "blue" },
    IsccNbsColorEntry { color_number: 183, iscc_nbs_color_name: "blue", iscc_nbs_formatter: Some("dark {0}"), alt_color_name: "blue", color_shade: "blue" },
    IsccNbsColorEntry { color_number: 184, iscc_nbs_color_name: "blue", iscc_nbs_formatter: Some("very pale {0}"), alt_color_name: "blue", color_shade: "blue" },
    IsccNbsColorEntry { color_number: 185, iscc_nbs_color_name: "blue", iscc_nbs_formatter: Some("pale {0}"), alt_color_name: "blue", color_shade: "blue" },
    IsccNbsColorEntry { color_number: 186, iscc_nbs_color_name: "blue", iscc_nbs_formatter: Some("grayish {0}"), alt_color_name: "blue", color_shade: "blue" },
    IsccNbsColorEntry { color_number: 187, iscc_nbs_color_name: "blue", iscc_nbs_formatter: Some("dark grayish {0}"), alt_color_name: "blue", color_shade: "blue" },
    IsccNbsColorEntry { color_number: 188, iscc_nbs_color_name: "blue", iscc_nbs_formatter: Some("blackish {0}"), alt_color_name: "blue", color_shade: "blue" },
    IsccNbsColorEntry { color_number: 189, iscc_nbs_color_name: "blue", iscc_nbs_formatter: Some("{1} white"), alt_color_name: "blue", color_shade: "blue" },
    IsccNbsColorEntry { color_number: 190, iscc_nbs_color_name: "blue", iscc_nbs_formatter: Some("light {1} gray"), alt_color_name: "blue", color_shade: "blue" },
    IsccNbsColorEntry { color_number: 191, iscc_nbs_color_name: "blue", iscc_nbs_formatter: Some("{1} gray"), alt_color_name: "blue", color_shade: "blue" },
    IsccNbsColorEntry { color_number: 192, iscc_nbs_color_name: "blue", iscc_nbs_formatter: Some("dark {1} gray"), alt_color_name: "blue", color_shade: "blue" },
    IsccNbsColorEntry { color_number: 193, iscc_nbs_color_name: "blue", iscc_nbs_formatter: Some("{1} black"), alt_color_name: "blue", color_shade: "blue" },
    IsccNbsColorEntry { color_number: 194, iscc_nbs_color_name: "purplish blue", iscc_nbs_formatter: Some("vivid {0}"), alt_color_name: "purplish blue", color_shade: "blue" },
    IsccNbsColorEntry { color_number: 195, iscc_nbs_color_name: "purplish blue", iscc_nbs_formatter: Some("brilliant {0}"), alt_color_name: "purplish blue", color_shade: "blue" },
    IsccNbsColorEntry { color_number: 196, iscc_nbs_color_name: "purplish blue", iscc_nbs_formatter: Some("strong {0}"), alt_color_name: "purplish blue", color_shade: "blue" },
    IsccNbsColorEntry { color_number: 197, iscc_nbs_color_name: "purplish blue", iscc_nbs_formatter: Some("deep {0}"), alt_color_name: "purplish blue", color_shade: "blue" },
    IsccNbsColorEntry { color_number: 198, iscc_nbs_color_name: "purplish blue", iscc_nbs_formatter: Some("very light {0}"), alt_color_name: "purplish blue", color_shade: "blue" },
    IsccNbsColorEntry { color_number: 199, iscc_nbs_color_name: "purplish blue", iscc_nbs_formatter: Some("light {0}"), alt_color_name: "purplish blue", color_shade: "blue" },
    IsccNbsColorEntry { color_number: 200, iscc_nbs_color_name: "purplish blue", iscc_nbs_formatter: Some("moderate {0}"), alt_color_name: "purplish blue", color_shade: "blue" },
    IsccNbsColorEntry { color_number: 201, iscc_nbs_color_name: "purplish blue", iscc_nbs_formatter: Some("dark {0}"), alt_color_name: "purplish blue", color_shade: "blue" },
    IsccNbsColorEntry { color_number: 202, iscc_nbs_color_name: "purplish blue", iscc_nbs_formatter: Some("very pale {0}"), alt_color_name: "purplish blue", color_shade: "blue" },
    IsccNbsColorEntry { color_number: 203, iscc_nbs_color_name: "purplish blue", iscc_nbs_formatter: Some("pale {0}"), alt_color_name: "purplish blue", color_shade: "blue" },
    IsccNbsColorEntry { color_number: 204, iscc_nbs_color_name: "purplish blue", iscc_nbs_formatter: Some("grayish {0}"), alt_color_name: "purplish blue", color_shade: "blue" },
    IsccNbsColorEntry { color_number: 205, iscc_nbs_color_name: "violet", iscc_nbs_formatter: Some("vivid {0}"), alt_color_name: "violet", color_shade: "violet" },
    IsccNbsColorEntry { color_number: 206, iscc_nbs_color_name: "violet", iscc_nbs_formatter: Some("brilliant {0}"), alt_color_name: "violet", color_shade: "violet" },
    IsccNbsColorEntry { color_number: 207, iscc_nbs_color_name: "violet", iscc_nbs_formatter: Some("strong {0}"), alt_color_name: "violet", color_shade: "violet" },
    IsccNbsColorEntry { color_number: 208, iscc_nbs_color_name: "violet", iscc_nbs_formatter: Some("deep {0}"), alt_color_name: "violet", color_shade: "violet" },
    IsccNbsColorEntry { color_number: 209, iscc_nbs_color_name: "violet", iscc_nbs_formatter: Some("very light {0}"), alt_color_name: "violet", color_shade: "violet" },
    IsccNbsColorEntry { color_number: 210, iscc_nbs_color_name: "violet", iscc_nbs_formatter: Some("light {0}"), alt_color_name: "violet", color_shade: "violet" },
    IsccNbsColorEntry { color_number: 211, iscc_nbs_color_name: "violet", iscc_nbs_formatter: Some("moderate {0}"), alt_color_name: "violet", color_shade: "violet" },
    IsccNbsColorEntry { color_number: 212, iscc_nbs_color_name: "violet", iscc_nbs_formatter: Some("dark {0}"), alt_color_name: "violet", color_shade: "violet" },
    IsccNbsColorEntry { color_number: 213, iscc_nbs_color_name: "violet", iscc_nbs_formatter: Some("very pale {0}"), alt_color_name: "violet", color_shade: "violet" },
    IsccNbsColorEntry { color_number: 214, iscc_nbs_color_name: "violet", iscc_nbs_formatter: Some("pale {0}"), alt_color_name: "violet", color_shade: "violet" },
    IsccNbsColorEntry { color_number: 215, iscc_nbs_color_name: "violet", iscc_nbs_formatter: Some("grayish {0}"), alt_color_name: "violet", color_shade: "violet" },
    IsccNbsColorEntry { color_number: 216, iscc_nbs_color_name: "purple", iscc_nbs_formatter: Some("vivid {0}"), alt_color_name: "purple", color_shade: "purple" },
    IsccNbsColorEntry { color_number: 217, iscc_nbs_color_name: "purple", iscc_nbs_formatter: Some("brilliant {0}"), alt_color_name: "purple", color_shade: "purple" },
    IsccNbsColorEntry { color_number: 218, iscc_nbs_color_name: "purple", iscc_nbs_formatter: Some("strong {0}"), alt_color_name: "purple", color_shade: "purple" },
    IsccNbsColorEntry { color_number: 219, iscc_nbs_color_name: "purple", iscc_nbs_formatter: Some("deep {0}"), alt_color_name: "purple", color_shade: "purple" },
    IsccNbsColorEntry { color_number: 220, iscc_nbs_color_name: "purple", iscc_nbs_formatter: Some("very deep {0}"), alt_color_name: "purple", color_shade: "purple" },
    IsccNbsColorEntry { color_number: 221, iscc_nbs_color_name: "purple", iscc_nbs_formatter: Some("very light {0}"), alt_color_name: "purple", color_shade: "purple" },
    IsccNbsColorEntry { color_number: 222, iscc_nbs_color_name: "purple", iscc_nbs_formatter: Some("light {0}"), alt_color_name: "purple", color_shade: "purple" },
    IsccNbsColorEntry { color_number: 223, iscc_nbs_color_name: "purple", iscc_nbs_formatter: Some("moderate {0}"), alt_color_name: "purple", color_shade: "purple" },
    IsccNbsColorEntry { color_number: 224, iscc_nbs_color_name: "purple", iscc_nbs_formatter: Some("dark {0}"), alt_color_name: "purple", color_shade: "purple" },
    IsccNbsColorEntry { color_number: 225, iscc_nbs_color_name: "purple", iscc_nbs_formatter: Some("very dark {0}"), alt_color_name: "purple", color_shade: "purple" },
    IsccNbsColorEntry { color_number: 226, iscc_nbs_color_name: "purple", iscc_nbs_formatter: Some("very pale {0}"), alt_color_name: "purple", color_shade: "purple" },
    IsccNbsColorEntry { color_number: 227, iscc_nbs_color_name: "purple", iscc_nbs_formatter: Some("pale {0}"), alt_color_name: "purple", color_shade: "purple" },
    IsccNbsColorEntry { color_number: 228, iscc_nbs_color_name: "purple", iscc_nbs_formatter: Some("grayish {0}"), alt_color_name: "purple", color_shade: "purple" },
    IsccNbsColorEntry { color_number: 229, iscc_nbs_color_name: "purple", iscc_nbs_formatter: Some("dark grayish {0}"), alt_color_name: "purple", color_shade: "purple" },
    IsccNbsColorEntry { color_number: 230, iscc_nbs_color_name: "purple", iscc_nbs_formatter: Some("blackish {0}"), alt_color_name: "purple", color_shade: "purple" },
    IsccNbsColorEntry { color_number: 231, iscc_nbs_color_name: "purple", iscc_nbs_formatter: Some("{1} white"), alt_color_name: "purple", color_shade: "purple" },
    IsccNbsColorEntry { color_number: 232, iscc_nbs_color_name: "purple", iscc_nbs_formatter: Some("light {1} gray"), alt_color_name: "purple", color_shade: "purple" },
    IsccNbsColorEntry { color_number: 233, iscc_nbs_color_name: "purple", iscc_nbs_formatter: Some("{1} gray"), alt_color_name: "purple", color_shade: "purple" },
    IsccNbsColorEntry { color_number: 234, iscc_nbs_color_name: "purple", iscc_nbs_formatter: Some("dark {1} gray"), alt_color_name: "purple", color_shade: "purple" },
    IsccNbsColorEntry { color_number: 235, iscc_nbs_color_name: "purple", iscc_nbs_formatter: Some("{1} black"), alt_color_name: "purple", color_shade: "purple" },
    IsccNbsColorEntry { color_number: 236, iscc_nbs_color_name: "reddish purple", iscc_nbs_formatter: Some("vivid {0}"), alt_color_name: "reddish purple", color_shade: "purple" },
    IsccNbsColorEntry { color_number: 237, iscc_nbs_color_name: "reddish purple", iscc_nbs_formatter: Some("strong {0}"), alt_color_name: "reddish purple", color_shade: "purple" },
    IsccNbsColorEntry { color_number: 238, iscc_nbs_color_name: "reddish purple", iscc_nbs_formatter: Some("deep {0}"), alt_color_name: "reddish purple", color_shade: "purple" },
    IsccNbsColorEntry { color_number: 239, iscc_nbs_color_name: "reddish purple", iscc_nbs_formatter: Some("very deep {0}"), alt_color_name: "reddish purple", color_shade: "purple" },
    IsccNbsColorEntry { color_number: 240, iscc_nbs_color_name: "reddish purple", iscc_nbs_formatter: Some("light {0}"), alt_color_name: "reddish purple", color_shade: "purple" },
    IsccNbsColorEntry { color_number: 241, iscc_nbs_color_name: "reddish purple", iscc_nbs_formatter: Some("moderate {0}"), alt_color_name: "reddish purple", color_shade: "purple" },
    IsccNbsColorEntry { color_number: 242, iscc_nbs_color_name: "reddish purple", iscc_nbs_formatter: Some("dark {0}"), alt_color_name: "reddish purple", color_shade: "purple" },
    IsccNbsColorEntry { color_number: 243, iscc_nbs_color_name: "reddish purple", iscc_nbs_formatter: Some("very dark {0}"), alt_color_name: "reddish purple", color_shade: "purple" },
    IsccNbsColorEntry { color_number: 244, iscc_nbs_color_name: "reddish purple", iscc_nbs_formatter: Some("pale {0}"), alt_color_name: "reddish purple", color_shade: "purple" },
    IsccNbsColorEntry { color_number: 245, iscc_nbs_color_name: "reddish purple", iscc_nbs_formatter: Some("grayish {0}"), alt_color_name: "reddish purple", color_shade: "purple" },
    IsccNbsColorEntry { color_number: 246, iscc_nbs_color_name: "purplish pink", iscc_nbs_formatter: Some("brilliant {0}"), alt_color_name: "purplish pink", color_shade: "pink" },
    IsccNbsColorEntry { color_number: 247, iscc_nbs_color_name: "purplish pink", iscc_nbs_formatter: Some("strong {0}"), alt_color_name: "purplish pink", color_shade: "pink" },
    IsccNbsColorEntry { color_number: 248, iscc_nbs_color_name: "purplish pink", iscc_nbs_formatter: Some("deep {0}"), alt_color_name: "purplish pink", color_shade: "pink" },
    IsccNbsColorEntry { color_number: 249, iscc_nbs_color_name: "purplish pink", iscc_nbs_formatter: Some("light {0}"), alt_color_name: "purplish pink", color_shade: "pink" },
    IsccNbsColorEntry { color_number: 250, iscc_nbs_color_name: "purplish pink", iscc_nbs_formatter: Some("moderate {0}"), alt_color_name: "purplish pink", color_shade: "pink" },
    IsccNbsColorEntry { color_number: 251, iscc_nbs_color_name: "purplish pink", iscc_nbs_formatter: Some("dark {0}"), alt_color_name: "purplish pink", color_shade: "pink" },
    IsccNbsColorEntry { color_number: 252, iscc_nbs_color_name: "purplish pink", iscc_nbs_formatter: Some("pale {0}"), alt_color_name: "purplish pink", color_shade: "pink" },
    IsccNbsColorEntry { color_number: 253, iscc_nbs_color_name: "purplish pink", iscc_nbs_formatter: Some("grayish {0}"), alt_color_name: "purplish pink", color_shade: "pink" },
    IsccNbsColorEntry { color_number: 254, iscc_nbs_color_name: "purplish pink", iscc_nbs_formatter: Some("vivid {0}"), alt_color_name: "purplish pink", color_shade: "pink" },
    IsccNbsColorEntry { color_number: 255, iscc_nbs_color_name: "purplish pink", iscc_nbs_formatter: Some("strong {0}"), alt_color_name: "purplish pink", color_shade: "pink" },
    IsccNbsColorEntry { color_number: 256, iscc_nbs_color_name: "purplish red", iscc_nbs_formatter: Some("deep {0}"), alt_color_name: "purplish red", color_shade: "red" },
    IsccNbsColorEntry { color_number: 257, iscc_nbs_color_name: "purplish red", iscc_nbs_formatter: Some("very deep {0}"), alt_color_name: "purplish red", color_shade: "red" },
    IsccNbsColorEntry { color_number: 258, iscc_nbs_color_name: "purplish red", iscc_nbs_formatter: Some("moderate {0}"), alt_color_name: "purplish red", color_shade: "red" },
    IsccNbsColorEntry { color_number: 259, iscc_nbs_color_name: "purplish red", iscc_nbs_formatter: Some("dark {0}"), alt_color_name: "purplish red", color_shade: "red" },
    IsccNbsColorEntry { color_number: 260, iscc_nbs_color_name: "purplish red", iscc_nbs_formatter: Some("very dark {0}"), alt_color_name: "purplish red", color_shade: "red" },
    IsccNbsColorEntry { color_number: 261, iscc_nbs_color_name: "purplish red", iscc_nbs_formatter: Some("pale {0}"), alt_color_name: "purplish red", color_shade: "red" },
    IsccNbsColorEntry { color_number: 262, iscc_nbs_color_name: "purplish red", iscc_nbs_formatter: Some("grayish {0}"), alt_color_name: "purplish red", color_shade: "red" },
    IsccNbsColorEntry { color_number: 263, iscc_nbs_color_name: "white", iscc_nbs_formatter: Some("{0}"), alt_color_name: "white", color_shade: "white" },
    IsccNbsColorEntry { color_number: 264, iscc_nbs_color_name: "gray", iscc_nbs_formatter: Some("light {0}"), alt_color_name: "gray", color_shade: "gray" },
    IsccNbsColorEntry { color_number: 265, iscc_nbs_color_name: "gray", iscc_nbs_formatter: Some("medium {0}"), alt_color_name: "gray", color_shade: "gray" },
    IsccNbsColorEntry { color_number: 266, iscc_nbs_color_name: "gray", iscc_nbs_formatter: Some("dark {0}"), alt_color_name: "gray", color_shade: "gray" },
    IsccNbsColorEntry { color_number: 267, iscc_nbs_color_name: "black", iscc_nbs_formatter: Some("{0}"), alt_color_name: "black", color_shade: "black" },
];

/// Lazy-initialized HashMap for fast color number lookup
static COLOR_LOOKUP: std::sync::LazyLock<HashMap<u16, &'static IsccNbsColorEntry>> = 
    std::sync::LazyLock::new(|| {
        ISCC_NBS_COLORS
            .iter()
            .map(|entry| (entry.color_number, entry))
            .collect()
    });

/// Look up ISCC-NBS color metadata by color number
pub fn get_color_by_number(color_number: u16) -> Option<&'static IsccNbsColorEntry> {
    COLOR_LOOKUP.get(&color_number).copied()
}

/// Convert embedded color entry to dynamic ColorMetadata for compatibility
pub fn color_entry_to_metadata(entry: &IsccNbsColorEntry) -> crate::iscc::ColorMetadata {
    crate::iscc::ColorMetadata {
        iscc_nbs_color_name: entry.iscc_nbs_color_name.to_string(),
        iscc_nbs_formatter: entry.iscc_nbs_formatter.map(|s| s.to_string()),
        extended_name: entry.alt_color_name.to_string(),
        color_shade: entry.color_shade.to_string(),
    }
}

/// Get all color numbers in the embedded dataset
pub fn get_all_color_numbers() -> Vec<u16> {
    ISCC_NBS_COLORS
        .iter()
        .map(|entry| entry.color_number)
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_embedded_colors_count() {
        assert_eq!(ISCC_NBS_COLORS.len(), 267, "Should have all 267 ISCC-NBS colors");
    }

    #[test]
    fn test_color_lookup_function() {
        // Test first color
        let color_1 = get_color_by_number(1).unwrap();
        assert_eq!(color_1.iscc_nbs_color_name, "pink");
        assert_eq!(color_1.iscc_nbs_formatter, Some("vivid {0}"));
        
        // Test last color
        let color_267 = get_color_by_number(267).unwrap();
        assert_eq!(color_267.iscc_nbs_color_name, "black");
        assert_eq!(color_267.iscc_nbs_formatter, Some("{0}"));
        
        // Test non-existent color
        assert!(get_color_by_number(999).is_none());
    }

    #[test]
    fn test_color_metadata_conversion() {
        let entry = get_color_by_number(1).unwrap();
        let metadata = color_entry_to_metadata(entry);
        
        assert_eq!(metadata.iscc_nbs_color_name, "pink");
        assert_eq!(metadata.iscc_nbs_formatter, Some("vivid {0}".to_string()));
        assert_eq!(metadata.extended_name, "pink");
        assert_eq!(metadata.color_shade, "pink");
    }

    #[test]
    fn test_all_color_numbers() {
        let numbers = get_all_color_numbers();
        assert_eq!(numbers.len(), 267);
        assert!(numbers.contains(&1));
        assert!(numbers.contains(&267));
        
        // Check sequential numbering
        for i in 1..=267 {
            assert!(numbers.contains(&i), "Missing color number: {}", i);
        }
    }

    #[test]
    fn test_color_data_integrity() {
        // Check specific known entries
        let pink_vivid = get_color_by_number(1).unwrap();
        assert_eq!(pink_vivid.color_shade, "pink");
        
        let white = get_color_by_number(263).unwrap();
        assert_eq!(white.iscc_nbs_color_name, "white");
        assert_eq!(white.color_shade, "white");
        
        let black = get_color_by_number(267).unwrap();
        assert_eq!(black.iscc_nbs_color_name, "black");
        assert_eq!(black.color_shade, "black");
    }

    #[test]
    fn test_formatter_variations() {
        // Test colors with different formatter patterns
        let vivid_pink = get_color_by_number(1).unwrap();
        assert_eq!(vivid_pink.iscc_nbs_formatter, Some("vivid {0}"));
        
        let pink_white = get_color_by_number(9).unwrap();
        assert_eq!(pink_white.iscc_nbs_formatter, Some("{1} white"));
        
        let white_simple = get_color_by_number(263).unwrap();
        assert_eq!(white_simple.iscc_nbs_formatter, Some("{0}"));
    }
}
