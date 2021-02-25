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

        #array for extra plot data
        self.test = []
        self.test1 = [np.NaN] * 49

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

            AM_candlesticks = self.ticker.getData("FULL")
            selected = AM_candlesticks[0:10]['close']
            #----------------------------------------------------------------------#
            #Add Running Logic Below
            coefficients, residuals, _, _, _ = np.polyfit(range(len(selected.index)),selected,1,full=True)
            mse = residuals[0]/(len(selected.index))
            nrmse = np.sqrt(mse)/(selected.max() - selected.min())
            print('Slope ' + str(coefficients[0]))
            print('NRMSE: ' + str(nrmse))

            test2 = [coefficients[0]*x + coefficients[1] for x in range(len(selected))]
            while len(test2) < 49:
                test2.append(np.NaN)

            test2.reverse()

            #Ensure that all the arrays are the same size before sending them to the plotter
            if len(self.test1) > 49:
                self.test1.pop(0)

            self.test = [self.test1, test2]

            if(self.inPosition):
                self.status = "In a Position. ID: " + self.tradeID

            else:
                self.status = "Running"

                #conditions that must be met to place a trade
                if 1:
                    #place a trade
                    volume = 10
                    trade = Trade(self.ticker.symbol, volume, self.tradeID, 1.01, self.ticker.AM_candlesticks.index[0], self.tradeapi, printInfo = True)
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

