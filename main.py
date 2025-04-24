from db import fetch_images_from_db
from image_processing import process_images_from_db
from logging_config import logger
from model import load_model_and_processor


def main():
    # Load the model and processor
    processor, model = load_model_and_processor()

    # Process all images fetched from PostgreSQL and generate captions and tags
    captions_and_tags = process_images_from_db(fetch_images_from_db, processor, model)

    # Optionally, log or save the generated captions and tags
    if captions_and_tags:
        logger.info("Generated captions and tags for all images.")
        for img_filename, data in captions_and_tags.items():
            logger.info(f"Image: {img_filename}")
            logger.info(f"Caption: {data['caption']}")
            logger.info(f"Tags: {', '.join(data['tags'])}")
    else:
        logger.warning("No captions or tags were generated.")


# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()
