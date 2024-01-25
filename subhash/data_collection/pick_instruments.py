from setup import symbols


def instruments():
    trade_list = dict()
    for symbol in symbols:
        conditions = [symbol["status"] == "Trading", symbol["quoteCoin"] == "USDT"]
        if all(conditions):
            trade_list[symbol["symbol"]] = symbol
    # print(len(trade_list))
    return trade_list
