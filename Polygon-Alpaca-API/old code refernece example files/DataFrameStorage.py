import time, json, requests, csv
from datetime import datetime
from polygon import WebSocketClient, STOCKS_CLUSTER
import websocket

import config

url = "wss://socket.polygon.io/stocks"

#tickerList = ["NVDA"]
tickerList = ["NVDA","AAPL","MSFT","TSLA","SPY"]
dataType = "T."
assetsToDownload = []
# AM_candlesticks = pandas.DataFrame(columns=["time","open","high","low","close","volume","color"])

def my_custom_process_message(message):
    print("Got Data: ",message)

    data = json.loads(message)[0]

    tick_datetime_object = datetime.utcfromtimestamp(data["s"] / 1000)
    data_time = tick_datetime_object.strftime('%Y-%m-%d %H:%M:%S')

    if data["ev"] == "AM":
        # print("=====  {} @ ${} @ {}  =====".format(data["sym"], data["c"], data_time))
        if data["o"] > data["c"]:
            trend = 1
        else:
            trend = 0

        new_row = {
            "time": data_time,
            "open": data["o"],
            "high": data["h"],
            "low": data["l"],
            "close": data["c"],
            "volume": data["v"],
            "color": trend
            }

        AM_candlesticks = AM_candlesticks.append(new_row, ignore_index=True)

        print(AM_candlesticks)


def my_custom_on_close(message):
    print(message)
    print("Connection Closed, attempting reconnection in 1 second")
    time.sleep(1)
    reconnect()

def my_custom_on_error(message):
    print(message)
    print("=============Error=============")

def connect():
    print("Connecting")

    my_ws = websocket.WebSocketApp(url, on_message = my_custom_process_message, on_error = my_custom_on_error, on_close = my_custom_on_close)
    my_ws.send('{"action":"auth","params":"%s"}' % config.API_KEY)
    time.sleep(1)
    createSubcription(my_ws)
    my_ws.run_forever()

def reconnect():
    print("Reconnecting...")
    time.sleep(1)
    print("Reconnecting...")
    my_new_client = WebSocketClient(STOCKS_CLUSTER, config.API_KEY, my_custom_process_message, my_custom_on_close, my_custom_on_error)
    print("Reconnecting...")
    my_new_client.run_async()
    print("Reconnecting...")
    createSubcription(my_new_client)
    print("Reconnecting...")
    
def createSubcription(my_ws):
    print("Create Subscriptions")
    size = len(tickerList)
    tickerData = ""
    for i in range(size):
        tickerData = dataType+tickerList[i]
        assetsToDownload.append(tickerData)
        sub_message = '{"action":"subscribe","params":"%s"}' % tickerData
        my_ws.send(sub_message)
        print("Connected to {}".format(tickerData))
        
def main():
    connect()

if __name__ == "__main__":
    main()