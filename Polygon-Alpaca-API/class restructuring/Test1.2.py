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
MSFT = Ticker("MSFT", "Stock", DB)  
TSLA = Ticker("TSLA", "Stock", DB)

AAPL.warmUp()

backtest = AAPL.BackTestAM_candlesticks
backtest = backtest.sort_index(ascending=True)
#print(backtest.shape)

#removes all the data that is outside of market hours
backtest = backtest.between_time('9:30', '15:59')
#print(backtest.shape)

#print(backtest.head())

backtest = backtest[start:start + plotSize]

#fig = mpf.figure(figsize=(7,8))

#Calculating mins and maxs
n = 15 #Adjust this to add more or less mins and maxs (2 was the best one I found for short term)
ilocs_min = argrelextrema(backtest.close.values, np.less_equal, order=n)[0]
ilocs_max = argrelextrema(backtest.close.values, np.greater_equal, order=n)[0]

#print(ilocs_min)
#print(ilocs_max)

mins = [np.NaN] * plotSize
for i in range (0,len(ilocs_min)):
    mins[ilocs_min[i]] = backtest.iloc[ilocs_min[i]].close * 0.999

maxs = [np.NaN] * plotSize
for i in range (0,len(ilocs_max)):
    maxs[ilocs_max[i]] = backtest.iloc[ilocs_max[i]].close * 1.001

#Now I just need to find these points automatically 
i = 4
j = 4
#valleys
x1 = ilocs_min[i]
y1 = mins[ilocs_min[i]]

x3 = ilocs_min[i+1]
y3 = mins[ilocs_min[i+1]]

x5 = ilocs_min[i+2]
y5 = mins[ilocs_min[i+2]]

#peaks
x2 = ilocs_max[j]
y2 = maxs[ilocs_max[j]]

x4 = ilocs_max[j+1]
y4 = maxs[ilocs_max[j+1]]

x6 = ilocs_max[j+2]
y6 = maxs[ilocs_max[j+2]]

wave = Elliotfuncs.ElliotImpulse(plotSize)
wave.definepoints(x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6)
#wave.printdata()
waveplot = wave.assemble()
#print(waveplot)
extraplots.append(plotting.make_addplot(waveplot,ax=ax1))

reach = 2

for i in range (0,len(ilocs_min)):
    if(1):
    #try:
        wave = Elliotfuncs.ElliotImpulse(plotSize)
        wave.x1 = ilocs_min[i]
        wave.y1 = mins[ilocs_min[i]]

        ilocs_max_valid = [x for x in ilocs_max if x>wave.x1]

        #print(wave.x1, ilocs_max_valid)

        for x in ilocs_max_valid[0:reach+1]:
            wave.x2 = x
            wave.y2 = maxs[x]

            ilocs_min_valid = [x for x in ilocs_min if x>wave.x2]

            for x in ilocs_min_valid[0:reach+1]:
                if(wave.checkpoint3(x,mins[x])):
                    wave.x3 = x
                    wave.y3 = mins[x]

                    ilocs_max_valid = [x for x in ilocs_max if x>wave.x3]

                    for x in ilocs_max_valid[0:reach+1]:

                        if(wave.checkpoint4(x,maxs[x])):
                            wave.x4 = x
                            wave.y4 = maxs[x]

                            ilocs_min_valid = [x for x in ilocs_min if x>wave.x4]

                            for x in ilocs_min_valid[0:reach+1]:
                                if(wave.checkpoint5(x,mins[x])):
                                    wave.x5 = x
                                    wave.y5 = mins[x]

                                    ilocs_max_valid = [x for x in ilocs_max if x>wave.x5]

                                    for x in ilocs_max_valid[0:reach+1]:

                                        if(wave.checkpoint6(x,maxs[x])):
                                            wave.x6 = x
                                            wave.y6 = maxs[x]


                                            waveplot = wave.assemble()
                                            #print(waveplot)
                                            extraplots.append(plotting.make_addplot(waveplot,ax=ax1))


        
        

    else:
    #except:
        
        print("something broke in the try thingy")

#setup the figure and subplots

extraplots.append(plotting.make_addplot(mins,type='scatter',markersize=200,marker='^',ax=ax1))
extraplots.append(plotting.make_addplot(maxs,type='scatter',markersize=200,marker='.',color='b',ax=ax1))

mpf.plot(backtest,type='candle',style='charles',addplot= extraplots,warn_too_much_data=10000000000,ax=ax1, volume=ax2)
plt.show()
plt.pause(120)
#mpf.plot(backtest[0:100])

