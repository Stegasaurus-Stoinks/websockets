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