"""
Unicode Space Manipulation Engine

Replaces standard ASCII spaces with visually identical Unicode space variants
to evade AI detection while maintaining readability.
"""

import random
from typing import Dict, List, Tuple


class SpaceManipulator:
    """Handles Unicode space character substitution with configurable intensity."""
    
    # Unicode space character mappings
    SPACE_VARIANTS: Dict[str, str] = {
        'standard': '\u0020',        # Standard Space
        'non_breaking': '\u00A0',    # Non-Breaking Space
        'en_space': '\u2002',        # En Space
        'em_space': '\u2003',        # Em Space
        'thin_space': '\u2009',      # Thin Space
        'hair_space': '\u200A',      # Hair Space
        'zero_width': '\u200B',      # Zero-Width Space
        'figure_space': '\u2007',    # Figure Space
        'narrow_no_break': '\u202F', # Narrow No-Break Space
    }
    
    def __init__(self, intensity: float = 0.5, seed: int = None):
        """
        Initialize the space manipulator.
        
        Args:
            intensity: Replacement percentage (0.0 to 1.0). Default 0.5 means 50% of spaces replaced.
            seed: Random seed for reproducible results. None for random behavior.
        """
        if not 0.0 <= intensity <= 1.0:
            raise ValueError("Intensity must be between 0.0 and 1.0")
        
        self.intensity = intensity
        self.random = random.Random(seed)
        
        # Get list of variant characters (excluding standard space)
        self.variants = [v for k, v in self.SPACE_VARIANTS.items() if k != 'standard']
    
    def replace_spaces(self, text: str, preserve_boundaries: bool = True) -> str:
        """
        Replace standard spaces with Unicode variants using randomized distribution.
        
        Args:
            text: Input text to process
            preserve_boundaries: If True, preserve spaces at word boundaries (start/end of lines)
        
        Returns:
            Text with replaced spaces
        """
        if not text or self.intensity == 0.0:
            return text
        
        result = []
        standard_space = self.SPACE_VARIANTS['standard']
        
        for i, char in enumerate(text):
            if char == standard_space:
                # Check if we should preserve this space (at boundaries)
                if preserve_boundaries:
                    is_start = i == 0
                    is_end = i == len(text) - 1
                    is_line_boundary = (i > 0 and text[i-1] == '\n') or (i < len(text)-1 and text[i+1] == '\n')
                    
                    if is_start or is_end or is_line_boundary:
                        result.append(char)
                        continue
                
                # Decide whether to replace based on intensity
                if self.random.random() < self.intensity:
                    # Choose a random variant
                    replacement = self.random.choice(self.variants)
                    result.append(replacement)
                else:
                    result.append(char)
            else:
                result.append(char)
        
        return ''.join(result)
    
    def analyze_distribution(self, text: str) -> Dict[str, int]:
        """
        Analyze the distribution of space characters in text.
        
        Args:
            text: Text to analyze
        
        Returns:
            Dictionary mapping space variant names to their counts
        """
        distribution = {name: 0 for name in self.SPACE_VARIANTS.keys()}
        
        # Create reverse mapping (character -> name)
        char_to_name = {char: name for name, char in self.SPACE_VARIANTS.items()}
        
        for char in text:
            if char in char_to_name:
                distribution[char_to_name[char]] += 1
        
        return distribution
    
    def visualize_distribution(self, text: str) -> str:
        """
        Create a visual representation of space distribution.
        
        Args:
            text: Text to visualize
        
        Returns:
            Formatted string showing distribution statistics
        """
        distribution = self.analyze_distribution(text)
        total_spaces = sum(distribution.values())
        
        if total_spaces == 0:
            return "No spaces found in text."
        
        lines = ["Space Character Distribution:", "=" * 50]
        
        for name, count in sorted(distribution.items(), key=lambda x: x[1], reverse=True):
            if count > 0:
                percentage = (count / total_spaces) * 100
                bar = '█' * int(percentage / 2)
                lines.append(f"{name:20s}: {count:5d} ({percentage:5.1f}%) {bar}")
        
        lines.append("=" * 50)
        lines.append(f"Total spaces: {total_spaces}")
        
        return '\n'.join(lines)
    
    def get_replacement_stats(self, original: str, modified: str) -> Dict[str, any]:
        """
        Compare original and modified text to get replacement statistics.
        
        Args:
            original: Original text
            modified: Modified text with replaced spaces
        
        Returns:
            Dictionary with statistics
        """
        orig_dist = self.analyze_distribution(original)
        mod_dist = self.analyze_distribution(modified)
        
        total_original = sum(orig_dist.values())
        total_replaced = total_original - mod_dist.get('standard', 0)
        
        return {
            'total_spaces': total_original,
            'spaces_replaced': total_replaced,
            'replacement_rate': (total_replaced / total_original * 100) if total_original > 0 else 0,
            'original_distribution': orig_dist,
            'modified_distribution': mod_dist,
        }


def main():
    """Demo function showing space manipulation in action."""
    sample_text = """However, the implementation of this algorithm demonstrates significant improvements. 
Therefore, it is important to consider its applications in various domains."""
    
    print("Original Text:")
    print(sample_text)
    print("\n" + "="*70 + "\n")
    
    # Test with different intensities
    for intensity in [0.3, 0.5, 0.8]:
        manipulator = SpaceManipulator(intensity=intensity, seed=42)
        modified = manipulator.replace_spaces(sample_text)
        
        print(f"Intensity: {intensity}")
        print(f"Modified Text: {modified}")
        
        stats = manipulator.get_replacement_stats(sample_text, modified)
        print(f"Replaced {stats['spaces_replaced']}/{stats['total_spaces']} spaces ({stats['replacement_rate']:.1f}%)")
        print("\n" + manipulator.visualize_distribution(modified))
        print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
