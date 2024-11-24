from flask_jwt_extended import create_access_token
import bcrypt
import base64
from models.user import User
from services.redis_service import store_session_data, get_session_data
from services.mongo_service import log_login_attempt
from datetime import datetime

def register_user(db, username, email, password):
    user = User.query.filter_by(username=username).first()
    if user:
        return {"message": "Username already exists"}, 400

    user = User.query.filter_by(email=email).first()
    if user:
        return {"message": "Email already exists"}, 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    encoded_password = base64.b64encode(hashed_password).decode('utf-8')

    new_user = User(username=username, email=email, password_hash=encoded_password)
    db.session.add(new_user)
    db.session.commit()

    # Store session data in Redis
    store_session_data(new_user)

    access_token = create_access_token(identity=str(new_user.id))
    return {"message": "User registered successfully", "access_token": access_token}, 201

def login_user(db, username_or_email, password):
    user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()
    if not user:
        return {"message": "Invalid credentials"}, 401

    stored_hash = base64.b64decode(user.password_hash)
    if not bcrypt.checkpw(password.encode('utf-8'), stored_hash):
        return {"message": "Invalid credentials"}, 401

    # Store session data in Redis
    store_session_data(user)

    access_token = create_access_token(identity=str(user.id))

    # Log login attempt
    log_login_attempt(user)

    return {"message": "Login successful", "access_token": access_token}, 200

