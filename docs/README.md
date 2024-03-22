# Stock Price Prediction with Sentiment Analysis

## Overview
This project forecasts stock prices for five major companies—Apple, Amazon, Tesla, Google, and Microsoft—by integrating sentiment analysis data with historical stock prices. Employing machine learning techniques, this project examines the correlation between sentiment scores and stock prices to predict future price movements. The combined dataset for these selected ticker symbols is processed through ChatGPT, which then outputs a CSV file with predictions on future stock price movements.

## Motivation
The dynamic nature of financial markets and the significant impact of investor sentiment on stock prices necessitate a multifaceted approach to prediction. By leveraging both quantitative historical data and qualitative sentiment analysis, this project aims to provide a more comprehensive tool for predicting stock market movements, enhancing decision-making processes for investors.

## Associated Thesis
The related thesis, detailing the research, methodology, and findings of this project, is published within this repository [Repo](https://github.com/ReadyResearchers-2023-24/cis-600-f2023-610-s2024-senior-thesis-jackturner83)

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
