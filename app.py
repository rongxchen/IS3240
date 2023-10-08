from flask import Flask, render_template
from controllers.user_controller import user_api
from controllers.stock_controller import stock_api
from controllers.news_controller import news_api

app = Flask(__name__, static_folder="static")
app.register_blueprint(user_api)
app.register_blueprint(stock_api)
app.register_blueprint(news_api)

@app.get('/index')
def to_index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
