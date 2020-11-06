import psycopg2
import time, json, requests, csv
from datetime import datetime
from dateutil import tz
from polygon import WebSocketClient, STOCKS_CLUSTER
import config
import threading

tickerList = ["AAPL","SPY","TSLA","MSFT","DIS","AAL","GE","DAL","CCL","GPRO","F"]
dataType = "AM."
assetsToDownload = []
A_candlesticks = []
AM_candlesticks = []
numDisconnect = 0
current_timestamp = 0
previous_timestamp = 0
data_package = []

#Define timezones for time stamp conversion
from_zone = tz.gettz('UTC')
to_zone = tz.gettz('America/New_York')

SQL_PATH = "INSERT INTO stockamdata(time, symbol, volume, day_volume, day_open, vwap, o, h, c, l, avg, unix) VALUES "
CONNECTION = "postgres://{}:{}@{}:{}/{}".format(config.TSDB_USERNAME, config.TSDB_AWS_PASSWORD, config.TSDB_AWS_HOST, config.TSDB_PORT, config.TSDB_DATABASE)
#print(CONNECTION)
conn = psycopg2.connect(CONNECTION)
cur = conn.cursor()

def my_custom_process_message(message):
    #print("Got Data")
    #print(message)

    data = json.loads(message)[0]
    #print(data)
    
    if data['ev'] == 'status':
        print("Status Message: {} -> {}".format(data["message"],data["status"]))

    #convert and format time stamp from UTC to Market Hours (NEW_YORK)
    tick_datetime_object = datetime.utcfromtimestamp(data["s"] / 1000)
    #print(tick_datetime_object)
    utc_time = tick_datetime_object.strftime('%Y-%m-%d %H:%M:%S')
    #print(utc_time)
    #utc_time = utc_time.replace(tzinfo=from_zone)
    #print(utc_time)
    #data_time = utc_time.astimezone(to_zone)
    #print(data_time)

    if data['ev'] == 'AM':
        stockAmData(utc_time, data)


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
    print("Connecting")
    my_client = WebSocketClient(STOCKS_CLUSTER, config.API_KEY, my_custom_process_message, on_close, on_error)    
    my_client.run_async()
    createSubcription(my_client)
    print("===Running===")
    
def createSubcription(my_client):
    size = len(tickerList)
    tickerData = ""
    for i in range(size):
        tickerData = dataType+tickerList[i]
        assetsToDownload.append(tickerData)
        my_client.subscribe(tickerData)
        print("Connected to {}".format(tickerData))

def stockAmData(data_time, data):
    print("stockAmData Detected")
    
    global current_timestamp
    global previous_timestamp
    global data_package

    curData = (data_time,data['sym'],data['v'],data['av'],data['z'],data['vw'],data['o'],data['h'],data['c'],data['l'],data['a'],data['s'])

    current_timestamp = data_time
    #print(current_timestamp)
    if current_timestamp != previous_timestamp:
        #print('timestamp not the same')
        data_package = []
        data_package.append(curData)
        previous_timestamp = current_timestamp
        # creates a timer that starts when a new timestamp is received
        # waits for a few seconds before pushing data to DB if not all data was received
        timer = threading.Timer(5.0, DBInsert, [SQL_PATH]) 
        timer.start()          
        
    else:
        #print('timestamp is the same')
        data_package.append(curData)
        #print(len(data_package))

    if len(data_package) >= len(tickerList):
        print('all data ready:')
        DBInsert(SQL_PATH)
        print('all data ready: package sent')
        data_package = []
    

def DBInsert(sql_path):
    if len(data_package) != 0:
        print('send to db')
        dataToSend = ''
        dataToSend += sql_path
        dataToSend += str(data_package[0])
        iterdata = iter(data_package)
        next(iterdata)
        for data in iterdata:
            dataToSend+=','
            dataToSend+=str(data)
            

        dataToSend+=';'

        #print(dataToSend)
        try:
            cur.execute(dataToSend)
            print('data sent')

        except (Exception, psycopg2.Error) as error:
            print(error.pgerror)

        conn.commit()

def main():
    connect()

    

if __name__ == "__main__":
    main()