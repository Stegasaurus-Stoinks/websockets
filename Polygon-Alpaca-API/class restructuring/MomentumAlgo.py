#inside imports
from trade import Trade
from datetime import datetime
from algo import Algo
import keystore
from ticker import Ticker

#outside imports
import select, time, requests, json, sys
import psycopg2
import psycopg2.extensions
import config
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import alpaca_trade_api as alpacaApi
import numpy as np
import pytz

#Import Functions and Indicators
from Algo_Functions import IsDownTrend,formatTime,Calc_EMA,plotter

class MomentumAlgo():

    """
    Risklevel = stop loss percentage
    """
    def __init__(self, ticker, name, risklevel, tradeapi):

        #------Config Variables------
        
        self.tradeID = name + ticker.symbol + str(risklevel)
        self.tickler = ticker
        self.api = tradeapi
        self.EMA1 = 0
        self.EMA2 = 0
        self.entry_price = 100
        self.exit_price = 100
        self.upTrade = False
        self.missing_data = 0
        self.number_of_trades = 0
        self.good_trades = 0
        self.bad_trades = 0
        self.curTrade = None
        self.stop_loss = (risklevel * 0.01)
        self.profit = 0
        
        self.highest = 0
        self.in_position = False

        #getting first EMA's and setting highest variable :D
        self.EMA1 = Calc_EMA(20,self.tickler.getData(),self.EMA1)
        self.EMA2 = Calc_EMA(50,self.tickler.getData(),self.EMA2)
        if self.EMA1 > self.EMA2:
            self.highest = 1
            print("EMA 1 is higher than EMA 2")
        else:
            self.highest = 2
            print("EMA 2 is higher than EMA 1")


    def update(self):
        time = datetime.now()
        AM_data = self.tickler.getData()
        
        #Breaks out to the code below if a notify is recieved on the above defined "notify_channel"
        #------------Add code Below Here----------

        C = AM_data['close']

        

        if self.curTrade.inPosition():

            if not self.upTrade:
                #calculate trailing stop loss
                temp = C + (C * self.stop_loss)
                if temp < self.exit_price:
                    self.exit_price = temp
                
                #if C > exit_price:
                if self.EMA1 > self.EMA2:
                    self.in_position = False
                    #Close Trade
                    self.curTrade.closePosition(self.exit_price, time)

                    self.number_of_trades += 1
                    profit = profit + (self.entry_price - self.exit_price)
                    print("Exited Trade at " + str(self.exit_price))
                    print("Trade profit: " + str(self.entry_price - self.exit_price))
                    print("Total Profit: " + str(profit))
                    if self.entry_price - self.exit_price > 0:
                        self.good_trades += 1

                    else:
                        self.bad_trades += 1
                
            else:
                #calculate trailing stop loss
                temp = C - (C * self.stop_loss)
                if temp > self.exit_price:
                    self.exit_price = temp

                #if C < exit_price:
                if self.EMA2 > self.EMA1:
                    self.in_position = False
                    #Close Trade
                    self.curTrade.closePosition(self.exit_price, time)

                    self.number_of_trades += 1
                    profit = profit + (self.exit_price - self.entry_price)
                    print("Trade profit: " + str(self.exit_price - self.entry_price))
                    print("Total Profit: " + str(profit))
                    if self.exit_price - self.entry_price > 0:
                        self.good_trades += 1

                    else:
                        self.bad_trades += 1

        else:

            #check if you need to enter position
            self.entry_price = C
            self.exit_price = C
            if (self.EMA1 > self.EMA2) and (self.highest == 2):
                self.highest = 1
                #Make trade
                volume = 10
                self.curTrade = Trade(self.tickler.symbol, volume, self.tradeID, 1.01, time, self.api, printInfo = True)

                self.upTrade = True
                self.entry_price = C
                self.exit_price = C - (C * self.stop_loss)
                print("EMA Cross: upTrade placed! Entry Price: " + str(self.entry_price))
                
                #trade = new trade
                self.in_position = True


            if (self.EMA1 < self.EMA2) and (self.highest == 1):
                self.highest = 2
                #Make trade
                volume = 10
                self.curTrade = Trade(self.tickler.symbol, volume, self.tradeID, 1.01, time, self.api, printInfo = True)

                self.upTrade = False
                self.entry_price = C
                self.exit_price = C + (C * self.stop_loss)
                print("EMA Cross: downTrade placed! Entry Price: " + str(self.entry_price))