import time, sys, json, requests
import config
import json
from datetime import datetime

from polygon import WebSocketClient, STOCKS_CLUSTER


A_candlesticks = []
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


def Calculate_trend():
    global downtrend, uptrend
    # need to add this
    downtrend = True

def Calculate_trend_Attempt():
    global downtrend, uptrend, downtrend_points, uptrend_points
    current_candle = AM_candlesticks[-1]
    previous_candle = AM_candlesticks[-2]
    if(current_candle['high'] < previous_candle['high']):
        downtrend_points = downtrend_points + 1
    if (current_candle['low'] > previous_candle['low']):
        uptrend_points = uptrend_points + 1

    if uptrend_points > 5 and uptrend_points >= (downtrend_points+1):
        uptrend = True
        downtrend = False
        print("uptrend located")
        uptrend_points = 0
        downtrend_points = 0

    if downtrend_points > 5 and downtrend_points >= (uptrend_points + 1):
        uptrend = False
        downtrend = True
        print("downtrend located")
        uptrend_points = 0
        downtrend_points = 0

    else:
        if downtrend_points < 5 and uptrend_points < 5:
            print("Not enough data to calculate trend")
        else:
            print("No Trend Found/Trading Sideways")

    print("uptrend points: {} downtrendpoints: {}".format(uptrend_points, downtrend_points))
    return

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

        print("uptrend points: {} not_uptrend_points: {}".format(uptrend_points, not_uptrend_points))
        print("downtrend points: {} not_downtrend_points: {}".format(downtrend_points, not_downtrend_points))

    return


def my_custom_process_message(message):
    # print("this is my custom message processing", message)
    data = json.loads(message)[0]

    tick_datetime_object = datetime.utcfromtimestamp(data["s"] / 1000)
    data_time = tick_datetime_object.strftime('%Y-%m-%d %H:%M:%S')

    if data["ev"] == "A":
        print("{} @ ${} @ {} ".format(data["sym"], data["c"], data_time))
        A_candlesticks.append({
            "time": data_time,
            "open": data["o"],
            "high": data["h"],
            "low": data["l"],
            "close": data["c"],
            "volume": data["v"],
            "change": data["c"]-data["o"]
        })

    if data["ev"] == "AM":
        print("=====  {} @ ${} @ {}  =====".format(data["sym"], data["c"], data_time))
        if data["o"] > data["c"]:
            trend = 1
        else:
            trend = 0
        AM_candlesticks.append({
            "time": data_time,
            "open": data["o"],
            "high": data["h"],
            "low": data["l"],
            "close": data["c"],
            "volume": data["v"],
            "color": trend
        })

    # Check for trend in price
    Calculate_trend_Attempt2()

    # Check for pattern
    ThreeWhiteSoldiers()


    #if len(A_candlesticks) % 10 == 0:
    #    print(A_candlesticks)



def my_custom_error_handler(ws, error):
    print("this is my custom error handler", error)


def my_custom_close_handler(ws):
    print("this is my custom close handler")


def main():
    key = config.API_KEY
    my_client = WebSocketClient(STOCKS_CLUSTER, key, my_custom_process_message)
    my_client.run_async()
    channel = "AM.{}".format(SYMBOL)
    my_client.subscribe(channel)


if __name__ == "__main__":
    main()