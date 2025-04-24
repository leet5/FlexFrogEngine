import logging
import string
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

# Set up logging
logger = logging.getLogger(__name__)


def generate_tags_from_caption(caption):
    """Generate tags (keywords) from the caption."""
    # Preprocess caption: remove punctuation, convert to lowercase
    caption = caption.lower()
    caption = caption.translate(str.maketrans('', '', string.punctuation))

    # Tokenize and remove stopwords
    stop_words = set(stopwords.words('english'))
    words = caption.split()
    words = [word for word in words if word not in stop_words]

    # Use a simple method to return the most frequent words as tags
    vectorizer = TfidfVectorizer(stop_words='english', max_features=10)
    tfidf_matrix = vectorizer.fit_transform([' '.join(words)])
    tags = vectorizer.get_feature_names_out()

    logger.info(f"Generated tags: {tags}")
    return tags