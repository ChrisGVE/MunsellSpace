# Munsell Color Space Conversion Algorithm Specification

## Overview

This document provides the complete, authoritative specification for converting between sRGB and Munsell color notations using mathematical methods, plus the ISCC-NBS color classification system. The mathematical algorithm is based on the Python colour-science library implementation and follows ASTM D1535 standards.

**Version**: 4.0  
**Date**: 2025-01-09  
**Status**: Complete specification including ISCC-NBS mechanical wedge system and descriptor construction

## 1. Complete Color Pipeline

### 1.1 Mathematical Conversion Pipeline
```
sRGB [0-255] → Linear RGB [0-1] → XYZ (D65) → xyY → Munsell Specification → Munsell Notation
```

### 1.2 ISCC-NBS Classification Pipeline  
```
Hex/sRGB/Lab → Munsell Color → ISCC-NBS Color Classification → Descriptors
```

---

# PART I: ISCC-NBS COLOR CLASSIFICATION SYSTEM

## Algorithm 1: Mechanical Wedge System for Polygon Distribution

### Overview
The ISCC-NBS system uses polygonal regions in Munsell Value-Chroma space to define color categories. To optimize classification performance, polygons are distributed across mechanical wedges based on Munsell hue ranges.

### 1.1 Polygon Structure from CSV
- **Coordinate System**: Chroma/Value coordinates with 90°/270° angles only
- **Polygon Closure**: Last point connects to first point to close polygon
- **Multi-Hue Spanning**: Polygons span multiple Munsell hue wedges with potentially different shapes
- **Point Numbering Format**: `#.#` where integer = polygon number, decimal = point number
  - Example: `1.1, 1.2, 1.3, 1.4` (4 points of polygon 1), `2.1, 2.2, 2.3` (3 points of polygon 2)

### 1.2 Wedge System Architecture
- **Wedge Definition**: One map per hue wedge `[n, n+1)R` where n ∈ {0,1,2,...,9}
- **Complete Coverage**: Wedges include `[0,1)R`, `[1,2)R`, `[2,3)R`, ..., `[9,10)R`
- **Wraparound**: `[9,10)R` connects to `[0,1)R` (10R = 0R cyclically)
- **Polygon Distribution**: If polygon spans "1R to 4R", create copies in wedges 1R, 2R, 3R

### 1.3 Multi-Polygon Color Support
- **Single Polygon**: Most colors have 1 polygon only
- **Multi-Polygon**: Some colors have 2+ polygons for complex shapes
- **Validation Rule**: All points of same polygon MUST have identical hue range
- **Data Error**: If polygon points have different hue ranges → invalid data

### 1.4 Achromatic Color Mapping (Outside Polygon System)
Special handling for neutral colors using value-based intervals:
- **N[0.0, 2.5]** → Color 267 (Black)
- **N(2.5, 4.5]** → Color 266  
- **N(4.5, 6.5]** → Color 265
- **N(6.5, 8.5]** → Color 264
- **N(8.5, 10.0]** → Color 263 (White)

### 1.5 Classification Process
**Input**: Munsell Color `1.2R 6.7/12.5`

1. **Hue Wedge Selection**: `1.2R` → `1R wedge [1,2)R`
2. **Point-in-Polygon Testing**: Check point `(6.7, 12.5)` against all polygons in wedge
3. **Result**: Return color number (1-267) with associated descriptor strings

### 1.6 Boundary Disambiguation Rules
**Critical for avoiding ambiguity**: Each boundary point belongs to exactly one color.

- **Segment Types**: Only horizontal/vertical segments (90°/270° angles)
- **Inclusion Rules**:
  - If `lowest_value == 0`: point ∈ `[0, upper_bound]` (closed interval)
  - Else: point ∈ `(lower_bound, upper_bound]` (half-open interval)
- **Implementation**: Use geometry crate for robust point-in-polygon testing
- **Complex Polygons**: Handle polygons with >4 corners correctly

---

## Algorithm 2: ISCC-NBS Descriptor Construction System

