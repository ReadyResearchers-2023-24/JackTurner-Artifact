import os
import pandas as pd
import matplotlib.pyplot as plt

# Function to create line graph and save it for each file
def create_line_graph(file_path):
    # Read CSV file
    df = pd.read_csv(file_path, parse_dates=['Date'])
    
    # Extract data
    date = df['Date']
    prediction = df['Prediction']
    actual = df['Actual']
    
    # Plot line graph with transparency
    plt.figure(figsize=(10, 6))
    plt.plot(date, prediction, label='Prediction', marker='o', alpha=0.7)  # Set transparency to 0.7
    plt.plot(date, actual, label='Actual', marker='o', alpha=0.7)  # Set transparency to 0.7
    
    # Add title and labels
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    plt.title(f'{file_name} - Prediction vs Actual')
    plt.xlabel('Date')
    plt.ylabel('Value')
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    
    # Add legend
    plt.legend()
    
    # Save graph as image file
    file_name = file_name + '_line_graph.png'
    plt.savefig(file_name, bbox_inches='tight', transparent=True)  # Save with transparency
    plt.close()

# Directory path containing CSV files
directory_path = 'metricdata'

# Iterate over files in directory
for file in os.listdir(directory_path):
    if file.endswith('.csv'):
        file_path = os.path.join(directory_path, file)
        create_line_graph(file_path)
