import jwt
from datetime import datetime

SEC_KEY = "5f4dcc3b5aa765d61d8327deb882cf99"
ONE_HOUR = 1000 * 60 * 60

def get_token(user_id, duration_hour = 4):
    token = jwt.encode({
        "user_id": user_id,
        "exp": int(datetime.now().timestamp() * 1000) + ONE_HOUR * duration_hour
    }, SEC_KEY, algorithm="HS256")
    return token

def verify_token(token):
    try:
        data = jwt.decode(token, SEC_KEY, algorithms="HS256")
        timestamp = int(datetime.now().timestamp() * 1000)
        expired = timestamp > data["exp"]
        return not expired, data["user_id"] if not expired else "token expired"
    except Exception as e:
        return False, str(e)
