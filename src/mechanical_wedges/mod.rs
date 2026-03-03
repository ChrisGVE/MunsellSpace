//! Mechanical Wedge System for Deterministic ISCC-NBS Color Classification
//!
//! This module implements a deterministic hue-based partitioning system that divides
//! the Munsell hue circle into 100 wedge containers for efficient color polygon
//! distribution and lookup.
//!
//! # Algorithm Overview
//!
//! The mechanical wedge system solves the boundary ambiguity problem in ISCC-NBS
//! classification by using a deterministic rule: **exclude starting boundary, include ending boundary**.
//!
//! ## Hue Sequence
//!
//! The system uses the complete Munsell hue sequence:
//! ```text
//! [1R, 2R, 3R, ..., 10R, 1YR, 2YR, ..., 10YR, 1Y, ..., 10RP]
//! ```
//!
//! This creates 100 unique hue positions (10 families x 10 steps each).
//!
//! ## Wedge Containers
//!
//! Each wedge spans from one hue to the next:
//! - `1R->2R`: Contains colors from >1R to <=2R
//! - `2R->3R`: Contains colors from >2R to <=3R
//! - `10RP->1R`: Contains colors from >10RP to <=1R (wraparound)
//!
//! # Thread Safety
//!
//! The wedge system can be safely shared across threads using `Arc<T>` as it
//! provides read-only access to its internal structure after initialization.
//!
//! # Examples
//!
//! ```rust
//! use munsellspace::mechanical_wedges::MechanicalWedgeSystem;
//!
//! # fn main() -> Result<(), Box<dyn std::error::Error>> {
//! let wedge_system = MechanicalWedgeSystem::new();
//!
//! // System automatically creates all 100 wedge containers
//! assert_eq!(wedge_system.wedge_count(), 100);
//!
//! // Find which wedge contains a specific hue
//! if let Some(wedge_key) = wedge_system.find_wedge_for_hue("5R") {
//!     println!("5R belongs to wedge: {}", wedge_key);
//! }
//! # Ok(())
//! # }
//! ```

mod system;
mod boundary;
mod diagnostics;

#[cfg(test)]
mod tests;

// Re-export public types
pub use system::MechanicalWedgeSystem;
pub use diagnostics::{WedgeStatistics, WedgeValidationResults, SingleWedgeValidation};
