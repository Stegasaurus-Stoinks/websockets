import sys
sys.path.append('../')

from extra.trade import Trade
from extra.plotter import LiveChartEnv

from datetime import datetime, timedelta
from scipy.signal import argrelextrema


import pandas as pd
import numpy as np
import time

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


        #---------Algo Sepcific Variables--------


        #----------------------------------------

        #Initialize extra plot data arrays
        self.test1 = [np.NaN] * self.plotSize
        self.test2 = [np.NaN] * self.plotSize
        self.mins = [np.NaN] * self.plotSize
        self.maxs = [np.NaN] * self.plotSize
        self.entry = [np.NaN] * self.plotSize
        self.exit = [np.NaN] * self.plotSize

        #Array for all extra plot data
        self.extraPlots = [self.test1, self.test2, self.mins, self.maxs, self.entry, self.exit]

        #Styling for extra plot data
        self.style = [['line','normal'],['line','normal'],['scatter','up'],['scatter','down'],['line','normal'],['line','normal']]

        #-----------STATS------------
        self.trades = []
        #----------------------------

        #initialize plot if plot variable is true
        if(self.plotting):
            self.plotInit()


    def update(self):
        #This function will be run once the database recieves a new data point
        #all the logic that is checked to see if you need to buy or sell should be in this function

        #print("Run Algo Update Loop using data from " + self.ticker.symbol)
        #print("Trades placed will have the ID: " + self.tradeID)
        current_data = self.ticker.getData()

        if self.ticker.validTradingHours == True:

            
            AM_candlesticks = self.ticker.getData("FULL")

            #--------------------------------------------------------
            #----------|---Trading Logic Goes Below---|--------------
            #----------v------------------------------v--------------


            #Calculating mins and maxs
            n = 3 #Adjust this to add more or less mins and maxs (2 was the best one I found for short term)
            ilocs_min = argrelextrema(AM_candlesticks.close.values, np.less_equal, order=n)[0]
            ilocs_max = argrelextrema(AM_candlesticks.close.values, np.greater_equal, order=n)[0]

            #Clear array without reinitializing... Need to find a better way of doing this
            for i in range (0,len(self.mins)):
                self.mins[i] = np.NaN               
            for i in range (0,len(ilocs_min)):
                if ilocs_min[i] < self.plotSize:
                    self.mins[ilocs_min[i]] = AM_candlesticks.iloc[ilocs_min[i]].close * 0.999
            
            #Flip array for plotter                         
            self.mins.reverse()
            #print(self.mins)
            
            size = 50
            if self.mins[-1] is not np.NaN and not self.inPosition:
                cleanedmins = [min for min in self.mins[len(self.mins)-size:] if ~np.isnan(min)]
                if len(cleanedmins) > 3:
                    #print("here")
                    #print(cleanedmins)
                    if cleanedmins[-1] > cleanedmins[-2] > cleanedmins[-3]:
                        print("")
                        print("3 increasing mins found")
                        print(cleanedmins[-1],cleanedmins[-2],cleanedmins[-3])
                        print("")
                        if self.plotting:
                            time.sleep(1)
                        #----------------------Entering Trade----------------------#\
                        #place a trade
                        volume = 10
                        self.entryPrice = current_data['open']
                        self.trade = Trade(self.ticker.symbol, volume, self.tradeID, self.entryPrice, datetime.now(), "UP",self.tradeapi, printInfo = True)
                        #print("The trade is " + trade.getStatus())
                        self.inPosition = True


                    
            
            #print(self.mins)
            


            #Clear array without reinitializing... Need to find a better way of doing this
            for i in range (0,len(self.maxs)):
                self.maxs[i] = np.NaN
            for i in range (0,len(ilocs_max)):
                if ilocs_max[i] < self.plotSize:
                    self.maxs[ilocs_max[i]] = AM_candlesticks.iloc[ilocs_max[i]].close * 1.001
            #Flip array for plotter    
            self.maxs.reverse()


            if self.inPosition == True:
                #Update Entry and Exit Price based on if its an up or down trade (both set to same at the moment..)
                self.entry.append(self.entryPrice)
                stop = 0.50
                stop = self.entryPrice * (stop/100)

                if self.trade.direction == "UP":

                    #Stop loss
                    if np.isnan(self.exitPrice):
                        self.exitPrice = self.entryPrice - stop
                    if self.exitPrice < current_data['close'] - stop:
                        self.exitPrice = current_data['close'] - stop 
                    self.exit.append(self.exitPrice)
                    #print("Up")

                    if self.exitPrice > current_data['close'] or self.exitPrice > current_data['low']:
                        self.trade.closePosition(self.exitPrice,datetime.now())
                        self.trades.append(self.trade)
                        stats = self.trade.getStats(display=False)
                        print(stats['PL'] , stats['duration'])
                        self.inPosition = False

                #Check if trade needs to be exited

            else:
                self.status = "Running"
                #time = datetime.now()
                self.exitPrice = np.NaN
                self.entryPrice = np.NaN
                self.exit.append(self.exitPrice)
                self.entry.append(self.entryPrice)



            if(self.inPosition):
                self.status = "In a Position. ID: " + self.tradeID

            else:
                self.status = "Running"

                    

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