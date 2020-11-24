import select, time, requests, json, sys
import psycopg2
import psycopg2.extensions
import config
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import alpaca_trade_api as tradeapi


#------Config Variables------
Live_Trading = True
notify_channel = "amdata"
ticker = "SPY"
#----------------------------

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
HEADERS = {'APCA-API-KEY-ID': config.PAPER_API_KEY, 'APCA-API-SECRET-KEY': config.PAPER_SECRET_KEY}

api = tradeapi.REST(config.PAPER_API_KEY, config.PAPER_SECRET_KEY, base_url='https://paper-api.alpaca.markets') # or use ENV Vars shown below

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

def place_order(profit_price, loss_price): 

    print("== Sending order ==")
    send_order(profit_price, loss_price)

def send_order(profit_price, loss_price):

    data = {
        "symbol": ticker,
        "qty": 10,
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

def ThreeKingsAlgo():
    global in_position
    if len(AM_candlesticks)<10:
        print("not enough data to start")
    
    else:
        firstcandle = AM_candlesticks[-1]
        secondcandle = AM_candlesticks[-2]
        thirdcandle = AM_candlesticks[-3]

        if firstcandle['change'] > 0 and secondcandle['change'] > 0 and thirdcandle['change'] > 0:
            print("three green candles detected: Now checking trend")
            if IsDownTrend(-4,-9):
                print("Found a downtrend: Three Kings Pattern Detected")
                distance = thirdcandle['close'] - firstcandle['open']
                print("Distance is {}".format(distance))
                profit_price = thirdcandle['close'] + (distance * 2)
                print("TP @ {}".format(profit_price))
                loss_price = firstcandle['open']
                print("Cut Loss @ {}".format(loss_price))
                in_position = True
                place_order(profit_price, loss_price)   

def IsDownTrend(Start, End):
    downtrend_candles = 0
    downtrend_value = 0.00
    uptrend_candles = 0
    uptrend_value = 0.00

    for x in range(Start,End,-1):
        current_candle = AM_candlesticks[x]
        cur_change = current_candle['change']
        #previous_candle = AM_candlesticks[x-1]
        if cur_change < 0:
            downtrend_candles += 1
            downtrend_value -= cur_change

        else:
            uptrend_candles += 1
            uptrend_value += cur_change

    if downtrend_candles > uptrend_candles and downtrend_value > uptrend_value:
        return True

    else:
        return False

def main():
    global NewData
    global in_position
    while True:
        AwaitNewData() 
        #Breaks out to the code below if a notify is recieved on the above defined "notify_channel"
        #------------Add code Below Here-------------

        print("Notify Recieved")
        UpdateDataArray(QueryData(ticker))

        if not in_position:
            ThreeKingsAlgo()

        else:
            if len(api.list_positions()) == 0:
                in_position = False   

        #------------Add code Above Here-------------
        #Reset the notification loop
        NewData=False

main()