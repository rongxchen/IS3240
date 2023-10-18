from flask import Blueprint, request
from general_config import token_required, result
from services import favourite_service

favourite_api = Blueprint("favourite_api", __name__)

@favourite_api.get("/api/favourites")
@token_required
def get_user_favourites(user_id):
    favourites = favourite_service.get_favourites(user_id)
    return result(200, "success", favourites)

@favourite_api.post("/api/favourites")
@token_required
def add_favourite(user_id):
    """
    :param user_id: user id
    :param data: {symbol: xxx, market: xxx}
    :return:
    """
    data = request.json
    symbol = str(data["symbol"]).upper()
    market = str(data["market"]).upper()
    favourite_service.add_or_remove_favourite(user_id, symbol, market)
    favourite = favourite_service.get_favourite_by_symbol(user_id, symbol)
    return result(200, "success", favourite)
