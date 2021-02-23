import pandas as pd 
from datetime import datetime, timedelta
import time

class Ticker:

    def __init__(self, symbol, type, Database):
        self.symbol = symbol
        self.type = type
        self.status = "Not Initialized"
        
        #local array size
        self.ArraySize = 50
        #backtest length minus the local array size
        self.length = 500
        #iteration to keep track of backtest
        self.iteration = 0
        #for timing the backtest
        self.start_time = 0
        self.end_time = 0

        #idk if these are gonna be calculated here yet
        self.EMA10 = 0
        self.EMA20 = 0
        self.EMA50 = 0
        self.EMA200 = 0

        #This object will be the only one communicating with the database
        self.DataBase = Database

        self.tradeList = pd.DataFrame()

        self.dayVolume = 0
        self.avgVolume = 0

        self.Current_time = datetime(2020, 11, 18, 18, 30, 0)
        self.Last_time = datetime(2020, 11, 18, 18, 30, 0)

        self.Data_errors = 0



    #main update function
    def update(self):
        """Call this Function to update the local data array with new data from database or backtest data"""
        #print("Update the local data array")
        self.Last_time = self.Current_time


        #Update for BACKTEST Data
        if self.DataBase.BackTest:
            if self.start_time == 0:
                self.start_time = time.time()

            self.iteration += 1
            #print("Update local array with backtest data")
            self.AM_candlesticks = self.BackTestAM_candlesticks.iloc[self.length-self.ArraySize-self.iteration:self.length-1-self.iteration]
            if self.iteration >= self.length-self.ArraySize:
                self.end_time = time.time()
                print("Backtesting Complete!")
                print("Backtesting " + str(self.length-self.ArraySize) + " points took " + str(self.end_time-self.start_time) + " seconds")
                quit()


        #Update for LIVE Data
        else:
            data = self.queryNewData()
            self.Checked_data = self.checkData(data)
            print(self.Checked_data[0])

            series = pd.Series(self.Checked_data[0][1:], index = self.AM_candlesticks.columns, name=self.Checked_data[0][0])

            self.AM_candlesticks = self.AM_candlesticks.append(series)
            self.AM_candlesticks = self.AM_candlesticks.sort_index(ascending=False)



    def queryNewData(self):
        print("call query function for specific type")
        data = self.DataBase.QueryLast(self.symbol, 1)
        return data



    def checkData(self, data):
        print("check to make sure the new point is actually differnt from the last")
        if 1: #Check if new timestamp is not equal to last time
            return(data)

        else:
            self.Data_errors += 1
            print("Possible data collection error | " + str(self.Data_errors))
            #Need to change timestamp to one minute ahead, but keep rest of the data.  This will help fill in missing data
            modified_data = data
            return(modified_data) 



    def warmUp(self):
        #warm up indicators and complete initial fill of data array
        print("Warm Up " + self.symbol)

        #Update for BACKTEST Data
        if self.DataBase.BackTest:
            #length of backtest
            data = self.DataBase.QueryLast(self.symbol, self.length)
            self.BackTestAM_candlesticks = pd.DataFrame(data)
            self.BackTestAM_candlesticks.columns = ['time','symbol','volume','day_volume','day_open','vwap','open','high','close','low','avg','unix']
            self.BackTestAM_candlesticks['datetime'] = pd.to_datetime(self.BackTestAM_candlesticks['time'])
            self.BackTestAM_candlesticks = self.BackTestAM_candlesticks.set_index('datetime')
            self.BackTestAM_candlesticks.drop(['time'], axis=1, inplace=True)

            self.AM_candlesticks = self.BackTestAM_candlesticks.iloc[self.length-self.ArraySize:self.length-1]

        #Update for LIVE Data
        else:
            data = self.DataBase.QueryLast(self.symbol, self.ArraySize)
            #Pandas Array for local data storage
            self.AM_candlesticks = pd.DataFrame(data)
            self.AM_candlesticks.columns = ['time','symbol','volume','day_volume','day_open','vwap','open','high','close','low','avg','unix']
            self.AM_candlesticks['datetime'] = pd.to_datetime(self.AM_candlesticks['time'])
            self.AM_candlesticks = self.AM_candlesticks.set_index('datetime')
            self.AM_candlesticks.drop(['time'], axis=1, inplace=True)


        self.status = "Initialized"



    def getData(self, type = "LAST"):
        """
        Pull current price for asset
        3 Options for type
        - LAST - Returns the single most recent data point (Default)
        - HEAD - Returns the last 5 data points
        - FULL - Returns the entire data array
        """
        if type == "LAST":
            return(self.AM_candlesticks.iloc[0])

        if type == "HEAD":
            return(self.AM_candlesticks.head())

        if type == "FULL":
            return(self.AM_candlesticks)



    def getStatus(self):
        #print(self.symbol + " is @ " + str(self.AM_candlesticks.iloc[0]['close']))
        #print(self.AM_candlesticks.tail())
        return self.status
        


    def addTrade(self):
        print("Trade recorded - Well not really this method still need to be implemented")
        #function will add trade to trade list which will then be sent to database, or maybe just send the newest trade? idk