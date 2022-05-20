import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from extra.trade import Trade
from IBKR.ibkrApi import ibkrApi as ibkr
from ib_insync import *
from extra.plotter import LiveChartEnv
from algos.elliot import Elliotfuncs
from datetime import datetime, timedelta
import mplfinance as mpf
from mplfinance import plotting
from matplotlib import gridspec
import pandas as pd
import numpy as np
import talib
from scipy.signal import argrelextrema


class Algo:
    
    #unique id so find trades that have been placed by this algo

    def __init__(self, ticker, name, risklevel, ib, live, plotting = False, plotSize = 50):
        self.ticker = ticker
        self.name = name
        self.risklevel = risklevel
        self.ib = ib
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
        self.saveWave = 0
        
        #----------------------------------------

        #initialize plot if plot variable is true
        if(self.plotting):
            self.plotInit()

        #Initialize extra plot data arrays
        self.finishedWaves = [np.NaN] * self.plotSize
        self.tradingWaves = [np.NaN] * self.plotSize
        self.mins = [np.NaN] * self.plotSize
        self.maxs = [np.NaN] * self.plotSize
        self.entry = [np.NaN] * self.plotSize
        self.exit = [np.NaN] * self.plotSize

        #array for all extra plot data
        self.extraPlots = [self.mins, self.maxs, self.exit, self.entry]
        self.waves = []
        #style for extra plot data
        self.style = [['scatter','up'],['scatter','down'],['line','normal'],['line','normal'],['line','normal'],['line','normal']]
        self.waveStyle = []

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
            #clearing arrays
            self.clearArray(self.mins)
            self.clearArray(self.maxs)
            self.clearArray(self.tradingWaves)
            self.clearArray(self.finishedWaves)
            self.extraPlots = [self.mins, self.maxs, self.exit, self.entry]

            volume = 10
            self.entryPrice = current_data['close']


            data = self.ticker.getData("FULL").iloc[::-1]
            ilocs_min = argrelextrema(data.low.values, np.less_equal, order=20)[0]
            ilocs_max = argrelextrema(data.high.values, np.greater_equal, order=20)[0]
            
            for i in range (0,len(ilocs_min)):
                self.mins[ilocs_min[i]] = data.iloc[ilocs_min[i]].low * 0.999
            
            for i in range (0,len(ilocs_max)):
                self.maxs[ilocs_max[i]] = data.iloc[ilocs_max[i]].high * 1.001
            
            


            self.finishedWaves,self.tradingWaves = Elliotfuncs.elliotRecursiveBlast(self.ticker.getData("FULL").iloc[::-1],self.plotSize,10)

            
            #plotting stuff
            self.plotWaves(self.finishedWaves)
            self.plotWaves(self.tradingWaves)

            ###find what wave the most recent unfinished elliot wave is on
             #curWave is first set to null in case there are no unfinished waves
            curWave = Elliotfuncs.ElliotImpulse(np.nan)
             #we check for waves and then set curWave to most recent wave
            if self.tradingWaves:
                curWave = self.tradingWaves[-1]
            waveNum = self.checkWaves(curWave)
            #print(waveNum)

            #If wave 2 or 4,check if x value of latest point is relatively recent, then buy for now.
            #    -Future implementation will have us wait for small uptrend before buying.
            if not self.inPosition:
                if waveNum == 2 or 4:#check if this works later
                    self.trade = Trade(self.ticker.symbol, volume, self.tradeID, self.entryPrice, datetime.now(), "UP",self.ib, printInfo = True)       
                    self.ib.simpleBuy(self.ticker.symbol, volume, self.entryPrice)
                    self.inPosition = True
                    self.saveWave = waveNum
                elif waveNum == 4:
                    self.trade = Trade(self.ticker.symbol, volume, self.tradeID, self.entryPrice, datetime.now(), "UP",self.ib, printInfo = True)       
                    self.ib.simpleBuy(self.ticker.symbol, volume, self.entryPrice)
                    self.inPosition = True
                    self.saveWave = waveNum
                else:#clear exit and entry price and place empty point
                    self.exitPrice = np.NaN
                    self.entryPrice = np.NaN
                    self.exit.append(self.exitPrice)
                    self.entry.append(self.entryPrice)
            #check if the next wave point has been added. When found, sell.
            else:
                #set stop loss and entry/exit prices
                self.entry.append(self.entryPrice)
                stop = 0.50
                stop = self.entryPrice * (stop/100)
                #Stop loss
                if np.isnan(self.exitPrice):
                    self.exitPrice = self.entryPrice - stop
                if self.exitPrice < current_data['close'] - stop:
                    self.exitPrice = current_data['close'] - stop 
                self.exit.append(self.exitPrice)

                if self.saveWave > waveNum or self.exitPrice > current_data['close']:
                    self.trade.closePosition(self.exitPrice,datetime.now())
                    self.trades.append(self.trade)
                    stats = self.trade.getStats(display=False)
                    print(stats['PL'] , stats['duration'])
                    self.inPosition = False
                    
                
            

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

    #clear array without reinitializing. If reinitialized then it will not plot properly
    def clearArray(self, array):
        for i in range (0,len(array)):
                array[i] = np.NaN       

#------------------------------------------------------------
#--------------|---ALGO SPECIFIC FUNCTIONS----|--------------
#--------------v------------------------------v--------------

    def plotWaves(self,waveList):
        toDisplay = Elliotfuncs.displaywaves(waveList)
        for wave in toDisplay:
            self.extraPlots.append(wave)

    #will return an int of which wave we are on
    def checkWaves(self,wave):
        if np.isnan(wave.x2):#.
            return 0
        elif np.isnan(wave.x3):#/
            return 1
        elif np.isnan(wave.x4):#/\
            return 2
        elif np.isnan(wave.x5):#/\/
            return 3
        elif np.isnan(wave.x6):#/\/\
            return 4