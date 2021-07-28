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


import time

#------Config Variables------
Trading = False
Live_Trading = False
BackTest = True
#----------------------------

DB = Database(BackTest)
api = TradeApi(Trading, Live_Trading)
#Initiaiize all relevant tickers for the day
AAPL = Ticker("AAPL", "Stock", DB)
MSFT = Ticker("MSFT", "Stock", DB)  
TSLA = Ticker("TSLA", "Stock", DB)

AAPL.warmUp()

backtest = AAPL.BackTestAM_candlesticks
backtest = backtest.sort_index(ascending=True)
#print(backtest)
#print(len(backtest))

backtest = backtest[start:start + plotSize]

#fig = mpf.figure(figsize=(7,8))

#Calculating mins and maxs
n = 20 #Adjust this to add more or less mins and maxs (2 was the best one I found for short term)
ilocs_min = argrelextrema(backtest.close.values, np.less_equal, order=n)[0]
ilocs_max = argrelextrema(backtest.close.values, np.greater_equal, order=n)[0]
ilocs_min_waves = argrelextrema(backtest.close.values, np.less_equal, order=5)[0]
ilocs_max_waves = argrelextrema(backtest.close.values, np.greater_equal, order=5)[0]

print(ilocs_min)

mins = [np.NaN] * plotSize
for i in range (0,len(ilocs_min)):
    mins[ilocs_min[i]] = backtest.iloc[ilocs_min[i]].close * 0.999

mins_waves = [np.NaN] * plotSize
for i in range (0,len(ilocs_min_waves)):
    mins_waves[ilocs_min_waves[i]] = backtest.iloc[ilocs_min_waves[i]].close * 0.999

maxs_waves = [np.NaN] * plotSize
for i in range (0,len(ilocs_max_waves)):
    maxs_waves[ilocs_max_waves[i]] = backtest.iloc[ilocs_max_waves[i]].close * 1.001


maxs = [np.NaN] * plotSize
for i in range (0,len(ilocs_max)):
    maxs[ilocs_max[i]] = backtest.iloc[ilocs_max[i]].close * 1.001

print(mins)
extraplots = []
extraplots.append(plotting.make_addplot(mins,type='scatter',markersize=200,marker='^'))
extraplots.append(plotting.make_addplot(maxs,type='scatter',markersize=200,marker='v'))
extraplots.append(plotting.make_addplot(mins_waves,type='scatter',markersize=200,marker='.'))
extraplots.append(plotting.make_addplot(maxs_waves,type='scatter',markersize=200,marker='.',color='red'))
mpf.plot(backtest,type='candle',style='charles',addplot= extraplots)
plt.show()
plt.pause(60)
#mpf.plot(backtest[0:100])

data = DB.QueryLast("MSFT", number = 1)
data1 = DB.QueryDate("MSFT", "2021-01-05", "2021-01-07")
print(data)
print(data1)