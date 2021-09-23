import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from extra import keystore,config
import alpaca_trade_api as tradeapi
import pandas as pd

base_url = 'https://paper-api.alpaca.markets'
api = tradeapi.REST(keystore.API_KEY, keystore.SECRET_KEY, base_url, api_version='v2')

def todict(bar):
    return{
        'time':bar.t,
        'volume':bar.v,
        'open': bar.o,
        'high':bar.h,
        'close':bar.c,
        'low':bar.l
    }

def getAlpacaData(Ticker):
    #Ticker = 'AAPL'
    # Get daily price data for AAPL over the last 5 trading days.
    barset = api.get_barset(Ticker, '1Min', limit=200)
    bars = barset[Ticker]

    BackTestAM_candlesticks = pd.DataFrame([todict(t) for t in bars ])
    BackTestAM_candlesticks['datetime'] = pd.to_datetime(BackTestAM_candlesticks['time'])
    BackTestAM_candlesticks = BackTestAM_candlesticks.set_index('datetime')
    BackTestAM_candlesticks.drop(['time'], axis=1, inplace=True)
    BackTestAM_candlesticks = BackTestAM_candlesticks.between_time('8:00', '16:30')

    return BackTestAM_candlesticks


    #print(bars[0].__dict__)

    # See how much AAPL moved in that timeframe.
    # week_open = aapl_bars[0].o
    # week_close = aapl_bars[-1].c
    # percent_change = (week_close - week_open) / week_open * 100
    # print('AAPL moved {}% over the last 5 days'.format(percent_change))