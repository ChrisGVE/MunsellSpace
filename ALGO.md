# Algorithm Specification: Mathematical Munsell Color Space Conversion

## Overview

This document specifies the complete mathematical algorithm for accurate Munsell color space conversion based on the Python colour-science library implementation. The algorithm follows ASTM D1535 standards and uses true mathematical conversion instead of lookup tables.

**LAST UPDATED**: 2024-01-03 - Complete line-by-line analysis of Python colour-science implementation

## Core Algorithm: sRGB ↔ Munsell Conversion

### Complete Conversion Pipeline

```
sRGB [0-255] → Linear RGB [0-1] → XYZ → xyY → Munsell Specification → Munsell Notation
```

### 1. sRGB to Linear RGB Conversion

**Gamma Correction (ITU-R BT.709):**
```
For each channel c in {R, G, B}:
c_norm = c / 255.0
if c_norm <= 0.04045:
    c_linear = c_norm / 12.92
else:
    c_linear = ((c_norm + 0.055) / 1.055)^2.4
```

### 2. Linear RGB to XYZ Conversion

**sRGB to XYZ Matrix (D65 illuminant):**
```
[X]   [0.4124564  0.3575761  0.1804375] [R_linear]
[Y] = [0.2126729  0.7151522  0.0721750] [G_linear]
[Z]   [0.0193339  0.1191920  0.9503041] [B_linear]
```

### 3. XYZ to xyY Conversion

```
X_total = X + Y + Z
if X_total == 0:
    x = 0.31006  # Illuminant C x
    y = 0.31616  # Illuminant C y
else:
    x = X / X_total
    y = Y / X_total

xyY = [x, y, Y]
```

### 4. xyY to Munsell Specification (Core Algorithm)

This is the heart of the mathematical conversion using ASTM D1535 method:

#### Step 4.1: Illuminant and Scaling

**Constants:**
```rust
const ILLUMINANT_C: [f64; 2] = [0.31006, 0.31616];
const MG_OXIDE_REFLECTANCE: f64 = 0.975;
const ASTM_COEFFICIENTS: [f64; 5] = [1.1914, -0.22533, 0.23352, -0.020484, 0.00081939];
```

**Scale Factor:**
- Y values must be scaled by 1/0.975 ≈ 1.0257 when using Munsell Renotation data
- This accounts for magnesium oxide reflectance relative to perfect reflecting diffuser

#### Step 4.2: ASTM D1535 Munsell Value Calculation

**Fifth-order polynomial for Munsell Value V from Luminance Y:**
```
Y = 1.1914*V - 0.22533*V² + 0.23352*V³ - 0.020484*V⁴ + 0.00081939*V⁵
```

**Inverse calculation (Newton-Raphson method):**
```rust
fn luminance_to_munsell_value(Y: f64) -> f64 {
    // Newton-Raphson iteration to solve for V given Y
    let mut v = 10.0 * Y.sqrt(); // Initial guess
    let tolerance = 1e-10;
    let max_iterations = 100;
    
    for _ in 0..max_iterations {
        let f = astm_polynomial(v) - Y;
        let df = astm_polynomial_derivative(v);
        let delta = f / df;
        v -= delta;
        
        if delta.abs() < tolerance {
            break;
        }
    }
    v
}

fn astm_polynomial(v: f64) -> f64 {
    1.1914*v - 0.22533*v*v + 0.23352*v*v*v - 0.020484*v*v*v*v + 0.00081939*v*v*v*v*v
}

fn astm_polynomial_derivative(v: f64) -> f64 {
    1.1914 - 2.0*0.22533*v + 3.0*0.23352*v*v - 4.0*0.020484*v*v*v + 5.0*0.00081939*v*v*v*v
}
```

#### Step 4.3: Hue and Chroma Calculation via Interpolation

The colour-science library uses the Munsell Renotation dataset for interpolation:

1. **Load Munsell Renotation Data:** 
   - Dataset contains mapping of Munsell notation → xyY coordinates
   - Covers comprehensive range of hue families, values, and chromas
   - Used for reverse interpolation to find Munsell coordinates

2. **Radial Basis Function Interpolation:**
   - Use the dataset to create interpolation functions
   - Given xyY coordinates, interpolate to find corresponding Munsell hue/chroma
   - Handle boundary conditions and extrapolation

3. **Cylindrical Coordinate Transformation:**
   - Convert from Cartesian (x,y) to polar coordinates for hue calculation
   - Use chroma as radial distance from neutral axis

#### Step 4.4: Special Cases

