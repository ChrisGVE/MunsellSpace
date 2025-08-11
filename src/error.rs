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
    
    /// Feature not yet implemented.
    NotImplemented(String),
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
            MunsellError::NotImplemented(message) => {
                write!(f, "Not implemented: {}", message)
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

#[cfg(test)]
mod tests {
    use super::*;
    use std::io;

    #[test]
    fn test_invalid_rgb_error_display() {
        let error = MunsellError::InvalidRgb {
            rgb: [255, 128, 64],
            reason: "Component value exceeds valid range".to_string(),
        };
        assert_eq!(
            error.to_string(),
            "Invalid RGB values [255, 128, 64]: Component value exceeds valid range"
        );
    }

    #[test]
    fn test_out_of_gamut_error_display() {
        let error = MunsellError::OutOfGamut {
            rgb: [255, 255, 255],
            context: "Color exceeds maximum chroma for this hue and value".to_string(),
        };
        assert_eq!(
            error.to_string(),
            "RGB [255, 255, 255] is out of Munsell gamut: Color exceeds maximum chroma for this hue and value"
        );
    }

    #[test]
    fn test_invalid_notation_error_display() {
        let error = MunsellError::InvalidNotation {
            notation: "invalid".to_string(),
            reason: "Unable to parse hue family".to_string(),
        };
        assert_eq!(
            error.to_string(),
            "Invalid Munsell notation 'invalid': Unable to parse hue family"
        );
    }

    #[test]
    fn test_reference_data_error_display() {
        let error = MunsellError::ReferenceDataError {
            message: "CSV file not found".to_string(),
        };
        assert_eq!(error.to_string(), "Reference data error: CSV file not found");
    }

    #[test]
    fn test_conversion_error_display() {
        let error = MunsellError::ConversionError {
            message: "Mathematical conversion failed".to_string(),
        };
        assert_eq!(error.to_string(), "Conversion error: Mathematical conversion failed");
    }

    #[test]
    fn test_io_error_display() {
        let error = MunsellError::IoError {
            message: "File permission denied".to_string(),
        };
        assert_eq!(error.to_string(), "I/O error: File permission denied");
    }

    #[test]
    fn test_convergence_failed_error_display() {
        let error = MunsellError::ConvergenceFailed;
        assert_eq!(error.to_string(), "Newton-Raphson iteration failed to converge");
    }

    #[test]
    fn test_interpolation_error_display() {
        let error = MunsellError::InterpolationError {
            message: "Insufficient neighboring points".to_string(),
        };
        assert_eq!(error.to_string(), "Interpolation error: Insufficient neighboring points");
    }

    #[test]
    fn test_invalid_munsell_color_error_display() {
        let error = MunsellError::InvalidMunsellColor("Invalid value -1".to_string());
        assert_eq!(error.to_string(), "Invalid Munsell color: Invalid value -1");
    }

    #[test]
    fn test_error_equality() {
        let error1 = MunsellError::ConvergenceFailed;
        let error2 = MunsellError::ConvergenceFailed;
        assert_eq!(error1, error2);

        let error3 = MunsellError::InvalidRgb {
            rgb: [0, 0, 0],
            reason: "test".to_string(),
        };
        let error4 = MunsellError::InvalidRgb {
            rgb: [0, 0, 0],
            reason: "test".to_string(),
        };
        assert_eq!(error3, error4);
    }

    #[test]
    fn test_error_cloning() {
        let error = MunsellError::ConversionError {
            message: "test error".to_string(),
        };
        let cloned = error.clone();
        assert_eq!(error, cloned);
    }

    #[test]
    fn test_error_debug() {
        let error = MunsellError::InvalidRgb {
            rgb: [255, 128, 64],
            reason: "out of range".to_string(),
        };
        let debug_str = format!("{:?}", error);
        assert!(debug_str.contains("InvalidRgb"));
        assert!(debug_str.contains("255"));
        assert!(debug_str.contains("out of range"));
    }

    #[test]
    fn test_from_io_error() {
        let io_error = io::Error::new(io::ErrorKind::NotFound, "File not found");
        let munsell_error: MunsellError = io_error.into();
        
        match munsell_error {
            MunsellError::IoError { message } => {
                assert!(message.contains("File not found"));
            }
            _ => panic!("Expected IoError variant"),
        }
    }

    #[test]
    fn test_from_serde_json_error() {
        // Create an invalid JSON string to generate a serde_json::Error
        let json_result = serde_json::from_str::<serde_json::Value>("invalid json");
        let json_error = json_result.unwrap_err();
        let munsell_error: MunsellError = json_error.into();
        
        match munsell_error {
            MunsellError::ConversionError { message } => {
                assert!(message.contains("JSON error"));
            }
            _ => panic!("Expected ConversionError variant"),
        }
    }

    #[test]
    fn test_error_source() {
        use std::error::Error;
        
        let error = MunsellError::ConversionError {
            message: "test".to_string(),
        };
        assert!(error.source().is_none());
    }

    #[test]
    fn test_error_trait_implementation() {
        let error = MunsellError::InvalidRgb {
            rgb: [0, 0, 0],
            reason: "test".to_string(),
        };
        
        // Test that it implements std::error::Error
        let _: &dyn std::error::Error = &error;
    }

    #[test]
    fn test_result_type_alias() {
        fn test_function() -> Result<i32> {
            Ok(42)
        }
        
        assert_eq!(test_function().unwrap(), 42);
        
        fn error_function() -> Result<i32> {
            Err(MunsellError::ConvergenceFailed)
        }
        
        assert!(error_function().is_err());
    }
}