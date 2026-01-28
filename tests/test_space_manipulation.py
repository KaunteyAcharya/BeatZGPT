"""
Unit tests for Unicode Space Manipulator
"""

import pytest
from src.core.space_manipulator import SpaceManipulator


def test_initialization():
    """Test SpaceManipulator initialization."""
    manipulator = SpaceManipulator(intensity=0.5)
    assert manipulator.intensity == 0.5
    
    # Test invalid intensity
    with pytest.raises(ValueError):
        SpaceManipulator(intensity=1.5)


def test_space_replacement():
    """Test basic space replacement."""
    manipulator = SpaceManipulator(intensity=1.0, seed=42)
    text = "Hello world test"
    result = manipulator.replace_spaces(text)
    
    # Should have replaced some spaces
    assert result != text
    # Should have same visible length
    assert len(result) == len(text)


def test_intensity_zero():
    """Test that intensity=0 doesn't change text."""
    manipulator = SpaceManipulator(intensity=0.0)
    text = "Hello world test"
    result = manipulator.replace_spaces(text)
    
    assert result == text


def test_intensity_one():
    """Test that intensity=1.0 replaces all spaces."""
    manipulator = SpaceManipulator(intensity=1.0, seed=42)
    text = "Hello world test"
    result = manipulator.replace_spaces(text, preserve_boundaries=False)
    
    # Count standard spaces
    standard_space = '\u0020'
    assert result.count(standard_space) < text.count(standard_space)


def test_preserve_boundaries():
    """Test boundary preservation."""
    manipulator = SpaceManipulator(intensity=1.0, seed=42)
    text = " Hello world "
    result = manipulator.replace_spaces(text, preserve_boundaries=True)
    
    # First and last spaces should be preserved
    assert result[0] == ' '
    assert result[-1] == ' '


def test_distribution_analysis():
    """Test distribution analysis."""
    manipulator = SpaceManipulator(intensity=0.5, seed=42)
    text = "Hello world test example"
    result = manipulator.replace_spaces(text)
    
    distribution = manipulator.analyze_distribution(result)
    
    # Should have multiple space types
    total_spaces = sum(distribution.values())
    assert total_spaces == text.count(' ')


def test_replacement_stats():
    """Test replacement statistics."""
    manipulator = SpaceManipulator(intensity=0.5, seed=42)
    original = "Hello world test example"
    modified = manipulator.replace_spaces(original)
    
    stats = manipulator.get_replacement_stats(original, modified)
    
    assert 'total_spaces' in stats
    assert 'spaces_replaced' in stats
    assert 'replacement_rate' in stats
    assert stats['total_spaces'] == original.count(' ')


def test_reproducibility():
    """Test that same seed produces same results."""
    text = "Hello world test example"
    
    manipulator1 = SpaceManipulator(intensity=0.5, seed=42)
    result1 = manipulator1.replace_spaces(text)
    
    manipulator2 = SpaceManipulator(intensity=0.5, seed=42)
    result2 = manipulator2.replace_spaces(text)
    
    assert result1 == result2


def test_empty_text():
    """Test handling of empty text."""
    manipulator = SpaceManipulator(intensity=0.5)
    
    assert manipulator.replace_spaces("") == ""
    assert manipulator.replace_spaces("   ") != ""


def test_no_spaces():
    """Test text without spaces."""
    manipulator = SpaceManipulator(intensity=0.5)
    text = "HelloWorld"
    result = manipulator.replace_spaces(text)
    
    assert result == text
