import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Define the stock symbol and date range
stock_symbol = 'AAPL'
start_date = '2020-01-01'
end_date = '2021-12-31'

# Fetch historical stock price data using yfinance
data = yf.download(stock_symbol, start=start_date, end=end_date)

# Select the 'Adj Close' column as the stock price
df = data[['Adj Close']].reset_index()

# Feature engineering
for i in range(1, 6):
    df[f'Lag_{i}'] = df['Adj Close'].shift(i)

# Drop rows with missing values (NaN) introduced by lagging
df = df.dropna()

# Split the data into training and testing sets
X = df.drop(['Date', 'Adj Close'], axis=1)
y = df['Adj Close']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train a linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
from sklearn.metrics import mean_squared_error, r2_score
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error: {mse}')
print(f'R-squared (R2) Score: {r2}')

# Visualize the predicted vs. actual prices
plt.figure(figsize=(12, 6))
plt.plot(df['Date'][-len(y_test):], y_test.values, label='Actual Price', color='blue')
plt.plot(df['Date'][-len(y_test):], y_pred, label='Predicted Price', color='red')
plt.xlabel('Date')
plt.ylabel('Stock Price')
plt.title(f'Stock Price Prediction for {stock_symbol}')
plt.legend()
plt.show()
