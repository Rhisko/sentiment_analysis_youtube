from data_collection.youtube_data_collector import get_video_comments, get_youtube_video_id
from preprocessing.clean_comments import preprocess_comments, assign_comment
from sentiment_analysis.analyze_sentiment import process_sentiment_dataset
from utils.logger import setup_logging
from utils.helpers import load_yaml
from visualization.plot_sentiment_distribution import create_grafik_sentiment_distribution
from data_collection.create_report_csv import save_to_csv
import os

token = os.getenv("TOKEN")

def collect_data(config, logger):
    logger.info("Collecting data from YouTube")
    all_comments = []
    for video_url in config["video_url"]:
        try:
            video_id = get_youtube_video_id(video_url)
            comments = get_video_comments(token, video_id, config["max_comments"])
            all_comments.extend(comments)
        except Exception as e:
            logger.error(f"Error collecting comments for video {video_url}: {e}")
    return all_comments


def preprocess_data(comments, config, logger):
    logger.info("Preprocessing comments")
    clean_comments = preprocess_comments(comments)
    comment_related = [
        {"comment": comment, "kebijakan": assign_comment(comment, config["keywords"])}
        for comment in clean_comments
    ]
    return comment_related


def perform_sentiment_analysis(cleaned_file, output_file, logger):
    logger.info("Analyzing sentiment")
    # process_sentiment_dataset(cleaned_file, output_file)
    create_grafik_sentiment_distribution(output_file)


def main():
    logger = setup_logging()
    
    try:
        # # Load configuration
        # logger.info("Loading configuration")
        # config = load_yaml("config/config.yaml")
        
        # # Step 1: Data Collection
        # comments = collect_data(config, logger)
        # logger.info(f"Collected {len(comments)} comments")
        
        # # Save raw comments
        # raw_comments_file = "data/raw/comments_raw.txt"
        # save_to_csv(raw_comments_file, comments)
        # logger.info(f"Saved raw comments to {raw_comments_file}")
        
        # # # Step 2: Data Preprocessing
        # comment_related = preprocess_data(comments, config, logger)
        cleaned_file = "data/processed/comments_raw_cleaned.csv"
        # save_to_csv(cleaned_file, comment_related, fieldnames=["comment", "kebijakan"])
        # logger.info(f"Saved preprocessed comments to {cleaned_file}")
        
        # #Step 3: Sentiment Analysis
        output_file = "data/outputs/dataset_with_sentiments.csv"
        perform_sentiment_analysis(cleaned_file, output_file, logger)
        logger.info(f"Sentiment analysis completed. Output saved to {output_file}")
    
    except Exception as e:
        logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
