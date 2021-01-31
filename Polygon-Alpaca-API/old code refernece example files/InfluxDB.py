import time, json, requests, csv
from datetime import datetime
from polygon import WebSocketClient, STOCKS_CLUSTER
from influxdb import InfluxDBClient
import config
import threading

tickerList = ["AAPL","MSFT","TSLA","SPY"]
dataType = "AM."
assetsToDownload = []
A_candlesticks = []
AM_candlesticks = []
client = InfluxDBClient(host='localhost', port=8086)
numDisconnect = 0
current_timestamp = 0
previous_timestamp = 0
data_package = []

def sendtoDB():
    if data_package:
        client.write_points(data_package)
        print('time out: package sent')

def sendGroupDB(json_body):    
    global current_timestamp
    global previous_timestamp
    global data_package

    current_timestamp = json_body['time']
    # print(current_timestamp)
    if current_timestamp != previous_timestamp:
        # print('timestamp not the same')
        data_package = []
        data_package.append(json_body)
        previous_timestamp = current_timestamp
        # creates a timer that starts when a new timestamp is received
        # waits for a few seconds before pushing data to DB if not all data was received
        timer = threading.Timer(5.0, sendtoDB) 
        timer.start()          
        
    else:
        # print('timestamp is the same')
        data_package.append(json_body)

    if len(data_package) >= len(tickerList):
        client.write_points(data_package)
        print('all data ready: package sent')
        data_package = []


def setupDB():
    print("Available DataBases, connecting to 'stockdata'")
    # print(client.get_list_database())
    client.switch_database('stockdata')

def my_custom_process_message(message):
    #print("Got Data:", message)

    data = json.loads(message)[0]

    tick_datetime_object = datetime.utcfromtimestamp(data["s"] / 1000)
    data_time = tick_datetime_object.strftime('%Y-%m-%d %H:%M:%S')

    if data["ev"] == "AM":
        print("=====  {} @ ${} @ {}  =====".format(data["sym"], data["c"], data_time))
        if data["o"] > data["c"]:
            trend = 1
        else:
            trend = 0
        json_body = [{
            "measurement": "AMcandle",
            "tags": {
                "symbol": str(data["sym"])
            },
            "time": str(data_time),
            "fields": {
                "unix": str(data["s"]),
                "open": str(data["o"]),
                "high": str(data["h"]),
                "low": str(data["l"]),
                "close": str(data["c"]),
                "volume": str(data["v"]),
                "color": str(trend)
            }
        }]

        single_json_body = {
            "measurement": "AMcandle",
            "tags": {
                "symbol": str(data["sym"])
            },
            "time": str(data_time),
            "fields": {
                "unix": str(data["s"]),
                "open": str(data["o"]),
                "high": str(data["h"]),
                "low": str(data["l"]),
                "close": str(data["c"]),
                "volume": str(data["v"]),
                "color": str(trend)
            }
        }
        #print( json_body )

        # sendtoDB( json_body )
        sendGroupDB(single_json_body)


def on_close(message):
    global numDisconnect
    print('=================================================================================================')
    print("Connection Closed, attempting reconnection in 1 second")
    print(message)
    numDisconnect = numDisconnect + 1
    print(numDisconnect)
    print('=================================================================================================')
    time.sleep(0.5)
    connect()

def on_error(message):
    print(message)
    print("Error")

def connect():
    setupDB()
    print("Connecting")
    my_client = WebSocketClient(STOCKS_CLUSTER, config.API_KEY, my_custom_process_message, on_close, on_error)    

    my_client.run_async()

    createSubcription(my_client)

    print("===Running===")
    #time.sleep(1)
    #print("3")
    #time.sleep(1)
    #print("2")
    #time.sleep(1)
    #print("1")
    #time.sleep(1)

    #my_client.close_connection()
    
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