from trade import Trade
from datetime import datetime
from plotter import LiveChartEnv


import pandas as pd
import numpy as np

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


        #---------Algo Sepcific Variables--------


        #----------------------------------------

        #Initialize extra plot data arrays
        self.test1 = [np.NaN] * self.plotSize
        self.test2 = [np.NaN] * self.plotSize

        #Array for all extra plot data
        self.extraPlots = [self.test1, self.test2]

        #Styling for extra plot data
        self.style = [['line','normal'],['line','normal']]

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
            AM_candlesticks = self.ticker.getData("FULL")

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

            #update plot if plotting is true
            if self.plotting:
                self.plot.update_chart(self.ticker.getData("FULL")[0:self.plotSize], self.extraPlots, self.style)
                

