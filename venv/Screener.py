# Ta-Lib can be downloaded for windows 64 bit from - https://www.lfd.uci.edu/~gohlke/pythonlibs/
# Download package and run pip install TA_Lib-0.4.17-cp37-cp37m-win_amd64.whl (cp37 is cpython 3.7)
# On linux it should be simple pip install TA-Lib

# import calcMovingAverage
# from bs4 import BeautifulSoup
# from oauth2client.service_account import ServiceAccountCredentials
# import gspread
import datetime
import json, os, requests
from datetime import date, datetime, timedelta
from nsepy.history import get_price_list
import pandas as pd 
import talib
from ta import *
import numpy as np

class Screener:

    universe = None
    # data = None

    # constructor
    def __init__(self, universe):
        # load universe 
        path = ".\\venv\\indices\\%s.csv" % (universe)
        if os.path.exists(path):
            self.universe = pd.read_csv(path, header=0)
        else : 
            raise Exception("Universe not found")
        
        # data = pd.DataFrame()

    def run(self):
        eodData = self.getEodData() # get todays EOD data date(2018, 12, 28)
        eodData = eodData.drop(['SERIES'], axis=1)
        report = pd.DataFrame()
        today = datetime.today()
        begin = today - timedelta(days=300)
        end = today - timedelta(days=1)
        for index, row in self.universe.iterrows(): # process universe 
            # merge eod data with universe 
            last = eodData.loc[eodData["SYMBOL"]==row["Symbol"]]
            last = last.assign(COMPANYNAME=row['Company Name'], INDUSTRY=row['Industry'])
            symbol = last['SYMBOL'].values[0]
            symbol = symbol.replace('-', '_')
            
            # get quandl data from 
            history = self.getHistory(symbol, begin, end)
            indicators = self.calculateIndicators(history)
            latestIndicators = indicators.tail(1) # take only last row 
            # finalRow = pd.concat([last, latestIndicators], axis = 1)
            
            lastColumns = last.columns.values
            lastValues = last.values[0]
            indiColumns = latestIndicators.columns.values
            indiValues = latestIndicators.values[0]

            columns = np.concatenate((lastColumns, indiColumns))
            values = np.concatenate((lastValues, indiValues))
            finalRow = dict(zip(columns, values))

            # merge with reports dataframe 
            report = report.append(finalRow, sort=False, ignore_index=True)
            report = report[columns]

        # store as csv 
        outPath = ".\\venv\\reports\\report-%s.csv" % (date.today().strftime("%Y-%m-%d"))
        report.to_csv(outPath)

    # upload processed csv/dataframe to sheets 
    def uploadToSheets(self, parameter_list):
        pass

    def calculateIndicators(self, timeseries):
        indicators = pd.DataFrame()
        close = timeseries['Close']
        high = timeseries['High']
        low = timeseries['Low']
        open1 = timeseries['Open']
        last = timeseries['Last']

        indicators['sma10'] = talib.SMA(close, timeperiod=10)
        indicators['sma50'] = talib.SMA(close, timeperiod=50)
        indicators['sma200'] = talib.SMA(close, timeperiod=200)
        indicators['ema9'] = talib.EMA(close, timeperiod=9)
        indicators['ema21'] = talib.EMA(close, timeperiod=21)
        bbupper, bbmiddle, bblower = talib.BBANDS(close, timeperiod=14, nbdevup=2, nbdevdn=2, matype=0)
        indicators['bbupper'] = bbupper
        indicators['bblower'] = bblower
        indicators['bbp'] = (last - bblower) / (bbupper-bblower)
        indicators['adx'] = talib.ADX(high, low, close, timeperiod=14)
        indicators['atr'] = talib.ATR(high, low, close, timeperiod=14)
        macd, macdsignal, macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
        indicators['macd'] = macd
        indicators['macdsignal'] = macdsignal
        indicators['roc'] = talib.ROC(close, timeperiod=14)
        indicators['rsi'] = talib.RSI(close, timeperiod=14)
        indicators['dojiCandle'] = talib.CDLDOJI(open1, high, low, close)
        indicators['beta'] = talib.BETA(high, low, timeperiod=30)
        indicators['stddev'] = talib.STDDEV(close, timeperiod=14, nbdev=1)
        indicators['dcUpper'] = donchian_channel_hband(close, n=20, fillna=False)
        indicators['dcLower'] = donchian_channel_lband(close, n=20, fillna=False)

        return indicators
    
    # get eod data from nse using nsepy 
    def getEodData(self, dt=None):
        if dt is None: 
            dt = date.today()
        return get_price_list(dt=dt)

    # get stock history from quantdl 
    def getHistory(self, symbol, begin, end, frequency="daily", forceDownload=False, authToken=None):
        # check if file already exists 
        storage = ".\\venv\\history"
        if not os.path.exists(storage):
            print("Creating %s directory" % (storage))
            os.mkdir(storage)

        csvFile = os.path.join(storage, "%s-quandl.csv" % (symbol))
        if not os.path.exists(csvFile) or forceDownload:
            print("Cache file not found downloading from quandl")
            url = "http://www.quandl.com/api/v1/datasets/NSE/%s.csv" % (symbol)
            params = {
                "trim_start": begin,
                "trim_end": end,
                "collapse": frequency,
                "order": "asc"
                # "rows": 300
            }
            
            if authToken is not None:
                params["auth_token"] = authToken
        
            response = requests.get(url, params=params)
            ret = response.text

            f = open(csvFile, "w+")
            f.write(ret)
            f.close()
        # return pandas data frame loaded with data file 
        return pd.read_csv(csvFile, header=0)

if __name__ == "__main__":
    screener = Screener("ind_test")
    # today = datetime.today()
    # begin = today - timedelta(days=300)
    # end = today - timedelta(days=1)
    # history = screener.getHistory('ASIANPAINT', begin, end)
    # indicators = screener.calculateIndicators(history)

    screener.run()
    # today = datetime.today()
    # begin = today - timedelta(days=30)
    # screener.getHistory("mindaind", begin.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'))