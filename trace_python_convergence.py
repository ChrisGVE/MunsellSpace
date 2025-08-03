[38;2;127;132;156m   1[0m [38;2;205;214;244m#\!/usr/bin/env python3[0m
[38;2;127;132;156m   2[0m [38;2;205;214;244m"""Trace exact convergence behavior of Python algorithm."""[0m
[38;2;127;132;156m   3[0m 
[38;2;127;132;156m   4[0m [38;2;205;214;244mimport numpy as np[0m
[38;2;127;132;156m   5[0m [38;2;205;214;244mfrom colour import sRGB_to_XYZ, XYZ_to_xyY[0m
[38;2;127;132;156m   6[0m [38;2;205;214;244mfrom colour.notation.munsell import _xyY_to_munsell_specification[0m
[38;2;127;132;156m   7[0m 
[38;2;127;132;156m   8[0m [38;2;205;214;244m# Patch to add more detailed tracing[0m
[38;2;127;132;156m   9[0m [38;2;205;214;244mimport colour.notation.munsell as munsell[0m
[38;2;127;132;156m  10[0m 
[38;2;127;132;156m  11[0m [38;2;205;214;244m# Save original function[0m
[38;2;127;132;156m  12[0m [38;2;205;214;244moriginal_func = munsell._xyY_to_munsell_specification[0m
[38;2;127;132;156m  13[0m 
[38;2;127;132;156m  14[0m [38;2;205;214;244mdef traced_xyY_to_munsell_specification(xyY):[0m
[38;2;127;132;156m  15[0m [38;2;205;214;244m    """Traced version with debugging output."""[0m
[38;2;127;132;156m  16[0m [38;2;205;214;244m    from colour.notation.munsell_value import munsell_value_ASTM_D1535[0m
[38;2;127;132;156m  17[0m [38;2;205;214;244m    from colour.notation.munsell import (_munsell_specification_to_xyY,[0m
[38;2;127;132;156m  18[0m [38;2;205;214;244m                                          hue_angle_to_hue)[0m
[38;2;127;132;156m  19[0m [38;2;205;214;244m    [0m
[38;2;127;132;156m  20[0m [38;2;205;214;244m    # Get initial guess[0m
[38;2;127;132;156m  21[0m [38;2;205;214;244m    x, y, Y = xyY[0m
[38;2;127;132;156m  22[0m [38;2;205;214;244m    value = munsell_value_ASTM_D1535(Y * 100)[0m
[38;2;127;132;156m  23[0m [38;2;205;214;244m    [0m
[38;2;127;132;156m  24[0m [38;2;205;214;244m    # Check if achromatic[0m
[38;2;127;132;156m  25[0m [38;2;205;214;244m    x_center = 0.31006[0m
[38;2;127;132;156m  26[0m [38;2;205;214;244m    y_center = 0.31616[0m
[38;2;127;132;156m  27[0m [38;2;205;214;244m    chromaticity_distance = np.sqrt((x - x_center)**2 + (y - y_center)**2)[0m
[38;2;127;132;156m  28[0m [38;2;205;214;244m    [0m
[38;2;127;132;156m  29[0m [38;2;205;214;244m    print(f"Input xyY: [{x:.6f}, {y:.6f}, {Y:.6f}]")[0m
[38;2;127;132;156m  30[0m [38;2;205;214;244m    print(f"Value from ASTM D1535: {value:.6f}")[0m
[38;2;127;132;156m  31[0m [38;2;205;214;244m    print(f"Chromaticity distance from grey: {chromaticity_distance:.6f}")[0m
[38;2;127;132;156m  32[0m [38;2;205;214;244m    [0m
[38;2;127;132;156m  33[0m [38;2;205;214;244m    if chromaticity_distance < 1e-3:[0m
[38;2;127;132;156m  34[0m [38;2;205;214;244m        print("ACHROMATIC: returning neutral color")[0m
[38;2;127;132;156m  35[0m [38;2;205;214;244m        return np.array([0, value, 0, 0])[0m
[38;2;127;132;156m  36[0m [38;2;205;214;244m    [0m
[38;2;127;132;156m  37[0m [38;2;205;214;244m    # Initial guess from Lab[0m
[38;2;127;132;156m  38[0m [38;2;205;214;244m    from colour import XYZ_to_Lab, Lab_to_LCHab, xyY_to_XYZ[0m
[38;2;127;132;156m  39[0m [38;2;205;214;244m    XYZ = xyY_to_XYZ(xyY)[0m
[38;2;127;132;156m  40[0m [38;2;205;214;244m    illuminant = np.array([0.31006, 0.31616])[0m
[38;2;127;132;156m  41[0m [38;2;205;214;244m    Lab = XYZ_to_Lab(XYZ, illuminant)[0m
[38;2;127;132;156m  42[0m [38;2;205;214;244m    LCHab = Lab_to_LCHab(Lab)[0m
[38;2;127;132;156m  43[0m [38;2;205;214;244m    [0m
[38;2;127;132;156m  44[0m [38;2;205;214;244m    L, C, hab = LCHab[0m
[38;2;127;132;156m  45[0m [38;2;205;214;244m    print(f"\nInitial guess from Lab:")[0m
[38;2;127;132;156m  46[0m [38;2;205;214;244m    print(f"  Lab: L={L:.6f}, a={Lab[1]:.6f}, b={Lab[2]:.6f}")[0m
[38;2;127;132;156m  47[0m [38;2;205;214;244m    print(f"  LCHab: L={L:.6f}, C={C:.6f}, hab={hab:.6f}°")[0m
[38;2;127;132;156m  48[0m [38;2;205;214;244m    [0m
[38;2;127;132;156m  49[0m [38;2;205;214;244m    # LCHab to Munsell specification[0m
[38;2;127;132;156m  50[0m [38;2;205;214;244m    # Determine code from hab angle[0m
[38;2;127;132;156m  51[0m [38;2;205;214;244m    code = (7 if hab <= 36 else[0m
[38;2;127;132;156m  52[0m [38;2;205;214;244m            6 if hab <= 72 else[0m
[38;2;127;132;156m  53[0m [38;2;205;214;244m            5 if hab <= 108 else[0m
[38;2;127;132;156m  54[0m [38;2;205;214;244m            4 if hab <= 144 else[0m
[38;2;127;132;156m  55[0m [38;2;205;214;244m            3 if hab <= 180 else[0m
[38;2;127;132;156m  56[0m [38;2;205;214;244m            2 if hab <= 216 else[0m
[38;2;127;132;156m  57[0m [38;2;205;214;244m            1 if hab <= 252 else[0m
[38;2;127;132;156m  58[0m [38;2;205;214;244m            10 if hab <= 288 else[0m
[38;2;127;132;156m  59[0m [38;2;205;214;244m            9 if hab <= 324 else 8)[0m
[38;2;127;132;156m  60[0m [38;2;205;214;244m    [0m
[38;2;127;132;156m  61[0m [38;2;205;214;244m    # Calculate hue[0m
[38;2;127;132;156m  62[0m [38;2;205;214;244m    hab_mod = hab % 36[0m
[38;2;127;132;156m  63[0m [38;2;205;214;244m    hue = hab_mod * 10 / 36[0m
[38;2;127;132;156m  64[0m [38;2;205;214;244m    if hue == 0:[0m
[38;2;127;132;156m  65[0m [38;2;205;214;244m        hue = 10[0m
[38;2;127;132;156m  66[0m [38;2;205;214;244m    [0m
[38;2;127;132;156m  67[0m [38;2;205;214;244m    print(f"  Initial: hue={hue:.6f}, code={code}")[0m
[38;2;127;132;156m  68[0m [38;2;205;214;244m    [0m
[38;2;127;132;156m  69[0m [38;2;205;214;244m    # Scale chroma[0m
[38;2;127;132;156m  70[0m [38;2;205;214;244m    chroma_initial = C / 5[0m
[38;2;127;132;156m  71[0m [38;2;205;214;244m    chroma_scaled = (5/5.5) * chroma_initial[0m
[38;2;127;132;156m  72[0m [38;2;205;214;244m    [0m
[38;2;127;132;156m  73[0m [38;2;205;214;244m    print(f"  Chroma: C={C:.6f} -> initial={chroma_initial:.6f} -> scaled={chroma_scaled:.6f}")[0m
[38;2;127;132;156m  74[0m [38;2;205;214;244m    [0m
[38;2;127;132;156m  75[0m [38;2;205;214;244m    # Initial specification[0m
[38;2;127;132;156m  76[0m [38;2;205;214;244m    specification_current = np.array([hue, value, chroma_scaled, code])[0m
[38;2;127;132;156m  77[0m [38;2;205;214;244m    print(f"\nStarting iterations with: [{hue:.6f}, {value:.6f}, {chroma_scaled:.6f}, {code}]")[0m
[38;2;127;132;156m  78[0m [38;2;205;214;244m    [0m
[38;2;127;132;156m  79[0m [38;2;205;214;244m    # Run a few iterations to see convergence[0m
[38;2;127;132;156m  80[0m [38;2;205;214;244m    convergence_threshold = 1e-7[0m
[38;2;127;132;156m  81[0m [38;2;205;214;244m    [0m
[38;2;127;132;156m  82[0m [38;2;205;214;244m    for iteration in range(5):  # Just first 5 iterations[0m
[38;2;127;132;156m  83[0m [38;2;205;214;244m        x_current, y_current, _ = _munsell_specification_to_xyY(specification_current)[0m
[38;2;127;132;156m  84[0m [38;2;205;214;244m        difference = np.sqrt((x - x_current)**2 + (y - y_current)**2)[0m
[38;2;127;132;156m  85[0m [38;2;205;214;244m        [0m
[38;2;127;132;156m  86[0m [38;2;205;214;244m        print(f"\nIteration {iteration}:")[0m
[38;2;127;132;156m  87[0m [38;2;205;214;244m        print(f"  Current spec: [{specification_current[0]:.6f}, {specification_current[1]:.6f}, "[0m
[38;2;127;132;156m  88[0m [38;2;205;214;244m              f"{specification_current[2]:.6f}, {specification_current[3]:.0f}]")[0m
[38;2;127;132;156m  89[0m [38;2;205;214;244m        print(f"  Current xy: [{x_current:.6f}, {y_current:.6f}]")[0m
[38;2;127;132;156m  90[0m [38;2;205;214;244m        print(f"  Distance: {difference:.6f}")[0m
[38;2;127;132;156m  91[0m [38;2;205;214;244m        [0m
[38;2;127;132;156m  92[0m [38;2;205;214;244m        if difference < convergence_threshold:[0m
[38;2;127;132;156m  93[0m [38;2;205;214;244m            print("CONVERGED\!")[0m
[38;2;127;132;156m  94[0m [38;2;205;214;244m            return specification_current[0m
[38;2;127;132;156m  95[0m [38;2;205;214;244m            [0m
[38;2;127;132;156m  96[0m [38;2;205;214;244m        # Would continue iterating here...[0m
[38;2;127;132;156m  97[0m [38;2;205;214;244m    [0m
[38;2;127;132;156m  98[0m [38;2;205;214;244m    # Call original for full result[0m
[38;2;127;132;156m  99[0m [38;2;205;214;244m    return original_func(xyY)[0m
[38;2;127;132;156m 100[0m 
[38;2;127;132;156m 101[0m [38;2;205;214;244m# Apply patch[0m
[38;2;127;132;156m 102[0m [38;2;205;214;244mmunsell._xyY_to_munsell_specification = traced_xyY_to_munsell_specification[0m
[38;2;127;132;156m 103[0m 
[38;2;127;132;156m 104[0m [38;2;205;214;244m# Test[0m
[38;2;127;132;156m 105[0m [38;2;205;214;244mrgb = np.array([1.0, 0.0, 0.0])[0m
[38;2;127;132;156m 106[0m [38;2;205;214;244mxyz = sRGB_to_XYZ(rgb)[0m
[38;2;127;132;156m 107[0m [38;2;205;214;244mxyy = XYZ_to_xyY(xyz)[0m
[38;2;127;132;156m 108[0m 
[38;2;127;132;156m 109[0m [38;2;205;214;244mprint("="*60)[0m
[38;2;127;132;156m 110[0m [38;2;205;214;244mresult = _xyY_to_munsell_specification(xyy)[0m
[38;2;127;132;156m 111[0m [38;2;205;214;244mprint("="*60)[0m
[38;2;127;132;156m 112[0m [38;2;205;214;244mprint(f"\nFinal result: {result}")[0m
[38;2;127;132;156m 113[0m [38;2;205;214;244mprint(f"  Hue: {result[0]:.6f}")[0m
[38;2;127;132;156m 114[0m [38;2;205;214;244mprint(f"  Value: {result[1]:.6f}")[0m
[38;2;127;132;156m 115[0m [38;2;205;214;244mprint(f"  Chroma: {result[2]:.6f}")[0m
[38;2;127;132;156m 116[0m [38;2;205;214;244mprint(f"  Code: {result[3]:.0f}")[0m
[38;2;127;132;156m 117[0m 
[38;2;127;132;156m 118[0m [38;2;205;214;244m# Map code to family[0m
[38;2;127;132;156m 119[0m [38;2;205;214;244mfamilies = {1: 'BG', 2: 'G', 3: 'GY', 4: 'Y', 5: 'YR', 6: 'R', 7: 'RP', 8: 'P', 9: 'PB', 10: 'B'}[0m
[38;2;127;132;156m 120[0m [38;2;205;214;244mprint(f"  Family: {families[int(result[3])]}")[0m
