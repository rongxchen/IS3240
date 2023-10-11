import os
import pandas as pd
from datetime import datetime
from caches.cache import asset_return_cache
from general_config import resource_path, remove_all_matched

required_headers = ["date", "open", "high", "low", "close", "volume"]

def store_returns_to_cache(df: pd.DataFrame, symbol, market, k_type):
    key = f"{symbol}-{market}"
    if not symbol in asset_return_cache:
        asset_return_cache[key] = {}
    asset_return_cache[key][k_type] = df["cumulative return"].values

def find_returns(df: pd.DataFrame, symbol, market, k_type):
    columns = df.columns
    if "close" not in [c.lower() for c in columns]:
        return
    df["daily return"] = df["close"].pct_change()
    df["cumulative return"] = (1 + df["daily return"]).cumprod() - 1
    store_returns_to_cache(df, symbol, market, k_type)

def find_from_resource(symbol, market, k_type, for_download=False):
    date = datetime.now().date().strftime("%Y%m%d")
    prefix = f"{symbol}-{market}-{k_type}"
    filename = f"{prefix}-{date}.csv"
    dir_path = os.path.join(resource_path, "csv", "stock_price")
    filepath = os.path.join(dir_path, filename)
    if os.path.exists(filepath):
        df = pd.read_csv(filepath)
        store_returns_to_cache(df, symbol, market, k_type)
        return filepath if for_download else df_to_json(df)
    remove_all_matched(dir_path, prefix)
    return None

def convert_to_base_type(value):
    if str(value).isnumeric():
        return float(value)
    return value

def df_to_json(df: pd.DataFrame):
    price_list = []
    length = len(df["date"])
    for i in range(length):
        price_list.append({header: convert_to_base_type(df[header].values[i]) for header in required_headers})
    return price_list
