import select, time, requests, json, sys
import psycopg2
import psycopg2.extensions
import config
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import alpaca_trade_api as tradeapi
import keystore
import numpy as np

#Import Functions and Indicators
from Algo_Functions import IsDownTrend,formatTime,Calc_EMA,plotter

#------Config Variables------
Live_Trading = False
notify_channel = "amdata"
ticker = "AAPL"
Start_time = datetime(2021, 1, 15, 14, 30, 0)
End_time = datetime(2020, 11, 18, 18, 30, 0)
#----------------------------

ALGO = 'Momentum'
NewData = False
AM_candlesticks = []
close_data = []
Current_time = datetime(2020, 11, 18, 18, 11, 0)
Next_time = datetime(2020, 11, 18, 18, 11, 0)
in_position = False

DAY_START_TIME = Start_time.replace(hour=14, minute=30)
DAY_END_TIME = Start_time.replace(hour=21, minute=00)

BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
ORDERS_URL = "{}/v2/orders".format(BASE_URL)
POSITIONS_URL = "{}/v2/positions/{}".format(BASE_URL, ticker)
HEADERS = {'APCA-API-KEY-ID': keystore.PAPER_API_KEY, 'APCA-API-SECRET-KEY': keystore.PAPER_SECRET_KEY}

api = tradeapi.REST(keystore.PAPER_API_KEY, keystore.PAPER_SECRET_KEY, base_url='https://paper-api.alpaca.markets') # or use ENV Vars shown below

CONNECTION = "postgres://{}:{}@{}:{}/{}".format(config.TSDB_USERNAME, config.TSDB_AWS_PASSWORD, config.TSDB_AWS_HOST, config.TSDB_PORT, config.TSDB_DATABASE)
conn = psycopg2.connect(CONNECTION)
cur = conn.cursor()
cur.execute("LISTEN " + notify_channel)

#cur.execute("NOTIFY testyy, 'this connection works';")
conn.commit()


def AwaitNewData():
    global NewData
    if Live_Trading:
        while not NewData:
            #print("NewData is", NewData)
            if select.select([conn],[],[],40) == ([],[],[]):
                print("Waiting for notifications on channel " + notify_channel)
            else:
                conn.poll()
                while conn.notifies:
                    notify = conn.notifies.pop(0)
                    #print("Got NOTIFY, New Data Recieved!")
                    #print(notify.pid, notify.channel, notify.payload)
                    NewData = True

def QueryData(ticker):
    global Current_time

    if Live_Trading:
        data = QueryLast(ticker)
        #print(Current_time)
        #print(data[0])
        if Current_time != data[0]:
            print("This is a new data point")
            print("{} opened @ {} at time {}".format(data[1],data[6],data[0]))
            Current_time = data[0]
            return(data)
        else:
            print("ERROR! This is the same time data as the last point, possible data collection error!")    


    else:
        #for backtesting
        QuerySpecificData(ticker, Current_time)
        #print("pull backtesting data using specific time stamp")

def QueryLast(ticker):
    query = """
    SELECT *
    FROM stockamdata
    WHERE symbol = %s
    ORDER BY time
    DESC LIMIT %s;
    """
    data = (ticker, 1)
    cur.execute(query, data)
    results = cur.fetchall()[0]
    conn.commit()
    return results

def QuerySpecificData(ticker, Current_time):
    query = """
    SELECT *
    FROM stockamdata
    WHERE symbol = %s
    AND time = %s
    ORDER BY time
    DESC LIMIT %s;
    """
    data = (ticker, Current_time, 1)
    cur.execute(query, data)
    results = cur.fetchall()[0]
    conn.commit()
    return results

def UpdateDataArray(data):
    global AM_candlesticks
    global close_data
    if data != None:
        change = 0.00
        change = float(data[8])-float(data[6])
        #print(change)
        AM_candlesticks.append({
                "dtime": data[0],
                "open": data[6],
                "high": data[7],
                "low": data[9],
                "close": data[8],
                "volume": data[2],
                "change": change
            })

        close_data.append(int(data[8]))

        #print(len(AM_candlesticks))
        if len(AM_candlesticks) > 20:
            AM_candlesticks.pop(0)
            close_data.pop(0)
            #print(len(AM_candlesticks))

def main():
    global NewData
    global in_position

    Current_time = Start_time

    size = 40
    x_vec = np.linspace(0,1,size+1)[0:-1]
    y_vec = np.zeros(len(x_vec))
    y_vec1 = np.zeros(len(x_vec))
    y_vec2 = np.zeros(len(x_vec))
    y_vec3 = np.zeros(len(x_vec))
    y_vec4 = np.zeros(len(x_vec))
    line1 = []
    line2 = []
    line3 = []
    line4 = []
    line5 = []
    EMA1 = 0
    EMA2 = 0
    entry_price = 100
    exit_price = 100
    upTrade = False
    missing_data = 0
    number_of_trades = 0

    stop_loss = 0.001
    profit = 0

    while True:
        #AwaitNewData() 
        #Breaks out to the code below if a notify is recieved on the above defined "notify_channel"
        #------------Add code Below Here----------
        if(Current_time >= DAY_START_TIME and Current_time <= DAY_END_TIME):
            try:
                data = QuerySpecificData(ticker, Current_time)

            except (IndexError):
                print("missing data")
                missing_data += 1
                Current_time = Current_time + timedelta(minutes=1)
            
            UpdateDataArray(data)
            #O = AM_candlesticks[-1]['open']
            C = AM_candlesticks[-1]['close']

            if EMA1 == 0:
                EMA1 = C
                EMA2 = C

            EMA1 = Calc_EMA(20,C,EMA1)
            EMA2 = Calc_EMA(50,C,EMA2)
            #print(O, C)
            
            if in_position:
                if upTrade:
                    temp = C + (C * stop_loss)
                    if temp < exit_price:
                        exit_price = temp
                    
                    if C > exit_price:
                        in_position = False
                        number_of_trades += 1
                        profit = profit + (exit_price - entry_price) 
                    
                else:
                    temp = C - (C * stop_loss)
                    if temp > exit_price:
                        exit_price = temp

                    if C < exit_price:
                        in_position = False
                        number_of_trades += 1
                        profit = profit + (entry_price - exit_price)

            else:
                #check if you need to enter position
                entry_price = C
                exit_price = C

                print(profit)

                if EMA1 > EMA2:
                    in_position = True
                    upTrade = True
                    #print("upTrade placed")
                    entry_price = C

                if EMA1 < EMA2:
                    in_position = True
                    upTrade = False
                    #print("downTrade placed")
                    entry_price = C
                

            y_vec[-1] = EMA1
            y_vec1[-1] = EMA2
            y_vec2[-1] = C
            y_vec3[-1] = entry_price
            y_vec4[-1] = exit_price
            line1,line2,line3,line4,line5 = plotter(x_vec,y_vec,y_vec1,y_vec2,y_vec3,y_vec4,line1,line2,line3,line4,line5)
            y_vec = np.append(y_vec[1:],0.0)
            y_vec1 = np.append(y_vec1[1:],0.0)
            y_vec2 = np.append(y_vec2[1:],0.0)
            y_vec3 = np.append(y_vec3[1:],0.0)
            y_vec4 = np.append(y_vec4[1:],0.0)

            Current_time = Current_time + timedelta(minutes=1)
            #time.sleep(.2)

        else:
            print("DONE!")
            print("# of trades " + str(number_of_trades))
            print("missing " + str(missing_data))
            time.sleep(5)
        #print("Notify Recieved")
        #UpdateDataArray(QueryData(ticker))
        #print(AM_candlesticks)
        

main()