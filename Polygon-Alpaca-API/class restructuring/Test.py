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

#Warmup all tickers
#AAPL.warmUp() 
#AAPL.getStatus()

#TSLA.warmUp()
#TSLA.getStatus()

#MSFT.warmUp()
#MSFT.getStatus()

data = DB.QueryLast("MSFT", number = 1)
data1 = DB.QueryDate("MSFT", "2021-01-05", "2021-01-07")
print(data)
print(data1)