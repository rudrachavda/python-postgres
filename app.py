from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rudra:T97qiqj7IfyXCNWUcuZDiQ@aloof-fly-2725.g95.cockroachlabs.cloud:26257/defaultdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-secret-key'

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

# Employee Model
class Employee(db.Model):
    employee_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)

    def __init__(self, first_name, last_name, location, department_id, date_of_birth):
        self.first_name = first_name
        self.last_name = last_name
        self.location = location
        self.department_id = department_id
        self.date_of_birth = date_of_birth

# Employee Schema
class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ('employee_id', 'first_name', 'last_name', 'location', 'department_id', 'date_of_birth')

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)

# Endpoint to get all employees
@app.route('/employees', methods=['GET'])
@jwt_required()
def get_employees():
    employees = Employee.query.all()
    result = employees_schema.dump(employees)
    return jsonify(result), 200

# Endpoint to create a new employee
@app.route('/employees', methods=['POST'])
@jwt_required()
def create_employee():
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    location = data.get('location')
    department_id = data.get('department_id')
    date_of_birth = data.get('date_of_birth')

    new_employee = Employee(first_name, last_name, location, department_id, date_of_birth)
    db.session.add(new_employee)
    db.session.commit()

    return jsonify(employee_schema.dump(new_employee)), 201

# Endpoint to update an employee
@app.route('/employees/<int:employee_id>', methods=['PUT'])
@jwt_required()
def update_employee(employee_id):
    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({'message': 'Employee not found'}), 404

    data = request.json
    employee.first_name = data.get('first_name', employee.first_name)
    employee.last_name = data.get('last_name', employee.last_name)
    employee.location = data.get('location', employee.location)
    employee.department_id = data.get('department_id', employee.department_id)
    employee.date_of_birth = data.get('date_of_birth', employee.date_of_birth)

    db.session.commit()

    return jsonify({'message': 'Employee updated successfully'}), 200

# Endpoint to delete an employee
@app.route('/employees/<int:employee_id>', methods=['DELETE'])
@jwt_required()
def delete_employee(employee_id):
    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({'message': 'Employee not found'}), 404

    db.session.delete(employee)
    db.session.commit()

    return jsonify({'message': 'Employee deleted successfully'}), 200

# Endpoint for user registration
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    hashed_password = generate_password_hash(password, method='sha256')

    # TODO: Save the user details to the database or any other storage

    return jsonify({'message': 'Registration successful'}), 201

# Endpoint for user login and generating JWT token
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # TODO: Retrieve the user details from the database or any other storage based on the provided username

    if not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=username)
    return jsonify({'access_token': access_token}), 200

if __name__ == '__main__':
    db.create_all()
    app.run()
