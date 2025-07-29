# MunsellSpace Python Package 🎨

[![PyPI version](https://badge.fury.io/py/munsellspace.svg)](https://badge.fury.io/py/munsellspace)
[![Python](https://img.shields.io/pypi/pyversions/munsellspace.svg)](https://pypi.org/project/munsellspace/)
[![License](https://img.shields.io/pypi/l/munsellspace.svg)](https://github.com/chrisgve/MunsellSpace/blob/main/LICENSE)
[![Downloads](https://pepy.tech/badge/munsellspace)](https://pepy.tech/project/munsellspace)

High-precision **sRGB to Munsell color space conversion** with **99.98% reference accuracy**.

This Python package provides bindings to the Rust MunsellSpace library, offering the most accurate open-source implementation for converting RGB colors to Munsell notation, validated against the complete 4,007-color reference dataset.

## ✨ Features

- **99.98% Accuracy**: Validated against complete reference dataset (4,006/4,007 exact matches)
- **High Performance**: 4,000+ colors/second batch processing
- **Scientific Precision**: Reference data lookup with intelligent interpolation
- **Zero Dependencies**: Pure implementation with minimal external requirements  
- **Easy Installation**: Simple pip install with automatic Rust binary compilation
- **Comprehensive Documentation**: Full API documentation with examples
- **Type Hints**: Complete type annotations for better IDE support

## 🚀 Installation

Install from PyPI:

```bash
pip install munsellspace
```

**Requirements:**
- Python 3.8+
- Rust (automatically handled during installation)
- No additional Python dependencies

## 📖 Quick Start

### Basic Usage

```python
import munsellspace

# Create converter
converter = munsellspace.MunsellConverter()

# Convert single color
red = converter.srgb_to_munsell([255, 0, 0])
print(f"Pure red: {red}")  # Output: Pure red: 7.9R 5.2/20.5

# Check if color is neutral (achromatic)
gray = converter.srgb_to_munsell([128, 128, 128])
if gray.is_neutral():
    print(f"Neutral gray: {gray}")  # Output: Neutral gray: N 5.6/
```

### Batch Processing

For better performance when converting multiple colors:

```python
# Convert multiple colors efficiently
colors = [
    [255, 0, 0],    # Red
    [0, 255, 0],    # Green  
    [0, 0, 255],    # Blue
    [255, 255, 0],  # Yellow
    [128, 128, 128] # Gray
]

results = converter.convert_batch(colors)
for rgb, munsell in zip(colors, results):
    print(f"RGB{rgb} -> {munsell}")

# Output:
# RGB[255, 0, 0] -> 7.9R 5.2/20.5
# RGB[0, 255, 0] -> 9.9GY 8.8/19.4  
# RGB[0, 0, 255] -> 7.3PB 3.2/25.5
# RGB[255, 255, 0] -> 2.8Y 9.1/14.3
# RGB[128, 128, 128] -> N 5.6/
```

For more examples and detailed documentation, see the complete README in the parent repository.