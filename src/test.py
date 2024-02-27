import sqlite3
import os
from newsapi import NewsApiClient
import datetime
from textblob import TextBlob

# Initialize NewsApiClient with your API key
api = NewsApiClient(api_key='22f6dfa7bb114867a3bcb7c56b6c6410')

# Ticker symbols you want to search for
ticker_symbols = ['apple', 'google', 'amazon','microsoft','tesla']

# Calculate the date range for the past month
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=30)

# Format dates as strings
end_date_str = end_date.strftime('%Y-%m-%d')
start_date_str = start_date.strftime('%Y-%m-%d')

# Path to the database file
database_path = os.path.join('data', 'stock_news.db')

# Connect to the SQLite database
conn = sqlite3.connect(database_path)
c = conn.cursor()

# Check if the 'articles' table exists
c.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='articles' ''')
if c.fetchone()[0] == 0:
    # If the 'articles' table does not exist, create it
    c.execute('''CREATE TABLE articles
                 (symbol TEXT, title TEXT, date TEXT, sentiment_score REAL)''')
    conn.commit()

# Iterate over ticker symbols
for symbol in ticker_symbols:
    # Make a request to get everything related to a specific ticker symbol for the past month
    response = api.get_everything(q=symbol, from_param=start_date_str, to=end_date_str)
    
    # Check if the response is successful
    if response['status'] == 'ok':
        # Extract articles from the response
        articles = response['articles']
        
        # Iterate over the articles and store relevant information
        for article in articles:
            # Extract only date part from publishedAt
            published_date = article['publishedAt'].split('T')[0]
            
            # Perform sentiment analysis on the article title
            title = article['title']
            sentiment_score = TextBlob(title).sentiment.polarity
            
            # Insert the data into the 'articles' table
            c.execute("INSERT INTO articles VALUES (?, ?, ?, ?)", (symbol, title, published_date, sentiment_score))
            
    else:
        print(f"Failed to retrieve data for {symbol}. Status:", response['status'])

# Commit changes and close the database connection
conn.commit()
conn.close()

print("Data saved successfully to", database_path)
