# Image Captioning and Tagging System

<img src="logo.png" width="256" alt="">

This project is an automated system for generating captions and tags for images using a pre-trained BLIP (Bootstrapped Language-Image Pretraining) model. It processes images from a database, generates captions and tags, and saves the results back to the database.

## Features

- **Image Captioning**: Generates descriptive captions for images using the BLIP model.
- **Tag Generation**: Extracts tags from captions for easier categorization.
- **Database Integration**: Fetches images from a database and saves generated tags back to it.
- **Dockerized Deployment**: Supports multi-architecture Docker builds for easy deployment.
- **Logging**: Provides detailed logs for debugging and monitoring.

## Technologies Used

- **Python**: Core programming language.
- **Transformers**: For using the BLIP model.
- **Pillow**: For image processing.
- **PyTorch**: For running the BLIP model.
- **Docker**: For containerization.
- **GitHub Actions**: For CI/CD workflows.

## Prerequisites

- Python 3.11
- Docker (optional for containerized deployment)
- A database for storing and retrieving images and tags
- Required Python dependencies (see `requirements.txt`)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/leet5/image-captioning-system.git
   cd image-captioning-system