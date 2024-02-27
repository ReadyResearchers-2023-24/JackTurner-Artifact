import csv
import sqlite3
from newsapi import NewsApiClient
import datetime

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

# Initialize lists to store data for CSV and database
csv_data = []
db_data = []

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
            
            # Create a dictionary with title and date
            article_data = {
                'title': article['title'],
                'date': published_date
            }
            
            # Append data to lists for CSV and database
            csv_data.append([symbol, article_data['title'], article_data['date']])
            db_data.append((symbol, article_data['title'], article_data['date']))
    else:
        print(f"Failed to retrieve data for {symbol}. Status:", response['status'])

# Save data to CSV
with open('stock_news.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Symbol', 'Title', 'Date'])
    writer.writerows(csv_data)

print("Data saved successfully to stock_news.csv")

# Save data to SQLite database
conn = sqlite3.connect('stock_news.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS articles
             (symbol text, title text, date text)''')
c.executemany('INSERT INTO articles VALUES (?, ?, ?)', db_data)
conn.commit()
conn.close()

print("Data saved successfully to stock_news.db")
