# Changelog

All notable changes to MunsellSpace will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial repository structure
- Comprehensive documentation for both Rust and Python APIs

## [1.0.0] - 2024-07-29

### Added
- High-precision sRGB to Munsell color space conversion
- 99.98% accuracy validated against 4,007-color reference dataset
- Rust crate with comprehensive API documentation
- Python package with PyPI-compatible documentation
- CLI binary for command-line color conversion
- Batch processing support for high-performance applications
- Comprehensive test suite with reference data validation
- Complete documentation with examples and API reference
- MIT license for open-source distribution

### Features
- **Rust Library**: Complete `munsellspace` crate with docs.rs documentation
- **Python Package**: Full PyPI package with Sphinx-style documentation
- **High Performance**: 4,000+ colors/second batch processing
- **Scientific Accuracy**: Reference data lookup with intelligent interpolation
- **Type Safety**: Full type annotations for both Rust and Python APIs
- **CLI Tool**: Command-line interface for interactive color conversion
- **Zero Dependencies**: Pure implementation with minimal external requirements

### Performance
- Single conversion: <1ms per color
- Batch processing: 4,000+ colors/second
- Memory usage: <100MB for complete reference dataset
- Accuracy: 99.98% exact matches on reference data (4,006/4,007)

### Documentation
- Complete README with installation and usage examples
- API documentation for all public interfaces
- Contributing guidelines and development setup
- Examples for common use cases
- Scientific background on Munsell color system