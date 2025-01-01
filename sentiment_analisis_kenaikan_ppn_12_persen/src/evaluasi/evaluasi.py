

# 1. Memuat dataset dari file CSV
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from transformers import pipeline

def evaluasi_model():
    # 1. Load dataset from CSV file
    df = pd.read_csv('data/outputs/dataset_with_sentiments.csv')

    # 2. Check the data
    print("Data loaded:")
    print(df.head())

    # 3. Split the data into training and testing sets
    X = df['comment']
    y = df['sentiment']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 4. Load the sentiment analysis model
    sentiment_model = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

    # 5. Predict sentiments on the test data
    predictions = sentiment_model(X_test.tolist())

    # 6. Convert prediction results into meaningful labels
    predicted_labels = []
    for prediction in predictions:
        label = prediction['label']
        if label in ["4 stars", "5 stars"]:
            predicted_labels.append("positif")  # Positive sentiment
        elif label in ["3 stars"]:
            predicted_labels.append("netral")    # Neutral sentiment
        elif label in ["1 star", "2 stars"]:
            predicted_labels.append("negatif")    # Negative sentiment
        else:
            predicted_labels.append("unknown")     # Handle unexpected labels

    # 7. Evaluate results
    conf_matrix = confusion_matrix(y_test, predicted_labels)
    class_report = classification_report(y_test, predicted_labels, output_dict=True)

    # 8. Visualize Confusion Matrix
    plt.figure(figsize=(10, 7))
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=['negatif', 'netral', 'positif'], yticklabels=['negatif', 'netral', 'positif'])
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.show()

    # 9. Visualize Classification Report
    report_df = pd.DataFrame(class_report).transpose()
    report_df = report_df.iloc[:-1, :-1]  # Remove 'accuracy' row and 'support' column

    plt.figure(figsize=(10, 6))
    sns.heatmap(report_df[['precision', 'recall', 'f1-score']], annot=True, cmap='Blues', vmin=0, vmax=1)
    plt.title('Classification Report')
    plt.xlabel('Metrics')
    plt.ylabel('Classes')
    plt.show()
