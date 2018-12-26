from datetime import date, datetime, timedelta
# from nsepy.history import get_price_list
import pandas as pd 
import numpy as np
import talib
import matplotlib.pyplot as plt
from ta import *

# path = ".\\venv\\indices\\ind_test.csv" 
# universe = pd.read_csv(path)

path2 = ".\\venv\\history\\ASIANPAINT-quandl.csv" 
eod = pd.read_csv(path2, header=0)
# eod = eod.drop(['SERIES', 'Unnamed: 13'], axis=1)

close = eod['Close']
high = eod['High']
low = eod['Low']
open1 = eod['Open']
last = eod['Last']

sma10 = talib.SMA(close, timeperiod=10)
# sma50 = talib.SMA(close, timeperiod=50)
# sma200 = talib.SMA(close, timeperiod=200)
# ema9 = talib.EMA(close, timeperiod=9)
# ema21 = talib.EMA(close, timeperiod=21)
# upper, middle, lower = talib.BBANDS(close, timeperiod=14, nbdevup=2, nbdevdn=2, matype=0)
# bbp = (last - lower) / (upper-lower)
# adx = talib.ADX(high, low, close, timeperiod=14)
# atr = talib.ATR(high, low, close, timeperiod=14)
# macd, macdsignal = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
# roc = talib.ROC(close, timeperiod=14)
# rsi = talib.RSI(close, timeperiod=14)
dojiCandle = talib.CDLDOJI(open1, high, low, close)
beta = talib.BETA(high, low, timeperiod=30)
stddev = talib.STDDEV(close, timeperiod=14, nbdev=1)

upper = donchian_channel_hband(close, n=20, fillna=False)
lower = donchian_channel_lband(close, n=20, fillna=False)

indicators = pd.DataFrame()
indicators['dcUpper'] = upper
indicators['dcLower'] = lower
indicators['sma10'] = sma10
indicators['beta'] = beta
indicators['stddev'] = stddev

result = pd.concat([eod, indicators], axis = 1)
print(result.tail(1))


# ta source - https://technical-analysis-library-in-python.readthedocs.io/en/latest/ta.html#momentum-indicators
# plt.plot(close, label='close')
# plt.plot(upper, label='upper')
# plt.plot(lower, label='lower')
# # plt.plot(middle, label='middle')
# # plt.xlabel('x label')
# # plt.ylabel('y label')
# plt.title("Simple Plot")
# plt.legend()
# plt.show()

# data = pd.DataFrame()
# print(data)

# print(universe.columns.values)
# print(eod.columns.values)

# print(eod.columns.values + universe.columns.values)

# for i, row in universe.iterrows():
#     list1 = eod.loc[eod['SYMBOL'] == row['Symbol']]
#     list1 = list1.assign(Company=row['Company Name'], Industry=row['Industry'])
#     # list1 = list1.to_dict(orient='records')
#     # list1[0]['Company Name'] = row['Company Name']
#     # list1[0]['Industry'] = row['Industry']
#     # print(list1)
#     data = data.append(list1, sort=False)

# print(data)


