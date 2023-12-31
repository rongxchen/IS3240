import os
import yahooquery as yq
import pandas as pd
import numpy as np
from models.model import session, Comparison
from services.stock_service_tiger_trade import search_stock, get_stock_price_list
from services.stock_service_helper import find_raw_csv_from_resource, find_from_resource
from general_config import resource_path

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

def find_financial_statements(symbol: str, market: str):
    path = os.path.join(resource_path, "excel", "financial_statements", f"{symbol}-{market}.xlsx")
    if not os.path.exists(path):
        if market == "HK":
            _symbol = symbol.lstrip("0")
        # initialize ticker
        ticker = yq.Ticker(symbol if market == "US" else f"{_symbol}.HK")
        # get three financials
        income_statement = ticker.income_statement().transpose()
        balance_sheet = ticker.balance_sheet().transpose()
        cash_flow_statement = ticker.cash_flow().transpose()
        # save it to file
        with pd.ExcelWriter(path) as writer:
            income_statement.to_excel(writer, sheet_name="income statement")
            balance_sheet.to_excel(writer, sheet_name="balance sheet")
            cash_flow_statement.to_excel(writer, sheet_name="cashflow statement")
    # return binary data and filename
    with open(path, "rb") as file:
        binary = file.read()
    return binary, path.split("\\")[-1]

def get_return(symbol, market, interval):
    get_stock_price(symbol, market, "D")
    df = find_raw_csv_from_resource(symbol, market, "D")
    key = f"{map_interval(interval)} return"
    returns = np.concatenate((np.array([0]), np.array([value for value in df[key].values if not np.isnan(value)]) * 100))
    dates = df["date"].values[-len(returns):]
    return [{"date": dates[i], "return": returns[i]} for i in range(len(dates))]

def map_interval(interval):
    return interval_map.get(interval, "1M")

indexes = [
    # {"symbol": ".DJI", "market": "US"},
    {"symbol": ".IXIC", "name": "NASDAQ", "market": "US", "color": "#c7a9a3"},
    {"symbol": ".SPX", "name": "SP500", "market": "US", "color": "#b3c5ad"},
    {"symbol": "HSI", "name": "HANG SENG", "market": "HK", "color": "#b29bc4"}
]
line_colors = [
    "#708090", # Slate Gray
    "#a89a8e", # Beige
    "#918151", # Taupe
    "#636363", # Charcoal
    "#8b8680", # Stone Gray
    "#4e4d4d", # Dim Gray
    "#7d7d7d", # Gray
    "#5e5d5d", # Dark Gray
    "#6f6e6e", # Medium Gray
    "#9c9c9c"  # Silver
]
interval_map = {"M": "1M", "3M": "3M", "1Y": "1Y"}
def get_index_return(interval):
    index_returns = []
    for stock_index in indexes:
        cumulative_return = get_return(stock_index["symbol"], stock_index["market"], interval)
        index_returns.append({
            "label": {"name": stock_index["name"], "symbol": stock_index["symbol"], "market": stock_index["market"]},
            "data": cumulative_return,
            "color": stock_index["color"]
        })
    return index_returns

def get_user_comparisons(user_id, interval):
    comparisons = session.query(Comparison).filter_by(user_id=user_id).all()
    comparison_returns = []
    count = 0
    for stock in comparisons:
        cumulative_return = get_return(stock.symbol, stock.market, interval)
        comparison_returns.append({
            "label": {"name": stock.name, "symbol": stock.symbol, "market": stock.market},
            "data": cumulative_return, "color": line_colors[count]
        })
        count += 1
    return comparison_returns

def save_comparison(user_id, symbol, name, market):
    comparison = Comparison(user_id, symbol, name, market)
    session.add(comparison)
    session.commit()

def remove_comparison(user_id, symbol):
    comparison = session.query(Comparison).filter_by(user_id=user_id, symbol=symbol).first()
    if not comparison:
        return False
    session.delete(comparison)
    session.commit()
    return True

def get_single_return(user_id, symbol, name, market, interval):
    length = session.query(Comparison).filter_by(user_id=user_id).count()
    cumulative_return = get_return(symbol, market, interval)
    save_comparison(user_id, symbol, name, market)
    return {
        "label": {"symbol": symbol, "name": name, "market": market},
        "data": cumulative_return, "color": line_colors[length]
    }

def find_comparison_from_db(user_id, symbol):
    return session.query(Comparison).filter_by(user_id=user_id, symbol=symbol).first()
