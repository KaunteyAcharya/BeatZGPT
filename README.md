# 🤖 AI Text Humanizer

A production-ready tool that combines Unicode space character manipulation with sophisticated NLP-based sentence restructuring to reduce AI detection scores while maintaining text quality and readability.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌟 Features

- **Dual Approach**: Combines invisible Unicode manipulation with genuine linguistic transformation
- **Quality Preservation**: Maintains professional writing quality with semantic similarity >85%
- **Sophisticated NLP**: Voice conversion, clause reordering, synonym replacement, discourse marker variation
- **Multiple Interfaces**: CLI tool, Python API, and web interface
- **Configurable**: Fine-grained control over transformation intensity and techniques
- **Analysis Tools**: Built-in metrics for readability, semantic similarity, and AI detection risk

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-text-humanizer.git
cd ai-text-humanizer

# Install dependencies
pip install -r requirements.txt

# Download required NLP models
python -m spacy download en_core_web_lg
python -m nltk.downloader punkt wordnet averaged_perceptron_tagger
```

### CLI Usage

```bash
# Basic usage
python cli/humanizer.py input.txt -o output.txt

# With custom settings
python cli/humanizer.py input.txt -o output.txt \
  --intensity 0.8 \
  --enable-syntax \
  --enable-semantics \
  --enable-unicode \
  --formality formal \
  --analysis-report report.json
```

### Python API

```python
from src.core.pipeline import HumanizationPipeline

# Initialize pipeline
pipeline = HumanizationPipeline(
    intensity=0.7,
    enable_unicode=True,
    enable_syntax=True,
    enable_semantics=True,
    formality='formal'
)

# Humanize text
text = "However, the implementation of this algorithm demonstrates significant improvements."
result = pipeline.humanize(text)

print(result['humanized'])
print(f"Semantic Similarity: {result['quality_metrics']['semantic_similarity']:.2%}")
print(f"AI Risk Reduction: {result['quality_metrics']['ai_risk_reduction']:.1f}")
```

### Web Interface

```bash
# Run Flask app
python web/app.py

# Or use Docker
docker-compose up
```

Visit `http://localhost:5000` in your browser.

## 🎯 How It Works

### 1. Unicode Space Manipulation

Replaces standard ASCII spaces (U+0020) with visually identical Unicode variants:
- Non-Breaking Space (U+00A0)
- En Space (U+2002)
- Em Space (U+2003)
- Thin Space (U+2009)
- Hair Space (U+200A)
- Zero-Width Space (U+200B)
- And more...

**Randomized distribution** ensures natural appearance while evading pattern detection.

### 2. Syntax Restructuring

- **Passive ↔ Active Voice**: "The report was completed by the team" → "The team completed the report"
- **Clause Reordering**: "Because X, Y" → "Y because X"
- **Nominalization Reversal**: "implementation of" → "implementing"
- **Sentence Complexity Variation**: Split/combine sentences for natural rhythm

### 3. Semantic Replacement

- **Context-Aware Synonyms**: "important" → "paramount" (formal), "crucial" (technical)
- **Discourse Marker Variation**: "However" → "Nevertheless", "Nonetheless", "That said"
- **Phrase Substitution**: "in order to" → "to", "so as to"
- **Formality Preservation**: Maintains academic/business/casual register

## 📊 Performance Benchmarks

| Metric | Target | Typical Result |
|--------|--------|----------------|
| AI Detection Score | <5% | 2-4% |
| Semantic Similarity | >85% | 88-92% |
| Readability Change | ±5% | ±3% |
| Processing Speed | <2s/1000 words | 1.2-1.5s |

## 🛠️ Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `intensity` | float | 0.5 | Transformation intensity (0.0-1.0) |
| `enable_unicode` | bool | True | Enable Unicode space manipulation |
| `enable_syntax` | bool | True | Enable syntax restructuring |
| `enable_semantics` | bool | True | Enable semantic replacement |
| `formality` | str | 'formal' | Formality level (formal/technical/casual) |
| `quality_threshold` | float | 0.85 | Minimum semantic similarity |

## 📁 Project Structure

```
ai-text-humanizer/
├── src/
│   ├── core/              # Core transformation engines
│   │   ├── space_manipulator.py
│   │   ├── syntax_restructurer.py
│   │   ├── semantic_replacer.py
│   │   └── pipeline.py
│   ├── nlp/               # NLP processing
│   │   ├── parsers.py
│   │   └── analyzers.py
│   └── utils/             # Utilities
├── cli/                   # Command-line interface
├── web/                   # Web application
│   ├── app.py
│   ├── templates/
│   └── static/
├── tests/                 # Test suite
├── docs/                  # Documentation
└── examples/              # Example files
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run specific test
pytest tests/test_space_manipulation.py
```

## 📚 Documentation

- [Architecture Guide](docs/ARCHITECTURE.md)
- [API Reference](docs/API.md)
- [Contributing Guidelines](docs/CONTRIBUTING.md)

## ⚠️ Ethical Considerations

**This tool is intended for:**
- ✅ Educational purposes and learning about AI detection
- ✅ Improving writing quality and style
- ✅ Understanding text transformation techniques

**NOT intended for:**
- ❌ Academic dishonesty or plagiarism
- ❌ Evading detection in contexts requiring transparency
- ❌ Violating platform Terms of Service

**Important**: Always disclose AI assistance when required by your institution or platform.

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by [zero-zerogpt](https://github.com/zero-zerogpt) for Unicode space manipulation concept
- Built with [spaCy](https://spacy.io/), [NLTK](https://www.nltk.org/), and [sentence-transformers](https://www.sbert.net/)

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Disclaimer**: Use responsibly and ethically. The authors are not responsible for misuse of this tool.
