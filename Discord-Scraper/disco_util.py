import re
from typing import Literal


"""
getters for every piece of data we need from message
"""

Animal = Literal['ant', 'bee', 'cat', 'dog']


def getName(author):
    #Get name variable
    tempName = re.search("[#][0-9]+", author)
    name = author.rstrip(tempName.group())
    #print(name)
    return name


def getStrikePrice(message):
    strikePrice = re.search("[$]*[0-9.]+[cCpP]", message)
    if strikePrice == None:
        return
    strikePrice = strikePrice.group()
    strikePrice = str.replace(strikePrice, '@', '')
    #print("Strike Price = " + strikePrice)

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
    #print(optionType)
    return optionType


#We will be converting date into dateTime object here later
def getDate(message):
    date = re.search("[0-9]+[/][0-9]+[0-9/]*", message)
    if date == None:
        return
    date = date.group()
    #print("Date = " + date)
    return date


def getPrice(message):
    price = re.search("[@][ ]*[0-9.]+[0-9.]+", message)
    if price == None:
        return
    price = price.group()
    price = str.replace(price, '@', '')
    price = str.replace(price, ' ', '')
    #print("price = " + price)
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
#checks in order of priority
switcher = {
    

    "all" : 1.0,
    "out on runners" : 1.0,
    "baby profits" : 0.0,
    "holding 1/3" : 0.66,
    "holding 2/3" : 0.33,
    "trim some" : 0.20,
    "trim half" : 0.49,
    "trim" : 0.49,
    "out most" : 0.80,
    "leave runners" : 0.80,
    
    "lotto" : 0.0,
    
    # "scale" : 0.50,
    # "scrape" : 0.25,
    # "scalp" : 0.50,
    # "more" : 0.50,
    # "some more" : 0.50,
    # "runner" : 0.80,
    # "risky scalp" : 0.50,
    # "half" : 0.50, #Sold half, hold a few runners if you want
    # "2 runners" : 0.50,
    # "First exit" : 0.50,
    


    #"10%" : 0.10,
    #"20%" : 0.20,
    #"30%" : 0.30,
    #"40%" : 0.40,
    #"50%" : 0.50,
    #"60%" : 0.60,
    #"70%" : 0.70,
   }


def getPercentage(key):
    print('percent:',switcher[key])
    return switcher[key]


def checkNotes(notes):
    perc = 1.0
    
    #if notes exist
    if notes != None:
        #if notes contain any phrase in switcher, set percentage.
        for i in switcher:
            temp = re.search(i, notes, re.IGNORECASE)
            if temp != None:
                #if temp.group().lower == i:
                catch = temp.group().lower()
                print("Found ",catch)
                perc = getPercentage(catch)
                return perc 
    #otherwise, return 1.0
    return perc



########################################
######## PRIMARY FUNCTIONALITY #########
########################################