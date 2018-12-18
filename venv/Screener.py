# create universes (indices)
# create download entire universe from quantdl (data for all stocks in index)
# daily - download nse eod prices and update old data 
# daily - calculate all required indicators 
# daily - push all indicators to a csv file 
# daily - push csv to google sheets - already done 

class Screener:
    def function(self):
        print("this is a screener class")

    def uploadToSheets(self, parameter_list):
        pass

    def calculateIndicators(self, parameter_list):
        pass
    
    def getEodData(self, parameter_list):
        pass

    def getHistory(self, parameter_list):
        # get stock history from quantdl 
        pass