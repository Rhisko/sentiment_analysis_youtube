from data_collection.youtube_data_collector import get_video_comments,get_youtube_video_id
from preprocessing.clean_comments import preprocess_comments,assign_candidate
from sentiment_analysis.analyze_sentiment import analyze_sentiment , process_sentiment_dataset
from sentiment_analysis.sentiment_report import generate_report
from utils.logger import setup_logging
from utils.helpers import load_yaml
from sentiment_analysis.textblob_sentiment import analyze_sentiment_textblob
from visualization.plot_score_trend import create_grafik_score
from visualization.plot_sentiment_distribution import create_grafik_sentiment_distribution
import csv





def save_to_csv(file_path, data):
    with open(file_path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["comment", "paslon"])
        writer.writeheader()  # Write the header
        writer.writerows(data) 

def main():
    logger = setup_logging()
    
    # Load configuration
    config = load_yaml("config/config.yaml")
    
    # Data Collection
    logger.info("Collecting data from YouTube")
    comments=[]
    
    for video in config["video_url"]:
        video_id= get_youtube_video_id(video)
        # print(video_id)
        comment = get_video_comments(config["api_key"], video_id, config["max_comments"])
        comments.extend(comment)

    # Save the CSV string to a file
    # save_to_csv("data/raw/comments_raw.csv",comments)


    # # Data Preprocessing
    logger.info("Preprocessing comments")
    clean_comments = preprocess_comments(comments)
    results_with_candidate = []
    for comment in clean_comments:
        candidates = assign_candidate(comment, config["keywords"])
        results_with_candidate.append({"comment": comment, "paslon": candidates})
    # print(results_with_candidate[:5])

        
    save_to_csv("data/raw/comments_raw_cleaned.csv",results_with_candidate)
    # clean_comments_with_candidate = assign_candidate(clean_comments,config["keywords"])

    
    
    # df=pd.read_csv("data/raw/comments_raw_cleaned.csv")
    # empty_columns = df.columns[df.isnull().all()].tolist()
    # print(empty_columns)
    # print(clean_comments)
    
    # # Sentiment Analysis
    logger.info("Analyzing sentiment")
    output_file="data/processed/dataset_with_sentiments.csv"
    process_sentiment_dataset("data/raw/comments_raw_cleaned.csv",output_file)
    create_grafik_sentiment_distribution(output_file)
    # print(sentiment_results)
    
    # Generate Report
    # logger.info("Generating sentiment report")
    # generate_report(sentiment_results)
    
    # # show Grafik
    # logger.info("Show Sentiment score & sentiment distribution")
    # file_path = "data/processed/sentiment_report.json"
    # create_grafik_score(file_path)
    

if __name__ == "__main__":
    main()
