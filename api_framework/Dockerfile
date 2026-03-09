# Zeal Code API - Dockerfile
FROM python:3.11-slim

LABEL maintainer="Riadhi Aditya Hermawan <ridzeal>"
LABEL description="Zeal Code API - AI-powered code assistant backend"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY api_framework/ ./api_framework/
COPY nlp_module/ ./nlp_module/
COPY code_analysis/ ./code_analysis/
COPY code_generation/ ./code_generation/
COPY code_review/ ./code_review/
COPY debugging/ ./debugging/
COPY documentation/ ./documentation/
COPY monitoring/ ./monitoring/
COPY performance/ ./performance/
COPY security/ ./security/

# Create non-root user
RUN useradd -m -u 1000 zealuser && \
    chown -R zealuser:zealuser /app
USER zealuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run the application
CMD ["uvicorn", "api_framework.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
