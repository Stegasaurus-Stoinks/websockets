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
ib.connect(host='127.0.0.1', port=7496, clientId=2)

for position in ib.trades():
    print(position.contract.symbol + " " + str(position.contract.strike) + str(position.contract.right) + " " + str(position.contract.lastTradeDateOrContractMonth))
    
    if position.orderStatus.status == "Filled":
    #    for x in position.log:
    #        print(str(x[2]))
        for fill in position.fills:
            print(str(fill.execution.permId) + " : Fill {} @ {}".format(str(fill.execution.cumQty),str(fill.execution.avgPrice)))
        #log=[TradeLogEntry(time=datetime.datetime(2021, 5, 17, 16, 12, 7, tzinfo=datetime.timezone.utc), status='Filled', message='Fill 8.0@6.7')])
    else:
        print(position.orderStatus.status)

    #print(position)
    print("____________________________________________________________________________________")
print(position)
print("")

for order in ib.orders():
    if order.permId == 93162526:
        print(order)
num = 0
for execution in ib.executions():
    if execution.permId == 93162526:
        print(execution)
    if execution.orderId == 450:
        print(execution)
    num += 1

print(num)

num = 0
for order in ib.orders():
    if order.action == 'SELL':
        print(order)
        num += 1

print(num)

QueryID = 554350



ib.sleep(5)

test = """Trade(
contract=Option(conId=404743330, symbol='VIAC', lastTradeDateOrContractMonth='20210618', strike=45.0, right='C', multiplier='100', exchange='SMART', currency='USD', localSymbol='VIAC  210618C00045000', tradingClass='VIAC'), 
order=Order(permId=93162526, action='BUY', orderType='LMT', lmtPrice=0.6000000000000001, auxPrice=0.0, tif='DAY', ocaType=3, trailStopPrice=1.6, volatilityType=2, deltaNeutralOrderType='None', referencePriceType=0, account='DU1942072', clearingIntent='IB', cashQty=0.0, dontUseAutoPriceForHedge=True, filledQuantity=42.0, refFuturesConId=2147483647, shareholder='Not an insider or substantial shareholder', parentPermId=9223372036854775807), 
orderStatus=OrderStatus(orderId=0, status='Filled', filled=0, remaining=0, avgFillPrice=0.0, permId=0, parentId=0, lastFillPrice=0.0, clientId=0, whyHeld='', mktCapPrice=0.0), 

fills=[Fill(contract=Option(conId=404743330, symbol='VIAC', lastTradeDateOrContractMonth='20210618', strike=45.0, right='C', multiplier='100', exchange='SMART', currency='USD', localSymbol='VIAC  210618C00045000', tradingClass='VIAC'), 
execution=Execution(execId='00020056.60a2098a.01.01', time=datetime.datetime(2021, 5, 17, 14, 59, 36, tzinfo=datetime.timezone.utc), acctNumber='DU1942072', exchange='PHLX', side='BOT', shares=30.0, price=0.6, permId=93162526, clientId=1, orderId=450, liquidation=0, cumQty=30.0, avgPrice=0.6, orderRef='', evRule='', evMultiplier=0.0, modelCode='', lastLiquidity=2), 
commissionReport=CommissionReport(execId='00020056.60a2098a.01.01', commission=21.984, currency='USD', realizedPNL=0.0, yield_=0.0, yieldRedemptionDate=0), 
time=datetime.datetime(2021, 5, 17, 14, 59, 36, tzinfo=datetime.timezone.utc)), 

Fill(contract=Option(conId=404743330, symbol='VIAC', lastTradeDateOrContractMonth='20210618', strike=45.0, right='C', multiplier='100', exchange='SMART', currency='USD', localSymbol='VIAC  210618C00045000', tradingClass='VIAC'), execution=Execution(execId='00020056.60a2098b.01.01', time=datetime.datetime(2021, 5, 17, 14, 59, 36, tzinfo=datetime.timezone.utc), 
acctNumber='DU1942072', exchange='BOX', side='BOT', shares=7.0, price=0.6, permId=93162526, clientId=1, orderId=450, liquidation=0, cumQty=37.0, avgPrice=0.6, orderRef='', evRule='', evMultiplier=0.0, modelCode='', lastLiquidity=2), 
commissionReport=CommissionReport(execId='00020056.60a2098b.01.01', commission=5.1296, currency='USD', realizedPNL=0.0, yield_=0.0, yieldRedemptionDate=0), 
time=datetime.datetime(2021, 5, 17, 14, 59, 36, tzinfo=datetime.timezone.utc)), 

Fill(contract=Option(conId=404743330, symbol='VIAC', lastTradeDateOrContractMonth='20210618', strike=45.0, right='C', multiplier='100', exchange='SMART', currency='USD', localSymbol='VIAC  210618C00045000', tradingClass='VIAC'), execution=Execution(execId='00020056.60a2098c.01.01', time=datetime.datetime(2021, 5, 17, 14, 59, 36, tzinfo=datetime.timezone.utc), 
acctNumber='DU1942072', exchange='MIAX', side='BOT', shares=5.0, price=0.6, permId=93162526, clientId=1, orderId=450, liquidation=0, cumQty=42.0, avgPrice=0.6, orderRef='', evRule='', evMultiplier=0.0, modelCode='', lastLiquidity=2), 
commissionReport=CommissionReport(execId='00020056.60a2098c.01.01', commission=3.664, currency='USD', realizedPNL=0.0, yield_=0.0, yieldRedemptionDate=0), 
time=datetime.datetime(2021, 5, 17, 14, 59, 36, tzinfo=datetime.timezone.utc))], 

log=[TradeLogEntry(time=datetime.datetime(2021, 5, 17, 14, 59, 36, tzinfo=datetime.timezone.utc), status='Filled', message='Fill 30.0@0.6'), TradeLogEntry(time=datetime.datetime(2021, 5, 17, 14, 59, 36, tzinfo=datetime.timezone.utc), status='Filled', message='Fill 7.0@0.6'), TradeLogEntry(time=datetime.datetime(2021, 5, 17, 14, 59, 36, tzinfo=datetime.timezone.utc), status='Filled', message='Fill 5.0@0.6')])"""