### Overview
Each ISCC-NBS color (1-267) has associated strings that generate both official and revised color descriptors through systematic transformation rules.

### 2.1 Input Strings (All Lowercase)
1. **iscc-nbs-descriptor**: Fully formed official descriptor for test comparison
2. **iscc-nbs-color**: Root color name (human-perceived color family)
3. **iscc-nbs-modifier**: Transformation rule string for descriptor construction  
4. **revised-color**: Alternative descriptive color name for revised system

### 2.2 Modifier Transformation Rules

#### Empty Modifiers (White/Black)
- **Colors**: White (263), Black (267)
- **Rule**: No transformation needed (no "light white" or "medium white")
- **Result**: Use color name as-is

#### Simple Prefix Modifiers
- **Format**: Direct prefix addition with space
- **Example**: `"light" + "blue"` → `"light blue"`

#### "-ish" Placeholder Modifiers  
- **Format**: Contains `-ish` as positional placeholder for color transformation
- **Processing**: Replace `-ish` with appropriately transformed color name

**Examples**:
- `"purple" + "-ish black"` → `"purplish black"`
- `"purple" + "dark -ish gray"` → `"dark purplish gray"`

### 2.3 English Grammar "-ish" Transformation Rules

#### Standard Transformations
```
blue    → bluish
red     → reddish  
green   → greenish
pink    → pinkish
brown   → brownish
yellow  → yellowish
purple  → purplish
```

#### Exception Rule
```
olive   → olive    (unchanged)
```

**Example**: `"olive" + "light -ish gray"` → `"light olive gray"`

### 2.4 Complete Transformation Constants
Store as implementation constants:
```rust
const COLOR_TO_ISH: &[(&str, &str)] = &[
    ("pink", "pinkish"),
    ("red", "reddish"), 
    ("brown", "brownish"),
    ("yellow", "yellowish"),
    ("olive", "olive"),        // Exception: unchanged
    ("green", "greenish"),
    ("blue", "bluish"),
    ("purple", "purplish"),
];
```

### 2.5 Dual Naming Systems

#### Official ISCC-NBS System
- **Construction**: `iscc-nbs-color` + `iscc-nbs-modifier` transformations
- **Usage**: Standards compliance and test comparison

#### Revised Descriptor System  
- **Construction**: `revised-color` + `iscc-nbs-modifier` transformations (same rules)
- **Usage**: More descriptive/intuitive color names

### 2.6 Additional Extracted Information

#### Color Shade
- **Definition**: Last word of color name or revised-color name
- **Single Word**: If only one word exists, that word is the shade
- **Examples**: 
  - `"light blue gray"` → shade = `"gray"`
  - `"red"` → shade = `"red"`

#### Caching Strategy
- **Purpose**: Prevent recalculation for repeated Munsell color queries
- **Current**: Cache by Munsell color coordinates  
- **Future Extension**: Cache by hex/sRGB/Lab/HSV/HSL input formats

### 2.7 API Access Patterns
- **Complete Set**: Return all descriptor information in single call
- **Individual Components**: Access specific parts (shade, revised descriptor, etc.)
- **Performance**: Use small cache for successive lookups

---

# PART II: MATHEMATICAL MUNSELL CONVERSION SYSTEM

## 2. Constants and Parameters

### 2.1 Critical Constants
- **THRESHOLD_ACHROMATIC**: `1e-3` - Distance threshold for achromatic detection
- **CONVERGENCE_THRESHOLD**: `1e-7` - Convergence criterion (THRESHOLD_ACHROMATIC / 1e4)
- **MAX_ITERATIONS_OUTER**: `64` - Maximum outer loop iterations
- **MAX_ITERATIONS_INNER**: `16` - Maximum inner loop iterations (both hue and chroma)

### 2.2 Illuminants
- **Illuminant D65**: `[0.31270, 0.32900]` - sRGB reference white
- **Illuminant C**: `[0.31006, 0.31616]` - Munsell reference white (CCS_ILLUMINANT_MUNSELL)

