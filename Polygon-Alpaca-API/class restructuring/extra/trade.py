class Trade:
    
    #unique id so find trades that have been placed by this algo

    def __init__(self, symbol, volume, ID, openPrice, openTime, direction, tradeapi, printInfo = False):
        self.symbol = symbol
        self.volume = volume
        self.ID = ID
        self.openPrice = openPrice
        self.openTime = openTime
        self.direction = direction
        self.tradeapi = tradeapi
        self.printInfo = printInfo
        self.openPosition()
        


    def openPosition(self):
        #call funtion to open order through api

        #check if short or long position
        if self.volume > 0:
            self.tradeapi.SimpleBuy(self.symbol, self.volume)

        if self.volume < 0:
            self.tradeapi.SimpleSell(self.symbol, self.volume)

        self.position = True
        self.status = "Open"

        #print to console trade placement info if asked for it
        if self.printInfo:
            print("______________________________________________________________________")
            print("Opened a Postion! Bought " + str(self.volume) + " of " + self.symbol + " at time: " + str(self.openTime) + " | Trade ID: " + self.ID)
            print("______________________________________________________________________")


    def closePosition(self, closePrice, closeTime):
        self.closePrice = closePrice
        self.closeTime = closeTime

        #call funtion to close order through api
        
        if self.volume > 0:
            self.tradeapi.SimpleBuy(self.symbol, self.volume)

        if self.volume < 0:
            self.tradeapi.SimpleSell(self.symbol, self.volume)

        self.position = False
        self.status = "Closed"

        if self.printInfo:
            print("______________________________________________________________________")
            print("Closed a Postion! Sold " + str(self.volume) + " of " + self.symbol + " Trade ID: " + self.ID)
            print("______________________________________________________________________")

    def fakeOpen(self):

            self.position = True
            self.status = "Open"

            #print to console trade placement info if asked for it
            if self.printInfo:
                print("______________________________________________________________________")
                print("Opened a fake Postion! Bought " + str(self.volume) + " of " + self.symbol + " at time: " + str(self.openTime) + " | Trade ID: " + self.ID)
                print("______________________________________________________________________")


    def fakeClose(self, closePrice, closeTime):
        self.closePrice = closePrice
        self.closeTime = closeTime

        self.position = False
        self.status = "Closed"

        if self.printInfo:
            print("Closed a fake Postion! Sold " + str(self.volume) + " of " + self.symbol + " Trade ID: " + self.ID)
    #return true or false whether we are in position or not
    def inPosition(self):
        return(self.position)

    def getStatus(self):
        return(self.status)

    def getStats(self, display = False):

        PL = self.closePrice - self.openPrice
        if self.direction == "DOWN":
            PL = PL*(-1)
        duration = self.closeTime - self.openTime
        
        if(display):
            print("---------Trade Stats---------")
            print("Open Price: ",self.openPrice)
            print("Close Price: ",self.closePrice)
            print("P/L: ",PL)
            print(" ")
            print("Open Time: ",self.openTime)
            print("Close Time: ",self.closeTime)
            print("Direction: ",self.direction)
            print(" ")
            print("Duration: ",duration)

        d = dict(); 
        d['openPrice'] = self.openPrice
        d['closePrice']   = self.closePrice
        d['PL']   = PL
        d['openTime']   = self.openTime
        d['closeTime']   = self.closeTime
        d['duration']   = duration

        return(d)