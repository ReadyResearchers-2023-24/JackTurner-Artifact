import os
from openai import OpenAI
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd

# Initialize Dash app
app = dash.Dash(__name__)

# Function to set up OpenAI API key
def setup_openai_api(api_key):
    os.environ["OPENAI_API_KEY"] = api_key

# Function to make predictions using OpenAI
def make_prediction(combined_summary, linear_regression_summary):
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[
            {
                "role": "system",
                "content": "You are a Predictive Modeler. You will be tasked with generating predictive analytics based on data. This involves interpreting the data you've processed and making forecasts, such as predicting stock prices. Your output needs to be a prediction, not a set of instructions. I want you to give me your prediction for the next day. ",
            },
            {
                "role": "user",
                "content": f"Given the attached CSV file named 'combined_data.csv', which contains daily stock prices and average sentiment scores for the last 30 days, please analyze the data to predict the stock's closing price for the next day. The dataset includes the following columns: 'Date', 'Average Sentiment', 'Open', 'High', 'Low', 'Close', 'Volume'. Use the 'Average Sentiment' and 'Volume' as features to predict the 'Close' price.{combined_summary}. Here is the linear regression model I have performed for today to assist you in making predictions. {linear_regression_summary} I want you to return to me a prediction with the 'Date' format.",
            },
        ],
    )
    return completion.choices[0].message

# Define layout of Dash app
app.layout = html.Div([
    dcc.Textarea(id='combined-summary', placeholder='Combined Summary', rows=4, style={'width': '100%'}),
    dcc.Textarea(id='linear-regression-summary', placeholder='Linear Regression Summary', rows=4, style={'width': '100%'}),
    html.Button('Get Prediction', id='get-prediction-btn', n_clicks=0),
    html.Div(id='prediction-output')
])

# Define callback to get prediction when button is clicked
@app.callback(
    Output('prediction-output', 'children'),
    [Input('get-prediction-btn', 'n_clicks')],
    [dash.dependencies.State('combined-summary', 'value'),
     dash.dependencies.State('linear-regression-summary', 'value')]
)
def get_prediction(n_clicks, combined_summary, linear_regression_summary):
    # Set up OpenAI API key
    setup_openai_api("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")

    # Make prediction
    prediction = make_prediction(combined_summary, linear_regression_summary)

    return prediction

if __name__ == '__main__':
    app.run_server(debug=True)