### 2.3 Color Space Matrices
```
sRGB to XYZ (D65):
[0.4124564  0.3575761  0.1804375]
[0.2126729  0.7151522  0.0721750]
[0.0193339  0.1191920  0.9503041]
```

## 3. Sub-Algorithm: sRGB to xyY Conversion

### 3.1 sRGB to Linear RGB
```python
def srgb_to_linear(c):
    c_norm = c / 255.0
    if c_norm <= 0.04045:
        return c_norm / 12.92
    else:
        return ((c_norm + 0.055) / 1.055) ** 2.4
```

### 3.2 Linear RGB to XYZ
```python
def linear_rgb_to_xyz(r_linear, g_linear, b_linear):
    X = 0.4124564 * r_linear + 0.3575761 * g_linear + 0.1804375 * b_linear
    Y = 0.2126729 * r_linear + 0.7151522 * g_linear + 0.0721750 * b_linear
    Z = 0.0193339 * r_linear + 0.1191920 * g_linear + 0.9503041 * b_linear
    return [X, Y, Z]
```

### 3.3 XYZ to xyY
```python
def xyz_to_xyy(X, Y, Z):
    total = X + Y + Z
    if total == 0:
        # Use Illuminant C as default
        return [0.31006, 0.31616, 0.0]
    else:
        x = X / total
        y = Y / total
        return [x, y, Y]
```

## 4. Sub-Algorithm: ASTM D1535 Munsell Value

### 4.1 Luminance to Munsell Value
```python
def luminance_to_munsell_value(Y):
    """Y in range [0, 1], returns V in range [0, 10]"""
    Y_percent = Y * 100  # Convert to percentage
    
    # ASTM D1535 quintic polynomial
    V = (1.1914 * Y_percent 
         - 0.22533 * (Y_percent ** 2)
         + 0.23352 * (Y_percent ** 3)
         - 0.020484 * (Y_percent ** 4)
         + 0.00081939 * (Y_percent ** 5))
    
    # Round if close to integer (within float precision)
    if abs(V - round(V)) < 1e-10:  # is_integer check
        V = round(V)
    
    return V
```

### 4.2 Munsell Value to Luminance (Inverse)
Uses Newton-Raphson iteration or pre-computed lookup table with linear interpolation.

## 5. Main Algorithm: xyY to Munsell Specification

### 5.1 Input Processing and Initial Setup
```python
def xyy_to_munsell(x, y, Y):
    # Step 1: Calculate Munsell value
    value = luminance_to_munsell_value(Y)
    
    # Step 2: Get achromatic center for this value
    # CRITICAL: Achromatic center is ALWAYS Illuminant C
    x_center, y_center = [0.31006, 0.31616]
    
    # Step 3: Calculate polar coordinates relative to achromatic center
    rho_input = sqrt((x - x_center)**2 + (y - y_center)**2)
    phi_input = degrees(atan2(y - y_center, x - x_center))
    
    # Step 4: Check if achromatic
    if rho_input < THRESHOLD_ACHROMATIC:  # 1e-3
        return normalise_munsell_specification([nan, value, nan, nan])
```

### 5.2 Initial Guess Generation
```python
    # Step 5: Convert to XYZ for Lab calculation
    XYZ = xyY_to_XYZ([x, y, Y])
    
    # Step 6: CRITICAL - Create custom reference white scaled by Y
    XYZ_w = [Y * 0.31006/0.31616,  # X_w
             Y,                      # Y_w
             Y * (1-0.31006-0.31616)/0.31616]  # Z_w
    
    # Step 7: Convert to Lab using custom reference
    Lab = XYZ_to_Lab(XYZ, XYZ_w)
    LCHab = Lab_to_LCH(Lab)
    
    # Step 8: Generate initial guess
    hue_initial, code = LCHab_to_munsell_specification(LCHab)
    chroma_initial = LCHab.C / 5 * (5 / 5.5)  # Convergence factor
    
    specification_current = [hue_initial, value, chroma_initial, code]
```

