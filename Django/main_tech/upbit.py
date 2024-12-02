import pyupbit

df = pyupbit.get_ohlcv("KRW-BTC", count=30, interval="day")
print(df)