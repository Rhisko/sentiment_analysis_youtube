import json
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import nltk
from nltk.corpus import stopwords

# def load_data(file_path):
#     """
#     Load JSON data from a file.
    
#     Parameters:
#     - file_path (str): Path to the JSON file containing the sentiment data.
    
#     Returns:
#     - list: List of dictionaries with sentiment data.
#     """
#     with open(file_path, 'r', encoding='utf-8') as f:
#         data = json.load(f)
#     return data

# def get_sentiment_counts(data):
#     """
#     Count occurrences of each sentiment label.
    
#     Parameters:
#     - data (list): List of dictionaries, each containing a 'sentiment' field.
    
#     Returns:
#     - dict: Dictionary with sentiment labels as keys and their counts as values.
#     """
#     sentiments = [item['sentiment'] for item in data]
#     sentiment_counts = Counter(sentiments)
#     return sentiment_counts

# def plot_bar_chart(sentiment_counts):
#     """
#     Plot the sentiment distribution as a bar chart.
    
#     Parameters:
#     - sentiment_counts (dict): Dictionary with sentiment labels and their respective counts.
#     """
#     labels = list(sentiment_counts.keys())
#     counts = list(sentiment_counts.values())
    
#     plt.figure(figsize=(10, 6))
#     plt.bar(labels, counts, color=['blue', 'red', 'green', 'purple', 'orange'])
#     plt.title('Sentiment Distribution (Bar Chart)')
#     plt.xlabel('Sentiments')
#     plt.ylabel('Number of Comments')
#     plt.show()

# def plot_pie_chart(sentiment_counts):
#     """
#     Plot the sentiment distribution as a pie chart.
    
#     Parameters:
#     - sentiment_counts (dict): Dictionary with sentiment labels and their respective counts.
#     """
#     labels = list(sentiment_counts.keys())
#     counts = list(sentiment_counts.values())
    
#     plt.figure(figsize=(8, 8))
#     plt.pie(counts, labels=labels, autopct='%1.1f%%', startangle=140, colors=['blue', 'red', 'green', 'purple', 'orange'])
#     plt.title('Sentiment Distribution (Pie Chart)')
#     plt.show()

def create_grafik_sentiment_distribution(file_path):
    df = pd.read_csv(file_path)

    pivot_table = df.pivot_table(
        index="kebijakan", 
        columns="sentiment", 
        aggfunc="size", 
        fill_value=0
    )
    
    # Calculate total comments per kebijakan
    pivot_table["total_comments"] = pivot_table.sum(axis=1)

    # Bar chart for sentiment distribution
    ax = pivot_table.drop(columns="total_comments").plot(
        kind="bar", 
        figsize=(10, 6), 
        stacked=False, 
        color={"positif": "green", "netral": "orange", "negatif": "red"}
    )
    plt.title("Distribusi Sentimen Berdasarkan kebijakan")
    plt.xlabel("kebijakan")
    plt.ylabel("Jumlah Komentar")
    plt.legend(title="Sentimen")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.xticks(rotation=45)

    # Add total comments as annotations
    for idx, total in enumerate(pivot_table["total_comments"]):
        ax.text(idx, pivot_table.drop(columns="total_comments").iloc[idx].max() + 2, 
                f"Total: {total}", 
                ha="center", fontsize=10, color="black")
    plt.show()

    # Pie charts for each kebijakan
    for kebijakan in pivot_table.index:
        sentiment_counts = pivot_table.drop(columns="total_comments").loc[kebijakan]
        total_comments = pivot_table.loc[kebijakan, "total_comments"]
        
        sentiment_counts.plot(
            kind="pie", 
            autopct="%1.1f%%", 
            colors=["red", "orange", "green"], 
            startangle=90, 
            figsize=(6, 6)
        )
        plt.title(f"Distribusi Sentimen untuk kebijakan {kebijakan}\nTotal Komentar: {total_comments}")
        plt.ylabel("")  # Remove y-axis label for better visualization
        plt.show()
        
    text_data = " ".join(comment for comment in df['comment'].astype(str))

    # Generate a word cloud
    nltk.download('stopwords')

# Ambil stop words dari NLTK
    stop_words = set(stopwords.words('indonesian'))
    additional_stopwords = {'yang', 'dan', 'di', 'itu', 'untuk', 'saja', 'dari', 'kalau', 'akan','yg'}
    stop_words = stop_words.union(additional_stopwords)
    wordcloud = WordCloud(stopwords=stop_words, width=800, height=400,background_color='white').generate(text_data)
     

    # Display the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Word Cloud of Comments", fontsize=16)
    plt.show()
