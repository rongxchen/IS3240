from flask import Blueprint
from general_config import token_required, result

favourite_api = Blueprint("favourite_api", __name__)

@favourite_api.post("/favourites")
@token_required
def get_user_favourites(user_id):
    # todo: fetch from database
    return result(200, "success")

@favourite_api.post("/favourites/add")
@token_required
def add_favourite(user_id):
    # todo: add to database
    return result(200, "success")

@favourite_api.delete("/favourites")
@token_required
def delete_favourite(user_id):
    # todo: delete from database
    return result(200, "success")
