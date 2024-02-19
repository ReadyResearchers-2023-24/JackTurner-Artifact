import os
from openai import OpenAI
import pandas as pd
from dotenv import load_dotenv
import re
from sklearn.metrics import mean_squared_error

# Load environment variables from .env
load_dotenv()

# Function to load data from the combined CSV file
def load_data(combined_data_path):
    df_combined = pd.read_csv(combined_data_path)
    return df_combined

# Function to set up OpenAI API key with an empty string as a fallback
def setup_openai_api():
    os.environ["OPENAI_API_KEY"] = os.getenv("GPT_KEY", "")

# Function to make predictions using OpenAI
def make_prediction(combined_summary):
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a Predictive Modeler. You will be tasked with generating predictive analytics based on data. This involves interpreting the data you've processed and making forecasts, such as predicting stock prices. Your output should be one number. I need you to give me predictions for the past 30 days based on the data that I am attaching. Make sure the CSV is formatted correctly so that I can easily extract data. ",
            },
            {
                "role": "user",
                "content": f"{combined_summary}"
            },
        ],
    )

    predicted_message = str(completion.choices[0].message)  # Convert to string
    predict_float = re.findall(r"\d+\.\d+", predicted_message)
    if predict_float:
        predict_float = float(predict_float[0])
    else:
        predict_float = None

    actual_price = 182.41
    mse = mean_squared_error([actual_price], [predict_float])  # Wrap actual_price and predict_float in lists

    return predicted_message, mse

# Main function to orchestrate the modular components
def main():
    # Get the current directory of the script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

    # Path to your combined CSV file
    combined_data_path = os.path.join(parent_dir, "data", "modified_combined_data.csv")

    # Load the data
    df_combined = load_data(combined_data_path)

    # Set up OpenAI API key
    setup_openai_api()

    # Insert actual closing price
    actual_price = 182.41

    # Make a prediction
    prediction, mse = make_prediction(df_combined)

    # Save prediction results to CSV
    prediction_df = pd.DataFrame({"Prediction": [prediction]})
    prediction_df.to_csv(
        os.path.join(current_dir, "../data/gpt_prediction.csv"), index=False
    )

    print("Prediction:", prediction)
    print("Mean Squared Error:", mse)

if __name__ == "__main__":
    main()