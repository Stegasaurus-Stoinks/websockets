import websocket
import config
import time

def on_message(ws, message):
	print(message)

def on_error(ws, error):
	print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
	ws.send('{"action":"auth","params":"AK88VYVZKTW30FTZ0X7S"}')
	ws.send('{"action":"subscribe","params":"T.AAPL,T.MSFT,T.TSLA"}')

if __name__ == "__main__":
	# websocket.enableTrace(True)
	ws = websocket.WebSocketApp("wss://socket.polygon.io/stocks",
							  on_message = on_message,
							  on_error = on_error,
							  on_close = on_close)
	ws.on_open = on_open
	ws.run_forever()
    
    ws.close()