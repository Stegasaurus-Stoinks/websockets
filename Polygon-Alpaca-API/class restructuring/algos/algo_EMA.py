import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from extra.trade import Trade
from extra.plotter import LiveChartEnv

from datetime import datetime , timedelta

import pandas as pd
import numpy as np
import talib

class Algo:
    
    #unique id so find trades that have been placed by this algo

    def __init__(self, ticker, name, risklevel, tradeapi, live, EMA1, EMA2, plotting = False, plotSize = 50):
        self.ticker = ticker
        self.name = name
        self.risklevel = risklevel
        self.tradeapi = tradeapi
        self.live = live
        self.plotting = plotting
        self.plotSize = plotSize

        self.EMA1 = EMA1
        self.EMA2 = EMA2

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
        self.ema1 = [np.NaN] * self.plotSize
        self.ema2 = [np.NaN] * self.plotSize
        self.upArrow = [np.NaN] * self.plotSize
        self.downArrow = [np.NaN] * self.plotSize
        self.entry = [np.NaN] * self.plotSize
        self.exit = [np.NaN] * self.plotSize

        
        #-----------STATS------------
        self.trades = []
        #----------------------------

        #initialize plot if plot variable is true
        if(self.plotting):
            self.plotInit()

        #array for all extra plot data
        self.extraPlots = [self.ema1, self.ema2, self.upArrow, self.downArrow, self.exit, self.entry]

        #style for extra plot data
        self.style = [['line','normal'],['line','normal'],['scatter','up'],['scatter','down'],['line','dashdot'],['line','dashdot']]


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

            #EMA calcs
            avg1 = self.ticker.getData("FULL")[0:self.EMA1]['close'].mean()
            avg2 = self.ticker.getData("FULL")[0:self.EMA2]['close'].mean()

            close = self.ticker.getData("FULL")
            close = close['close'].to_numpy()
            close = close[::-1]
            avg1 = talib.EMA(close, timeperiod=self.EMA1)[-1]
            avg2 = talib.EMA(close, timeperiod=self.EMA2)[-1]
            #print(output)

            self.ema1.append(avg1)
            self.ema2.append(avg2)

            #EMA Crossing Logic
            if avg1 > avg2 and self.highest != 1:

                time = datetime.now()
                #close open position if already in one
                if self.inPosition:
                    if self.trade.getStatus() == "Open":
                        self.trade.closePosition(current_data['open'],time)
                        self.trades.append(self.trade)

                #-------Enter a down trade-------
                num = current_data['open']*1.001
                self.downArrow.append(num)
                self.highest = 1
                self.entryPrice = current_data['open']
                self.inPosition = True 

                #Place a Trade
                volume = 10
                self.trade = Trade(self.ticker.symbol, volume, self.tradeID, current_data['open'], time, "DOWN", self.tradeapi, printInfo = True)
                #print("The trade is " + self.trade.getStatus())

            else:
                self.downArrow.append(np.NaN)

            if avg2 > avg1 and self.highest != 2:

                time = datetime.now()
                #close open position if already in one
                if self.inPosition:
                    if self.trade.getStatus() == "Open":
                        self.trade.closePosition(current_data['open'],time)
                        self.trades.append(self.trade)

                #-------Enter an up trade-------
                num = current_data['open']*0.999
                self.upArrow.append(num)
                self.highest = 2
                self.entryPrice = current_data['open']
                self.inPosition = True

                #Place a Trade
                volume = 10
                self.trade = Trade(self.ticker.symbol, volume, self.tradeID, current_data['open'], time, "UP", self.tradeapi, printInfo = True)
                #print("The trade is " + self.trade.getStatus())
                

            else:
                self.upArrow.append(np.NaN) 

            
            if self.inPosition == True:
                #Update Entry and Exit Price based on if its an up or down trade (both set to same at the moment..)
                self.entry.append(self.entryPrice)
                stop = 0.5
                stop = current_data['close'] * (stop/100)
                if self.highest == 1:

                    #Stop loss
                    if np.isnan(self.exitPrice):
                        self.exitPrice = self.entryPrice + stop
                    if self.exitPrice > current_data['close'] + stop:
                        self.exitPrice = current_data['close'] + stop

                    #print(self.entryPrice,self.exitPrice) 
                    self.exit.append(self.exitPrice)
                    #print("Down")

                    if self.exitPrice < current_data['close']:
                        self.trade.closePosition(current_data['close'],datetime.now())
                        self.trades.append(self.trade)
                        stats = self.trade.getStats(display=False)
                        print(stats['PL'] , stats['duration'])
                        self.inPosition = False
                        

                if self.highest == 2:

                    #Stop loss
                    if np.isnan(self.exitPrice):
                        self.exitPrice = self.entryPrice - stop
                    if self.exitPrice < current_data['close'] - stop:
                        self.exitPrice = current_data['close'] - stop 
                    self.exit.append(self.exitPrice)
                    #print("Up")

                    if self.exitPrice > current_data['close']:
                        self.trade.closePosition(current_data['close'],datetime.now())
                        self.trades.append(self.trade)
                        stats = self.trade.getStats(display=False)
                        print(stats['PL'] , stats['duration'])
                        self.inPosition = False

                #Check if trade needs to be exited

            else:
                self.status = "Running"
                time = datetime.now()
                self.exitPrice = np.NaN
                self.entryPrice = np.NaN
                self.exit.append(self.exitPrice)
                self.entry.append(self.entryPrice)

            #print(current_data.name)
            # = datetime.timedelta(minutes = 2)


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
            self.plot.update_chart(self.ticker.getData("FULL")[0:self.plotSize])#, self.extraPlots, self.style) Removed xtraplots
            

