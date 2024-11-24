# User Authentication System with Flask, PostgreSQL, MongoDB, and Redis

This is a user authentication system built with **Flask**, **PostgreSQL**, **MongoDB**, and **Redis**. The system provides secure user registration, login, JWT-based session management, and logging of user activities. Redis is used for session caching, and MongoDB logs all login attempts.

## Features

- **User Registration**: Users can register with a username, email, and password. Passwords are securely hashed and stored.
- **User Login**: Users can log in with their username/email and password, and a JWT token is generated for session management.
- **Session Management**: Redis is used to cache session data, making it fast and scalable.
- **Login Logging**: All successful login attempts are logged in MongoDB, including the timestamp and IP address.
- **Protected Routes**: Certain routes, like the user profile, require authentication using JWT tokens.

## Requirements

- Python 3
- PostgreSQL
- MongoDB
- Redis

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/user-auth-system.git
   cd user-auth-system
   ```

2. **Create a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use venv\Scripts\activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Create and update the .env file with your configuration:**

    ```env
    DATABASE_URI=postgresql://username:password@localhost:5432/user_auth_db
    MONGO_URI=mongodb://localhost:27017
    REDIS_URL=redis://localhost:6379/0
    
    MONGO_DB=user_auth_mongo
    SECRET_KEY=your-secret-key
    JWT_SECRET_KEY=your-jwt-secret-key
    ```

Replace the placeholders with your actual credentials.

## Run the application:

  ```bash
  flask run
  ```

## Endpoints
- `POST /register`: Register a new user with `username`, `email`, and `password`.
- `POST /login`: Log in with `username` or `email` and `password`.
- `GET /profile`: Get the user's profile information. Requires a valid JWT token.

## Usage
1. Register a new user via `/register`.
2. Log in to obtain a JWT token via `/login`.
3. Use the token to access protected routes like `/profile`.
