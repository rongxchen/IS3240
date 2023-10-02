from services import stock_service
from general_config import result, token_required
from flask import Blueprint

stock_api = Blueprint("stock_api", __name__)

@stock_api.get("/api/stocks/search/<string:symbol>/<string:market>")
@token_required
def search_stock(user_id, symbol, market):
    market = str(market).upper()
    stock_list = stock_service.TigerTrade.search_stock(symbol, market!="ALL", market)
    return result(200, "success", stock_list)

@stock_api.get("/api/stocks/price/<string:symbol>/<string:market>/<string:k_type>")
@token_required
def get_stock_price(user_id, symbol, market, k_type):
    stock_price_info = stock_service.TigerTrade.get_stock_price_info(symbol, market, k_type)
    return result(200, "success", stock_price_info)
