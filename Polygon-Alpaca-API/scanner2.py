import config
import csv
import pandas as pd
from polygon import RESTClient
from datetime import date, time, datetime
import time

def main():

    nasdaq_traded_raw = pd.read_csv("../../../../Downloads/nasdaqlisted.txt",delimiter='|',skipfooter=1,engine='python')
    #print raw data
    #print(nasdaq_traded)

    #filter raw data to get only valid tickers
    nasdaq_traded_valid = nasdaq_traded_raw[(nasdaq_traded_raw["Test Issue"] == "N") & (nasdaq_traded_raw["Financial Status"] == "N")]

    #split ETFs and Stocks
    nasdaq_traded_ETF = nasdaq_traded_valid[nasdaq_traded_valid["ETF"] != "N"]
    nasdaq_traded = nasdaq_traded_valid[nasdaq_traded_valid["ETF"] == "N"]
 
    #further filtering
    nasdaq_tradedQ = nasdaq_traded[nasdaq_traded["Market Category"] == "Q"]
    print(nasdaq_tradedQ)

    key = config.API_KEY
    polygon_snapshot = pd.DataFrame(columns=['Symbol', 'todaysChange'])

    print(nasdaq_tradedQ.Symbol)
    
    
    with RESTClient(key) as client:
        response = client.stocks_equities_snapshot_all_tickers()
        print("Reading data from nasdaq list")
        tickernum = 0
        for ticker in response.tickers:
            tickernum += 1
            if tickernum % 100 == 0:
                print(str(tickernum) + " tickers read")
            #print(f" {ticker['ticker']} dropped {ticker['todaysChange']}$ which was {ticker['todaysChangePerc']}% updated @ {ticker['updated']}")
            #print(new_row)
            symbol = ticker['ticker']
            if symbol in nasdaq_tradedQ.values:
                #print(str(symbol) + " is in nasdaq_tradedQ")
                new_row = {'Symbol':ticker['ticker'], 'todaysChange':ticker['todaysChange']}
                polygon_snapshot = polygon_snapshot.append(new_row, ignore_index=True)

    
    print(polygon_snapshot)
    #tickers = ['AAPL', 'MSFT']
    #polygon_snapshot = polygon_snapshot[polygon_snapshot.Symbol.isin(nasdaq_tradedQ.Symbol)]
    #print(polygon_snapshot)
    #polygon_snapshot = polygon_snapshot[polygon_snapshot.Symbol.isin(tickers)]
    #print(polygon_snapshot)



if __name__ == '__main__':

    main()
    while(1):
        now = datetime.now()
        if now.hour == 6 and now.minute == 30:
            main()
            quit()
    
        else:
            #print("not time yet")
            time.sleep(60)