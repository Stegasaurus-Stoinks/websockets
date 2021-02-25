from algo_SMA import Algo as AlgoSMA
from algo_Trendlines import Algo as AlgoTrendlines
from ticker import Ticker
from database import Database
from tradeApi import TradeApi
from plotter import LiveChartEnv

import time

#------Config Variables------
Trading = False
Live_Trading = False
BackTest = True
#----------------------------

DB = Database(BackTest)
Api = TradeApi(Trading, Live_Trading)

#Initiaiize all relevant tickers for the day
AAPL = Ticker("AAPL", "Stock", DB)

#Warmup all tickers
AAPL.warmUp()
AAPL.getStatus()

#Initialize all algos for the day
AAPLalgo1 = AlgoSMA(AAPL, "ThreeKings", 9, Api, live = False, plotting = False)
AAPLalgo2 = AlgoTrendlines(AAPL, "MomentumEMA", 2, Api, live = False, plotting = True)

while 1:
    DB.awaitNewData()

    AAPL.update()
    AAPL.getStatus()
    
    #time.sleep(0.01)

    AAPLalgo1.update()
    AAPLalgo2.update()
    
    #quit()
