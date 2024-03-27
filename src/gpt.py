import os
from openai import OpenAI
import pandas as pd
from dotenv import load_dotenv
import re
from sklearn.metrics import mean_squared_error

# Load environment variables from .env
load_dotenv()

# Function to load data from the combined CSV file
def load_data(data_dir):
    dfs = {}
    for filename in os.listdir(data_dir):
        if filename.endswith("data.csv"):
            ticker = os.path.splitext(filename)[0]
            dfs[ticker] = pd.read_csv(os.path.join(data_dir, filename))
    return dfs

# Function to set up OpenAI API key with an empty string as a fallback
def setup_openai_api():
    os.environ["OPENAI_API_KEY"] = os.getenv("GPT_KEY", "")

# Function to make predictions using OpenAI API
def make_prediction(df):
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"Give me a closing price prediction every day for the past month based on the data attached. {df.to_string()}",
            },
        ],
    )
    return completion.choices[0].message

# Main function to orchestrate the modular components
def main():
    # Get the current directory of the script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    data_dir = os.path.join(parent_dir, "data")

    # Load the data
    dfs = load_data(data_dir)

    # Set up OpenAI API key
    setup_openai_api()

    # Make predictions for each ticker symbol
    predictions = {}
    for ticker, df in dfs.items():
        predictions[ticker] = make_prediction(df)

    # Save prediction results to CSV
    prediction_df = pd.DataFrame(predictions.items(), columns=['Ticker', 'Prediction'])
    prediction_df.to_csv(
        os.path.join(current_dir, "../data/gpt_prediction.csv"), index=False
    )

    print("Predictions:", predictions)

if __name__ == "__main__":
    main()
