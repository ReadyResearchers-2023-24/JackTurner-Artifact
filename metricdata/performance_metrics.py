# Import necessary libraries
import pandas as pd
import numpy as np
import os
from math import sqrt
from sklearn.metrics import r2_score, explained_variance_score as ev_score
import matplotlib.pyplot as plt

# Function to calculate performance metrics
def calculate_metrics(data):
    # Define column names for actual and predicted values
    actual_col = 'Actual'
    predicted_col = 'Prediction'

    # Extract actual and predicted values from the data
    actual = data[actual_col]
    predicted = data[predicted_col]

    # Calculate various performance metrics
    metrics = {}
    metrics['MAE'] = mean_absolute_error(actual, predicted)
    metrics['RMSE'] = root_mean_squared_error(actual, predicted)
    metrics['R_squared'] = r_squared(actual, predicted)
    metrics['Explained_Variance'] = ev_score(actual, predicted)
    metrics['Median_Absolute_Error'] = median_absolute_error(actual, predicted)
    return metrics

# Function to calculate Mean Absolute Error (MAE)
def mean_absolute_error(actual, predicted):
    return np.mean(np.abs(actual - predicted))

# Function to calculate Root Mean Squared Error (RMSE)
def root_mean_squared_error(actual, predicted):
    return sqrt(mean_squared_error(actual, predicted))

# Function to calculate R-squared value
def r_squared(actual, predicted):
    return r2_score(actual, predicted)

# Function to calculate Median Absolute Error
def median_absolute_error(actual, predicted):
    return np.median(np.abs(actual - predicted))

# Function to calculate Mean Squared Error (MSE)
def mean_squared_error(actual, predicted):
    return np.mean((actual - predicted) ** 2)

# Function to load data from CSV files in a directory
def load_data(data_dir):
    data_frames = {}
    for file in os.listdir(data_dir):
        if file.endswith('.csv'):
            # Extract ticker symbol from filename
            ticker = os.path.splitext(file)[0]
            # Read CSV file and store in dictionary with ticker symbol as key
            data_frames[ticker] = pd.read_csv(os.path.join(data_dir, file))
    return data_frames

# Function to analyze performance metrics for all files in a directory
def analyze_all_files(directory_path):
    # Load data from CSV files
    data_frames = load_data(directory_path)
    metrics_results = {}
    # Calculate metrics for each ticker
    for ticker, df in data_frames.items():
        metrics = calculate_metrics(df)
        metrics_results[ticker] = metrics
    return metrics_results

# Function to plot performance metrics for each ticker
def plot_metrics(metrics_results):
    # Convert metrics results to DataFrame
    metrics_df = pd.DataFrame(metrics_results).T
    # Plot bar graph
    metrics_df.plot(kind='bar', figsize=(12, 8))
    # Add title and labels
    plt.title('Performance Metrics for Each Ticker')
    plt.xlabel('Ticker')
    plt.ylabel('Metric Value')
    plt.xticks(rotation=45)
    # Show plot
    plt.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))
    plt.tight_layout()
    plt.show()

# Directory path containing CSV files
directory_path = 'metricdata'
# Analyze performance metrics for all files in the directory
all_metrics = analyze_all_files(directory_path)
# Print metrics results
print(all_metrics)
# Plot performance metrics
plot_metrics(all_metrics)
