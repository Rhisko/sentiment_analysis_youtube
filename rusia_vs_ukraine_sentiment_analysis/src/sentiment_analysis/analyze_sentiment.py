from transformers import pipeline
import pandas as pd
from utils.helpers import load_yaml
from transformers import pipeline, AutoTokenizer

# Explicitly load tokenizer
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")


def initialize_sentiment_pipeline():
    return pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english",
        tokenizer=tokenizer
    )

    # return pipeline(
    #     "sentiment-analysis",
    #     model="nlptown/bert-base-multilingual-uncased-sentiment",
    #     tokenizer="nlptown/bert-base-multilingual-uncased-sentiment"
    # )

# def map_sentiment_to_category(label):
#     if label in ["4 stars", "5 stars"]:
#         return "positif"
#     elif label in ["3 stars"]:
#         return "netral"
#     elif label in ["1 star", "2 stars"]:
#         return "negatif"
#     else:
#         return "unknown"
def map_sentiment_to_category(label, score):
    if label == "POSITIVE":
        if score > 0.75:
            return "positif"
        else:
            return "netral" 
    elif label == "NEGATIVE":
        if score > 0.75:  
            return "negatif"
        else:
            return "netral" 
    else:
        return "unknown"
  


def dictionary_sentiment_analysis(text):
    sentiment_dict= load_yaml("config/config.yaml")
    text_lower = text.lower()
    for sentiment, keywords in sentiment_dict["SENTIMENT_DICTIONARY"].items():
        if any(keyword in text_lower for keyword in keywords):
            return sentiment
    return None

def analyze_sentiment(text, sentiment_pipeline):
    try:
        # First, use the dictionary-based sentiment analysis
        dict_sentiment = dictionary_sentiment_analysis(text)
        if dict_sentiment:
            return dict_sentiment  # Use dictionary result if available

        # Fall back to model-based sentiment analysis
        result = sentiment_pipeline(text[:512])  # limit to 512 characters
        # label = result[0]['label']
        label = result[0]['label']
        score = result[0]['score']
        return map_sentiment_to_category(label,score)
    except Exception as e:
        return "error"

def process_sentiment_dataset(file_path, output_path, comment_column="comment"):
    dataset = pd.read_csv(file_path)
    dataset = dataset[dataset['comment_target'] != "unknown"]
    sentiment_pipeline = initialize_sentiment_pipeline()

    # Apply sentiment analysis to each comment
    dataset["sentiment"] = dataset[comment_column].apply(
        lambda x: analyze_sentiment(x, sentiment_pipeline)
    )

    dataset.to_csv(output_path, index=False)
    print(f"Dataset has been created successfully: {output_path}")

    return dataset


