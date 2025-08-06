//! Error types for MunsellSpace conversion operations.

use std::fmt;

/// Result type alias for MunsellSpace operations.
pub type Result<T> = std::result::Result<T, MunsellError>;

/// Comprehensive error type for Munsell color space conversion operations.
#[derive(Debug, Clone, PartialEq)]
pub enum MunsellError {
    /// Invalid RGB values (components not in 0-255 range).
    InvalidRgb {
        /// The invalid RGB values provided
        rgb: [u8; 3],
        /// Description of the validation error
        reason: String,
    },
    
    /// Color is out of the Munsell gamut and cannot be converted.
    OutOfGamut {
        /// The RGB values that are out of gamut
        rgb: [u8; 3],
        /// Additional context about the gamut limitation
        context: String,
    },
    
    /// Invalid Munsell notation string format.
    InvalidNotation {
        /// The invalid notation string
        notation: String,
        /// Description of the parsing error
        reason: String,
    },
    
    /// Reference data loading or parsing error.
    ReferenceDataError {
        /// Description of the data error
        message: String,
    },
    
    /// Internal conversion algorithm error.
    ConversionError {
        /// Description of the conversion failure
        message: String,
    },
    
    /// I/O error during file operations.
    IoError {
        /// Description of the I/O error
        message: String,
    },
    
    /// Newton-Raphson iteration failed to converge.
    ConvergenceFailed,
    
    /// Color interpolation error in mathematical conversion.
    InterpolationError {
        /// Description of the interpolation failure
        message: String,
    },
    
    /// Invalid Munsell color specification.
    InvalidMunsellColor(String),
}

impl fmt::Display for MunsellError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            MunsellError::InvalidRgb { rgb, reason } => {
                write!(f, "Invalid RGB values {:?}: {}", rgb, reason)
            }
            MunsellError::OutOfGamut { rgb, context } => {
                write!(f, "RGB {:?} is out of Munsell gamut: {}", rgb, context)
            }
            MunsellError::InvalidNotation { notation, reason } => {
                write!(f, "Invalid Munsell notation '{}': {}", notation, reason)
            }
            MunsellError::ReferenceDataError { message } => {
                write!(f, "Reference data error: {}", message)
            }
            MunsellError::ConversionError { message } => {
                write!(f, "Conversion error: {}", message)
            }
            MunsellError::IoError { message } => {
                write!(f, "I/O error: {}", message)
            }
            MunsellError::ConvergenceFailed => {
                write!(f, "Newton-Raphson iteration failed to converge")
            }
            MunsellError::InterpolationError { message } => {
                write!(f, "Interpolation error: {}", message)
            }
            MunsellError::InvalidMunsellColor(message) => {
                write!(f, "Invalid Munsell color: {}", message)
            }
        }
    }
}

impl std::error::Error for MunsellError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        None
    }
}

impl From<std::io::Error> for MunsellError {
    fn from(error: std::io::Error) -> Self {
        MunsellError::IoError {
            message: error.to_string(),
        }
    }
}

impl From<csv::Error> for MunsellError {
    fn from(error: csv::Error) -> Self {
        MunsellError::ReferenceDataError {
            message: format!("CSV parsing error: {}", error),
        }
    }
}

impl From<serde_json::Error> for MunsellError {
    fn from(error: serde_json::Error) -> Self {
        MunsellError::ConversionError {
            message: format!("JSON error: {}", error),
        }
    }
}