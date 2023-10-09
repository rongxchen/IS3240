import requests
import re
from datetime import datetime
from utils.http import get_headers
from general_config import tiger_token_path

headers = get_headers()

def obtain_TigerTrade_access_token():
    """ get a new access token from Tiger Trade if the token is expired
    :return: a new token / none
    """
    url = "https://www.laohu8.com/quotes"
    resp = requests.get(url=url, headers=get_headers())
    find_access_token = re.compile(r'"access_token":"(.*?)"')
    access_token = re.findall(find_access_token, resp.text)
    print(access_token)
    if len(access_token) > 0:
        with open(tiger_token_path, "w") as file:
            file.write(access_token[0])
        return True
    return False

class TigerTrade:
    __k_type = {
        "D": "day",
        "W": "week",
        "M": "month",
    }

    with open(tiger_token_path, "r") as file:
        access_token = "Bearer" + file.read()
    headers["Authorization"] = access_token

    retry = 0

    @staticmethod
    def reconfig_token():
        has_token = obtain_TigerTrade_access_token()
        if has_token:
            with open(tiger_token_path, "r") as file:
                token = file.read()
            TigerTrade.authorization_token = "Bearer " + token
            headers["Authorization"] = TigerTrade.authorization_token

    @staticmethod
    def search_stock(symbol, by_market = False, market = "ALL"):
        """ search for stocks by symbol and/or market
        :param symbol: stock symbol
        :param by_market: whether by market or not
        :param market: US / HK / ALL
        :return: a list of stocks
        """
        timestamp = int(datetime.now().timestamp() * 1000)
        url = "https://frontend-community.laohu8.com/search/v5/general?" \
              f"_s={timestamp}&lang=zh_CN&lang_content=cn&region=HKG&" \
              "deviceId=web-dd481837-24f3-4f54-8f2d-b2a9097&appVer=4.17.2&" \
              f"appName=laohu8&vendor=web&platform=web&edition=full&word={symbol}&market=US,HK"
        resp = requests.get(url=url, headers=headers)
        stock_list = []
        try:
            data = resp.json()["data"]["stockList"]
            if len(data) == 0 and TigerTrade.retry == 0:
                TigerTrade.reconfig_token()
                TigerTrade.retry += 1
                TigerTrade.search_stock(symbol, by_market, market)
                return
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
        return {
            "list": stock_list,
            "size": len(stock_list)
        }

    @staticmethod
    def __map_k_type(_type):
        if _type not in TigerTrade.__k_type:
            return TigerTrade.__k_type["D"]
        return TigerTrade.__k_type[_type]

    @staticmethod
    def get_stock_price_info(symbol, market, k_type):
        """ get stock price info including last price and historical price list
        :param symbol: stock symbol
        :param market: stock market
        :param k_type: k line type: D / W / M
        :return: stock detail (e.g., last price) + historical price list
        """
        timestamp = int(datetime.now().timestamp() * 1000)
        k_line = TigerTrade.__map_k_type(k_type)
        url = f"https://hq.laohu8.com/{'' if market == 'US' else 'hk_stock/'}stock_info/candle_stick/{k_line}/{symbol}?" \
              f"_s={timestamp}&lang=zh_CN&lang_content=cn&region=HKG&deviceId=web-dd481837-24f3-4f54-8f2d-b2a9097&appVer=4.17.2&" \
              "appName=laohu8&vendor=web&platform=web&edition=full&delay=true&manualRefresh=true"
        resp = requests.get(url=url, headers=headers)
        stock_price_info = {}
        try:
            data = resp.json()
            if "error" in data and data["error"] == "invalid_token" and TigerTrade.retry == 0:
                TigerTrade.reconfig_token()
                TigerTrade.retry += 1
                TigerTrade.get_stock_price_info(symbol, market, k_type)
                return
            details = data["detail"]
            stock_price_info["detail"] = {
                "last_price": details["adjPreClose"]
            }
            price_items = data['items']
            stock_price_info["price_list"] = []
            for price in price_items:
                stock_price_info["price_list"].append({
                    "date": datetime.fromtimestamp(price["time"] / 1000).date().strftime("%Y-%m-%d"),
                    "high": price["high"],
                    "open": price["open"],
                    "close": price["close"],
                    "low": price["low"],
                    "volume": price["volume"]
                })
        except Exception as e:
            print(f"exception: {e}")
        return stock_price_info

if __name__ == '__main__':
    stocks = TigerTrade.get_stock_price_info("BABA", "US", "d")
    print(stocks)
