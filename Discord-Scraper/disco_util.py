import re
from typing import Literal


"""
This section will be the getters for every piece of data we need from the message
"""

Animal = Literal['ant', 'bee', 'cat', 'dog']


def getName(author):
    #Get name variable
    tempName = re.search("[#][0-9]+", author)
    name = author.rstrip(tempName.group())
    print(name)
    return name


def getStrikePrice(message):
    strikePrice = re.search("[$]*[0-9.]+[cCpP]", message)
    if strikePrice == None:
        return
    strikePrice = strikePrice.group()
    strikePrice = str.replace(strikePrice, '@', '')
    print("Strike Price = " + strikePrice)

    if strikePrice.startswith('$'):
        strikePrice = strikePrice[1:]
    return strikePrice


def getOptionType(strikePrice):
    if strikePrice.endswith('c') or strikePrice.endswith('C'):
        strikePrice = strikePrice[:-1]
        optionType = "C"
    elif strikePrice.endswith('p') or strikePrice.endswith('P'):
        strikePrice = strikePrice[:-1]
        optionType = "P"
    print(optionType)
    return optionType


#We will be converting date into dateTime object here later
def getDate(message):
    date = re.search("[0-9]+[/][0-9]+[0-9/]*", message)
    if date == None:
        return
    date = date.group()
    print("Date = " + date)
    return date


def getPrice(message):
    price = re.search("[@][ ]*[0-9.]+[0-9.]+", message)
    if price == None:
        return
    price = price.group()
    price = str.replace(price, '@', '')
    price = str.replace(price, ' ', '')
    print("price = " + price)
    return price


def getNotes(message):
    noteStart = re.search("\(", message)
    if noteStart == None:
        return
    noteStart = noteStart.span()[0]
    notes = message[noteStart:]
    
    
    return notes


      
################################
######## trade details #########
################################
switcher = {
      "scale" : 0.50,
      "scrape" : 0.25,
      "scalp" : 0.50,
      "more" : 0.50,
      "some more" : 0.50,
      "runner" : 0.50,
      "risky scalp" : 0.50,
      "half" : 0.50 #Sold half, hold a few runners if you want
   }


def getPercentage(key):
    print('percent:',switcher[key])
    return switcher[key]


def checkNotes(notes):
    #if notes contain any phrase in switcher, return it.
    for i in switcher:
        temp = re.search(i, notes)
        print(temp)
        if temp != None:
            print(temp)
            #if temp.group().lower == i:
            print("Found ",temp.group())
            return getPercentage(temp.group())
    #otherwise, return 1.0
    return 1.0
