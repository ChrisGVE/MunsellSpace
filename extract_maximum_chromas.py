#!/usr/bin/env python3
"""Extract maximum chromas data from Python colour-science"""

import colour.notation.munsell as munsell

# Get the maximum chromas data
max_chromas = munsell._munsell_maximum_chromas_from_renotation()

print("//! Maximum chromas from Munsell renotation data")
print("//! Auto-generated from Python colour-science library")
print()
print("/// Maximum chromas: ((hue, value, code), max_chroma)")
print("pub const MAXIMUM_CHROMAS: &[((f64, f64, u8), f64)] = &[")

for (hue, value, code), chroma in max_chromas:
    print(f"    (({hue}, {value}, {int(code)}), {chroma}),")

print("];")
print()
print(f"// Total entries: {len(max_chromas)}")