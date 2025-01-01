from transformers import pipeline

def analyze_sentiment(text):
    sentiment_pipeline = pipeline("sentiment-analysis")
    result = sentiment_pipeline(text)
    return result

def extract_entities(text):
    ner_pipeline = pipeline("ner", grouped_entities=True)
    result = ner_pipeline(text)
    return result