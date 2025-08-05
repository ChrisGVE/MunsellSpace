"""Trace Python's exact flow when phi_input ≈ phi_current"""

# When phi_input ≈ phi_current:
# 1. Hue refinement inner loop collects 2 points with phi_diff ≈ 0
# 2. Extrapolator returns hue_angle_difference_new ≈ 0
# 3. hue_new ≈ hue_current (no change in hue)
# 4. First convergence check - if already close enough, RETURN
# 5. If not converged, continue to chroma refinement
# 6. Chroma refinement adjusts chroma to get rho closer to rho_input
# 7. Second convergence check - if close enough, RETURN
# 8. Loop continues

print("Python's algorithm has TWO convergence checks per iteration:")
print("1. After hue refinement")
print("2. After chroma refinement")
print()
print("This means even if hue can't be refined further (phi_input ≈ phi_current),")
print("the algorithm can still make progress by refining chroma!")
print()
print("Our Rust implementation only has ONE convergence check at the end,")
print("so we miss the opportunity to converge after hue-only refinement.")