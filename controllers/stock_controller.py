import os
import pandas as pd
from datetime import datetime
from services import stock_service
from general_config import result, token_required, resource_path
from flask import Blueprint, make_response, request

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

@stock_api.post("/api/stocks/price/download")
@token_required
def download_price_data(user_id):
    body = request.json
    symbol = body["symbol"]
    market = body["market"]
    k_type = body["k_type"]
    date = "".join(datetime.now().strftime("%Y-%m-%d").split("-"))
    # join the path
    path = os.path.join(resource_path, "excel", "stock_price")
    file_name = f"{symbol}-{market}-{k_type}-{date}.xlsx"
    # check if the path directory exists
    if not os.path.exists(path):
        os.makedirs(path)
    path = os.path.join(path, file_name)
    # if the price.xlsx does not exist, create a new one
    if not os.path.exists(path):
        price_data = stock_service.TigerTrade.get_stock_price_info(symbol, market, k_type)["price_list"]
        df = pd.DataFrame(price_data)
        df.to_excel(path, index=False)
        print("data not exist, creating...")
    # read the binary data
    with open(path, "rb") as file:
        binary = file.read()
    # send to frontend in response body
    response = make_response(binary)
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = f'attachment; filename="{file_name}"'
    return response
