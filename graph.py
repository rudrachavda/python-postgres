import psycopg2
import matplotlib.pyplot as plt

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

# Execute a SELECT query to retrieve employee data
cursor.execute("SELECT department_id, COUNT(*) FROM employee GROUP BY department_id;")

# Fetch all rows from the result set
rows = cursor.fetchall()

# Store department IDs and employee counts
department_ids = []
employee_counts = []
for row in rows:
    department_id, count = row
    department_ids.append(department_id)
    employee_counts.append(count)

# Close the cursor and connection
cursor.close()
conn.close()

# Create a bar chart
plt.bar(department_ids, employee_counts)
plt.xlabel("Department ID")
plt.ylabel("Number of Employees")
plt.title("Employee Count by Department")
plt.show()
