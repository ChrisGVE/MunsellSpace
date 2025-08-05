#!/bin/bash
# Test single color RGB [68,0,68] with debug output
export DEBUG_MUNSELL=1
echo "68,0,68" | cargo run --release --bin mathematical_convert_rgb 2>&1 | head -100