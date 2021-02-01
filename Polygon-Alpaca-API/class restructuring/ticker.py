class Ticker:

    def __init__(self, symbol, type):
        self.symbol = symbol
        self.type = type
        self.status = "Not Initialized"
        self.EMA10 = 0
        self.EMA20 = 0
        self.EMA50 = 0
        self.EMA200 = 0

        #Pandas Array for local data storage
        self.AM_candlesticks = []

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