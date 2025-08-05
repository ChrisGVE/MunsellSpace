[38;2;127;132;156m   1[0m [38;2;205;214;244mimport subprocess[0m
[38;2;127;132;156m   2[0m [38;2;205;214;244mimport json[0m
[38;2;127;132;156m   3[0m 
[38;2;127;132;156m   4[0m [38;2;205;214;244m# Test specific RGB that we know is problematic[0m
[38;2;127;132;156m   5[0m [38;2;205;214;244mrgb = [238, 0, 85][0m
[38;2;127;132;156m   6[0m [38;2;205;214;244mprint(f"Testing RGB {rgb}")[0m
[38;2;127;132;156m   7[0m 
[38;2;127;132;156m   8[0m [38;2;205;214;244m# Run through Rust[0m
[38;2;127;132;156m   9[0m [38;2;205;214;244mrust_result = subprocess.run([0m
[38;2;127;132;156m  10[0m [38;2;205;214;244m    ['./target/release/mathematical_convert_rgb'] + [str(c) for c in rgb],[0m
[38;2;127;132;156m  11[0m [38;2;205;214;244m    capture_output=True,[0m
[38;2;127;132;156m  12[0m [38;2;205;214;244m    text=True[0m
[38;2;127;132;156m  13[0m [38;2;205;214;244m)[0m
[38;2;127;132;156m  14[0m 
[38;2;127;132;156m  15[0m [38;2;205;214;244mif rust_result.returncode == 0:[0m
[38;2;127;132;156m  16[0m [38;2;205;214;244m    rust_output = rust_result.stdout.strip()[0m
[38;2;127;132;156m  17[0m [38;2;205;214;244m    print(f"Rust output: {rust_output}")[0m
[38;2;127;132;156m  18[0m [38;2;205;214;244melse:[0m
[38;2;127;132;156m  19[0m [38;2;205;214;244m    print(f"Rust error: {rust_result.stderr}")[0m
[38;2;127;132;156m  20[0m 
[38;2;127;132;156m  21[0m [38;2;205;214;244m# Compare with Python[0m
[38;2;127;132;156m  22[0m [38;2;205;214;244mimport colour[0m
[38;2;127;132;156m  23[0m [38;2;205;214;244mmunsell_py = colour.sRGB_to_munsell(rgb)[0m
[38;2;127;132;156m  24[0m [38;2;205;214;244mprint(f"Python output: {munsell_py}")[0m
[38;2;127;132;156m  25[0m 
[38;2;127;132;156m  26[0m [38;2;205;214;244m# Also test the color that was working[0m
[38;2;127;132;156m  27[0m [38;2;205;214;244mprint("\nTesting RGB [68,0,68] which was working correctly:")[0m
[38;2;127;132;156m  28[0m [38;2;205;214;244mrgb2 = [68, 0, 68][0m
[38;2;127;132;156m  29[0m [38;2;205;214;244mrust_result2 = subprocess.run([0m
[38;2;127;132;156m  30[0m [38;2;205;214;244m    ['./target/release/mathematical_convert_rgb'] + [str(c) for c in rgb2],[0m
[38;2;127;132;156m  31[0m [38;2;205;214;244m    capture_output=True,[0m
[38;2;127;132;156m  32[0m [38;2;205;214;244m    text=True[0m
[38;2;127;132;156m  33[0m [38;2;205;214;244m)[0m
[38;2;127;132;156m  34[0m [38;2;205;214;244mif rust_result2.returncode == 0:[0m
[38;2;127;132;156m  35[0m [38;2;205;214;244m    print(f"Rust output: {rust_result2.stdout.strip()}")[0m
[38;2;127;132;156m  36[0m [38;2;205;214;244mmunsell_py2 = colour.sRGB_to_munsell(rgb2)[0m
[38;2;127;132;156m  37[0m [38;2;205;214;244mprint(f"Python output: {munsell_py2}")[0m
[38;2;127;132;156m  38[0m [38;2;205;214;244mEOF < /dev/null[0m
