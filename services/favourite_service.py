import os
import numpy as np
import pandas as pd
from datetime import datetime
from general_config import resource_path
from services.stock_service_tiger_trade import get_stock_price_list
from caches.cache import asset_return_cache

def read_from_cache(symbol, market, days):
    key = f"{symbol}-{market}"
    if not key in asset_return_cache:
        return None
    close = asset_return_cache.get(key, np.array([]))
    if days < len(close):
        return calculate_cumulative_return(close[-days:])
    return calculate_cumulative_return(close)

def store_to_cache(symbol, market, data):
    key = f"{symbol}-{market}"
    asset_return_cache[key] = data

def calculate_cumulative_return(close: np.array):
    daily_returns = np.diff(close) / close[:-1]
    return (np.cumprod(1 + daily_returns) - 1)[-1]

def read_cumulative_returns(symbol, market, start_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    days = (datetime.now().date() - start.date()).days
    find_return = read_from_cache(symbol, market, days)
    if find_return:
        return find_return
    date = datetime.now().date().strftime("%Y%m%d")
    filename = f"{symbol}-{market}-D-{date}.csv"
    path = os.path.join(resource_path, "csv", "stock_price", filename)
    if not os.path.exists(path):
        get_stock_price_list(symbol, market, "D")
    df = pd.read_csv(path)
    closing = np.array(df["close"].to_list())
    close = closing[-days:]
    store_to_cache(symbol, market, closing)
    return calculate_cumulative_return(close)