**Achromatic Colors (Near Neutral):**
```rust
const ACHROMATIC_THRESHOLD: f64 = 1e-6;

if is_achromatic(x, y, ILLUMINANT_C[0], ILLUMINANT_C[1], ACHROMATIC_THRESHOLD) {
    return MunsellSpecification {
        hue: 0.0,
        family: "N".to_string(),
        value: munsell_value,
        chroma: 0.0,
    };
}
```

**MacAdam Limits Check:**
```rust
fn is_within_macadam_limits(x: f64, y: f64) -> bool {
    // Check if chromaticity coordinates are within physically realizable limits
    // Implementation depends on MacAdam limit boundary definition
}
```

### 5. Munsell Specification to Notation Conversion

Convert numerical specification to standard Munsell notation:

```rust
fn format_munsell_notation(spec: &MunsellSpecification) -> String {
    if spec.family == "N" {
        format!("N {:.1}", spec.value)
    } else {
        format!("{:.1}{} {:.1}/{:.1}", spec.hue, spec.family, spec.value, spec.chroma)
    }
}
```

## Bidirectional Conversion: Munsell → xyY

### Munsell Notation Parsing

```rust
fn parse_munsell_notation(notation: &str) -> Result<MunsellSpecification, MunsellError> {
    // Parse strings like "5.0R 4.0/12.0" or "N 5.0"
    // Handle neutral colors and chromatic colors separately
}
```

### Specification to xyY Conversion

1. **Value to Luminance:** Use ASTM polynomial directly
2. **Hue/Chroma to xy:** Interpolate using Munsell Renotation dataset
3. **Apply Scaling:** Account for magnesium oxide reflectance factor

## Data Structures

### Rust Implementation Types

```rust
#[derive(Debug, Clone, PartialEq)]
pub struct MunsellSpecification {
    pub hue: f64,           // 0.0-10.0
    pub family: String,     // "R", "YR", "Y", "GY", "G", "BG", "B", "PB", "P", "RP", "N"
    pub value: f64,         // 0.0-10.0 (lightness)
    pub chroma: f64,        // 0.0+ (saturation)
}

#[derive(Debug, Clone, PartialEq)]
pub struct CieXyY {
    pub x: f64,            // Chromaticity x
    pub y: f64,            // Chromaticity y  
    pub Y: f64,            // Luminance Y
}

pub struct MunsellRenotationData {
    entries: Vec<(MunsellSpecification, CieXyY)>,
    interpolator: RadialBasisInterpolator,
}
```

## Implementation Requirements

### Dependencies
- `palette` crate for color space conversions
- Radial basis function interpolation library
- High-precision floating point operations (f64)

### Constants Module
```rust
pub mod constants {
    pub const ILLUMINANT_C: [f64; 2] = [0.31006, 0.31616];
    pub const MG_OXIDE_REFLECTANCE: f64 = 0.975;
    pub const ASTM_D1535_COEFFICIENTS: [f64; 5] = [1.1914, -0.22533, 0.23352, -0.020484, 0.00081939];
    pub const ACHROMATIC_THRESHOLD: f64 = 1e-6;
    pub const NEWTON_RAPHSON_TOLERANCE: f64 = 1e-10;
    pub const NEWTON_RAPHSON_MAX_ITERATIONS: usize = 100;
}
```

### Error Handling
```rust
#[derive(thiserror::Error, Debug)]
pub enum MunsellError {
    #[error("Invalid RGB values: {0:?}")]
    InvalidRgb([u8; 3]),
    
    #[error("Invalid Munsell notation: {0}")]
    InvalidNotation(String),
    
    #[error("Color outside MacAdam limits: x={x}, y={y}")]
    OutsideMacAdamLimits { x: f64, y: f64 },
    
    #[error("Newton-Raphson convergence failed")]
    ConvergenceFailed,
    
    #[error("Interpolation error: {0}")]
    InterpolationError(String),
}
```

## Performance Considerations

- Pre-compute interpolation functions at initialization
- Cache frequently used calculations
- Use lookup tables for polynomial evaluations if needed
- Optimize for common cases (achromatic colors, primary hues)

## Validation Requirements

The implementation must achieve:
- **Mathematical Accuracy:** Match Python colour-science results within floating-point precision
- **Random Color Testing:** 100% agreement with reference implementation on arbitrary RGB inputs
- **Bidirectional Consistency:** Round-trip conversion accuracy (sRGB → Munsell → sRGB)
- **Edge Case Handling:** Proper behavior for out-of-gamut colors, achromatic colors, extreme values

## References

