from functools import wraps
from flask import Blueprint, request
from general_config import result
from utils import jwt_util
from utils.jwt_util import get_token
from services import user_service

user_api = Blueprint("user_api", __name__)

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

@user_api.post("/api/users")
def login():
    body = request.json
    username = body["username"]
    password = body["password"]
    is_login, msg, data = user_service.login(username, password)
    if not is_login:
        return result(401, msg)
    token = get_token(data)
    return result(200, msg, token)

@user_api.post("/api/users/register")
def register():
    body = request.json
    username = body["username"]
    password = body["password"]
    is_registered, msg = user_service.register(username, password)
    if is_registered:
        return result(200, msg)
    return result(400, msg)

@user_api.put("/api/users")
@token_required
def change_password(user_id):
    body = request.json
    new_password = body["new_password"]
    is_changed, msg = user_service.change_password(user_id, new_password)
    if is_changed:
        return result(200, msg)
    return result(400, msg)

@user_api.delete("/api/users")
@token_required
def delete_account(user_id):
    is_deleted, msg = user_service.delete_account(user_id)
    if is_deleted:
        return result(200, msg)
    return result(400, msg)
