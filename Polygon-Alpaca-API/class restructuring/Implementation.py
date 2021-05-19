from algo_SMA import Algo as AlgoSMA
from algo_Trendlines import Algo as AlgoTrendlines
from algo_Template import Algo as AlgoTemplate
from ticker import Ticker
from database import Database
from tradeApi import TradeApi
from plotter import LiveChartEnv
from MomentumAlgo import MomentumAlgo

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
AAPL.getStatus()

#TSLA.warmUp()
#TSLA.getStatus()

#######Initialize all algos for the day#######
#momentum1 = MomentumAlgo(AAPL, "testy", 2, api)

AAPLalgo1 = AlgoSMA(AAPL, "ThreeKings", 9, api, live = False, plotting = True)
#AAPLalgo1 = AlgoTrendlines(AAPL, "MomentumEMA", 2, api, live = False, plotting = True)

while 1:

    DB.awaitNewData()

    AAPL.update()
    AAPL.getStatus()

    #TSLA.update()
    #TSLA.getStatus()
    
    
    time.sleep(0.1)

    AAPLalgo1.update()
    #AAPLalgo2.update()
    
    #quit()
