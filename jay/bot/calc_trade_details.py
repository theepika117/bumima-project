from settings import instrument_1, stop_loss, rounding_1, rounding_2, qty1_rounding, qty2_rounding
import math


def close_prices(prices):
    closing_prices = [candle[4] for candle in prices["list"] if not math.isnan(candle[4])]
    return closing_prices


def calc_trade_details(orderbook, direction="Long", capital=0):
    """Returns prices, stop loss / fail-safe and quantity"""
    mid_price, quantity, fail_safe = 0, 0, 0

    if orderbook:
        # Rounding the prices and quantities
        price_round = rounding_1 if orderbook["result"]["s"] == instrument_1 else rounding_2
        quantity_round = qty1_rounding if orderbook["result"]["s"] == instrument_1 else qty2_rounding

        # Organising prices
        bid_prices = [float(level[0]) for level in orderbook["result"]["b"]]
        ask_prices = [float(level[0]) for level in orderbook["result"]["a"]]

        # Calculating price, size, stop loss and average liquidity
        if bid_prices and ask_prices:
            bid_prices.sort(reverse=True)
            ask_prices.sort()
            nearest_ask = ask_prices[0]  # Getting the nearest ask
            nearest_bid = bid_prices[0]  # Getting the nearest bid

            if direction == "Long":
                mid_price = nearest_bid
                fail_safe = round(mid_price * (1 - stop_loss), price_round)
            else:
                mid_price = nearest_ask
                fail_safe = round(mid_price * (1 + stop_loss), price_round)

            quantity = round(capital / mid_price, quantity_round)

    return mid_price, fail_safe, quantity
