from flask import Flask, render_template
from controllers.user_controller import user_api
from controllers.stock_controller import stock_api
from controllers.news_controller import news_api
from controllers.favourite_controller import favourite_api

app = Flask(__name__, static_folder="static")
app.register_blueprint(user_api)
app.register_blueprint(stock_api)
app.register_blueprint(news_api)
app.register_blueprint(favourite_api)

@app.get('/index')
def to_index():
    return render_template("index.html")

@app.get("/error/401")
def to_401():
    return render_template("error/401.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
