import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os


# Function to fetch the last 30 days of stock prices for a given ticker
def fetch_stock_prices(ticker):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    # Format dates as YYYY-MM-DD
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    # Fetch data
    stock_data = yf.download(ticker, start=start_date_str, end=end_date_str)

    return stock_data


# Main function to fetch stock prices and save to CSV
def main(ticker):
    # Fetch stock prices
    stock_prices = fetch_stock_prices(ticker)

    # Get the current directory of the script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the path to the existing data folder relative to the script's directory
    data_folder = os.path.join(current_dir, "..", "data")

    # Define the path for saving the CSV file within the existing data folder
    csv_file_path = os.path.join(data_folder, "stock_prices_last_30_days.csv")

    # Save to CSV
    stock_prices.to_csv(csv_file_path)

    print(f"Saved stock prices for {ticker} to '{csv_file_path}'.")


if __name__ == "__main__":
    ticker = "AAPL"
    main(ticker)
