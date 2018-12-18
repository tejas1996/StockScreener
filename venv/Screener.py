# create universes (indices)
# create download entire universe from quantdl (data for all stocks in index)
# daily - download nse eod prices and update old data 
# daily - calculate all required indicators 
# daily - push all indicators to a csv file 
# daily - push csv to google sheets - already done 

# import calcMovingAverage
# from bs4 import BeautifulSoup
# from oauth2client.service_account import ServiceAccountCredentials
# import gspread
import datetime
import json, os, datetime, requests
from datetime import datetime, timedelta
from nsepy.history import get_price_list
import pandas as pd 

class Screener:

    universe = None
    data = None

    # constructor
    def __init__(self, universe):
        # load universe 
        path = ".\\venv\\indices\\%s.csv" % (universe)
        print(path)
        if os.path.exists(path):
            self.universe = pd.read_csv(path, header=0)
        else : 
            raise Exception("Universe not found")

    def run(self):
        # load universe - done
        # for each stock in universe 
            # download quantdl data - done
            # download latest stock eod data - done 
            # merge eod data with quantdl csvs 
            # calculate indicators and save all data to dataFrame 
            # save entire dataframe as csv with date 
            # upload to sheets 
        pass

    # upload processed csv/dataframe to sheets 
    def uploadToSheets(self, parameter_list):
        pass

    def calculateIndicators(self, parameter_list):
        # may be use talib directly or any similar library 
        pass
    
    # get eod data from nse using nsepy 
    def getEodData(self):
        return get_price_list(dt=datetime.today())

    # get stock history from quantdl 
    def getHistory(self, symbol, begin, end, frequency="daily", forceUpdate=False, authToken=None):
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
                "collapse": frequency
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
    # begin = today - timedelta(days=30)
    # screener.getHistory("mindaind", begin.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'))