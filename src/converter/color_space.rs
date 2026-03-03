//! Color space transformation functions (sRGB, XYZ, xyY, Lab, LCHab).

use crate::constants::{BRADFORD_MATRIX, BRADFORD_MATRIX_INV, ILLUMINANT_D65_XYZ, ILLUMINANT_C_XYZ};

use super::MunsellConverter;

impl MunsellConverter {
    /// Apply sRGB gamma correction to convert to linear RGB.
    #[inline]
    pub(crate) fn srgb_to_linear_rgb(&self, srgb: [f64; 3]) -> [f64; 3] {
        const THRESHOLD: f64 = 0.04045;
        const INV_12_92: f64 = 1.0 / 12.92;
        const ALPHA: f64 = 0.055;
        const INV_1_055: f64 = 1.0 / 1.055;
        const GAMMA: f64 = 2.4;

        [
            if srgb[0] <= THRESHOLD {
                srgb[0] * INV_12_92
            } else {
                ((srgb[0] + ALPHA) * INV_1_055).powf(GAMMA)
            },
            if srgb[1] <= THRESHOLD {
                srgb[1] * INV_12_92
            } else {
                ((srgb[1] + ALPHA) * INV_1_055).powf(GAMMA)
            },
            if srgb[2] <= THRESHOLD {
                srgb[2] * INV_12_92
            } else {
                ((srgb[2] + ALPHA) * INV_1_055).powf(GAMMA)
            }
        ]
    }

    /// Convert linear RGB to XYZ using sRGB D65 transformation matrix.
    #[inline]
    pub(crate) fn linear_rgb_to_xyz_d65(&self, linear_rgb: [f64; 3]) -> [f64; 3] {
        // sRGB to XYZ D65 transformation matrix (ITU-R BT.709)
        const M00: f64 = 0.4124564; const M01: f64 = 0.3575761; const M02: f64 = 0.1804375;
        const M10: f64 = 0.2126729; const M11: f64 = 0.7151522; const M12: f64 = 0.0721750;
        const M20: f64 = 0.0193339; const M21: f64 = 0.1191920; const M22: f64 = 0.9503041;

        let [r, g, b] = linear_rgb;

        [
            M00 * r + M01 * g + M02 * b,
            M10 * r + M11 * g + M12 * b,
            M20 * r + M21 * g + M22 * b,
        ]
    }

    /// Perform chromatic adaptation from D65 to Illuminant C using Bradford transform.
    /// This is CRITICAL for accurate Munsell conversion as reference data uses Illuminant C.
    #[allow(dead_code)]
    pub(crate) fn chromatic_adaptation_d65_to_c(&self, xyz_d65: [f64; 3]) -> [f64; 3] {
        let illuminant_d65 = ILLUMINANT_D65_XYZ;
        let illuminant_c = ILLUMINANT_C_XYZ;

        // Convert illuminants to Bradford cone space
        let mut source_bradford = [0.0; 3];
        let mut dest_bradford = [0.0; 3];

        for i in 0..3 {
            source_bradford[i] = BRADFORD_MATRIX[i][0] * illuminant_d65[0] +
                               BRADFORD_MATRIX[i][1] * illuminant_d65[1] +
                               BRADFORD_MATRIX[i][2] * illuminant_d65[2];

            dest_bradford[i] = BRADFORD_MATRIX[i][0] * illuminant_c[0] +
                             BRADFORD_MATRIX[i][1] * illuminant_c[1] +
                             BRADFORD_MATRIX[i][2] * illuminant_c[2];
        }

        // Convert input XYZ to Bradford cone space
        let mut xyz_bradford = [0.0; 3];
        for i in 0..3 {
            xyz_bradford[i] = BRADFORD_MATRIX[i][0] * xyz_d65[0] +
                            BRADFORD_MATRIX[i][1] * xyz_d65[1] +
                            BRADFORD_MATRIX[i][2] * xyz_d65[2];
        }

        // Apply adaptation
        for i in 0..3 {
            xyz_bradford[i] *= dest_bradford[i] / source_bradford[i];
        }

        // Convert back to XYZ
        let mut xyz_c = [0.0; 3];
        for i in 0..3 {
            xyz_c[i] = BRADFORD_MATRIX_INV[i][0] * xyz_bradford[0] +
                      BRADFORD_MATRIX_INV[i][1] * xyz_bradford[1] +
                      BRADFORD_MATRIX_INV[i][2] * xyz_bradford[2];
        }

        xyz_c
    }

    /// Convert XYZ to xyY color space.
    #[inline]
    pub(crate) fn xyz_to_xyy(&self, xyz: [f64; 3]) -> [f64; 3] {
        let sum = xyz[0] + xyz[1] + xyz[2];
        if sum == 0.0 {
            [0.0, 0.0, 0.0]
        } else {
            [xyz[0] / sum, xyz[1] / sum, xyz[1]]
        }
    }

    /// Convert xyY back to XYZ.
    pub(crate) fn xyy_to_xyz(&self, xyy: [f64; 3]) -> [f64; 3] {
        let [x, y, big_y] = xyy;
        if y == 0.0 {
            [0.0, 0.0, 0.0]
        } else {
            [big_y * x / y, big_y, big_y * (1.0 - x - y) / y]
        }
    }

    /// Lab to XYZ conversion with D65 white point.
    pub(crate) fn lab_to_xyz_d65(&self, lab: [f64; 3]) -> [f64; 3] {
        let [l, a, b] = lab;

        let d65_white = [0.95047, 1.00000, 1.08883];

        let fy = (l + 16.0) / 116.0;
        let fx = fy + (a / 500.0);
        let fz = fy - (b / 200.0);

        let delta = 6.0 / 29.0;
        let delta_squared = delta * delta;

        let x = if fx > delta {
            fx * fx * fx
        } else {
            3.0 * delta_squared * (fx - 4.0 / 29.0)
        } * d65_white[0];

        let y = if l > 8.0 {
            ((l + 16.0) / 116.0).powf(3.0)
        } else {
            l / (116.0 * delta_squared * 3.0)
        } * d65_white[1];

        let z = if fz > delta {
            fz * fz * fz
        } else {
            3.0 * delta_squared * (fz - 4.0 / 29.0)
        } * d65_white[2];

        [x, y, z]
    }

    /// XYZ to Lab conversion with D65 white point.
    pub(crate) fn xyz_to_lab_d65(&self, xyz: [f64; 3]) -> [f64; 3] {
        let [x, y, z] = xyz;

        let d65_white = [0.95047, 1.00000, 1.08883];

        let xn = x / d65_white[0];
        let yn = y / d65_white[1];
        let zn = z / d65_white[2];

        let delta = 6.0 / 29.0;
        let delta_cubed = delta * delta * delta;

        let f = |t: f64| {
            if t > delta_cubed {
                t.powf(1.0 / 3.0)
            } else {
                t / (3.0 * delta * delta) + 4.0 / 29.0
            }
        };

        let fx = f(xn);
        let fy = f(yn);
        let fz = f(zn);

        let l = 116.0 * fy - 16.0;
        let a = 500.0 * (fx - fy);
        let b = 200.0 * (fy - fz);

        [l, a, b]
    }

    /// Lab to LCHab conversion.
    pub(crate) fn lab_to_lchab(&self, lab: [f64; 3]) -> [f64; 3] {
        let [l, a, b] = lab;
        let c = (a * a + b * b).sqrt();
        let h = b.atan2(a).to_degrees();
        let h_normalized = if h < 0.0 { h + 360.0 } else { h };
        [l, c, h_normalized]
    }
}
