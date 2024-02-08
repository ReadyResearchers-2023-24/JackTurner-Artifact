# Combines data from sent.py and main.py

import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the path to the data folder relative to the script's directory
data_folder = os.path.join(current_dir, "..", "data")

# Ensure the data folder exists, if not create it
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

# Load your datasets using relative paths
sentiment_data = pd.read_csv(os.path.join(data_folder, "average_sentiment_daily.csv"))
stock_prices = pd.read_csv(os.path.join(data_folder, "stock_prices_last_30_days.csv"))

# Merge datasets on the 'Date' column
combined_data = pd.merge(sentiment_data, stock_prices, on="Date")

# Define the path for saving the combined data CSV file
csv_file_path = os.path.join(data_folder, "combined_data.csv")

# Save the combined data to a new CSV file
combined_data.to_csv(csv_file_path, index=False)
print("Combined data saved to 'data/combined_data.csv'.")

# Select your features and target variable
features = combined_data[["Average Sentiment", "Volume"]]  # Example features
target = combined_data["Close"]  # Example target

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    features, target, test_size=0.2, random_state=42
)

# Initialize and train a linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict and evaluate
predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)

print(f"Mean Squared Error: {mse}")
