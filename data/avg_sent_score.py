import sqlite3
import pandas as pd

# Connect to the SQLite database
conn_prices = sqlite3.connect('data/stock_prices.db')

# Read daily average sentiment scores from CSV
sentiment_data = pd.read_csv('data/daily_average_sentiment_scores.csv')

# Query to fetch stock prices data from the database
query = """
    SELECT "Date", "Open", "High", "Low", "Volume", "symbol"
    FROM stock_prices
"""

# Fetch stock prices data into a DataFrame
stock_prices_data = pd.read_sql_query(query, conn_prices)

# Close the database connection
conn_prices.close()

# Merge sentiment data with stock prices data based on symbol and date
combined_data = pd.merge(stock_prices_data, sentiment_data, how='inner', left_on=['symbol', 'Date'], right_on=['symbol', 'date'])

# Drop the duplicate date column
combined_data.drop(columns=['date'], inplace=True)

# Save the combined data to a CSV file
combined_data.to_csv('combined_data.csv', index=False)

print("Combined data saved to combined_data.csv")
