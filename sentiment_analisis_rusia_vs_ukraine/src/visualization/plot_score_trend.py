import json
import matplotlib.pyplot as plt

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

def extract_scores(data):
    """
    Extract sentiment scores from the data.
    
    Parameters:
    - data (list): List of dictionaries, each containing a 'score' field.
    
    Returns:
    - list: List of sentiment scores.
    """
    scores = [item['score'] for item in data if item['score'] is not None]
    return scores

def plot_line_chart(scores):
    """
    Plot the sentiment score trend as a line chart.
    
    Parameters:
    - scores (list): List of sentiment scores.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(scores, marker='o', linestyle='-', color='blue')
    plt.title('Sentiment Score Trend (Line Chart)')
    plt.xlabel('Comment Index')
    plt.ylabel('Sentiment Score')
    plt.show()

def plot_scatter_chart(scores):
    """
    Plot the sentiment score trend as a scatter plot.
    
    Parameters:
    - scores (list): List of sentiment scores.
    """
    plt.figure(figsize=(10, 6))
    plt.scatter(range(len(scores)), scores, color='red')
    plt.title('Sentiment Score Trend (Scatter Plot)')
    plt.xlabel('Comment Index')
    plt.ylabel('Sentiment Score')
    plt.show()

def plot_area_chart(scores):
    """
    Plot the sentiment score trend as an area chart.
    
    Parameters:
    - scores (list): List of sentiment scores.
    """
    plt.figure(figsize=(10, 6))
    plt.fill_between(range(len(scores)), scores, color="skyblue", alpha=0.4)
    plt.plot(scores, color="Slateblue", alpha=0.6, linewidth=2)
    plt.title('Sentiment Score Trend (Area Chart)')
    plt.xlabel('Comment Index')
    plt.ylabel('Sentiment Score')
    plt.show()


def create_grafik_score(file_path):
    data = load_data(file_path)
    
    # Extract scores
    scores = extract_scores(data)
    
    # Plot the score trend in different charts
    plot_line_chart(scores)
    plot_scatter_chart(scores)
    plot_area_chart(scores)
