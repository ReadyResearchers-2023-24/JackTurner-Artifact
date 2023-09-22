# Stock Price Prediction and Financial News Sentiment Analysis

This project combines two distinct functionalities: stock price prediction using historical data and sentiment analysis of financial news headlines. Below, you'll find a brief overview of each component along with how to use them.

## Stock Price Prediction

### Overview

The stock price prediction component employs a linear regression model to forecast the future price of a given stock based on its historical price data. This tool utilizes the Yahoo Finance API to fetch historical stock price data, engineers lagged features, trains a linear regression model, and evaluates its performance.

### Dependencies

- pandas
- numpy
- yfinance
- scikit-learn
- matplotlib

### Usage

1. Modify the `stock_symbol`, `start_date`, and `end_date` variables at the beginning of the script to select the stock symbol and date range for analysis.

2. Run the script.

3. The script will fetch historical stock price data, engineer lagged features, split the data into training and testing sets, create and train a linear regression model, and make predictions.

4. The script will display evaluation metrics including Mean Squared Error (MSE) and R-squared (R2) Score.

5. A plot comparing actual and predicted stock prices will be displayed.

## Financial News Sentiment Analysis

### Overview

The financial news sentiment analysis component retrieves financial news articles for a list of tickers, performs sentiment analysis on the headlines using the VADER algorithm, and displays the sentiment scores and headlines in a graphical user interface (GUI) built with the tkinter library.

### Dependencies

- pandas
- matplotlib
- nltk
- beautifulsoup4
- tkinter

### Usage
