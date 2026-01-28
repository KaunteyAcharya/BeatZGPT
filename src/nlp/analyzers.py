"""
Text Analysis and Quality Metrics Module

Provides readability scoring, semantic similarity checking,
and AI detection risk estimation.
"""

import textstat
from typing import Dict, Optional
from sentence_transformers import SentenceTransformer, util
import torch


class ReadabilityAnalyzer:
    """Analyzes text readability using various metrics."""
    
    @staticmethod
    def analyze(text: str) -> Dict[str, float]:
        """
        Calculate readability metrics.
        
        Args:
            text: Input text
        
        Returns:
            Dictionary with readability scores
        """
        return {
            'flesch_reading_ease': textstat.flesch_reading_ease(text),
            'flesch_kincaid_grade': textstat.flesch_kincaid_grade(text),
            'gunning_fog': textstat.gunning_fog(text),
            'smog_index': textstat.smog_index(text),
            'automated_readability_index': textstat.automated_readability_index(text),
            'coleman_liau_index': textstat.coleman_liau_index(text),
            'dale_chall_readability': textstat.dale_chall_readability_score(text),
        }
    
    @staticmethod
    def compare(original: str, modified: str) -> Dict[str, any]:
        """
        Compare readability between original and modified text.
        
        Args:
            original: Original text
            modified: Modified text
        
        Returns:
            Comparison statistics
        """
        orig_scores = ReadabilityAnalyzer.analyze(original)
        mod_scores = ReadabilityAnalyzer.analyze(modified)
        
        # Calculate differences
        differences = {}
        for key in orig_scores:
            diff = mod_scores[key] - orig_scores[key]
            pct_change = (diff / orig_scores[key] * 100) if orig_scores[key] != 0 else 0
            differences[key] = {
                'original': orig_scores[key],
                'modified': mod_scores[key],
                'difference': diff,
                'percent_change': pct_change
            }
        
        return differences


class SemanticSimilarityChecker:
    """Checks semantic similarity between texts using sentence embeddings."""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize similarity checker.
        
        Args:
            model_name: Sentence transformer model name
        """
        try:
            self.model = SentenceTransformer(model_name)
        except Exception as e:
            print(f"Warning: Could not load sentence transformer model: {e}")
            self.model = None
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate cosine similarity between two texts.
        
        Args:
            text1: First text
            text2: Second text
        
        Returns:
            Similarity score (0.0 to 1.0)
        """
        if self.model is None:
            return 0.0
        
        # Generate embeddings
        embedding1 = self.model.encode(text1, convert_to_tensor=True)
        embedding2 = self.model.encode(text2, convert_to_tensor=True)
        
        # Calculate cosine similarity
        similarity = util.cos_sim(embedding1, embedding2)
        
        return float(similarity.item())
    
    def calculate_sentence_similarities(self, original_sentences: list, 
                                       modified_sentences: list) -> Dict[str, any]:
        """
        Calculate similarity for each sentence pair.
        
        Args:
            original_sentences: List of original sentences
            modified_sentences: List of modified sentences
        
        Returns:
            Detailed similarity statistics
        """
        if self.model is None or not original_sentences or not modified_sentences:
            return {'average_similarity': 0.0, 'min_similarity': 0.0, 'max_similarity': 0.0}
        
        similarities = []
        
        # Compare sentence by sentence
        for orig, mod in zip(original_sentences, modified_sentences):
            sim = self.calculate_similarity(orig, mod)
            similarities.append(sim)
        
        return {
            'average_similarity': sum(similarities) / len(similarities) if similarities else 0.0,
            'min_similarity': min(similarities) if similarities else 0.0,
            'max_similarity': max(similarities) if similarities else 0.0,
            'sentence_similarities': similarities,
        }