1. ASTM D1535-08e1 Standard Practice for Specifying Color by the Munsell System
2. Python colour-science library implementation
3. Munsell Renotation data (Newhall, Nickerson, and Judd, 1943)
4. CIE colorimetry standards for XYZ and xyY color spaces

---

# ISCC-NBS Classification System

## Overview

The ISCC-NBS (Inter-Society Color Council - National Bureau of Standards) color classification system provides standardized color names for colors in the Munsell color space. This system remains unchanged from the previous implementation.

## Hue Wedge Distribution Algorithm

The ISCC-NBS color classification uses a mechanical hue wedge distribution approach where polygons are systematically organized into adjacent hue planes for efficient lookup.

### Core Principles

#### 1. Mechanical Wedge Construction

**Reference Hue Sequence** (in order):
```
1R → 2R → 3R → 4R → 5R → 6R → 7R → 8R → 9R → 10R →
1YR → 2YR → 3YR → 4YR → 5YR → 6YR → 7YR → 8YR → 9YR → 10YR →
1Y → 2Y → 3Y → 4Y → 5Y → 6Y → 7Y → 8Y → 9Y → 10Y →
1GY → 2GY → 3GY → 4GY → 5GY → 6GY → 7GY → 8GY → 9GY → 10GY →
1G → 2G → 3G → 4G → 5G → 6G → 7G → 8G → 9G → 10G →
1BG → 2BG → 3BG → 4BG → 5BG → 6BG → 7BG → 8BG → 9BG → 10BG →
1B → 2B → 3B → 4B → 5B → 6B → 7B → 8B → 9B → 10B →
1PB → 2PB → 3PB → 4PB → 5PB → 6PB → 7PB → 8PB → 9PB → 10PB →
1P → 2P → 3P → 4P → 5P → 6P → 7P → 8P → 9P → 10P →
1RP → 2RP → 3RP → 4RP → 5RP → 6RP → 7RP → 8RP → 9RP → 10RP →
(wraps back to 1R)
```

#### 2. ISCC-NBS Descriptor Construction Rules

The `revised_descriptor` field combines the `revised_color` and `iscc_nbs_modifier` following specific ISCC-NBS standardized rules:

##### Rule 1: Basic Prefix Rule
```
modifier + color = descriptor
```
**Examples:**
- "vivid" + "red" = "vivid red"
- "light" + "blue" = "light blue"  
- "dark" + "green" = "dark green"

##### Rule 2: No Modifier Case
```
If iscc_nbs_modifier is None → revised_descriptor = revised_color
```

##### Rule 3: "-ish" Transformation Rules
When the modifier contains "-ish", apply color transformation with English grammar rules.

##### Rule 4: English "-ish" Grammar Transformations
- brown → brownish
- blue → bluish  
- red → reddish
- green → greenish
- yellow → yellowish
- purple → purplish
- pink → pinkish

##### Rule 5: "Olive" Exception
The color "olive" is never transformed with "-ish".

## Integration with Mathematical Munsell Conversion

The ISCC-NBS classification system will use the new mathematical Munsell conversion algorithm to:

1. Convert sRGB colors to accurate Munsell specifications
2. Use the Munsell hue/value/chroma coordinates to classify colors into ISCC-NBS categories
3. Apply the descriptor construction rules to generate standardized color names

This integration ensures that the ISCC-NBS system benefits from the improved mathematical accuracy of the new Munsell conversion algorithm.

---

## DEEP ANALYSIS: Python colour-science Algorithm

Based on comprehensive analysis of the Python colour-science library source code, I have extracted the complete algorithm. The implementation is significantly more complex than initially understood.

### Core Algorithm: `_xyY_to_munsell_specification`

This is the heart of the mathematical conversion. The algorithm uses an **iterative dual-loop convergence approach**:

#### Initial Setup
1. **MacAdam Limits Check**: Validates input xyY coordinates are within physically realizable limits
2. **Value Calculation**: Uses `munsell_value_ASTMD1535(Y * 100)` - direct ASTM polynomial
3. **Grey Threshold**: If chromaticity distance < `THRESHOLD_INTEGER = 1e-3`, return neutral color
4. **Initial Guess**: Uses Lab/LCHab conversion to generate starting Munsell specification

#### Dual Iteration Structure
```python
convergence_threshold = THRESHOLD_INTEGER / 1e4  # = 1e-7
iterations_maximum = 64  # Outer loop
iterations_maximum_inner = 16  # Inner loop
```

