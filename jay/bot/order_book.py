from settings import session, instrument_1, instrument_2

orderbook = [session.get_orderbook(category="linear", symbol=instrument_1, limit=200),
             session.get_orderbook(category="linear", symbol=instrument_2, limit=200)]
