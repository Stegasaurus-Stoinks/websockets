from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import time

class LiveChartEnv:
    def __init__(self, time_frame, candle_window, wait = 0.01):
        self.time_frame = time_frame
        self.candle_window = candle_window
        self.wait = wait
        print('Class initialized succesfully')
    
    def initialize_chart(self):
        self.fig = plt.figure(figsize=(8,5))
        self.ax = plt.subplot2grid((1,1), (0,0))
        plt.ion()
        self.fig.show()
        self.fig.canvas.draw()
        
    def update_chart(self, candle_data):
            candle_counter = range(len(candle_data["open"]))
            ohlc = []
            for candle in candle_counter:
                append_me = candle_counter[candle], \
                            candle_data["open"][candle], \
                            candle_data["high"][candle],  \
                            candle_data["low"][candle], \
                            candle_data["close"][candle]
                ohlc.append(append_me)
            self.ax.clear() # - Clear the chart
            candlestick_ohlc(self.ax, ohlc, width=0.4, colorup='#075105', colordown='#AF141A')
            for label in self.ax.xaxis.get_ticklabels():
                label.set_rotation(45)
            self.ax.xaxis.set_major_locator(mticker.MaxNLocator(10))
            self.ax.grid(True)
            plt.grid(False)
            plt.xlabel('Candle count')
            plt.ylabel('Price')
            plt.title('Candlestick chart simulation')
            plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
            self.fig.canvas.draw() # - Draw on the chart