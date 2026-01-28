# Multi-stage build for optimized container
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Download NLP models
RUN python -m spacy download en_core_web_lg
RUN python -m nltk.downloader punkt wordnet averaged_perceptron_tagger

# Production stage
FROM python:3.11-slim

WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy application code
COPY . .

# Make CLI executable
ENV PATH=/root/.local/bin:$PATH

# Expose port for web interface
EXPOSE 5000

# Default command runs web interface
CMD ["python", "web/app.py"]
