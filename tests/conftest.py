"""Test configuration and fixtures."""

import pytest


@pytest.fixture(scope="session")
def sample_texts():
    """Provide sample texts for testing."""
    return {
        'simple': "Hello world.",
        'passive': "The report was completed by the team.",
        'ai_typical': "However, the implementation demonstrates significant improvements.",
        'complex': "The system was designed by the team to address critical challenges in data processing.",
        'multi_sentence': "This is sentence one. This is sentence two. This is sentence three."
    }
