import os
from flask import Flask
from flask_cors import CORS
from controllers.user_controller import user_api
from controllers.stock_controller import stock_api
from controllers.news_controller import news_api
from controllers.favourite_controller import favourite_api
from services.news_service import sync_news
from general_config import resource_path, remove_under
from waitress import serve

app = Flask(__name__, static_folder="static")
app.register_blueprint(user_api)
app.register_blueprint(stock_api)
app.register_blueprint(news_api)
app.register_blueprint(favourite_api)

CORS(app)


if __name__ == '__main__':
    # remove all outdated stock price csv files
    stock_csv_path = os.path.join(resource_path, "csv", "stock_price")
    remove_under(stock_csv_path)
    # sync news data
    sync_news()
    serve(app, host="0.0.0.0")
