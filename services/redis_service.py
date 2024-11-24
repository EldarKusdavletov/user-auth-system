import redis
import os

redis_client = redis.StrictRedis.from_url(os.getenv('REDIS_URL'), decode_responses=True)

def store_session_data(user):
    redis_client.set(f"user_session:{user.id}", str(user.to_dict()), ex=3600)  # 1 hour expiry

def get_session_data(user_id):
    session_data = redis_client.get(f"user_session:{user_id}")
    if not session_data:
        return None
    return eval(session_data)

