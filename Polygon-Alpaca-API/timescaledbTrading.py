import time, sys, json, requests
import config
import json
from datetime import datetime, timedelta
import psycopg2

Start_time = datetime(2020, 11, 6, 17, 59, 0)
#print(Start_time)
Current_time = datetime.now()
Next_time = datetime(2020, 11, 6, 17, 30, 0)
newData = False

AM_candlesticks = []
in_position = False
downtrend = False
uptrend = False
uptrend_points = 0
downtrend_points = 0
SYMBOL = "AAPL"

BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
ORDERS_URL = "{}/v2/orders".format(BASE_URL)
POSITIONS_URL = "{}/v2/positions/{}".format(BASE_URL, SYMBOL)

HEADERS = {'APCA-API-KEY-ID': config.PAPER_API_KEY, 'APCA-API-SECRET-KEY': config.PAPER_SECRET_KEY}

CONNECTION = "postgres://{}:{}@{}:{}/{}".format(config.TSDB_USERNAME, config.TSDB_AWS_PASSWORD, config.TSDB_AWS_HOST, config.TSDB_PORT, config.TSDB_DATABASE)
conn = psycopg2.connect(CONNECTION)
cur = conn.cursor()



def send_order(profit_price, loss_price):

    data = {
        "symbol": SYMBOL,
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

def place_order(profit_price, loss_price):

    print("== Sending order ==")
    quit()
    #send_order(profit_price, loss_price)

def ThreeWhiteSoldiers():
    global in_position, downtrend
    if len(AM_candlesticks) > 3 and downtrend is True and in_position is False:
        #print("== Checking for Three White Soldiers pattern ==")
        third_candle = AM_candlesticks[-1]
        second_candle = AM_candlesticks[-2]
        first_candle = AM_candlesticks[-3]

        if third_candle['close'] > second_candle['close'] > first_candle['close']\
                and third_candle['close'] > third_candle['open']\
                and second_candle['close'] > second_candle['open']\
                and first_candle['close'] > first_candle['open']:
            print("Found three green candlesticks in a row")
            distance = third_candle['close'] - first_candle['open']
            print("Distance is {}".format(distance))
            profit_price = third_candle['close'] + (distance * 2)
            print("TP @ {}".format(profit_price))
            loss_price = first_candle['open']
            print("Cut Loss @ {}".format(loss_price))

            in_position = True
            place_order(profit_price, loss_price)

        else:
            print("No go")

def Calculate_trend_Attempt2():
    global downtrend, uptrend

    uptrend_points = 0
    downtrend_points = 0
    not_downtrend_points = 0
    not_uptrend_points = 0

    if len(AM_candlesticks) < 5:
        print("not enough data to determine trend")

    else:
        for x in range(-1,-5,-1):
            current_candle = AM_candlesticks[x]
            previous_candle = AM_candlesticks[x-1]
            if(current_candle['high'] < previous_candle['high']):
                downtrend_points += 1
            else:
                not_downtrend_points += 1

            if (current_candle['low'] > previous_candle['low']):
                uptrend_points = uptrend_points + 1
            else:
                not_uptrend_points += 1

        if uptrend_points >= (not_uptrend_points + 2):
            uptrend = True
            downtrend = False
            print("uptrend located")

        if downtrend_points >= (not_downtrend_points + 2):
            uptrend = False
            downtrend = True
            print("downtrend located")

        else:
            print("Trading Sideways")
            uptrend = False
            downtrend = False

        #print("uptrend points: {} not_uptrend_points: {}".format(uptrend_points, not_uptrend_points))
        #print("downtrend points: {} not_downtrend_points: {}".format(downtrend_points, not_downtrend_points))

    return


def ReceiveNewData():
    global newData
    global Current_time

    while not newData:
        result = query('SPY')
        #result = result[0]

        if result == []:
            time.sleep(1)
            print("no new data")
            IncrementTime()

        else:
            result = result[0]
            #print("NEW DATA DETECTED")
            newData = True
            Current_time = result[0]

    print("{} opened @ {} at time {}".format(result[1],result[6],result[0]))
    UpdateDataArray(result)
    newData = False

def query(ticker):
    query = """
    SELECT *
    FROM stockamdata
    WHERE symbol = %s
    AND time = %s
    ORDER BY time
    DESC LIMIT %s;
    """
    data = (ticker, Next_time, 1)
    cur.execute(query, data)
    results = cur.fetchall()
    return results

def IncrementTime():
    global Next_time
    Next_time += timedelta(minutes=1)

def UpdateDataArray(data):
    global AM_candlesticks
    AM_candlesticks.append({
            "dtime": data[0],
            "open": data[6],
            "high": data[7],
            "low": data[9],
            "close": data[8],
            "volume": data[2]
        })

    if len(AM_candlesticks) > 20:
        AM_candlesticks.pop(0)
        #print(len(AM_candlesticks))


def main():
    while True:
        ReceiveNewData()
        IncrementTime()
        time.sleep(2)
        # Check for trend in price
        Calculate_trend_Attempt2()
        # Check for pattern
        ThreeWhiteSoldiers()  
            
main()
