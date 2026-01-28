"""
CLI Tool for AI Text Humanizer

Command-line interface for humanizing text files.
"""

import click
import json
from pathlib import Path
from typing import Optional
from src.core.pipeline import HumanizationPipeline


@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('-o', '--output', 'output_file', type=click.Path(), 
              help='Output file path (default: input_file.humanized.txt)')
@click.option('--intensity', type=float, default=0.5, 
              help='Transformation intensity (0.0 to 1.0, default: 0.5)')
@click.option('--enable-syntax/--no-syntax', default=True,
              help='Enable syntax restructuring (default: enabled)')
@click.option('--enable-semantics/--no-semantics', default=True,
              help='Enable semantic replacement (default: enabled)')
@click.option('--enable-unicode/--no-unicode', default=True,
              help='Enable Unicode space manipulation (default: enabled)')
@click.option('--formality', type=click.Choice(['formal', 'technical', 'casual']),
              default='formal', help='Formality level for semantic replacement')
@click.option('--quality-threshold', type=float, default=0.85,
              help='Minimum semantic similarity threshold (0.0 to 1.0, default: 0.85)')
@click.option('--analysis-report', type=click.Path(),
              help='Path to save analysis report (JSON format)')
@click.option('--preserve-formatting/--no-preserve-formatting', default=True,
              help='Preserve original formatting (default: enabled)')
@click.option('--seed', type=int, default=None,
              help='Random seed for reproducibility')
@click.option('--verbose', is_flag=True, help='Show detailed progress')
def main(input_file: str, output_file: Optional[str], intensity: float,
         enable_syntax: bool, enable_semantics: bool, enable_unicode: bool,
         formality: str, quality_threshold: float, analysis_report: Optional[str],
         preserve_formatting: bool, seed: Optional[int], verbose: bool):
    """
    Humanize AI-generated text to reduce detection scores.
    
    INPUT_FILE: Path to the text file to humanize
    
    Example:
        humanizer input.txt -o output.txt --intensity 0.8
    """
    
    # Read input file
    input_path = Path(input_file)
    
    if verbose:
        click.echo(f"Reading input file: {input_path}")
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        click.echo(f"Error reading input file: {e}", err=True)
        return 1
    
    if not text.strip():
        click.echo("Error: Input file is empty", err=True)
        return 1
    
    # Determine output file path
    if output_file is None:
        output_path = input_path.with_suffix('.humanized.txt')
    else:
        output_path = Path(output_file)
    
    if verbose:
        click.echo(f"Output file: {output_path}")
        click.echo(f"Configuration:")
        click.echo(f"  Intensity: {intensity}")
        click.echo(f"  Syntax: {enable_syntax}")
        click.echo(f"  Semantics: {enable_semantics}")
        click.echo(f"  Unicode: {enable_unicode}")
        click.echo(f"  Formality: {formality}")
        click.echo(f"  Quality Threshold: {quality_threshold}")
    
    # Initialize pipeline
    click.echo("Initializing humanization pipeline...")
    
    try:
        pipeline = HumanizationPipeline(
            intensity=intensity,
            enable_unicode=enable_unicode,
            enable_syntax=enable_syntax,
            enable_semantics=enable_semantics,
            formality=formality,
            quality_threshold=quality_threshold,
            seed=seed
        )
    except Exception as e:
        click.echo(f"Error initializing pipeline: {e}", err=True)
        return 1
    
    # Humanize text
    click.echo("Humanizing text...")
    
    try:
        result = pipeline.humanize(text, preserve_formatting=preserve_formatting)
    except Exception as e:
        click.echo(f"Error during humanization: {e}", err=True)
        return 1
    
    # Write output
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result['humanized'])
        
        click.echo(f"✓ Humanized text saved to: {output_path}")
    except Exception as e:
        click.echo(f"Error writing output file: {e}", err=True)
        return 1
    
    # Display summary
    click.echo("\n" + "="*60)
    click.echo("HUMANIZATION SUMMARY")
    click.echo("="*60)
    
    metrics = result['quality_metrics']
    
    click.echo(f"Transformations Applied: {', '.join(result['transformations_applied']) or 'None'}")
    click.echo(f"Quality Check: {'PASSED ✓' if result['passed_quality_check'] else 'FAILED ✗'}")
    click.echo(f"\nQuality Metrics:")
    click.echo(f"  Semantic Similarity: {metrics['semantic_similarity']:.2%}")
    click.echo(f"  Readability Change: {metrics['readability_change']:+.1f}%")
    click.echo(f"  AI Detection Risk: {metrics['ai_risk_original']:.1f} → {metrics['ai_risk_modified']:.1f} "
               f"({metrics['ai_risk_reduction']:+.1f})")
    
    if enable_unicode:
        click.echo(f"  Spaces Replaced: {metrics['spaces_replaced']} ({metrics['space_replacement_rate']:.1f}%)")
    
    click.echo(f"\nText Statistics:")
    click.echo(f"  Word Count: {metrics['original_word_count']} → {metrics['modified_word_count']}")
    click.echo(f"  Lexical Diversity Change: {metrics['lexical_diversity_change']:+.3f}")
    
    # Save analysis report if requested
    if analysis_report:
        try:
            report_path = Path(analysis_report)
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, default=str)
            
            click.echo(f"\n✓ Analysis report saved to: {report_path}")
        except Exception as e:
            click.echo(f"\nWarning: Could not save analysis report: {e}", err=True)
    
    click.echo("="*60)
    
    return 0


if __name__ == '__main__':
    exit(main())
