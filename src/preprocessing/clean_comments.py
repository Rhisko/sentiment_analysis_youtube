import re
import pandas as pd
import unicodedata

def clean_comment(comment):
    """
    Clean and normalize a single comment by removing unwanted elements, non-Latin characters, and more.
    :param comment: The input string (comment) to be cleaned.
    :return: The cleaned and normalized comment string.
    """
    # Remove URLs
    comment = re.sub(r'http\S+|www\.\S+', '', comment)
    # Remove HTML tags
    comment = re.sub(r'<.*?>', '', comment)
    # Remove punctuation (including double quotes)
    comment = re.sub(r'[^\w\s]', '', comment)
    # Convert to lowercase
    comment = comment.lower()
    # Explicitly remove all types of quotes (straight or curly)
    comment = comment.replace('"', '').replace("'", '').replace("“", '').replace("”", '')
    # Remove non-Latin characters
    comment = re.sub(r'[^\u0020-\u00FF]', '', comment)
    # Remove accents
    comment = ''.join(
        char for char in unicodedata.normalize('NFKD', comment) 
        if not unicodedata.combining(char)
    )
    # Strip leading and trailing spaces
    return comment.strip() if comment.strip() else None

def preprocess_comments(comments):
    return [clean_comment(comment) for comment in comments if clean_comment(comment)]




def assign_candidate(comment, keywords):
    detected_candidates = []
    for candidate, terms in keywords.items():
        # print(f"{candidate} - {terms}")
        if any(term in comment.lower() for term in terms):
            detected_candidates.append(candidate)
    return ", ".join(detected_candidates) if detected_candidates else "unknown"

