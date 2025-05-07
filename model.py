import io

import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

from logging_config import logger  # Import the logger from logging_config.py

# Device setup: Use MPS if available, otherwise fall back to CPU
device = "mps" if torch.backends.mps.is_available() else "cpu"


def load_model_and_processor():
    logger.info("Loading model and processor...")
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large", use_fast=True)
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large", torch_dtype=torch.float32)
    model.to(device)
    logger.info("Model and processor loaded successfully.")
    return processor, model


def generate_caption_for_image(image_data, image_name, processor, model):
    try:
        logger.info(f"Processing image: {image_name}")
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
        inputs = processor(images=image, return_tensors="pt").to(device)
        with torch.no_grad():
            output = model.generate(
                **inputs,
                do_sample=True,
                top_p=0.9,
                temperature=0.8,
                max_new_tokens=200,  # Higher value for longer captions
                repetition_penalty=1.2
            )
        caption = processor.tokenizer.decode(output[0], skip_special_tokens=True)
        logger.info(f"Caption for {image_name}: {caption}")
        return caption
    except Exception as e:
        logger.error(f"Error processing {image_name}: {e}")
        return None
