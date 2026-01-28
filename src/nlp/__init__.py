"""NLP module initialization."""

from .parsers import NLPParser
from .analyzers import (
    ReadabilityAnalyzer,
    SemanticSimilarityChecker,
    AIDetectionEstimator,
    TextMetrics
)

__all__ = [
    'NLPParser',
    'ReadabilityAnalyzer',
    'SemanticSimilarityChecker',
    'AIDetectionEstimator',
    'TextMetrics'
]
