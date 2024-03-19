from statsmodels.tsa.stattools import coint
import statsmodels.api as sm
import pandas as pd
import time

from settings import session, window, instrument_1, instrument_2
from calc_trade_details import calc_trade_details
from price_calls import candles


def calc_zscore(spread):
    """Calculates Z-Score using spread"""
    df = pd.DataFrame(spread)
    mean = df.rolling(center=False, window=window).mean()
    std = df.rolling(center=False, window=window).std()
    x = df.rolling(center=False, window=1).mean()
    df["ZSCORE"] = (x - mean) / std
    return df["ZSCORE"].astype(float).values


def calc_spread(series_1, series_2, hedge_ratio):
    """Calculates Spread"""
    spread = pd.Series(series_1) - (pd.Series(series_2) * hedge_ratio)
    return spread


def calc_coint(series_1, series_2):
    """Calculates Co-integration and returns Z-Score values"""
    coint_test = 0
    t_value, p_value, critical_value = coint(series_1, series_2)
    model = sm.OLS(series_1, series_2).fit()
    hedge_ratio = model.params[0]
    spread = calc_spread(series_1, series_2, hedge_ratio)
    zscore_list = calc_zscore(spread)
    if p_value < 0.5 and t_value < critical_value[1]:
        coint_test = 1
    return coint_test, list(zscore_list)


def z_score():
    """Calculates z-score of the two tickers based on mid-prices, using the latest order book data."""
    orderbook1 = session.get_orderbook(category="linear", symbol=instrument_1)
    mid_price_1, _, _, = calc_trade_details(orderbook1)

    time.sleep(0.5)  # To manage API calls

    orderbook2 = session.get_orderbook(category="linear", symbol=instrument_2)
    mid_price_2, _, _, = calc_trade_details(orderbook2)

    time.sleep(0.5)  # To manage API calls

    # Getting latest candles
    series_1, series_2 = candles()

    if len(series_1) > 0 and len(series_2) > 0:

        # Replacing last candle with latest mid-price from orderbook
        series_1 = series_1[:-1]
        series_2 = series_2[:-1]
        series_1.append(mid_price_1)
        series_2.append(mid_price_2)

        # Getting latest zscore
        _, zscore_list = calc_coint(series_1, series_2)
        zscore = zscore_list[-1]
        positive_signal = True if zscore > 0 else False

        return zscore, positive_signal
    return