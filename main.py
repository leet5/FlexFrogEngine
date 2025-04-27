import time
from datetime import datetime, timezone

from db import fetch_images_from_db_since, save_tags_to_db
from image_processing import process_images_from_db
from logging_config import logger
from model import load_model_and_processor


def main():
    processor, model = load_model_and_processor()
    last_checked_time = datetime.now(timezone.utc)
    while True:
        try:
            images = fetch_images_from_db_since(last_checked_time)
            if images:
                logger.info(f"Found {len(images)} new image(s) to process.")
                captions_and_tags = process_images_from_db(images, processor, model)
                for image_id, _, _ in images:
                    result = captions_and_tags.get(image_id)
                    if result:
                        logger.info(f"Image: {image_id}")
                        logger.info(f"Caption: {result['caption']}")
                        logger.info(f"Tags: {', '.join(result['tags'])}")
                        save_tags_to_db(image_id, result["tags"])
                    else:
                        logger.warning(f"No tags generated for image: {image_id}")
                latest_time = max(img[2] for img in images)  # assuming img[3] is created_at
                last_checked_time = latest_time
            else:
                logger.info("No new images to process.")
        except Exception:
            logger.exception("Error occurred while processing new images.")
        time.sleep(10)


if __name__ == "__main__":
    main()
