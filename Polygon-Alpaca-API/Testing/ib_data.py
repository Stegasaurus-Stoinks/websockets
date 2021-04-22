from ib_insync import *
import time
import pandas as pd
import numpy as np

ib = IB()
ib.connect(host='127.0.0.1', port=7496, clientId=1)

nflx_contract = Stock('NFLX', 'SMART', 'USD')

historical_data_nflx = ib.reqHistoricalData(
    nflx_contract, 
    '', 
    barSizeSetting='15 mins', 
    durationStr='2 D', 
    whatToShow='MIDPOINT', 
    useRTH=True
    )