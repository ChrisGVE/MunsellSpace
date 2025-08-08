
import numpy as np
from traced_python_munsell import (
    traced_xyY_to_munsell_specification,
    save_trace_to_file,
    clear_trace,
    enable_tracing,
    apply_monkey_patches
)

# Enable tracing
enable_tracing()
apply_monkey_patches()
clear_trace()

# Convert directly from xyY
xyY = np.array([np.float64(0.3016555411), np.float64(0.3289901051), np.float64(0.8269331673)])
print("Input xyY:", xyY)

# Run conversion
result = traced_xyY_to_munsell_specification(xyY)
print("Result:", result)

# Save trace
save_trace_to_file("python_trace_aligned.txt")
print("Python trace saved to python_trace_aligned.txt")
