from candlesticks import get_candles
import json


def store_data(symbols):
    """Stores the price history for all available symbols"""
    # Getting prices and storing in Dictionary
    price_history_dict = {}
    count = 0
    for symbol in symbols:
        symbol_name = symbol["symbol"]
        price_history = get_candles(symbol_name)
        count += 1
        if len(price_history) > 0:
            price_history_dict[symbol_name] = price_history
            print(f"{count} completed; {len(symbols) - count} remaining")
        else:
            print(f"{symbol_name} not saved; {len(symbols) - count} remaining")

    # Saving the data in JSON
    with open("data.json", "w") as file:
        json.dump(price_history_dict, file, indent=4)
    print("Price data saved successfully.")
