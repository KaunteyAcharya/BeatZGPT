"""Utils module initialization."""

from .text_processing import (
    normalize_whitespace,
    preserve_formatting,
    split_into_chunks,
    clean_text
)

__all__ = [
    'normalize_whitespace',
    'preserve_formatting',
    'split_into_chunks',
    'clean_text'
]
