import json
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd

def load_data(file_path):
    """
    Load JSON data from a file.
    
    Parameters:
    - file_path (str): Path to the JSON file containing the sentiment data.
    
    Returns:
    - list: List of dictionaries with sentiment data.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def get_sentiment_counts(data):
    """
    Count occurrences of each sentiment label.
    
    Parameters:
    - data (list): List of dictionaries, each containing a 'sentiment' field.
    
    Returns:
    - dict: Dictionary with sentiment labels as keys and their counts as values.
    """
    sentiments = [item['sentiment'] for item in data]
    sentiment_counts = Counter(sentiments)
    return sentiment_counts

def plot_bar_chart(sentiment_counts):
    """
    Plot the sentiment distribution as a bar chart.
    
    Parameters:
    - sentiment_counts (dict): Dictionary with sentiment labels and their respective counts.
    """
    labels = list(sentiment_counts.keys())
    counts = list(sentiment_counts.values())
    
    plt.figure(figsize=(10, 6))
    plt.bar(labels, counts, color=['blue', 'red', 'green', 'purple', 'orange'])
    plt.title('Sentiment Distribution (Bar Chart)')
    plt.xlabel('Sentiments')
    plt.ylabel('Number of Comments')
    plt.show()

def plot_pie_chart(sentiment_counts):
    """
    Plot the sentiment distribution as a pie chart.
    
    Parameters:
    - sentiment_counts (dict): Dictionary with sentiment labels and their respective counts.
    """
    labels = list(sentiment_counts.keys())
    counts = list(sentiment_counts.values())
    
    plt.figure(figsize=(8, 8))
    plt.pie(counts, labels=labels, autopct='%1.1f%%', startangle=140, colors=['blue', 'red', 'green', 'purple', 'orange'])
    plt.title('Sentiment Distribution (Pie Chart)')
    plt.show()

def create_grafik_sentiment_distribution(file_path):
    
    # file_path = "data/processed/dataset_with_sentiments.csv"  # Ganti dengan path file CSV Anda
    df = pd.read_csv(file_path)

    pivot_table = df.pivot_table(
        index="paslon", 
        columns="sentiment", 
        aggfunc="size", 
        fill_value=0
    )


    pivot_table.plot(
        kind="bar", 
        figsize=(10, 6), 
        stacked=False, 
        color={"positif": "green", "netral": "orange", "negatif": "red"}
    )


    plt.title("Distribusi Sentimen Berdasarkan Paslon")
    plt.xlabel("Paslon")
    plt.ylabel("Jumlah Komentar")
    plt.legend(title="Sentimen")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.xticks(rotation=45)
    plt.show()