**Outer Loop**: Hue angle refinement (up to 64 iterations)
**Inner Loop**: Chroma magnitude refinement (up to 16 iterations)

#### Detailed Algorithm Steps

##### Step 1: Initial Guess Generation
```python
# Convert to Lab color space for initial estimate
XYZ = xyY_to_XYZ(xyY)
Lab = XYZ_to_Lab(XYZ, illuminant_reference)  
LCHab = Lab_to_LCHab(Lab)
hue_initial, _value_initial, chroma_initial, code_initial = LCHab_to_munsell_specification(LCHab)

# Scale chroma: (5 / 5.5) factor
specification_current = [hue_initial, value, (5/5.5) * chroma_initial, code_initial]
```

##### Step 2: Outer Iteration Loop (Hue Refinement)
For each outer iteration:

1. **Chroma Boundary Check**: 
   ```python
   chroma_maximum = maximum_chroma_from_renotation([hue_current, value, code_current])
   if chroma_current > chroma_maximum:
       chroma_current = chroma_maximum
   ```

2. **Current xyY Calculation**:
   ```python
   x_current, y_current, _Y_current = _munsell_specification_to_xyY(specification_current)
   ```

3. **Cylindrical Coordinate Conversion**:
   ```python
   rho_current, phi_current, _z_current = cartesian_to_cylindrical(
       [x_current - x_center, y_current - y_center, Y_center]
   )
   phi_current = np.degrees(phi_current)
   ```

4. **Inner Loop: Hue Angle Search** (up to 16 iterations):
   - Systematically vary hue angle until bracketing target direction
   - Uses angle differences and modular arithmetic for wrapping
   - Builds arrays for interpolation: `phi_differences_data`, `hue_angles_data`

5. **Linear Interpolation for Hue Correction**:
   ```python
   hue_angle_difference_new = Extrapolator(LinearInterpolator(phi_differences, hue_angles_differences))(0)
   hue_angle_new = (hue_angle_current + hue_angle_difference_new) % 360
   ```

##### Step 3: Chroma Magnitude Refinement
After hue correction, refine chroma magnitude:

1. **Inner Loop: Chroma Scaling** (up to 16 iterations):
   ```python
   chroma_inner = ((rho_input / rho_current) ** iterations_inner) * chroma_current
   ```

2. **Build Interpolation Data**: Collect rho/chroma pairs for boundaries

3. **Linear Interpolation for Chroma**:
   ```python
   chroma_new = LinearInterpolator(rho_bounds, chroma_bounds)(rho_input)
   ```

##### Step 4: Convergence Check
```python
difference = euclidean_distance([x, y], [x_current, y_current])
if difference < convergence_threshold:  # 1e-7
    return specification_current
```

### Critical Infrastructure Functions

#### 1. `_munsell_specification_to_xyY(specification)`
- Handles grey colors directly: returns Illuminant C coordinates
- For chromatic colors: Uses value-based interpolation
- **Key**: Calls `munsell_specification_to_xy()` for xy coordinates
- **Key**: Uses `luminance_ASTMD1535(value)` for Y coordinate
- Performs linear interpolation between integer value planes

#### 2. `munsell_specification_to_xy(specification)`
- **Critical**: This is where renotation data is accessed
- Rounds value to integer, handles chroma as even numbers only
- For exact matches: calls `xyY_from_renotation(specification)`
- For interpolation: calls `xy_from_renotation_ovoid(specification)`
- Performs linear interpolation between chroma boundaries

#### 3. `xy_from_renotation_ovoid(specification)`
- Handles direct renotation data access for standard hue angles (0, 2.5, 5, 7.5, 10)
- For intermediate hues: finds bounding hues using `bounding_hues_from_renotation()`
- **Selection Logic**: Uses `interpolation_method_from_renotation_ovoid()` to choose:
  - **"Linear"**: Direct interpolation in xy coordinates
  - **"Radial"**: Interpolation in cylindrical coordinates (rho, phi)
- Handles complex angle wrapping and boundary conditions

#### 4. `xyY_from_renotation(specification)`
- **Direct data access**: `MUNSELL_COLOURS_ALL[index][1]`
- Uses `np.isclose()` with tolerance to find exact matches
- Returns xyY coordinates for exact specification matches

### Data Structure: `MUNSELL_COLOURS_ALL`

Located in `/colour/notation/datasets/munsell/all.py`:
```python
MUNSELL_COLOURS_ALL: tuple = (
    (("2.5GY", 0.2, 2.0), np.array([0.7130, 1.4140, 0.2370])),
    (("5GY", 0.2, 2.0), np.array([0.4490, 1.1450, 0.2370])),
    # ... thousands of entries
)
```