### 5.3 Main Iterative Loop
```python
    iterations = 0
    while iterations <= MAX_ITERATIONS_OUTER:
        iterations += 1
        
        hue_current, _, chroma_current, code_current = specification_current
        hue_angle_current = hue_to_hue_angle(hue_current, code_current)
        
        # CRITICAL: Cap chroma at maximum (FIRST TIME)
        chroma_maximum = maximum_chroma_from_renotation(hue_current, value, code_current)
        if chroma_current > chroma_maximum:
            chroma_current = chroma_maximum
            specification_current[2] = chroma_current
```

### 5.4 First Inner Loop: Hue Refinement
```python
        # Calculate current position
        x_current, y_current = munsell_specification_to_xy(specification_current)
        rho_current = sqrt((x_current - x_center)**2 + (y_current - y_center)**2)
        phi_current = degrees(atan2(y_current - y_center, x_current - x_center))
        
        # Calculate phi difference with wraparound
        phi_current_difference = (360 - phi_input + phi_current) % 360
        if phi_current_difference > 180:
            phi_current_difference -= 360
        
        # Initialize data arrays
        phi_differences_data = [phi_current_difference]
        hue_angles_differences_data = [0]
        iterations_inner = 0
        extrapolate = False
        
        # Inner loop: Find bracketing hue angles
        while (sign(min(phi_differences_data)) == sign(max(phi_differences_data)) 
               and not extrapolate):
            iterations_inner += 1
            
            if iterations_inner > MAX_ITERATIONS_INNER:
                raise RuntimeError("Maximum inner iterations exceeded")
            
            # Calculate new hue angle
            hue_angle_inner = (hue_angle_current + 
                              iterations_inner * (phi_input - phi_current)) % 360
            hue_angle_difference_inner = (iterations_inner * 
                                         (phi_input - phi_current)) % 360
            if hue_angle_difference_inner > 180:
                hue_angle_difference_inner -= 360
            
            hue_inner, code_inner = hue_angle_to_hue(hue_angle_inner)
            
            # CRITICAL: Enable extrapolation after 2 points
            if len(phi_differences_data) >= 2:
                extrapolate = True
            
            if not extrapolate:
                # Calculate phi for this hue
                x_inner, y_inner = munsell_specification_to_xy(
                    [hue_inner, value, chroma_current, code_inner])
                phi_inner = degrees(atan2(y_inner - y_center, x_inner - x_center))
                phi_inner_difference = (360 - phi_input + phi_inner) % 360
                if phi_inner_difference > 180:
                    phi_inner_difference -= 360
                
                phi_differences_data.append(phi_inner_difference)
                hue_angles_differences_data.append(hue_angle_difference_inner)
```

### 5.5 Hue Interpolation/Extrapolation
```python
        # Sort by phi differences
        phi_differences = array(phi_differences_data)
        hue_angles_differences = array(hue_angles_differences_data)
        sort_indices = argsort(phi_differences)
        phi_differences = phi_differences[sort_indices]
        hue_angles_differences = hue_angles_differences[sort_indices]
        
        # CRITICAL: Use Extrapolator for hue to find zero crossing
        interpolator = LinearInterpolator(phi_differences, hue_angles_differences)
        extrapolator = Extrapolator(interpolator)
        hue_angle_difference_new = extrapolator(0) % 360
        hue_angle_new = (hue_angle_current + hue_angle_difference_new) % 360
        
        # Update specification with new hue
        hue_new, code_new = hue_angle_to_hue(hue_angle_new)
        specification_current = [hue_new, value, chroma_current, code_new]
        
        # Check convergence
        x_current, y_current = munsell_specification_to_xy(specification_current)
        difference = euclidean_distance([x, y], [x_current, y_current])
        if difference < CONVERGENCE_THRESHOLD:
            return normalise_munsell_specification(specification_current)
```

