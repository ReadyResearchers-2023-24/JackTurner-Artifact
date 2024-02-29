import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
import sqlite3

# Function to fetch the last 30 days of stock prices for a given ticker
def fetch_stock_prices(ticker):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    # Fetch data
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    
    # Add a new column 'symbol' containing the ticker symbol
    stock_data['symbol'] = ticker

    return stock_data


# Main function to fetch stock prices and save to SQLite database
def main(tickers):
    # Get the current directory of the script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the path to the existing data folder relative to the script's directory
    data_folder = os.path.join(current_dir, "..", "data")

    # Define the path for saving the SQLite database file within the existing data folder
    database_path = os.path.join(data_folder, "stock_prices.db")

    # Connect to the SQLite database
    conn = sqlite3.connect(database_path)

    # Iterate over ticker symbols
    for ticker in tickers:
        # Delete existing data for the ticker
        conn.execute(f"DELETE FROM stock_prices WHERE symbol = '{ticker}'")

        # Fetch stock prices
        stock_prices = fetch_stock_prices(ticker)

        # Save to SQLite database
        stock_prices.to_sql('stock_prices', conn, if_exists='append', index=True)

        print(f"Saved stock prices for {ticker} to '{database_path}'.")

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    # Ticker symbols you want to fetch historical prices for
    ticker_symbols = ['AAPL', 'GOOGL', 'AMZN', 'MSFT', 'TSLA']
    main(ticker_symbols)
