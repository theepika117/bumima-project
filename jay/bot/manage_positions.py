from settings import overvalued, undervalued, session_private


def position_info(ticker):
    """Returns information on positions, if present, of the specified ticker"""
    side = 0
    size = ""
    position = session_private.get_positions(category="linear", symbol=ticker)
    if "retMsg" in position.keys() and position["retMsg"] == "OK":
        if int(position["result"]["list"][0]["size"]) > 0:
            size = int(position["result"]["list"][0]["size"])
            side = position["result"]["list"][0]["side"]
        else:
            size = int(position["result"]["list"][0]["size"])
            side = "Sell"

    return side, size


def close_position(ticker, side, size):
    """Closes a position immediately by placing a market order"""

    session_private.place_order(
        category="linear",
        symbol=ticker,
        side=side,
        orderType="Market",
        qty=size,
        reduceOnly=True,
    )
    return


def exit_all_positions():
    """Closes all the existing positions and cancels any pending orders"""
    session_private.cancel_all_orders(category="linear", symbol=overvalued, settleCoin="USDT")
    session_private.cancel_all_orders(category="linear", symbol=undervalued, settleCoin="USDT")

    side_1, size_1 = position_info(overvalued)
    side_2, size_2 = position_info(undervalued)

    if size_1 > 0:
        close_position(overvalued, side_2, size_1)

    if size_2 > 0:
        close_position(undervalued, side_1, size_2)
    return