### 5.6 Second Inner Loop: Chroma Refinement
```python
        # CRITICAL: Cap chroma at maximum (SECOND TIME)
        hue_current, _, chroma_current, code_current = specification_current
        chroma_maximum = maximum_chroma_from_renotation(hue_current, value, code_current)
        if chroma_current > chroma_maximum:
            chroma_current = chroma_maximum
            specification_current[2] = chroma_current
        
        # Calculate current rho
        x_current, y_current = munsell_specification_to_xy(specification_current)
        rho_current = sqrt((x_current - x_center)**2 + (y_center - y_center)**2)
        
        # Initialize bounds
        rho_bounds_data = [rho_current]
        chroma_bounds_data = [chroma_current]
        iterations_inner = 0
        
        # Inner loop: Find bracketing rho values
        while not (min(rho_bounds_data) < rho_input < max(rho_bounds_data)):
            iterations_inner += 1
            
            if iterations_inner > MAX_ITERATIONS_INNER:
                raise RuntimeError("Maximum inner iterations exceeded")
            
            # Calculate new chroma using power scaling
            # CRITICAL: Use safe division mode
            if rho_current == 0:
                chroma_inner = chroma_current
            else:
                chroma_inner = ((rho_input / rho_current) ** iterations_inner) * chroma_current
            
            # Cap at maximum
            if chroma_inner > chroma_maximum:
                chroma_inner = chroma_maximum
            
            # Calculate rho for this chroma
            x_inner, y_inner = munsell_specification_to_xy(
                [hue_current, value, chroma_inner, code_current])
            rho_inner = sqrt((x_inner - x_center)**2 + (y_inner - y_center)**2)
            
            rho_bounds_data.append(rho_inner)
            chroma_bounds_data.append(chroma_inner)
```

### 5.7 Chroma Interpolation
```python
        # Sort by rho
        rho_bounds = array(rho_bounds_data)
        chroma_bounds = array(chroma_bounds_data)
        sort_indices = argsort(rho_bounds)
        rho_bounds = rho_bounds[sort_indices]
        chroma_bounds = chroma_bounds[sort_indices]
        
        # CRITICAL: Use LinearInterpolator only (NO extrapolation for chroma)
        chroma_new = LinearInterpolator(rho_bounds, chroma_bounds)(rho_input)
        
        # Update specification
        specification_current = [hue_current, value, chroma_new, code_current]
        
        # Check convergence
        x_current, y_current = munsell_specification_to_xy(specification_current)
        difference = euclidean_distance([x, y], [x_current, y_current])
        if difference < CONVERGENCE_THRESHOLD:
            return normalise_munsell_specification(specification_current)
    
    # If we get here, maximum iterations exceeded
    raise RuntimeError("Maximum outer iterations exceeded")
```

## 6. Normalization Rules

### 6.1 Normalise Munsell Specification
```python
def normalise_munsell_specification(specification):
    hue, value, chroma, code = specification
    
    # Check if grey/achromatic
    if is_grey_munsell_colour(specification):
        return [nan, value, nan, nan]
    
    # CRITICAL: 0YR is equivalent to 10R
    if hue == 0:
        hue = 10
        code = (code + 1) % 10
    
    # CRITICAL: Zero chroma returns achromatic
    if chroma == 0:
        return [nan, value, nan, nan]
    
    return [hue, value, chroma, code]
```

### 6.2 Is Grey Munsell Colour
```python
def is_grey_munsell_colour(specification):
    # Returns True if specification contains only value (all others are nan)
    non_nan = specification[~isnan(specification)]
    return len(non_nan) == 1  # Only value is present
```

## 7. Helper Functions

### 7.1 Munsell Specification to xy
```python
def munsell_specification_to_xy(specification):
    specification = normalise_munsell_specification(specification)
    
    # CRITICAL: Grey colors return Illuminant C coordinates
    if is_grey_munsell_colour(specification):
        return [0.31006, 0.31616]
    
    # Otherwise, interpolate from renotation data
    return interpolate_from_renotation_data(specification)
```

### 7.2 Hue Angle Conversions
```python
HUE_FAMILIES = ['R', 'YR', 'Y', 'GY', 'G', 'BG', 'B', 'PB', 'P', 'RP']

def hue_to_hue_angle(hue, code):
    """Convert hue (0-10) and family code (0-9) to angle (0-360)"""
    return code * 36 + hue * 3.6

def hue_angle_to_hue(angle):
    """Convert angle (0-360) to hue (0-10) and family code (0-9)"""
    angle = angle % 360
    code = int(angle / 36)
    hue = (angle % 36) / 3.6
    return hue, code
```

