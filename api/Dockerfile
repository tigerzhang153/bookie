# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files from api directory
COPY . .

# Verify model file is present and valid (not a Git LFS pointer)
# This will FAIL the build if the model file is a Git LFS pointer
RUN python3 -c "import os; path='recommender/ml_model.joblib'; size=os.path.getsize(path) if os.path.exists(path) else 0; print(f'Model file size: {size} bytes'); assert size > 100000000, f'Model file too small ({size} bytes) - likely Git LFS pointer! Expected ~149MB. Build will fail.'"

# Cloud Run uses PORT environment variable
ENV PORT=8080
EXPOSE 8080

# Run the application - use main:app since main.py is in the root of /app
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 --worker-class uvicorn.workers.UvicornWorker main:app
