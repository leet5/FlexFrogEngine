import psycopg

# Function to connect to PostgreSQL database
def get_db_connection():
    """Connect to PostgreSQL and return the connection."""
    return psycopg.connect(
        dbname="flex_frog_db", user="admin", password="admin", host="localhost", port="5432"
    )

# Function to fetch images as binary data from the database
def fetch_images_from_db():
    """Fetch image data (filename and binary image data) from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, filename, image_data FROM Images;")
    images = cursor.fetchall()

    cursor.close()
    conn.close()

    return images

# Function to save generated tags to the database
def save_tags_to_db(image_id, tags):
    """Save the generated tags to the database and associate them with an image."""
    conn = get_db_connection()
    cursor = conn.cursor()

    for tag in tags:
        cursor.execute(
            "INSERT INTO Tags (image_id, tag) VALUES (%s, %s);",
            (image_id, tag)
        )
    conn.commit()
    cursor.close()
    conn.close()