## 8. Critical Implementation Details

### 8.1 Major Requirements
1. **Custom Lab Reference White**: Must scale XYZ_w by input luminance Y
2. **Achromatic Center**: Always use Illuminant C coordinates [0.31006, 0.31616]
3. **Normalization**: Implement 0YR→10R and chroma==0→achromatic rules
4. **Interpolation Strategy**: Extrapolator for hue, LinearInterpolator for chroma
5. **Chroma Capping**: Must cap TWICE per outer iteration

### 8.2 Convergence Details
- Convergence threshold: 1e-7 (euclidean distance in xy space)
- Check convergence after EACH inner loop (not just at end)
- Enable extrapolation after 2 points for hue refinement

### 8.3 Edge Cases
- Pure black [0,0,0] → "N 0.0"
- Pure white [255,255,255] → "N 9.5" (approximately)
- Zero chroma colors → Achromatic "N x.x" notation
- 0YR colors → Convert to 10R

## 9. Validation Criteria

The implementation should achieve:
- ≤0.1 difference in all dimensions (hue, value, chroma) for all 4007 reference colors
- Maximum 2 family mismatches (matching Python colour-science)
- Exact achromatic handling for grey colors

## 10. Version History

- v1.0: Initial specification
- v2.0: Added normalization rules and convergence details
- v3.0: Complete rewrite from systematic line-by-line analysis of Python implementation

---

## 11. Function Mapping: Rust vs Python colour-science

This section maps all functions between our Rust implementation and Python's colour-science library to identify which functions are true 1:1 ports and where we diverge.

### Legend
- ✅ = 1:1 port completed
- ⚠️ = Partial port (some differences)
- ❌ = Not ported / Different approach
- 🔧 = Uses palette crate function
- 📝 = Custom shim required

### 11.1 Python colour-science Functions (notation.munsell module)

#### Main Conversion Functions
1. `notation.munsell.xyY_to_munsell_colour(xyY: ArrayLike) -> str`
   - Rust: `xyy_to_munsell()` ⚠️
   - Differences: Returns MunsellSpecification struct, not string
   
2. `notation.munsell._xyY_to_munsell_specification(xyY: ArrayLike) -> NDArrayFloat`
   - Rust: `xyy_to_munsell_specification()` ⚠️
   - Main iterative algorithm - attempting 1:1 port but with issues

3. `notation.munsell.munsell_colour_to_xyY(munsell_colour: ArrayLike) -> NDArrayFloat`
   - Rust: Not implemented ❌

#### Value Calculation Functions
4. `notation.munsell.munsell_value_ASTMD1535(Y: ArrayLike) -> NDArrayFloat`
   - Rust: `luminance_to_munsell_value()` ✅
   - Uses Newton-Raphson iteration with same polynomial

5. `notation.munsell.luminance_ASTMD1535(value: ArrayLike) -> NDArrayFloat`
   - Rust: `munsell_value_to_luminance()` / `astm_polynomial()` ✅

#### Hue/Angle Conversion Functions
6. `notation.munsell.hue_to_ASTM_hue(hue: ArrayLike, code: ArrayLike) -> NDArrayFloat`
   - Rust: `hue_conversions::hue_to_astm_hue()` ✅
   - Fixed to use 17.0 constant and Python-style modulo

7. `notation.munsell.ASTM_hue_to_hue(hue: ArrayLike) -> NDArrayFloat`
   - Rust: Part of `hue_conversions::hue_angle_to_hue()` ✅

8. `notation.munsell.hue_angle_to_hue(hue_angle: ArrayLike) -> tuple[NDArrayFloat, NDArrayFloat]`
   - Rust: `hue_conversions::hue_angle_to_hue()` ✅
   - Returns (hue, code) tuple

