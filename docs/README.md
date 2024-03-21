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
- csv
- newsapi
- dotenv

## Usage
1. Clone the repository: `git clone https://github.com/ReadyResearchers-2023-24/JackTurner-Artifact`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Run the provided Python script: `python3 run_all.py`
4. Results will be displayed in the command line and stored in the `data` folder under the name: `gpt_prediction.csv`

## Additional Notes
- Modify the prompt in `gpt.py` to determine the desired output format.
- Sometimes, the data size may exceed the capacity of the ChatGPT API. In such cases, consider removing one or two CSV files from the `data` folder to allow processing a smaller batch at a time, ensuring more consistent results.
