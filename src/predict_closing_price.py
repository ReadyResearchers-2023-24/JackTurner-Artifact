import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from datetime import datetime


# Function to load data from the combined CSV file
def load_data(combined_data_path):
    df_combined = pd.read_csv(combined_data_path)
    return df_combined


# Function to split data into training and testing sets
def split_data(df_combined):
    features = df_combined[["Average Sentiment", "Volume"]]
    target = df_combined["Close"]
    X_train, X_test, y_train, y_test = train_test_split(
        features, target, test_size=0.2, random_state=42
    )
    return X_train, X_test, y_train, y_test


# Function to train a linear regression model
def train_model(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model


# Function to evaluate the model's performance
def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    return mse


# Function to predict the next day's closing price
def predict_next_day_closing_price(model, next_day_features):
    predicted_closing_price = model.predict([next_day_features])
    return predicted_closing_price


# Main function to orchestrate the process
def main():
    # Get the current directory of the script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

    # Path to your combined CSV file
    combined_data_path = os.path.join(parent_dir, "data", "combined_data.csv")

    # Load the data
    df_combined = load_data(combined_data_path)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = split_data(df_combined)

    # Train the linear regression model
    model = train_model(X_train, y_train)

    # Evaluate the model's performance
    mse = evaluate_model(model, X_test, y_test)
    print(f"Mean Squared Error: {mse}")

    # Example: Features for the next day
    next_day_features = [
        0.2,
        10000,
    ]  # Example values for 'Average Sentiment' and 'Volume'

    # Predict the next day's closing price
    next_day_closing_price = predict_next_day_closing_price(model, next_day_features)
    print("Predicted Closing Price for the Next Day:", next_day_closing_price)

    # Get the current date
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Save MSE, predicted closing price, and date to a CSV file
    data = {
        "Date": [current_date, current_date],
        "Metric": ["Mean Squared Error", "Predicted Closing Price for the Next Day"],
        "Value": [
            mse,
            next_day_closing_price[0],
        ],  # Convert the closing price to a scalar value
    }
    df_results = pd.DataFrame(data)
    prediction_csv_path = os.path.join(
        current_dir, "../data/linear_regression_prediction.csv"
    )
    df_results.to_csv(prediction_csv_path, index=False)
    print(f"Prediction results saved to '{prediction_csv_path}'.")


if __name__ == "__main__":
    main()
