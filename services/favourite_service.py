from models.model import Favourite, session
from sqlalchemy import desc, text
from datetime import datetime
from services.stock_service import get_stock_price

def find_cur_price(symbol, market):
    stock_price = get_stock_price(symbol, market, "D")
    return stock_price[-1]["date"], stock_price[-1]["close"]

def find_if_exists(user_id, symbol, market):
    return session.query(Favourite).filter_by(user_id=user_id, symbol=symbol, market=market).first()

def add_or_remove_favourite(user_id, symbol, market):
    favourite = find_if_exists(user_id, symbol, market)
    if favourite:
        session.delete(favourite)
        session.commit()
        return
    _, cur_price = find_cur_price(symbol, market)
    timestamp = int(datetime.now().timestamp())
    date = datetime.now().date().strftime('%Y-%m-%d')
    favourite = Favourite(user_id, symbol, market, date, timestamp, cur_price, cur_price)
    session.add(favourite)
    session.commit()

def update_quantity(user_id, symbol, market, quantity):
    favourite = find_if_exists(user_id, symbol, market)
    if not favourite:
        return None
    favourite.quantity = quantity
    session.add(favourite)
    session.commit()
    return get_favourite_by_symbol(user_id, symbol)

def update_current_price(user_id):
    favourites = session.query(Favourite).filter_by(user_id=user_id).order_by(desc("timestamp")).all()
    for favourite in favourites:
        _, cur_price = find_cur_price(favourite.symbol, favourite.market)
        params = {"user_id": user_id, "cur_price": cur_price, "symbol": favourite.symbol, "market": favourite.market}
        session.execute(text("update favourites set current_price = :cur_price "
                        "where user_id = :user_id and symbol = :symbol and market = :market"), params)
        session.commit()

def get_favourites(user_id):
    update_current_price(user_id)
    favourites = session.query(Favourite).filter_by(user_id=user_id).all()
    return [{
        "symbol": favourite.symbol, "market": favourite.market, "added_date": favourite.added_date,
        "cost": favourite.cost, "current_price": favourite.current_price, "timestamp": favourite.timestamp,
        "return": round((favourite.current_price - favourite.cost) * favourite.quantity, 3), "quantity": favourite.quantity,
        "return_rate": round((favourite.current_price / favourite.cost - 1) * 100, 3)
    } for favourite in favourites]

def get_favourite_by_symbol(user_id, symbol):
    favourite = session.query(Favourite).filter_by(user_id=user_id, symbol=symbol).first()
    return {
        "symbol": favourite.symbol, "market": favourite.market, "added_date": favourite.added_date,
        "cost": favourite.cost, "current_price": favourite.current_price, "timestamp": favourite.timestamp,
        "return": round((favourite.current_price - favourite.cost) * favourite.quantity, 3), "quantity": favourite.quantity,
        "return_rate": round((favourite.current_price/favourite.cost-1) * 100, 3)
    } if favourite else None
