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

ib = IB()
ib.connect(host='127.0.0.1', port=7496, clientId=1)


openPosition('TSLA', 715, '20210423', 'P', 10, price=6.5)

print("These are all my current postions")
for position in ib.positions():
    print("-------------------------------------")
    print(position)

    if position.contract.symbol == 'TSLA' and position.contract.strike == 712 and position.contract.right == 'P':
        closePosition(position,percent=1,price=8)
        print(position.contract.conId)


ib.run()