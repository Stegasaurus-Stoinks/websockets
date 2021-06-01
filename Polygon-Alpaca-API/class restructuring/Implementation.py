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

MSFT.warmUp()
#MSFT.getStatus()

#######Initialize all algos for the day#######
#momentum1 = MomentumAlgo(AAPL, "testy", 2, api)
 
#AAPLalgo1 = AlgoEMA(TSLA, "ThreeKings", 9, api, False, 50, 20)
#AAPLalgo2 = AlgoEMA(AAPL, "ThreeKings", 9, api, False, 50, 20)
#AAPLalgo3 = AlgoEMA(AAPL, "ThreeKings", 9, api, False, 50, 30)
#AAPLalgo1 = AlgoEMA(AAPL, "ThreeKings", 9, api, False, 40, 10 , plotting = True)
AAPLalgo1 = AlgoSupport2(MSFT, "MomentumEMA", 2, api, live = False, plotting = False,plotSize = 75)
#AAPLalgo1 = AlgoTrend(AAPL, "MomentumEMA", 2, api, live = False, plotting = True,plotSize = 75)
#AAPLalgo1 = AlgoHigherLows(TSLA, "MomentumEMA", 2, api, live = False, plotting = True,plotSize = 75)

while 1:

    DB.awaitNewData()

    #AAPL.update()
    #AAPL.getStatus()

    #TSLA.update()
    #TSLA.getStatus()

    MSFT.update()
    #MSFT.getStatus()
    
    
    #time.sleep(0.1)

    AAPLalgo1.update()
    #AAPLalgo2.update()
    #AAPLalgo3.update()
    
    #quit()
