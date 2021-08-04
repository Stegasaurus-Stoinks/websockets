from ib_insync import *
ib = IB()
ib.connect('127.0.0.1', 7496, clientId=1)

def position_status(position):
    print("Working")

def order_status(trade):
    if trade.orderStatus.status == 'Filled':
        fill = trade.fills[-1]
        print("HERE")
        print(f'{fill.time} - {fill.execution.side} {fill.contract.symbol} {fill.execution.shares} @ {fill.execution.avgPrice}')


nflx_order = MarketOrder('BUY', 100)
nflx_contract = Stock('NFLX', 'SMART', 'USD')
trade = ib.placeOrder(nflx_contract, nflx_order)

#trade.fillEvent += order_status

ib.positionEvent += position_status

ib.run()

