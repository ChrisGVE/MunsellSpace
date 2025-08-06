#!/usr/bin/env python3
"""Check maximum chroma for green spec"""

# Check maximum chroma for hue=7.877 GY, value=8
# The spec is [7.877, 8.0, 22.595, 4]

from colour.notation.munsell.renotation import \
    maximum_chroma_from_renotation

# Check maximum chroma
hue = 7.877
value = 8.0
code = 4  # GY

max_chroma = maximum_chroma_from_renotation(hue, value, code)
print(f"Maximum chroma for hue={hue:.3f} value={value} code={code}: {max_chroma}")

# Try 7.5GY instead
hue = 7.5
max_chroma = maximum_chroma_from_renotation(hue, value, code)
print(f"Maximum chroma for hue={hue:.3f} value={value} code={code}: {max_chroma}")

# Try value 9
value = 9.0
hue = 7.877
max_chroma = maximum_chroma_from_renotation(hue, value, code)
print(f"Maximum chroma for hue={hue:.3f} value={value} code={code}: {max_chroma}")