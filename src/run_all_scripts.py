import os
import subprocess


def run_script(script_path):
    print(f"Running script: {script_path}")
    subprocess.run(["python", script_path])


def main():
    # Define the paths to your scripts
    script_paths = [
        "combine_data.py",
        "fetch_historical_data.py",
        "fetch_sentiment_data.py",
        "predict_closing_price.py",
    ]

    # Get the current directory of the script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Run each script
    for script_path in script_paths:
        full_script_path = os.path.join(current_dir, script_path)
        run_script(full_script_path)


if __name__ == "__main__":
    main()
