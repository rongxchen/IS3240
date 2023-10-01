import requests
from datetime import datetime
from utils.http import get_headers

headers = get_headers()

class TigerTrade:
    __k_type = {
        "D": "day",
        "W": "week",
        "M": "month",
    }

    authorization_token = "Bearer eyJhbGciOiJFUzI1NiIsImtpZCI6IjVVQzB5NGhnUXUiLCJ0eXAiOiJKV1QifQ.eyJleHAiOjE2OTg2MDYwNjIsImlzcyI6IkNITiIsIm5vbmNlIjoiQ0p3TWZzbGtCek9UNmdtMDZNQ2NEdTY1MXVNTkZzSU53aVFhbVZHeTlmRjg4aFNsUnoifQ.4QmAfXXm_IQjix-wURSaWn9qw4S5OC44_BVoXVIcetmr_cSomBNrAJE4RKVstX450gSvTUf2zugE-VKWe78tgA"
    headers["Authorization"] = authorization_token

    @staticmethod
    def search_stock(symbol, by_market = False, market = "ALL"):
        timestamp = int(datetime.now().timestamp() * 1000)
        url = "https://frontend-community.laohu8.com/search/v5/general?" \
              f"_s={timestamp}&lang=zh_CN&lang_content=cn&region=HKG&" \
              "deviceId=web-dd481837-24f3-4f54-8f2d-b2a9097&appVer=4.17.2&" \
              f"appName=laohu8&vendor=web&platform=web&edition=full&word={symbol}&market=US,HK"
        resp = requests.get(url=url, headers=headers)

        stock_list = []
        try:
            data = resp.json()["data"]["stockList"]
            for stock in data:
                if (by_market and market != stock["market"]) or stock["type"] != 0:
                    continue
                stock_list.append({
                    "symbol": stock["symbol"],
                    "name": stock["nameCN"],
                    "market": stock["market"]
                })
        except Exception as e:
            print(e)
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
    def get_stock_price_info(keyword, market, k_type):
        keyword = str(keyword).upper()
        market = str(market).upper()
        k_type = str(k_type).upper()
        timestamp = int(datetime.now().timestamp() * 1000)
        k_line = TigerTrade.__map_k_type(k_type)
        url = f"https://hq.laohu8.com/{'' if market == 'US' else 'hk_stock/'}stock_info/candle_stick/{k_line}/{keyword}?" \
              f"_s={timestamp}&lang=zh_CN&lang_content=cn&region=HKG&" \
              "deviceId=web-dd481837-24f3-4f54-8f2d-b2a9097&appVer=4.17.2&" \
              "appName=laohu8&vendor=web&platform=web&edition=full&delay=true&manualRefresh=true"
        resp = requests.get(url=url, headers=headers)

        stock_price_info = {}
        try:
            data = resp.json()
            details = data["detail"]
            stock_price_info["detail"] = {
                "last_price": details["adjPreClose"]
            }
            price_items = data['items']
            stock_price_info["price_list"] = []
            for price in price_items:
                stock_price_info["price_list"].append({
                    "high": price["high"],
                    "open": price["open"],
                    "close": price["close"],
                    "low": price["low"],
                    "volume": price["volume"],
                    "date": datetime.fromtimestamp(price["time"] / 1000).date().strftime("%Y-%m-%d")
                })
        except Exception as e:
            print(e)
        return stock_price_info