**Format**: `((hue_family, value, chroma), [x, y, Y_scaled])`
**Scale Factor**: Y values are scaled by `1/0.975 ≈ 1.02568` (magnesium oxide reflectance)
**Illuminant**: All chromaticity coordinates assume CIE Illuminant C

### Critical Constants and Scaling

```python
THRESHOLD_INTEGER = 1e-3  # Grey detection threshold
convergence_threshold = 1e-7  # Iteration convergence
ILLUMINANT_C = [0.31006, 0.31616]  # CIE Illuminant C
MG_OXIDE_SCALE = 0.975  # Magnesium oxide reflectance factor
```

### Missing Datasets Analysis

The Python implementation has access to multiple datasets:
- `all.py`: Complete dataset including extrapolated colors
- `experimental.py`: Experimental measurements only  
- `real.py`: Real measurements only

**Current Analysis**: Only `all.py` is used in the main algorithm. The experimental and real datasets appear to be for research/validation purposes.

### CRITICAL FINDINGS

1. **No Simple Lookup**: The algorithm does NOT use simple lookup tables
2. **Pure Interpolation**: Uses sophisticated interpolation between renotation data points
3. **Iterative Convergence**: Dual-loop iterative refinement for precision
4. **Complex Coordinate Transforms**: Cylindrical coordinates for hue angle calculations
5. **Multiple Interpolation Methods**: "Linear" vs "Radial" based on color characteristics
6. **Initial Guess Sophistication**: Uses Lab/LCHab conversion for starting point

### IMPLEMENTATION REQUIREMENTS

To achieve 100% alignment with Python colour-science:

1. **Port Complete Algorithm**: Implement the full dual-loop iterative structure
2. **Import Full Dataset**: Use complete `MUNSELL_COLOURS_ALL` data
3. **Add Coordinate Transforms**: Implement cylindrical coordinate conversions
4. **Implement Interpolation Methods**: Both "Linear" and "Radial" approaches
5. **Add Missing Functions**: All helper functions for hue angles, boundaries, etc.

This is a complete mathematical interpolation system, not a lookup table approach. The complexity explains why achieving 100% accuracy requires implementing the exact algorithm structure.

### Additional Critical Functions Analyzed

#### 5. Coordinate Transformation Functions

**`cartesian_to_cylindrical([x, y, z])`**:
```python
def cartesian_to_cylindrical(a):
    rho, phi = cartesian_to_polar(a[..., 0:2])  # Use x,y for polar coordinates
    return [rho, phi, a[..., -1]]  # Keep z as-is

def cartesian_to_polar([x, y]):
    rho = np.hypot(x, y)  # sqrt(x² + y²)
    phi = np.arctan2(y, x)  # angle in radians [-π, π]
    return [rho, phi]
```

**Usage in Algorithm**:
- Converts chromaticity differences to polar coordinates for angle calculations
- `rho` = chromaticity distance from center point
- `phi` = angle in radians, converted to degrees for hue calculations
- Critical for hue angle interpolation and convergence detection

#### 6. Hue Angle Conversion Functions

**`hue_to_hue_angle([hue, code])`**:
```python
def hue_to_hue_angle(hue_and_code):
    hue, code = hue_and_code
    single_hue = ((17 - code) % 10 + (hue / 10) - 0.5) % 10
    
    # Mapping using specific angle breakpoints
    hue_angle = LinearInterpolator(
        [0, 2, 3, 4, 5, 6, 8, 9, 10], 
        [0, 45, 70, 135, 160, 225, 255, 315, 360]
    )(single_hue)
    
    return hue_angle
```

**`hue_angle_to_hue(hue_angle)`**:
```python
def hue_angle_to_hue(hue_angle):
    # Reverse mapping from angle to hue
    single_hue = LinearInterpolator(
        [0, 45, 70, 135, 160, 225, 255, 315, 360], 
        [0, 2, 3, 4, 5, 6, 8, 9, 10]
    )(hue_angle)
    
    # Determine hue family code based on single_hue ranges
    if single_hue <= 0.5: code = 7      # RP
    elif single_hue <= 1.5: code = 6    # R  
    elif single_hue <= 2.5: code = 5    # YR
    elif single_hue <= 3.5: code = 4    # Y
    elif single_hue <= 4.5: code = 3    # GY
    elif single_hue <= 5.5: code = 2    # G
    elif single_hue <= 6.5: code = 1    # BG
    elif single_hue <= 7.5: code = 10   # B
    elif single_hue <= 8.5: code = 9    # PB
    elif single_hue <= 9.5: code = 8    # P
    else: code = 7                      # RP (wraparound)
    
    hue = (10 * (single_hue % 1) + 5) % 10
    if hue == 0: hue = 10
    
    return [hue, code]
```

