import pandas as pd 
from datetime import datetime, timedelta

class Ticker:

    def __init__(self, symbol, type, Database):
        self.symbol = symbol
        self.type = type
        self.status = "Not Initialized"
        
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
        #print("Update the local data array")
        self.Last_time = self.Current_time

        data = self.queryNewData()
        self.Checked_data = self.checkData(data)
        #add to local AM_candlesticks
        self.AM_candlesticks.append(Checked_data)

        self.Current_time = 



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

        data = self.DataBase.QueryLast(self.symbol, 50)
        #Pandas Array for local data storage
        self.AM_candlesticks = pd.DataFrame(data)
        self.AM_candlesticks.columns = ['time','symbol','volume','day_volume','day_open','vwap','open','high','close','low','avg','unix']
        self.AM_candlesticks['datetime'] = pd.to_datetime(self.AM_candlesticks['time'])
        self.AM_candlesticks = self.AM_candlesticks.set_index('datetime')
        self.AM_candlesticks.drop(['time'], axis=1, inplace=True)

        self.status = "Initialized"



    def getData(self):
        #return entire data array
        return(self.AM_candlesticks)



    def getCurrentData(self):
        #pull current price for specific type
        return(self.Checked_data)



    def getStatus(self):
        #print(self.AM_candlesticks.head())
        return self.status
        



    def addTrade(self):
        print("Trade recorded")
        #function will add trade to trade list which will then be sent to database, or maybe just send the newest trade? idk