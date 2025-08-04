# Systematic Line-by-Line Analysis of xyY_to_munsell Algorithm

## Overview
This document provides a complete, systematic analysis of the Python colour-science xyY_to_munsell implementation, comparing it with our Rust implementation to identify all discrepancies.

## Part 1: Input Processing and Initial Setup

### Python Implementation (lines 1050-1082)
```python
def xyY_to_munsell_specification(xyY):
    # Input validation and setup
    xyY = as_float_array(xyY)
    x, y, Y = tsplit(xyY)
    
    # Value calculation (line 1068)
    value = munsell_value(Y, method="ASTM D1535")
    
    # Integer value check (line 1070-1071)
    if is_integer(value):
        value = np.around(value)
    
    # Get achromatic center for this value (line 1074)
    x_center, y_center, Y_center = tsplit(_munsell_specification_to_xyY(value))
    
    # Calculate rho and phi relative to achromatic center (lines 1076-1079)
    rho_input, phi_input, _z_input = tsplit(
        cartesian_to_cylindrical([x - x_center, y - y_center, Y_center])
    )
    phi_input = np.degrees(phi_input)
    
    # Achromatic check (lines 1081-1083)
    grey_threshold = THRESHOLD_INTEGER  # 1e-3
    if rho_input < grey_threshold:
        return from_range_10(normalise_munsell_specification(value))
```

### Critical Details:
1. **Achromatic Center**: `_munsell_specification_to_xyY(value)` returns Illuminant C coordinates `[0.31006, 0.31616, Y]` for achromatic colors
2. **Integer Rounding**: If value is close to integer (within float precision), round it
3. **Achromatic Return**: Uses `normalise_munsell_specification` which handles special cases

### Rust Implementation Issues Found:
1. ✅ FIXED: We were checking achromatic relative to D65, not value-specific center
2. ❌ MISSING: Integer value rounding (if value is close to integer, round it)
3. ❌ MISSING: The achromatic return doesn't use `normalise_munsell_specification`
4. ❌ WRONG: Our achromatic center calculation might be wrong

## Part 2: Initial Guess Generation

### Python Implementation (lines 1085-1103)
```python
    # Convert to XYZ (line 1085)
    XYZ = xyY_to_XYZ(xyY)
    
    # Create reference white at same luminance (lines 1090-1093)
    XYZ_w = full(3, luminance(xyY))  # Creates [Y, Y, Y]
    XYZ_w[..., 0:2] = (
        luminance(xyY)[..., np.newaxis] / CCS_ILLUMINANT_MUNSELL[1]
    ) * CCS_ILLUMINANT_MUNSELL[0:2]
    # This creates: XYZ_w = [Y * x_c/y_c, Y, Y * z_c/y_c]
    
    # Convert to Lab using Illuminant C reference (line 1096)
    Lab = XYZ_to_Lab(XYZ, XYZ_w)
    LCHab = Lab_to_LCH(Lab)
    
    # Convert LCHab hue to Munsell (lines 1099-1103)
    hue_initial, code = LCHab_to_munsell_specification(LCHab)
    chroma_initial = LCHab[..., 1] / 5
    chroma_initial *= 5 / 5.5  # Convergence factor
    specification = tstack([hue_initial, value, chroma_initial, code])
```

### Critical Finding:
The reference white `XYZ_w` is CUSTOM for each color based on its luminance Y:
- X_w = Y * (0.31006 / 0.31616) 
- Y_w = Y 
- Z_w = Y * ((1 - 0.31006 - 0.31616) / 0.31616)

This is NOT the standard Illuminant C white point! It's scaled by the input luminance.

### Rust Implementation Issues Found:
1. ❌ CRITICAL: We're using palette's standard Illuminant C, not a custom scaled reference
2. ❌ MISSING: Custom XYZ_w calculation based on input luminance

## Part 3: Main Iterative Loop Structure

### Python Implementation (lines 1106-1331)

#### Outer Loop Setup (lines 1106-1109)
```python
convergence_threshold = THRESHOLD_INTEGER / 1e4  # 1e-3 / 1e4 = 1e-7
iterations_maximum = 64
iterations = 0
```

