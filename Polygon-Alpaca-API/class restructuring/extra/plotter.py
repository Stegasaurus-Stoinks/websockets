from mplfinance.original_flavor import candlestick_ohlc
import mplfinance as mpf
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import time
import numpy as np
plt.ion()

class LiveChartEnv:
    def __init__(self, time_frame, candle_window, wait = 0.01):
        self.time_frame = time_frame
        self.candle_window = candle_window
        self.wait = wait
        print('Class initialized succesfully')
    
    def initialize_chart(self):

        #self.fig = mpf.figure(style='charles',figsize=(7,8))
        self.fig = mpf.figure(figsize=(7,8))
        self.ax1 = self.fig.subplot(2,1,1)
        self.ax2 = self.fig.add_subplot(2,1,2)
        #self.fig.show()
        #self.fig.canvas.draw()

        #self.fig = plt.figure(figsize=(8,5))
        #self.ax = plt.subplot2grid((1,1), (0,0))
        #plt.ion()
        #self.fig.show()
        #self.fig.canvas.draw()
        
    def update_chart(self, candle_data, extraData = [], style = []):
            candle_data = candle_data.sort_index(ascending=True)
            candle_counter = range(len(candle_data["open"]))
            ohlc = []
            for candle in candle_counter:
                append_me = candle_counter[candle], \
                            candle_data["open"][candle], \
                            candle_data["high"][candle],  \
                            candle_data["low"][candle], \
                            candle_data["close"][candle]
                ohlc.append(append_me)
            #print(candle_data)

            extraPlots = []
            if extraData:
                for i in range(0,len(extraData),1):
                    if style[i][0] == 'scatter':
                        if style[i][1] == 'up':
                            extraPlots.append(mpf.make_addplot(extraData[i],type='scatter',markersize=200,marker='^', ax=self.ax1))
                        if style[i][1] == 'down':
                            extraPlots.append(mpf.make_addplot(extraData[i],type='scatter',markersize=200,marker='v', ax=self.ax1))
                        if style[i][1] == 'normal':
                            extraPlots.append(mpf.make_addplot(extraData[i],type='scatter',markersize=200, ax=self.ax1))

                    if style[i][0] == 'line':
                        if style[i][1] == 'normal':
                            extraPlots.append(mpf.make_addplot(extraData[i], ax=self.ax1))
                        if style[i][1] == 'dashdot':
                            extraPlots.append(mpf.make_addplot(extraData[i],linestyle='dashdot', ax=self.ax1))

            volAvg = int(candle_data["volume"].mean())
            mean = [volAvg] * len(candle_data)
            extraPlots.append(mpf.make_addplot(mean,markersize=200, ax=self.ax2))
            self.ax1.clear() # - Clear the chart
            self.ax2.clear()


            mpf.plot(candle_data,type='candle',style='charles', addplot=extraPlots, ax=self.ax1, volume=self.ax2)
            #mpf.plot(candle_data,type='candle',ax=self.ax1)
            plt.show()
            plt.pause(0.0001)
            
            
            self.fig.canvas.draw() # - Draw on the chart
            #self.fig.show()

            