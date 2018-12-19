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
        eodData = self.getEodData() # get todays EOD data 
        eodData = eodData.drop(['SERIES'], axis=1)
        report = pd.DataFrame()
        for index, row in self.universe.iterrows(): # process universe 
            # merge eod data with universe 
            last = eodData.loc[eodData["SYMBOL"]==row["Symbol"]]
            last = last.assign(COMPANYNAME=row['Company Name'], INDUSTRY=row['Industry'])
            
            # get quandl data from 
            today = datetime.today()
            begin = today - timedelta(days=300)
            end = today - timedelta(days=1)
            history = self.getHistory(last['SYMBOL'], begin, end)
            indicators = self.calculateIndicators(history)

            # merge with reports dataframe 
            report = report.append(last, sort=False)

        # store as csv 
        outPath = ".\\venv\\reports\\report-%s.csv" % (date.today().strftime("%Y-%m-%d"))
        report.to_csv(outPath)

        # merge eod data with quantdl csvs 
        # calculate indicators and save all data to dataFrame 
        # upload to sheets 

    # upload processed csv/dataframe to sheets 
    def uploadToSheets(self, parameter_list):
        pass

    def calculateIndicators(self, timeseries):
        print(timeseries)
        pass
    
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
    today = datetime.today()
    begin = today - timedelta(days=300)
    end = today - timedelta(days=1)
    history = screener.getHistory('ASIANPAINT', begin, end)
    indicators = screener.calculateIndicators(history)

    # screener.run()
    # today = datetime.today()
    # begin = today - timedelta(days=30)
    # screener.getHistory("mindaind", begin.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'))