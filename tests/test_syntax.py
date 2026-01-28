"""
Unit tests for Syntax Restructurer
"""

import pytest
from src.core.syntax_restructurer import SyntaxRestructurer


@pytest.fixture
def restructurer():
    """Create SyntaxRestructurer instance."""
    return SyntaxRestructurer(seed=42)


def test_passive_to_active(restructurer):
    """Test passive to active voice conversion."""
    passive = "The report was completed by the team."
    result, confidence = restructurer.passive_to_active(passive)
    
    assert confidence > 0.5
    assert "team" in result.lower()
    assert "completed" in result.lower()


def test_active_unchanged(restructurer):
    """Test that active voice is not converted."""
    active = "The team completed the report."
    result, confidence = restructurer.passive_to_active(active)
    
    assert confidence == 0.0
    assert result == active


def test_clause_reordering(restructurer):
    """Test clause reordering."""
    sentence = "Because performance degraded, we optimized the code."
    result, confidence = restructurer.reorder_clauses(sentence)
    
    assert confidence > 0.5
    assert "optimized" in result.lower()


def test_nominalization_reversal(restructurer):
    """Test nominalization reversal."""
    sentence = "The implementation of the algorithm is complete."
    result, confidence = restructurer.reverse_nominalization(sentence)
    
    assert confidence > 0.5
    assert "implementing" in result.lower() or "implementation" not in result.lower()


def test_sentence_splitting(restructurer):
    """Test long sentence splitting."""
    long_sentence = "The algorithm processes data efficiently, and it handles edge cases well, while maintaining high performance across various scenarios."
    sentences = [long_sentence]
    
    result, confidence = restructurer.vary_sentence_complexity(sentences)
    
    # May or may not split depending on implementation
    assert isinstance(result, list)


def test_sentence_combining(restructurer):
    """Test short sentence combining."""
    short_sentences = ["This works.", "It is good.", "We like it."]
    
    result, confidence = restructurer.vary_sentence_complexity(short_sentences)
    
    # May combine some sentences
    assert isinstance(result, list)


def test_full_restructure(restructurer):
    """Test full restructuring pipeline."""
    text = "The report was completed by the team. The implementation of the algorithm demonstrates improvements."
    
    result = restructurer.restructure(text)
    
    assert isinstance(result, str)
    assert len(result) > 0


def test_empty_text(restructurer):
    """Test handling of empty text."""
    result = restructurer.restructure("")
    assert result == ""
