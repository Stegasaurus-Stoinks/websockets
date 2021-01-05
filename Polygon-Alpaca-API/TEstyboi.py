from Algo_Functions import ListAverage
from datetime import datetime, timedelta

#A = datetime(2020, 11, 18, 18, 11, 0)
#AM_candlesticks = [[1,1,1,A],[2,2,2,A],[3,3,3,A]]
#print(ListAverage(AM_candlesticks))
    
from Algo_Functions import plotter
import numpy as np

size = 20
x_vec = np.linspace(0,1,size+1)[0:-1]
y_vec = np.zeros(len(x_vec))
y_vec2 = np.zeros(len(x_vec))
line1 = []
line2 = []
while True:
    rand_val = np.random.randn(1)
    y_vec[-1] = 1
    y_vec2[-1] = rand_val
    line1,line2 = plotter(x_vec,y_vec,y_vec2,line1,line2)
    y_vec = np.append(y_vec[1:],0.0)
    y_vec2 = np.append(y_vec2[1:],0.0)
