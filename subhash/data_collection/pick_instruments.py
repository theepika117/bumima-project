from setup import symbols


def instruments():
    trade_list = dict()
    file = open("Available Instruments.txt", "w")
    for symbol in symbols:
        conditions = [symbol["status"] == "Trading", symbol["quoteCoin"] == "USDT"]
        if all(conditions):
            trade_list[symbol["symbol"]] = symbol
            file.write(symbol["symbol"] + "\n")
    file.close()
    return trade_list
