from Algo_Functions import ListAverage,Calc_EMA
from datetime import datetime, timedelta

#A = datetime(2020, 11, 18, 18, 11, 0)
#AM_candlesticks = [[1,1,1,A],[2,2,2,A],[3,3,3,A]]
#print(ListAverage(AM_candlesticks))

test_data = [1.125,2.12,4.13,4.56,5.73,4.62,3.62,4.73,5.83,6.52,7.62,8.26,5.26]
EMA = Calc_EMA(5,test_data,0,1)
print(EMA)
EMA = Calc_EMA(5,8.43,EMA,0)
print(EMA)
    
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
