# Contributing to MunsellSpace 🤝

Thank you for your interest in contributing to MunsellSpace! This document provides guidelines and information for contributors.

## Code of Conduct

This project adheres to a code of conduct that we expect all participants to uphold. Please be respectful and professional in all interactions.

## How to Contribute

### Reporting Issues

- Use the GitHub issue tracker to report bugs or request features
- Search existing issues before creating a new one
- Provide detailed information including:
  - Steps to reproduce the issue
  - Expected vs actual behavior
  - Environment details (OS, Rust/Python version, etc.)
  - Sample code if applicable

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/MunsellSpace.git
   cd MunsellSpace
   ```

2. **Rust Development**
   ```bash
   # Install Rust if needed
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   
   # Build and test
   cargo build
   cargo test
   ```

3. **Python Development**
   ```bash
   cd python
   pip install -e .[dev]
   pytest
   ```

### Making Changes

1. Create a feature branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following the coding standards below

3. Add tests for new functionality

4. Ensure all tests pass:
   ```bash
   cargo test
   cd python && pytest
   ```

5. Update documentation if needed

6. Commit your changes with a descriptive message

7. Push to your fork and create a pull request

## Coding Standards

### Rust

- Follow standard Rust formatting (`cargo fmt`)
- Run clippy and fix warnings (`cargo clippy`)
- Add comprehensive documentation for public APIs
- Write unit tests for new functionality
- Consider performance implications for color conversion code

### Python

- Follow PEP 8 style guidelines
- Use type hints for all public APIs
- Add docstrings in Sphinx format
- Write unit tests using pytest
- Maintain compatibility with Python 3.8+

### Documentation

- Update README.md for user-facing changes
- Add docstring examples for new APIs
- Update CHANGELOG.md following semantic versioning
- Consider adding examples for significant features

## Testing

### Rust Tests
```bash
# Unit tests
cargo test

# Integration tests
cargo test --test integration

# Benchmark tests
cargo bench
```

### Python Tests
```bash
cd python
pytest
pytest --cov=munsellspace  # With coverage
```

### Accuracy Validation
```bash
# Validate against reference dataset
cargo run --bin validate_reference_dataset data/srgb-to-munsell.csv
```

## Performance Considerations

- Color conversion performance is critical
- Profile before optimizing
- Maintain the 99.98% accuracy requirement
- Consider memory usage for large batch operations
- Test with the full 4,007-color reference dataset

## Pull Request Process

1. Ensure your PR has a clear title and description
2. Reference any related issues
3. Include test coverage for new features
4. Update documentation as needed
5. Ensure CI passes (tests, formatting, clippy)
6. Be responsive to review feedback

## Release Process

Releases are handled by maintainers following semantic versioning:

- **Patch (1.0.1)**: Bug fixes, documentation updates
- **Minor (1.1.0)**: New features, backwards-compatible changes  
- **Major (2.0.0)**: Breaking changes

## Questions?

- Open a GitHub discussion for general questions
- Join our community discussions
- Review existing documentation and examples

Thank you for contributing to MunsellSpace! 🎨