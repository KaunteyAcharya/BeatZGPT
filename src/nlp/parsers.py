"""
NLP Parsers Module

Provides text analysis utilities using spaCy for dependency parsing,
POS tagging, and sentence segmentation.
"""

import spacy
from typing import List, Dict, Optional
from functools import lru_cache


class NLPParser:
    """Handles NLP parsing operations with model caching."""
    
    _nlp_model = None
    
    @classmethod
    @lru_cache(maxsize=1)
    def get_model(cls, model_name: str = "en_core_web_lg"):
        """
        Load and cache spaCy model.
        
        Args:
            model_name: Name of spaCy model to load
        
        Returns:
            Loaded spaCy model
        """
        if cls._nlp_model is None:
            try:
                cls._nlp_model = spacy.load(model_name)
            except OSError:
                print(f"Model '{model_name}' not found. Downloading...")
                import subprocess
                subprocess.run(["python", "-m", "spacy", "download", model_name])
                cls._nlp_model = spacy.load(model_name)
        
        return cls._nlp_model
    
    def __init__(self, model_name: str = "en_core_web_lg"):
        """Initialize parser with specified model."""
        self.nlp = self.get_model(model_name)
    
    def parse(self, text: str):
        """
        Parse text using spaCy.
        
        Args:
            text: Input text
        
        Returns:
            spaCy Doc object
        """
        return self.nlp(text)
    
    def get_sentences(self, text: str) -> List[str]:
        """
        Segment text into sentences.
        
        Args:
            text: Input text
        
        Returns:
            List of sentence strings
        """
        doc = self.parse(text)
        return [sent.text.strip() for sent in doc.sents]
    
    def get_pos_tags(self, text: str) -> List[Dict[str, str]]:
        """
        Get part-of-speech tags for text.
        
        Args:
            text: Input text
        
        Returns:
            List of dicts with token, pos, and tag information
        """
        doc = self.parse(text)
        return [
            {
                'token': token.text,
                'pos': token.pos_,
                'tag': token.tag_,
                'dep': token.dep_,
                'lemma': token.lemma_
            }
            for token in doc
        ]
    
    def get_dependency_tree(self, text: str) -> List[Dict]:
        """
        Extract dependency tree structure.
        
        Args:
            text: Input text
        
        Returns:
            List of dependency relationships
        """
        doc = self.parse(text)
        return [
            {
                'token': token.text,
                'dep': token.dep_,
                'head': token.head.text,
                'children': [child.text for child in token.children]
            }
            for token in doc
        ]
    
    def get_noun_chunks(self, text: str) -> List[str]:
        """
        Extract noun phrases.
        
        Args:
            text: Input text
        
        Returns:
            List of noun chunk strings
        """
        doc = self.parse(text)
        return [chunk.text for chunk in doc.noun_chunks]
    
    def get_named_entities(self, text: str) -> List[Dict[str, str]]:
        """
        Extract named entities.
        
        Args:
            text: Input text
        
        Returns:
            List of entities with text and label
        """
        doc = self.parse(text)
        return [
            {'text': ent.text, 'label': ent.label_}
            for ent in doc.ents
        ]
    
    def is_passive_voice(self, sentence: str) -> bool:
        """
        Detect if sentence is in passive voice.
        
        Args:
            sentence: Input sentence
        
        Returns:
            True if passive voice detected
        """
        doc = self.parse(sentence)
        
        for token in doc:
            # Look for passive auxiliary (be) + past participle
            if token.dep_ == "nsubjpass":
                return True
            # Alternative pattern: auxiliary + past participle
            if token.tag_ == "VBN" and any(child.dep_ == "auxpass" for child in token.children):
                return True
        
        return False
    
    def find_clauses(self, sentence: str) -> Dict[str, List[str]]:
        """
        Identify different types of clauses in a sentence.
        
        Args:
            sentence: Input sentence
        
        Returns:
            Dictionary with clause types and their text
        """
        doc = self.parse(sentence)
        clauses = {
            'main': [],
            'dependent': [],
            'relative': []
        }
        
        for token in doc:
            # Dependent clauses often start with subordinating conjunctions
            if token.dep_ in ['advcl', 'ccomp', 'xcomp']:
                clause_text = ' '.join([t.text for t in token.subtree])
                clauses['dependent'].append(clause_text)
            
            # Relative clauses
            elif token.dep_ == 'relcl':
                clause_text = ' '.join([t.text for t in token.subtree])
                clauses['relative'].append(clause_text)
        
        return clauses


def main():
    """Demo function."""
    parser = NLPParser()
    
    sample = "The report was completed by the team because performance degraded."
    
    print(f"Text: {sample}\n")
    print(f"Sentences: {parser.get_sentences(sample)}\n")
    print(f"Is passive: {parser.is_passive_voice(sample)}\n")
    print(f"POS tags: {parser.get_pos_tags(sample)[:5]}\n")
    print(f"Clauses: {parser.find_clauses(sample)}\n")


if __name__ == "__main__":
    main()
