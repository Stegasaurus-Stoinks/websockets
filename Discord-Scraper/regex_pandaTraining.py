import pandas as pd
import re
from datetime import datetime


"""
BTO CRWD $210C 3/26 @2.38
 Long: CRWD Mar 26 2021 $210.00 Call @ 2.38 | market : $2.4

STC FSLY 77c 3/19 @.19 all
 Closed long: FSLY Mar 19 2021 $77.00 Call @ 0.19 | market : $0.19

STC NFLX 500p 3/19 @1.45
Closed long: NFLX Mar 19 2021 $500.00 Put @ 1.45 | market : $1.45

BTO FB 280p 3/19 @1.42 yolo still above 281.50 is strength but risking it
Long: FB Mar 19 2021 $280.00 Put @ 1.42 | market : $1.35

STC SQQQ 3/26/21 13P @ 0.66 (bot)
Closed long: SQQQ Mar 26 2021 $13.00 Put @ 0.66 | market : $0.36
"""
pandy = pd.DataFrame(columns=['tradeType', 'ticker', 'strikePrice', 'optionType', 'date', 'price', 'timePlaced'])
list = ["BTO CRWD $210C 3/26 @2.38", "STC FSLY 77c 3/19 @.19 all", "STC NFLX 500p 3/19 @1.45", 
        "BTO FB 280p 3/19 @1.42 yolo still above 281.50 is strength but risking it", "STC SQQQ 3/26/21 13P @ 0.66 (bot)"]
#pandy.columns = ['tradeType','ticker','strikePrice','date','price', 'timePlaced']


for testy in list:

    splitString = re.split("\s", testy, 2)
    #print(splitString)

    tradeType = splitString[0]
    ticker = splitString[1]
    otherStuff = splitString[2]

    strikePrice = re.search("[$]*[0-9.]*[cCpP]", otherStuff)
    strikePrice = strikePrice.group()
    #print("Strike Price = " + strikePrice)


    if strikePrice.startswith('$'):
        strikePrice = strikePrice[1:]

    if strikePrice.endswith('c') or strikePrice.endswith('C'):
        strikePrice = strikePrice[:-1]
        optionType = "C"
    elif strikePrice.endswith('p') or strikePrice.endswith('P'):
        strikePrice = strikePrice[:-1]
        optionType = "P"






    date = re.search("[0-9]+[/][0-9]+[0-9/]*", otherStuff)
    date = date.group()
    #print("Date = " + date)

    price = re.search("[@][ ]*[0-9.]+[0-9.]+", otherStuff)
    price = price.group()
    #print("price = " + price)

    now = datetime.now()

    tempList = {'tradeType': tradeType, 'ticker': ticker, 'strikePrice': strikePrice, 'optionType': optionType, 'date': date, 'price': price, 'timePlaced':now}

    #print(tempList)
    pandy = pandy.append(tempList, ignore_index=True)
    
    #print("\n")

#print(pandy.tail())

name = "Justinvred#2767"
test = re.search("[#][0-9]+", name)
print(test.group())
print(test.span())
print(name.rstrip(test.group()))
#TODO: turn date into dateTime object
#TODO: add names to panda
#TODO: remove number sign from price
#TODO: add logic for stuff