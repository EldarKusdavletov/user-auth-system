import pymongo
from datetime import datetime
import os

mongo_client = pymongo.MongoClient(os.getenv('MONGO_URI'))
mongo_db = mongo_client[os.getenv('MONGO_DB')]
login_logs = mongo_db['login_logs']  # MongoDB collection for login logs

def log_login_attempt(user):
    login_log = {
        "user_id": user.id,
        "username": user.username,
        "timestamp": datetime.utcnow()
    }
    login_logs.insert_one(login_log)

