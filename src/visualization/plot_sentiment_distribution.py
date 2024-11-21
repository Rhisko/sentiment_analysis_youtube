import json
import matplotlib.pyplot as plt
from collections import Counter

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
    
    data = load_data(file_path)
    
    # Get sentiment counts
    sentiment_counts = get_sentiment_counts(data)
    
    # Plot both Bar Chart and Pie Chart
    plot_bar_chart(sentiment_counts)
    plot_pie_chart(sentiment_counts)

