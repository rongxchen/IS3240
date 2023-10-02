import os
from functools import wraps
from flask import request
from utils import jwt_util

db_path = "sqlite:///" + os.path.join(os.path.dirname(__file__), "sqlite3.db")

def result(code: int, message: str, data: any = None):
    return {
        "code": code,
        "data": data,
        "message": message
    }

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers["Authorization"]
        if not token:
            return result(403, "unauthorized")
        verified, resp = jwt_util.verify_token(token)
        if not verified:
            return result(403, f"unauthorized: {resp}")
        return f(resp, *args, **kwargs)
    return decorator
