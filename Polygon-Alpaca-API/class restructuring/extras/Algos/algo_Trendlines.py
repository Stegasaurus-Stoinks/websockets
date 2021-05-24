from trade import Trade
from datetime import datetime
from plotter import LiveChartEnv


import pandas as pd
import numpy as np
import talib

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
        self.highest = 0
        self.stoploss = 0
        #----------------------------------------

        #Initialize extra plot data arrays
        self.trend1 = [np.NaN] * self.plotSize
        self.trend2 = [np.NaN] * self.plotSize
        self.upArrow = [np.NaN] * self.plotSize
        self.downArrow = [np.NaN] * self.plotSize
        self.entry = [np.NaN] * self.plotSize
        self.exit = [np.NaN] * self.plotSize

        
        #-----------STATS------------
        self.goodTrades = 0
        self.badTrades = 0
        self.totalProfit = 0
        self.totalTrades = 0
        #----------------------------

        #initialize plot if plot variable is true
        if(self.plotting):
            self.plotInit()

        #array for all extra plot data
        self.extraPlots = [self.upArrow, self.downArrow, self.exit, self.entry]

        #style for extra plot data
        self.style = [['scatter','up'],['scatter','down'],['line','dashdot'],['line','dashdot']]


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

            close = self.ticker.getData("FULL")
            close = close['close'].to_numpy()
            close = close[::-1]
            
            trendline = talib.LINEARREG(close, timeperiod=14).tolist()
            levels = []
            df = self.ticker.getData("FULL")
            for i in range(2,df.shape[0]-2):    
                if self.isSupport(df,i):
                    if not self.isClosetoLevel(df['low'][i],levels):
                        levels.append((df['low'][i]))
                elif self.isResistance(df,i):
                    if not self.isClosetoLevel(df['high'][i],levels):
                        levels.append((df['high'][i]))

            #print(levels)
            i = 4
            self.extraPlots = self.extraPlots[0:i-1]
            for level in levels:
                levelline = [level] * self.plotSize
                self.extraPlots.append(levelline)

            
            
            #print(len(trendline))
            #self.extraPlots[0] = trendline
            #self.extraPlots[1] = trendline1
            #print(output)

            
            

            #----------^------------------------------^--------------
            #----------|---Trading Logic Goes Above---|--------------
            #--------------------------------------------------------

            #This function handles all the plotting garbage

            self.plotUpdate()


        #if not valid Trading hours...
        else:
            self.Stats()
            if self.plotting:
                #update just the candles on the chart
                self.plot.update_chart(self.ticker.getData("FULL")[0:self.plotSize])

            #quit()



    def isSupport(self,df,i):
        support = df['low'][i] < df['low'][i-1]  and df['low'][i] < df['low'][i+1] \
        and df['low'][i+1] < df['low'][i+2] and df['low'][i-1] < df['low'][i-2]

        return support

    def isResistance(self,df,i):
        resistance = df['high'][i] > df['high'][i-1]  and df['high'][i] > df['high'][i+1] \
        and df['high'][i+1] > df['high'][i+2] and df['high'][i-1] > df['high'][i-2] 

        return resistance

    def isClosetoLevel(self,l,levels):
        isClose = False
        for level in levels:
            #print(l,level)
            if abs(l - level) <= .10:
                isClose = True
        return(isClose)


    def Stats(self):
        print("----------------This will print all of the statistics of the algo----------------")
        #will probably need to connect to the database to find all that data, but not rn
        print("Good Trades: " + str(self.goodTrades) + "/" + str(self.totalTrades))
        print("Total Profit: " + str(self.totalProfit))



    def getStatus(self):
        return(self.status)
        #return(self.ticker.status)



    def plotInit(self):
        self.plot = LiveChartEnv("1min", self.plotSize)
        self.plot.initialize_chart()

    def plotUpdate(self):

        #Ensure that all the arrays are the same size before sending them to the plotter
            for array in self.extraPlots:
                while len(array) > self.plotSize:
                    array.pop(0)

                while len(array) < self.plotSize:
                    array.append(np.NaN)

            if(self.inPosition):
                self.status = "In a Position. ID: " + self.tradeID

            #ensure that style is always a normal line
            while len(self.style) < len(self.extraPlots):
                self.style.append(['line','normal'])

            #update plot if plotting is true
            if self.plotting:
                
                self.plot.update_chart(self.ticker.getData("FULL")[0:self.plotSize], self.extraPlots, self.style)
                