9. `notation.munsell.hue_to_hue_angle(hue: ArrayLike, code: ArrayLike) -> NDArrayFloat`
   - Rust: `hue_conversions::hue_to_hue_angle()` ✅
   - Note: Python is deprecated, uses hue_to_ASTM_hue internally

#### Renotation Data Functions
10. `notation.munsell._munsell_specification_to_xyY(specification: ArrayLike) -> NDArrayFloat`
    - Rust: `munsell_specification_to_xy()` ⚠️
    - Differences: Returns (x,y) not full xyY, doesn't handle value interpolation same way

11. `notation.munsell.xy_from_renotation_ovoid(specification: ArrayLike) -> NDArrayFloat`
    - Rust: `xy_from_renotation_ovoid()` ⚠️
    - Complex interpolation logic, attempting port but may have differences

12. `notation.munsell.maximum_chroma_from_renotation(specification: ArrayLike) -> NDArrayFloat`
    - Rust: `maximum_chroma_from_renotation()` ⚠️
    - Different lookup approach

13. `notation.munsell.bounding_hues_from_renotation(hue: ArrayLike, code: ArrayLike) -> tuple`
    - Rust: `hue_conversions::bounding_hues_from_renotation()` ✅

#### Interpolation Functions
14. `notation.munsell.interpolation_method_from_renotation_ovoid(specification: ArrayLike) -> Literal["Linear", "Radial"]`
    - Rust: `get_interpolation_method()` ❌
    - We use simplified logic, not full 1,250-entry table

#### Initial Guess Functions
15. `notation.munsell.LCHab_to_munsell_specification(LCHab: ArrayLike) -> NDArrayFloat`
    - Rust: `lchab_to_munsell_specification()` ⚠️

#### Helper Functions
16. `notation.munsell.normalise_munsell_specification(specification: ArrayLike) -> NDArrayFloat`
    - Rust: `normalize_munsell_specification()` ✅

17. `notation.munsell.is_grey_munsell_colour(specification: ArrayLike) -> bool`
    - Rust: Part of achromatic detection logic ✅

#### Coordinate Transform Functions (from colour.algebra)
18. `colour.algebra.cartesian_to_cylindrical(a: ArrayLike) -> NDArrayFloat`
    - Rust: `coordinate_transforms::cartesian_to_cylindrical()` ✅

19. `colour.algebra.polar_to_cartesian(rho: ArrayLike, phi: ArrayLike) -> NDArrayFloat`
    - Rust: `coordinate_transforms::polar_to_cartesian()` ✅

#### Color Space Conversions (from colour.models)
20. `colour.sRGB_to_XYZ(RGB: ArrayLike) -> NDArrayFloat`
    - Rust: Uses palette crate 🔧
    - `Srgb::from_components()` -> `LinSrgb::from_color_unclamped()` -> `Xyz::from_color()`

21. `colour.XYZ_to_xyY(XYZ: ArrayLike) -> NDArrayFloat`
    - Rust: `xyz_to_xyy()` ✅ (custom implementation)

22. `colour.xyY_to_XYZ(xyY: ArrayLike) -> NDArrayFloat`
    - Rust: `xyy_to_xyz()` ✅ (custom implementation)

23. `colour.XYZ_to_Lab(XYZ: ArrayLike, illuminant: ArrayLike) -> NDArrayFloat`
    - Rust: `xyz_to_lab_with_xy_reference()` ⚠️
    - Custom implementation, may have differences

24. `colour.Lab_to_LCHab(Lab: ArrayLike) -> NDArrayFloat`
    - Rust: `lab_to_lchab()` ✅

#### Interpolation Classes (from colour.algebra)
25. `colour.algebra.LinearInterpolator(x: ArrayLike, y: ArrayLike)`
    - Rust: `linear_interpolate_clamped()` ⚠️
    - Custom implementation, clamps to boundaries

26. `colour.algebra.Extrapolator(interpolator: Interpolator)`
    - Rust: `linear_interpolate()` ⚠️
    - Custom implementation with extrapolation support

### 11.2 Rust Implementation Functions

