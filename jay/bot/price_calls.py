from settings import session, instrument_1, instrument_2, interval, limit
from calc_trade_details import close_prices
import datetime
import time


def timestamps():
    time_start_date = 0
    now = datetime.datetime.now()
    if isinstance(interval, int):
        time_start_date = now - datetime.timedelta(hours=limit)
    if interval == "D":
        time_start_date = now - datetime.timedelta(days=limit)
    time_start_seconds = int(time_start_date.timestamp())
    time_now_seconds = int(now.timestamp())
    return time_start_seconds, time_now_seconds


def get_candles(ticker):
    """Fetches and Returns candle data for a given ticker from the API"""
    time_start_seconds, _ = timestamps()
    prices = session.get_mark_price_kline(
        category="linear",
        symbol=ticker,
        interval=interval,
        limit=limit,
        start=time_start_seconds
    )

    # To manage API calls
    time.sleep(0.1)

    if len(prices["result"]["list"]) != limit:
        return []
    return prices["result"]


def candles():
    series_1 = []
    series_2 = []
    prices_1 = get_candles(instrument_1)
    prices_2 = get_candles(instrument_2)
    if len(prices_1) > 0:
        series_1 = close_prices(prices_1)
    if len(prices_2) > 0:
        series_2 = close_prices(prices_2)
    return series_1, series_2


def liquidity(ticker):
    """Calculates average liquidity of a given ticker over the past 30 intervals"""
    # Getting trade history by API call
    trades = session.get_public_trade_history(
        category="linear",
        symbol=ticker,
        limit=30,
    )

    qty_list = []  # Formatted response data
    if "result" in trades.keys():
        for trade in trades["result"]["list"]:
            qty_list.append(float(trade["size"]))

    # Calculating and returning the average liquidity value
    if len(qty_list) > 0:
        avg_liq = sum(qty_list) / len(qty_list)
        latest_price = float(trades["result"]["list"][0]["price"])
        return avg_liq, latest_price
    return 0, 0