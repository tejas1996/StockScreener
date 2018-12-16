import requests
import calcMovingAverage
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials
import datetime
from datetime import timedelta
import gspread
import json

def crawler():
    url = "https://www.quandl.com/api/v3/datasets/NSE/MINDAIND.json?&start_date=2018-10-01&end_date=2018-11-04"
    source = requests.get(url)
    text = source.text
    json_data = json.loads(text)
    print(json_data)
    stockdata = json_data['dataset']['data']
    print(text)
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('StockScreener-7a4b3e7ae834.json',scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key('1BJLD-NZYsaU8mFCyXjXCgnTAplV6u4OgCP5-nqRi1yA').sheet1
    stocks = sheet.get_all_records()
    print(stocks)
    count = 0
    for i in stockdata :
        count = count + 1
        sheet.insert_row(i,count)



def getTcikerData(ticker,days):
    # url = "https://www.quandl.com/api/v3/datasets/NSE/MINDAIND.json?&start_date=2018-10-01&end_date=2018-11-04"
    endDate = datetime.datetime.now().date().strftime("%Y-%m-%d")
    date_N_days_ago = datetime.datetime.now() - timedelta(days)
    startDate = date_N_days_ago.date().strftime("%Y-%m-%d")
    url = "https://www.quandl.com/api/v3/datasets/NSE/" + ticker + ".json?&start_date=" + startDate + "&end_date=" + endDate
    # print (url)
    source = requests.get(url)
    text = source.text
    json_data = json.loads(text)
    stockdata = json_data['dataset']['data']
    return stockdata


def storeForToday():

    tickers = ["MINDAIND","TATAMOTORS","PHILIPCARB","JSWSTEEL","AUROPHARMA"]
    count = 1
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('StockScreener-7a4b3e7ae834.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key('1BJLD-NZYsaU8mFCyXjXCgnTAplV6u4OgCP5-nqRi1yA').sheet1
    row = ["Stock","Open","High","Low","Last","Close","Quantity","Turnover (Lacs)"]
    sheet.insert_row(row, count)
    for ticker in tickers :
        # url = "https://www.quandl.com/api/v3/datasets/NSE/MINDAIND.json?&start_date=2018-10-01&end_date=2018-11-04"
        date = datetime.datetime.now().date().strftime("%Y-%m-%d")
        url = "https://www.quandl.com/api/v3/datasets/NSE/"+ ticker+ "?&start_date=2018-12-14&end_date=2018-12-14"
        # print (url)
        source = requests.get(url)
        text = source.text
        json_data = json.loads(text)
        stockdata = json_data['dataset']['data']
        count = count + 1
        for i in stockdata :
            i[0] =  ticker
            count = count + 1
            sheet.insert_row(i,count)





# getTcikerData("MINDAIND",3)
storeForToday();