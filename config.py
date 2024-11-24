import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class Config:
    # PostgreSQL settings
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret Keys
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

    # MongoDB settings
    MONGO_URI = os.getenv('MONGO_URI')
    MONGO_DB = os.getenv('MONGO_DB')

    # Redis settings
    REDIS_URL = os.getenv('REDIS_URL')

