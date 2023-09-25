from functools import wraps
from flask import Flask, render_template, request
from utils import jwt_util, cipher
from services import stock_price_service, financial_news_service
from config import db_path
from models import User, db

app = Flask(__name__, static_folder="static")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
db.init_app(app)

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
    body = request.json
    username = body["username"]
    password = body["password"]
    user = User.query.filter_by(username=username).first()
    if user is None:
        return result(400, "no such user")
    _password = cipher.md5_encrypt(password)
    if user.password == _password:
        token = jwt_util.get_token(username)
        return result(200, "success", token)
    return result(400, "wrong username or password")

@app.route("/api/users/register", methods=["POST"])
def register():
    body = request.json
    username = body["username"]
    password = body["password"]
    # search for username first
    find = User.query.filter_by(username=username).first()
    if not find is None:
        return result(400, "username already exists")
    user = User(username, cipher.md5_encrypt(password))
    db.session.add(user)
    db.session.commit()
    return result(200, "success")

@app.route("/api/users", methods=["PUT", "DELETE"])
@token_required
def manipulate_account(username):
    if request.method == "PUT":
        password = request.json["password"]
        new_password = request.json["new_password"]
        if password == new_password:
            return result(400, "new password cannot be the same as the old one")
        # check if the user is authorized to change his/her password
        user = User.query.filter_by(username=username, password=cipher.md5_encrypt(password)).first()
        if user is None:
            return result(400, "no such user")
        # md5 encrypt the new password
        user.password = cipher.md5_encrypt(password)
        db.session.add(user)
        db.session.commit()
        print(User.query.all())
        return result(200, "success")
    user = User.query.filter_by(username=username).first()
    if user is None:
        return result(400, "no such user")
    db.session.delete(user)
    db.session.commit()
    return result(200, "success")


"""
stocks
"""
@app.route("/api/stocks/price/<symbol>")
def get_stock_price(symbol):
    price_list = stock_price_service.get_stock_price(symbol, 1)
    if not price_list:
        return result(400, "no such data")
    return result(200, "stock price fetched", price_list)


"""
news
"""
@app.route("/api/news/<int:page>/<int:size>", methods=["GET"])
def get_news_list(page, size):
    news_list = financial_news_service.from_reuters(page, size)
    return result(200, "success", news_list)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
