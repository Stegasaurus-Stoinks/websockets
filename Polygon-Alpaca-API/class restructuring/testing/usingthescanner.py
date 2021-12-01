import sys, os
import keyboard
import numpy as np
from scipy.signal import argrelextrema

import mplfinance as mpf
import matplotlib.pyplot as plt
from matplotlib import gridspec
from mplfinance import plotting

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from testing.scanner import scanner
from extra.Data_Collection_Historical import getAlpacaData

scan_results = scanner(num = 5, signal = 'Most Active', filter={'Exchange':'NASDAQ','Index':'S&P 500','Market Cap.':'+Large (over $10bln)','Average Volume':'Over 100K'})

print(scan_results)
tickerlist = list(scan_results['Ticker'])
print(tickerlist)

for ticker in tickerlist:
    keyboard.wait('right arrow')
    os.system('cls')
    print("Now analyzing ticker:",ticker)
    data = getAlpacaData(ticker,500)
    print(data.head())
    
    n = 60
    ilocs_min = []
    ilocs_max = []

    while(len(ilocs_max) + len(ilocs_min)) < 8:
        n = n-1
        ilocs_min = argrelextrema(data.low.values, np.less_equal, order=n)[0]
        ilocs_max = argrelextrema(data.high.values, np.greater_equal, order=n)[0]
        
    print("starting n =",n)


    plt.ion()
    plt.close('all')

    extraplots = []
    spec = gridspec.GridSpec(ncols=1, nrows=2, hspace=0.5, height_ratios=[2, 1])
    fig = mpf.figure(figsize=(7,8))
    ax1 = fig.subplot(spec[0])
    ax2 = fig.add_subplot(spec[1])
    fig.gridspec_kw={'height_ratios': [1, 2]}

    mins = [np.NaN] * data.shape[0]
    for i in range (0,len(ilocs_min)):
        mins[ilocs_min[i]] = data.iloc[ilocs_min[i]].low * 0.999

    maxs = [np.NaN] * data.shape[0]
    for i in range (0,len(ilocs_max)):
        maxs[ilocs_max[i]] = data.iloc[ilocs_max[i]].high * 1.001

    extraplots.append(plotting.make_addplot(mins,type='scatter',markersize=200,marker='^',ax=ax1))
    extraplots.append(plotting.make_addplot(maxs,type='scatter',markersize=200,marker='.',color='b',ax=ax1))

    mpf.plot(data,type='candle',style='charles',addplot= extraplots,warn_too_much_data=10000000000,ax=ax1, volume=ax2)

    #open window in full screen
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    
    plt.show()
    plt.pause(1)

keyboard.wait('right arrow')




