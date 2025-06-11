import os
from dotenv import load_dotenv
from utils import calculate_cost, make_order
from flask import Flask
from flask import request
from werkzeug.middleware.proxy_fix import ProxyFix
from pybit.unified_trading import HTTP

app = Flask(__name__)

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

load_dotenv()

api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

api_key = os.getenv("DEMO_API_KEY")
api_secret = os.getenv("DEMO_API_SECRET")

session = HTTP(
        demo = True,
        api_key = api_key,
        api_secret = api_secret,
)

@app.route("/")
def hello_world():
    return "<h1>hello world</h1>"

@app.route("/get-balance")
def get_balance():
    return session.get_wallet_balance(
        accountType="UNIFIED",
        coin="USDT",
    )

@app.route("/alert-hook", methods=['POST'])
def alert_hook():
    try:
        data = request.json
    except:
        print("error during parsing")
    
    position = None
    side = None
    ticker = data["ticker"]

    if data["position"] == "open" and data["side"] == "long":
        position = False
        side = "Buy"
    elif data["position"] == "open" and data["side"] == "short":
        position = False
        side = "Sell"
    elif data["position"] == "close" and data["side"] == "long":
        position = True
        side = "Sell"
    elif data["position"] == "close" and data["side"] == "short":
        position = True
        side = "Buy"

    return make_order(session, side, position, ticker)

if __name__ == "__main__":
    app.run(debug=True)