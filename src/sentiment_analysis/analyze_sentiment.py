from transformers import pipeline

# sentiment_pipeline = pipeline(
#     "sentiment-analysis",
#     model="indobenchmark/indobert-base-p2",
#     tokenizer="indobenchmark/indobert-base-p2"
# )
# sentiment_pipeline = pipeline(
#     "sentiment-analysis",
#     model="xlm-roberta-base",
#     tokenizer="xlm-roberta-base"
# )
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="bert-base-multilingual-cased",
    tokenizer="bert-base-multilingual-cased"
)

label_mapping = {
    "LABEL_0": "negative",
    "LABEL_1": "neutral",
    "LABEL_2": "positive"
}

def analyze_sentiment(comments):
    results = []
    for comment in comments:
        if comment.strip():  
            try:
                analysis = sentiment_pipeline(comment)
                label = analysis[0]['label']
                sentiment = label_mapping.get(label, "unknown")  # Map label ke sentimen
                results.append({
                    "comment": comment,
                    "sentiment": sentiment,
                    "score": round(analysis[0]['score'], 2)
                })
            except Exception as e:
                print(f"Error processing comment: {comment}. Error: {e}")
        else:
            print(f"empty Comment")
            # results.append({
            #     "comment": comment,
            #     "sentiment": "neutral",
            #     "score": 0
            # })
    return results

# def analyze_sentiment(comments):
#     results = []
#     for comment in comments:
#         if comment.strip():  # Skip empty comments
#             analysis = sentiment_pipeline(comment)
#             label = analysis[0]['label']
#             sentiment = label_mapping.get(label, "unknown")  # Map label to sentiment
#             results.append({
#                 "comment": comment,
#                 "sentiment": sentiment,  # Mapped sentiment label
#                 "score": round(analysis[0]['score'], 2)  # Rounded confidence score
#             })
#         else:
#             # Handle empty comments as neutral
#             results.append({
#                 "comment": comment,
#                 "sentiment": "neutral",
#                 "score": 0
#             })
#     return results