class AIDetectionEstimator:
    """Estimates AI detection risk using heuristic analysis."""
    
    # Common AI writing patterns
    AI_PATTERNS = [
        'however', 'therefore', 'additionally', 'furthermore', 'moreover',
        'in conclusion', 'it is important to note', 'it should be noted',
        'significantly', 'notably', 'essentially', 'particularly',
    ]
    
    @staticmethod
    def estimate_risk(text: str) -> Dict[str, any]:
        """
        Estimate AI detection risk based on heuristics.
        
        Args:
            text: Input text
        
        Returns:
            Risk assessment
        """
        text_lower = text.lower()
        
        # Count AI-typical patterns
        pattern_count = sum(1 for pattern in AIDetectionEstimator.AI_PATTERNS 
                          if pattern in text_lower)
        
        # Calculate pattern density
        words = text.split()
        word_count = len(words)
        pattern_density = pattern_count / word_count if word_count > 0 else 0
        
        # Sentence length variance (AI tends to be more uniform)
        sentences = text.split('.')
        sentence_lengths = [len(s.split()) for s in sentences if s.strip()]
        
        if len(sentence_lengths) > 1:
            avg_length = sum(sentence_lengths) / len(sentence_lengths)
            variance = sum((l - avg_length) ** 2 for l in sentence_lengths) / len(sentence_lengths)
            std_dev = variance ** 0.5
            coefficient_of_variation = std_dev / avg_length if avg_length > 0 else 0
        else:
            coefficient_of_variation = 0
        
        # Calculate risk score (0-100)
        # Higher pattern density = higher risk
        # Lower sentence variation = higher risk
        pattern_risk = min(pattern_density * 1000, 50)  # Cap at 50
        uniformity_risk = max(0, 50 - (coefficient_of_variation * 100))  # Cap at 50
        
        total_risk = pattern_risk + uniformity_risk
        
        return {
            'risk_score': min(total_risk, 100),
            'pattern_count': pattern_count,
            'pattern_density': pattern_density,
            'sentence_length_variance': coefficient_of_variation,
            'assessment': 'High' if total_risk > 70 else 'Medium' if total_risk > 40 else 'Low',
        }


class TextMetrics:
    """General text statistics."""
    
    @staticmethod
    def analyze(text: str) -> Dict[str, any]:
        """
        Calculate general text metrics.
        
        Args:
            text: Input text
        
        Returns:
            Text statistics
        """
        words = text.split()
        sentences = [s for s in text.split('.') if s.strip()]
        
        # Character counts
        char_count = len(text)
        char_no_spaces = len(text.replace(' ', ''))
        
        # Word statistics
        word_count = len(words)
        avg_word_length = sum(len(w) for w in words) / word_count if word_count > 0 else 0
        
        # Sentence statistics
        sentence_count = len(sentences)
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        
        # Vocabulary diversity (unique words / total words)
        unique_words = len(set(w.lower() for w in words))
        lexical_diversity = unique_words / word_count if word_count > 0 else 0
        
        return {
            'character_count': char_count,
            'character_count_no_spaces': char_no_spaces,
            'word_count': word_count,
            'sentence_count': sentence_count,
            'avg_word_length': avg_word_length,
            'avg_sentence_length': avg_sentence_length,
            'unique_words': unique_words,
            'lexical_diversity': lexical_diversity,
        }


def main():
    """Demo function."""
    original = "However, the implementation of this algorithm demonstrates significant improvements. Therefore, it is important to consider its applications."
    modified = "This algorithm's implementation yields substantial performance gains. Its potential applications warrant careful evaluation."
    
    print("=== Readability Comparison ===")
    comparison = ReadabilityAnalyzer.compare(original, modified)
    for metric, values in list(comparison.items())[:3]:
        print(f"{metric}: {values['original']:.2f} → {values['modified']:.2f} ({values['percent_change']:+.1f}%)")
    
    print("\n=== Semantic Similarity ===")
    checker = SemanticSimilarityChecker()
    similarity = checker.calculate_similarity(original, modified)
    print(f"Similarity: {similarity:.2%}")
    
    print("\n=== AI Detection Risk ===")
    orig_risk = AIDetectionEstimator.estimate_risk(original)
    mod_risk = AIDetectionEstimator.estimate_risk(modified)
    print(f"Original: {orig_risk['risk_score']:.1f} ({orig_risk['assessment']})")
    print(f"Modified: {mod_risk['risk_score']:.1f} ({mod_risk['assessment']})")
    
    print("\n=== Text Metrics ===")
    metrics = TextMetrics.analyze(modified)
    print(f"Words: {metrics['word_count']}, Sentences: {metrics['sentence_count']}")
    print(f"Lexical Diversity: {metrics['lexical_diversity']:.2%}")


if __name__ == "__main__":
    main()
