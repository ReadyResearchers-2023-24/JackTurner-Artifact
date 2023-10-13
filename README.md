# Stock Price Prediction and Financial News Sentiment Analysis

## Introduction and Motivation
This project combines two distinct functionalities: stock price prediction using historical data and sentiment analysis of financial news headlines. The motivation behind this project is to provide a tool that empowers users to make data-driven decisions in the complex world of financial investments. By predicting stock prices and analyzing sentiment in financial news, I aim to offer valuable insights to investors and financial analysts.

## Technical Details
### Stock Price Prediction
The stock price prediction component employs a linear regression model to forecast the future price of a given stock based on its historical price data. This tool utilizes the Yahoo Finance API to fetch historical stock price data, engineers lagged features, trains a linear regression model, and evaluates its performance.

#### Usage
1. Modify the `stock_symbol`, `start_date`, and `end_date` variables at the beginning of the script to select the stock symbol and date range for analysis.
2. Run the script.
3. The script will fetch historical stock price data, engineer lagged features, split the data into training and testing sets, create and train a linear regression model, and make predictions.
4. The script will display evaluation metrics including Mean Squared Error (MSE) and R-squared (R2) Score.
5. A plot comparing actual and predicted stock prices will be displayed.

### Financial News Sentiment Analysis
The financial news sentiment analysis component retrieves financial news articles for a list of tickers, performs sentiment analysis on the headlines using the VADER algorithm, and displays the sentiment scores and headlines in a graphical user interface (GUI) built with the tkinter library.

## Future Plans
As I continue to develop this project, I have several key areas of focus:

1. **Enhanced Data Integration**: I plan to integrate more data sources and improve the quality and granularity of data to enhance our predictive models.

2. **Modeling Improvements**: I aim to explore advanced machine learning models and algorithms to improve the accuracy and reliability of our stock price predictions.

## Related Work
To provide a broader context for our project, I am inspired by and acknowledge related work in the following areas:

- **Sentiment analysis algorithms and applications: A survey**: The main contributions of this paper include the sophisticated categorizations of a large number of recent articles and the illustration of the recent trend of research in the sentiment analysis and its related areas.
- **Prediction of stock performance by using logistic regression model**: Projects and studies that focus on predicting stock prices using historical data and machine learning techniques.
