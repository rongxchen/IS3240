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
    stock_list = stock_service.search(symbol, market!="ALL", market)
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
    stock_price = stock_service.get_stock_price(symbol, market, k_type)
    return result(200, "success", stock_price)

# @stock_api.post("/api/stocks/price/download")
# @token_required
# def download_price_data(user_id):
#     """ download price data .xlsx
#     :param user_id: /
#     :return: binary data of Excel file for download
#     """
#     body = request.json
#     symbol = body["symbol"]
#     market = str(body["market"]).upper()
#     k_type = str(body["k_type"]).upper()
#     date = "".join(datetime.now().strftime("%Y-%m-%d").split("-"))
#     # join the path
#     dir_path = os.path.join(resource_path, "csv", "stock_price")
#     prefix = f"{symbol}-{market}-{k_type}"
#     file_name = f"{prefix}-{date}.xlsx"
#     # check if the path directory exists
#     if not os.path.exists(dir_path):
#         os.makedirs(dir_path)
#     path = os.path.join(dir_path, file_name)
#     # if the price.xlsx does not exist, create a new one
#     if not os.path.exists(path):
#         remove_all_matched(dir_path, prefix)
#         price_data = stock_service.TigerTrade.get_stock_price_info(symbol, market, k_type)["price_list"]
#         df = pd.DataFrame(price_data)
#         df.to_excel(path, index=False)
#         print("data not exist, creating...")
#     # read the binary data
#     with open(path, "rb") as file:
#         binary = file.read()
#     # send to frontend in response body
#     response = make_response(binary)
#     response.headers['Content-Type'] = 'application/octet-stream'
#     response.headers['Content-Disposition'] = f'attachment; filename="{file_name}"'
#     return response
