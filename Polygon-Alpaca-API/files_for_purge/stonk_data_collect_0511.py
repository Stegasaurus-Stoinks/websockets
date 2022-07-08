IEX_TOKEN = 'pk_536cdf66059a4846a9ce981fb1f19b38'
IEX_SECRET_TOKEN = 'sk_32ec0f26646e4dea975af53b7fce5bad'

from email import message
from lib2to3.pygram import Symbols
from matplotlib.font_manager import json_load
import pyEX as p
import json
import datetime
import psycopg2
from enum import Enum
import threading

import config


from sseclient import SSEClient

SQL_PATH = "INSERT INTO stockamdata(time, symbol, volume, day_volume, day_open, vwap, o, h, c, l, avg, unix) VALUES "
CONNECTION = "postgres://{}:{}@{}:{}/{}".format(config.TSDB_USERNAME, config.TSDB_AWS_PASSWORD, config.TSDB_AWS_HOST, config.TSDB_PORT, config.TSDB_DATABASE)
#print(CONNECTION)
#conn = psycopg2.connect(CONNECTION)
#cur = conn.cursor()

current_timestamp = 0
previous_timestamp = 0


class Ticker(Enum):
    Open = 1
    High = 2
    Low = 3
    Close = 4
    Volume = 5

tickerList = ["spy"]
tickerData = [[] for x in range(len(tickerList))]

url = 'https://cloud-sse.iexapis.com/stable/stocksUSNoUTP1Second?token=pk_536cdf66059a4846a9ce981fb1f19b38&symbols='
for ticker in tickerList:
    url = url+ticker+','

print(url)

message = SSEClient(url)

for msg in message:
    outputMsg = msg.data
    outputJS = json.loads(outputMsg)
    #print( FilterName, outputJS[FilterName] )
    #print(outputJS)
    for line in outputJS:
        #print("Calculation Price: " + str(line['calculationPrice']) + " Close: " + str(line['close']))
        time = datetime.datetime.fromtimestamp(line['lastTradeTime']//1000).strftime('%Y-%m-%d %H:%M:%S')
        current_timestamp = datetime.datetime.fromtimestamp(line['lastTradeTime']//1000).replace(second=0)
        print("Last Trade Time " + str(time) + " Latest Price: " + str(line['latestPrice']) + " Latest Volume: " + str(line['latestVolume']))
        if current_timestamp != previous_timestamp:
            print("New Time Stamp!!")
            previous_timestamp = current_timestamp
            print(tickerData)
            for x in range(len(tickerData)):
                tickerData[x] = [1,1,1,1]

            print(tickerData)



def stockAmData(data_time, data):
    print("stockAmData Detected")
    
    global current_timestamp
    global previous_timestamp
    global data_package

    curData = (data_time,data['sym'],data['v'],data['av'],data['z'],data['vw'],data['o'],data['h'],data['c'],data['l'],data['a'],data['s'])

    current_timestamp = data_time
    #print(current_timestamp)
    #If a new minute of data was recieved, start timeout timer and create new data array
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