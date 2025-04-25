FROM python:3.11-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies and clean up
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download NLTK stopwords and models
RUN python -m nltk.downloader stopwords \
    && python -c "from transformers import BlipProcessor, BlipForConditionalGeneration; \
    BlipProcessor.from_pretrained('Salesforce/blip-image-captioning-base', use_fast=True); \
    BlipForConditionalGeneration.from_pretrained('Salesforce/blip-image-captioning-base')"

# Copy application code into the container
COPY . .

# Set the default command to run your application
CMD ["python", "main.py"]