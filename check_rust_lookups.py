"""Check what Rust is looking up"""

# Our debug output shows:
# For 4.13R 4.0/18.0:
#   Boundaries: cw=2.5R, ccw=5R
#   Minus (cw): xy=(0.589800, 0.262200)
#   Plus (ccw): xy=(0.632900, 0.288100)

# CHROMA INTERPOLATION RESULT:
#   Lower (chroma 18): xy=(0.589800, 0.262200)
#   Upper (chroma 20): xy=(0.615000, 0.253000)
#   t=0.079659, result: xy=(0.591807, 0.261467)

# So the issue is: Why is lower chroma 18 giving (0.589800, 0.262200)?
# That's exactly the value for 2.5R 4.0/18.0!

# It seems like for chroma 18, when looking up non-standard hue 4.13R,
# it's returning the cw boundary value (2.5R) instead of interpolating

print("The problem:")
print("For 4.13R 4.0/18.0, Rust is returning:")
print("  xy=(0.589800, 0.262200) which is exactly 2.5R 4.0/18.0")
print("\nIt should be returning:")
print("  xy=(0.617901, 0.279087) which is the interpolated value")
print("\nThis suggests xy_from_renotation_ovoid_for_even_chroma is")
print("not doing the hue interpolation correctly!")

# What about chroma 20?
print("\n\nFor chroma 20:")
print("Rust returns (0.615000, 0.253000) which is exactly 2.5R 4.0/20.0")
print("Should return (0.643036, 0.269300) which is interpolated")

print("\n\nConclusion: The bug is that xy_from_renotation_ovoid_for_even_chroma")
print("is returning the cw (minus) boundary value directly instead of")
print("interpolating between the boundaries!")