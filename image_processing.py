from typing import Any, Dict

from db import save_tags_to_db
from logging_config import logger
from model import generate_caption_for_image
from tags import generate_tags_from_caption


def process_images_from_db(images: list, processor: Any, model: Any) -> Dict[str, Dict[str, Any]]:
    try:
        logger.info(f"Found {len(images)} images in the database.")
    except Exception:
        logger.exception("Failed to fetch images from the database.")
        return {}

    captions_and_tags = {}
    for image in images:
        image_id, image_name, image_data, created_at = image

        try:
            caption = generate_caption_for_image(image_data, image_name, processor, model)
        except Exception:
            logger.exception(f"Failed to generate caption for image: {image_name}")
            continue

        if not caption:
            logger.warning(f"No caption generated for image: {image_name}")
            continue

        tags = generate_tags_from_caption(caption)
        captions_and_tags[image_name] = {"caption": caption, "tags": tags}

        try:
            save_tags_to_db(image_id, tags)
        except Exception:
            logger.exception(f"Failed to save tags for image: {image_name}")

    return captions_and_tags
