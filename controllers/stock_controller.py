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
    """ search for stocks by symbol and market (market can be 'ALL')
    :param user_id: /
    :param symbol: symbol of the stock, e.g., for US: BABA, TSLA; for HK: 09988, 03690
    :param market: US / HK
    :return: a list of stock info
    """
    market = str(market).upper()
    stock_list = stock_service.TigerTrade.search_stock(symbol, market!="ALL", market)
    return result(200, "success", stock_list)

@stock_api.get("/api/stocks/price/<string:symbol>/<string:market>/<string:k_type>")
@token_required
def get_stock_price(user_id, symbol, market, k_type):
    """ get stock price list for given symbol, market and k line type
    :param user_id: /
    :param symbol: stock symbol
    :param market: stock market
    :param k_type: k line type: D (daily), W (weekly), M (monthly)
    :return: {"detail": {"last_price": }, "price_list": [...]}
    """
    market = str(market).upper()
    k_type = str(k_type).upper()
    stock_price_info = stock_service.TigerTrade.get_stock_price_info(symbol, market, k_type)
    return result(200, "success", stock_price_info)

@stock_api.post("/api/stocks/price/download")
@token_required
def download_price_data(user_id):
    """ download price data .xlsx
    :param user_id: /
    :return: binary data of Excel file for download
    """
    body = request.json
    symbol = body["symbol"]
    market = str(body["market"]).upper()
    k_type = str(body["k_type"]).upper()
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
