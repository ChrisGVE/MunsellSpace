//! Interpolation and extrapolation classes - exact 1:1 port from Python colour-science
//! Line-by-line port with exact behavior matching

use crate::error::Result;

/// Linear interpolator - exact 1:1 port from Python colour-science LinearInterpolator
/// This class wraps numpy.interp functionality
pub struct LinearInterpolator {
    x: Vec<f64>,
    y: Vec<f64>,
}

impl LinearInterpolator {
    /// Create a new LinearInterpolator
    /// Exact 1:1 port from Python LinearInterpolator.__init__
    pub fn new(x: Vec<f64>, y: Vec<f64>) -> Result<Self> {
        // Python: attest(x.ndim == 1, '"x" independent variable must have exactly one dimension!')
        // Python: attest(y.ndim == 1, '"y" dependent variable must have exactly one dimension!')
        
        // Python: validate dimensions match
        if x.len() != y.len() {
            return Err(crate::error::MunsellError::ConversionError {
                message: format!("x and y dimensions must match: {} != {}", x.len(), y.len())
            });
        }
        
        Ok(Self { x, y })
    }
    
    /// Evaluate the interpolating polynomial at given point(s)
    /// Exact 1:1 port from Python LinearInterpolator.__call__
    pub fn interpolate(&self, x: f64) -> f64 {
        // Python: return np.interp(x, self._x, self._y)
        // np.interp behavior:
        // - Returns y[0] if x <= x[0]
        // - Returns y[-1] if x >= x[-1]
        // - Linear interpolation between points
        
        if x <= self.x[0] {
            return self.y[0];
        }
        
        if x >= self.x[self.x.len() - 1] {
            return self.y[self.y.len() - 1];
        }
        
        // Find the interval containing x
        for i in 0..self.x.len() - 1 {
            if x >= self.x[i] && x <= self.x[i + 1] {
                // Linear interpolation formula: y = y0 + (x - x0) * (y1 - y0) / (x1 - x0)
                let t = (x - self.x[i]) / (self.x[i + 1] - self.x[i]);
                return self.y[i] + t * (self.y[i + 1] - self.y[i]);
            }
        }
        
        // Should not reach here if x is in range
        self.y[self.y.len() - 1]
    }
    
    /// Interpolate multiple points
    /// Helper for batch interpolation
    pub fn interpolate_many(&self, xs: &[f64]) -> Vec<f64> {
        xs.iter().map(|&x| self.interpolate(x)).collect()
    }
    
    /// Get x values
    pub fn x(&self) -> &[f64] {
        &self.x
    }
    
    /// Get y values
    pub fn y(&self) -> &[f64] {
        &self.y
    }
}

/// Extrapolator - exact 1:1 port from Python colour-science Extrapolator
/// Extrapolates 1-D function using Linear or Constant methods
pub struct Extrapolator {
    interpolator: LinearInterpolator,
    method: ExtrapolationMethod,
    left: Option<f64>,
    right: Option<f64>,
}

/// Extrapolation method
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum ExtrapolationMethod {
    Linear,
    Constant,
}

impl Extrapolator {
    /// Create a new Extrapolator
    /// Exact 1:1 port from Python Extrapolator.__init__
    pub fn new(
        interpolator: LinearInterpolator,
        method: ExtrapolationMethod,
        left: Option<f64>,
        right: Option<f64>,
    ) -> Self {
        Self {
            interpolator,
            method,
            left,
            right,
        }
    }
    
    /// Evaluate the Extrapolator at given point
    /// Exact 1:1 port from Python Extrapolator.__call__ and _evaluate
    pub fn extrapolate(&self, x: f64) -> f64 {
        let xi = self.interpolator.x();
        let yi = self.interpolator.y();
        
        // Check if x is in interpolation range
        if x >= xi[0] && x <= xi[xi.len() - 1] {
            // Within range - use interpolator
            return self.interpolator.interpolate(x);
        }
        
        // Handle extrapolation
        if x < xi[0] {
            // Below range
            if let Some(left_val) = self.left {
                // Python: if self._left is not None: y[x < xi[0]] = self._left
                return left_val;
            }
            
            match self.method {
                ExtrapolationMethod::Linear => {
                    // Python: y[x < xi[0]] = yi[0] + (x[x < xi[0]] - xi[0]) * sdiv(yi[1] - yi[0], xi[1] - xi[0])
                    let slope = if (xi[1] - xi[0]).abs() < 1e-10 {
                        0.0
                    } else {
                        (yi[1] - yi[0]) / (xi[1] - xi[0])
                    };
                    yi[0] + (x - xi[0]) * slope
                }
                ExtrapolationMethod::Constant => {
                    // Python: y[x < xi[0]] = yi[0]
                    yi[0]
                }
            }
        } else {
            // Above range (x > xi[-1])
            if let Some(right_val) = self.right {
                // Python: if self._right is not None: y[x > xi[-1]] = self._right
                return right_val;
            }
            
            let n = xi.len();
            match self.method {
                ExtrapolationMethod::Linear => {
                    // Python: y[x > xi[-1]] = yi[-1] + (x[x > xi[-1]] - xi[-1]) * sdiv(yi[-1] - yi[-2], xi[-1] - xi[-2])
                    let slope = if (xi[n - 1] - xi[n - 2]).abs() < 1e-10 {
                        0.0
                    } else {
                        (yi[n - 1] - yi[n - 2]) / (xi[n - 1] - xi[n - 2])
                    };
                    yi[n - 1] + (x - xi[n - 1]) * slope
                }
                ExtrapolationMethod::Constant => {
                    // Python: y[x > xi[-1]] = yi[-1]
                    yi[n - 1]
                }
            }
        }
    }
    
