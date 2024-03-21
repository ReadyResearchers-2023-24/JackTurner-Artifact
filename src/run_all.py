import subprocess

def run_script(script_path):
    subprocess.run(["python", script_path])

if __name__ == "__main__":
    # Run fetch_historical_data.py and multiple_ticker_sent.py
    run_script("src/fetch_historical_data.py")
    run_script("src/multiple_ticker_sent.py")

    # Run avg.py located in the data folder
    run_script("data/avg.py")

    # Run combined_data.py
    run_script("data/combined_data.py")

    # Run seperate_tickers.py
    run_script("data/seperate_tickers.py")

    # Run gpt.py
    run_script("src/gpt.py")
