import sqlite3
import csv
from flask import Flask, render_template, jsonify

app = Flask(__name__)



# Function to import data from CSV to SQLite database
def import_csv_to_sqlite(csv_file, db_file, table_name):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create table
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join([f'{h.strip()} TEXT' for h in headers])})")

        # Insert data
        for row in reader:
            cursor.execute(f"INSERT INTO {table_name} VALUES ({', '.join(['?' for _ in headers])})", row)

    conn.commit()
    conn.close()

# Route to fetch data from SQLite database and serve it as JSON
@app.route('/fetch-data')
def fetch_data():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM ScoresTable")
    rows = cursor.fetchall()

    conn.close()

    # Convert SQLite rows to JSON
    data = [{key: row[key] for key in row.keys()} for row in rows]
    return jsonify(data)

# Route to serve the HTML view page
@app.route('/')
def view_page():
    return render_template('index.html')

if __name__ == '__main__':
    # Import data from CSV to SQLite database
    import_csv_to_sqlite('2006-07_School_Progress_Reports_-_All_Schools.csv', 'data.db', 'ScoresTable')
    
    # Run Flask app
    app.run(debug=True)  # Debug mode for development
