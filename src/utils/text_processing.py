"""Text processing utilities."""

import re
from typing import List


def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace while preserving paragraph breaks.
    
    Args:
        text: Input text
    
    Returns:
        Normalized text
    """
    # Replace multiple spaces with single space
    text = re.sub(r' +', ' ', text)
    
    # Preserve paragraph breaks (double newlines)
    text = re.sub(r'\n\n+', '\n\n', text)
    
    # Remove spaces at line starts/ends
    lines = text.split('\n')
    lines = [line.strip() for line in lines]
    
    return '\n'.join(lines)


def preserve_formatting(original: str, modified: str) -> str:
    """
    Apply modifications while preserving original formatting.
    
    Args:
        original: Original text with formatting
        modified: Modified text
    
    Returns:
        Modified text with original formatting preserved
    """
    # Simple approach: preserve leading/trailing whitespace
    # and paragraph structure
    
    orig_lines = original.split('\n')
    mod_lines = modified.split('\n')
    
    # If line counts match, preserve line-by-line formatting
    if len(orig_lines) == len(mod_lines):
        result = []
        for orig_line, mod_line in zip(orig_lines, mod_lines):
            # Preserve leading whitespace
            leading = len(orig_line) - len(orig_line.lstrip())
            result.append(' ' * leading + mod_line.strip())
        return '\n'.join(result)
    
    return modified


def split_into_chunks(text: str, max_chunk_size: int = 5000) -> List[str]:
    """
    Split text into chunks for processing.
    
    Args:
        text: Input text
        max_chunk_size: Maximum characters per chunk
    
    Returns:
        List of text chunks
    """
    # Split by paragraphs first
    paragraphs = text.split('\n\n')
    
    chunks = []
    current_chunk = []
    current_size = 0
    
    for para in paragraphs:
        para_size = len(para)
        
        if current_size + para_size > max_chunk_size and current_chunk:
            # Save current chunk
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = [para]
            current_size = para_size
        else:
            current_chunk.append(para)
            current_size += para_size
    
    # Add remaining chunk
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))
    
    return chunks


def clean_text(text: str) -> str:
    """
    Clean text by removing unwanted characters.
    
    Args:
        text: Input text
    
    Returns:
        Cleaned text
    """
    # Remove zero-width characters except those we intentionally add
    # (This is for cleaning input, not output)
    text = re.sub(r'[\u200B-\u200D\uFEFF]', '', text)
    
    # Normalize quotes
    text = text.replace('"', '"').replace('"', '"')
    text = text.replace(''', "'").replace(''', "'")
    
    return text
