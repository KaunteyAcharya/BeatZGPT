# Contributing to AI Text Humanizer

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help maintain a welcoming environment

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/ai-text-humanizer.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Run tests: `pytest tests/`
6. Commit: `git commit -m "Add your feature"`
7. Push: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8 mypy

# Download NLP models
python -m spacy download en_core_web_lg
python -m nltk.downloader punkt wordnet averaged_perceptron_tagger
```

## Code Style

- Follow PEP 8 guidelines
- Use Black for formatting: `black src/ cli/ web/`
- Use type hints where appropriate
- Write docstrings (Google style)

### Example:

```python
def transform_text(text: str, intensity: float = 0.5) -> str:
    """
    Transform text with specified intensity.
    
    Args:
        text: Input text to transform
        intensity: Transformation intensity (0.0 to 1.0)
    
    Returns:
        Transformed text
    
    Raises:
        ValueError: If intensity is out of range
    """
    pass
```

## Testing

- Write tests for new features
- Maintain >80% code coverage
- Run tests before submitting PR

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_space_manipulation.py
```

## Pull Request Guidelines

1. **Title**: Clear, descriptive title
2. **Description**: Explain what and why
3. **Tests**: Include tests for new features
4. **Documentation**: Update docs if needed
5. **Changelog**: Add entry to CHANGELOG.md

## Areas for Contribution

### High Priority
- [ ] Additional language support
- [ ] Performance optimizations
- [ ] More transformation techniques
- [ ] Improved quality metrics

### Medium Priority
- [ ] Browser extension
- [ ] API rate limiting
- [ ] Batch processing improvements
- [ ] Additional export formats

### Documentation
- [ ] Tutorial videos
- [ ] More examples
- [ ] Translation to other languages

## Reporting Issues

When reporting bugs, include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages/logs

## Feature Requests

For feature requests, describe:
- Use case
- Proposed solution
- Alternatives considered
- Additional context

## Questions?

Open an issue with the "question" label or start a discussion.

Thank you for contributing! 🎉
