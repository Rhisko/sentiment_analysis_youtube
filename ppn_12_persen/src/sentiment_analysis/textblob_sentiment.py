from textblob import TextBlob
from googletrans import Translator

def analyze_sentiment_textblob(comments):
    translator = Translator()
    results = []
    for comment in comments:
        try:
            # Translate the comment to English
            translation = translator.translate(comment, dest="en")
            translated_comment = translation.text
            # Analyze sentiment on the translated text
            polarity = TextBlob(translated_comment).sentiment.polarity
        except Exception as e:
            # Log or handle translation failures
            print(f"Translation failed for: {comment} - Error: {e}")
            translated_comment = comment
            polarity = TextBlob(comment).sentiment.polarity

        results.append({"comment": comment, "translated": translated_comment, "polarity": polarity})
    return results


