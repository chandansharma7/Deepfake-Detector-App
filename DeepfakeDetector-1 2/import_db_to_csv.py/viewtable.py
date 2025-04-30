import sqlite3

# Connect to your database
conn = sqlite3.connect('instance/deepfake_detector.db')
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tables inside database:", tables)

conn.close()