**Critical Constants**:
- **Hue Family Codes**: {1:BG, 2:G, 3:GY, 4:Y, 5:YR, 6:R, 7:RP, 8:P, 9:PB, 10:B}
- **Angle Breakpoints**: Non-linear mapping with specific angles for each hue transition
- **Wraparound Logic**: Handles 360° → 0° transition properly

### COMPLETE INTERPOLATION INFRASTRUCTURE

#### 7. `interpolation_method_from_renotation_ovoid(specification)`

This function contains **MASSIVE** logic for determining whether to use "Linear" or "Radial" interpolation based on detailed value/chroma/ASTM_hue range criteria:

**Structure**:
1. **Grey Check**: If grey color → return None (no interpolation)
2. **Standard Hue Check**: If hue is exact multiple of 2.5 → return None (direct lookup)
3. **Value-Specific Logic**: Complex cascading rules for each value from 1-10

**Key Patterns**:
- **Value 1**: Different ASTM_hue ranges for each chroma (2,4,6,8,10+) 
- **Value 2**: Similar pattern with slightly different ranges
- **Values 3-9**: Each has specific ASTM_hue range criteria for Radial vs Linear
- **Value 10**: Ideal white → return None

**Example Rules (Value=5)**:
```python
if chroma == 2:
    if 5 < ASTM_hue < 37.5 or 55 < ASTM_hue < 85:
        interpolation_method = 2  # "Radial"
    else:
        interpolation_method = 1  # "Linear"
elif chroma in (4, 6, 8):
    if 2.5 < ASTM_hue < 42.5 or 55 < ASTM_hue < 85:
        interpolation_method = 2  # "Radial"
    else:
        interpolation_method = 1  # "Linear"
```

**Critical Finding**: This is **NOT** a simple heuristic - it's a detailed empirical lookup table with specific ranges for every combination of value/chroma/ASTM_hue that determines the optimal interpolation method.

#### 8. `xy_from_renotation_ovoid(specification)`

**Purpose**: Convert Munsell specification to xy chromaticity coordinates using interpolation

**Algorithm Steps**:
1. **Direct Lookup Check**: If hue is 0, 2.5, 5, 7.5, or 10 → use `xyY_from_renotation` directly
2. **Bounding Hues**: Find clockwise/counterclockwise hue boundaries using `bounding_hues_from_renotation`
3. **Coordinate Conversion**: Convert boundary coordinates to cylindrical for angle calculations
4. **Hue Angle Mapping**: Use `hue_to_hue_angle` for all three hues (lower, target, upper)
5. **Angle Wrapping**: Handle 360° wraparound with complex logic
6. **Interpolation Method Selection**: Call `interpolation_method_from_renotation_ovoid`
7. **Interpolation Execution**:
   - **"Linear"**: Direct xy coordinate interpolation
   - **"Radial"**: Cylindrical coordinate (rho, phi) interpolation

**Key Code Sections**:
```python
# Cylindrical conversion for boundary points
rho_minus, phi_minus, _z_minus = cartesian_to_cylindrical(
    [x_minus - x_grey, y_minus - y_grey, Y_minus]
)

# Angle wrapping logic
if phi_minus - phi_plus > 180:
    phi_plus += 360

# Interpolation method execution
if interpolation_method == "Linear":
    x = LinearInterpolator(hue_angle_lower_upper, x_minus_plus)(hue_angle)
    y = LinearInterpolator(hue_angle_lower_upper, y_minus_plus)(hue_angle)
elif interpolation_method == "Radial":
    rho = LinearInterpolator(hue_angle_lower_upper, rho_minus_plus)(hue_angle)
    phi = LinearInterpolator(hue_angle_lower_upper, phi_minus_plus)(hue_angle)
    x, y = polar_to_cartesian([rho, radians(phi)]) + [x_grey, y_grey]
```

#### 9. `bounding_hues_from_renotation([hue, code])`

**Purpose**: Find the two standard hues that bound a given intermediate hue

**Logic**:
- If hue is exact multiple of 2.5 → return same hue for both bounds
- If hue = 0 → special case: hue_cw = 10, code_cw = (code + 1) % 10  
- Otherwise: hue_cw = floor(hue/2.5) * 2.5, hue_ccw = hue_cw + 2.5
- Handle wraparound: if hue_ccw = 0 → hue_ccw = 10

