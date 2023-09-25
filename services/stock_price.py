import requests
from datetime import datetime, timedelta

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}

def search_stock(symbol):
    url = f"https://api.nasdaq.com/api/autocomplete/slookup/10?search={symbol}"
    resp = requests.get(url=url, headers=headers)

    stock_list = []
    try:
        data = resp.json()["data"]
        if not data:
            return None
        for stock in data:
            if stock["asset"] != "STOCKS":
                continue
            stock_list.append({
                "symbol": stock["symbol"], "name": stock["name"], "exchange": stock["exchange"]
            })
    except Exception as e:
        print(e)
    return stock_list

if __name__ == '__main__':
    search_stock("msft")

def get_stock_price(symbol, years = 3):
    today = datetime.now().date()
    start = today - timedelta(days=365 * years)
    url = f"https://api.nasdaq.com/api/quote/{symbol}/chart?assetclass=stocks&fromdate={start}&todate={today}"

    resp = requests.get(url=url, headers=headers)
    price_list = []
    try:
        data = resp.json()["data"]
        if not data:
            return None
        chart = data["chart"]
        for price in chart:
            z = price["z"]
            price_list.append({
                "open": float(z["open"]), "high": float(z["high"]), "low": float(z["low"]),
                "close": float(z["close"]), "volume": float(z["volume"].replace(",", "")),
                "date": str(datetime.strptime(z["dateTime"], "%m/%d/%Y")).split()[0]
            })
    except Exception as e:
        print(e)
    return price_list
