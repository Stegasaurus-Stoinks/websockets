import time, json, requests, csv
from datetime import datetime
from polygon import WebSocketClient, STOCKS_CLUSTER

import config

tickerList = ["NVDA","AAPL","MSFT","TSLA","SPY"]
dataType = "AM."
assetsToDownload = []
A_candlesticks = []
AM_candlesticks = []

def my_custom_process_message(message):
    # print("Got Data:", message)

    data = json.loads(message)[0]

    tick_datetime_object = datetime.utcfromtimestamp(data["s"] / 1000)
    data_time = tick_datetime_object.strftime('%Y-%m-%d %H:%M:%S')

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

def on_close():
    print("Connection Closed, attempting reconnection in 1 second")
    time.sleep(1)
    connect()

def on_error():
    print("Error")

def connect():
    print("Connecting")
    my_client = WebSocketClient(STOCKS_CLUSTER, config.API_KEY, my_custom_process_message, on_close=on_close, on_error=on_error)    

    my_client.run_async()

    createSubcription(my_client)
    
def createSubcription(my_client):
    size = len(tickerList)
    tickerData = ""
    for i in range(size):
        tickerData = dataType+tickerList[i]
        assetsToDownload.append(tickerData)
        my_client.subscribe(tickerData)
        print("Connected to {}".format(tickerData))
        
def main():
    connect()

if __name__ == "__main__":
    main()