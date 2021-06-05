import pandas as pd
import numpy as np

import psycopg2
import time, json, requests, csv
from datetime import datetime
from dateutil import tz
import threading

import config
import keystore

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

ticker = "AAPL"
#path1 = 'C:\Users\pwild\Downloads\TestData\{}.csv'.format(ticker)
#path2 = 'C:\Users\pwild\Downloads\{}.csv'.format(ticker)
#path3 = 'C:\Users\pwild\Downloads\{}.csv'.format(ticker)
#path4 = 'C:\Users\pwild\Downloads\{}.csv'.format(ticker)
#path5 = 'C:\Users\pwild\Downloads\{}.csv'.format(ticker)

df = pd.read_csv ('C:/Users/pwild/Downloads/{}_stock_sample/{}_1min_sample.txt'.format(ticker,ticker))

# df1 = pd.read_csv ('C:/Users/pwild/Downloads/TestData/{}.csv'.format(ticker))
# df2 = pd.read_csv ('C:/Users/pwild/Downloads/TestData/{}(1).csv'.format(ticker))
# df3 = pd.read_csv ('C:/Users/pwild/Downloads/TestData/{}(2).csv'.format(ticker))
# df4 = pd.read_csv ('C:/Users/pwild/Downloads/TestData/{}(3).csv'.format(ticker))
# df5 = pd.read_csv ('C:/Users/pwild/Downloads/TestData/{}(4).csv'.format(ticker))
#df = pd.concat([df1,df2,df3,df4,df5])

df.columns = ['time','o','h','l','c','volume'] 
#print(df.shape[0])
df['symbol'] = [ticker] * df.shape[0]      
print(df)
    
def execute_many(conn, df, table):
    """
    Using cursor.executemany() to insert the dataframe
    """
    # Create a list of tupples from the dataframe values
    tuples = [tuple(x) for x in df.to_numpy()]
    # Comma-separated dataframe columns
    cols = ','.join(list(df.columns))
    # SQL quert to execute
    query  = "INSERT INTO %s(%s) VALUES(%%s,%%s,%%s,%%s,%%s,%%s,%%s)" % (table, cols)
    cursor = conn.cursor()
    try:
        cursor.executemany(query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    print("execute_many() done")
    cursor.close()

execute_many(conn, df, 'stockamdata')

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
    