from algo import Algo
from ticker import Ticker
from database import Database
from tradeApi import TradeApi

#------Config Variables------
Live_Trading = True
#----------------------------

DB = Database()
Api = TradeApi()

#Initiaiize all relevant tickers for the day
AAPL = Ticker("AAPL", "Stock", DB)

#Warmup all tickers
AAPL.warmUp()

#Initialize all algos for the day
AAPLalgo1 = Algo(AAPL, "ThreeKings", 9, Api, live = True)
AAPLalgo2 = Algo(AAPL, "MomentumEMA", 2, Api, live = True)


while 1:
    #DB.awaitNewData()

    AAPL.update()

    AAPLalgo1.update()
    AAPLalgo2.update()
    quit()
