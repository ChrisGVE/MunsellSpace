# Contributing to MunsellSpace

Thank you for your interest in contributing to MunsellSpace! This document provides comprehensive guidelines for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)

## Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please:

- Be respectful and considerate in all interactions
- Welcome newcomers and help them get started
- Focus on constructive criticism and helpful feedback
- Respect differing viewpoints and experiences
- Accept responsibility for mistakes and learn from them

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/MunsellSpace.git
   cd MunsellSpace
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/chrisgve/MunsellSpace.git
   ```
4. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

### Prerequisites

- Rust 1.70 or later
- Cargo (comes with Rust)
- Git

### Building the Project

```bash
# Build in debug mode
cargo build

# Build in release mode
cargo build --release

# Run tests
cargo test

# Run benchmarks
cargo bench

# Check code formatting
cargo fmt --check

# Run linter
cargo clippy
```

## How to Contribute

### Types of Contributions

We welcome various types of contributions:

- **Bug Fixes**: Fix issues reported in the issue tracker
- **Features**: Implement new functionality or enhance existing features
- **Documentation**: Improve documentation, add examples, fix typos
- **Tests**: Add missing tests or improve test coverage
- **Performance**: Optimize algorithms or improve efficiency
- **Refactoring**: Improve code quality and maintainability

### Before You Start

1. **Check existing issues** to see if someone is already working on it
2. **Open an issue** to discuss significant changes before starting work
3. **Small fixes** (typos, obvious bugs) can be submitted directly

## Coding Standards

### Rust Style Guide

We follow the standard Rust style guide:

- Use `cargo fmt` to format code automatically
- Use `cargo clippy` to catch common mistakes
- Follow Rust naming conventions:
  - `snake_case` for functions, variables, and modules
  - `PascalCase` for types and traits
  - `SCREAMING_SNAKE_CASE` for constants

### Code Organization

```rust
// 1. Imports (grouped and sorted)
use std::collections::HashMap;
use std::sync::Arc;

use external_crate::Something;

use crate::module::Type;

// 2. Type definitions
pub struct ColorConverter {
    // fields
}

// 3. Implementations
impl ColorConverter {
    // Constructor first
    pub fn new() -> Self {
        // ...
    }
    
    // Public methods
    pub fn convert(&self) -> Result<Color> {
        // ...
    }
    
    // Private methods
    fn internal_helper(&self) {
        // ...
    }
}

// 4. Tests (in same file)
#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_conversion() {
        // ...
    }
}
```

### Documentation

All public APIs must have documentation:

```rust
/// Converts an sRGB color to Munsell notation.
///
/// # Arguments
///
/// * `rgb` - Array of [R, G, B] values in range 0-255
///
/// # Returns
///
/// Returns a `Result` containing the Munsell color or an error.
///
/// # Examples
///
/// ```
/// let converter = MunsellConverter::new()?;
/// let munsell = converter.srgb_to_munsell([255, 0, 0])?;
/// assert_eq!(munsell.to_string(), "7.9R 5.2/20.5");
/// ```
pub fn srgb_to_munsell(&self, rgb: [u8; 3]) -> Result<MunsellColor> {
    // ...
}
```

## Testing Guidelines

### Test Organization

- Unit tests go in the same file as the code they test
- Integration tests go in `tests/` directory
- Use descriptive test names that explain what is being tested

### Writing Tests

```rust
#[test]
fn test_rgb_to_munsell_pure_red() {
    let converter = MunsellConverter::new().unwrap();
    let result = converter.srgb_to_munsell([255, 0, 0]).unwrap();
    
    assert!(result.hue.unwrap().starts_with("R"));
    assert!((result.value - 5.2).abs() < 0.1);
    assert!((result.chroma.unwrap() - 20.5).abs() < 0.1);
}

#[test]
fn test_invalid_rgb_values() {
    let converter = MunsellConverter::new().unwrap();
    // RGB values are u8, so this test would need different approach
    // This is just an example of testing error conditions
}
```

### Test Coverage

- Aim for >80% code coverage
- Test edge cases and error conditions
- Include property-based tests where appropriate
- Add benchmarks for performance-critical code

## Documentation

### Code Documentation

- Document all public APIs
- Include examples in documentation
- Explain complex algorithms with comments
- Keep documentation up-to-date with code changes

### README Updates

When adding new features, update the README to include:
- Feature description in the features list
- Usage examples
- Any new dependencies or requirements

## Pull Request Process

### Before Submitting

1. **Update your branch** with latest upstream changes:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run all checks**:
   ```bash
   cargo fmt
   cargo clippy -- -D warnings
   cargo test
   cargo doc --no-deps
   ```

3. **Write clear commit messages**:
   ```
   feat: Add Lab color space support
   
   - Implement Lab to Munsell conversion
   - Add tests for Lab conversion
   - Update documentation
   
   Closes #123
   ```

### Commit Message Format

We use conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Formatting, missing semicolons, etc.
- `refactor:` Code restructuring
- `test:` Adding tests
- `perf:` Performance improvements
- `chore:` Maintenance tasks

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added new tests
- [ ] Updated documentation

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
```

### Review Process

1. Submit your pull request
2. Wait for automated checks to pass
3. Address reviewer feedback
4. Once approved, maintainers will merge

## Reporting Issues

### Bug Reports

When reporting bugs, please include:

- **Description**: Clear description of the bug
- **Reproduction**: Steps to reproduce the issue
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Environment**: Rust version, OS, etc.
- **Code sample**: Minimal example that reproduces the issue

### Feature Requests

For feature requests, please provide:

- **Use case**: Why is this feature needed?
- **Proposed solution**: How might it work?
- **Alternatives**: Other solutions you've considered
- **Additional context**: Any relevant information

## Questions?

If you have questions about contributing:

1. Check the [documentation](https://docs.rs/munsellspace)
2. Search [existing issues](https://github.com/chrisgve/MunsellSpace/issues)
3. Open a [discussion](https://github.com/chrisgve/MunsellSpace/discussions)
4. Contact the maintainers

## Recognition

Contributors are recognized in:
- The project's contributors list
- Release notes for significant contributions
- Special thanks in documentation for major features

Thank you for contributing to MunsellSpace! Your efforts help make color science more accessible to the Rust community.