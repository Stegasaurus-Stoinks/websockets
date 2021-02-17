#inside imports
from trade import Trade
from datetime import datetime
from algo import Algo
#outside imports
import select, time, requests, json, sys
import psycopg2
import psycopg2.extensions
import config
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import alpaca_trade_api as tradeapi
import keystore
import numpy as np
import pytz

#Import Functions and Indicators
from Algo_Functions import IsDownTrend,formatTime,Calc_EMA,plotter

class MomentumAlgo(Algo):

    def __init__(self, ticker, name, risklevel, tradeapi, live):
        Algo.__init__(self, ticker, name, risklevel, tradeapi, live)
        self.NewData
        self.highest

        #------Config Variables------
        self.Live_Trading = True
        self.notify_channel = "amdata"

        #Start_time = datetime(2021, 1, 29, 17, 40, 0) 
        self.Start_time = datetime.utcnow()
        self.End_time = datetime(2020, 11, 18, 18, 30, 0)

        self.Current_time = self.Start_time

        self.EMA1 = 0
        self.EMA2 = 0
        self.entry_price = 100
        self.exit_price = 100
        self.upTrade = False
        self.missing_data = 0
        self.number_of_trades = 0
        self.good_trades = 0
        self.bad_trades = 0

        self.stop_loss = 0.002
        self.profit = 0

        #----------------------------
        self.utc=pytz.UTC
        self.Start_time = utc.localize(Start_time) 
        self.NewData = False
        self.AM_candlesticks = []
        self.close_data = []
        self.Current_time = datetime(2020, 11, 18, 18, 11, 0)
        self.Next_time = datetime(2020, 11, 18, 18, 11, 0)
        self.in_position = False

        self.DAY_START_TIME = Start_time.replace(hour=14, minute=30)
        self.DAY_END_TIME = Start_time.replace(hour=21, minute=00)


    def update(self):
        if(self.Live_Trading):
            AwaitNewData() 
        #Breaks out to the code below if a notify is recieved on the above defined "notify_channel"
        #------------Add code Below Here----------
        if(not self.Live_Trading):
            try:
                data = QuerySpecificData(self.ticker, self.Current_time)
                UpdateDataArray(data)
                #O = AM_candlesticks[-1]['open']

            except (IndexError):
                print("missing data")
                self.missing_data += 1
                Current_time = Current_time + timedelta(minutes=1)


        if(self.Live_Trading):
            UpdateDataArray(QueryData(self.ticker))
            Current_time = self.AM_candlesticks[-1]['dtime']

        #print(Current_time)
        #print(DAY_END_TIME)
        #print(DAY_START_TIME)
        if(ValidTradingHours(Current_time)):

            C = self.AM_candlesticks[-1]['close']

            if EMA1 == 0:
                EMA1 = C
                EMA2 = C

            EMA1 = Calc_EMA(20,C,EMA1)
            EMA2 = Calc_EMA(50,C,EMA2)
            #print(O, C)

            #getting first EMA point :D
            if len(self.AM_candlesticks) == 2:
                if EMA1 > EMA2:
                    highest = 1
                else:
                    highest = 2

            print(highest)

            if self.in_position:
                if not self.upTrade:
                    #calculate trailing stop loss
                    temp = C + (C * self.stop_loss)
                    if temp < exit_price:
                        exit_price = temp
                    
                    #if C > exit_price:
                    if EMA1 > EMA2 or not ValidTradingHours(Current_time, -3):
                        in_position = False
                        Sell_Position()
                        self.number_of_trades += 1
                        profit = profit + (self.entry_price - self.exit_price)
                        print("Exited Trade at " + str(exit_price))
                        print("Trade profit: " + str(self.entry_price - exit_price))
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
                    if EMA2 > EMA1 or not ValidTradingHours(Current_time, -5):
                        in_position = False
                        Sell_Position()
                        number_of_trades += 1
                        profit = profit + (self.exit_price - self.entry_price)
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
                        in_position = True
                        upTrade = True
                        entry_price = C
                        exit_price = C - (C * stop_loss)
                        print("EMA Cross: upTrade placed! Entry Price: " + str(entry_price))
                        place_order(entry_price, 10)

                    if (EMA1 < EMA2) and (highest == 1):
                        highest = 2
                        in_position = True
                        upTrade = False
                        entry_price = C
                        exit_price = C + (C * self.stop_loss)
                        print("EMA Cross: downTrade placed! Entry Price: " + str(entry_price))
                        place_order(entry_price, -10)


            if(not self.Live_Trading):
                Current_time = Current_time + timedelta(minutes=1)

            #print(Current_time)
            self.NewData = False

        if (Current_time > self.DAY_END_TIME):
            print("DONE!")
            print("# of trades: " + str(number_of_trades))
            print("Good trades: " + str(good_trades) + " | Bad trades: " + str(bad_trades))
            print("Total Profit: " + str(profit))
            print("missing data: " + str(missing_data))
            time.sleep(10)
            quit()
        #print("Notify Recieved")
        #UpdateDataArray(QueryData(ticker))
        #print(AM_candlesticks)