from logging_config import logger  # Import the logger from logging_config.py
import string
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def generate_tags_from_caption(caption):
    """Generate tags (keywords) from the caption."""
    # Preprocess caption: remove punctuation, convert to lowercase
    caption = caption.lower()
    caption = caption.translate(str.maketrans('', '', string.punctuation))

    # Tokenize and remove stopwords
    stop_words = set(stopwords.words('english'))
    words = caption.split()
    words = [word for word in words if word not in stop_words]

    # Use TfidfVectorizer to calculate TF-IDF values for the words
    vectorizer = TfidfVectorizer(stop_words='english', max_features=10)
    tfidf_matrix = vectorizer.fit_transform([' '.join(words)])

    # Get the feature names (words) and their corresponding TF-IDF values
    feature_names = np.array(vectorizer.get_feature_names_out())
    tfidf_values = tfidf_matrix.toarray().flatten()

    # Get the top 10 words with the highest TF-IDF scores
    sorted_indices = np.argsort(tfidf_values)[::-1]  # Sort in descending order
    top_words = feature_names[sorted_indices][:10]  # Top 10 words based on TF-IDF score

    logger.info(f"Generated tags: {top_words}")

    return top_words