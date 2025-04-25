import io

import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

from logging_config import logger  # Import the logger from logging_config.py

# Device setup: Use MPS if available, otherwise fall back to CPU
device = "mps" if torch.backends.mps.is_available() else "cpu"


def load_model_and_processor():
    logger.info("Loading model and processor...")
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base", use_fast=True)
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    model.to(device)
    logger.info("Model and processor loaded successfully.")
    return processor, model


def generate_caption_for_image(image_data, image_name, processor, model):
    try:
        logger.info(f"Processing image: {image_name}")
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
        inputs = processor(image, return_tensors="pt").to(device)
        with torch.no_grad():
            output = model.generate(
                **inputs,
                max_length=100,  # Set a maximum length for the caption
                num_beams=5,  # Use beam search for more diverse generation
                early_stopping=True
            )
        caption = processor.decode(output[0], skip_special_tokens=True)
        logger.info(f"Caption for {image_name}: {caption}")
        return caption
    except Exception as e:
        logger.error(f"Error processing {image_name}: {e}")
        return None
