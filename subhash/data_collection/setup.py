from pybit.unified_trading import HTTP

test = True
session = HTTP(testnet=test)

limit = 1000
interval = 120

symbols = session.get_instruments_info(category="linear")
if symbols["retMsg"] == "OK":
    symbols = symbols["result"]["list"]

