import matplotlib.pyplot as plt
import numpy as np

def IsDownTrend(Start, End, AM_candlesticks):
    downtrend_candles = 0
    downtrend_value = 0.00
    uptrend_candles = 0
    uptrend_value = 0.00

    for x in range(Start,End,-1):
        current_candle = AM_candlesticks[x]
        cur_change = current_candle['change']
        #previous_candle = AM_candlesticks[x-1]
        if cur_change < 0:
            downtrend_candles += 1
            downtrend_value -= cur_change

        else:
            uptrend_candles += 1
            uptrend_value += cur_change

    if downtrend_candles > uptrend_candles and downtrend_value > uptrend_value:
        return True

    else:
        return False

def formatTime(timey):
    year = timey.year
    month = timey.month
    day = timey.day
    hour = timey.hour
    minute = timey.minute
    second = timey.second

    timeyy = "{}-{}-{} {}:{}:{}".format(year, month , day, hour, minute, second)
    return timeyy
    
def ListAverage(ListofList):
    Totals = [sum(i) for i in zip(*ListofList) if type(i)==int]
    Length = len(ListofList)
    Average = [x / Length for x in Totals]
    return Average

# use ggplot style for more sophisticated visuals
plt.style.use('ggplot')

def plotter(x_vec,y1_data,y2_data,y3_data,y4_data,y5_data,line1,line2,line3,line4,line5,identifier='',pause_time=0.1):
    if line1==[]:
        # this is the call to matplotlib that allows dynamic plotting
        plt.ion()
        fig = plt.figure(figsize=(13,6))
        ax = fig.add_subplot(111)
        # create a variable for the line so we can later update it
        line1, = ax.plot(x_vec,y1_data,'-o',alpha=0.8)
        line2, = ax.plot(x_vec,y2_data,'-o',alpha=0.8)
        line3, = ax.plot(x_vec,y3_data,'-o',alpha=0.8)
        line4, = ax.plot(x_vec,y3_data,'-o',alpha=0.8)
        line5, = ax.plot(x_vec,y3_data,'-o',alpha=0.8)            
        #update plot label/title
        plt.ylabel('Y Label')
        plt.title('Title: {}'.format(identifier))
        plt.show()
    
    # after the figure, axis, and line are created, we only need to update the y-data
    line1.set_ydata(y1_data)
    line2.set_ydata(y2_data)
    line3.set_ydata(y3_data)
    line4.set_ydata(y4_data)
    line5.set_ydata(y5_data)
    # adjust limits if new data goes beyond bounds
    min1 = min(np.min(y1_data), np.min(y2_data), np.min(y3_data), np.min(y4_data), np.min(y5_data))
    max1 = max(np.max(y1_data), np.max(y2_data), np.max(y3_data), np.max(y4_data), np.max(y5_data))

    if min1<=line1.axes.get_ylim()[0] or min1>=line1.axes.get_ylim()[0]+(min1*0.02) or max1>=line1.axes.get_ylim()[1] or max1<=line1.axes.get_ylim()[0]-(max1*0.02):
        plt.ylim([min1-np.std(y1_data),max1+np.std(y1_data)])
    # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
    plt.pause(pause_time)
    
    # return line so we can update it again in the next iteration
    return line1, line2, line3, line4, line5

def Calc_EMA(length,data,old_EMA=0,initial_val=0):
    EMA = 0.00
    k = 2/(length+1)
    #print(data)

    if initial_val == 1:
        #if EMA has never been calculatedb
        if length > len(data):
            return "Error"
        data = data[len(data)+1-length:len(data)+1]

        for x in range(len(data)):
            EMA = (data[x] * k) + (EMA*(1-k))

        return round(EMA,2)

    else:
        EMA = (data*k)+(old_EMA*(1-k))

        return round(EMA,2)
