# Stock Price Prediction with Sentiment Analysis

## Overview
This project aims to predict stock prices using sentiment analysis data combined with historical stock prices. By leveraging machine learning techniques, specifically linear regression, we analyze the relationship between sentiment scores and stock prices to forecast future price movements.

## Features
- **Data Sources:** Utilizes historical stock price data and sentiment analysis scores
- **Machine Learning Model:** Implements linear regression to predict stock prices
- **Prediction Outputs:** Provides Mean Squared Error (MSE) and predicted closing price for the next day
- **Integration with OpenAI GPT-3:** Utilizes OpenAI's GPT-3 for generating predictions based on provided data

## Requirements
- Python 3.x
- pandas
- scikit-learn
- yfinance
- textblob
- requests

## Usage
1. Clone the repository: `git clone https://github.com/your_username/stock-price-prediction.git`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Navigate to the `src` folder `cd src`
4. Execute the `run_all_scripts.py` file: `python3 run_all_scripts.py`
5. Results will be displayed in the command line and stored in the `data` folder under the name: `gpt_prediction.csv`


