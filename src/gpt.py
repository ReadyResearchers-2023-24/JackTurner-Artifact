import os
from openai import OpenAI
import pandas as pd
from dotenv import load_dotenv
import re
from sklearn.metrics import mean_squared_error

# Load environment variables from .env
load_dotenv()

# Function to load data from the combined CSV file
def load_data(aapl,amzn,goog,msft,tsla):
    df_aapl = pd.read_csv(aapl)
    df_amzn = pd.read_csv(amzn)
    df_goog = pd.read_csv(goog)
    df_msft = pd.read_csv(msft)
    df_tsla = pd.read_csv(tsla)
    return df_aapl,df_amzn,df_goog,df_msft,df_tsla

# Function to set up OpenAI API key with an empty string as a fallback
def setup_openai_api():
    os.environ["OPENAI_API_KEY"] = os.getenv("GPT_KEY", "")

def make_prediction(df_aapl, df_amzn, df_goog, df_msft, df_tsla):
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"You are a Predictive Modeler. You will be tasked with generating predictive analytics based on data. This involves interpreting the data you've processed and making forecasts, such as predicting stock prices. Your output should be a your predictions for closing prices based on the five ticker symbols in the attached file. I need you to give me predictions for the next day closing price based on the data that I am attaching. Make sure the CSV is formatted correctly so that I can easily extract data. Make sure the date is properly formatted for when your prediction is. {df_aapl,df_amzn,df_goog,df_msft,df_tsla}",
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
    aapl = os.path.join(parent_dir, "data", "AAPL_data.csv")
    amzn = os.path.join(parent_dir, "data", "AMZN_data.csv")
    goog = os.path.join(parent_dir, "data", "GOOGL_data.csv")
    msft = os.path.join(parent_dir, "data", "MSFT_data.csv")
    tsla = os.path.join(parent_dir, "data", "TSLA_data.csv")

    # Load the data
    df_aapl, df_amzn, df_goog, df_msft, df_tsla = load_data(aapl, amzn, goog, msft, tsla)

    # Set up OpenAI API key
    setup_openai_api()

    # Make a prediction
    prediction = make_prediction(df_aapl, df_amzn, df_goog, df_msft, df_tsla)

    # Save prediction results to CSV
    prediction_df = pd.DataFrame({"Prediction": [prediction]})
    prediction_df.to_csv(
        os.path.join(current_dir, "../data/gpt_prediction.csv"), index=False
    )

    print("Prediction:", prediction)

if __name__ == "__main__":
    main()
