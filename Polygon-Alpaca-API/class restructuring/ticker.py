import pandas as pd 

class Ticker:

    def __init__(self, symbol, type, Database):
        self.symbol = symbol
        self.type = type
        self.status = "Not Initialized"
        self.EMA10 = 0
        self.EMA20 = 0
        self.EMA50 = 0
        self.EMA200 = 0

        #This object will be the only one communicating with the database
        self.DataBase = Database

        #Pandas Array for local data storage
        self.AM_candlesticks = pd.DataFrame()
        self.tradeList = []

        self.dayVolume = 0
        self.avgVolume = 0

    #main update function
    def update(self):
        #print("Update the local data array")
        self.queryNewData()
        self.checkData()
        #add to local AM_candlesticks

    def queryNewData(self):
        print("call query function for specific type")

    def checkData(self):
        print("check to make sure the new point is actually differnt from the last")

    def warmUp(self):
        #warm up indicators and complete initial fill of data array

        
        print("Warm Up " + self.symbol)
        self.status = "Initialized"

    def getCurrentPrice(self):
        #pull current price for specific type
        print("")

    def getStatus(self):
        return self.status

    def addTrade(self):
        print("Trade recorded")
        #function will add trade to trade list which will then be sent to database, or maybe just send the newest trade? idk