import select, time, requests, json, sys
import psycopg2
import psycopg2.extensions
import config
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import alpaca_trade_api as tradeapi
import keystore

#Import Functions and Indicators
from Algo_Functions import IsDownTrend,formatTime,AverageCalc

#------Config Variables------
Live_Trading = False
notify_channel = "amdata"
ticker = "AAPL"
#----------------------------

ALGO = 'Momentum'
NewData = False
AM_candlesticks = []
Current_time = datetime(2020, 11, 18, 18, 11, 0)
Next_time = datetime(2020, 11, 18, 18, 11, 0)
End_time = datetime(2020, 11, 18, 18, 30, 0)
in_position = True

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
        print("pull backtesting data using specific time stamp")

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
    if data != None:
        change = 0.00
        change = float(data[8])-float(data[6])
        print(change)
        AM_candlesticks.append({
                "dtime": data[0],
                "open": data[6],
                "high": data[7],
                "low": data[9],
                "close": data[8],
                "volume": data[2],
                "change": change
            })
        #print(len(AM_candlesticks))
        if len(AM_candlesticks) > 20:
            AM_candlesticks.pop(0)
            #print(len(AM_candlesticks))

def main():
    global NewData
    global in_position
    while True:
        #AwaitNewData() 
        #Breaks out to the code below if a notify is recieved on the above defined "notify_channel"
        #------------Add code Below Here----------
        #print("Notify Recieved")
        #UpdateDataArray(QueryData(ticker))
        #print(AM_candlesticks)
        

main()