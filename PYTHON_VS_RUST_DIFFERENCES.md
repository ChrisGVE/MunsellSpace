# Python vs Rust Implementation Differences

## Critical Differences Found

### 1. Initial Guess Generation
**Python (lines 55-74):**
- Converts xyY → XYZ → Lab → LCHab
- Uses LCHab_to_munsell_specification for initial guess
- Scales initial chroma by (5/5.5) ≈ 0.909

**Rust:**
- Uses direct xyY polar angle for initial guess
- No Lab/LCH conversion
- No chroma scaling factor

### 2. Chromatic Adaptation
**Python:**
- NO chromatic adaptation
- Works directly in Illuminant C space throughout

**Rust:**
- Has Bradford chromatic adaptation code (D65 to C)
- This is WRONG - should be removed

### 3. Grey/Achromatic Detection
**Python (line 52):**
- Uses `rho_input < THRESHOLD_INTEGER` (1e-3)
- Returns normalized specification for grey

**Rust:**
- Uses `rho_input < THRESHOLD_INTEGER || xyy.Y < 1e-6`
- Additional check for near-black colors

### 4. Y Domain
**Python (line 29):**
- Converts Y to domain [0,1] using `to_domain_1(Y)`
- Then multiplies by 100 for munsell_value_ASTMD1535

**Rust:**
- Expects Y already in [0,1] range
- Multiplies by 100 for value calculation

### 5. Convergence Check
**Python:**
- Uses euclidean distance between (x,y) coordinates
- Threshold: THRESHOLD_INTEGER / 1e4 = 1e-7

**Rust:**
- Same approach, likely correct

### 6. Maximum Iterations
**Python:**
- Outer loop: 64 iterations
- Inner hue loop: 16 iterations

**Rust:**
- Same values (MAX_OUTER_ITERATIONS = 64, MAX_INNER_ITERATIONS = 16)

### 7. Initial Phi Difference Storage
**Python (lines 112-113):**
- Always starts with `phi_differences_data = [phi_current_difference]`
- Always includes initial point

**Rust:**
- Only includes if abs(phi_current_difference) >= 1e-6
- This could cause issues with convergence

## Required Changes for 1:1 Port

1. **Remove all chromatic adaptation code**
2. **Implement Lab/LCH initial guess generation**
3. **Add chroma scaling factor (5/5.5)**
4. **Always include initial phi difference**
5. **Implement exact interpolation method table**
6. **Match all numerical thresholds exactly**