from trade import Trade
from datetime import datetime
from plotter import LiveChartEnv

import pandas as pd
import numpy as np

class Algo:
    
    #unique id so find trades that have been placed by this algo

    def __init__(self, ticker, name, risklevel, tradeapi, live, plotting = False):
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

        self.highest = 0
        self.stoploss = 0

        #array for extra plot data
        self.test = []
        self.test1 = [np.NaN] * 49
        self.test2 = [np.NaN] * 49
        self.test3 = [np.NaN] * 49
        self.entry = [np.NaN] * 49
        self.exit = [np.NaN] * 49
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
        if self.ticker.validTradingHours == True:

            current_data = self.ticker.getData()

            #SMA calcs
            avg1 = self.ticker.getData("FULL")['close'].mean()
            avg2 = self.ticker.getData("FULL")[0:20]['close'].mean()

            self.test1.append(avg1)
            self.test2.append(avg2)

            #SMA Crossing Logic
            if avg1 > avg2 and self.highest != 1:
                num = current_data['close']*1.001
                self.test3.append(num)
                self.highest = 1
                self.entry = [current_data['close']] * 49
                self.inPosition = True 

            if avg2 > avg1 and self.highest != 2:
                num = current_data['close']*0.999
                self.test3.append(num)
                self.highest = 2
                self.entry = [current_data['close']] * 49
                self.inPosition = True 

            if len(self.test3) == 49:
                #print("else")
                self.test3.append(np.NaN)

            #Set Exit Price based on if its an up or down trade (both set to same at the moment..)
            if self.inPosition == True:
                if self.highest == 1:
                    self.exit = [current_data['close']] * 49

                if self.highest == 2:
                    self.exit = [current_data['close']] * 49


            #Ensure that all the arrays are the same size before sending them to the plotter
            if len(self.test1) > 49:
                self.test1.pop(0)
            if len(self.test2) > 49:
                self.test2.pop(0)
            if len(self.test3) > 49:
                self.test3.pop(0)
            if len(self.entry) > 49:
                self.entry.pop(0)
            if len(self.exit) > 49:
                self.exit.pop(0)

            self.test = [self.test1,self.test2,self.test3, self.entry, self.exit]

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


        #if not valid Trading hours...
        else:
            if self.plotting:
                #update just the candles on the chart
                self.plot.update_chart(self.ticker.getData("FULL"))




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