#### Main Module (mathematical.rs)
1. `srgb_to_munsell()` 🔧
   - Uses palette for sRGB -> XYZ conversion
   - Then custom xyy_to_munsell_specification
   
2. `srgb_to_xyy()` 🔧
   - Uses palette: `Srgb` -> `LinSrgb` -> `Xyz` (D65)
   - Custom XYZ -> xyY conversion

3. `xyy_to_munsell_specification()` ⚠️
   - Main algorithm, attempting 1:1 port of Python's `_xyY_to_munsell_specification`
   - Has convergence issues

4. `generate_initial_guess()` ⚠️
   - Implements Lab/LCH initial guess
   - Uses custom Lab conversion

5. `linear_interpolate()` ⚠️
   - Implements extrapolation (Python uses Extrapolator class)
   - Custom implementation

6. `linear_interpolate_clamped()` ❌
   - Custom function for chroma interpolation
   - Not in Python

#### Lab/LCH Functions (custom implementations)
7. `xyz_to_lab_with_xy_reference()` ⚠️
   - Custom implementation to match Python's XYZ_to_Lab with xy reference
   - May have precision differences

8. `lab_to_lchab()` ✅
   - Simple conversion matching Python

9. `lchab_to_munsell_specification()` ⚠️
   - Partial port of Python's LCHab_to_munsell_specification

#### Renotation Data Access
10. `lookup_xy_from_renotation()` ❌
    - Direct lookup in our data structure
    - Python uses complex numpy operations

11. `interpolate_from_renotation_data()` ❌
    - Custom bilinear interpolation
    - Python uses different approach

12. `xy_from_renotation_ovoid()` ⚠️
    - Attempting to port Python's complex logic
    - May have differences in edge cases

13. `xy_from_renotation_ovoid_for_even_chroma()` ⚠️
    - Helper for above

14. `get_interpolation_method()` ❌
    - Simplified logic instead of full table lookup

### 11.3 Key Differences Identified

1. **Lab Conversion**: Python uses `colour.XYZ_to_Lab()` with xy chromaticity reference, we implemented custom version
2. **Interpolation Classes**: Python uses scipy's LinearInterpolator/Extrapolator, we use custom functions
3. **Renotation Data Access**: Python uses numpy array operations, we use direct lookups
4. **Interpolation Method Table**: Python has full 1,250-entry table, we use simplified logic
5. **Value Interpolation**: Python's `_munsell_specification_to_xyY` handles non-integer values differently
6. **Domain Range Scale**: Python uses context manager, we don't implement this
7. **Array Operations**: Python handles array inputs, we only handle scalars

### 11.4 Functions Needing True 1:1 Port

Priority functions that likely affect accuracy:
1. ❌ `interpolation_method_from_renotation_ovoid()` - Need full table
2. ⚠️ `xy_from_renotation_ovoid()` - Complex interpolation logic
3. ⚠️ `_munsell_specification_to_xyY()` - Value interpolation handling
4. ⚠️ Lab/XYZ conversions - Using palette + custom instead of exact port
5. ⚠️ Interpolation/Extrapolation - Custom instead of using same algorithm

### 11.5 Shims and Adaptations

1. **Palette crate usage for sRGB->XYZ**:
   ```rust
   // We use:
   let rgb = Srgb::from_components((r, g, b));
   let linear = LinSrgb::from_color_unclamped(rgb);
   let xyz = Xyz::from_color(linear);
   
   // Python uses:
   XYZ = colour.sRGB_to_XYZ([r/255, g/255, b/255])
   ```
   Note: Palette uses D65, we don't adapt to C (removed adaptation code)

2. **Custom Lab conversion**:
   - Had to implement `xyz_to_lab_with_xy_reference()` because palette doesn't support xy reference
   - Python: `colour.XYZ_to_Lab(XYZ, xy_ref)`
   - Rust: Custom implementation

3. **Interpolation**:
   - Python: `Extrapolator(LinearInterpolator(x, y))(target)`
   - Rust: Custom `linear_interpolate()` with extrapolation logic