    /// Extrapolate multiple points
    /// Helper for batch extrapolation
    pub fn extrapolate_many(&self, xs: &[f64]) -> Vec<f64> {
        xs.iter().map(|&x| self.extrapolate(x)).collect()
    }
}

/// Create a simple linear interpolator from two arrays
/// Helper function matching Python's common usage pattern
pub fn linear_interp(x: &[f64], y: &[f64], xi: f64) -> f64 {
    // This matches np.interp behavior
    if xi <= x[0] {
        return y[0];
    }
    if xi >= x[x.len() - 1] {
        return y[y.len() - 1];
    }
    
    // Find interval and interpolate
    for i in 0..x.len() - 1 {
        if xi >= x[i] && xi <= x[i + 1] {
            let t = (xi - x[i]) / (x[i + 1] - x[i]);
            return y[i] + t * (y[i + 1] - y[i]);
        }
    }
    
    y[y.len() - 1]
}

/// Clamp linear interpolation (ensure result is within y bounds)
/// This matches np.interp with bounds checking
pub fn linear_interp_clamped(x: &[f64], y: &[f64], xi: f64) -> f64 {
    let result = linear_interp(x, y, xi);
    
    // Find min and max of y values
    let y_min = y.iter().fold(f64::INFINITY, |a, &b| a.min(b));
    let y_max = y.iter().fold(f64::NEG_INFINITY, |a, &b| a.max(b));
    
    // Clamp result to y range
    result.max(y_min).min(y_max)
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_linear_interpolator() {
        let x = vec![0.0, 1.0, 2.0, 3.0];
        let y = vec![0.0, 2.0, 4.0, 6.0];
        let interp = LinearInterpolator::new(x, y).unwrap();
        
        // Test exact points
        assert_eq!(interp.interpolate(0.0), 0.0);
        assert_eq!(interp.interpolate(1.0), 2.0);
        assert_eq!(interp.interpolate(2.0), 4.0);
        assert_eq!(interp.interpolate(3.0), 6.0);
        
        // Test interpolation
        assert_eq!(interp.interpolate(0.5), 1.0);
        assert_eq!(interp.interpolate(1.5), 3.0);
        assert_eq!(interp.interpolate(2.5), 5.0);
        
        // Test extrapolation (np.interp clamps)
        assert_eq!(interp.interpolate(-1.0), 0.0);
        assert_eq!(interp.interpolate(4.0), 6.0);
    }
    
    #[test]
    fn test_extrapolator_linear() {
        let x = vec![1.0, 2.0, 3.0];
        let y = vec![1.0, 2.0, 3.0];
        let interp = LinearInterpolator::new(x, y).unwrap();
        let extrap = Extrapolator::new(interp, ExtrapolationMethod::Linear, None, None);
        
        // Test interpolation range
        assert_eq!(extrap.extrapolate(1.5), 1.5);
        assert_eq!(extrap.extrapolate(2.0), 2.0);
        assert_eq!(extrap.extrapolate(2.5), 2.5);
        
        // Test linear extrapolation
        assert_eq!(extrap.extrapolate(0.0), 0.0); // Extends line backwards
        assert_eq!(extrap.extrapolate(4.0), 4.0); // Extends line forwards
    }
    
    #[test]
    fn test_extrapolator_constant() {
        let x = vec![1.0, 2.0, 3.0];
        let y = vec![1.0, 2.0, 3.0];
        let interp = LinearInterpolator::new(x, y).unwrap();
        let extrap = Extrapolator::new(interp, ExtrapolationMethod::Constant, None, None);
        
        // Test constant extrapolation
        assert_eq!(extrap.extrapolate(0.0), 1.0); // Uses first value
        assert_eq!(extrap.extrapolate(4.0), 3.0); // Uses last value
    }
    
    #[test]
    fn test_extrapolator_with_bounds() {
        let x = vec![1.0, 2.0, 3.0];
        let y = vec![1.0, 2.0, 3.0];
        let interp = LinearInterpolator::new(x, y).unwrap();
        let extrap = Extrapolator::new(
            interp,
            ExtrapolationMethod::Linear,
            Some(0.0),  // Left bound
            Some(5.0),  // Right bound
        );
        
        // Test custom bounds override extrapolation
        assert_eq!(extrap.extrapolate(0.0), 0.0); // Uses left bound
        assert_eq!(extrap.extrapolate(4.0), 5.0); // Uses right bound
    }
    
    #[test]
    fn test_linear_interp_function() {
        let x = [0.0, 1.0, 2.0];
        let y = [0.0, 2.0, 4.0];
        
        assert_eq!(linear_interp(&x, &y, 0.5), 1.0);
        assert_eq!(linear_interp(&x, &y, 1.5), 3.0);
        assert_eq!(linear_interp(&x, &y, -1.0), 0.0); // Clamps
        assert_eq!(linear_interp(&x, &y, 3.0), 4.0);  // Clamps
    }
}