import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kusdavletov'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://kusdavletov@localhost/user_auth_db'
