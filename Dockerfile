FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV HF_HOME=/cache/transformers
ENV TORCH_HOME=/cache/torch

WORKDIR /app

# Install minimal system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Only download NLTK stopwords, skip BLIP model
RUN python -m nltk.downloader stopwords

COPY . .

# Create cache directory for transformers
RUN mkdir -p /cache/transformers

CMD ["python", "main.py"]