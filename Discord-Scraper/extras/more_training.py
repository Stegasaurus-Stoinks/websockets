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











scaleList = {"half","scale","scale out"}

testString = "scale out"

for i in scaleList:
   temp = re.search(i, testString)
   if temp != None:
      if temp.group() == i:
         print("Found ",temp.group())
         getPercentage(temp.group())
      