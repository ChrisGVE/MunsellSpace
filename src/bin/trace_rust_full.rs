use munsellspace::python_port::*;
use munsellspace::python_port_helpers::euclidean_distance;
use munsellspace::python_port_lab::{srgb_to_xyz, lchab_to_munsell_specification};
use munsellspace::python_port_utils::*;
use munsellspace::error::Result;

// Helper function for XYZ to xyY conversion
fn xyz_to_xyy(xyz: [f64; 3]) -> [f64; 3] {
    let sum = xyz[0] + xyz[1] + xyz[2];
    if sum == 0.0 {
        [0.0, 0.0, 0.0]
    } else {
        [xyz[0] / sum, xyz[1] / sum, xyz[1]]
    }
}

// Helper function for xyz_to_lab with illuminant
fn xyz_to_lab_with_illuminant(xyz: [f64; 3], illuminant_xy: [f64; 2]) -> [f64; 3] {
    use munsellspace::python_port_helpers::xyz_to_lab;
    xyz_to_lab(xyz, illuminant_xy)
}

fn traced_xyy_to_munsell_specification(xyy: [f64; 3]) -> Result<[f64; 4]> {
    println!("\n{}", "=".repeat(80));
    println!("ENTERING _xyY_to_munsell_specification");
    println!("{}", "=".repeat(80));
    println!("INPUT: xyY = {:?}", xyy);
    
    // Line 2197: x, y, Y = tsplit(xyY)
    let x = xyy[0];
    let y = xyy[1];
    let big_y = xyy[2];
    println!("\nLine 2197: tsplit(xyY)");
    println!("  x = {}", x);
    println!("  y = {}", y);
    println!("  Y = {}", big_y);
    
    // Line 2199: Y * 100
    let y_times_100 = big_y * 100.0;
    println!("\nLine 2199: Y * 100");
    println!("  Y_times_100 = {}", y_times_100);
    
    // Line 2199: munsell_value_ASTMD1535 - Python passes Y*100 directly, NO from_range_100!
    let munsell_value_raw = munsell_value_astmd1535(y_times_100);
    println!("\nLine 2199: munsell_value_ASTMD1535(Y * 100)");
    println!("  munsell_value_raw = {}", munsell_value_raw);
    
    // Line 2199: as_float_array (Rust doesn't need this)
    let mut value = munsell_value_raw;
    println!("\nLine 2199: as_float_array(munsell_value_ASTMD1535(...))");
    println!("  value = {}", value);
    
    // Line 2202: value.round()
    let value_rounded = value.round();
    println!("\nLine 2202: value.round()");
    println!("  value_rounded = {}", value_rounded);
    
    // Line 2202: value - value.round()
    let value_diff = value - value_rounded;
    println!("\nLine 2202: value - value.round()");
    println!("  value_diff = {}", value_diff);
    
    // Line 2202: value_diff_item (in Rust it's just value_diff)
    let value_diff_item = value_diff;
    println!("\nLine 2202: (value - value.round()).item()");
    println!("  value_diff_item = {}", value_diff_item);
    
    // Line 2202: condition = value_diff_item < 1e-6
    let condition = value_diff_item.abs() < 1e-6;
    println!("\nLine 2202: value_diff_item.abs() < 1e-6");
    println!("  condition = {}", condition);
    
    // Line 2202-2204: value = round(value) if condition else value
    if condition {
        value = value_rounded;
        println!("\nLine 2203: value = value.round() [condition True]");
    } else {
        println!("\nLine 2204: value = value [condition False]");
    }
    println!("  value = {}", value);
    
    // Line 2207: Create specification for neutral
    let neutral_spec = [f64::NAN, value, 0.0, f64::NAN];
    println!("\nLine 2207: neutral_spec = [NaN, {}, 0, NaN]", value);
    println!("  neutral_spec = {:?}", neutral_spec);
    
    // Line 2208: _munsell_specification_to_xyY call
    let xyy_center = munsell_specification_to_xyy(&neutral_spec)?;
    let x_center = xyy_center[0];
    let y_center = xyy_center[1];
    let y_center_big = xyy_center[2];
    println!("\nLine 2208: _munsell_specification_to_xyY(neutral_spec)");
    println!("  x_center = {}", x_center);
    println!("  y_center = {}", y_center);
    println!("  Y_center = {}", y_center_big);
    
    // Line 2212: x_diff = x - x_center
    let x_diff = x - x_center;
    println!("\nLine 2212: x - x_center");
    println!("  x_diff = {}", x_diff);
    
    // Line 2212: y_diff = y - y_center
    let y_diff = y - y_center;
    println!("\nLine 2212: y - y_center");
    println!("  y_diff = {}", y_diff);
    
    // Line 2211-2213: cartesian_to_cylindrical call
    let (rho_input, phi_input_rad, _z_input) = cartesian_to_cylindrical(x_diff, y_diff, y_center_big);
    println!("\nLine 2211-2213: cartesian_to_cylindrical([x - x_center, y - y_center, Y_center])");
    println!("  rho_input = {}", rho_input);
    println!("  phi_input = {} (radians)", phi_input_rad);
    println!("  _z_input = {}", _z_input);
    
    // Line 2215: Convert phi to degrees
    let phi_input = phi_input_rad.to_degrees();
    println!("\nLine 2215: phi_input.to_degrees()");
    println!("  phi_input = {} (degrees)", phi_input);
    
    // Line 2218: grey_threshold = 1e-3
    let grey_threshold = 1e-3;
    println!("\nLine 2218: grey_threshold = 1e-3");
    println!("  grey_threshold = {}", grey_threshold);
    
    // Line 2219: Check if grey
    let is_grey = rho_input < grey_threshold;
    println!("\nLine 2219: rho_input < grey_threshold");
    println!("  is_grey = {}", is_grey);
    
    if is_grey {
        println!("\nLine 2220-2222: Returning grey specification");
        let result = normalise_munsell_specification(&[f64::NAN, value, 0.0, f64::NAN]);
        println!("  result = {:?}", result);
        return Ok(result);
    }
    
    // Line 2226: XYZ conversion
    use munsellspace::python_port_helpers::xyy_to_xyz as conv_xyy_to_xyz;
    let xyz = conv_xyy_to_xyz(xyy);
    println!("\nLine 2226: xyY_to_XYZ(xyY)");
    println!("  XYZ = {:?}", xyz);
    
    // Line 2227-2232: Chromatic adaptation
    // In Rust, we do the adaptation directly
    let xyz_c = chromatic_adaptation_vonkries(xyz, "D65", "C");
    println!("\nLine 2227-2232: chromatic_adaptation_VonKries");
    println!("  Source illuminant (D65) = [0.98074, 1.00000, 1.18232]");
    println!("  Target illuminant (C) = [0.31006, 0.31616]");
    println!("  XYZ_c = {:?}", xyz_c);
    
    // Line 2233: Lab conversion
    // Use illuminant C xy coordinates [0.31006, 0.31616]
    let lab = xyz_to_lab_with_illuminant(xyz_c, [0.31006, 0.31616]);
    println!("\nLine 2233: XYZ_to_Lab(XYZ_c, illuminant_C)");
    println!("  Lab = {:?}", lab);
    
    // Line 2237: Calculate LCHab manually to show components
    let l = lab[0];
    let a = lab[1];
    let b = lab[2];
    let c = (a * a + b * b).sqrt();
    let h_rad = b.atan2(a);
    let mut h = h_rad.to_degrees();
    if h < 0.0 {
        h += 360.0;
    }
    let lchab = [l, c, h];
    println!("\nLine 2237: Manual LCHab calculation");
    println!("  L = {}", l);
    println!("  a = {}", a);
    println!("  b = {}", b);
    println!("  C = sqrt(a^2 + b^2) = sqrt({} + {}) = {}", a*a, b*b, c);
    println!("  H_rad = atan2(b, a) = atan2({}, {}) = {}", b, a, h_rad);
    println!("  H = degrees(H_rad) = {}", h);
    println!("  LCHab = {:?}", lchab);
    
    // Line 2237: LCHab_to_munsell_specification
    let mut specification_current = lchab_to_munsell_specification(lchab);
    println!("\nLine 2237: LCHab_to_munsell_specification(LCHab)");
    println!("  specification_current = {:?}", specification_current);
    
    // Line 2239: Update value
    specification_current[1] = value;
    println!("\nLine 2239: specification_current[1] = value");
    println!("  specification_current = {:?}", specification_current);
    
    // Line 2244: convergence_threshold
    let convergence_threshold = 1e-7;
    println!("\nLine 2244: convergence_threshold = 1e-7");
    println!("  convergence_threshold = {}", convergence_threshold);
    
    // Line 2246: iterations_maximum
    let iterations_maximum = 64;
    println!("\nLine 2246: iterations_maximum = 64");
    
    let mut iterations = 0;
    
    // Main convergence loop
    while iterations <= iterations_maximum {
        iterations += 1;
        println!("\n{}", "-".repeat(60));
        println!("ITERATION {}", iterations);
        println!("{}", "-".repeat(60));
        
        // Line 2252-2255: Extract current values
        let hue_current = specification_current[0];
        let _value_current = specification_current[1];
        let mut chroma_current = specification_current[2];
        let code_current = if specification_current[3].is_nan() { 0 } else { specification_current[3] as u8 };
        println!("\nLine 2252-2255: Extract current values");
        println!("  hue_current = {}", hue_current);
        println!("  _value_current = {}", _value_current);
        println!("  chroma_current = {}", chroma_current);
        println!("  code_current = {}", code_current);
        
        // Line 2257: hue_to_hue_angle
        let hue_angle_current = hue_to_hue_angle(hue_current, code_current);
        println!("\nLine 2257: hue_to_hue_angle([{}, {}])", hue_current, code_current);
        println!("  hue_angle_current = {}", hue_angle_current);
        
        // Line 2259: maximum_chroma_from_renotation
        let chroma_maximum = maximum_chroma_from_renotation(hue_current, value, code_current)?;
        println!("\nLine 2259: maximum_chroma_from_renotation([{}, {}, {}])", hue_current, value, code_current);
        println!("  chroma_maximum = {}", chroma_maximum);
        
        // Line 2261-2263: Check chroma limit
        let exceeds_max = chroma_current > chroma_maximum;
        println!("\nLine 2261: chroma_current > chroma_maximum");
        println!("  {} > {} = {}", chroma_current, chroma_maximum, exceeds_max);
        
        if exceeds_max {
            chroma_current = chroma_maximum;
            specification_current[2] = chroma_maximum;
            println!("\nLine 2262: Clamping chroma to maximum");
            println!("  chroma_current = {}", chroma_current);
        }
        
        // Line 2267: _munsell_specification_to_xyY
        let xyy_current = munsell_specification_to_xyy(&specification_current)?;
        let x_current = xyy_current[0];
        let y_current = xyy_current[1];
        let _y_current_big = xyy_current[2];
        println!("\nLine 2267: _munsell_specification_to_xyY(specification_current)");
        println!("  x_current = {}", x_current);
        println!("  y_current = {}", y_current);
        println!("  _Y_current = {}", _y_current_big);
        
        // Line 2271-2273: cartesian_to_cylindrical for current
        let (rho_current, phi_current_rad, _z_current) = cartesian_to_cylindrical(
            x_current - x_center,
            y_current - y_center,
            y_center_big
        );
        println!("\nLine 2271-2273: cartesian_to_cylindrical current");
        println!("  x_current - x_center = {}", x_current - x_center);
        println!("  y_current - y_center = {}", y_current - y_center);
        println!("  rho_current = {}", rho_current);
        println!("  phi_current = {} (radians)", phi_current_rad);
        
        // Line 2275: Convert phi_current to degrees
        let phi_current = phi_current_rad.to_degrees();
        println!("\nLine 2275: phi_current.to_degrees()");
        println!("  phi_current = {} (degrees)", phi_current);
        
        // Line 2277: Calculate phi difference
        let phi_diff_raw = (360.0 - phi_input + phi_current) % 360.0;
        println!("\nLine 2277: (360 - phi_input + phi_current) % 360");
        println!("  (360 - {} + {}) % 360 = {}", phi_input, phi_current, phi_diff_raw);
        
        let mut phi_current_difference = phi_diff_raw;
        if phi_current_difference > 180.0 {
            phi_current_difference -= 360.0;
            println!("\nLine 2278-2279: Adjusting phi_current_difference");
            println!("  {} - 360 = {}", phi_diff_raw, phi_current_difference);
        } else {
            println!("\nLine 2277: phi_current_difference = {}", phi_current_difference);
        }
        
        // Inner loop for chroma refinement
        let mut rho_bounds_data = vec![rho_current];
        let mut chroma_bounds_data = vec![chroma_current];
        println!("\nLine 2282-2283: Initialize bounds");
        println!("  rho_bounds_data = {:?}", rho_bounds_data);
        println!("  chroma_bounds_data = {:?}", chroma_bounds_data);
        
        let iterations_maximum_inner = 16;
        let mut iterations_inner = 0;
        
        // Line 2287: Check if rho_input is within bounds
        let min_rho = rho_bounds_data.iter().cloned().fold(f64::INFINITY, f64::min);
        let max_rho = rho_bounds_data.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
        let mut in_bounds = min_rho < rho_input && rho_input < max_rho;
        println!("\nLine 2287: Check bounds");
        println!("  min(rho_bounds_data) = {}", min_rho);
        println!("  max(rho_bounds_data) = {}", max_rho);
        println!("  {} < {} < {} = {}", min_rho, rho_input, max_rho, in_bounds);
        
        while !in_bounds {
            iterations_inner += 1;
            println!("\n  Inner iteration {}:", iterations_inner);
            
            if iterations_inner > iterations_maximum_inner {
                return Err(munsellspace::error::MunsellError::ConversionError {
                    message: "Maximum inner iterations reached".to_string()
                });
            }
            
            // Line 2296-2297: Calculate chroma_inner
            let ratio = sdiv(rho_input, rho_current);
            let power = iterations_inner as f64;
            let ratio_powered = spow(ratio, power);
            let mut chroma_inner = ratio_powered * chroma_current;
            
            println!("    Line 2296-2297: chroma refinement");
            println!("      rho_input = {}", rho_input);
            println!("      rho_current = {}", rho_current);
            println!("      ratio = {}", ratio);
            println!("      power = {}", power);
            println!("      ratio^power = {}", ratio_powered);
            println!("      chroma_current = {}", chroma_current);
            println!("      chroma_inner = {}", chroma_inner);
            
            // Line 2300-2302: Check chroma limit
            if chroma_inner > chroma_maximum {
                chroma_inner = chroma_maximum;
                specification_current[2] = chroma_maximum;
                println!("    Line 2301: Clamping chroma_inner to {}", chroma_maximum);
            }
            
            // Line 2304: Create inner specification
            let specification_inner = [
                hue_current,
                value,
                chroma_inner,
                code_current as f64,
            ];
            println!("    Line 2304: specification_inner = {:?}", specification_inner);
            
            // Line 2312: Get xy for inner specification
            let xyy_inner = munsell_specification_to_xyy(&specification_inner)?;
            let x_inner = xyy_inner[0];
            let y_inner = xyy_inner[1];
            println!("    Line 2312: _munsell_specification_to_xyY(specification_inner)");
            println!("      x_inner = {}", x_inner);
            println!("      y_inner = {}", y_inner);
            
            // Line 2316: cartesian_to_cylindrical for inner
            let (rho_inner, _phi_inner, _z_inner) = cartesian_to_cylindrical(
                x_inner - x_center,
                y_inner - y_center,
                y_center_big
            );
            println!("    Line 2316: cartesian_to_cylindrical inner");
            println!("      rho_inner = {}", rho_inner);
            
            // Update bounds
            rho_bounds_data.push(rho_inner);
            chroma_bounds_data.push(chroma_inner);
            println!("    Updated bounds:");
            println!("      rho_bounds_data = {:?}", rho_bounds_data);
            println!("      chroma_bounds_data = {:?}", chroma_bounds_data);
            
            // Check new bounds
            let min_rho = rho_bounds_data.iter().cloned().fold(f64::INFINITY, f64::min);
            let max_rho = rho_bounds_data.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
            in_bounds = min_rho < rho_input && rho_input < max_rho;
            println!("    New bounds check:");
            println!("      {} < {} < {} = {}", min_rho, rho_input, max_rho, in_bounds);
        }
        
        // Line 2323-2333: Linear interpolation
        println!("\nLine 2323-2324: Convert to arrays");
        println!("  rho_bounds = {:?}", rho_bounds_data);
        println!("  chroma_bounds = {:?}", chroma_bounds_data);
        
        // Line 2328: Sort by rho
        let mut indexed: Vec<_> = rho_bounds_data.iter().cloned().enumerate().collect();
        indexed.sort_by(|a, b| a.1.partial_cmp(&b.1).unwrap());
        let rhos_bounds_indexes: Vec<_> = indexed.iter().map(|(i, _)| *i).collect();
        println!("\nLine 2328: rho_bounds.argsort()");
        println!("  rhos_bounds_indexes = {:?}", rhos_bounds_indexes);
        
        let rho_bounds: Vec<_> = indexed.iter().map(|(_, v)| *v).collect();
        let chroma_bounds: Vec<_> = rhos_bounds_indexes.iter().map(|&i| chroma_bounds_data[i]).collect();
        println!("\nLine 2329-2330: Sort arrays");
        println!("  rho_bounds (sorted) = {:?}", rho_bounds);
        println!("  chroma_bounds (sorted) = {:?}", chroma_bounds);
        
        // Line 2332: Linear interpolation
        use munsellspace::python_port_interpolation::linear_interp_clamped;
        let chroma_new = linear_interp_clamped(&rho_bounds, &chroma_bounds, rho_input);
        println!("\nLine 2332: LinearInterpolator");
        println!("  rho_input = {}", rho_input);
        println!("  chroma_new = {}", chroma_new);
        
        // Update specification
        specification_current = [
            hue_current,
            value,
            chroma_new,
            code_current as f64,
        ];
        println!("\nLine 2337-2342: Update specification");
        println!("  specification_current = {:?}", specification_current);
        
        // Check convergence
        let xyy_check = munsell_specification_to_xyy(&specification_current)?;
        let x_check = xyy_check[0];
        let y_check = xyy_check[1];
        
        let difference = euclidean_distance([x, y], [x_check, y_check]);
        println!("\nLine 2354: Convergence check");
        println!("  Target: x={}, y={}", x, y);
        println!("  Current: x={}, y={}", x_check, y_check);
        println!("  difference = {}", difference);
        println!("  threshold = {}", convergence_threshold);
        println!("  converged = {}", difference < convergence_threshold);
        
        if difference < convergence_threshold {
            println!("\n{}", "=".repeat(60));
            println!("CONVERGED at iteration {}", iterations);
            println!("{}", "=".repeat(60));
            break;
        }
        
        // Limit output for readability
        if iterations >= 3 {
            println!("\n[Stopping detailed trace after 3 iterations for brevity]");
            break;
        }
    }
    
    // Final result
    let result = normalise_munsell_specification(&specification_current);
    println!("\nFINAL RESULT: {:?}", result);
    Ok(result)
}

