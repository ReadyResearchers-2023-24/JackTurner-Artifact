import requests
from textblob import TextBlob
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Function to fetch news headlines for a specific date
def fetch_news(date):
    all_headlines = []
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "Apple",
        "from": date,
        "to": date,
        "sortBy": "publishedAt",
        "language": "en",
        "apiKey": os.getenv("SENTIMENT_KEY"),  # Use environment variable
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        for article in articles:
            all_headlines.append(article["title"])
    else:
        print(f"Failed to fetch news for {date}")
    return all_headlines

# Function to calculate average sentiment score for headlines
def average_sentiment(headlines):
    sentiment_scores = [TextBlob(headline).sentiment.polarity for headline in headlines]
    return sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0

# Main function to fetch, process news headlines, and save to CSV
def main():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    dates = [
        start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)
    ]
    average_sentiments = []

    for date in dates:
        date_str = date.strftime("%Y-%m-%d")
        headlines = fetch_news(date_str)
        if headlines:  # Proceed if there are headlines for the day
            avg_sentiment = average_sentiment(headlines)
            average_sentiments.append(
                {"Date": date_str, "Average Sentiment": avg_sentiment}
            )
        else:
            average_sentiments.append({"Date": date_str, "Average Sentiment": 0})

    df = pd.DataFrame(average_sentiments)

    # Get the current directory of the script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the path to the data folder one level up from the script's directory
    data_folder = os.path.join(current_dir, "..", "data")

    # Ensure the data folder exists, if not create it
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    # Define the path for saving the CSV file within the data folder
    csv_file_path = os.path.join(data_folder, "average_sentiment_daily.csv")

    # Save to CSV
    df.to_csv(csv_file_path, index=False)
    print(f"Saved daily average sentiment to '{csv_file_path}'.")


if __name__ == "__main__":
    main()