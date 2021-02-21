from algo import Algo
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
AAPLalgo1 = Algo(AAPL, "ThreeKings", 9, Api, live = L)
AAPLalgo2 = Algo(AAPL, "MomentumEMA", 2, Api, live = True)

plot = LiveChartEnv("1min", 50)
plot.initialize_chart()

while 1:
    DB.awaitNewData()

    AAPL.update()
    AAPL.getStatus()

    plot.update_chart(AAPL.getData("FULL"))
    
    #time.sleep(0.01)

    #AAPLalgo1.update()
    #AAPLalgo2.update()
    
    #quit()
