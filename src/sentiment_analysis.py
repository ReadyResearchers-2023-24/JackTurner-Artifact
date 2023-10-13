import pandas as pd
import matplotlib.pyplot as plt
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

# Initialize NLTK
nltk.download('vader_lexicon')

# Define functions
def get_financial_news(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urlopen(req)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    headlines = soup.find_all('h2', class_='financial-news-headline')
    return [headline.text for headline in headlines]

def analyze_sentiment(headline):
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(headline)
    return sentiment

def main():
    # Read the CSV file with the format "headline, url, publisher, date, stock"
    df = pd.read_csv('src/300_stock_headlines.csv')  # Replace with the actual file path of your CSV.

    # Apply sentiment analysis to headlines
    df['sentiment'] = df['headline'].apply(analyze_sentiment)

    # Display results
    for index, row in df.iterrows():
        print(f"Headline: {row['headline']}")
        print(f"Sentiment Scores: {row['sentiment']}")
        print()

    # Save results to a new CSV file
    df.to_csv('sentiment_analysis_results.csv', index=False)

if __name__ == "__main__":
    main()
