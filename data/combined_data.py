import pandas as pd
import sqlite3
from datetime import datetime

# Connect to the SQLite database
conn_prices = sqlite3.connect('data/stock_prices.db')

# Read daily average sentiment scores from CSV
sentiment_data = pd.read_csv('data/daily_average_sentiment_scores.csv')

# Convert symbol to uppercase in sentiment data
sentiment_data['symbol'] = sentiment_data['symbol'].str.upper()

# Mapping dictionary to map symbols in sentiment data to match the symbols in stock prices data
symbol_mapping = {
    'AMAZON': 'AMZN',
    'APPLE': 'AAPL',
    'GOOGLE': 'GOOGL',
    'MICROSOFT': 'MSFT',
    'TESLA': 'TSLA'
}

# Map symbols in sentiment data using the mapping dictionary
sentiment_data['symbol'] = sentiment_data['symbol'].map(symbol_mapping)

# Query to fetch stock prices data from the database
query = """
    SELECT "symbol", "Date", "Open", "High", "Low"
    FROM stock_prices
"""

# Fetch stock prices data into a DataFrame
stock_prices_data = pd.read_sql_query(query, conn_prices)

# Close the database connection
conn_prices.close()

# Convert 'Date' columns to consistent format
sentiment_data['date'] = pd.to_datetime(sentiment_data['date'])
stock_prices_data['Date'] = pd.to_datetime(stock_prices_data['Date'])

# Print unique symbols in both datasets
print("Unique symbols in stock prices data:", stock_prices_data['symbol'].unique())
print("Unique symbols in sentiment data:", sentiment_data['symbol'].unique())

# Print data types of the 'Date' columns in both datasets
print("Data type of 'Date' column in stock prices data:", stock_prices_data['Date'].dtype)
print("Data type of 'date' column in sentiment data:", sentiment_data['date'].dtype)

# Merge sentiment data with stock prices data based on uppercase symbol and date
combined_data = pd.merge(stock_prices_data, sentiment_data, how='inner', left_on=['symbol', 'Date'], right_on=['symbol', 'date'])

# Drop the duplicate date column
combined_data.drop(columns=['date'], inplace=True)

# Save the combined data to a CSV file
combined_data.to_csv('data/combineddata.csv', index=False)

print("\nCombined data saved to combineddata.csv")
