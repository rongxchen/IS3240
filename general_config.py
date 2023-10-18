import os
from functools import wraps
from flask import request, render_template
from utils import jwt_util

db_path = "sqlite:///" + os.path.join(os.path.dirname(__file__), "sqlite3.db")
tiger_token_path = os.path.join(os.path.dirname(__file__), "TigerTrade_access_token.txt")
resource_path = os.path.join(os.path.dirname(__file__), "resources")

def result(code: int, message: str, data: any = None):
    return {
        "code": code,
        "data": data,
        "message": message
    }

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        # token = request.headers["Authorization"] if "Authorization" in request.headers else None
        # if not token:
            # return result(403, "unauthorized")
        # verified, resp = jwt_util.verify_token(token)
        # if not verified:
            # return result(403, f"unauthorized: {resp}")
        return f('resp', *args, **kwargs)
    return decorator

def remove_all_matched(dir_path, prefix):
    files = os.listdir(dir_path)
    for file in files:
        if file.startswith(prefix):
            os.remove(os.path.join(dir_path, file))
