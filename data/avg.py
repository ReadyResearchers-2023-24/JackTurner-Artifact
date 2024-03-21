import sqlite3
import csv
from collections import defaultdict

# Path to the database file
database_path = 'data/stock_news.db'

# Connect to the SQLite database
conn = sqlite3.connect(database_path)
c = conn.cursor()

# Retrieve all data from the database
c.execute("SELECT symbol, date, AVG(sentiment_score) AS avg_sentiment_score FROM articles GROUP BY symbol, date")
rows = c.fetchall()

# Write data to CSV file
with open('data/daily_average_sentiment_scores.csv', 'w', newline='') as csvfile:
    fieldnames = ['symbol', 'date', 'avg_sentiment_score']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    for row in rows:
        writer.writerow({'symbol': row[0], 'date': row[1], 'avg_sentiment_score': row[2]})

# Close the database connection
conn.close()

print("Data saved successfully to daily_average_sentiment_scores.csv")
