from flask import Blueprint, request
from general_config import result, token_required
from utils.jwt_util import get_token
from services import user_service

user_api = Blueprint("user_api", __name__)

@user_api.post("/api/users")
def login():
    """ user login
    :return: authorization token if the user is logged in successfully
    """
    body = request.json
    username = body["username"]
    password = body["password"]
    is_login, msg, data = user_service.login(username, password)
    user_info = {"username": data.username, "email": data.email}
    if not is_login:
        return result(401, msg)
    token = get_token(data.user_id)
    return result(200, msg, token)

@user_api.post("/api/users/register")
def register():
    """ user registration
    :return: /
    """
    body = request.json
    username = body["username"]
    email = body["email"]
    password = body["password"]
    is_registered, msg = user_service.register(username, email, password)
    if is_registered:
        return result(200, msg)
    return result(400, msg)

@user_api.put("/api/users")
@token_required
def change_password(user_id):
    """ change password
    :param user_id: user id for changing password
    :return: /
    """
    body = request.json
    new_password = body["new_password"]
    is_changed, msg = user_service.change_password(user_id, new_password)
    if is_changed:
        return result(200, msg)
    return result(400, msg)

@user_api.delete("/api/users")
@token_required
def delete_account(user_id):
    """ delete user account
    :param user_id: user id for deleting account
    :return: /
    """
    is_deleted, msg = user_service.delete_account(user_id)
    if is_deleted:
        return result(200, msg)
    return result(400, msg)
