<<<<<<< HEAD
import http.client
import urllib.parse
import json
import pandas as pd 


def fetch_data(symbols, limit=50):
    conn = http.client.HTTPSConnection('api.marketaux.com')
    params = urllib.parse.urlencode({
        'api_token': 'YrnxgrKvZsSxEYVJDLsN0Ly2EdRBh0ZbDIcJOxud',
        'symbols': symbols,
        'limit': limit,
        'language': 'en'
    })

    conn.request('GET', '/v1/news/all?{}'.format(params))
    res = conn.getresponse()
    data = res.read()
    data_dict = json.loads(data.decode('utf-8'))

    extracted_data = []
    for item in data_dict['data']:
        for entity in item.get('entities', []):
            symbol = entity.get('symbol', 'N/A')
            if symbol.lower() == symbols.lower():
                for highlight in entity.get('highlights', []):
                    extracted_data.append({
                        'symbol': symbol,
                        'highlight': highlight['highlight'],
                        'sentiment': highlight['sentiment']
                    })

    conn.close()
    return extracted_data

def save_predictions_to_csv(dates, y_test, y_pred, stock_symbol):
    """
    Saves the predicted vs. actual prices to a CSV file.
    """
    results_df = pd.DataFrame({
        'Date': pd.to_datetime(dates),  # Ensure dates are in datetime format
        'Actual Price': y_test,
        'Predicted Price': y_pred
    })

    # Sort the DataFrame by the 'Date' column
    results_df = results_df.sort_values(by='Date')

    filename = f"{stock_symbol}_predictions.csv"
    results_df.to_csv(filename, index=False)
    print(f"Predictions saved to {filename}")


def main():
    ticker_symbol = input("Enter the ticker symbol: ")
    highlights = fetch_data(ticker_symbol, limit=10)

    # Convert list of dictionaries to pandas DataFrame
    highlights_df = pd.DataFrame(highlights)

    # Save the DataFrame to a CSV file
    csv_filename = f"{ticker_symbol}_highlights.csv"
    highlights_df.to_csv(csv_filename, index=False)
    print(f"Highlights saved to {csv_filename}")
    
if __name__ == '__main__':
=======
import pandas as pd
import matplotlib.pyplot as plt
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

# Initialize NLTK
nltk.download("vader_lexicon")

# Define functions
def get_financial_news(url):
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    response = urlopen(req)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    headlines = soup.find_all("h2", class_="financial-news-headline")
    return [headline.text for headline in headlines]


def analyze_sentiment(headline):
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(headline)
    return sentiment


def main():
    # Read the CSV file with the format "headline, url, publisher, date, stock"
    df = pd.read_csv("src/300_stock_headlines.csv")

    # Apply sentiment analysis to headlines
    df["sentiment"] = df["headline"].apply(analyze_sentiment)

    # Display results
    for index, row in df.iterrows():
        print(f"Headline: {row['headline']}")
        print(f"Sentiment Scores: {row['sentiment']}")
        print()

    # Save results to a new CSV file
    df.to_csv("sentiment_analysis_results.csv", index=False)


if __name__ == "__main__":
>>>>>>> 4a37affb967117f3f46c7f52009422745bb33eeb
    main()
