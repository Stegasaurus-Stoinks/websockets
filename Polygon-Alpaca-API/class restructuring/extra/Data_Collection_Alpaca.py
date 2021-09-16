import keystore
import config
#_________________________________________________________________________
#1: Try to put NANs back in, or figure out how to leave the slot blank
#2: add .timestamp to convert to unix on last variable
#3: hopefully it all works

import threading
import asyncio
import time
from datetime import datetime, timezone
from dateutil import tz
import numpy as np
import psycopg2

from alpaca_trade_api import StreamConn
from alpaca_trade_api.common import URL

ALPACA_API_KEY = keystore.API_KEY
ALPACA_SECRET_KEY = keystore.SECRET_KEY

conn: StreamConn = None


def stockAmData(data_time, data):
    print("stockAmData Detected")
    
    global current_timestamp
    global previous_timestamp
    global data_package

    curData = (data_time,data.symbol,data.volume,0,0,data.vwap,data.open,data.high,data.close,data.low,0,data.start)

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

        dbconn.commit()




#initialize data package to be sent to database
data_package = []

current_timestamp = 0
previous_timestamp = 0

#database stuff
SQL_PATH = "INSERT INTO stockamdata(time, symbol, volume, day_volume, day_open, vwap, o, h, c, l, avg, unix) VALUES "
CONNECTION = "postgres://{}:{}@{}:{}/{}".format(config.TSDB_USERNAME, config.TSDB_AWS_PASSWORD, config.TSDB_AWS_HOST, config.TSDB_PORT, config.TSDB_DATABASE)
dbconn = psycopg2.connect(CONNECTION)
cur = dbconn.cursor()

#list of tickers to be subbed to
tickerList = ["AAPL"]#,"TSLA","F"]

def createSubList(list):
    formatedList = []
    for ticker in list:
        sub = ['alpacadatav1/AM.{}'.format(ticker)]
        formatedList.append(sub)

    return formatedList

def consumer_thread():
    try:
        # make sure we have an event loop, if not create a new one
        loop = asyncio.get_event_loop()
        loop.set_debug(True)
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

    global conn
    conn = StreamConn(
        ALPACA_API_KEY,
        ALPACA_SECRET_KEY,
        base_url=URL('https://paper-api.alpaca.markets'),
        data_url=URL('https://data.alpaca.markets'),
        data_stream='alpacadatav1'

    )

    @conn.on(r'^AM\..+$')
    async def on_minute_bars(conn, channel, bar):
        #print('bars', bar)
        #Bar example
        # Agg({   'average': 0,
        # 'close': 296.695,
        # 'end': 1631303100000,
        # 'high': 296.695,
        # 'low': 296.44,
        # 'open': 296.44,
        # 'start': 1631303040000,
        # 'symbol': 'MSFT',
        # 'timestamp': 1631303040000,
        # 'totalvolume': 0,
        # 'volume': 2804,
        # 'vwap': 0})

        print(bar.symbol, ":", bar.close)
        #eastTime = tz.gettz("America/New_York")
        #tick_datetime_object = datetime.utcfromtimestamp(bar.start / 1000)
        #tick_datetime_object = tick_datetime_object.replace(tzinfo=timezone.utc).astimezone(tz=eastTime)
        #print(bar.start)
        utc_time = bar.start.strftime('%Y-%m-%d %H:%M:%S')
        #print(utc_time)

        stockAmData(utc_time, bar)


    #Example functions for quotes and trades
    # @conn.on(r'Q\..+')
    # async def on_quotes(conn, channel, quote):
    #     print('quote', quote)

    # @conn.on(r'T\..+')
    # async def on_trades(conn, channel, trade):
    #     print('trade', trade)


if __name__ == '__main__':
    threading.Thread(target=consumer_thread).start()

    loop = asyncio.get_event_loop()

    time.sleep(5)  # give the initial connection time to be established
    #example subscriptionList [['alpacadatav1/AM.TSLA'],['alpacadatav1/AM.ATVI'],['alpacadatav1/AM.F']]
    subscriptionList = createSubList(tickerList)
    print(subscriptionList)

    while 1:
        for channels in subscriptionList:
            loop.run_until_complete(conn.subscribe(channels))

        #loop.run_until_complete(conn.unsubscribe(['alpacadatav1/AM.ATVI']))







            
