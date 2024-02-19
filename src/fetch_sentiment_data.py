import requests
from textblob import TextBlob
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Function to fetch news headlines for a specific date range
def fetch_news(start_date, end_date):
    all_headlines = []
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "Apple",
        "from": start_date,
        "to": end_date,
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": 100,  # Max articles per request, adjust as needed
        "apiKey": os.getenv("SENTIMENT_KEY"),  # Use environment variable
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        for article in articles:
            all_headlines.append(article["title"])
    else:
        print(f"Failed to fetch news from {start_date} to {end_date}")
    return all_headlines

# Function to calculate average sentiment score for headlines
def average_sentiment(headlines):
    sentiment_scores = []
    for headline in headlines:
        if headline:  # Check if headline is not None or empty
            sentiment_scores.append(TextBlob(headline).sentiment.polarity)
    return sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0

# Main function to fetch, process news headlines, calculate sentiment, and save to CSV
def main():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    headlines = fetch_news(start_date_str, end_date_str)
    if headlines:  # Proceed if there are headlines for the period
        avg_sentiment = average_sentiment(headlines)
        print(f"Average sentiment from {start_date_str} to {end_date_str}: {avg_sentiment}")

        # Prepare data to save
        data_to_save = {
            "Start Date": [start_date_str],
            "End Date": [end_date_str],
            "Average Sentiment": [avg_sentiment]
        }
        df = pd.DataFrame(data_to_save)

        # Get the current directory of the script
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Define the path to the data folder, which is a level up from the script's directory
        data_folder = os.path.join(current_dir, "..", "data")

        # Define the full path for the CSV file within the data folder
        csv_file_path = os.path.join(data_folder, "average_sentiment_daily.csv")

        # Save the DataFrame to a CSV file
        df.to_csv(csv_file_path, index=False)

        # Print out the location of the saved CSV file
        print(f"Saved sentiment scores to '{csv_file_path}'")

if __name__ == "__main__":
    main()

