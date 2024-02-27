import sqlite3

try:
    conn = sqlite3.connect('data/stock_news.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articles")
    rows = cursor.fetchall()

    # Print the fetched rows
    for row in rows:
        print(row)

except sqlite3.Error as e:
    print("SQLite error:", e)

finally:
    # Close the cursor and database connection
    cursor.close()
    conn.close()
