# 🔧 Text cleaning, polarity functions
import re
from textblob import TextBlob

def clean_text(text):
    """Cleans tweet text by removing mentions, URLs, and other noise."""
    text = re.sub(r'@[A-Za-z0-9_]+', '', text)  # Remove @mentions
    text = re.sub(r'#', '', text)                # Remove the '#' symbol (keep the word)
    text = re.sub(r'RT[\s]+', '', text)          # Remove RT
    text = re.sub(r'https?:\/\/\S+', '', text)   # Remove hyperlinks
    text = re.sub(r'\n', ' ', text)              # Replace newlines with spaces
    return text.strip()

def get_subjectivity(text):
    """Calculates the subjectivity of a text using TextBlob."""
    return TextBlob(text).sentiment.subjectivity

def get_polarity(text):
    """Calculates the polarity of a text using TextBlob."""
    return TextBlob(text).sentiment.polarity

def get_sentiment_label(polarity_score):
    """Converts a polarity score into a sentiment label."""
    if polarity_score < 0:
        return "Negative"
    elif polarity_score == 0:
        return "Neutral"
    else:
        return "Positive"