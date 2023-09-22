"""
Financial News Sentiment Analysis

This program uses web scraping to retrieve financial news articles for a list of tickers, and performs sentiment analysis
on the headlines using the VADER algorithm. The sentiment scores are displayed for each article and an overall sentiment score is calculated for each ticker. The results are displayed in a
GUI using the tkinter library.

Dependencies:
    - pandas
    - matplotlib
    - nltk
    - beautifulsoup4
    - tkinter

Usage:
    1. Run the script.
    2. Enter one or more tickers separated by commas in the input field.
    3. Click the "Analyze" button to retrieve and analyze financial news articles for the tickers.
    4. View the sentiment scores and headlines for each article in the GUI.
"""
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('Financial News Sentiment Analysis')
        self.create_widgets()

    def create_widgets(self):
        # create ticker label and entry field
        ticker_label = Label(self.master, text='Ticker(s):')
        ticker_label.grid(row=0, column=0, sticky=W)
        self.ticker_entry = Entry(self.master, width=25)
        self.ticker_entry.grid(row=0, column=1, columnspan=2, sticky=W+E)

        # create button to start analysis
        self.analyze_button = Button(self.master, text='Analyze', command=self.analyze_sentiment)
        self.analyze_button.grid(row=1, column=1, sticky=W)

        # create label for results
        results_label = Label(self.master, text='Results:')
        results_label.grid(row=2, column=0, sticky=W)

        # create scrolled text widget to display results
        self.results_text = ScrolledText(self.master, width=50, height=10)
        self.results_text.grid(row=3, column=0, columnspan=12, padx=15, pady=15, sticky="NSEW")

        # configure grid weights to fit all the articles on one page
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(3, weight=1)

        self.results_text.grid_propagate(False)


    def get_html_content(self, url):
        # get HTML content from url
        req = Request(url=url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'})
        response = urlopen(req)
        return response.read()

    def get_news_tables(self, tickers):
        # get news table for each ticker
        site_url = 'https://finviz.com/quote.ashx?t='
        news_tables = {}
        for ticker in tickers:
            url = site_url + ticker
            html = BeautifulSoup(self.get_html_content(url), features="html.parser")
            news_table = html.find(id='news-table')
            news_tables[ticker] = news_table
        return news_tables

    def parse_news(self, news_tables):
        parsed_news = []
        for file_name, news_table in news_tables.items():
            for x in news_table.findAll('tr'):
                text = x.get_text()
                date_scrape = x.td.text.split()
                if len(date_scrape) == 1:
                    time = date_scrape[0]
                else:
                    date = date_scrape[0]
                    time = date_scrape[1]
                ticker = file_name.split('_')[0]
                parsed_news.append([ticker, date, time, text])
        return parsed_news

    def analyze_sentiment(self):
        # download NLTK data
        nltk.download('vader_lexicon')

        # get tickers from entry field
        tickers = self.ticker_entry.get().split(',')

        # get news tables
        news_tables = self.get_news_tables(tickers)

        # parse news
        parsed_news = self.parse_news(news_tables)

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
        self.results_text.delete(1.0, END)
        for index, row in parsed_and_scored_news.iterrows():
            ticker = row['ticker']
            sentiment_score = row['compound']
            headline = row['headline']

            # create a new ScrolledText widget for each news article and display its score
            news_text = ScrolledText(self.master, width=100, height=5)
            news_text.grid(row=index+3, column=0, columnspan=3, padx=10, pady=10)
            news_text.insert(END, headline)
            news_text.insert(END, f"\nNegative Score: {row['neg']:.2f}")
            news_text.insert(END, f"\nNeutral Score: {row['neu']:.2f}")
            news_text.insert(END, f"\nPositive Score: {row['pos']:.2f}")
            news_text.insert(END, f"\nCompound Score: {sentiment_score:.2f}")

            # update sentiment score for the ticker
            sentiment_dict[ticker] += sentiment_score

        # display overall sentiment score for each ticker
        for ticker, sentiment_score in sentiment_dict.items():
            self.results_text.insert(END, f"\n{ticker}: {sentiment_score:.2f}")

if __name__ == '__main__':
    root = Tk()
    app = Application(master=root)
    app.mainloop()