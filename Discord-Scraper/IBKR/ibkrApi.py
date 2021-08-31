from ib_insync import *
import time
import pandas as pd
import numpy as np


class ibkrApi(IB):
    pass
    #unique id so find trades that have been placed by this algo


    def orderfilled(trade, fill):
        print("------------------order has been filled")
        print(trade)
        print(fill)

    def closePosition(self, position, price = 0, percent=1.00):
        position.contract.exchange = 'SMART'
        numShares = round(percent * position.position)
        if numShares == 0:
            return   
        if price == 0:
            sellOrder = MarketOrder('SELL', numShares)

        else:
            sellOrder = LimitOrder('SELL', numShares, price)

        sell = self.placeOrder(position.contract,sellOrder)
        print(sell)
        sell.fillEvent += self.orderfilled   

    def openPosition(self, ticker, strike, date, direction, quantity, price = 0):
        #ticker: 'AAPL'
        #strike: int
        #date: '20210430' = 'YYYYMMDD'
        #direction: 'C' or 'P'
        #quantity: int
        #price: float
        if quantity == 0:
            return
        call_option = Option(symbol = ticker,lastTradeDateOrContractMonth = date, strike=strike, right = direction, exchange='SMART', currency='USD')
        if price == 0:
            buyOrder = MarketOrder('BUY', quantity) 

        else:
            buyOrder = LimitOrder('BUY', quantity, price)

        trade = self.placeOrder(call_option,buyOrder)


    #Generate new list of positions
    def refresh(self):
        positions = self.positions()
        return positions