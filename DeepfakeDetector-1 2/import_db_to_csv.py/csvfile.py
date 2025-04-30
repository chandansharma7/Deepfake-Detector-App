import sqlite3
import csv

# Connect to your SQLite database
conn = sqlite3.connect('instance/deepfake_detector.db')
cursor = conn.cursor()

# Choose the table to export
table_name = 'uploads'  # change this if your table is named differently

# Fetch all data
cursor.execute(f"SELECT * FROM {'detection_result'}")
rows = cursor.fetchall()

# Get column names
column_names = [description[0] for description in cursor.description]

# Export to CSV
with open('exported_data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(column_names)  # Write headers
    writer.writerows(rows)         # Write data rows

print(f"✅ Exported {len(rows)} records to 'exported_data.csv'")

# Close connection
conn.close()

