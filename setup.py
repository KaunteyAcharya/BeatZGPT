from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-text-humanizer",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="AI text humanization tool combining Unicode manipulation with NLP-based restructuring",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ai-text-humanizer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Topic :: Text Processing :: Linguistic",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=[
        "spacy>=3.7.0",
        "nltk>=3.8.1",
        "textblob>=0.17.1",
        "sentence-transformers>=2.2.2",
        "flask>=3.0.0",
        "flask-cors>=4.0.0",
        "click>=8.1.7",
        "python-docx>=1.1.0",
        "fpdf2>=2.7.6",
        "textstat>=0.7.3",
        "language-tool-python>=2.7.1",
        "requests>=2.31.0",
        "tqdm>=4.66.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "humanizer=cli.humanizer:main",
        ],
    },
    include_package_data=True,
)
