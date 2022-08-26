from ib_insync import *
import time
import pandas as pd
import numpy as np
#pd.set_option("display.max_rows", None, "display.max_columns", None)

def orderfilled(trade, fill):
    print("order has been filled")
    print(trade)
    print(fill)

def closePosition(position, price = 0, percent=1.00):
    position.contract.exchange = 'SMART'
    numShares = round(percent * position.position)
    if numShares == 0:
        numShares = 1

    if price == 0:
        sellOrder = MarketOrder('SELL', numShares)

    else:
        sellOrder = LimitOrder('SELL', numShares, price)

    sell = ib.placeOrder(position.contract,sellOrder)
    print(sell)
    sell.fillEvent += orderfilled
    

def openPosition(ticker, strike, date, direction, quantity, price = 0):
    #ticker: 'AAPL'
    #strike: int
    #date: '20210430' = 'YYYYMMDD'
    #direction: 'C' or 'P'
    #quantity: int
    #price: float

    call_option = Option(symbol = ticker,lastTradeDateOrContractMonth = date, strike=strike, right = direction, exchange='SMART', currency='USD')
    if price == 0:
        buyOrder = MarketOrder('BUY', quantity)

    else:
        buyOrder = LimitOrder('BUY', quantity, price)

    trade = ib.placeOrder(call_option,buyOrder)

    print(trade)



dataNotNeeded = ['contract',"minTick",'orderTypes','validExchanges','priceMagnifier','underConId','longName','nextOptionPartial','convertible','tradingHours','liquidHours','evMultiplier','mdSizeMultiplier','aggGroup','underSymbol','underSecType','marketRuleIds','secIdList','contractMonth','evRule','coupon','lastTradeTime','callable','putable']

ib = IB()
ib.connect(host='127.0.0.1', port=7496, clientId=1)

#data = ib.contract.Option('SPY', '20210319', 240, 'C', 'SMART')

aapl = Option(symbol = 'AAPL',lastTradeDateOrContractMonth = '20210423', right = 'C', exchange='SMART', currency='USD')

data = ib.reqContractDetails(aapl)

#time.sleep(1)

length = len(data)

strikes = [0 for x in range(length)]
for i in range(length):
    strikes[i] = data[i].contract.strike
    

#u_strikes_r = np.asarray(strikes)
#strike_r = np.sort(u_strikes_r)

#print(strike_r)

call_option = Option(symbol = 'AAPL',lastTradeDateOrContractMonth = '20210430', strike=140, right = 'C', exchange='SMART', currency='USD')
call_quote = ib.reqMktData(call_option,"",True,False)
#print(str(call_quote.bid) + " : " + str(call_quote.ask))
#print(call_quote)

#stock = Stock('AAPL', 'SMART', 'USD')

#order = LimitOrder('BUY', 5, 1.75)
#order = MarketOrder('BUY', 10)

#trade = ib.placeOrder(call_option,order)

#print(trade)



#trade = ib.placeOrder(call_option,order)
#print(trade)
#trade.fillEvent += orderfilled
#ib.sleep(5)

#openPosition('AAPL', 132, '20210423', 'P', 20)



print("these are all my postions")
for position in ib.positions():
    print("-------------------------------------")
    print(position)

    if position.contract.symbol == 'AAPL' and position.contract.strike == 132 and position.contract.right == 'P':
        closePosition(position,percent=.5)

        print(position.contract.conId)
        #sellorder = MarketOrder('SELL', position.position)
        #position.contract.exchange = 'SMART'
        #sell = ib.placeOrder(position.contract,sellorder)
        #print(sell)

#print("these are all my trades")
#for trades in ib.trades():
#    print("-------------------------------------")
#    print(trades.contract.conId)


ib.run()
#data = pd.DataFrame(data)
#data.drop('contract')
#for col in data.columns:
#    if col in dataNotNeeded:
#        del data[col]
#        
#    else:
#        print(col)
#print(data)



