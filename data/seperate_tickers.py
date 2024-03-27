import csv

# Read the data
with open('data/combineddata.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header
    data = [row for row in reader]

# Organize data based on ticker symbol
ticker_data = {}
for row in data:
    ticker = row[0]
    if ticker not in ticker_data:
        ticker_data[ticker] = []
    ticker_data[ticker].append(row)

# Write data to separate files
for ticker, rows in ticker_data.items():
    filename = f'data/{ticker}_data.csv'
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['symbol', 'Date', 'Open', 'High', 'Low', 'avg_sentiment_score'])
        writer.writerows(rows)

print("Data has been split into separate files based on ticker symbol.")
