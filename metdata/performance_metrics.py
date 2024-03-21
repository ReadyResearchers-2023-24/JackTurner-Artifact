import pandas as pd
import numpy as np
import os
from math import sqrt
from sklearn.metrics import r2_score, explained_variance_score as ev_score
import matplotlib.pyplot as plt

def calculate_metrics(data):
    actual_col = 'Actual'
    predicted_col = 'Prediction'
    actual = data[actual_col]
    predicted = data[predicted_col]
    metrics = {}
    metrics['MAE'] = mean_absolute_error(actual, predicted)
    metrics['RMSE'] = root_mean_squared_error(actual, predicted)
    metrics['R_squared'] = r_squared(actual, predicted)
    metrics['Explained_Variance'] = ev_score(actual, predicted)
    metrics['Median_Absolute_Error'] = median_absolute_error(actual, predicted)
    return metrics

def mean_absolute_error(actual, predicted):
    return np.mean(np.abs(actual - predicted))

def root_mean_squared_error(actual, predicted):
    return sqrt(mean_squared_error(actual, predicted))

def r_squared(actual, predicted):
    return r2_score(actual, predicted)

def median_absolute_error(actual, predicted):
    return np.median(np.abs(actual - predicted))

def mean_squared_error(actual, predicted):
    return np.mean((actual - predicted) ** 2)

def load_data(data_dir):
    data_frames = {}
    for file in os.listdir(data_dir):
        if file.endswith('.csv'):
            ticker = os.path.splitext(file)[0]
            data_frames[ticker] = pd.read_csv(os.path.join(data_dir, file))
    return data_frames

def analyze_all_files(directory_path):
    data_frames = load_data(directory_path)
    metrics_results = {}
    for ticker, df in data_frames.items():
        metrics = calculate_metrics(df)
        metrics_results[ticker] = metrics
    return metrics_results

def plot_metrics(metrics_results):
    metrics_df = pd.DataFrame(metrics_results).T
    metrics_df.plot(kind='bar', figsize=(12, 8))
    plt.title('Performance Metrics for Each Ticker')
    plt.xlabel('Ticker')
    plt.ylabel('Metric Value')
    plt.xticks(rotation=45)
    plt.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))
    plt.tight_layout()
    plt.show()

# Example usage
directory_path = 'metdata'
all_metrics = analyze_all_files(directory_path)
print(all_metrics)

plot_metrics(all_metrics)
