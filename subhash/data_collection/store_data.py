from candlesticks import get_candles
import json


def store_data(symbols):
    """Stores the price history for all available symbols"""
    price_history = {}
    count = 0
    # Getting prices and storing in Dictionary
    for symbol in symbols:
        symbol_name = symbol["symbol"]
        prices = get_candles(symbol_name)
        count += 1
        if len(prices) > 0:
            price_history[symbol_name] = prices
            print(f"{count} completed; {len(symbols) - count} remaining")
        else:
            print(f"{symbol_name} not saved; {len(symbols) - count} remaining")

    # Saving the data in JSON
    if len(price_history) > 0:
        with open("data.json", "w") as file:
            json.dump(price_history, file, indent=4)
        print("Price data saved successfully.")
    return
