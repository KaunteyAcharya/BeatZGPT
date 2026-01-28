"""
Syntax Restructurer Module

Implements sophisticated sentence transformations including voice conversion,
clause reordering, and sentence complexity variation.
"""

import random
from typing import List, Optional, Tuple
from src.nlp.parsers import NLPParser


class SyntaxRestructurer:
    """Handles syntactic transformations for text humanization."""
    
    def __init__(self, parser: Optional[NLPParser] = None, seed: int = None):
        """
        Initialize syntax restructurer.
        
        Args:
            parser: NLPParser instance (creates new one if None)
            seed: Random seed for reproducibility
        """
        self.parser = parser or NLPParser()
        self.random = random.Random(seed)
    
    def passive_to_active(self, sentence: str) -> Tuple[str, float]:
        """
        Convert passive voice to active voice.
        
        Args:
            sentence: Input sentence in passive voice
        
        Returns:
            Tuple of (transformed sentence, confidence score)
        """
        if not self.parser.is_passive_voice(sentence):
            return sentence, 0.0
        
        doc = self.parser.parse(sentence)
        
        # Find passive subject and agent
        passive_subject = None
        agent = None
        main_verb = None
        
        for token in doc:
            if token.dep_ == "nsubjpass":
                passive_subject = token
            elif token.dep_ == "agent" or (token.dep_ == "pobj" and token.head.text == "by"):
                agent = token
            elif token.tag_ == "VBN" and any(child.dep_ == "auxpass" for child in token.children):
                main_verb = token
        
        # Simple transformation if we found all components
        if agent and passive_subject and main_verb:
            # Reconstruct: agent + verb + passive_subject
            new_sentence = f"{agent.text.capitalize()} {main_verb.lemma_} {passive_subject.text}"
            
            # Add remaining parts (objects, modifiers)
            remaining = [t.text for t in doc if t not in [agent, passive_subject, main_verb] 
                        and t.dep_ not in ["auxpass", "agent", "prep"] 
                        and t.text.lower() not in ["was", "were", "been", "by", "the"]]
            
            if remaining:
                new_sentence += " " + " ".join(remaining)
            
            new_sentence += "."
            return new_sentence, 0.8
        
        return sentence, 0.0
    
    def active_to_passive(self, sentence: str) -> Tuple[str, float]:
        """
        Convert active voice to passive voice (when stylistically appropriate).
        
        Args:
            sentence: Input sentence in active voice
        
        Returns:
            Tuple of (transformed sentence, confidence score)
        """
        if self.parser.is_passive_voice(sentence):
            return sentence, 0.0
        
        doc = self.parser.parse(sentence)
        
        # Find subject, verb, and object
        subject = None
        verb = None
        obj = None
        
        for token in doc:
            if token.dep_ == "nsubj":
                subject = token
            elif token.pos_ == "VERB" and token.dep_ == "ROOT":
                verb = token
            elif token.dep_ in ["dobj", "obj"]:
                obj = token
        
        # Only convert if we have all components
        if subject and verb and obj:
            # Reconstruct: object + was/were + past_participle + by + subject
            be_verb = "was" if obj.tag_ in ["NN", "NNP"] else "were"
            new_sentence = f"{obj.text.capitalize()} {be_verb} {verb.text} by {subject.text.lower()}."
            return new_sentence, 0.6
        
        return sentence, 0.0
    
    def reorder_clauses(self, sentence: str) -> Tuple[str, float]:
        """
        Reorder dependent clauses while preserving meaning.
        
        Args:
            sentence: Input sentence
        
        Returns:
            Tuple of (transformed sentence, confidence score)
        """
        clauses = self.parser.find_clauses(sentence)
        
        if not clauses['dependent']:
            return sentence, 0.0
        
        doc = self.parser.parse(sentence)
        
        # Simple pattern: move "Because X, Y" to "Y because X"
        if sentence.lower().startswith("because"):
            parts = sentence.split(",", 1)
            if len(parts) == 2:
                dependent = parts[0].strip()
                main = parts[1].strip()
                
                # Capitalize main clause, lowercase because
                main = main[0].upper() + main[1:] if main else main
                dependent = dependent.lower()
                
                new_sentence = f"{main} {dependent}."
                return new_sentence, 0.7
        
        return sentence, 0.0
    
    def reverse_nominalization(self, sentence: str) -> Tuple[str, float]:
        """
        Convert noun forms back to verbs for more direct language.
        
        Args:
            sentence: Input sentence
        
        Returns:
            Tuple of (transformed sentence, confidence score)
        """
        # Common nominalization patterns
        nominalizations = {
            'implementation of': 'implementing',
            'completion of': 'completing',
            'development of': 'developing',
            'creation of': 'creating',
            'analysis of': 'analyzing',
            'evaluation of': 'evaluating',
            'examination of': 'examining',
        }
        
        modified = sentence
        confidence = 0.0
        
        for nominal, verbal in nominalizations.items():
            if nominal in sentence.lower():
                # Simple replacement
                modified = sentence.replace(nominal, verbal)
                modified = modified.replace(nominal.capitalize(), verbal.capitalize())
                confidence = 0.6
                break
        
        return modified, confidence
    
    def vary_sentence_complexity(self, sentences: List[str]) -> Tuple[List[str], float]:
        """
        Split long sentences or combine short ones.
        
        Args:
            sentences: List of sentences
        
        Returns:
            Tuple of (transformed sentences, confidence score)
        """
        if not sentences:
            return sentences, 0.0
        
        result = []
        i = 0
        
        while i < len(sentences):
            sent = sentences[i]
            words = sent.split()
            
            # Split long sentences (>30 words)
            if len(words) > 30 and ',' in sent:
                parts = sent.split(',', 1)
                if len(parts) == 2:
                    result.append(parts[0].strip() + '.')
                    result.append(parts[1].strip())
                    i += 1
                    continue
            
            # Combine short sentences (<8 words)
            if len(words) < 8 and i + 1 < len(sentences):
                next_sent = sentences[i + 1]
                next_words = next_sent.split()
                
                if len(next_words) < 8:
                    # Combine with connector
                    connectors = ['and', 'while', 'as']
                    connector = self.random.choice(connectors)
                    combined = f"{sent.rstrip('.')} {connector} {next_sent.lower()}"
                    result.append(combined)
                    i += 2
                    continue
            
            result.append(sent)
            i += 1
        
        confidence = 0.5 if len(result) != len(sentences) else 0.0
        return result, confidence
    
    def restructure(self, text: str, enable_voice: bool = True, 
                   enable_clauses: bool = True, enable_nominalization: bool = True) -> str:
        """
        Apply all restructuring transformations.
        
        Args:
            text: Input text
            enable_voice: Enable voice conversion
            enable_clauses: Enable clause reordering
            enable_nominalization: Enable nominalization reversal
        
        Returns:
            Restructured text
        """
        sentences = self.parser.get_sentences(text)
        transformed = []
        
        for sent in sentences:
            current = sent
            
            # Try passive to active conversion
            if enable_voice and self.parser.is_passive_voice(current):
                result, conf = self.passive_to_active(current)
                if conf > 0.5:
                    current = result
            
            # Try clause reordering
            if enable_clauses:
                result, conf = self.reorder_clauses(current)
                if conf > 0.5:
                    current = result
            
            # Try nominalization reversal
            if enable_nominalization:
                result, conf = self.reverse_nominalization(current)
                if conf > 0.5:
                    current = result
            
            transformed.append(current)
        
        # Vary sentence complexity
        transformed, _ = self.vary_sentence_complexity(transformed)
        
        return ' '.join(transformed)


def main():
    """Demo function."""
    restructurer = SyntaxRestructurer(seed=42)
    
    samples = [
        "The report was completed by the team.",
        "Because performance degraded, we optimized the code.",
        "The implementation of the algorithm demonstrates improvements.",
    ]
    
    for sample in samples:
        print(f"Original: {sample}")
        result = restructurer.restructure(sample)
        print(f"Transformed: {result}\n")


if __name__ == "__main__":
    main()
