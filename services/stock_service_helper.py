import os
import pandas as pd
from datetime import datetime
from general_config import resource_path

required_headers = ["date", "open", "high", "low", "close", "volume"]

def find_returns(df: pd.DataFrame):
    columns = df.columns
    if "close" not in [c.lower() for c in columns]:
        return
    df["daily return"] = df["close"].pct_change()
    _1m_return = df["close"][-30:].pct_change()
    _3M_return = df["close"][-90:].pct_change()
    _1Y_return = df["close"][-365:].pct_change()
    df["cumulative return"] = (1 + df["daily return"]).cumprod() - 1
    df["1M return"] = (1 + _1m_return).cumprod() - 1
    df["3M return"] = (1 + _3M_return).cumprod() - 1
    df["1Y return"] = (1 + _1Y_return).cumprod() - 1

def find_raw_csv_from_resource(symbol, market, k_type):
    date = datetime.now().date().strftime("%Y%m%d")
    prefix = f"{symbol}-{market}-{k_type}"
    filename = f"{prefix}-{date}.csv"
    dir_path = os.path.join(resource_path, "csv", "stock_price")
    filepath = os.path.join(dir_path, filename)
    return pd.read_csv(filepath)

def find_from_resource(symbol, market, k_type, for_download=False):
    date = datetime.now().date().strftime("%Y%m%d")
    prefix = f"{symbol}-{market}-{k_type}"
    filename = f"{prefix}-{date}.csv"
    dir_path = os.path.join(resource_path, "csv", "stock_price")
    filepath = os.path.join(dir_path, filename)
    if os.path.exists(filepath):
        if for_download:
            return filepath
        df = pd.read_csv(filepath)
        return df_to_json(df)
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