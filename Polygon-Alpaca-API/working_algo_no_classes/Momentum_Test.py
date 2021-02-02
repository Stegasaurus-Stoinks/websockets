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

#------Config Variables------
Live_Trading = True
notify_channel = "amdata"
ticker = "MSFT"

#Start_time = datetime(2021, 1, 29, 17, 40, 0) 
Start_time = datetime.utcnow()
End_time = datetime(2020, 11, 18, 18, 30, 0)
#----------------------------
utc=pytz.UTC
Start_time = utc.localize(Start_time) 
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

#variable for checking EMA cross
highest = 0

def Sell_Position():
    r = requests.delete(POSITIONS_URL, headers=HEADERS)
    response = json.loads(r.content)
    print(response)

def place_order(entry_price, volume, profit_price = 0, loss_price = 0): 

    print("== Sending order ==")
    if loss_price == 0 and profit_price ==0:
        if volume > 0:
            send_buy_order(volume)
        
        else:
            volume = volume * -1
            send_sell_order(volume)


    else:
        send_order(profit_price, loss_price, volume)
        log_order(profit_price, loss_price, entry_price, volume)

def send_order(profit_price, loss_price, volume):

    data = {
        "symbol": ticker,
        "qty": volume,
        "side": "buy",
        "type": "market",
        "time_in_force": "gtc",
        "order_class": "bracket",
        "take_profit": {
            "limit_price": profit_price
        },
        "stop_loss": {
            "stop_price": loss_price
        }
    }

    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)

    response = json.loads(r.content)

    print(response)

def send_buy_order(volume):

    data = {
        "symbol": ticker,
        "qty": volume,
        "side": "buy",
        "type": "market",
        "time_in_force": "gtc",
        "order_class": "simple",
    }

    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)

    response = json.loads(r.content)

    print(response)

def send_sell_order(volume):

    data = {
        "symbol": ticker,
        "qty": volume,
        "side": "sell",
        "type": "market",
        "time_in_force": "gtc",
        "order_class": "simple",
    }

    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)

    response = json.loads(r.content)

    print(response)

def send_trail_order(profit_price, loss_price, volume):

    data = {
        "symbol": ticker,
        "qty": volume,
        "side": "buy",
        "type": "market",
        "time_in_force": "gtc",
        "order_class": "bracket",
        "take_profit": {
            "limit_price": profit_price
        },
        "stop_loss": {
            "stop_price": loss_price
        }
    }

    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)

    response = json.loads(r.content)

    print(response)

def log_order(profit_price, loss_price, entry_price, volume):
    data_send = """
    INSERT INTO trades(entrytime, exittime, algo, entryprice, exitprice, symbol, tradetype, volume, id) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    data = (formatTime(Current_time), formatTime(Current_time), ALGO, entry_price, profit_price, ticker, 'Shares', volume, 1)
    try:
        cur.execute(data_send, data)
        print("order data logged")

    except (Exception, psycopg2.Error) as error:
            print(error.pgerror)
                
    conn.commit()

def AwaitNewData():
    global NewData
    if Live_Trading:
        while not NewData:
            #print("NewData is", NewData)
            if select.select([conn],[],[],70) == ([],[],[]):
                print(" ")
                #print("Waiting for notifications on channel " + notify_channel)

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

def ValidTradingHours(Current_time, Offset = 0):
    Startt = DAY_START_TIME
    Endt = DAY_END_TIME
    Shiftt = timedelta(minutes = Offset)

    if Offset > 0:
        Startt = Startt + Shiftt

    if Offset < 0:
        Endt = Endt + Shiftt

    if (Current_time >= Startt and Current_time <= Endt):
        return True

    else:
        return False

def main():
    global NewData
    global in_position
    global highest

    Current_time = Start_time

    EMA1 = 0
    EMA2 = 0
    entry_price = 100
    exit_price = 100
    upTrade = False
    missing_data = 0
    number_of_trades = 0
    good_trades = 0
    bad_trades = 0

    stop_loss = 0.002
    profit = 0

    while True:
        if(Live_Trading):
            AwaitNewData() 
        #Breaks out to the code below if a notify is recieved on the above defined "notify_channel"
        #------------Add code Below Here----------
        if(not Live_Trading):
            try:
                data = QuerySpecificData(ticker, Current_time)
                UpdateDataArray(data)
                #O = AM_candlesticks[-1]['open']

            except (IndexError):
                print("missing data")
                missing_data += 1
                Current_time = Current_time + timedelta(minutes=1)


        if(Live_Trading):
            UpdateDataArray(QueryData(ticker))
            Current_time = AM_candlesticks[-1]['dtime']

        #print(Current_time)
        #print(DAY_END_TIME)
        #print(DAY_START_TIME)
        if(ValidTradingHours(Current_time)):

            C = AM_candlesticks[-1]['close']

            if EMA1 == 0:
                EMA1 = C
                EMA2 = C

            EMA1 = Calc_EMA(20,C,EMA1)
            EMA2 = Calc_EMA(50,C,EMA2)
            #print(O, C)

            #getting first EMA point :D
            if len(AM_candlesticks) == 2:
                if EMA1 > EMA2:
                    highest = 1
                else:
                    highest = 2

            print(highest)

            if in_position:
                if not upTrade:
                    #calculate trailing stop loss
                    temp = C + (C * stop_loss)
                    if temp < exit_price:
                        exit_price = temp
                    
                    #if C > exit_price:
                    if EMA1 > EMA2 or not ValidTradingHours(Current_time, -3):
                        in_position = False
                        Sell_Position()
                        number_of_trades += 1
                        profit = profit + (entry_price - exit_price)
                        print("Exited Trade at " + str(exit_price))
                        print("Trade profit: " + str(entry_price - exit_price))
                        print("Total Profit: " + str(profit))
                        if entry_price - exit_price > 0:
                            good_trades += 1

                        else:
                            bad_trades += 1
                    
                else:
                    #calculate trailing stop loss
                    temp = C - (C * stop_loss)
                    if temp > exit_price:
                        exit_price = temp

                    #if C < exit_price:
                    if EMA2 > EMA1 or not ValidTradingHours(Current_time, -5):
                        in_position = False
                        Sell_Position()
                        number_of_trades += 1
                        profit = profit + (exit_price - entry_price)
                        print("Trade profit: " + str(exit_price - entry_price))
                        print("Total Profit: " + str(profit))
                        if exit_price - entry_price > 0:
                            good_trades += 1

                        else:
                            bad_trades += 1

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
                        exit_price = C + (C * stop_loss)
                        print("EMA Cross: downTrade placed! Entry Price: " + str(entry_price))
                        place_order(entry_price, -10)


            if(not Live_Trading):
                Current_time = Current_time + timedelta(minutes=1)

            #print(Current_time)
            NewData = False

        if (Current_time > DAY_END_TIME):
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
        

main()