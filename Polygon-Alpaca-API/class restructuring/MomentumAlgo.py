#inside imports
from trade import Trade
from datetime import datetime
from algo import Algo
import keystore

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
        utc=pytz.UTC
        self.Start_time = utc.localize(self.Start_time) 
        self.NewData = False
        self.AM_candlesticks = []
        self.close_data = []
        self.Current_time = datetime(2020, 11, 18, 18, 11, 0)
        self.Next_time = datetime(2020, 11, 18, 18, 11, 0)
        self.in_position = False

        self.DAY_START_TIME = self.Start_time.replace(hour=14, minute=30)
        self.DAY_END_TIME = self.Start_time.replace(hour=21, minute=00)


    def update(self):
        if(self.Live_Trading):

            AwaitNewData() #Is this method now supposed to be algo.update? or will we be checking for new data in the main?***************

        #Breaks out to the code below if a notify is recieved on the above defined "notify_channel"
        #------------Add code Below Here----------
        if(not self.Live_Trading):
            try:
                data = QuerySpecificData(self.ticker, self.Current_time)
                self.UpdateDataArray(data)
                #O = AM_candlesticks[-1]['open']

            except (IndexError):
                print("missing data")
                self.missing_data += 1
                self.Current_time = self.Current_time + timedelta(minutes=1)


        if(self.Live_Trading):
            self.UpdateDataArray(QueryData(self.ticker))
            self.Current_time = self.AM_candlesticks[-1]['dtime']

        #print(Current_time)
        #print(DAY_END_TIME)
        #print(DAY_START_TIME)
        if(ValidTradingHours(self.Current_time)):

            C = self.AM_candlesticks[-1]['close']

            if self.EMA1 == 0:
                self.EMA1 = C
                self.EMA2 = C

            self.EMA1 = Calc_EMA(20,C,self.EMA1)
            self.EMA2 = Calc_EMA(50,C,self.EMA2)
            #print(O, C)

            #getting first EMA point :D
            if len(self.AM_candlesticks) == 2:
                if self.EMA1 > self.EMA2:
                    self.highest = 1
                else:
                    self.highest = 2

            print(self.highest)

            if self.in_position:
                if not self.upTrade:
                    #calculate trailing stop loss
                    temp = C + (C * self.stop_loss)
                    if temp < self.exit_price:
                        self.exit_price = temp
                    
                    #if C > exit_price:
                    if self.EMA1 > self.EMA2 or not ValidTradingHours(self.Current_time, -3):
                        self.in_position = False
                        Sell_Position()#Will be done through trade/position class*************
                        self.number_of_trades += 1
                        self.profit = self.profit + (self.entry_price - self.exit_price)
                        print("Exited Trade at " + str(self.exit_price))
                        print("Trade profit: " + str(self.entry_price - self.exit_price))
                        print("Total Profit: " + str(self.profit))
                        if self.entry_price - self.exit_price > 0:
                            self.good_trades += 1

                        else:
                            self.bad_trades += 1
                    
                else:
                    #calculate trailing stop loss
                    temp = C - (C * self.stop_loss)
                    if temp > exit_price:
                        exit_price = temp

                    #if C < exit_price:
                    if self.EMA2 > self.EMA1 or not ValidTradingHours(self.Current_time, -5):
                        self.in_position = False
                        Sell_Position()#Will be done through trade/position class*********
                        self.number_of_trades += 1
                        self.profit = self.profit + (self.exit_price - self.entry_price)
                        print("Trade profit: " + str(self.exit_price - self.entry_price))
                        print("Total Profit: " + str(self.profit))
                        if self.exit_price - self.entry_price > 0:
                            self.good_trades += 1

                        else:
                            self.bad_trades += 1

            else:
                if len(api.list_positions()) == 0:  #list_positions can be switched to a value connecting ot the position class. current impl wont work************
                    #check if you need to enter position
                    self.entry_price = C
                    self.exit_price = C

                    if (self.EMA1 > self.EMA2) and (self.highest == 2):
                        self.highest = 1
                        self.in_position = True
                        self.upTrade = True
                        self.entry_price = C
                        self.exit_price = C - (C * self.stop_loss)
                        print("EMA Cross: upTrade placed! Entry Price: " + str(self.entry_price))
                        place_order(self.entry_price, 10)

                    if (self.EMA1 < self.EMA2) and (self.highest == 1):
                        self.highest = 2
                        self.in_position = True
                        self.upTrade = False
                        self.entry_price = C
                        self.exit_price = C + (C * self.stop_loss)
                        print("EMA Cross: downTrade placed! Entry Price: " + str(self.entry_price))
                        place_order(self.entry_price, -10)


            if(not self.Live_Trading):
                self.Current_time = self.Current_time + timedelta(minutes=1)

            #print(Current_time)
            self.NewData = False

        if (self.Current_time > self.DAY_END_TIME):
            print("DONE!")
            print("# of trades: " + str(self.number_of_trades))
            print("Good trades: " + str(self.good_trades) + " | Bad trades: " + str(bad_trades))
            print("Total Profit: " + str(self.profit))
            print("missing data: " + str(self.missing_data))
            time.sleep(10)
            quit()
        #print("Notify Recieved")
        #UpdateDataArray(QueryData(ticker))
        #print(AM_candlesticks)


    #Taken from Momentum_Test. Could be moved to algo mebe
    def UpdateDataArray(self, data):
    
        if data != None:
            change = 0.00
            change = float(data[8])-float(data[6])
            #print(change)

            self.AM_candlesticks.append({
                "dtime": data[0],
                "open": data[6],
                "high": data[7],
                "low": data[9],
                "close": data[8],
                "volume": data[2],
                "change": change
            })

            self.close_data.append(int(data[8]))

            #print(len(AM_candlesticks))
            if len(self.AM_candlesticks) > 20:
                self.AM_candlesticks.pop(0)
                self.close_data.pop(0)
                #print(len(AM_candlesticks))