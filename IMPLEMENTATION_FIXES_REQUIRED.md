# Implementation Fixes Required

Based on systematic line-by-line analysis of Python colour-science implementation.

## Critical Fixes (High Priority)

### 1. Custom Lab Reference White ❌ CRITICAL
**Location**: `xyy_to_munsell` initial guess generation
**Current**: Using standard Illuminant C from palette
**Required**: Custom XYZ_w scaled by input luminance Y
```rust
// WRONG - current implementation
let lab = Lab::<IlluminantC, f64>::from_color(xyz);

// CORRECT - needs custom implementation
let xyz_w = [
    Y * 0.31006 / 0.31616,  // X_w
    Y,                       // Y_w  
    Y * (1.0 - 0.31006 - 0.31616) / 0.31616  // Z_w
];
// Then manually convert XYZ to Lab using xyz_w
```

### 2. Normalization Rules ❌ CRITICAL
**Location**: End of `xyy_to_munsell` and output formatting
**Current**: Missing normalization logic
**Required**:
- If hue == 0.0 → hue = 10.0, family_code = (family_code + 1) % 10
- If chroma == 0.0 → return achromatic (N value)
- Implement `normalise_munsell_specification` function

### 3. Interpolation Strategy ❌ CRITICAL  
**Location**: Chroma refinement loop
**Current**: Using Extrapolator for chroma
**Required**: LinearInterpolator ONLY (no extrapolation)
```rust
// WRONG
let chroma_interpolator = Extrapolator::new(points);

// CORRECT
let chroma_interpolator = LinearInterpolator::new(points);
```

## Major Fixes (Important)

### 4. Chroma Capping Twice ❌
**Location**: Main outer loop
**Current**: Only capping once before hue refinement
**Required**: Cap TWICE - before hue refinement AND before chroma refinement

### 5. Extrapolation Enable After 2 Points ❌
**Location**: Hue refinement inner loop
**Current**: Enabling after 4 points
**Required**: Enable after 2 points
```rust
// WRONG
if phi_differences.len() >= 4

// CORRECT  
if phi_differences.len() >= 2
```

### 6. Achromatic Center Always Illuminant C ✅ (Already fixed)
**Location**: Beginning of `xyy_to_munsell`
**Status**: Fixed but needs verification it's working correctly

## Minor Fixes (Nice to Have)

### 7. Integer Value Rounding ❌
**Location**: After calculating Munsell value
**Current**: Not rounding near-integer values
**Required**: If abs(value - round(value)) < 1e-10, round it

### 8. Safe Division for Power Scaling ❌
**Location**: Chroma refinement inner loop
**Current**: Direct division
**Required**: Check for rho_current == 0 case

### 9. Final Output Scaling ❌
**Location**: Return statement
**Current**: Direct return of specification
**Required**: Scale components appropriately (domain range handling)

## Implementation Order

1. **First**: Fix custom Lab reference white (most critical)
2. **Second**: Fix normalization rules (0YR→10R, chroma==0)
3. **Third**: Fix interpolation strategy (LinearInterpolator for chroma)
4. **Fourth**: Fix chroma capping twice
5. **Fifth**: Fix extrapolation trigger (2 points not 4)
6. **Sixth**: Minor fixes (rounding, safe division, etc.)

## Testing Strategy

After each fix:
1. Run full 4007 color validation
2. Check exact match percentage
3. Check family mismatch count
4. Compare with Python results
5. Document improvement in accuracy

## Expected Outcome

With all fixes applied, we should achieve:
- ~61% exact matches (matching previous best)
- ≤2 family mismatches (matching Python)
- ≤0.1 difference in all dimensions for all colors