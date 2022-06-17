# from ib_insync import *

# class Trading:
#     def __init__(self):
#          self.dataStreams = []
#          self.conn = IB()  #establish connecting to the api
#          self.conn.connect(host='127.0.0.1', port=7497, clientId=0)
#          self.tickers = [('TSLA'), ('SPY')]

#     def _stream_data(self): # this function established the data stream and appends it to an array
#          for contract in self.tickers:
#               stock = Stock(contract, exchange="SMART", currency="USD")
#               self.conn.reqMarketDataType(3)
#               stream = self.conn.reqMktData(stock, '', False, False)
#               self.dataStreams.append(stream)
#               self.conn.sleep(1)

#     def start(self):
#         self._stream_data()  # fill the datastream array
#         print(self.dataStreams[0].last , self.dataStreams[1].last)  # so this should return the sum of two prices, but it does not

# strategy = Trading()
# strategy.start()

import asyncio
from time import time_ns

import ib_insync as ibi
import pandas as pd
import numpy as np
import datetime
from enum import Enum

tickerList = ['AAPL','TSLA','SPY','AMD','GME']
#tickerList = ['AAPL']
candles = []
lists = []

firsttime = 1

for ticker in tickerList:
    lists.append([])
    candles.append([])

symbol = 'AAPL'

#lists[tickerList.index(symbol)].append(9)
#print(lists)

#lists[0].append(9)
#lists[1].append(8)

#print(lists)

current_time = datetime.datetime(1, 1, 1, 1, 1, 1, 1, tzinfo=datetime.timezone.utc).replace(second=0,microsecond=0)
last_time = datetime.datetime(1, 1, 1, 1, 1, 1, 1, tzinfo=datetime.timezone.utc).replace(second=0,microsecond=0)



class App:
    
    async def run(self):
        global last_time
        global current_time
        global firsttime
        self.ib = ibi.IB()
        with await self.ib.connectAsync():
            contracts = [
                ibi.Stock(symbol, 'SMART', 'USD')
                for symbol in tickerList]
            for contract in contracts:
                #self.ib.reqMarketDataType(3)
                self.ib.reqMktData(contract)

            async for tickers in self.ib.pendingTickersEvent:
                for ticker in tickers:
                    #print(ticker.contract.symbol)
                    #print(ticker.time)
                    for tick in ticker.ticks:
                        if tick.tickType == 4:
                            current_time = tick.time.replace(second=0,microsecond=0)
                            if last_time == current_time:
                                firsttime = 0
                                lists[tickerList.index(ticker.contract.symbol)].append(tick.price)
                                #print(ticker.contract.symbol, tick.price, tick.size, tick.tickType)
                                
                            
                            else:
                                print('new minute: ', current_time, datetime.datetime.now().replace(microsecond=0))
                                last_time = current_time
                                #print(lists)
                                if firsttime:
                                    onehour = current_time + datetime.timedelta(minutes=90)
                                    print('Endtime:',onehour)
                                
                                if not firsttime:
                                    for x in range(0,len(tickerList)):
                                        candles[x].append([lists[x][0],max(lists[x]),min(lists[x]),lists[x][-1]])
                                        lists[x] = []

                                    #print(candles)
                                    if current_time >= onehour:
                                        print('done')
                                        my_df = pd.DataFrame(candles)

                                        print(my_df)

                                        my_df.to_csv('out.csv', index=False, header=False)
                                        quit()

                                    

    def stop(self):
        self.ib.disconnect()


app = App()
try:
    asyncio.run(app.run())
except (KeyboardInterrupt, SystemExit):
    app.stop()