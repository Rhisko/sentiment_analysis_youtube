import json

def generate_report(sentiment_results, output_file="data/processed/sentiment_report.json"):
    with open(output_file, "w") as f:
        json.dump(sentiment_results, f, indent=4)
    print("Sentiment report saved to", output_file)

