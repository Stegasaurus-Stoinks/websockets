import asyncio
from time import time_ns

import ib_insync as ibi
import pandas as pd
import numpy as np
import datetime
import time
from dateutil import tz
from enum import Enum
import psycopg2
from csv import writer

import config

tickerList = ['AAPL','TSLA','SPY','AMD','GME']
#tickerList = ['AAPL']
candles = []
lists = []
volume = []
prevdataclose = []

data_package = []

firsttime = 1

for ticker in tickerList:
    lists.append([])
    volume.append([])
    prevdataclose.append([])

symbol = 'AAPL'

#lists[tickerList.index(symbol)].append(9)
#print(lists)

#lists[0].append(9)
#lists[1].append(8)

#print(lists)

current_time = datetime.datetime(1, 1, 1, 1, 1, 1, 1, tzinfo=datetime.timezone.utc).replace(second=0,microsecond=0)
last_time = datetime.datetime(1, 1, 1, 1, 1, 1, 1, tzinfo=datetime.timezone.utc).replace(second=0,microsecond=0)

from_zone = tz.gettz('UTC')
to_zone = tz.gettz('America/New_York')

SQL_PATH = "INSERT INTO stockamdata(time, symbol, volume, o, h, c, l, unix) VALUES "
CONNECTION = "postgres://{}:{}@{}:{}/{}".format(config.TSDB_USERNAME, config.TSDB_AWS_PASSWORD, config.TSDB_AWS_HOST, config.TSDB_PORT, config.TSDB_DATABASE)
print("Connection to database", CONNECTION)
conn = psycopg2.connect(CONNECTION)
cur = conn.cursor()



class App:
    async def reconnect(self):
        print("Disconnected, Trying to reconnect!")
        time.sleep(5)
        await self.ib.connectAsync()
        contracts = [
            ibi.Stock(symbol, 'SMART', 'USD')
            for symbol in tickerList]
        for contract in contracts:
            #self.ib.reqMarketDataType(3)
            self.ib.reqMktData(contract)
        print("connected, waiting for data")
        self.ib.disconnectedEvent += lambda: asyncio.create_task(self.reconnect())
        conn = psycopg2.connect(CONNECTION)
        cur = conn.cursor()

    async def run(self):
        global last_time
        global current_time
        global firsttime
        global data_package
        global prevdataclose
        self.ib = ibi.IB()
        with await self.ib.connectAsync():
            contracts = [
                ibi.Stock(symbol, 'SMART', 'USD')
                for symbol in tickerList]
            for contract in contracts:
                #self.ib.reqMarketDataType(3)
                self.ib.reqMktData(contract)
            print("connected, waiting for data")

            self.ib.disconnectedEvent += lambda: asyncio.create_task(self.reconnect())

            async for tickers in self.ib.pendingTickersEvent:
                for ticker in tickers:
                    #print(ticker.contract.symbol)
                    #print(ticker.time)
                    for tick in ticker.ticks:
                        if tick.tickType == 4:
                            current_time = tick.time.replace(second=0,microsecond=0)
                            #current_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
                            if last_time == current_time:
                                firsttime = 0
                                lists[tickerList.index(ticker.contract.symbol)].append(tick.price)
                                #print(ticker.contract.symbol, tick.price, tick.size, tick.tickType)
                                
                            
                            else:
                                print('new minute: ', current_time, datetime.datetime.now().replace(microsecond=0))
                                
                                #print(lists)
                                # if firsttime:
                                #     onehour = current_time + datetime.timedelta(minutes=90)
                                #     print('Endtime:',onehour)
                                
                                if not firsttime:
                                    data_package = []
                                    for x in range(0,len(tickerList)):
                                        if lists[x]:

                                            if volume[x]:
                                                minutevolume = volume[x][-1] - volume[x][0]
                                            else:
                                                minutevolume = 0

                                            prevdataclose[x] = lists[x][-1]

                                            #ohlc = (lists[x][0],max(lists[x]),min(lists[x]),lists[x][-1])
                                            curData = (last_time.strftime('%Y-%m-%d %H:%M:%S'),tickerList[x],minutevolume,lists[x][0],max(lists[x]),lists[x][-1],min(lists[x]),time.mktime(current_time.timetuple())*1000)
                                            lists[x] = []
                                            volume[x] = []
                                        
                                        else: #if data is empty
                                            print("DATA WAS MISSING")
                                            print(lists)
                                            curData = (last_time.strftime('%Y-%m-%d %H:%M:%S'),tickerList[x],0,prevdataclose[x],prevdataclose[x],prevdataclose[x],prevdataclose[x],time.mktime(current_time.timetuple())*1000)
                                        
                                        data_package.append(curData)

                                    
                                    print('data: package ready')
                                    DBInsert(SQL_PATH)
                                    #CSVInsert(data_package)
                                    print('data: package sent')

                            last_time = current_time
                        
                        if tick.tickType == 8:
                            volume[tickerList.index(ticker.contract.symbol)].append(tick.size)

                                    

    def stop(self):
        self.ib.disconnect()

def DBInsert(sql_path):
    #print(data_package)
    if data_package:
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

def CSVInsert(data):
    with open('out.csv', 'a', newline='') as f_object:  
        # Pass the CSV  file object to the writer() function
        writer_object = writer(f_object)
        # Result - a writer object
        # Pass the data in the list as an argument into the writerow() function
        writer_object.writerow(data)  
        # Close the file object
        f_object.close()


app = App()
try:
    asyncio.run(app.run())
except (KeyboardInterrupt, SystemExit):
    app.stop()