// Helper function for chromatic adaptation
fn chromatic_adaptation_vonkries(xyz: [f64; 3], _from_illuminant: &str, _to_illuminant: &str) -> [f64; 3] {
    // Simplified version - in reality this would do full CAT02 transformation
    // For now just return the input (assuming illuminants are close)
    xyz
}

fn main() -> Result<()> {
    // Test RGB(187,255,153)
    let rgb = [187.0 / 255.0, 255.0 / 255.0, 153.0 / 255.0];
    println!("Testing RGB: [187, 255, 153]");
    println!("Expected: 8.5GY 9.4/12.8");
    
    // Convert RGB to XYZ
    let xyz = srgb_to_xyz(rgb);
    println!("\nXYZ: {:?}", xyz);
    
    // Convert XYZ to xyY
    let xyy = xyz_to_xyy(xyz);
    println!("xyY: {:?}", xyy);
    
    // Run conversion with tracing
    let result = traced_xyy_to_munsell_specification(xyy)?;
    
    // Format as Munsell string
    let hue_names = ["PB", "B", "BG", "G", "GY", "Y", "YR", "R", "RP", "P"];
    let code = result[3] as usize;
    let hue_name = if code < hue_names.len() { hue_names[code] } else { "??" };
    
    println!("\n{}", "=".repeat(80));
    println!("FINAL MUNSELL: {:.1}{} {:.1}/{:.1}", 
             result[0], hue_name, result[1], result[2]);
    println!("{}", "=".repeat(80));
    
    Ok(())
}