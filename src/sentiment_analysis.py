"""
Financial News Sentiment Analysis

This program uses web scraping to retrieve financial news articles for a list of tickers and performs sentiment analysis
on the headlines using the VADER algorithm. The sentiment scores are displayed for each article, and an overall sentiment
score is calculated for each ticker.
"""

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def get_html_content(url):
    # get HTML content from url
    req = Request(url=url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'})
    response = urlopen(req)
    return response.read()

def get_news_tables(tickers):
    # get news table for each ticker
    site_url = 'https://finviz.com/quote.ashx?t='
    news_tables = {}
    for ticker in tickers:
        url = site_url + ticker
        html = BeautifulSoup(get_html_content(url), features="html.parser")
        news_table = html.find(id='news-table')
        news_tables[ticker] = news_table
    return news_tables

def parse_news(news_tables):
    parsed_news = []
    for ticker, news_table in news_tables.items():
        rows = news_table.findAll('tr')
        for row in rows[:5]:
            text = row.get_text()
            date_scrape = row.td.text.split()
            if len(date_scrape) == 1:
                time = date_scrape[0]
            else:
                date = date_scrape[0]
                time = date_scrape[1]
            parsed_news.append([ticker, date, time, text])
    return parsed_news

def analyze_sentiment(tickers):
    # download NLTK data
    nltk.download('vader_lexicon')

    # get news tables
    news_tables = get_news_tables(tickers)

    # parse news
    parsed_news = parse_news(news_tables)

    # analyze sentiment
    vader = SentimentIntensityAnalyzer()
    c = ['ticker', 'date', 'time ', 'headline']
    parsed_and_scored_news = pd.DataFrame(parsed_news, columns=c)
    scores = parsed_and_scored_news['headline'].apply(vader.polarity_scores).tolist()
    scores_df = pd.DataFrame(scores)
    parsed_and_scored_news = parsed_and_scored_news.join(scores_df, rsuffix='_right')
    parsed_and_scored_news['date'] = pd.to_datetime(parsed_and_scored_news.date).dt.date

    # create a sentiment dictionary to hold the sentiment score of each ticker
    sentiment_dict = {}
    for ticker in tickers:
        sentiment_dict[ticker] = 0

    # display results
    for index, row in parsed_and_scored_news.iterrows():
        ticker = row['ticker']
        sentiment_score = row['compound']
        headline = row['headline']

        # display sentiment score for each article
        print("Ticker:", ticker)
        print(headline)
        print(f"Negative Score: {row['neg']:.2f}")
        print(f"Neutral Score: {row['neu']:.2f}")
        print(f"Positive Score: {row['pos']:.2f}")
        print(f"Compound Score: {sentiment_score:.2f}")
        print()

        # update sentiment score for the ticker
        sentiment_dict[ticker] += sentiment_score

    # display overall sentiment score for each ticker
    for ticker, sentiment_score in sentiment_dict.items():
        print(f"Overall Sentiment for {ticker}: {sentiment_score:.2f}")

if __name__ == '__main__':
    # Input your tickers as a list, e.g., tickers = ['AAPL', 'GOOGL', 'TSLA']
    tickers = input("Enter one or more tickers separated by commas: ").split(',')
    analyze_sentiment(tickers)
