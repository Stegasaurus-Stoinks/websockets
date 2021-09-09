import sys
sys.path.append('../')

from extra.trade import Trade
from extra.plotter import LiveChartEnv

from datetime import datetime, timedelta


import pandas as pd
import numpy as np
import talib
from scipy.signal import argrelextrema

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

        #Initialize extra plot data arrays
        self.trend1 = [np.NaN] * self.plotSize
        self.trend2 = [np.NaN] * self.plotSize
        self.upArrow = [np.NaN] * self.plotSize
        self.downArrow = [np.NaN] * self.plotSize
        self.entry = [np.NaN] * self.plotSize
        self.exit = [np.NaN] * self.plotSize


        #initialize plot if plot variable is true
        if(self.plotting):
            self.plotInit()

        #array for all extra plot data
        self.extraPlots = [self.upArrow, self.downArrow, self.exit, self.entry]

        #style for extra plot data
        self.style = [['scatter','up'],['scatter','down']]


    def update(self):
        #This function will be run once the database recieves a new data point
        #all the logic that is checked to see if you need to buy or sell should be in this function

        #print("Run Algo Update Loop using data from " + self.ticker.symbol)
        #print("Trades placed will have the ID: " + self.tradeID)
        self.current_data = self.ticker.getData()
        #print(self.ticker.validTradingHours)
        if self.ticker.validTradingHours == True:
            #--------------------------------------------------------
            #----------|---Trading Logic Goes Below---|--------------
            #----------v------------------------------v--------------

            self.AM_candlesticks = self.ticker.getData("FULL")
            close = self.AM_candlesticks['close'].to_numpy()
            close = close[::-1]
            
            trendline = talib.LINEARREG(close, timeperiod=14).tolist()
            trendline = trendline[len(close)-self.plotSize::] #shorten trendline calc to plotsize

            levels = []
            #Finding key price levels by matching candle pattern
            df = self.ticker.getData("FULL")
            for i in range(2,df.shape[0]-2):    
                if self.isSupport(df,i):
                    if not self.isClosetoLevel(df['low'][i],levels,1):
                        levels.append((df['close'][i]))
                elif self.isResistance(df,i):
                    if not self.isClosetoLevel(df['high'][i],levels,1):
                        levels.append((df['high'][i]))
                    #print("")

            #Adding some key price levels with local mins and maxs
            n = 3 #Adjust this to add more or less mins and maxs (2 was the best one I found for short term)
            ilocs_min = argrelextrema(self.AM_candlesticks.close.values, np.less_equal, order=n)[0]
            ilocs_max = argrelextrema(self.AM_candlesticks.close.values, np.greater_equal, order=n)[0]
            #levels.extend(ilocs_max)
            #levels.extend(ilocs_min)



            current_data_average = (self.current_data["open"] + self.current_data["close"])/2
            print(current_data_average)
            if self.isClosetoLevel(current_data_average, levels):
                print("close to critical price level")
            #print(l,level)
            
                
            i = 4
            self.extraPlots = self.extraPlots[0:i-1]
            #print(levels)
            for level in levels:
                #print("LEVEL: ",level)
                levelline = []
                levelline = [level] * self.plotSize
                #print(levelline)
                self.extraPlots.append(levelline)
            
            #print(self.extraPlots)

            
            
            print(len(trendline))
            self.extraPlots.append(trendline)
            #self.extraPlots[1] = trendline1
            #print(output)

            
            

            #----------^------------------------------^--------------
            #----------|---Trading Logic Goes Above---|--------------
            #--------------------------------------------------------

            #This function handles all the plotting garbage

            self.plotUpdate()


        #if not valid Trading hours...
        else:
            #One minute before market close: close any open positions and print stats
            if self.current_data.name == self.ticker.DAY_END_TIME - timedelta(minutes=1):
                if self.inPosition:
                    self.trade.closePosition(self.current_data['close'],datetime.now())
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
                #print("update")
                self.plot.update_chart(self.ticker.getData("FULL")[0:self.plotSize], self.extraPlots, self.style)
                

#----------------------------ALGO SPECIFIC FUNCTIONS---------------------------

    def isSupport(self,df,i):
            support = df['close'][i] < df['close'][i-1]  and df['close'][i] < df['close'][i+1] \
            and df['close'][i+1] < df['close'][i+2] and df['close'][i-1] < df['close'][i-2]

            return support

    def isResistance(self,df,i):
        resistance = df['open'][i] > df['open'][i-1]  and df['open'][i] > df['open'][i+1] \
        and df['open'][i+1] > df['open'][i+2] and df['open'][i-1] > df['open'][i-2] 

        return resistance

    def isClosetoLevel(self,l,levels,range = 0.1):
        isClose = False
        for level in levels:
            #print(l,level)
            if abs(l - level) <= range:
                isClose = True
        return(isClose)

    def isSimilarLevel(levels):
        fillteredLevels = []
        for level in levels:
                simlevels = []
                for otherlevel in levels:
                    if abs(level - otherlevel) <= current_data["open"]*0.001:
                        simlevels.append(otherlevel)
                        levels.remove(otherlevel)

                if len(simlevels) > 1:
                    mean = sum(simlevels)/len(simlevels)
                    fillteredLevels.append(mean)

        return fillteredLevels