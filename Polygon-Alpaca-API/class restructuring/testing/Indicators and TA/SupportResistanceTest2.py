import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

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
plotSize =300
#----------------------------

DB = Database(BackTest)
api = TradeApi(Trading, Live_Trading)
#Initiaiize all relevant tickers for the day

#pick from {CCL, AAPL, MSFT, HD, NFLX, GOOG, TSLA, VZ, INTC, AMZN, FB}
AAPL = Ticker("AAPL", "Stock", DB, startDate='2021-01-08', endDate='2021-01-09')
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
print(backtest.head())

#Calculating mins and maxs
n = 1 #Adjust this to add more or less mins and maxs (2 was the best one I found for short term)
ilocs_min = argrelextrema(backtest.low.values, np.less_equal, order=n)[0]
ilocs_max = argrelextrema(backtest.high.values, np.greater_equal, order=n)[0]

n = 3 #Adjust this to add more or less mins and maxs (2 was the best one I found for short term)
ilocs_min2 = argrelextrema(backtest.low.values, np.less_equal, order=n)[0]
ilocs_max2 = argrelextrema(backtest.high.values, np.greater_equal, order=n)[0]

mins = [np.NaN] * plotSize
#mins2 = [np.NaN] * plotSize
minsadj = [np.NaN] * plotSize
for i in range (0,len(ilocs_min)):
    mins[ilocs_min[i]] = backtest.iloc[ilocs_min[i]].low
    #mins2[ilocs_min[i]] = backtest.iloc[ilocs_min2[i]].low
    minsadj[ilocs_min[i]] = backtest.iloc[ilocs_min[i]].low * 0.999

maxs = [np.NaN] * plotSize
#maxs2 = [np.NaN] * plotSize
maxsadj = [np.NaN] * plotSize
for i in range (0,len(ilocs_max)):
    maxs[ilocs_max[i]] = backtest.iloc[ilocs_max[i]].high
    #maxs2[ilocs_max[i]] = backtest.iloc[ilocs_max2[i]].high
    maxsadj[ilocs_max[i]] = backtest.iloc[ilocs_max[i]].high * 1.001


reach = 20
possibleWaves = []
counter = 0

supportlines = []
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
        
        line,score = SupportResistanceFunc.createline(slope,x1,point1,x2,point2,backtest.low.values,ilocs_min,plotSize)
        #print(score)
        if score >= 3:
            supportlines.append((slope,x1,point1,x2,point2,line))
            #extraplots.append(plotting.make_addplot(line,ax=ax1))
             
#print(supportlines)
lineremoved = 0
for mainline in supportlines:
    #format of line is [slope,x1,y1,x2,y2,line]
    start = mainline[1]
    for extraline in supportlines:
        #print(mainline)
        slope1 = round(extraline[0],3)
        slope2 = round(mainline[0],3)
        if extraline[1] == start and slope1 == slope2:
            try:
                supportlines.remove(mainline)
                lineremoved += 1
            except:
                print("couldnt remove line")
                print(line)

#print(supportlines)
#print(lineremoved)
for line in supportlines:
    extraplots.append(plotting.make_addplot(line[5],ax=ax1))

mins2 = [np.NaN] * plotSize
maxs2 = [np.NaN] * plotSize

for i in range (0,len(ilocs_min2)):
    mins2[ilocs_min2[i]] = backtest.iloc[ilocs_min2[i]].low

for i in range (0,len(ilocs_max2)):
    maxs2[ilocs_max2[i]] = backtest.iloc[ilocs_max2[i]].high

for j in range(0,len(ilocs_min2)):
    for max in ilocs_max2:
        try:
            if ilocs_min2[j]<max<ilocs_min2[j+1]:
                if mins[ilocs_min2[j]]<mins[ilocs_min2[j+1]]<maxs[max]:
                    uptrace = maxs[max] - mins[ilocs_min2[j]]
                    downtrace = maxs[max] - mins[ilocs_min2[j+1]]
                    ratio = downtrace/uptrace
                    if 0.5 < ratio < 0.717:
                        print("possible valid setup @",backtest.index.values[ilocs_min2[j+1]], "with retracement ratio of", ratio)
        except:
            print("something wong")

# for i in range(0,len(ilocs_max)-reach):
#     for x in range(i+1,i+reach):
#         x1 = ilocs_max[i]
#         x2 = ilocs_max[x]
#         point1 = maxs[x1]
#         point2 = maxs[x2]
#         #plot line between the 2 points
#         slope = SupportResistanceFunc.calculateslope(x1,point1,x2,point2)
#         line = [np.NaN] * plotSize
#         for k in range(x1,x2+1):
#             line[k] = (point1-slope*x1)+(slope*k)
        
#         wiggle = 0.03
#         wiggle1 = wiggle
#         #check to make sure there are no lows in the range the invalidate the line
#         score = 0 #using this to rank the trend lines based on how many bounces bounce off the line
        
#         for j in range(x1,x2):
#             if line[j] >= backtest.high.values[j]-wiggle1:
#                 plot = True
#                 if line[j]-wiggle <= backtest.high.values[j] <= line[j]+wiggle:
#                     #score += 1
#                     if j in ilocs_max[i:x]:
#                         score+=1
#                         #print("found another min on the line")

#             else:
#                 plot = False
#                 break

#         if plot and score >= 3:
#             #print(line)
#             extraplots.append(plotting.make_addplot(line,ax=ax1))



#setup the figure and subplots

extraplots.append(plotting.make_addplot(minsadj,type='scatter',markersize=200,marker='^',ax=ax1))
extraplots.append(plotting.make_addplot(maxsadj,type='scatter',markersize=200,marker='v',color='b',ax=ax1))

extraplots.append(plotting.make_addplot(mins2,type='scatter',markersize=200,marker='.',ax=ax1))
extraplots.append(plotting.make_addplot(maxs2,type='scatter',markersize=200,marker='.',color='b',ax=ax1))

mpf.plot(backtest,type='candle',style='charles',addplot= extraplots,warn_too_much_data=10000000000,ax=ax1, volume=ax2)
plt.show()
plt.pause(120)
#mpf.plot(backtest[0:100])

