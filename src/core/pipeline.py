"""
Humanization Pipeline

Orchestrates all text transformations with quality assurance and rollback mechanisms.
"""

from typing import Dict, Optional
from src.core.space_manipulator import SpaceManipulator
from src.core.syntax_restructurer import SyntaxRestructurer
from src.core.semantic_replacer import SemanticReplacer
from src.nlp.parsers import NLPParser
from src.nlp.analyzers import (
    ReadabilityAnalyzer, 
    SemanticSimilarityChecker, 
    AIDetectionEstimator,
    TextMetrics
)


class HumanizationPipeline:
    """Main pipeline for text humanization."""
    
    def __init__(self, 
                 intensity: float = 0.5,
                 enable_unicode: bool = True,
                 enable_syntax: bool = True,
                 enable_semantics: bool = True,
                 formality: str = 'formal',
                 quality_threshold: float = 0.85,
                 seed: int = None):
        """
        Initialize humanization pipeline.
        
        Args:
            intensity: Overall transformation intensity (0.0 to 1.0)
            enable_unicode: Enable Unicode space manipulation
            enable_syntax: Enable syntax restructuring
            enable_semantics: Enable semantic replacement
            formality: Formality level for semantic replacement
            quality_threshold: Minimum semantic similarity to accept (0.0 to 1.0)
            seed: Random seed for reproducibility
        """
        self.intensity = intensity
        self.enable_unicode = enable_unicode
        self.enable_syntax = enable_syntax
        self.enable_semantics = enable_semantics
        self.formality = formality
        self.quality_threshold = quality_threshold
        
        # Initialize components
        self.parser = NLPParser()
        self.space_manipulator = SpaceManipulator(intensity=intensity, seed=seed)
        self.syntax_restructurer = SyntaxRestructurer(parser=self.parser, seed=seed)
        self.semantic_replacer = SemanticReplacer(
            parser=self.parser, 
            formality=formality, 
            seed=seed
        )
        self.similarity_checker = SemanticSimilarityChecker()
    
    def humanize(self, text: str, preserve_formatting: bool = True) -> Dict[str, any]:
        """
        Apply all humanization transformations with quality checks.
        
        Args:
            text: Input text to humanize
            preserve_formatting: Preserve original formatting (newlines, etc.)
        
        Returns:
            Dictionary with humanized text and analysis
        """
        if not text or not text.strip():
            return {
                'original': text,
                'humanized': text,
                'transformations_applied': [],
                'quality_metrics': {},
                'passed_quality_check': True,
            }
        
        original_text = text
        current_text = text
        transformations_applied = []
        
        # Step 1: Syntax Restructuring (if enabled)
        if self.enable_syntax:
            try:
                restructured = self.syntax_restructurer.restructure(
                    current_text,
                    enable_voice=True,
                    enable_clauses=True,
                    enable_nominalization=True
                )
                
                # Quality check
                similarity = self.similarity_checker.calculate_similarity(
                    original_text, restructured
                )
                
                if similarity >= self.quality_threshold:
                    current_text = restructured
                    transformations_applied.append('syntax_restructuring')
                else:
                    print(f"Warning: Syntax restructuring rejected (similarity: {similarity:.2%})")
            
            except Exception as e:
                print(f"Warning: Syntax restructuring failed: {e}")
        
        # Step 2: Semantic Replacement (if enabled)
        if self.enable_semantics:
            try:
                semantic_text = self.semantic_replacer.replace_semantics(
                    current_text, 
                    intensity=self.intensity
                )
                
                # Quality check
                similarity = self.similarity_checker.calculate_similarity(
                    original_text, semantic_text
                )
                
                if similarity >= self.quality_threshold:
                    current_text = semantic_text
                    transformations_applied.append('semantic_replacement')
                else:
                    print(f"Warning: Semantic replacement rejected (similarity: {similarity:.2%})")
            
            except Exception as e:
                print(f"Warning: Semantic replacement failed: {e}")
        
        # Step 3: Unicode Space Manipulation (if enabled)
        if self.enable_unicode:
            try:
                unicode_text = self.space_manipulator.replace_spaces(
                    current_text,
                    preserve_boundaries=True
                )
                current_text = unicode_text
                transformations_applied.append('unicode_manipulation')
            
            except Exception as e:
                print(f"Warning: Unicode manipulation failed: {e}")
        
        # Calculate final quality metrics
        quality_metrics = self._calculate_quality_metrics(original_text, current_text)
        
        # Final quality check
        passed_quality_check = (
            quality_metrics['semantic_similarity'] >= self.quality_threshold and
            abs(quality_metrics['readability_change']) <= 5.0  # ±5% grade level
        )
        
        # Rollback if quality check failed
        if not passed_quality_check:
            print("Warning: Final quality check failed. Returning original text.")
            current_text = original_text
            transformations_applied = []
        
        return {
            'original': original_text,
            'humanized': current_text,
            'transformations_applied': transformations_applied,
            'quality_metrics': quality_metrics,
            'passed_quality_check': passed_quality_check,
        }
    
    def _calculate_quality_metrics(self, original: str, modified: str) -> Dict[str, any]:
        """
        Calculate comprehensive quality metrics.
        
        Args:
            original: Original text
            modified: Modified text
        
        Returns:
            Quality metrics dictionary
        """
        # Readability comparison
        readability_comparison = ReadabilityAnalyzer.compare(original, modified)
        fk_grade_change = readability_comparison['flesch_kincaid_grade']['percent_change']
        
        # Semantic similarity
        semantic_similarity = self.similarity_checker.calculate_similarity(original, modified)
        
        # AI detection risk
        original_risk = AIDetectionEstimator.estimate_risk(original)
        modified_risk = AIDetectionEstimator.estimate_risk(modified)
        risk_reduction = original_risk['risk_score'] - modified_risk['risk_score']
        
        # Text metrics
        original_metrics = TextMetrics.analyze(original)
        modified_metrics = TextMetrics.analyze(modified)
        
        # Space distribution (if Unicode manipulation applied)
        space_stats = self.space_manipulator.get_replacement_stats(original, modified)
        
        return {
            'semantic_similarity': semantic_similarity,
            'readability_change': fk_grade_change,
            'original_readability': readability_comparison['flesch_kincaid_grade']['original'],
            'modified_readability': readability_comparison['flesch_kincaid_grade']['modified'],
            'ai_risk_original': original_risk['risk_score'],
            'ai_risk_modified': modified_risk['risk_score'],
            'ai_risk_reduction': risk_reduction,
            'original_word_count': original_metrics['word_count'],
            'modified_word_count': modified_metrics['word_count'],
            'lexical_diversity_change': (
                modified_metrics['lexical_diversity'] - original_metrics['lexical_diversity']
            ),
            'spaces_replaced': space_stats['spaces_replaced'],
            'space_replacement_rate': space_stats['replacement_rate'],
        }
    
    def batch_humanize(self, texts: list, show_progress: bool = True) -> list:
        """
        Humanize multiple texts.
        
        Args:
            texts: List of texts to humanize
            show_progress: Show progress bar
        
        Returns:
            List of humanization results
        """
        results = []
        
        if show_progress:
            try:
                from tqdm import tqdm
                iterator = tqdm(texts, desc="Humanizing texts")
            except ImportError:
                iterator = texts
        else:
            iterator = texts
        
        for text in iterator:
            result = self.humanize(text)
            results.append(result)
        
        return results


