from trade import Trade
from datetime import datetime
from plotter import LiveChartEnv

import pandas as pd
import numpy as np

class Algo:
    
    #unique id so find trades that have been placed by this algo

    def __init__(self, ticker, name, risklevel, tradeapi, live, plotting = True):
        self.ticker = ticker
        self.name = name
        self.risklevel = risklevel
        self.tradeapi = tradeapi
        self.live = live
        self.plotting = plotting

        self.tradeID = name + ticker.symbol + str(risklevel)
        self.type = ticker.type
        self.inPosition = False
        self.status = "Initialized"

        #array for extra plot data
        self.test = []
        self.test1 = [np.NaN] * 49
        self.test2 = [np.NaN] * 49
        #print(self.test)

        #initialize plot if plot variable is true
        if(self.plotting):
            self.plotInit()

        #-----------STATS------------
        self.goodTrades = 0
        self.badTrades = 0
        self.totalProfit = 0
        #----------------------------

    def update(self):
        #This function will be run once the database recieves a new data point
        #all the logic that is checked to see if you need to buy or sell should be in this function

        #print("Run Algo Update Loop using data from " + self.ticker.symbol)
        #print("Trades placed will have the ID: " + self.tradeID)

        #creating df for extra plot data for plotter

        avg1 = self.ticker.getData("FULL")['close'].mean()
        avg2 = self.ticker.getData("FULL")[0:20]['close'].mean()  
        self.test1.append(avg1)
        self.test2.append(avg2)
        if len(self.test1) >= 49:
            self.test1.pop(0)
        if len(self.test2) >= 49:
            self.test2.pop(0)

        self.test = [self.test1,self.test2]

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
                self.inPosition = True

        #update plot if plot is true
        if self.plotting:
            self.plot.update_chart(self.ticker.getData("FULL"), self.test)

    def Statistics(self):
        print("This will print all of the statistics of the algo")
        #will probably need to connect to the database to find all that data, but not rn
        print("Good Trades: " + str(self.goodTrades) + "/" + str(self.goodTrades + self.badTrades))
        print("Total Profit: " + str(self.totalProfit))

    def getStatus(self):
        return(self.status)
        #return(self.ticker.status)

    def plotInit(self):
        self.plot = LiveChartEnv("1min", 50)
        self.plot.initialize_chart()

