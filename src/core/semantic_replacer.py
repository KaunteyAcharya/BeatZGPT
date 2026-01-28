"""
Semantic Replacer Module

Implements context-aware synonym replacement, phrase substitution,
and discourse marker variation for natural text transformation.
"""

import random
from typing import List, Dict, Optional, Tuple
import nltk
from nltk.corpus import wordnet
from src.nlp.parsers import NLPParser


# Download required NLTK data
try:
    wordnet.synsets('test')
except LookupError:
    nltk.download('wordnet')
    nltk.download('omw-1.4')


class SemanticReplacer:
    """Handles semantic-level text transformations."""
    
    # Discourse marker variations
    DISCOURSE_MARKERS = {
        'however': ['nevertheless', 'nonetheless', 'that said', 'on the other hand', 'conversely', 'yet'],
        'therefore': ['thus', 'hence', 'consequently', 'as a result', 'accordingly', 'for this reason'],
        'additionally': ['furthermore', 'moreover', "what's more", 'beyond that', 'in addition', 'also'],
        'in conclusion': ['ultimately', 'in summary', 'to sum up', 'all things considered', 'in the end'],
        'for example': ['for instance', 'such as', 'like', 'namely', 'to illustrate'],
        'in other words': ['that is to say', 'put differently', 'to put it another way', 'namely'],
        'first': ['firstly', 'to begin with', 'initially', 'first of all'],
        'finally': ['lastly', 'in the end', 'ultimately', 'to conclude'],
    }
    
    # Common phrase substitutions
    PHRASE_SUBSTITUTIONS = {
        'in order to': ['to', 'so as to', 'for the purpose of'],
        'due to the fact that': ['because', 'since', 'as', 'given that'],
        'at this point in time': ['now', 'currently', 'at present'],
        'in the event that': ['if', 'should', 'in case'],
        'with regard to': ['regarding', 'concerning', 'about'],
        'a number of': ['several', 'many', 'some'],
        'in spite of': ['despite', 'notwithstanding'],
        'prior to': ['before'],
        'subsequent to': ['after', 'following'],
        'in the process of': ['currently', 'while'],
    }
    
    # Context-aware synonym groups (formality levels)
    SYNONYM_GROUPS = {
        'important': {
            'formal': ['paramount', 'crucial', 'vital', 'essential'],
            'technical': ['critical', 'significant', 'key'],
            'casual': ['big', 'major', 'main'],
        },
        'show': {
            'formal': ['demonstrate', 'illustrate', 'exhibit'],
            'technical': ['indicate', 'reveal', 'display'],
            'casual': ['prove', 'point out'],
        },
        'improve': {
            'formal': ['enhance', 'augment', 'optimize'],
            'technical': ['refine', 'advance', 'upgrade'],
            'casual': ['boost', 'better', 'fix up'],
        },
        'use': {
            'formal': ['utilize', 'employ', 'apply'],
            'technical': ['implement', 'deploy', 'leverage'],
            'casual': ['try', 'work with'],
        },
    }
    
    def __init__(self, parser: Optional[NLPParser] = None, 
                 formality: str = 'formal', seed: int = None):
        """
        Initialize semantic replacer.
        
        Args:
            parser: NLPParser instance
            formality: Formality level ('formal', 'technical', 'casual')
            seed: Random seed for reproducibility
        """
        self.parser = parser or NLPParser()
        self.formality = formality
        self.random = random.Random(seed)
    
    def get_wordnet_synonyms(self, word: str, pos: Optional[str] = None) -> List[str]:
        """
        Get synonyms from WordNet.
        
        Args:
            word: Input word
            pos: Part of speech (n, v, a, r)
        
        Returns:
            List of synonyms
        """
        synonyms = set()
        
        for syn in wordnet.synsets(word, pos=pos):
            for lemma in syn.lemmas():
                synonym = lemma.name().replace('_', ' ')
                if synonym.lower() != word.lower():
                    synonyms.add(synonym)
        
        return list(synonyms)
    
    def replace_with_synonym(self, word: str, pos: str = None) -> Tuple[str, float]:
        """
        Replace word with context-appropriate synonym.
        
        Args:
            word: Word to replace
            pos: Part of speech
        
        Returns:
            Tuple of (replacement word, confidence score)
        """
        word_lower = word.lower()
        
        # Check curated synonym groups first
        if word_lower in self.SYNONYM_GROUPS:
            group = self.SYNONYM_GROUPS[word_lower]
            if self.formality in group:
                replacement = self.random.choice(group[self.formality])
                # Preserve capitalization
                if word[0].isupper():
                    replacement = replacement.capitalize()
                return replacement, 0.9
        
        # Fall back to WordNet
        synonyms = self.get_wordnet_synonyms(word_lower, pos)
        if synonyms:
            replacement = self.random.choice(synonyms)
            if word[0].isupper():
                replacement = replacement.capitalize()
            return replacement, 0.6
        
        return word, 0.0
    
    def replace_discourse_markers(self, text: str) -> Tuple[str, int]:
        """
        Replace discourse markers with varied alternatives.
        
        Args:
            text: Input text
        
        Returns:
            Tuple of (modified text, number of replacements)
        """
        modified = text
        replacements = 0
        
        for marker, alternatives in self.DISCOURSE_MARKERS.items():
            # Case-insensitive search
            if marker.lower() in modified.lower():
                # Find all occurrences
                words = modified.split()
                new_words = []
                
                for i, word in enumerate(words):
                    word_clean = word.strip('.,;:!?').lower()
                    
                    if word_clean == marker.lower():
                        # Replace with random alternative
                        replacement = self.random.choice(alternatives)
                        
                        # Preserve capitalization and punctuation
                        if word[0].isupper():
                            replacement = replacement.capitalize()
                        
                        # Preserve trailing punctuation
                        for punct in '.,;:!?':
                            if word.endswith(punct):
                                replacement += punct
                                break
                        
                        new_words.append(replacement)
                        replacements += 1
                    else:
                        new_words.append(word)
                
                modified = ' '.join(new_words)
        
        return modified, replacements
    
    def replace_phrases(self, text: str) -> Tuple[str, int]:
        """
        Replace common phrases with more concise alternatives.
        
        Args:
            text: Input text
        
        Returns:
            Tuple of (modified text, number of replacements)
        """
        modified = text
        replacements = 0
        
        for phrase, alternatives in self.PHRASE_SUBSTITUTIONS.items():
            if phrase in modified.lower():
                replacement = self.random.choice(alternatives)
                
                # Case-sensitive replacement
                if phrase in modified:
                    modified = modified.replace(phrase, replacement)
                    replacements += 1
                elif phrase.capitalize() in modified:
                    modified = modified.replace(phrase.capitalize(), replacement.capitalize())
                    replacements += 1
        
        return modified, replacements
    
    def replace_semantics(self, text: str, intensity: float = 0.5) -> str:
        """
        Apply all semantic transformations.
        
        Args:
            text: Input text
            intensity: Replacement intensity (0.0 to 1.0)
        
        Returns:
            Transformed text
        """
        # Start with discourse markers
        modified, _ = self.replace_discourse_markers(text)
        
        # Replace common phrases
        modified, _ = self.replace_phrases(modified)
        
        # Replace individual words based on intensity
        if intensity > 0.3:
            doc = self.parser.parse(modified)
            words = []
            
            for token in doc:
                # Only replace content words (not function words)
                if token.pos_ in ['VERB', 'ADJ', 'ADV'] and len(token.text) > 4:
                    if self.random.random() < intensity:
                        # Map spaCy POS to WordNet POS
                        pos_map = {'VERB': 'v', 'ADJ': 'a', 'ADV': 'r'}
                        wn_pos = pos_map.get(token.pos_)
                        
                        replacement, conf = self.replace_with_synonym(token.text, wn_pos)
                        if conf > 0.5:
                            words.append(replacement)
                        else:
                            words.append(token.text)
                    else:
                        words.append(token.text)
                else:
                    words.append(token.text_with_ws.rstrip())
            
            # Reconstruct with proper spacing
            modified = ' '.join(words)
            # Fix spacing around punctuation
            for punct in '.,;:!?':
                modified = modified.replace(f' {punct}', punct)
        
        return modified


def main():
    """Demo function."""
    replacer = SemanticReplacer(formality='formal', seed=42)
    
    sample = "However, it is important to show that we can improve the use of this method. Therefore, in order to demonstrate this, we need additional testing."
    
    print(f"Original: {sample}\n")
    
    result = replacer.replace_semantics(sample, intensity=0.7)
    print(f"Transformed: {result}\n")
    
    # Show individual transformations
    markers, m_count = replacer.replace_discourse_markers(sample)
    print(f"Discourse markers ({m_count} replacements): {markers}\n")
    
    phrases, p_count = replacer.replace_phrases(sample)
    print(f"Phrases ({p_count} replacements): {phrases}\n")


if __name__ == "__main__":
    main()
