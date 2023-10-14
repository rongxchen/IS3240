from services.stock_service_tiger_trade import search_stock, get_stock_price_list
from services.stock_service_helper import find_from_resource

def search(symbol, market = "ALL"):
    symbol = str(symbol).upper()
    market = str(market).upper()
    return search_stock(symbol, market != "ALL", market)

def get_stock_price(symbol, market, k_type):
    symbol = str(symbol).upper()
    market = str(market).upper()
    k_type = str(k_type).upper()
    result = find_from_resource(symbol, market, k_type)
    if result:
        return result
    symbol = str(symbol).upper()
    market = str(market).upper()
    k_type = str(k_type).upper()
    return get_stock_price_list(symbol, market, k_type)

def get_csv_binary(symbol, market, k_type):
    symbol = str(symbol).upper()
    market = str(market).upper()
    k_type = str(k_type).upper()
    try:
        path = find_from_resource(symbol, market, k_type, for_download=True)
        if path:
            with open(path, "rb") as file:
                binary = file.read()
            return binary, path.split("\\")[-1]
    except Exception as e:
        print(f"exception: {e}")
    return None, None
