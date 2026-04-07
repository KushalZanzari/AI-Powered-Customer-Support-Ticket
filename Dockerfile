FROM python:3.10-slim

LABEL maintainer="OpenEnv Customer Support Env"
LABEL org.opencontainers.image.source="https://github.com/your-username/customer-support-env"

WORKDIR /app

# Install dependencies first (layer caching)
COPY env/server/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt && rm /tmp/requirements.txt

# Copy application code
COPY env/ /app/env/

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Run the server
CMD ["uvicorn", "env.server.app:app", "--host", "0.0.0.0", "--port", "8000"]
