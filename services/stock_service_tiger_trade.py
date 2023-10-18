import requests
import re
import os
import pandas as pd
from datetime import datetime
from utils.http import get_headers
from general_config import tiger_token_path, resource_path, remove_all_matched
from services.stock_service_helper import required_headers, find_returns

def obtain_TigerTrade_access_token():
    """ get a new access token from Tiger Trade if the token is expired
    :return: a new token / none
    """
    url = "https://www.laohu8.com/quotes"
    resp = requests.get(url=url, headers=get_headers())
    find_access_token = re.compile(r'"access_token":"(.*?)"')
    access_token = re.findall(find_access_token, resp.text)
    if len(access_token) > 0:
        write_token(access_token[0])
        return True
    return False

k_map = {"D": "day", "W": "week", "M": "month"}
def map_kline(k_type):
    return k_map[k_type] if k_type in k_map else k_map["D"]

def read_token():
    with open(tiger_token_path, "r") as file:
        authorization_token = "Bearer " + file.read()
    return authorization_token

headers = get_headers()
headers["Authorization"] = read_token()
retry = 0

def write_token(token):
    with open(tiger_token_path, "w") as file:
        file.write(token)

def reconfig_token():
    obtained = obtain_TigerTrade_access_token()
    if obtained:
        token = read_token()
        headers["Authorization"] = token

def search_stock(symbol, by_market = False, market = "ALL"):
    """ search for stocks by symbol and/or market
    :param symbol: stock symbol
    :param by_market: whether by market or not
    :param market: US / HK / ALL
    :return: a list of stocks
    """
    global retry
    timestamp = int(datetime.now().timestamp() * 1000)
    url = "https://frontend-community.laohu8.com/search/v5/general?" \
          f"_s={timestamp}&lang=zh_CN&lang_content=cn&region=HKG&" \
          "deviceId=web-dd481837-24f3-4f54-8f2d-b2a9097&appVer=4.17.2&" \
          f"appName=laohu8&vendor=web&platform=web&edition=full&word={symbol}&market=US,HK"
    resp = requests.get(url=url, headers=headers)
    stock_list = []
    try:
        data = resp.json()["data"]["stockList"]
        if len(data) == 0 and retry == 0:
            reconfig_token()
            retry += 1
            return search_stock(symbol, by_market, market)
        for stock in data:
            if (by_market and market != stock["market"]) or stock["type"] != 0:
                continue
            stock_list.append({
                "symbol": stock["symbol"],
                "name": stock["nameCN"],
                "market": stock["market"]
            })
    except Exception as e:
        print(f"exception: {e}")
    return {"list": stock_list,"size": len(stock_list)}

def get_stock_price_list(symbol, market, k_type):
    """ get stock price info including last price and historical price list
    :param symbol: stock symbol
    :param market: stock market
    :param k_type: k line type: D / W / M
    :return: stock detail (e.g., last price) + historical price list
    """
    global retry
    timestamp = int(datetime.now().timestamp() * 1000)
    k_line = map_kline(k_type)
    url = f"https://hq.laohu8.com/{'' if market == 'US' else 'hkstock/'}stock_info/candle_stick/{k_line}/{symbol}?" \
          f"_s={timestamp}&lang=zh_CN&lang_content=cn&region=HKG&deviceId=web-dd481837-24f3-4f54-8f2d-b2a9097&appVer=4.17.2&" \
          "appName=laohu8&vendor=web&platform=web&edition=full&delay=true&manualRefresh=true"
    resp = requests.get(url=url, headers=headers)
    price_list = []
    try:
        data = resp.json()
        if "error" in data and data["error"] == "invalid_token" and retry == 0:
            reconfig_token()
            retry += 1
            return get_stock_price_list(symbol, market, k_type)
        price_items = data['items']
        for price in price_items:
            price_list.append({
                "date": datetime.fromtimestamp(price["time"] / 1000).date().strftime("%Y-%m-%d"),
                "high": price["high"],
                "open": price["open"],
                "close": price["close"],
                "low": price["low"],
                "volume": price["volume"]
            })
        # save it as csv
        df = pd.DataFrame(price_list, columns=required_headers)
        find_returns(df, symbol, market, k_type)
        date = datetime.now().date().strftime("%Y%m%d")
        dir_path = os.path.join(resource_path, "csv", "stock_price")
        prefix = f"{symbol}-{market}-{k_type}"
        filepath = os.path.join(dir_path, f"{prefix}-{date}.csv")
        remove_all_matched(dir_path, prefix)
        df.to_csv(filepath, index=False)
    except Exception as e:
        print(f"exception: {e}")
    return price_list
