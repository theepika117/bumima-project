from pybit.unified_trading import HTTP

test = True
session = HTTP(testnet=test)

limit = 180
interval = 720

symbols = session.get_instruments_info(category="linear")
symbols = symbols["result"]["list"]


