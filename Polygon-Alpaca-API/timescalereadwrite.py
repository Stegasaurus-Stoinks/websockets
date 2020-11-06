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

SQL_PATH = "INSERT INTO test(index, data1, data2) VALUES (%s, %s, %s);"
data = (4, 4, 4)
CONNECTION = "postgres://{}:{}@{}:{}/{}".format(config.TSDB_USERNAME, config.TSDB_AWS_PASSWORD, config.TSDB_AWS_HOST, config.TSDB_PORT, config.TSDB_DATABASE)
conn = psycopg2.connect(CONNECTION)
cur = conn.cursor()

try:
    cur.execute(SQL_PATH, data)
    print('data sent')

except (Exception, psycopg2.Error) as error:
    print(error.pgerror)

conn.commit()
