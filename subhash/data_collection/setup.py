from pybit.unified_trading import HTTP

test = True
session = HTTP(testnet=test)

limit = 300
interval = 60

symbols = session.get_instruments_info(category="linear")
if symbols["retMsg"] == "OK":
    symbols = symbols["result"]["list"]