def main():
    """Demo function."""
    sample_text = """However, the implementation of this algorithm demonstrates significant improvements. Therefore, it is important to consider its applications in various domains. Additionally, the results show that performance has been enhanced substantially."""
    
    print("="*70)
    print("ORIGINAL TEXT:")
    print("="*70)
    print(sample_text)
    print()
    
    # Test with different configurations
    configs = [
        {'intensity': 0.5, 'enable_unicode': True, 'enable_syntax': True, 'enable_semantics': True},
        {'intensity': 0.8, 'enable_unicode': True, 'enable_syntax': True, 'enable_semantics': True},
    ]
    
    for i, config in enumerate(configs, 1):
        print("="*70)
        print(f"CONFIGURATION {i}: Intensity={config['intensity']}")
        print("="*70)
        
        pipeline = HumanizationPipeline(**config, seed=42)
        result = pipeline.humanize(sample_text)
        
        print("HUMANIZED TEXT:")
        print(result['humanized'])
        print()
        
        print("TRANSFORMATIONS APPLIED:")
        print(", ".join(result['transformations_applied']))
        print()
        
        print("QUALITY METRICS:")
        metrics = result['quality_metrics']
        print(f"  Semantic Similarity: {metrics['semantic_similarity']:.2%}")
        print(f"  Readability Change: {metrics['readability_change']:+.1f}%")
        print(f"  AI Risk: {metrics['ai_risk_original']:.1f} → {metrics['ai_risk_modified']:.1f} ({metrics['ai_risk_reduction']:+.1f})")
        print(f"  Spaces Replaced: {metrics['spaces_replaced']} ({metrics['space_replacement_rate']:.1f}%)")
        print(f"  Quality Check: {'PASSED' if result['passed_quality_check'] else 'FAILED'}")
        print()


if __name__ == "__main__":
    main()
