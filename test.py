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

# Execute a SELECT query to retrieve employee data
cursor.execute("SELECT employee_id, first_name, last_name, location, department_id FROM employee;")

# Fetch all rows from the result set
rows = cursor.fetchall()

# Assign employees to their departments based on their IDs
employee_departments = {}
for row in rows:
    employee_id, first_name, last_name, location, department_id = row

    # Determine the department based on the employee ID
    if department_id == 1:
        department = "Marketing"
    elif department_id == 2:
        department = "Sales"
    elif department_id == 3:
        department = "IT"
    else:
        department = "Unknown Department"

    # Determine if the employee can work remotely or locally based on their location
    if location == "California":
        work_status = "Local"
    else:
        work_status = "Remote"

    # Store the employee's department and work status
    employee_departments[employee_id] = {
        "department": department,
        "work_status": work_status
    }

# Print the assigned departments and work status for each employee
for employee_id, data in employee_departments.items():
    department = data["department"]
    work_status = data["work_status"]
    print(f"Employee ID: {employee_id}, Department: {department}, Work Status: {work_status}")

# Close the cursor and connection
cursor.close()
conn.close()
