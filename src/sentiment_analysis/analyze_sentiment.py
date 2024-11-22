from transformers import pipeline
import pandas as pd

def initialize_sentiment_pipeline():
    return pipeline(
        "sentiment-analysis",
        model="nlptown/bert-base-multilingual-uncased-sentiment",
        tokenizer="nlptown/bert-base-multilingual-uncased-sentiment"
    )

def map_sentiment_to_category(label):
    if label in ["4 stars", "5 stars"]:
        return "positif"
    elif label in ["3 stars"]:
        return "netral"
    elif label in ["1 star", "2 stars"]:
        return "negatif"
    else:
        return "unknown"  


def analyze_sentiment(text, sentiment_pipeline):
    try:
        result = sentiment_pipeline(text[:512])  # limit 512
        label = result[0]['label']  
        return map_sentiment_to_category(label) 
    except Exception as e:
        return "error"  


def process_sentiment_dataset(file_path, output_path, comment_column="comment"):

    dataset = pd.read_csv(file_path)
    sentiment_pipeline = initialize_sentiment_pipeline()
    dataset["sentiment"] = dataset[comment_column].apply(lambda x: analyze_sentiment(x, sentiment_pipeline))
    dataset.to_csv(output_path, index=False)
    print(f"Dataset has been created succesfully {output_path}")
    
    return dataset

