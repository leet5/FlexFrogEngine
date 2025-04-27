import os

import psycopg

from logging_config import logger


def get_db_connection():
    try:
        logger.debug("Establishing database connection...")
        conn = psycopg.connect(
            dbname=os.environ.get("DB_NAME", "flex_frog_db"),
            user=os.environ.get("DB_USER", "admin"),
            password=os.environ.get("DB_PASSWORD", "admin"),
            host=os.environ.get("DB_HOST", "localhost"),
            port=os.environ.get("DB_PORT", "5432")
        )
        logger.debug("Database connection established successfully.")
        return conn
    except Exception as e:
        logger.exception("Failed to establish database connection.")
        raise


def fetch_images_from_db_since(timestamp):
    try:
        logger.info(f"Fetching images created after {timestamp}...")
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT id, image_data, created_at FROM images WHERE created_at > %s", (timestamp,))
            results = cur.fetchall()
            logger.info(f"Fetched {len(results)} images from the database.")
            return results
    except Exception as e:
        logger.exception("Error fetching images from the database.")
        return []
    finally:
        conn.close()


def save_tags_to_db(image_id, tags):
    try:
        logger.info(f"Saving tags for image_id {image_id}: {tags}")
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                for tag_name in tags:
                    logger.debug(f"Processing tag: {tag_name}")

                    cursor.execute("""
                                   INSERT INTO tags (name)
                                   VALUES (%s) ON CONFLICT (name) DO NOTHING;
                                   """, (tag_name,))

                    cursor.execute("SELECT id FROM tags WHERE name = %s;", (tag_name,))
                    tag_id = cursor.fetchone()[0]

                    cursor.execute("""
                                   INSERT INTO images_tags (image_id, tag_id)
                                   VALUES (%s, %s) ON CONFLICT DO NOTHING;
                                   """, (image_id, tag_id))
            conn.commit()
        logger.info(f"Tags saved successfully for image_id {image_id}")
    except Exception as e:
        logger.exception(f"Failed to save tags for image_id {image_id}")
