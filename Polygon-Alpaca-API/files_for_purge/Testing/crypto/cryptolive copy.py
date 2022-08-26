import shrimpy
import plotly.graph_objects as go
import time

# sign up for the Shrimpy Developer APIs for your free API keys
public_key = '5c5c5f288b4d61a98780c3d25ddf71f76f51b7f47d2da41e10255b5d06b6b560'
private_key = '13c3e415e5c478123a2dfe4a2b5274a0f8d732228ea179b1cef72d36756e117ef3def0e59cc5b4cf729e1e22cf7314c8bfc09581239befdfa8711b4993f46ea8'

# This is a sample handler, it simply prints the incoming message to the console
def error_handler(err):
    print(err)


# This is a sample handler, it simply prints the incoming message to the console
def handler(msg):
    print(msg)


api_client = shrimpy.ShrimpyApiClient(public_key, private_key)
raw_token = api_client.get_token()
client = shrimpy.ShrimpyWsClient(error_handler, raw_token['token'])

subscribe_data = {
    "type": "subscribe",
    "exchange": "coinbasepro",
    "pair": "ltc-btc",
    "channel": "orderbook"
}

# Start processing the Shrimpy websocket stream!
client.connect()
client.subscribe(subscribe_data, handler)

time.sleep(10)
# Once complete, stop the client
client.disconnect()