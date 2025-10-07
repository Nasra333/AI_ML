# Use Python slim image for faster builds
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first for better caching
COPY requirements-prod.txt .

# Install Python dependencies with optimizations
RUN pip install --no-cache-dir -r requirements-prod.txt

# Copy application code
COPY app.py .
COPY constants.py .
COPY utils.py .
COPY tabs/ tabs/

# Expose port (Railway will override this)
EXPOSE 7860

# Run the application
CMD ["python", "app.py"]
