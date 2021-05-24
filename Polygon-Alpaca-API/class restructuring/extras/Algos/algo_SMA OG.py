from trade import Trade
from datetime import datetime
from plotter import LiveChartEnv


import pandas as pd
import numpy as np

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
        self.sma50 = [np.NaN] * self.plotSize
        self.sma20 = [np.NaN] * self.plotSize
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
        self.extraPlots = [self.sma50, self.sma20, self.upArrow, self.downArrow, self.exit, self.entry]

        #style for extra plot data
        self.style = [['line','normal'],['line','normal'],['scatter','up'],['scatter','down'],['line','dashdot'],['line','dashdot']]


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
            avg1 = self.ticker.getData("FULL")[0:self.EMA1]['close'].mean()
            avg2 = self.ticker.getData("FULL")[0:self.EMA2]['close'].mean()

            self.sma50.append(avg1)
            self.sma20.append(avg2)

            #SMA Crossing Logic
            if avg1 > avg2 and self.highest != 1:
                #-------Enter a down trade-------
                num = current_data['close']*1.001
                self.downArrow.append(num)
                self.highest = 1
                self.entryPrice = current_data['open']
                self.inPosition = True 

                #Place a Trade
                time = datetime.now()
                volume = 10
                self.trade = Trade(self.ticker.symbol, volume, self.tradeID, current_data['open'], time, self.tradeapi, printInfo = True)
                #print("The trade is " + self.trade.getStatus())
                self.goodTrades += 1

            else:
                self.downArrow.append(np.NaN)

            if avg2 > avg1 and self.highest != 2:
                #-------Enter an up trade-------
                num = current_data['close']*0.999
                self.upArrow.append(num)
                self.highest = 2
                self.entryPrice = current_data['open']
                self.inPosition = True

                #Place a Trade
                time = datetime.now()
                volume = 10
                self.trade = Trade(self.ticker.symbol, volume, self.tradeID, current_data['open'], time, self.tradeapi, printInfo = True)
                #print("The trade is " + self.trade.getStatus())
                self.goodTrades += 1

            else:
                self.upArrow.append(np.NaN) 

            
            if self.inPosition == True:
                #Update Entry and Exit Price based on if its an up or down trade (both set to same at the moment..)
                self.entry.append(self.entryPrice)
                stop = 0.5
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
                        self.totalTrades += 1
                        stats = self.trade.getStats(display=False)
                        print(stats['PL'] , stats['duration'])
                        self.totalProfit -= stats['PL'] 
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
                        self.totalTrades += 1
                        stats = self.trade.getStats(display=False)
                        print(stats['PL'] , stats['duration'])
                        self.totalProfit += stats['PL']
                        self.inPosition = False

                #Check if trade needs to be exited

            else:
                self.status = "Running"
                time = datetime.now()
                self.exitPrice = np.NaN
                self.entryPrice = np.NaN
                self.exit.append(self.exitPrice)
                self.entry.append(self.entryPrice)


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





    def Stats(self):
        print("This will print all of the statistics of the algo")
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
                if len(array) > self.plotSize:
                    array.pop(0)

                if len(array) < self.plotSize:
                    array.append(np.NaN)

            if(self.inPosition):
                self.status = "In a Position. ID: " + self.tradeID

            #update plot if plotting is true
            if self.plotting:
                
                self.plot.update_chart(self.ticker.getData("FULL")[0:self.plotSize], self.extraPlots, self.style)
                

