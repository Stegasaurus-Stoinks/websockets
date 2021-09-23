import sys, os
import keyboard

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from testing.scanner import scanner
from extra.Data_Collection_Historical import getAlpacaData

scan_results = scanner(num = 21, signal = 'Most Active', filter={'Exchange':'NASDAQ','Index':'S&P 500','Market Cap.':'+Large (over $10bln)','Average Volume':'Over 100K'})

print(scan_results)
tickerlist = list(scan_results['Ticker'])
print(tickerlist)

for ticker in tickerlist:
    keyboard.wait('right arrow')
    os.system('cls')
    print("Now analyzing ticker:",ticker)
    data = getAlpacaData(ticker)
    print(data)

