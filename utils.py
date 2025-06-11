import math

def round_down(number, decimals):
    factor = 10 ** decimals
    return math.floor(number * factor) / factor

def calculate_cost(ticker, session):
    json_data = session.get_wallet_balance(
        accountType="UNIFIED",
        coin="USDT",
    )
    value = json_data["result"]["list"][0]["totalWalletBalance"]

    #json_data = session.get_tickers(
        #category="linear",
        #symbol="BTCUSDT",
    #)
    #price = json_data["result"]["list"][0]["lastPrice"]
    price = ticker

    cost = (float(value)*20)*0.95/float(price)
    return str(round_down(cost, 3))

def make_order(session, side, position, ticker):
    if position:
        qty = 1
    else:
        qty = calculate_cost(ticker, session)

    return session.place_order(
        category="linear",
        symbol="BTCUSDT",
        side=side,
        orderType="Market",
        qty=qty,
        reduce_only=position,
    )