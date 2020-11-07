import psycopg2
import time, json, requests, csv
from datetime import datetime
from dateutil import tz
from polygon import WebSocketClient, STOCKS_CLUSTER
import config
import threading

tickerList = ["AAPL","SPY","TSLA","MSFT"]
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

SQL_PATH_SEND = "INSERT INTO test(index, data1, data2) VALUES (%s, %s, %s);"
SQL_PATH_PULL = "SELECT * FROM test"
data = (4, 4, 4)
CONNECTION = "postgres://{}:{}@{}:{}/{}".format(config.TSDB_USERNAME, config.TSDB_AWS_PASSWORD, config.TSDB_AWS_HOST, config.TSDB_PORT, config.TSDB_DATABASE)
conn = psycopg2.connect(CONNECTION)
cur = conn.cursor()

def sendData():
    try:
        cur.execute(SQL_PATH_SEND, data)
        print('data sent')

    except (Exception, psycopg2.Error) as error:
        print(error.pgerror)

    conn.commit()

def pullData():
    cur.execute(SQL_PATH_PULL)
    results = cur.fetchall()
    for result in results:
        if result[0] % 2 == 0:
            print(result[0])

def pullAMData(ticker, numPoints):
    query = """
    SELECT *
    FROM stockamdata
    WHERE symbol = %s
    ORDER BY time
    DESC LIMIT %s;
    """
    data = (ticker, numPoints)
    cur.execute(query, data)
    results = cur.fetchall()
    for result in results:
        print("{} opened @ {} at time {}".format(result[1],result[6],result[0]))
        

pullAMData('TSLA' , 20)