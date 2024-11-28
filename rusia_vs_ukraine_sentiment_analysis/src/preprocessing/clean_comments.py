import re
import unicodedata
from nltk.corpus import stopwords
from utils.helpers import load_yaml
# # Ensure the stopwords resource is downloaded
# import nltk
# nltk.download('stopwords')

# # Define the stopword list for Indonesian
# stop_words = set(stopwords.words('indonesian'))

def replace_slang(text):
    slang_dict= load_yaml("config/config.yaml")
    words = text.split()
    replaced_words = [slang_dict['slang_to_formal'].get(word.lower(), word) for word in words]
    return ' '.join(replaced_words)

def clean_comment(comment):
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
    comment = replace_slang(comment)
    # # Remove stopwords
    # comment_words = comment.split()
    # comment = ' '.join(word for word in comment_words if word not in stop_words)
    # Strip leading and trailing spaces
    return comment.strip() if comment.strip() else None


def preprocess_comments(comments):
    return [clean_comment(comment) for comment in comments if clean_comment(comment)]


def assign_comment(comment, keywords):
    detected_coment = []
    for candidate, terms in keywords.items():
        # print(f"{candidate} - {terms}")
        if any(term in comment.lower() for term in terms):
            detected_coment.append(candidate)
    return ", ".join(detected_coment) if detected_coment else "unknown"