#### Main Outer Loop (lines 1110-1331)
```python
while iterations <= iterations_maximum:
    iterations += 1
    
    # Unpack current specification (lines 1113-1119)
    hue_current, _value_current, chroma_current, code_current = specification_current
    hue_angle_current = hue_to_hue_angle([hue_current, code_current])
    
    # Check and cap chroma at maximum (lines 1121-1125)
    chroma_maximum = maximum_chroma_from_renotation([hue_current, value, code_current])
    if chroma_current > chroma_maximum:
        chroma_current = specification_current[2] = chroma_maximum
```

### First Inner Loop: Hue Refinement (lines 1127-1234)

Purpose: Find the correct hue angle by iterating until phi differences bracket zero.

```python
# Calculate current position relative to achromatic center (lines 1127-1141)
x_current, y_current, _Y_current = _munsell_specification_to_xyY(specification_current)
rho_current, phi_current, _z_current = cartesian_to_cylindrical(
    [x_current - x_center, y_current - y_center, Y_center]
)
phi_current = np.degrees(phi_current)
phi_current_difference = (360 - phi_input + phi_current) % 360
if phi_current_difference > 180:
    phi_current_difference -= 360

# Initialize inner loop data (lines 1142-1148)
phi_differences_data = [phi_current_difference]
hue_angles_differences_data = [0]
hue_angles = [hue_angle_current]
iterations_maximum_inner = 16
iterations_inner = 0
extrapolate = False

# Inner loop: Find bracketing hue angles (lines 1150-1203)
while (np.sign(np.min(phi_differences_data)) == np.sign(np.max(phi_differences_data)) 
       and extrapolate is False):
    iterations_inner += 1
    
    # Calculate new hue angle (lines 1166-1174)
    hue_angle_inner = (hue_angle_current + iterations_inner * (phi_input - phi_current)) % 360
    hue_angle_difference_inner = (iterations_inner * (phi_input - phi_current)) % 360
    if hue_angle_difference_inner > 180:
        hue_angle_difference_inner -= 360
    
    # Convert to hue specification (line 1175)
    hue_inner, code_inner = hue_angle_to_hue(hue_angle_inner)
    
    # Get position for this hue (lines 1177-1185)
    x_inner, y_inner, _Y_inner = _munsell_specification_to_xyY(
        [hue_inner, value, chroma_current, code_inner]
    )
    
    # Enable extrapolation after 2 points (lines 1187-1188)
    if len(phi_differences_data) >= 2:
        extrapolate = True
    
    # If not extrapolating, calculate and store phi difference (lines 1190-1201)
    if extrapolate is False:
        rho_inner, phi_inner, _z_inner = cartesian_to_cylindrical(
            [x_inner - x_center, y_inner - y_center, Y_center]
        )
        phi_inner = np.degrees(phi_inner)
        phi_inner_difference = (360 - phi_input + phi_inner) % 360
        if phi_inner_difference > 180:
            phi_inner_difference -= 360
        
        phi_differences_data.append(phi_inner_difference)
        hue_angles.append(hue_angle_inner)
        hue_angles_differences_data.append(hue_angle_difference_inner)
```

#### Hue Interpolation/Extrapolation (lines 1204-1234)
```python
# Sort by phi differences (lines 1204-1209)
phi_differences = np.array(phi_differences_data)
hue_angles_differences = np.array(hue_angles_differences_data)
phi_differences_indexes = phi_differences.argsort()
phi_differences = phi_differences[phi_differences_indexes]
hue_angles_differences = hue_angles_differences[phi_differences_indexes]

# Extrapolate to find hue angle at phi_difference = 0 (lines 1211-1217)
hue_angle_difference_new = (
    Extrapolator(LinearInterpolator(phi_differences, hue_angles_differences))(0) % 360
)
hue_angle_new = (hue_angle_current + hue_angle_difference_new) % 360

# Update specification with new hue (lines 1219-1220)
hue_new, code_new = hue_angle_to_hue(hue_angle_new)
specification_current = [hue_new, value, chroma_current, code_new]

# Check convergence (lines 1222-1234)
x_current, y_current, _Y_current = _munsell_specification_to_xyY(specification_current)
chroma_scale = 50 if get_domain_range_scale() == "1" else 2
difference = euclidean_distance([x, y], [x_current, y_current])
if difference < convergence_threshold:
    return from_range_10(
        np.array(specification_current),
        np.array([10, 10, chroma_scale, 10])
    )
```