**Example**: `bounding_hues_from_renotation([3.2, 4])` → `[[2.5, 4], [5.0, 4]]`

#### 10. `maximum_chroma_from_renotation([hue, value, code])`

**Purpose**: Return maximum achievable chroma for given hue/value combination

**Algorithm**:
1. **Ideal White Check**: If value ≥ 9.99 → return 0
2. **Value Boundaries**: If value is integer → use same value, else use floor/ceil
3. **Hue Boundaries**: Get bounding hues using `bounding_hues_from_renotation`
4. **Cache Lookup**: Access `_munsell_maximum_chromas_from_renotation()` cached data
5. **Interpolation**: Use bilinear interpolation between boundary points

### PRECISE ASTM D1535 IMPLEMENTATION

#### 11. `luminance_ASTMD1535(V)`

**Exact Implementation**:
```python
def luminance_ASTMD1535(V):
    V = to_domain_10(V)  # Scale to [0,10] if needed
    
    Y = (1.1914 * V
         - 0.22533 * (V**2)
         + 0.23352 * (V**3)
         - 0.020484 * (V**4)
         + 0.00081939 * (V**5))
    
    return from_range_100(Y)  # Scale from [0,100] if needed
```

**Critical**: This is the **EXACT** ASTM D1535 polynomial used by Python colour-science.

#### 12. `munsell_value_ASTMD1535(Y)`

**Implementation**: Uses cached interpolator built from inverse lookup table:
```python
def _munsell_value_ASTMD1535_interpolator():
    munsell_values = np.arange(0, 10, 0.001)  # 0.001 precision
    interpolator = LinearInterpolator(
        luminance_ASTMD1535(munsell_values), munsell_values  # Y→V lookup
    )
    return Extrapolator(interpolator)
```

**Usage**: `V = _munsell_value_ASTMD1535_interpolator()(Y * 100)`

### COORDINATE TRANSFORMATION FUNCTIONS

#### 13. `cartesian_to_cylindrical([x, y, z])`

**Exact Implementation**:
```python
def cartesian_to_cylindrical(a):
    rho, phi = cartesian_to_polar(a[..., 0:2])  # Use first 2 coordinates
    return [rho, phi, a[..., -1]]  # Keep z unchanged

def cartesian_to_polar([x, y]):
    rho = np.hypot(x, y)  # sqrt(x² + y²)
    phi = np.arctan2(y, x)  # angle in radians [-π, π]
    return [rho, phi]
```

**Usage in Algorithm**: Converts chromaticity differences (x-x_center, y-y_center) to polar coordinates for angle-based interpolation and hue calculations.

## COMPLETE LINE-BY-LINE ANALYSIS OF PYTHON IMPLEMENTATION

### Critical Constants (VERIFIED)
- **THRESHOLD_INTEGER**: `1e-3` (0.001) - NOT 1e-10 as we implemented!
- **convergence_threshold**: `1e-7` (THRESHOLD_INTEGER / 1e4)
- **iterations_maximum**: 64 (outer loop)
- **iterations_maximum_inner**: 16 (both hue and chroma inner loops)

### Critical Algorithm Details Found

#### 1. Achromatic Detection (lines 1081-1083)
```python
grey_threshold = THRESHOLD_INTEGER  # 1e-3
if rho_input < grey_threshold:
    return from_range_10(normalise_munsell_specification(value))
```
**BUG IN OUR CODE**: We check against 1e-10, should be 1e-3

#### 2. Normalization Rules

##### normalise_munsell_specification (lines 1576-1583)
```python
if hue == 0:
    # 0YR is equivalent to 10R
    hue, code = 10, (code + 1) % 10

if chroma == 0:
    return [np.nan, value, np.nan, np.nan]  # Achromatic
```
**MISSING IN OUR CODE**: Both normalization rules

##### hue_angle_to_hue (lines 1945-1947)
```python
hue = (10 * (single_hue % 1) + 5) % 10
if hue == 0:
    hue = 10
```
**MISSING IN OUR CODE**: The hue==0 → 10 conversion

#### 3. Chroma Interpolation (line 1310)
```python
chroma_new = LinearInterpolator(rho_bounds, chroma_bounds)(rho_input)
```
**DIFFERENCE**: Python uses LinearInterpolator (no extrapolation), we use linear_interpolate which extrapolates

#### 4. Chroma Exponential Scaling (lines 1276-1279)
```python
with sdiv_mode():
    chroma_inner = ((rho_input / rho_current) ** iterations_inner) * chroma_current
```
**VERIFIED**: We implement this correctly

