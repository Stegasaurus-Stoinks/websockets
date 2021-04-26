from trade import Trade
from datetime import datetime
from plotter import LiveChartEnv


import pandas as pd
import numpy as np

class Algo:
    
    #unique id so find trades that have been placed by this algo

    def __init__(self, ticker, name, risklevel, tradeapi, live, plotting = False, plotSize = 50):
        self.ticker = ticker
        self.name = name
        self.risklevel = risklevel
        self.tradeapi = tradeapi
        self.live = live
        self.plotting = plotting
        self.plotSize = plotSize

        self.tradeID = name + ticker.symbol + str(risklevel)
        self.type = ticker.type
        self.inPosition = False
        self.status = "Initialized"


        #---------Algo Sepcific Variables--------
        self.highest = 0
        self.stoploss = 0
        #----------------------------------------

        #Initialize extra plot data arrays
        self.test1 = [np.NaN] * self.plotSize
        self.test2 = [np.NaN] * self.plotSize
        self.test3 = [np.NaN] * self.plotSize
        self.test4 = [np.NaN] * self.plotSize
        self.entry = [np.NaN] * self.plotSize
        self.exit = [np.NaN] * self.plotSize
        #array for all extra plot data
        self.extraPlots = [self.test1, self.test2, self.test3, self.test4, self.exit, self.entry]
        #style for extra plot data
        self.style = [['line','dashdot'],['line','dashdot'],['scatter','up'],['scatter','down'],['line','normal'],['line','normal']]

        #-----------STATS------------
        self.goodTrades = 0
        self.badTrades = 0
        self.totalProfit = 0
        #----------------------------

        #initialize plot if plot variable is true
        if(self.plotting):
            self.plotInit()


    def update(self):
        #This function will be run once the database recieves a new data point
        #all the logic that is checked to see if you need to buy or sell should be in this function

        #print("Run Algo Update Loop using data from " + self.ticker.symbol)
        #print("Trades placed will have the ID: " + self.tradeID)

        if self.ticker.validTradingHours == True:

            current_data = self.ticker.getData()
            #--------------------------------------------------------
            #----------|---Trading Logic Goes Below---|--------------
            #----------v------------------------------v--------------

            #SMA calcs
            avg1 = self.ticker.getData("FULL")[0:50]['close'].mean()
            avg2 = self.ticker.getData("FULL")[0:20]['close'].mean()

            self.test1.append(avg1)
            self.test2.append(avg2)

            #SMA Crossing Logic
            if avg1 > avg2 and self.highest != 1:
                num = current_data['close']*1.001
                self.test4.append(num)
                self.highest = 1
                self.entry = [current_data['close']] * self.plotSize
                self.inPosition = True 

            else:
                self.test4.append(np.NaN)

            if avg2 > avg1 and self.highest != 2:
                num = current_data['close']*0.999
                self.test3.append(num)
                self.highest = 2
                self.entry = [current_data['close']] * self.plotSize
                self.inPosition = True

            else:
                self.test3.append(np.NaN) 

            #Set Exit Price based on if its an up or down trade (both set to same at the moment..)
            if self.inPosition == True:
                if self.highest == 1:
                    self.exit = [current_data['close']] * self.plotSize

                if self.highest == 2:
                    self.exit = [current_data['close']] * self.plotSize

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

            #----------^------------------------------^--------------
            #----------|---Trading Logic Goes Above---|--------------
            #--------------------------------------------------------

            #This function handles all the plotting garbage
            self.plotUpdate()


        #if not valid Trading hours...
        else:
            if self.plotting:
                #update just the candles on the chart
                self.plot.update_chart(self.ticker.getData("FULL")[0:self.plotSize])




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

    def plotUpdate(self):

        #Ensure that all the arrays are the same size before sending them to the plotter
            for array in self.extraPlots:
                if len(array) > self.plotSize:
                    array.pop(0)

                if len(array) < self.plotSize:
                    array.append(np.NaN)

            if(self.inPosition):
                self.status = "In a Position. ID: " + self.tradeID

            #update plot if plotting is true
            if self.plotting:
                
                self.plot.update_chart(self.ticker.getData("FULL")[0:self.plotSize], self.extraPlots, self.style)
                

