import re


"""
This section will be the getters for every piece of data we need from the message
"""
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
    noteStart = noteStart.span()[0]
    notes = message[noteStart:]
    if notes == None:
        return
    
    return notes