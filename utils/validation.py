def validate_registration_data(data):
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return {"message": "Missing required fields"}, 400
    return None

def validate_login_data(data):
    if not data or not data.get('username') or not data.get('password'):
        return {"message": "Missing required fields"}, 400
    return None

