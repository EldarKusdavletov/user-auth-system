from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import os
from dotenv import load_dotenv
from services.auth_service import register_user, login_user
from utils.validation import validate_registration_data, validate_login_data

# Load environment variables
load_dotenv()

# Initialize Flask and Extensions
app = Flask(__name__)

# Configuration
app.config.from_object('config.Config')

# Initialize SQLAlchemy (PostgreSQL)
db = SQLAlchemy(app)
jwt = JWTManager(app)

# User Registration Endpoint
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    validation_error = validate_registration_data(data)
    if validation_error:
        return jsonify(validation_error)

    return jsonify(*register_user(db, data['username'], data['email'], data['password']))

# User Login Endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    validation_error = validate_login_data(data)
    if validation_error:
        return jsonify(validation_error)

    return jsonify(*login_user(db, data['username'], data['password']))

# Protected Route Example
@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()

    session_data = get_session_data(current_user_id)
    if not session_data:
        return jsonify(message="Session expired. Please log in again."), 401

    return jsonify(session_data), 200

if __name__ == '__main__':
    db.create_all()  # Create PostgreSQL tables if they don't exist yet
    app.run(debug=True)

