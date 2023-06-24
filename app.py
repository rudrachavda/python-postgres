from flask import Flask, jsonify, request
import psycopg2
from colorama import Fore, Style

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="aloof-fly-2725.g95.cockroachlabs.cloud",
    port="26257",
    database="defaultdb",
    user="rudra",
    password="T97qiqj7IfyXCNWUcuZDiQ"
)

app = Flask(__name__)

# Endpoint to get all employees 
@app.route('/employees', methods=['GET']) #add /id: after employees
def get_employees():
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Execute a SELECT query to retrieve employee data
    cursor.execute("SELECT e.employee_id, e.first_name, e.last_name, e.location, d.department_name FROM employee e, department d where e.department_id=d.department_id")

    # Fetch all rows from the result set
    rows = cursor.fetchall()

    # Assign employees to their departments based on their IDs
    employee_departments = []
    for row in rows:
        employee_id, first_name, last_name, location, department_name = row

        if location == "California":
            work_status =  "Local" 
        else:
            work_status =  "Remote" 

        employee = {
            "id" : employee_id,
            "firstName" : first_name,
            "lastName" : last_name,
            "location" : location,
            "departmentName":department_name,
            "workStatus"  : work_status
        }
        
        # # Store the employee's department and work status
        # employee_departments[employee_id] = {
        #     "department": department,
        #     "work_status": work_status
        # }
        employee_departments.append(employee)

    # Close the cursor
    cursor.close()

    return jsonify(employee_departments), 200


# Endpoint to create a new employee
@app.route('/employees', methods=['POST'])
def create_employee():
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    location = data.get('location')
    department_id = data.get('department_id')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Execute an INSERT query to create a new employee
    cursor.execute("INSERT INTO employee (first_name, last_name, location, department_id) VALUES (%s, %s, %s, %s) RETURNING employee_id;",
        (first_name, last_name, location, department_id))

    # Get the newly created employee ID
    employee_id = cursor.fetchone()[0]

    # Commit the transaction
    conn.commit()

    # Close the cursor
    cursor.close()

    return jsonify({'employee_id': employee_id}), 201


# Endpoint to update an employee
@app.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    location = data.get('location')
    department_id = data.get('department_id')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Execute an UPDATE query to update the employee
    cursor.execute("UPDATE employee SET first_name = %s, last_name = %s, location = %s, department_id = %s WHERE employee_id = %s;",
        (first_name, last_name, location, department_id, employee_id))

    # Commit the transaction
    conn.commit()

    # Close the cursor
    cursor.close()

    return jsonify({'message': 'Employee updated successfully'}), 200


# Endpoint to delete an employee
@app.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Execute a DELETE query to delete the employee
    cursor.execute("DELETE FROM employee WHERE employee_id = %s;", (employee_id,))

    # Commit the transaction
    conn.commit()

    # Close the cursor
    cursor.close()

    return jsonify({'message': 'Employee deleted successfully'}), 200


if __name__ == '__main__':
    app.run()
