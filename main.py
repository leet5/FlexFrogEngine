import logging
import os
from model import load_model_and_processor, generate_caption_for_image
from tags import generate_tags_from_caption

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def process_images_in_directory(img_dir, processor, model):
    """Process all images in a directory, generate captions, and extract tags."""
    # List all image files in the directory
    image_files = [f for f in os.listdir(img_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]

    # Log the number of images found
    logger.info(f"Found {len(image_files)} images in '{img_dir}'.")

    # Generate captions and tags for each image
    captions_and_tags = {}
    for img_name in image_files:
        img_path = os.path.join(img_dir, img_name)
        caption = generate_caption_for_image(img_path, processor, model)
        if caption:
            tags = generate_tags_from_caption(caption)
            captions_and_tags[img_name] = {"caption": caption, "tags": tags}
    return captions_and_tags


def main():
    img_dir = "images"  # Change this to the path of your image directory

    # Load the model and processor
    processor, model = load_model_and_processor()

    # Process all images and generate captions and tags
    captions_and_tags = process_images_in_directory(img_dir, processor, model)

    # Optionally, log or save the generated captions and tags
    if captions_and_tags:
        logger.info("Generated captions and tags for all images.")
        for img_name, data in captions_and_tags.items():
            logger.info(f"Image: {img_name}")
            logger.info(f"Caption: {data['caption']}")
            logger.info(f"Tags: {', '.join(data['tags'])}")
    else:
        logger.warning("No captions or tags were generated.")


# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()