import sys
sys.path.append('../')

from extra.trade import Trade
from extra.plotter import LiveChartEnv

from datetime import datetime, timedelta
from scipy.signal import argrelextrema


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


        #----------------------------------------

        #Initialize extra plot data arrays
        self.test1 = [np.NaN] * self.plotSize
        self.test2 = [np.NaN] * self.plotSize
        self.mins = [np.NaN] * self.plotSize
        self.maxs = [np.NaN] * self.plotSize
        self.test3 = [np.NaN] * self.plotSize
        self.test4 = [np.NaN] * self.plotSize

        #Array for all extra plot data
        #self.extraPlots = [self.test1, self.test2, self.mins, self.maxs, self.test3, self.test4]
        self.extraPlots = [self.mins, self.maxs]

        #Styling for extra plot data
        self.style = [['scatter','up'],['scatter','down']]

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
        self.current_data = self.ticker.getData()

        if self.ticker.validTradingHours == True:
            
            AM_candlesticks = self.ticker.getData("FULL")

            #--------------------------------------------------------
            #----------|---Trading Logic Goes Below---|--------------
            #----------v------------------------------v--------------

            #calculating trend line for certain range
            selected = AM_candlesticks[0:10]['close']
            coefficients, residuals, _, _, _ = np.polyfit(range(len(selected.index)),selected,1,full=True)
            mse = residuals[0]/(len(selected.index))
            nrmse = np.sqrt(mse)/(selected.max() - selected.min())
            #print('Slope ' + str(coefficients[0]))
            #print('NRMSE: ' + str(nrmse))
            temp = [coefficients[0]*x + coefficients[1] for x in range(len(selected))]
            for i in range (0,len(temp)):
                self.test2[self.plotSize - 1 - i] = temp[i]

            #calculating second trend line for longer range
            selected1 = AM_candlesticks[0:20]['close']
            coefficients, residuals, _, _, _ = np.polyfit(range(len(selected1.index)),selected1,1,full=True)
            mse = residuals[0]/(len(selected1.index))
            nrmse = np.sqrt(mse)/(selected1.max() - selected1.min())
            #print('Slope ' + str(coefficients[0]))
            #print('NRMSE: ' + str(nrmse))
            temp1 = [coefficients[0]*x + coefficients[1] for x in range(len(selected1))]
            for i in range (0,len(temp1)):
                self.test1[self.plotSize - 1 - i] = temp1[i]


            #Calculating mins and maxs
            n = 2 #Adjust this to add more or less mins and maxs (2 was the best one I found for short term)
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

            #Clear array without reinitializing... Need to find a better way of doing this
            for i in range (0,len(self.maxs)):
                self.maxs[i] = np.NaN
            for i in range (0,len(ilocs_max)):
                if ilocs_max[i] < self.plotSize:
                    self.maxs[ilocs_max[i]] = AM_candlesticks.iloc[ilocs_max[i]].close * 1.001
            #Flip array for plotter    
            self.maxs.reverse()


            #Adding min and max trend lines
            if(True):
                ply = 0.0005 #adjust this to make the trendlines more or less lenient
                ilocs_min2 = []
                for i in range (0,4):
                    if ilocs_min[i] < self.plotSize-1:
                        ilocs_min2.append(ilocs_min[i])

                x = np.array([x.seconds for x in np.diff(np.array(AM_candlesticks.index[0:self.plotSize]))]).cumsum()
                m, x = divmod(x, 60*1439)
                coefficients1, residuals1, _, _, _ = np.polyfit(m[ilocs_min2],AM_candlesticks.close[ilocs_min2],1,full=True)

                #create min trend line
                temp4 = [coefficients1[0]*x + coefficients1[1] for x in range(0,self.plotSize)]

                for i in range (0,len(self.test4)):
                    self.test4[i] = np.NaN

                #check if trend is valid by comparing it to trend line
                if((AM_candlesticks.close[ilocs_min2[1]]*(1+ply)) >= temp4[ilocs_min2[1]]) and (AM_candlesticks.close[ilocs_min2[2]]*(1+ply)) >= temp4[ilocs_min2[2]]:           
                    for i in range (0,ilocs_min2[-1]):
                        self.test4[i] = temp4[i]
                    self.test4.reverse()


                ilocs_max2 = []
                for i in range (0,4):
                    if ilocs_max[i] < self.plotSize-1:
                        ilocs_max2.append(ilocs_max[i])

                x = np.array([x.seconds for x in np.diff(np.array(AM_candlesticks.index[0:self.plotSize]))]).cumsum()
                m, x = divmod(x, 60*1439)
                coefficients2, residuals1, _, _, _ = np.polyfit(m[ilocs_max2],AM_candlesticks.close[ilocs_max2],1,full=True)
                #create max trend line
                temp3 = [coefficients2[0]*x + coefficients2[1] for x in range(0,self.plotSize)]
                
                #print(ilocs_max2)
                
                for i in range (0,len(self.test3)):
                    self.test3[i] = np.NaN

                if((AM_candlesticks.close[ilocs_max2[1]]*(1-ply)) <= temp3[ilocs_max2[1]] and (AM_candlesticks.close[ilocs_max2[2]]*(1-ply)) <= temp3[ilocs_max2[2]]):
                    for i in range (0,ilocs_max2[-1]):
                        self.test3[i] = temp3[i]
                    self.test3.reverse()



            self.extraPlots.append(self.test3)
            self.extraPlots.append(self.test4)


            if(self.inPosition):
                self.status = "In a Position. ID: " + self.tradeID

            else:
                self.status = "Running"

                #conditions that must be met to place a trade
                if 1:
                    #place a trade
                    volume = 10
                    trade = Trade(self.ticker.symbol, volume, self.tradeID, 1.01, self.ticker.AM_candlesticks.index[0], "UP",self.tradeapi, printInfo = True)
                    print("The trade is " + trade.getStatus())
                    self.inPosition = True


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
                
                self.plot.update_chart(self.ticker.getData("FULL")[0:self.plotSize], self.extraPlots, self.style)