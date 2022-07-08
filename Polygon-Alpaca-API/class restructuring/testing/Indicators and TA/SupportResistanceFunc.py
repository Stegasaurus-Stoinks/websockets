import numpy as np

def calculateslope(x1,y1,x2,y2):
        slope = float((y2-y1)/(x2-x1))
        return slope

def createline(slope,x1,y1,x2,y2,data,keypoints,plotSize,wiggle = 0.02):
    plot = False
    score = 0 #using this to rank the trend lines based on how many bounces bounce off the line
    line = [np.NaN] * plotSize
    for k in range(x1,x2+1):
        line[k] = (y1-slope*x1)+(slope*k)

    wiggle1 = wiggle #using these to give a little leway to the "bouncing off the line" check

    #check to make sure there are no lows in the range the invalidate the line
    for j in range(x1,x2):
        if line[j] <= data[j]+wiggle1:
            plot = True
            #score the line based on how many other points touch the line
            if line[j]-wiggle <= data[j] <= line[j]+wiggle:
                #score += 1
                #score the line based on how many other "key" points touch the line
                if j in keypoints:
                    score+=1

        else:
            plot = False
            return line,0
    
    if plot:
        return line,score

def HA(df):
    df['HA_Close']=(df['open']+ df['high']+ df['low']+df['close'])/4

    idx = df.index.name
    df.reset_index(inplace=True)

    for i in range(0, len(df)):
        if i == 0:
            df.at[i, 'HA_Open'] = ((df._get_value(i, 'open') + df._get_value(i, 'close')) / 2)
        else:
            df.at[i, 'HA_Open'] = ((df._get_value(i - 1, 'HA_Open') + df._get_value(i - 1, 'HA_Close')) / 2)

    if idx:
        df.set_index(idx, inplace=True)

    df['HA_High']=df[['HA_Open','HA_Close','high']].max(axis=1)
    df['HA_Low']=df[['HA_Open','HA_Close','low']].min(axis=1)
    return df