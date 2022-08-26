import finnhub
from datetime import datetime
import pandas as pd
from candle import Candle

# Setup client
finnhub_client = finnhub.Client(api_key="c1hvriv48v6sod8lo0n0")

import websocket
import json

tickers = ["BINANCE:BTCUSDT"]

BINANCE:BTCUSDT = 

def on_message(ws, message):
    global last_time, o, h, l, c, v, timestamp, candles
    #example message:{'c': None, 'p': 58667.6, 's': 'BINANCE:BTCUSDT', 't': 1617166936886, 'v': 0.000193}
    try:
        data = json.loads(message)["data"]
        for package in data:
            sercurity = package['s']
            price = package['p']
            volume = package['v']
            unix = int(package['t'])
            time = datetime.utcfromtimestamp(unix/1000)
            if time.minute != last_time.minute:
                print(f'{timestamp} - O:{o} H:{h} L:{l} C:{c} Volume:{v} - {unix}')
                candle = {'timestamp':timestamp, 'o':o,'h':h, 'l':l, 'c':c,'v':v}
                candles = candles.append(candle,ignore_index=True)
                print(candles)
                o, h, l, c, v, timestamp = 0,price,price,price,0,time
                #print("form new candle")
                last_time = time
                
                
                

            else:
                c = price

                if price > h:
                    h = price

                if price < l:
                    l = price

                if o == 0:
                    o = price

                v = v + volume

            
            #print(f't:{time} - {sercurity} @ {price:.2f} - v:{volume}')

    except:
        print(message)

    if candles.shape[0] > 10:
        # Stock candles
        quit()
        

        
    

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    for ticker in tickers:
        ticker = type()
        ws.send(json.dumps({"type":"subscribe","symbol": ticker}))

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=c1hvriv48v6sod8lo0n0",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

