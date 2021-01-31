class Ticker:
    
    self.EMA10 = 0
    self.EMA20 = 0
    self.EMA50 = 0
    self.EMA200 = 0

    #Pandas Array for local data storage
    self.AM_candlesticks

    self.dayVolume
    self.avgVolume


    def __init__(self, ticker, type):
        self.ticker = ticker
        self.type = type  

    def updateArray(self):
        #This function will be run once the database recieves a new data point
        print("Update the local data array")

    def getCurrentPrice(self):
        #pull current price

    def checkData(self):
        #check to make sure the new point is actually differnt from the last

    def warmUp(self):
        #warm up indicators and complete initial fill of data array

    def  
