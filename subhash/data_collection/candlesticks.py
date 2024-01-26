from setup import session, interval, limit
import datetime
import time

# Getting start times
start_date = 0
if isinstance(interval, int):
    start_date = datetime.datetime.now() - datetime.timedelta(hours=limit)
if interval == "D":
    start_date = datetime.datetime.now() - datetime.timedelta(days=limit)
start_seconds = int(start_date.timestamp())


def get_candles(symbol):
    # Getting price candles
    candles = session.get_mark_price_kline(
        symbol=symbol, category="linear", interval=interval, limit=limit, start=start_seconds
    )

    # In order to manage API call limit issues
    time.sleep(0.1)

    return candles["result"] if len(candles["result"]["list"]) == limit else []
