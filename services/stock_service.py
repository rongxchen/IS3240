from services.stock_service_tiger_trade import search_stock, get_stock_price_list
from services.stock_service_helper import find_from_resource

def search(symbol, by_market = False, market = "ALL"):
    symbol = str(symbol).upper()
    market = str(market).upper()
    return search_stock(symbol, by_market, market)

def get_stock_price(symbol, market, k_type):
    result = find_from_resource(symbol, market, k_type)
    if result:
        print("found in resource")
        return result
    symbol = str(symbol).upper()
    market = str(market).upper()
    k_type = str(k_type).upper()
    return get_stock_price_list(symbol, market, k_type)

def get_csv_binary(symbol, market, k_type):
    path = find_from_resource(symbol, market, k_type, for_download=True)
    with open(path, "rb") as file:
        binary = file.read()
    return binary
