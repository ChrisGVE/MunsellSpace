//! Chromatic adaptation transformation matrices
//! 
//! This module provides matrices for various chromatic adaptation transforms
//! used in color science for adapting colors from one illuminant to another.

/// Von Kries transformation matrix (Hunt-Pointer-Estevez primaries)
/// Transforms XYZ to cone response domain
pub const VON_KRIES_MATRIX: [[f64; 3]; 3] = [
    [ 0.38971,  0.68898, -0.07868],
    [-0.22981,  1.18340,  0.04641],
    [ 0.00000,  0.00000,  1.00000],
];

/// Von Kries inverse transformation matrix
/// Transforms cone response back to XYZ
pub const VON_KRIES_MATRIX_INV: [[f64; 3]; 3] = [
    [ 1.91019, -1.11214,  0.20195],
    [ 0.37095,  0.62905,  0.00000],
    [ 0.00000,  0.00000,  1.00000],
];

/// Bradford transformation matrix (most commonly used)
/// RGB primaries to cone response domain, used in ICC profiles
pub const BRADFORD_MATRIX: [[f64; 3]; 3] = [
    [ 0.8951000,  0.2664000, -0.1614000],
    [-0.7502000,  1.7135000,  0.0367000],
    [ 0.0389000, -0.0685000,  1.0296000],
];

/// Bradford inverse transformation matrix
pub const BRADFORD_MATRIX_INV: [[f64; 3]; 3] = [
    [ 0.9869929, -0.1470543,  0.1599627],
    [ 0.4323053,  0.5183603,  0.0492912],
    [-0.0085287,  0.0400428,  0.9684867],
];

/// CAT02 transformation matrix (used in CIECAM02)
/// Part of the CAT02 color appearance model
pub const CAT02_MATRIX: [[f64; 3]; 3] = [
    [ 0.7328000,  0.4296000, -0.1624000],
    [-0.7036000,  1.6975000,  0.0061000],
    [ 0.0030000,  0.0136000,  0.9834000],
];

/// CAT02 inverse transformation matrix
pub const CAT02_MATRIX_INV: [[f64; 3]; 3] = [
    [ 1.0961238, -0.2788690,  0.1827452],
    [ 0.4544690,  0.4735332,  0.0720978],
    [-0.0096276, -0.0056980,  1.0153256],
];

#[cfg(test)]
mod tests {
    use super::*;

    /// Helper function to multiply a 3x3 matrix with a 3D vector
    fn matrix_multiply_3x3(matrix: &[[f64; 3]; 3], vector: &[f64; 3]) -> [f64; 3] {
        [
            matrix[0][0] * vector[0] + matrix[0][1] * vector[1] + matrix[0][2] * vector[2],
            matrix[1][0] * vector[0] + matrix[1][1] * vector[1] + matrix[1][2] * vector[2],
            matrix[2][0] * vector[0] + matrix[2][1] * vector[1] + matrix[2][2] * vector[2],
        ]
    }

    #[test]
    fn test_bradford_inverse_identity() {
        // Test that Bradford matrix * Bradford inverse = identity
        let test_vector = [0.5, 0.7, 0.9];
        let transformed = matrix_multiply_3x3(&BRADFORD_MATRIX, &test_vector);
        let recovered = matrix_multiply_3x3(&BRADFORD_MATRIX_INV, &transformed);
        
        for i in 0..3 {
            assert!((recovered[i] - test_vector[i]).abs() < 1e-6, 
                "Bradford inverse failed at index {}: expected {}, got {}", 
                i, test_vector[i], recovered[i]);
        }
    }

    #[test]
    fn test_von_kries_inverse_identity() {
        // Test that Von Kries matrix * Von Kries inverse = identity
        let test_vector = [0.5, 0.7, 0.9];
        let transformed = matrix_multiply_3x3(&VON_KRIES_MATRIX, &test_vector);
        let recovered = matrix_multiply_3x3(&VON_KRIES_MATRIX_INV, &transformed);
        
        for i in 0..3 {
            assert!((recovered[i] - test_vector[i]).abs() < 1e-4, 
                "Von Kries inverse failed at index {}: expected {}, got {}", 
                i, test_vector[i], recovered[i]);
        }
    }

    #[test]
    fn test_cat02_inverse_identity() {
        // Test that CAT02 matrix * CAT02 inverse = identity
        let test_vector = [0.5, 0.7, 0.9];
        let transformed = matrix_multiply_3x3(&CAT02_MATRIX, &test_vector);
        let recovered = matrix_multiply_3x3(&CAT02_MATRIX_INV, &transformed);
        
        for i in 0..3 {
            assert!((recovered[i] - test_vector[i]).abs() < 1e-4, 
                "CAT02 inverse failed at index {}: expected {}, got {}", 
                i, test_vector[i], recovered[i]);
        }
    }

    #[test]
    fn test_matrix_determinants_non_zero() {
        // All transformation matrices should be invertible (non-zero determinant)
        fn determinant_3x3(m: &[[f64; 3]; 3]) -> f64 {
            m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
        }

        let matrices = [
            ("Bradford", &BRADFORD_MATRIX),
            ("Von Kries", &VON_KRIES_MATRIX),
            ("CAT02", &CAT02_MATRIX),
        ];

        for (name, matrix) in &matrices {
            let det = determinant_3x3(matrix);
            assert!(det.abs() > 1e-10, 
                "{} matrix has zero or near-zero determinant: {}", name, det);
        }
    }
}