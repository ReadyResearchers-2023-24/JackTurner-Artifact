import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from datetime import datetime

def load_data(combined_data_path):
    """Load data from a CSV file."""
    df_combined = pd.read_csv(combined_data_path)
    return df_combined

def train_model(X_train, y_train):
    """Train a linear regression model."""
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    """Evaluate the model's performance using MSE."""
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    return mse

def predict_next_day_closing_price(model, next_day_features):
    """Predict the next day's closing price."""
    predicted_closing_price = model.predict([next_day_features])
    return predicted_closing_price

def save_results(current_dir, mse, next_day_closing_price, coefficients, intercept):
    """Save MSE, predicted closing price, coefficients, and intercept to a CSV file."""
    current_date = datetime.now().strftime("%Y-%m-%d")
    data = {
        "Date": [current_date] * 3,
        "Metric": ["Mean Squared Error", "Predicted Closing Price for the Next Day", "Coefficients", "Intercept"],
        "Value": [
            mse,
            next_day_closing_price[0],
            str(coefficients.tolist()),  # Coefficients as string list
            intercept  # Directly use intercept as it's a single value
        ]
    }
    df_results = pd.DataFrame(data)
    prediction_csv_path = os.path.join(current_dir, "linear_regression_prediction.csv")
    df_results.to_csv(prediction_csv_path, index=False)
    print(f"Prediction results saved to '{prediction_csv_path}'.")

def main():
    """Orchestrate the process from data loading to result saving."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    combined_data_path = os.path.join(current_dir, "data", "combined_data.csv")

    df_combined = load_data(combined_data_path)

    X = df_combined[['Average Sentiment', 'Volume']]
    y = df_combined['Close']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = train_model(X_train, y_train)

    coefficients = model.coef_
    intercept = model.intercept_
    print("Coefficients:", coefficients)
    print("Intercept:", intercept)

    mse = evaluate_model(model, X_test, y_test)
    print(f"Mean Squared Error: {mse}")

    next_day_features = [0.2, 10000]
    next_day_closing_price = predict_next_day_closing_price(model, next_day_features)
    print("Predicted Closing Price for the Next Day:", next_day_closing_price)

    save_results(current_dir, mse, next_day_closing_price, coefficients, intercept)

if __name__ == "__main__":
    main()
