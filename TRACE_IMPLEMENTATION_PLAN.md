# Trace Implementation Plan

## Objective
Create comprehensive trace logging for both Python and Rust implementations of the Munsell color conversion algorithm to identify exact points of divergence.

## Trace Format
Each trace line should follow this format:
```
<function_name>:<line_no> | vars: <var1>=<val1>, <var2>=<val2>, ... | action: <operation_type> <details>
```

Where operation_type is one of:
- ENTER: Function entry with arguments
- BRANCH: Conditional branch with condition and result
- LOOP: Loop iteration with condition
- CALL: Function call with arguments
- RETURN: Function return with value
- CALC: Calculation with expression and result

## Functions to Trace

### Core Convergence Functions
1. `xyY_to_munsell_specification` / `xyy_to_munsell_specification`
2. `xy_from_renotation_ovoid` / `xy_from_renotation_ovoid`
3. `xy_from_renotation_ovoid_interpolated` (Rust specific)
4. `maximum_chroma_from_renotation`
5. `LCHab_to_munsell_specification` / `lchab_to_munsell_specification`

### Helper Functions
1. `hue_to_hue_angle`
2. `hue_angle_to_hue`
3. `bounding_hues_from_renotation`
4. `interpolation_method_from_renotation_ovoid`
5. `luminance_ASTMD1535` / `luminance_astmd1535`
6. `munsell_value_ASTMD1535` / `munsell_value_astmd1535`

### Calculation Functions
1. `lerp` / linear interpolation
2. `cartesian_to_cylindrical`
3. `polar_to_cartesian`
4. `xyz_to_lab`
5. `lab_to_lchab`

## Test Cases
Focus on problematic colors:
1. RGB(221, 238, 238) - #ddeeee - Low chroma issue
2. RGB(68, 0, 187) - #4400bb - High chroma PB
3. RGB(34, 17, 119) - #221177 - PB family issue

## Implementation Steps

### Phase 1: Python Instrumentation
1. Create `traced_python_munsell.py` with instrumented functions
2. Add trace output to all relevant functions
3. Run test cases and save traces to `python_trace_<color>.txt`

### Phase 2: Rust Instrumentation  
1. Create `src/traced_port.rs` with instrumented functions
2. Add trace output matching Python format
3. Create test binary `src/bin/trace_color.rs`
4. Run test cases and save traces to `rust_trace_<color>.txt`

### Phase 3: Analysis
1. Create `analyze_traces.py` to compare traces line by line
2. Identify first divergence point for each test case
3. Generate divergence report with context

## Expected Outcomes
1. Exact identification of where algorithms diverge
2. Understanding of why chroma converges differently
3. Identification of family assignment errors
4. Clear path to fixes

## Files to Create
- `traced_python_munsell.py` - Instrumented Python implementation
- `src/traced_port.rs` - Instrumented Rust implementation  
- `src/bin/trace_color.rs` - Rust test runner
- `analyze_traces.py` - Trace comparison tool
- `python_trace_<color>.txt` - Python trace outputs
- `rust_trace_<color>.txt` - Rust trace outputs
- `DIVERGENCE_REPORT.md` - Analysis results