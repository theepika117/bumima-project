from pick_instruments import instruments
from store_data import store_data
from cointegration import cointegrated_pairs
import json

if __name__ == "__main__":
    #
    # # Getting all available symbols
    # print("Fetching available instruments...")
    # response = instruments()
    #
    # # Saving price history data
    # print(f"Successfully fetched {len(response)} total symbols")
    # print("Constructing and saving price data in JSON...")
    # if len(response) > 0:
    #     store_data(response.values())

    # Getting Co-integrated pairs
    print("Calculating co-integration...")
    with open("data.json") as file:
        price_data = json.load(file)
        if len(price_data) > 0:
            pairs = cointegrated_pairs(price_data)

