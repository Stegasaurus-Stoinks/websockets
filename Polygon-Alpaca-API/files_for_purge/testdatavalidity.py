import csv
import pandas as pd
from matplotlib import ticker

def stringToList(string):
    listRes = list(string.split(','))
    return listRes

with open('out.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

tickerdata = []
#print(data)
for segment in data:
    #print(segment)
    for tick in segment:
        tick = tick[1:-1]
        tick[2] = Integer.parseInt(tick[2])
        print(stringToList(tick))

        
        
#print(tickerdata)

df = pd.DataFrame(data, columns = ['Time', 'Ticker','Volume','Open','High','Low','Close','unix'])

print(df)