import os
from openai import OpenAI
import pandas as pd


# Function to load data from the combined CSV file
def load_data(combined_data_path, linear_regression_data):
    df_combined = pd.read_csv(combined_data_path)
    df_linear = pd.read_csv(linear_regression_data)
    return df_combined, df_linear


# Function to create summaries or extract relevant data
def summarize_data(df_combined, df_linear):
    combined_summary = df_combined.describe().to_string()
    linear_regression_summary = df_linear.describe().to_string()
    return combined_summary, linear_regression_summary


# Function to set up OpenAI API key
def setup_openai_api(api_key):
    os.environ["OPENAI_API_KEY"] = api_key


# Function to make predictions using OpenAI
def make_prediction(combined_summary, linear_regression_summary):
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a Predictive Modeler tasked with generating theoretical predictive analytics. Your output should be a hypothetical prediction based on provided data and insights, not real-time analysis or data processing. ",
            },
            {
                "role": "user",
                "content": f"Given a dataset with daily stock prices and average sentiment scores for the last 30 days, including 'Date', 'Average Sentiment', 'Open', 'High', 'Low', 'Close', 'Volume', please simulate an analysis to predict the stock's closing price for tomorrow. Assume today's date is YYYY-MM-DD, and use 'Average Sentiment' and 'Volume' as key features in your theoretical model. Here's a summary of a linear regression analysis performed today: [insert summary here]. Based on this, predict the closing price for the next day (YYYY-MM-DD+1), focusing on the impact of 'Average Sentiment' and 'Volume'.",
            },
        ],
    )
    return completion.choices[0].message


# Main function to orchestrate the modular components
def main():
    # Get the current directory of the script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

    # Path to your combined CSV file
    combined_data_path = os.path.join(parent_dir, "data", "combined_data.csv")
    linear_data_path = os.path.join(
        parent_dir, "data", "linear_regression_prediction.csv"
    )

    # Load the data
    df_combined, df_linear = load_data(combined_data_path, linear_data_path)

    # Summarize the data
    combined_summary, linear_regression_summary = summarize_data(df_combined, df_linear)

    # Set up OpenAI API key
    setup_openai_api("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")

    # Make a prediction
    prediction = make_prediction(combined_summary, linear_regression_summary)

    # Save prediction results to CSV
    prediction_df = pd.DataFrame({"Prediction": [prediction]})
    prediction_df.to_csv(
        os.path.join(current_dir, "../data/gpt_prediction.csv"), index=False
    )

    print("Prediction:", prediction)


if __name__ == "__main__":
    main()