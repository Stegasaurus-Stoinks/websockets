import shrimpy
import plotly.graph_objects as go

# sign up for the Shrimpy Developer APIs for your free API keys
shrimpy_public_key = '5c5c5f288b4d61a98780c3d25ddf71f76f51b7f47d2da41e10255b5d06b6b560'
shrimpy_secret_key = '13c3e415e5c478123a2dfe4a2b5274a0f8d732228ea179b1cef72d36756e117ef3def0e59cc5b4cf729e1e22cf7314c8bfc09581239befdfa8711b4993f46ea8'

# collect the historical candlestick data
client = shrimpy.ShrimpyApiClient(shrimpy_public_key, shrimpy_secret_key)
candles = client.get_candles(
    'binance', # exchange
    'LTC',         # base_trading_symbol
    'USD',         # quote_trading_symbol
    '1m'           # interval
)

dates = []
open_data = []
high_data = []
low_data = []
close_data = []

# format the data to match the plotting library
for candle in candles:
    dates.append(candle['time'])
    open_data.append(candle['open'])
    high_data.append(candle['high'])
    low_data.append(candle['low'])
    close_data.append(candle['close'])

# plot the candlesticks
fig = go.Figure(data=[go.Candlestick(x=dates,
                       open=open_data, high=high_data,
                       low=low_data, close=close_data)])
fig.show()