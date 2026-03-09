# Zeal Code UI - Dockerfile
FROM python:3.11-slim

LABEL maintainer="Riadhi Aditya Hermawan <ridzeal>"
LABEL description="Zeal Code UI - Streamlit web interface"

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ui/ ./ui/
COPY code_analysis/ ./code_analysis/
COPY code_generation/ ./code_generation/
COPY nlp_module/ ./nlp_module/
COPY code_review/ ./code_review/
COPY debugging/ ./debugging/

# Create non-root user
RUN useradd -m -u 1000 zealuser && \
    chown -R zealuser:zealuser /app
USER zealuser

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run Streamlit application
CMD ["streamlit", "run", "ui/web_interface.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true", "--server.fileWatcherType=none"]
