import logging
import os
import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

# Set up logging
logger = logging.getLogger(__name__)

# Device setup: Use MPS if available, otherwise fall back to CPU
device = "mps" if torch.backends.mps.is_available() else "cpu"


def load_model_and_processor():
    """Load and return the BLIP model and processor."""
    logger.info("Loading model and processor...")
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base", use_fast=True)
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    model.to(device)
    logger.info("Model and processor loaded successfully.")
    return processor, model


def generate_caption_for_image(img_path, processor, model):
    """Generate a detailed caption for a single image."""
    try:
        logger.info(f"Processing image: {img_path}")

        # Open and process the image
        raw_image = Image.open(img_path).convert('RGB')

        # Prepare the image for BLIP
        inputs = processor(raw_image, return_tensors="pt").to(device)

        # Generate caption
        with torch.no_grad():
            output = model.generate(**inputs)

        # Decode and return the caption
        caption = processor.decode(output[0], skip_special_tokens=True)
        logger.info(f"Caption for {os.path.basename(img_path)}: {caption}")
        return caption
    except Exception as e:
        logger.error(f"Error processing {img_path}: {e}")
        return None