### Second Inner Loop: Chroma Refinement (lines 1236-1324)

Purpose: Find the correct chroma by iterating until rho bounds bracket the input rho.

```python
# Check and cap chroma again (lines 1237-1252)
hue_current, _value_current, chroma_current, code_current = specification_current
chroma_maximum = maximum_chroma_from_renotation([hue_current, value, code_current])
if chroma_current > chroma_maximum:
    chroma_current = specification_current[2] = chroma_maximum

# Calculate current rho (lines 1254-1261)
x_current, y_current, _Y_current = _munsell_specification_to_xyY(specification_current)
rho_current, phi_current, _z_current = cartesian_to_cylindrical(
    [x_current - x_center, y_current - y_center, Y_center]
)

# Initialize bounds (lines 1263-1267)
rho_bounds_data = [rho_current]
chroma_bounds_data = [chroma_current]
iterations_maximum_inner = 16
iterations_inner = 0

# Inner loop: Find bracketing rho values (lines 1268-1301)
while not (np.min(rho_bounds_data) < rho_input < np.max(rho_bounds_data)):
    iterations_inner += 1
    
    # Calculate new chroma using power scaling (lines 1276-1279)
    with sdiv_mode():  # Safe division mode
        chroma_inner = ((rho_input / rho_current) ** iterations_inner) * chroma_current
    
    # Cap at maximum chroma (lines 1281-1282)
    if chroma_inner > chroma_maximum:
        chroma_inner = specification_current[2] = chroma_maximum
    
    # Calculate rho for this chroma (lines 1284-1298)
    specification_inner = [hue_current, value, chroma_inner, code_current]
    x_inner, y_inner, _Y_inner = _munsell_specification_to_xyY(specification_inner)
    rho_inner, phi_inner, _z_inner = cartesian_to_cylindrical(
        [x_inner - x_center, y_inner - y_center, Y_center]
    )
    
    # Store bounds (lines 1300-1301)
    rho_bounds_data.append(rho_inner)
    chroma_bounds_data.append(chroma_inner)
```

#### Chroma Interpolation (lines 1303-1324)
```python
# Sort by rho (lines 1303-1309)
rho_bounds = np.array(rho_bounds_data)
chroma_bounds = np.array(chroma_bounds_data)
rhos_bounds_indexes = rho_bounds.argsort()
rho_bounds = rho_bounds[rhos_bounds_indexes]
chroma_bounds = chroma_bounds[rhos_bounds_indexes]

# Linear interpolation for final chroma (line 1310)
chroma_new = LinearInterpolator(rho_bounds, chroma_bounds)(rho_input)

# Update specification and check convergence (lines 1312-1324)
specification_current = [hue_current, value, chroma_new, code_current]
x_current, y_current, _Y_current = _munsell_specification_to_xyY(specification_current)
difference = euclidean_distance([x, y], [x_current, y_current])
if difference < convergence_threshold:
    return from_range_10(
        np.array(specification_current),
        np.array([10, 10, chroma_scale, 10])
    )
```

### Critical Details Found:

1. **Extrapolation vs Interpolation**:
   - Hue uses `Extrapolator(LinearInterpolator(...))` to find zero crossing
   - Chroma uses plain `LinearInterpolator(...)` without extrapolation
   - Extrapolation is enabled after 2 points (`len(phi_differences_data) >= 2`)

2. **Angle Wraparound Handling**:
   - Multiple modulo 360 operations
   - Conversion to [-180, 180] range when difference > 180

3. **Chroma Capping**:
   - Chroma is capped at maximum TWICE per outer iteration (before each inner loop)
   - Uses `maximum_chroma_from_renotation` function

