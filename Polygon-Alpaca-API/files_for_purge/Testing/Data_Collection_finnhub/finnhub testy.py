import finnhub
from datetime import datetime
import pandas as pd

# Setup client
finnhub_client = finnhub.Client(api_key="c1hvriv48v6sod8lo0n0")

#res = finnhub_client.stock_candles('BINANCE:BTCUSDT', 'M', 1617253063, 1617253320)
#print(res)

#Convert to Pandas Dataframe
#import pandas as pd
#print(pd.DataFrame(res))

#quit()
import websocket
import json

last_time = datetime(1,1,1,1,1,1)
timestamp = datetime(1,1,1,1,1,1)
o, h, l, c, v = 0,0,0,0,0
candles = pd.DataFrame(columns=('timestamp','o','h','l','c','v'))

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
    #ws.send('{"type":"subscribe","symbol":"AAPL"}')
    #ws.send('{"type":"subscribe","symbol":"AMZN"}')
    ws.send('{"type":"subscribe","symbol":"BINANCE:ETHUSDT"}')
    #ws.send('{"type":"subscribe","symbol":"IC MARKETS:1"}')

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=c1hvriv48v6sod8lo0n0",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

