from trade import Trade
from datetime import datetime

class Algo:
    
    #unique id so find trades that have been placed by this algo

    def __init__(self, ticker, name, risklevel, tradeapi, live):
        self.ticker = ticker
        self.name = name
        self.risklevel = risklevel
        self.tradeapi = tradeapi
        self.live = live

        self.tradeID = name + ticker.symbol + str(risklevel)
        self.type = ticker.type
        self.inPosition = False
        self.status = "Initialized"

        #-----------STATS------------
        self.goodTrades = 0
        self.badTrades = 0
        self.totalProfit = 0
        #----------------------------

    def update(self):
        #This function will be run once the database recieves a new data point
        #all the logic that is checked to see if you need to buy or sell should be in this function
        print("Run Algo Update Loop using data from " + self.ticker.symbol)
        print("Trades placed will have the ID: " + self.tradeID)

        if(self.inPosition):
            self.status = "In a Position. ID: " + self.tradeID

        else:
            self.status = "Running"
            time = datetime.now()

            #conditions that must be met to place a trade
            if 1:
                #place a trade
                volume = 10
                trade = Trade(self.ticker.symbol, volume, self.tradeID, 1.01, time, self.tradeapi, printInfo = True)
                print("The trade is " + trade.getStatus())

    def Statistics(self):
        print("This will print all of the statistics of the algo")
        #will probably need to connect to the database to find all that data, but not rn
        print("Good Trades: " + str(self.goodTrades) + "/" + str(self.goodTrades + self.badTrades))
        print("Total Profit: " + str(self.totalProfit))

    def getStatus(self):
        return(self.status)
        #return(self.ticker.status)

