from ib_insync import *

def orderfilled(trade, fill):
    print("order has been filled")
    print(trade)
    print(fill)

def closePosition(ib, position, price = 0, percent=1.00):
    position.contract.exchange = 'SMART'
    numShares = round(percent * position.position)
    if numShares == 0:
        return

    if price == 0:
        sellOrder = MarketOrder('SELL', numShares)

    else:
        sellOrder = LimitOrder('SELL', numShares, price)

    sell = ib.placeOrder(position.contract,sellOrder)
    print(sell)
    sell.fillEvent += orderfilled   

def openPosition(ib, ticker, strike, date, direction, quantity, price = 0):
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