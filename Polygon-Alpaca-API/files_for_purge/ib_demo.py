from ib_insync import *

ib = IB()
ib.connect('127.0.0.1', 7496, clientId=1)

contract = Forex('EURUSD')
AMDcontract = Stock('AMD', 'SMART', 'USD')

bars = ib.reqHistoricalData(
    AMDcontract, endDateTime='', durationStr='30 D',
    barSizeSetting='1 hour', whatToShow='MIDPOINT', useRTH=True)

# convert to pandas dataframe:
df = util.df(bars)
print(df)