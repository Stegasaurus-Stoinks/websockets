import re
from typing import Literal
#import eva_panda
from enum import Enum

test = 'BTO CRWD blahblahblah 3/26 @2.38'
#print(re.search("[$]*[0-9.]+[cCpP]", test))

tempList = {'name': 'name', 'tradeType': 'tradeType', 'ticker': 'ticker', 'strikePrice': 'strikePrice', 'optionType': 'optionType', 'date': 'date', 'price': 'price', 'timePlaced':'now'}
#print(tempList)

tempList['traded'] = True




def getPercentage(key):
   switcher = {
      "scale" : 0.5,
      "scrape" : 0.25,
      "half" : 0.75
   }
   return switcher.get(key)










switcher = {
      "scale" : 0.50,
      "scrape" : 0.25,
      "scalp" : 0.50,
      "more" : 0.50,
      "some more" : 0.50,
      "runner" : 0.50,
      "risky scalp" : 0.50,
      "half" : 0.50, #Sold half, hold a few runners if you want
      "*" : 0.50,
      "*" : 0.50,
      "*" : 0.50,
      "*" : 0.50,
      "*" : 0.50,
      "*" : 0.50,
      "*" : 0.50,
      "*" : 0.50,
      "*" : 0.50,
      "*" : 0.50,
      "*" : 0.50,
      "*" : 0.50,
      "*" : 0.50,
      "*" : 0.50,
      "*" : 0.50,
      "*" : 0.50,
      "*" : 0.50,
      "*" : 0.50,
      "*" : 0.50,
      "*" : 0.50,
      "*" : 0.50,
      "*" : 0.50,
      "*" : 0.50,

   }

for i in switcher:
   print('1')