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
    def __init__(self, ticker, risklevel, tradeapi):

        #------Config Variables------
        

        self.tickler = ticker

        self.EMA1 = 0
        self.EMA2 = 0
        self.entry_price = 100
        self.exit_price = 100
        self.upTrade = False
        self.missing_data = 0
        self.number_of_trades = 0
        self.good_trades = 0
        self.bad_trades = 0

        self.stop_loss = (risklevel * 0.01)
        self.profit = 0
        
        self.in_position = False



    def update(self):
        AM_data = self.tickler.getData()
        curTrade
        #Breaks out to the code below if a notify is recieved on the above defined "notify_channel"
        #------------Add code Below Here----------
       

        C = AM_data['close']

        if EMA1 == 0:
            EMA1 = C
            EMA2 = C

        EMA1 = Calc_EMA(20,C,EMA1)
        EMA2 = Calc_EMA(50,C,EMA2)
        #print(O, C)

        #getting first EMA point :D
        
        if EMA1 > EMA2:
            highest = 1
        else:
            highest = 2

        print(highest)

        if self.in_Position:
            if not self.upTrade:
                #calculate trailing stop loss
                temp = C + (C * self.stop_loss)
                if temp < exit_price:
                    exit_price = temp
                
                #if C > exit_price:
                if EMA1 > EMA2:
                    self.in_position = False
                    #Sell_Position()trade.close 
                    self.number_of_trades += 1
                    profit = profit + (self.entry_price - self.exit_price)
                    print("Exited Trade at " + str(exit_price))
                    print("Trade profit: " + str(self.entry_price - self.exit_price))
                    print("Total Profit: " + str(profit))
                    if entry_price - exit_price > 0:
                        self.good_trades += 1

                    else:
                        self.bad_trades += 1
                
            else:
                #calculate trailing stop loss
                temp = C - (C * self.stop_loss)
                if temp > exit_price:
                    exit_price = temp

                #if C < exit_price:
                if EMA2 > EMA1:
                    self.in_position = False
                    #Sell_Position()
                    self.number_of_trades += 1
                    profit = profit + (exit_price - entry_price)
                    print("Trade profit: " + str(self.exit_price - self.entry_price))
                    print("Total Profit: " + str(profit))
                    if exit_price - entry_price > 0:
                        self.good_trades += 1

                    else:
                        self.bad_trades += 1

        else:
            if len(api.list_positions()) == 0:
                #check if you need to enter position
                entry_price = C
                exit_price = C

                if (EMA1 > EMA2) and (highest == 2):
                    highest = 1
                    
                    self.upTrade = True
                    entry_price = C
                    exit_price = C - (C * self.stop_loss)
                    print("EMA Cross: upTrade placed! Entry Price: " + str(entry_price))
                    
                    trade = new trade
                    self.in_position = True

                    #place_order(entry_price, 10)

                if (EMA1 < EMA2) and (highest == 1):
                    highest = 2
                    self.in_position = True
                    self.upTrade = False
                    entry_price = C
                    exit_price = C + (C * self.stop_loss)
                    print("EMA Cross: downTrade placed! Entry Price: " + str(entry_price))
                    #place_order(entry_price, -10)