4. **Power Scaling for Chroma**:
   - Formula: `chroma_inner = ((rho_input / rho_current) ** iterations_inner) * chroma_current`
   - Uses `sdiv_mode()` context for safe division

5. **Convergence Check**:
   - Euclidean distance between input (x,y) and current (x,y)
   - Threshold: 1e-7 (THRESHOLD_INTEGER / 1e4)
   - Checked after EACH inner loop (not just at end of outer loop)

### Rust Implementation Issues Found:
1. ❌ MISSING: Chroma is not capped TWICE per iteration
2. ❌ WRONG: We use Extrapolator for chroma (should be LinearInterpolator only)
3. ❌ MISSING: Safe division context for power scaling
4. ✅ CORRECT: Convergence checks after each inner loop
5. ✅ CORRECT: Angle wraparound handling

## Part 4: Normalization and Final Output

### Python Implementation - `normalise_munsell_specification` (lines 1547-1583)

This function handles special cases for the final output:

```python
def normalise_munsell_specification(specification):
    specification = as_float_array(specification)
    
    # Check if it's a grey/achromatic color
    if is_grey_munsell_colour(specification):
        # Return [nan, value, nan, nan] for greys
        return specification * np.array([np.nan, 1, np.nan, np.nan])
    else:
        hue, value, chroma, code = specification
        
        # CRITICAL: 0YR is equivalent to 10R (lines 1576-1578)
        if hue == 0:
            hue, code = 10, (code + 1) % 10
        
        # CRITICAL: Chroma == 0 returns achromatic (lines 1580-1581)
        if chroma == 0:
            return tstack([np.nan, value, np.nan, np.nan])
        else:
            return tstack([hue, value, chroma, code])
```

### `is_grey_munsell_colour` (lines 1518-1544)

```python
def is_grey_munsell_colour(specification):
    specification = as_float_array(specification)
    # Remove NaN values and check if what remains is a single number
    specification = np.squeeze(specification[~np.isnan(specification)])
    return is_numeric(as_float(specification))
```

This returns True if the specification contains only a value (all other components are NaN).

### Critical Normalization Rules:

1. **Grey/Achromatic Colors**:
   - Input: Any specification where only value is non-NaN
   - Output: `[nan, value, nan, nan]`

2. **0YR → 10R Conversion**:
   - If hue == 0, convert to hue=10 and increment family code
   - Example: `0YR` becomes `10R`

3. **Zero Chroma → Achromatic**:
   - If chroma == 0 (regardless of hue), return `[nan, value, nan, nan]`
   - This makes it achromatic even if it has a hue

### `from_range_10` Final Scaling (lines 1231-1234, 1321-1324)

```python
chroma_scale = 50 if get_domain_range_scale() == "1" else 2
return from_range_10(
    np.array(specification_current),
    np.array([10, 10, chroma_scale, 10])
)
```

The `from_range_10` function divides each component by its scale factor:
- Hue: divided by 10 (range 0-10 → 0-1)
- Value: divided by 10 (range 0-10 → 0-1)
- Chroma: divided by 50 or 2 depending on domain range scale
- Code: divided by 10 (but code is typically 0-9)

### Rust Implementation Issues Found:
1. ❌ CRITICAL: We don't have the 0YR → 10R conversion
2. ❌ CRITICAL: We don't handle chroma==0 → achromatic conversion
3. ❌ MISSING: Final output scaling with `from_range_10`
4. ❌ MISSING: Domain range scale handling for chroma

## Part 5: Critical Helper Functions

### `munsell_specification_to_xy` (lines 2573-2632)

This function returns the chromaticity coordinates for a Munsell specification:

```python
def munsell_specification_to_xy(specification):
    specification = normalise_munsell_specification(specification)
    
    # CRITICAL: Grey colors return Illuminant C coordinates
    if is_grey_munsell_colour(specification):
        return CCS_ILLUMINANT_MUNSELL  # [0.31006, 0.31616]
```

