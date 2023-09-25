import os
from functools import wraps
from flask import Flask, render_template, request
from models import user
from utils import jwt_util
from services import stock_price, financial_news

app = Flask(__name__, static_folder="static")
db_name = os.getcwd() + "/sqlite3.db"

def result(code: int, message: str, data: any = None):
    return {
        "code": code,
        "data": data,
        "message": message
    }

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers["Authorization"]
        if not token:
            return result(403, "unauthorized")
        verified, username = jwt_util.verify_token(token)
        if not verified:
            return result(403, "unauthorized")
        return f(username, *args, **kwargs)
    return decorator

"""
pages
"""
@app.route('/index', methods=["GET"])
def to_index():
    return render_template("index.html")

"""
users
"""
@app.route("/api/users", methods=["POST"])
def login():
    body = request.get_json()
    username = body["username"]
    password = body["password"]
    is_login = user.login(username, password)
    if is_login:
        token = jwt_util.get_token(username)
        return result(200, "login ok", token)
    return result(401, "wrong username or password")

@app.route("/api/users/register", methods=["POST"])
def register():
    body = request.get_json()
    username = body["username"]
    password = body["password"]
    is_registered, msg = user.register(username, password)
    if is_registered:
        return result(200, msg)
    return result(400, msg)

@app.route("/api/users", methods=["PUT"])
@token_required
def change_password(username):
    body = request.get_json()
    password = body["password"]
    new_password = body["new_password"]
    password_changed, msg = user.change_password(username, password, new_password)
    if password_changed:
        return result(200, msg)
    return result(400, msg)

@app.route("/api/users", methods=["DELETE"])
@token_required
def delete_account(username):
    user.delete_user(username)
    return result(200, "success")

"""
stocks
"""
@app.route("/api/stocks/price/<symbol>")
def get_stock_price(symbol):
    price_list = stock_price.get_stock_price(symbol, 1)
    if not price_list:
        return result(400, "no such data")
    return result(200, "stock price fetched", price_list)

"""
news
"""
@app.route("/api/news/<int:page>/<int:size>", methods=["GET"])
def get_news_list(page, size):
    news_list = financial_news.from_reuters(page, size)
    return result(200, "success", news_list)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
