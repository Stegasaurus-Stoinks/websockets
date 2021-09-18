import sys
sys.path.append('../')

from extra.trade import Trade
from extra.plotter import LiveChartEnv

from datetime import datetime, timedelta


import pandas as pd
import numpy as np
import talib

"""
This file was made as a template to create other algos,  The plotting method should work...
In order to add extra data to the plots you need to append or replace the values in teh arrays that are
initialized at the top.  It works with object pointers so if you create a new array object it will not 
work properly.  Styling options are limited rn. Check the plotter function for styling details.
"""

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
        self.exitPrice = np.NaN
        self.entryPrice = np.NaN

        #-----------STATS------------
        self.trades = []
        #----------------------------


        #---------Algo Sepcific Variables--------

        #----------------------------------------

        #initialize plot if plot variable is true
        if(self.plotting):
            self.plotInit()

        #Initialize extra plot data arrays
        self.trend1 = [np.NaN] * self.plotSize
        self.trend2 = [np.NaN] * self.plotSize
        self.upArrow = [np.NaN] * self.plotSize
        self.downArrow = [np.NaN] * self.plotSize
        self.entry = [np.NaN] * self.plotSize
        self.exit = [np.NaN] * self.plotSize

        #array for all extra plot data
        self.extraPlots = [self.upArrow, self.downArrow, self.exit, self.entry]

        #style for extra plot data
        self.style = [['scatter','up'],['scatter','down'],['line','dashdot'],['line','dashdot']]


    def update(self):
        #This function will be run once the database recieves a new data point
        #all the logic that is checked to see if you need to buy or sell should be in this function

        #print("Run Algo Update Loop using data from " + self.ticker.symbol)
        #print("Trades placed will have the ID: " + self.tradeID)
        current_data = self.ticker.getData()

        if self.ticker.validTradingHours == True:

            #--------------------------------------------------------
            #----------|---Trading Logic Goes Below---|--------------
            #----------v------------------------------v--------------


            #----------^------------------------------^--------------
            #----------|---Trading Logic Goes Above---|--------------
            #--------------------------------------------------------

            #This function handles all the plotting garbage

            self.plotUpdate()


        #if not valid Trading hours...
        else:
            #One minute before market close: close any open positions and print stats
            if current_data.name == self.ticker.DAY_END_TIME - timedelta(minutes=1):
                if self.inPosition:
                    self.trade.closePosition(current_data['close'],datetime.now())
                    self.trades.append(self.trade)

                self.Stats()

            if self.plotting:
                #update just the candles on the chart
                self.plot.update_chart(self.ticker.getData("FULL")[0:self.plotSize])

            

    def Stats(self):
        print(" ")
        print("--------------------ALGO STATS--------------------")
        #will probably need to connect to the database to find all that data, but not rn
        #print(self.trades)
        goodTrades = 0
        totalTrades = 0
        PL = 0
        for trade in self.trades:
            stats = trade.getStats(display = True)
            if stats["PL"] > 0:
                goodTrades += 1
            PL += stats["PL"]
            totalTrades += 1

        print("Good Trades: " + str(goodTrades) + "/" + str(totalTrades))
        print("Total Profit: " + str(PL))
        print(" ")



    def getStatus(self):
        return(self.status)
        #return(self.ticker.status)



    def plotInit(self):
        self.plot = LiveChartEnv("1min", self.plotSize)
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

            #ensure that style is always a normal line if not specified
            while len(self.style) < len(self.extraPlots):
                self.style.append(['line','normal'])

            #update plot if plotting is true
            if self.plotting:
                
                self.plot.update_chart(self.ticker.getData("FULL")[0:self.plotSize], self.extraPlots, self.style)


#------------------------------------------------------------
#--------------|---ALGO SPECIFIC FUNCTIONS----|--------------
#--------------v------------------------------v--------------

