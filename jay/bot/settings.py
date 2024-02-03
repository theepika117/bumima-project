from pybit.unified_trading import HTTP
import pandas as pd
import os

test = 1
testnet = [os.environ.get("bybit_key"), os.environ.get("bybit_private")]
mainnet = [os.environ.get("key_bybit"), os.environ.get("private_bybit")]

key, private = testnet if test else mainnet

limit = 1000  # Number of candles
interval = 120  # Length of a candle's data in minutes
window = 60  # To calculate Z-Score

pairs_data = pd.read_csv("../data_collection/co-integrated_pairs.csv")
rank = 18  # rank of the pair to be traded
instrument_1 = pairs_data.iloc[rank - 1]['Instrument-1']
instrument_2 = pairs_data.iloc[rank - 1]['Instrument-2']
overvalued = instrument_2
undervalued = instrument_1
rounding_1, rounding_2 = 5, 3
qty1_rounding, qty2_rounding = 2, 2

capital = 1000  # total capital allocated to be split between both pairs in USD
stop_loss = 0.20
trigger = 1.1  # z-score value at which order is placed

session = HTTP(testnet=test)
session_private = HTTP(testnet=test, api_key=key, api_secret=private)
