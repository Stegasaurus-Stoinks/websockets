from algo import Algo
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

#Warmup all tickers
AAPL.warmUp()
AAPL.getStatus()

#Initialize all algos for the day
AAPLalgo1 = Algo(AAPL, "ThreeKings", 9, api, live = True)
AAPLalgo2 = Algo(AAPL, "MomentumEMA", 2, api, live = True)
momentum1 = MomentumAlgo(AAPL, 2, api)

#plot = LiveChartEnv("1min", 50)
#plot.initialize_chart()

while 1:

    #Add ValidTradingHours here ************

    DB.awaitNewData()

    AAPL.update()
    AAPL.getStatus()

    #plot.update_chart(AAPL.getData("FULL"))
    
    #time.sleep(0.01)

    momentum1.update()
    #AAPLalgo1.update()
    #AAPLalgo2.update()
    
    #quit()
