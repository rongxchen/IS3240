from functools import wraps
from flask import Flask, render_template, request
from utils import jwt_util
from general_config import result
from controllers.user_controller import user_api
from controllers.stock_controller import stock_api

app = Flask(__name__, static_folder="static")
app.register_blueprint(user_api)
app.register_blueprint(stock_api)

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers["Authorization"]
        if not token:
            return result(403, "unauthorized")
        verified, resp = jwt_util.verify_token(token)
        if not verified:
            return result(403, f"unauthorized: {resp}")
        return f(resp, *args, **kwargs)
    return decorator

@app.get('/index')
def to_index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
