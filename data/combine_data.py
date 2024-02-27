import sqlite3

# Connect to the stock_prices database
conn_prices = sqlite3.connect('data/stock_prices.db')

# Connect to the stock_news database
conn_news = sqlite3.connect('data/stock_news.db')

try:
    # Create cursors for both connections
    cursor_prices = conn_prices.cursor()
    cursor_news = conn_news.cursor()

    # Execute SQL queries to select all records from each table
    cursor_prices.execute("SELECT * FROM stock_prices")
    cursor_news.execute("SELECT * FROM articles")

    # Fetch all records from the queries
    data_prices = cursor_prices.fetchall()
    data_news = cursor_news.fetchall()

    # Print the data from the stock_prices database
    print("Data from stock_prices database:")
    for row in data_prices:
        print(row)

    # Print the data from the stock_news database
    print("\nData from stock_news database:")
    for row in data_news:
        print(row)

except sqlite3.Error as e:
    print("Error:", e)

finally:
    # Close the cursors and database connections
    cursor_prices.close()
    cursor_news.close()
    conn_prices.close()
    conn_news.close()
