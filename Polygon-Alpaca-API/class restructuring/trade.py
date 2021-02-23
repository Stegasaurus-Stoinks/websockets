class Trade:
    
    #unique id so find trades that have been placed by this algo

    def __init__(self, symbol, volume, ID, openPrice, openTime, tradeapi, printInfo = False):
        self.symbol = symbol
        self.volume = volume
        self.ID = ID
        self.openPrice = openPrice
        self.openTime = openTime
        self.tradeapi = tradeapi
        self.printInfo = printInfo
        self.openPostion()
        


    def openPostion(self):
        #call funtion to open order through api

        #check if short or long position
        if self.volume > 0:
            self.tradeapi.SimpleBuy(self.symbol, self.volume)

        if self.volume < 0:
            self.tradeapi.SimpleSell(self.symbol, self.volume)

        self.status = True

        #print to console trade placement info if asked for it
        if self.printInfo:
            print("Opened a Postion! Bought " + str(self.volume) + " of " + self.symbol + " at time: " + str(self.openTime) + " | Trade ID: " + self.ID)



    def closePostion(self, closePrice, closeTime):
        self.closePrice = closePrice
        self.closeTime = closeTime

        #call funtion to close order through api
        
        if self.volume > 0:
            self.tradeapi.SimpleBuy(self.symbol, self.volume)

        if self.volume < 0:
            self.tradeapi.SimpleSell(self.symbol, self.volume)

        self.status = False

        if self.printInfo:
            print("Opened a Postion! Bought " + str(self.volume) + " of " + self.symbol + " Trade ID: " + self.ID)


    #return true or false whether we are in position or not
    def inPosition(self):
        return(self.status)