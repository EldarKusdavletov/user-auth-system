from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import bcrypt
import base64

app = Flask(__name__)

# Configuration for Flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kusdavletov:your_password@localhost/user_auth_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secure key in production
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this in production

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)

# User model for PostgreSQL
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')
    
    def __repr__(self):
        return f"<User {self.username}>"

# Endpoint to check if the server is running
@app.route('/')
def home():
    return jsonify(message="User Authentication System is up and running!")

# User Registration Endpoint
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()  # Get the incoming JSON data
    
    # Check if the data is provided
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify(message="Missing required fields"), 400
    
    username = data['username']
    email = data['email']
    password = data['password']
    
    # Check if the user already exists
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify(message="Username already exists"), 400
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify(message="Email already exists"), 400
    
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # You can store it as base64-encoded string if needed:
    encoded_password = base64.b64encode(hashed_password).decode('utf-8')

    # Create a new user
    new_user = User(username=username, email=email, password_hash=encoded_password)
    
    # Add the user to the database
    db.session.add(new_user)
    db.session.commit()
    
    # Generate JWT token for the user (ensure identity is a string)
    access_token = create_access_token(identity=str(new_user.id))
    
    return jsonify(message="User registered successfully", access_token=access_token), 201

# User Login Endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Get the incoming JSON data
    
    # Check if the data is provided
    if not data or not data.get('username') or not data.get('password'):
        return jsonify(message="Missing required fields"), 400
    
    username_or_email = data['username']
    password = data['password']
    
    # Check if the user exists by username or email
    user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()
    
    if not user:
        return jsonify(message="Invalid credentials"), 401
    
    # Decode the stored password hash from base64 if stored as base64
    stored_hash = base64.b64decode(user.password_hash)
    
    # Check if the password matches
    if not bcrypt.checkpw(password.encode('utf-8'), stored_hash):
        return jsonify(message="Invalid credentials"), 401
    
    # Generate JWT token for the user (ensure identity is a string)
    access_token = create_access_token(identity=str(user.id))
    
    return jsonify(message="Login successful", access_token=access_token), 200

# Protected Route Example
@app.route('/profile', methods=['GET'])
@jwt_required()  # Protect this route
def profile():
    # Get the current user's identity from the JWT token
    current_user_id = get_jwt_identity()

    # Query the user details from the database using their ID
    user = User.query.get(current_user_id)

    if not user:
        return jsonify(message="User not found"), 404

    return jsonify(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role
    ), 200

if __name__ == '__main__':
    db.create_all()  # Create tables if they don't exist yet
    app.run(debug=True)

