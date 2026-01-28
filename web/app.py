"""
Web Application for AI Text Humanizer

Flask-based web interface for real-time text humanization.
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import io
import json
from pathlib import Path
from docx import Document
from fpdf import FPDF

from src.core.pipeline import HumanizationPipeline


app = Flask(__name__)
CORS(app)

# Global pipeline instance (initialized on first request)
pipeline = None


def get_pipeline():
    """Get or create pipeline instance."""
    global pipeline
    if pipeline is None:
        pipeline = HumanizationPipeline(
            intensity=0.5,
            enable_unicode=True,
            enable_syntax=True,
            enable_semantics=True,
            formality='formal',
            quality_threshold=0.85
        )
    return pipeline


@app.route('/')
def index():
    """Render main interface."""
    return render_template('index.html')


@app.route('/api/humanize', methods=['POST'])
def humanize():
    """Humanize text endpoint."""
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text or not text.strip():
            return jsonify({'error': 'No text provided'}), 400
        
        # Get configuration
        intensity = float(data.get('intensity', 0.5))
        enable_unicode = data.get('enable_unicode', True)
        enable_syntax = data.get('enable_syntax', True)
        enable_semantics = data.get('enable_semantics', True)
        formality = data.get('formality', 'formal')
        
        # Create pipeline with custom settings
        custom_pipeline = HumanizationPipeline(
            intensity=intensity,
            enable_unicode=enable_unicode,
            enable_syntax=enable_syntax,
            enable_semantics=enable_semantics,
            formality=formality,
            quality_threshold=0.85
        )
        
        # Humanize
        result = custom_pipeline.humanize(text)
        
        return jsonify({
            'success': True,
            'humanized': result['humanized'],
            'transformations': result['transformations_applied'],
            'metrics': result['quality_metrics'],
            'passed_quality_check': result['passed_quality_check']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analyze text quality metrics."""
    try:
        data = request.json
        original = data.get('original', '')
        modified = data.get('modified', '')
        
        if not original or not modified:
            return jsonify({'error': 'Both original and modified text required'}), 400
        
        pipeline = get_pipeline()
        metrics = pipeline._calculate_quality_metrics(original, modified)
        
        return jsonify({
            'success': True,
            'metrics': metrics
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/export/<format>', methods=['POST'])
def export(format):
    """Export humanized text in various formats."""
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        if format == 'txt':
            # Plain text
            buffer = io.BytesIO()
            buffer.write(text.encode('utf-8'))
            buffer.seek(0)
            
            return send_file(
                buffer,
                mimetype='text/plain',
                as_attachment=True,
                download_name='humanized.txt'
            )
        
        elif format == 'docx':
            # Word document
            doc = Document()
            doc.add_paragraph(text)
            
            buffer = io.BytesIO()
            doc.save(buffer)
            buffer.seek(0)
            
            return send_file(
                buffer,
                mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                as_attachment=True,
                download_name='humanized.docx'
            )
        
        elif format == 'pdf':
            # PDF document
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font('Arial', size=12)
            
            # Handle Unicode by encoding
            for line in text.split('\n'):
                pdf.multi_cell(0, 10, line.encode('latin-1', 'replace').decode('latin-1'))
            
            buffer = io.BytesIO()
            pdf.output(buffer)
            buffer.seek(0)
            
            return send_file(
                buffer,
                mimetype='application/pdf',
                as_attachment=True,
                download_name='humanized.pdf'
            )
        
        else:
            return jsonify({'error': 'Unsupported format'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
