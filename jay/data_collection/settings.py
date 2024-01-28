from pybit.unified_trading import HTTP

test = True
session = HTTP(testnet=test)

limit = 1000  # Number of candles
interval = 120  # Length of a candle's data in minutes
window = 60  # Z Score using the average of last n candles; Higher value for less volatility

symbols = session.get_instruments_info(category="linear")
if symbols["retMsg"] == "OK":
    symbols = symbols["result"]["list"]
