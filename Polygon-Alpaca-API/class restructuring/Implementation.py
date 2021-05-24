#import sys
#sys.path.append('../')

from mplfinance import plotting
from . algos.algo_EMA import Algo as AlgoEMA
#from algos.algo_Trendlines import Algo as AlgoTrendlines
#from ..algos.MomentumAlgo import MomentumAlgo

from extras.ticker import Ticker
from extras.database import Database
from extras.tradeApi import TradeApi
from extras.plotter import LiveChartEnv


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
TSLA = Ticker("TSLA", "Stock", DB)

#Warmup all tickers
AAPL.warmUp() 
#AAPL.getStatus()

TSLA.warmUp()
#TSLA.getStatus()

#######Initialize all algos for the day#######
#momentum1 = MomentumAlgo(AAPL, "testy", 2, api)
 
AAPLalgo1 = AlgoEMA(TSLA, "ThreeKings", 9, api, False, 50, 20, plotting = True)
#AAPLalgo2 = AlgoEMA(AAPL, "ThreeKings", 9, api, False, 50, 20)
#AAPLalgo3 = AlgoEMA(AAPL, "ThreeKings", 9, api, False, 50, 30)
#AAPLalgo1 = AlgoEMA(AAPL, "ThreeKings", 9, api, False, 40, 10 , plotting = True)
#AAPLalgo1 = AlgoTrendlines(AAPL, "MomentumEMA", 2, api, live = False, plotting = True)

while 1:

    DB.awaitNewData()

    AAPL.update()
    #AAPL.getStatus()

    TSLA.update()
    #TSLA.getStatus()
    
    
    #time.sleep(0.1)

    AAPLalgo1.update()
    #AAPLalgo2.update()
    #AAPLalgo3.update()
    
    #quit()