**Key Finding**: ANY achromatic color returns Illuminant C coordinates `[0.31006, 0.31616]`

### `_munsell_specification_to_xyY` (lines 848-925)

For achromatic colors (line 865-867):
```python
if is_grey_munsell_colour(specification):
    # ... calculations ...
    # Returns [0.31006, 0.31616, Y]
```

This confirms that:
1. Achromatic center for ANY value is always Illuminant C coordinates
2. The function returns `[0.31006, 0.31616, Y]` for achromatic specifications

### Key Constants

From earlier in the file:
```python
CCS_ILLUMINANT_MUNSELL = np.array([0.31006, 0.31616])  # Illuminant C
THRESHOLD_INTEGER = 1e-3  # Achromatic threshold
```

## Part 7: Palette vs Python Function Equivalence

### Color Space Conversions

| Python colour-science | Rust palette | Notes |
|-----------------------|--------------|--------|
| `xyY_to_XYZ` | `Yxy::into_color::<Xyz>` | ✅ Standard conversion |
| `XYZ_to_xyY` | `Xyz::into_color::<Yxy>` | ✅ Standard conversion |
| `XYZ_to_Lab` | `Lab::from_color(xyz)` | ❌ CRITICAL DIFFERENCE - Python uses custom XYZ_w |
| `Lab_to_LCH` | `Lch::from_color(lab)` | ✅ Standard conversion |
| `cartesian_to_cylindrical` | Manual calculation | ✅ Can be done with atan2 |
| `euclidean_distance` | Manual calculation | ✅ Simple sqrt(dx² + dy²) |

### Critical Difference in Lab Conversion:

**Python Implementation**:
```python
# Custom reference white scaled by luminance Y
XYZ_w = full(3, luminance(xyY))  # [Y, Y, Y]
XYZ_w[..., 0:2] = (luminance(xyY) / CCS_ILLUMINANT_MUNSELL[1]) * CCS_ILLUMINANT_MUNSELL[0:2]
# Results in: XYZ_w = [Y * 0.31006/0.31616, Y, Y * (1-0.31006-0.31616)/0.31616]
Lab = XYZ_to_Lab(XYZ, XYZ_w)  # Uses custom reference
```

**Rust palette (INCORRECT)**:
```rust
// Uses standard Illuminant C, not scaled by Y
let lab = Lab::<IlluminantC, f64>::from_color(xyz);
```

**Fix Required**: We need to implement custom Lab conversion with Y-scaled reference white.

## Part 8: Summary of Critical Implementation Differences

### Major Architectural Issues:

1. **Custom Reference White for Lab Conversion**:
   - Python: `XYZ_w = [Y * 0.31006/0.31616, Y, Y * (1-0.31006-0.31616)/0.31616]`
   - Rust: Using standard Illuminant C (not scaled by Y)

2. **Achromatic Detection**:
   - Python: Checks rho relative to value-specific achromatic center (always Illuminant C)
   - Rust: Was checking relative to D65 (now fixed but not working)

3. **Normalization Rules**:
   - Python: 0YR → 10R conversion, chroma==0 → achromatic
   - Rust: Missing these critical normalizations

4. **Interpolation Strategy**:
   - Python: Extrapolator for hue, LinearInterpolator for chroma
   - Rust: Using Extrapolator for both (incorrect)

5. **Chroma Capping**:
   - Python: Caps chroma TWICE per outer iteration
   - Rust: Only caps once

### Minor But Important Details:

1. **Integer Value Rounding**: If value is close to integer, round it
2. **Safe Division Context**: Python uses `sdiv_mode()` for power scaling
3. **Final Output Scaling**: Python uses `from_range_10` with domain-specific scales
4. **Extrapolation Trigger**: Enabled after 2 points, not 4

### Constants Verification:
- ✅ THRESHOLD_INTEGER = 1e-3 (achromatic threshold)
- ✅ CONVERGENCE_THRESHOLD = 1e-7 (1e-3 / 1e4)
- ✅ CCS_ILLUMINANT_MUNSELL = [0.31006, 0.31616]
- ✅ Iterations: 64 outer, 16 inner