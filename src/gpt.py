import os
from openai import OpenAI
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Function to load data from the combined CSV file
def load_data(combined_data_path, linear_regression_data_path):
    df_combined = pd.read_csv(combined_data_path)
    df_linear = pd.read_csv(linear_regression_data_path)
    return df_combined, df_linear

# Function to set up OpenAI API key with an empty string as a fallback
def setup_openai_api():
    os.environ["OPENAI_API_KEY"] = os.getenv("GPT_KEY", "")


# Function to make predictions using OpenAI
def make_prediction(combined_summary, linear_regression_summary):
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a Predictive Modeler. You will be tasked with generating predictive analytics based on data. This involves interpreting the data you've processed and making forecasts, such as predicting stock prices. Your output should be one number. Not a formula",
            },
            {
                "role": "user",
                "content": f"Give me a next day closing price prediction based on the data from these two CSV files: {combined_summary}, {linear_regression_summary}."
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

    # Set up OpenAI API key
    setup_openai_api()

    # Make a prediction
    prediction = make_prediction(df_combined, df_linear)

    # Save prediction results to CSV
    prediction_df = pd.DataFrame({"Prediction": [prediction]})
    prediction_df.to_csv(
        os.path.join(current_dir, "../data/gpt_prediction.csv"), index=False
    )

    print("Prediction:", prediction)


if __name__ == "__main__":
    main()
