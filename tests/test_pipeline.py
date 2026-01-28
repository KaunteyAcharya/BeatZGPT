"""
Integration tests for Humanization Pipeline
"""

import pytest
from src.core.pipeline import HumanizationPipeline


@pytest.fixture
def pipeline():
    """Create pipeline instance."""
    return HumanizationPipeline(
        intensity=0.5,
        enable_unicode=True,
        enable_syntax=True,
        enable_semantics=True,
        seed=42
    )


def test_basic_humanization(pipeline):
    """Test basic humanization."""
    text = "However, the implementation of this algorithm demonstrates significant improvements."
    
    result = pipeline.humanize(text)
    
    assert 'original' in result
    assert 'humanized' in result
    assert 'quality_metrics' in result
    assert result['original'] == text
    assert len(result['humanized']) > 0


def test_quality_preservation(pipeline):
    """Test that quality metrics meet thresholds."""
    text = "The system was designed by the team to process data efficiently."
    
    result = pipeline.humanize(text)
    metrics = result['quality_metrics']
    
    # Check semantic similarity
    assert metrics['semantic_similarity'] >= 0.80
    
    # Check readability change is reasonable
    assert abs(metrics['readability_change']) <= 10.0


def test_transformations_applied(pipeline):
    """Test that transformations are tracked."""
    text = "However, the report was completed by the team."
    
    result = pipeline.humanize(text)
    
    assert 'transformations_applied' in result
    assert isinstance(result['transformations_applied'], list)


def test_empty_text(pipeline):
    """Test handling of empty text."""
    result = pipeline.humanize("")
    
    assert result['humanized'] == ""
    assert result['passed_quality_check'] == True


def test_unicode_only(pipeline):
    """Test Unicode-only transformation."""
    pipeline_unicode = HumanizationPipeline(
        intensity=0.5,
        enable_unicode=True,
        enable_syntax=False,
        enable_semantics=False,
        seed=42
    )
    
    text = "Hello world test example"
    result = pipeline_unicode.humanize(text)
    
    assert 'unicode_manipulation' in result['transformations_applied']
    assert len(result['transformations_applied']) == 1


def test_syntax_only(pipeline):
    """Test syntax-only transformation."""
    pipeline_syntax = HumanizationPipeline(
        intensity=0.5,
        enable_unicode=False,
        enable_syntax=True,
        enable_semantics=False,
        seed=42
    )
    
    text = "The report was completed by the team."
    result = pipeline_syntax.humanize(text)
    
    # May or may not apply syntax depending on confidence
    assert 'unicode_manipulation' not in result['transformations_applied']


def test_batch_processing(pipeline):
    """Test batch humanization."""
    texts = [
        "The system processes data efficiently.",
        "However, the implementation demonstrates improvements.",
        "The algorithm was designed by the team."
    ]
    
    results = pipeline.batch_humanize(texts, show_progress=False)
    
    assert len(results) == len(texts)
    assert all('humanized' in r for r in results)


def test_quality_threshold():
    """Test quality threshold enforcement."""
    # Very high threshold should cause rollback
    strict_pipeline = HumanizationPipeline(
        intensity=0.9,
        quality_threshold=0.99,
        seed=42
    )
    
    text = "The system was designed to process data."
    result = strict_pipeline.humanize(text)
    
    # May rollback if transformations are too aggressive
    assert 'quality_metrics' in result


def test_different_intensities():
    """Test different intensity levels."""
    text = "However, the implementation demonstrates significant improvements."
    
    for intensity in [0.3, 0.5, 0.8]:
        pipeline = HumanizationPipeline(intensity=intensity, seed=42)
        result = pipeline.humanize(text)
        
        assert result['humanized'] is not None
        assert 'quality_metrics' in result
