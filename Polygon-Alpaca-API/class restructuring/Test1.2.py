import sys
sys.path.append('../')

from mplfinance import plotting
from algos.algo_EMA import Algo as AlgoEMA
from algos.algo_Support import Algo as AlgoSupport
from algos.algo_Support2 import Algo as AlgoSupport2
from algos.trend.algo_Trendlines import Algo as AlgoTrend
from algos.trend.algo_higherlows import Algo as AlgoHigherLows

from extra.ticker import Ticker
from extra.database import Database
from extra.tradeApi import TradeApi
from extra.plotter import LiveChartEnv

import Elliotfuncs

import time
import mplfinance as mpf
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
import numpy as np
from matplotlib import gridspec

plt.ion()

extraplots = []
spec = gridspec.GridSpec(ncols=1, nrows=2, hspace=0.5, height_ratios=[2, 1])
fig = mpf.figure(figsize=(7,8))
ax1 = fig.subplot(spec[0])
ax2 = fig.add_subplot(spec[1])
fig.gridspec_kw={'height_ratios': [1, 2]}

#------Config Variables------
Trading = False
Live_Trading = False
BackTest = True

start = 0
plotSize = 900
#----------------------------

DB = Database(BackTest)
api = TradeApi(Trading, Live_Trading)
#Initiaiize all relevant tickers for the day

#pick from {CCL, AAPL, MSFT, HD, NFLX, GOOG, TSLA, VZ, INTC, AMZN, FB}
AAPL = Ticker("AAPL", "Stock", DB, startDate='2021-01-04', endDate='2021-01-14')
MSFT = Ticker("MSFT", "Stock", DB, startDate='2021-01-04', endDate='2021-01-14')  
TSLA = Ticker("TSLA", "Stock", DB, startDate='2021-01-04', endDate='2021-01-14')

AAPL.warmUp()

backtest = AAPL.BackTestAM_candlesticks
backtest = backtest.sort_index(ascending=True)
#print(backtest.shape)

#removes all the data that is outside of market hours
backtest = backtest.between_time('9:30', '15:59')

#skrinks the working data so its easier to use/analyze
backtest = backtest[start:start + plotSize]
print(backtest.head())

#Calculating mins and maxs
n = 20 #Adjust this to add more or less mins and maxs (2 was the best one I found for short term)
ilocs_min = argrelextrema(backtest.low.values, np.less_equal, order=n)[0]
ilocs_max = argrelextrema(backtest.high.values, np.greater_equal, order=n)[0]

#print(ilocs_min)
#print(ilocs_max)

#array of min and max plotpoints
#fill array with nan's first, then replace nan's with min and max values where necessary
mins = [np.NaN] * plotSize
for i in range (0,len(ilocs_min)):
    mins[ilocs_min[i]] = backtest.iloc[ilocs_min[i]].low * 0.999

maxs = [np.NaN] * plotSize
for i in range (0,len(ilocs_max)):
    maxs[ilocs_max[i]] = backtest.iloc[ilocs_max[i]].high * 1.001

#---------------Now I just need to find these points automatically----------------

#wave = Elliotfuncs.ElliotImpulse(plotSize)
#wave.definepoints(x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6)
#wave.printdata()
#waveplot = wave.assemble()
#print(waveplot)
#extraplots.append(plotting.make_addplot(waveplot,ax=ax1))

#-----------------------------------------------------------------------------------

reach = 2
possibleWaves = list()
counter = 0

#for every min in chart
for i in range (0,len(ilocs_min)):
    if(1):
    #try:
        wave = Elliotfuncs.ElliotImpulse(plotSize)
        wave.x1 = ilocs_min[i]
        wave.y1 = mins[ilocs_min[i]]

        
           
        ilocs_max_valid = [x for x in ilocs_max if x>wave.x1]#all max's past point 1

        #print(wave.x1, ilocs_max_valid)
        maxval2 = wave.y1
        for x in ilocs_max_valid[0:reach+1]:
            if(maxs[x] > maxval2):
                maxval2 = maxs[x]
                wave.x2 = x
                wave.y2 = maxs[x]
                

                ilocs_min_valid = [x for x in ilocs_min if x>wave.x2]

                minval3 = wave.y2
                for x in ilocs_min_valid[0:reach+1]:
                    if(wave.checkpoint3(x,mins[x])):
                        if(mins[x] < minval3):
                            minval3 = mins[x]
                            wave.x3 = x
                            wave.y3 = mins[x]

                            ilocs_max_valid = [x for x in ilocs_max if x>wave.x3]
                        
                            maxval4 = wave.y3
                            for x in ilocs_max_valid[0:reach+1]:

                                if(wave.checkpoint4(x,maxs[x])):
                                    if(maxs[x] > maxval4):
                                        maxval4 = maxs[x]
                                        wave.x4 = x
                                        wave.y4 = maxs[x]
                                        #print("found valid 4")

                                        ilocs_min_valid = [x for x in ilocs_min if x>wave.x4]

                                        minval5 = wave.y4
                                        for x in ilocs_min_valid[0:reach+1]:
                                            if(wave.checkpoint5(x,mins[x])):
                                                if(mins[x] < minval5):
                                                    minval5 = mins[x]
                                                    wave.x5 = x
                                                    wave.y5 = mins[x]
                                                    #print("found valid 5")

                                                    ilocs_max_valid = [x for x in ilocs_max if x>wave.x5]

                                                    maxval6 = wave.y5
                                                    for x in ilocs_max_valid[0:reach+1]:

                                                        if(wave.checkpoint6(x,maxs[x])):
                                                            if(maxs[x] > maxval6):
                                                                maxval6 = maxs[x]
                                                                wave.x6 = x
                                                                wave.y6 = maxs[x]
                                                                #print("found valid 6")
                                                                print("wave:",counter)
                                                                wave.printdata()
                                                                possibleWaves.append(wave)
                                                                possibleWaves[counter].printdata()
                                                                counter += 1
                                                                #waveplot = wave.assemble()
                                                                #print(wave.printdata())
                                                                #print(waveplot)
                                                                #extraplots.append(plotting.make_addplot(waveplot,ax=ax1))        
        
    else:
    #except:
        
        print("something broke in the try thingy")
possibleWaves[0].printdata()
print("found", len(possibleWaves),"possible elliot wave impulses")

#[2,9] give decent results
toDisplay = Elliotfuncs.displaywaves(possibleWaves)
for waves in toDisplay:
    extraplots.append(plotting.make_addplot(waves,ax=ax1))
    

#setup the figure and subplots

#extraplots.append(plotting.make_addplot(mins,type='scatter',markersize=200,marker='^',ax=ax1))
#extraplots.append(plotting.make_addplot(maxs,type='scatter',markersize=200,marker='.',color='b',ax=ax1))

mpf.plot(backtest,type='candle',style='charles',addplot= extraplots,warn_too_much_data=10000000000,ax=ax1, volume=ax2)
plt.show()
plt.pause(120)
#mpf.plot(backtest[0:100])

