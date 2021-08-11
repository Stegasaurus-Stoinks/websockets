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

# for i in range(0, len(mins), 1):
#     if (not np.isnan(mins[i])):
#         print(mins[i])
reach = 2

for i in range (0,len(ilocs_min)):
    try:
    
        x1 = ilocs_min[i]
        y1 = mins[ilocs_min[i]]
        x3 = 0
        y3 = 0
        for m in range(0,reach+1):
            if mins[ilocs_min[i+m]] > y1:
                x3 = ilocs_min[i+m]
                y3 = mins[ilocs_min[i+m]]

            if x3 != 0 and y3 != 0:
                #print("found valid second minimum")
                for j in range (x1,x3):
                    if (not np.isnan(maxs[j])):
                        #print("Found a max between two mins")
                        x2 = j
                        y2 = maxs[j]
                        slope = (y2-y1)/(x2-x1)
                        line = [np.NaN] * plotSize
                        #print(slope)
                        x = 0
                        for k in range (x1, x2+1):
                            line[k] = float(slope*x) + y1
                            x += 1

                        slope = (y3-y2)/(x3-x2)
                        x = 0
                        for k in range (x2, x3+1):
                            line[k] = float(slope*x) + y2
                            x += 1

                        
                            
                        extraplots.append(plotting.make_addplot(line,ax=ax1))
                    

                


    except:
        
        print("something broke in the try thingy")

#setup the figure and subplots

extraplots.append(plotting.make_addplot(mins,type='scatter',markersize=200,marker='^',ax=ax1))
extraplots.append(plotting.make_addplot(maxs,type='scatter',markersize=200,marker='.',color='b',ax=ax1))

mpf.plot(backtest,type='candle',style='charles',addplot= extraplots,warn_too_much_data=10000000000,ax=ax1, volume=ax2)
plt.show()
plt.pause(120)
#mpf.plot(backtest[0:100])

