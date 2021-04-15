import re

test = 'BTO CRWD blahblahblah 3/26 @2.38'

print(re.search("[$]*[0-9.]+[cCpP]", test))

tempList = {'name': 'name', 'tradeType': 'tradeType', 'ticker': 'ticker', 'strikePrice': 'strikePrice', 'optionType': 'optionType', 'date': 'date', 'price': 'price', 'timePlaced':'now'}
print(tempList)

tempList['traded'] = True

print(tempList)