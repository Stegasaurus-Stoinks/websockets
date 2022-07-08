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
#AAPL = Ticker("AAPL", "Stock", DB)
#MSFT = Ticker("MSFT", "Stock", DB)  
#TSLA = Ticker("TSLA", "Stock", DB)

#AAPL = Ticker("AAPL", "Stock", DB, startDate='2022-07-05', endDate='2022-07-08',datasize=75)
#MSFT = Ticker("MSFT", "Stock", DB, startDate='2021-01-04', endDate='2021-01-14')  
TSLA = Ticker("TSLA", "Stock", DB, startDate='2022-07-05', endDate='2022-07-08',datasize=200)


#Warmup all tickers
#AAPL.warmUp() 
#AAPL.getStatus()

TSLA.warmUp()
TSLA.getStatus()

#MSFT.warmUp()
#MSFT.getStatus()

#######Initialize all algos for the day#######
#momentum1 = MomentumAlgo(AAPL, "testy", 2, api)
 
EMAalgo = AlgoEMA(TSLA, "ThreeKings", 9, api, False, 40, 10 , plotting = True,plotSize=199)
# AAPLalgo1 = AlgoSupport2(TSLA, "MomentumEMA", 2, api, live = False, plotting = True,plotSize = 75)
#AAPLalgo1 = AlgoHigherLows(TSLA, "MomentumEMA", 2, api, live = False, plotting = True,plotSize = 75)

#AAPLalgo1 = AlgoSupport2(AAPL, "MomentumEMA", 2, api, live = False, plotting = True,plotSize = 75)
#ElliotAlgo = AlgoElliotWave(AAPL, "ElliotWaves", 2, api, live = False, plotting = True,plotSize = 199)

while 1:

    DB.awaitNewData()

    #AAPL.update()
    #AAPL.getStatus()

    TSLA.update()
    #TSLA.getStatus()

    #MSFT.update()
    #MSFT.getStatus()
    
    
    #time.sleep(0.1)
    EMAalgo.update()
    #AAPLalgo1.update()
    #AAPLalgo2.update()
    #AAPLalgo3.update()
    
    #quit()