#### 5. Inner Loop Conditions

##### Hue Loop (lines 1150-1153)
```python
while (np.sign(np.min(phi_differences_data)) == np.sign(np.max(phi_differences_data)) 
       and extrapolate is False):
```
**VERIFIED**: We implement this correctly

##### Chroma Loop (line 1268)
```python
while not (np.min(rho_bounds_data) < rho_input < np.max(rho_bounds_data)):
```
**VERIFIED**: We implement this correctly

#### 6. Extrapolation Enable (lines 1187-1188)
```python
if len(phi_differences_data) >= 2:
    extrapolate = True
```
**DIFFERENCE**: Python enables after 2 points, we check for sign change OR 4 points

## TODO Tasks for Complete Implementation

### Deep Analysis Phase
- [x] **CRITICAL**: Deep dive into Python colour-science `_xyY_to_munsell_specification` function
  - [x] Extract exact iterative algorithm with convergence criteria
  - [x] Understand initial guess generation using Lab/LCHab conversion  
  - [x] Document dual iteration loops (outer: hue adjustment, inner: chroma refinement)
  - [x] Map all helper functions: `_munsell_specification_to_xyY`, `xy_from_renotation_ovoid`, etc.

- [x] **CRITICAL**: Analyze Munsell renotation data usage
  - [x] Understand `MUNSELL_COLOURS_ALL` vs `experimental.py` vs `real.py` datasets
  - [x] Document exact interpolation methods: "Linear" vs "Radial" selection logic
  - [x] Extract `xyY_from_renotation` direct lookup approach
  - [x] Map cylindrical coordinate transformations for hue wrapping

- [x] **CRITICAL**: Study interpolation infrastructure
  - [x] Document `LinearInterpolator` and `Extrapolator` usage patterns
  - [x] Understand `cartesian_to_cylindrical` coordinate transformations
  - [x] Extract `hue_to_hue_angle` and `hue_angle_to_hue` conversion logic
  - [x] Document `maximum_chroma_from_renotation` boundary checking

- [x] **CRITICAL**: Understand algorithm precision requirements  
  - [x] Extract exact convergence thresholds: `THRESHOLD_INTEGER / 1e4 = 1e-7`
  - [x] Document iteration limits: 64 outer, 16 inner max iterations
  - [x] Understand extrapolation vs interpolation decision logic
  - [x] Map MacAdam limit checking and error handling

### Implementation Phase  
- [ ] **CRITICAL**: Implement exact Python algorithm in Rust
  - [ ] Port complete iterative algorithm structure
  - [ ] Implement proper initial guess using Lab/LCHab → Munsell conversion
  - [ ] Add dual iteration loops with exact convergence logic
  - [ ] Ensure 100% mathematical alignment with Python results

- [ ] **CRITICAL**: Build renotation data infrastructure
  - [ ] Import exact `MUNSELL_COLOURS_ALL` dataset (not simplified version)
  - [ ] Implement `xyY_from_renotation` direct lookup with tolerance matching
  - [ ] Add `bounding_hues_from_renotation` for interpolation bounds
  - [ ] Create `interpolation_method_from_renotation_ovoid` logic

- [ ] **CRITICAL**: Add missing coordinate transformations
  - [ ] Implement `cartesian_to_cylindrical` for hue angle calculations
  - [ ] Add proper hue angle wrapping with 360° modular arithmetic
  - [ ] Create `hue_to_hue_angle` and reverse conversion functions
  - [ ] Add chromatic adaptation between D65 and Illuminant C

- [ ] **CRITICAL**: Implement interpolation methods
  - [ ] Add "Linear" interpolation for direct hue angle mapping
  - [ ] Implement "Radial" interpolation using cylindrical coordinates  
  - [ ] Create `LinearInterpolator` equivalent for boundary interpolation
  - [ ] Add extrapolation logic for out-of-bounds colors

### Validation Phase
- [ ] **CRITICAL**: Achieve 100% Python alignment
  - [ ] Test identical results on random RGB colors
  - [ ] Validate exact decimal precision matching
  - [ ] Ensure convergence behavior matches Python exactly
  - [ ] Test edge cases: achromatic colors, MacAdam limits, extrapolation

- [ ] **FINAL**: Clean up and optimize
  - [ ] Remove old lookup table approach completely
  - [ ] Optimize mathematical operations for performance
  - [ ] Add comprehensive error handling
  - [ ] Complete documentation with algorithm references