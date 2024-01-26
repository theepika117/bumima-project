import math

import pandas as pd
import numpy as np

from statsmodels.tsa.stattools import coint
import statsmodels.api as sm


# Calculating Z-Score
def calc_zscore(series, window_size):
    mean = series.rolling(window=window_size).mean()
    std = series.rolling(window=window_size).std()
    zscore = (series - mean) / std
    return zscore


# Calculating Spread
def calc_spread(series_1, series_2, hedge_ratio):
    spread = series_1 - (series_2 * hedge_ratio)
    return spread


# Calculating Co-integration
def cointegration(series_1, series_2):
    coint_test = 0
    t_value, p_value, critical_value = coint(series_1, series_2)
    model = sm.OLS(series_1, series_2).fit()  # To calculate the hedge ratio
    hedge_ratio = model.params.iloc[0]
    spread = calc_spread(series_1, series_2, hedge_ratio)
    zero_crossings = len(np.where(np.diff(np.sign(spread)))[0])
    if p_value < 0.5 and t_value < critical_value[1]:
        coint_test = 1
    return (coint_test, round(p_value, 2), round(t_value, 2),
            round(critical_value[1], 2), round(hedge_ratio, 2), zero_crossings)


# Extracting close prices from the data
def close_prices(prices):
    closing_prices = [float(candle[4]) for candle in prices["list"] if not math.isnan(float(candle[4]))]
    return closing_prices


# Calculating Cointegrated Pairs
def cointegrated_pairs(prices):
    pairs = []
    included_list = []

    for symbol_1 in prices.keys():
        for symbol_2 in prices.keys():
            if symbol_2 != symbol_1:
                sorted_characters = sorted(symbol_1 + symbol_2)
                unique = "".join(sorted_characters)
                if unique in included_list:
                    continue

                series_1 = pd.Series(close_prices(prices[symbol_1]))
                series_2 = pd.Series(close_prices(prices[symbol_2]))

                coint_test, p_value, t_value, c_value, hedge_ratio, zero_crossings = cointegration(series_1, series_2)
                if coint_test == 1:
                    included_list.append(unique)
                    pairs.append({
                        "instrument-1": symbol_1,
                        "instrument-2": symbol_2,
                        "p-value": p_value,
                        "t-value": t_value,
                        "c-value": c_value,
                        "hedge_ratio": hedge_ratio,
                        "zero_crossings": zero_crossings
                    })

    coint_df = pd.DataFrame(pairs).sort_values("zero_crossings", ascending=False)
    coint_df.to_csv("co-integrated_pairs.csv", index=False)
    return coint_df
