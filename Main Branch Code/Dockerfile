# Multi-stage build for smaller image
FROM python:3.11-slim as builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final production image
FROM python:3.11-slim

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app && \
    chown -R appuser:appuser /app

WORKDIR /app

# Copy dependencies from builder
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local

# Copy all application files
COPY --chown=appuser:appuser app.py .
COPY --chown=appuser:appuser models.py .
COPY --chown=appuser:appuser config.py .
COPY --chown=appuser:appuser forms.py .
COPY --chown=appuser:appuser templates.py .
COPY --chown=appuser:appuser templates_orders.py .
COPY --chown=appuser:appuser email_utils.py .
COPY --chown=appuser:appuser payment_utils.py .
COPY --chown=appuser:appuser requirements.txt .
COPY --chown=appuser:appuser static/ ./static/

# Copy .env file (optional, better to use K8s secrets)
COPY --chown=appuser:appuser .env* ./ 2>/dev/null || true

# Set environment variables
ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/').read()" || exit 1

# Run application
CMD ["python", "app.py"]
