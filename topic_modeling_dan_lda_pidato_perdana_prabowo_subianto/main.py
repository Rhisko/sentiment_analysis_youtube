from src.download_video import download_video_audio 
from src.transcribe import transcribe_audio
from src.data_preprocessing import DataPreprocessor
from src.lda_modeling import LdaModeling
from src.visualization import Visualization

def main(youtube_url):
    # Step 1: Download video
    print("Downloading audio only from youtube video...")
    video_id=download_video_audio(youtube_url)


    # Step 2: Transcribe audio
    print("Transcribing audio...")
    text = transcribe_audio(f"data/audios/{video_id}.webm",video_id)

    
    # Load and preprocess data
    data_preprocessor = DataPreprocessor(f'data/transcripts/transcription_{video_id}.csv',video_id)
    data_preprocessor.load_data()
    df = data_preprocessor.preprocess()
    print(f"Dataframe After Cleaned : {df['Transcription_after_preprocess']} \n {df['Transcription_tokens']}")

    # # Build LDA model
    lda_modeling = LdaModeling(df,video_id, total_topics=3, number_words=10)
    lda_modeling.create_corpus()
    lda_modeling.build_model()
    lda_modeling.print_topics()
    lda_modeling.word_count_of_topic_keywords()
    sent_topics_df = lda_modeling.format_topics_sentences(corpus=lda_modeling.corpus, texts=lda_modeling.tokenized_texts)
    print(f"{sent_topics_df}")
    # # Visualize results
    filename=f"data/outputs/lda_visualization_{video_id}.html"
    visualization = Visualization(lda_modeling.lda_model, lda_modeling.corpus, lda_modeling.dictionary)
    visualization.save(filename)


if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=56mWVnv0wQk" # please change with your Youtube Video
    main(url)