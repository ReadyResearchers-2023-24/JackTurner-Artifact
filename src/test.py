from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download the VADER lexicon for sentiment analysis
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def scrape_finviz_sentiment(ticker, num_articles=5):
    finwiz_url = f"https://finviz.com/quote.ashx?t={ticker}"

    req = Request(
        url=finwiz_url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0"
        },
    )
    response = urlopen(req)
    html = BeautifulSoup(response, 'html.parser')

    news_table = html.find(id="news-table")
    if not news_table:
        print("News table not found. Exiting.")
        return None

    parsed_news = []

    # Initialize VADER sentiment analyzer
    sid = SentimentIntensityAnalyzer()

    for row in news_table.findAll("tr")[:num_articles]:
        date_time = row.td.text.strip()
        # Convert "Today" to the current date
        if "Today" in date_time:
            date_time = datetime.now().strftime("%Y-%m-%d") + date_time[5:]

        # Check if date and time are present
        if len(date_time.split()) == 2:
            date, time = date_time.split()
        else:
            date, time = None, None

        headline = row.find("a", class_="tab-link-news").text.strip()

        # Perform sentiment analysis using VADER
        sentiment_scores = sid.polarity_scores(headline)
        compound_score = sentiment_scores['compound']

        parsed_news.append({"ticker": ticker, "date": date, "time": time, "headline": headline, "compound_score": compound_score})

    return pd.DataFrame(parsed_news)

# Example usage:
ticker = "AAPL"
num_articles = 5
df = scrape_finviz_sentiment(ticker, num_articles)

# Save the results to a CSV file
csv_file_path = f"{ticker}_sentiment_analysis.csv"
df.to_csv(csv_file_path, index=False)

print(f"Sentiment analysis results saved to {csv_file_path}")
