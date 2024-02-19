import os
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import re

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


# Function to extract predicted price from the prediction sentence
def extract_predicted_price(prediction_sentence):
    # Use regular expression to find the predicted price in the sentence
    matches = re.findall(r'\d+(\.\d+)?', prediction_sentence)
    if matches:
        return float(matches[0])  # Assuming the first match is the predicted price
    else:
        return None  # Return None if no price is found

# Function to calculate Mean Squared Error (MSE)
def calculate_mse(predicted_price, actual_price):
    if predicted_price is not None:
        mse = (predicted_price - actual_price) ** 2
        return mse
    else:
        return None

# Function to make predictions using OpenAI
def make_prediction(combined_summary, linear_regression_summary, actual_price):
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
    predicted_sentence = completion.choices[0].message

    # Check if the predicted_sentence is a string
    if isinstance(predicted_sentence, str):
        predicted_price = extract_predicted_price(predicted_sentence)
    else:
        predicted_price = None

    # Calculate MSE
    mse = calculate_mse(predicted_price, actual_price)

    return predicted_sentence, mse


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

    # Assuming you have an actual price available
    actual_price = 100.0  # Replace with the actual price

    # Make a prediction
    prediction, mse = make_prediction(df_combined, df_linear, actual_price)

    # Save prediction results and MSE to CSV
    prediction_df = pd.DataFrame({"Prediction": [prediction], "MSE": [mse]})
    prediction_df.to_csv(
        os.path.join(current_dir, "../data/gpt_prediction.csv"), index=False
    )

    print("Prediction:", prediction)
    print("Mean Squared Error:", mse)


if __name__ == "__main__":
    main()

