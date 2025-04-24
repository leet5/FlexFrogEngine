import io
from db import save_tags_to_db  # Import the function to save tags
from PIL import Image
from model import generate_caption_for_image
from tags import generate_tags_from_caption

def process_images_from_db(fetch_images_function, processor, model):
    """Process images fetched from PostgreSQL database, generate captions, and extract tags."""
    # Fetch images from the database
    images = fetch_images_function()

    # Log the number of images found
    print(f"Found {len(images)} images in the database.")

    # Generate captions and tags for each image
    captions_and_tags = {}
    for image in images:
        img_id, img_filename, img_data = image

        # Convert the binary image data to a PIL Image
        img = Image.open(io.BytesIO(img_data))

        # Generate the caption using the model and processor
        caption = generate_caption_for_image(img, processor, model)

        if caption:
            tags = generate_tags_from_caption(caption)
            captions_and_tags[img_filename] = {"caption": caption, "tags": tags}

            # Save the tags to the database
            save_tags_to_db(img_id, tags)  # Save the tags and associate them with the image

    return captions_and_tags