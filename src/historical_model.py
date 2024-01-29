# stock_prediction_module.py

import pandas as pd
import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

def fetch_stock_data(stock_symbol, start_date, end_date):
    """
    Fetches historical stock price data.
    """
    data = yf.download(stock_symbol, start=start_date, end=end_date)
    return data[["Adj Close"]].reset_index()

def feature_engineering(df):
    """
    Adds lag features to the dataframe.
    """
    for i in range(1, 6):
        df[f"Lag_{i}"] = df["Adj Close"].shift(i)
    df = df.dropna()
    return df

def split_data(df):
    """
    Splits the data into features and targets and into training and testing sets.
    """
    X = df.drop(["Date", "Adj Close"], axis=1)
    y = df["Adj Close"]
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_model(X_train, y_train):
    """
    Trains a linear regression model.
    """
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

def predict(model, X_test):
    """
    Makes predictions using the trained model.
    """
    return model.predict(X_test)

def evaluate(y_test, y_pred):
    """
    Evaluates the model performance and prints the results.
    """
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"Mean Squared Error: {mse}")
    print(f"R-squared (R2) Score: {r2}")
    return mse, r2

def save_predictions_to_csv(dates, y_test, y_pred, stock_symbol):
    """
    Saves the predicted vs. actual prices to a CSV file.
    """
    results_df = pd.DataFrame({
        'Date': dates,
        'Actual Price': y_test,
        'Predicted Price': y_pred
    })
    filename = f"{stock_symbol}_predictions.csv"
    results_df.to_csv(filename, index=False)
    print(f"Predictions saved to {filename}")

if __name__ == "__main__":
    stock_symbol = "AAPL"
    start_date = "2020-01-01"
    end_date = "2021-12-31"

    df = fetch_stock_data(stock_symbol, start_date, end_date)
    df = feature_engineering(df)
    X_train, X_test, y_train, y_test = split_data(df)
    model = train_model(X_train, y_train)
    y_pred = predict(model, X_test)
    mse, r2 = evaluate(y_test, y_pred)

    # Save predictions to CSV instead of plotting
    save_predictions_to_csv(df["Date"][-len(y_test):], y_test.values, y_pred, stock_symbol)
