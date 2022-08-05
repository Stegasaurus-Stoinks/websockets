import sys
sys.path.append('../')

from algos.algo_EMA import Algo as AlgoEMA
from algos.algo_Support import Algo as AlgoSupport
from algos.algo_Support2 import Algo as AlgoSupport2
from algos.trend.algo_Trendlines import Algo as AlgoTrend
from algos.trend.algo_higherlows import Algo as AlgoHigherLows
from algos.elliot.algo_Elliot import Algo as AlgoElliotWave
from extra.ticker import Ticker
from extra.database import Database
from IBKR.ibkrApi import ibkrApi as ibkr
from extra.plotter import LiveChartEnv

from mplfinance import plotting
from datetime import datetime

#------Config Variables------
Trading = True
BackTest = False
#----------------------------

DB = Database(BackTest)

#-----------------------
#starting IBKR API
#-----------------------
try:
    ib = ibkr()
    #ib.orderStatusEvent += onOrderUpdate
    ib.connect(host='127.0.0.1', port=7496, clientId=1)
    Trading = True

    try:
        mintickrule = ib.reqMarketRule(110)
        print(mintickrule)
        rulelowthresh = float(mintickrule[0][0])
        rulelowtick = float(mintickrule[0][1])
        rulehighthresh = float(mintickrule[1][0])
        rulehightick = float(mintickrule[1][1])


    except:
        rulelowthresh = float(0)
        rulelowtick = float(.05)
        rulehighthresh = float(3.00)
        rulehightick = float(0.1)

except:
    print(
        "--------------------------------------------------------------------------------------------------------------------------------")
    print(
        "Trading offline: There was a problem connecting to IB. Make sure Trader Workstation is open and try restarting the python script")
    print(
        "--------------------------------------------------------------------------------------------------------------------------------")
    Trading = False

#-----------------------
#End of IBKR API startup
#-----------------------
#Initiaiize all relevant tickers for the day
#AAPL = Ticker("AAPL", "Stock", DB)
#MSFT = Ticker("MSFT", "Stock", DB)  
#TSLA = Ticker("TSLA", "Stock", DB)

AAPL = Ticker("AAPL", "Stock", DB, 200, '2021-01-08', '2021-01-09')
#MSFT = Ticker("MSFT", "Stock", DB, startDate='2021-01-04', endDate='2021-01-14')  
#TSLA = Ticker("TSLA", "Stock", DB, startDate='2021-01-04', endDate='2021-01-14')


#Warmup all tickers
AAPL.warmUp() 
AAPL.getStatus()

#TSLA.warmUp()
#TSLA.getStatus()

#MSFT.warmUp()
#MSFT.getStatus()

#######Initialize all algos for the day#######

 
#EMAalgo = AlgoEMA(TSLA, "ThreeKings", 9, api, False, 40, 10 , plotting = True,plotSize=199)
# AAPLalgo1 = AlgoSupport2(TSLA, "MomentumEMA", 2, api, live = False, plotting = True,plotSize = 75)
#AAPLalgo1 = AlgoHigherLows(TSLA, "MomentumEMA", 2, api, live = False, plotting = True,plotSize = 75)

#AAPLalgo1 = AlgoSupport2(AAPL, "MomentumEMA", 2, api, live = False, plotting = True,plotSize = 75)
ElliotAlgo = AlgoElliotWave(AAPL, "ElliotWaves", 2, ib, live = not BackTest, plotting = True,plotSize = 200)

while 1:

    DB.awaitNewData()

    #AAPL.update()
    #AAPL.getStatus()

    TSLA.update()
    #TSLA.getStatus()

    #MSFT.update()
    #MSFT.getStatus()
    
    
    #time.sleep(0.1)
    start = datetime.now()
    ElliotAlgo.update()
    stop = datetime.now()
    #print(stop-start)
    #AAPLalgo1.update()
    #AAPLalgo2.update()
    #AAPLalgo3.update()
    
    #quit()
