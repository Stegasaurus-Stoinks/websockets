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

import SupportResistanceFunc

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
AAPL = Ticker("AAPL", "Stock", DB, startDate='2021-01-06', endDate='2021-01-07')
MSFT = Ticker("MSFT", "Stock", DB, startDate='2021-01-04', endDate='2021-01-14')  
TSLA = Ticker("TSLA", "Stock", DB, startDate='2021-01-04', endDate='2021-01-14')

AAPL.warmUp()

backtest = AAPL.BackTestAM_candlesticks
backtest = backtest.sort_index(ascending=True)
#print(backtest.shape)

#removes all the data that is outside of market hours
backtest = backtest.between_time('9:30', '15:59')
if plotSize > backtest.shape[0]:
    plotSize = backtest.shape[0]

#skrinks the working data so its easier to use/analyze
backtest = backtest[start:start + plotSize]
#print(backtest.head())

#Calculating mins and maxs
n =  #Adjust this to add more or less mins and maxs (2 was the best one I found for short term)
ilocs_min = argrelextrema(backtest.low.values, np.less_equal, order=n)[0]
ilocs_max = argrelextrema(backtest.high.values, np.greater_equal, order=n)[0]

mins = [np.NaN] * plotSize
minsadj = [np.NaN] * plotSize
for i in range (0,len(ilocs_min)):
    mins[ilocs_min[i]] = backtest.iloc[ilocs_min[i]].low
    minsadj[ilocs_min[i]] = backtest.iloc[ilocs_min[i]].low * 0.999

maxs = [np.NaN] * plotSize
maxsadj = [np.NaN] * plotSize
for i in range (0,len(ilocs_max)):
    maxs[ilocs_max[i]] = backtest.iloc[ilocs_max[i]].high
    maxsadj[ilocs_max[i]] = backtest.iloc[ilocs_max[i]].high * 1.001


reach = 4
possibleWaves = []
counter = 0

#find horizontal support resistance
for i in range(0,len(ilocs_min)-reach):
    for x in range(i+1,i+reach):
        plot = False
        x1 = ilocs_min[i]
        x2 = ilocs_min[x]
        point1 = mins[x1]
        point2 = mins[x2]

        #create line between the 2 points
        slope = SupportResistanceFunc.calculateslope(x1,point1,x2,point2)
        line = [np.NaN] * plotSize
        for k in range(x1,x2+1):
            line[k] = (point1-slope*x1)+(slope*k)

        #check to make sure there are no mins in the range the invalidate the line
        for j in range(i,x):
            if line[ilocs_min[j]] <= mins[ilocs_min[j]]:
                plot = True

            else:
                plot = False
                break

        if plot:
            #print(line)
            extraplots.append(plotting.make_addplot(line,ax=ax1))

for i in range(0,len(ilocs_max)-reach):
    for x in range(i+1,i+reach):
        x1 = ilocs_max[i]
        x2 = ilocs_max[x]
        point1 = maxs[x1]
        point2 = maxs[x2]
        #plot line between the 2 points
        slope = SupportResistanceFunc.calculateslope(x1,point1,x2,point2)
        line = [np.NaN] * plotSize
        for k in range(x1,x2+1):
            line[k] = (point1-slope*x1)+(slope*k)
        
        #check to make sure there are no maxs in the range the invalidate the line
        for j in range(i,x):
            if line[ilocs_max[j]] >= maxs[ilocs_max[j]]:
                plot = True

            else:
                plot = False
                break

        if plot:
            #print(line)
            extraplots.append(plotting.make_addplot(line,ax=ax1))



#setup the figure and subplots

extraplots.append(plotting.make_addplot(minsadj,type='scatter',markersize=200,marker='^',ax=ax1))
extraplots.append(plotting.make_addplot(maxsadj,type='scatter',markersize=200,marker='.',color='b',ax=ax1))

mpf.plot(backtest,type='candle',style='charles',addplot= extraplots,warn_too_much_data=10000000000,ax=ax1, volume=ax2)
plt.show()
plt.pause(120)
#mpf.plot(backtest[0:100])

