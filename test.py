import psycopg2

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="aloof-fly-2725.g95.cockroachlabs.cloud",
    port="26257",
    database="defaultdb",
    user="rudra",
    password="T97qiqj7IfyXCNWUcuZDiQ"
)

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Execute a SELECT query
cursor.execute("SELECT * FROM employees")

# Fetch all rows from the result set
rows = cursor.fetchall()

# Print the data
for row in rows:
    print(row)

# Close the cursor and connection
cursor.close()
conn.close()
