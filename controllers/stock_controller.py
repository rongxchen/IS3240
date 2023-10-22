from services import stock_service
from general_config import result, token_required
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
    stock_list = stock_service.search(symbol, market)
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

@stock_api.post("/api/stocks/price/download")
@token_required
def download_price_data(user_id):
    """ download price data .xlsx
    :param user_id: /
    :return: binary data of Excel file for download
    """
    body = request.json
    symbol = str(body["symbol"]).upper()
    market = str(body["market"]).upper()
    k_type = str(body["k_type"]).upper()
    binary, filename = stock_service.get_csv_binary(symbol, market, k_type)
    # send to frontend in response body
    if binary and filename:
        response = make_response(binary)
        response.headers['Content-Type'] = 'application/octet-stream'
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    return result(400, "error")

@stock_api.get("/api/stocks/return/index/<string:interval>")
@token_required
def get_default_indexes_returns(user_id, interval):
    interval = str(interval).upper()
    data = stock_service.get_index_return(interval) + stock_service.get_user_comparisons(user_id, interval)
    if not data:
        return result(400, "failed")
    return result(200, "success", data)

@stock_api.post("/api/stocks/return")
@token_required
def get_single_return(user_id):
    body = request.json
    symbol = str(body["symbol"]).upper()
    interval = str(body["interval"]).upper()
    stocks = stock_service.search(symbol, "ALL")
    for stock in stocks["list"]:
        if stock["symbol"] == symbol:
            data = stock_service.get_single_return(user_id, stock["symbol"], stock["name"], stock["market"], interval)
            return result(200, "success", data)
    return result(400, "no such stock")

@stock_api.delete("/api/stocks/return")
@token_required
def remove_comparison(user_id):
    body = request.json
    symbol = str(body["symbol"]).upper()
    removed = stock_service.remove_comparison(user_id, symbol)
    if removed:
        return result(200, "success")
    return result(400, "failed")
