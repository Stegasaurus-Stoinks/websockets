#local imports 
import config
import disco_util as utily

import discord
import asyncio

import re
from datetime import datetime
import pandas as pd
import os

from ib_insync import *

nameList = ['testy', 'test', 'anotha test']
pandy = pd.DataFrame(columns=['name', 'tradeType', 'ticker', 'strikePrice', 'optionType', 'date', 'price', 'timePlaced', 'traded'])
cur_positions = pd.DataFrame(columns=['name', 'tradeType', 'ticker', 'strikePrice', 'optionType', 'date', 'price', 'timePlaced'])

try:
    ib = IB()
    ib.connect(host='127.0.0.1', port=7496, clientId=1)
    Trading = True
    
    try:
        mintickrule = ib.reqMarketRule(110)
        print(mintickrule)
        rulelowthresh = float(mintickrule[0][0])
        rulelowtick = float(mintickrule[0][1])
        rulehighthresh = float(mintickrule[1][0])
        rulehightick = float(mintickrule[1][1])
        
    
    except:
        rulelowthresh = float(0)
        rulelowtick = float(.05)
        rulehighthresh = float(3.00)
        rulehightick = float(0.1)


except:
    print("--------------------------------------------------------------------------------------------------------------------------------")
    print("Trading offline: There was a problem connecting to IB. Make sure Trader Workstation is open and try restarting the python script")
    print("--------------------------------------------------------------------------------------------------------------------------------")
    Trading = False

def orderfilled(trade, fill):
    print("order has been filled")
    print(trade)
    print(fill)

def closePosition(position, price = 0, percent=1.00):
    position.contract.exchange = 'SMART'
    numShares = round(percent * position.position)
    if numShares == 0:
        numShares = 1

    if price == 0:
        sellOrder = MarketOrder('SELL', numShares)

    else:
        sellOrder = LimitOrder('SELL', numShares, price)

    sell = ib.placeOrder(position.contract,sellOrder)
    print(sell)
    sell.fillEvent += orderfilled   

def openPosition(ticker, strike, date, direction, quantity, price = 0):
    #ticker: 'AAPL'
    #strike: int
    #date: '20210430' = 'YYYYMMDD'
    #direction: 'C' or 'P'
    #quantity: int
    #price: float

    call_option = Option(symbol = ticker,lastTradeDateOrContractMonth = date, strike=strike, right = direction, exchange='SMART', currency='USD')
    
    if price == 0:
        buyOrder = MarketOrder('BUY', quantity)

    else:
        buyOrder = LimitOrder('BUY', quantity, price)

    trade = ib.placeOrder(call_option,buyOrder)

    print(trade)

#Primary parsey thing
async def parseAndStuff(author, message):
    global pandy
    print(message)
    #split string into array
    splitString = re.split("\s", message, 2)
    if len(splitString) < 3:
        return
    tradeType = splitString[0]
    ticker = splitString[1]
    otherStuff = splitString[2]


    #Get name variable
    name = utily.getName(author)

    #get strike price
    strikePrice = utily.getStrikePrice(otherStuff)
    if strikePrice == None:
        return

    #get option type
    optionType = utily.getOptionType(strikePrice)

    #get date
    date = utily.getDate(otherStuff)
    if date == None:
        return

    #get price
    price = utily.getPrice(otherStuff)
    if price == None:
        return

    now = datetime.now()

    #get notes
    notes = utily.getNotes(otherStuff)
    print(notes)

    tempList = {'name': name, 'tradeType': tradeType, 'ticker': ticker, 'strikePrice': strikePrice, 'optionType': optionType, 'date': date, 'price': price, 'timePlaced':now}

    print(tempList)
    

    #print(pandy.tail())
    print("\n")
    return tempList





#Buy or sell and stuff. Takes recent trade information and checks to see if we need to buy or sell, and adds it to recent positions if so
async def tradeAndStuff(trade):
    global cur_positions
    traded = False

    
    tradeType = trade.get('tradeType')
    tradeName = trade.get('name')
    tradeTicker = trade.get('ticker')
    price = float(trade.get('price'))
    date = trade.get('date')
    dat = date.split('/')
    dateyear = '2021'
    datemonth = dat[0].zfill(2)
    dateday = dat[1].zfill(2)
    
    date = dateyear+datemonth+dateday

    direction = trade.get('optionType')
    strike = trade.get('strikePrice')
    strike = float(strike[:-1])

    indx = None
    #logic block for buy or sell
    if tradeType.lower() == 'stc':
        if cur_positions.empty:
            return traded
        #check if we already have a position from same author
        for i in range(len(cur_positions.name)):
            if cur_positions.name[i] == tradeName and cur_positions.ticker[i] == tradeTicker:
                #save index of name to call later
                indx = i
        #if we have a match, then sell and delete position from cur_positions. Could also hold record here for our buys ans sells.
        if indx != None:
            print('\nSold some '+ tradeTicker +' with '+ tradeName +'!\n')#########DO LE SELL HERE :D

            #this will place market sell for now
            if Trading:
                for position in ib.positions():
                    print(position.contract.symbol,tradeTicker,position.contract.strike,strike,position.contract.right,direction)
                    if position.contract.symbol == tradeTicker and position.contract.strike == strike and position.contract.right == direction:
                        closePosition(position)
                        print(position.contract.conId)

                cur_positions = cur_positions.drop(indx)
                traded = True

    elif tradeType.lower() == 'bto':
        #if tradeName in nameList:
        print('\nBought some '+ tradeTicker +' with '+ tradeName +'!\n')##########DO LE BUY HERE :D
        if Trading:
            #calculate quatity based on price
            quantity = round(50/price)
            if quantity == 0:
                quantity = 1

            #calculate price
            wiggle = 0.03 #percentage wiggle on entry price

            if price > rulehighthresh: #rounding price to correct multiple based on trading rules
                base = rulehightick
            else:
                base = rulelowtick

            price = price+(price*wiggle)
            price = base * round(price/base)


            #this will place market order for now
            openPosition(tradeTicker, strike, date, direction, quantity, price = price)

            cur_positions = cur_positions.append(trade, ignore_index=True)
            traded = True

    print('saving current positions')
    cur_positions.to_csv('trade_data/cur_positions.csv', index = False)
    return traded



#Check if we need to load in data from previous days
fileExist = os.path.isfile('trade_data/pandy.csv')
print('File exists: ', str(fileExist), '\n')
if fileExist:
    pandy = pd.read_csv('trade_data/pandy.csv')

fileExist2 = os.path.isfile('trade_data/cur_positions.csv')
print('File exists: ', str(fileExist2), '\n')
if fileExist2:
    cur_positions = pd.read_csv('trade_data/cur_positions.csv')

print('Current Positions:\n', cur_positions, '\n')





#Client code from here onward
client = discord.Client()
print('pandy contents:\n', pandy, '\n')
@client.event
async def on_ready():
    print(await client.fetch_guild(723418405067161640), '\n')


#Primary method that activates on recieving message. Uses methods above to execute scraper logic
@client.event
async def on_message(message):
    global pandy
    #print("message recieved", message)
    if message.guild != None:
        #print(message.guild.name,config.GUILD_NAME,message.channel.id,config.CHANNEL_ID,str(message.author),str(message.content))
        if (message.guild.name == config.GUILD_NAME and message.channel.id == config.CHANNEL_ID and str(message.author) != 'Xcapture#0190'):
            print("from: "+ str(message.author) + ",\n" + str(message.content))
            tradeData = await parseAndStuff(str(message.author), str(message.content))

            if tradeData != None:
                #if not cur_positions.empty:
                traded = await tradeAndStuff(tradeData)
                tradeData.update({'traded': traded});

                tempPandy = pd.DataFrame(columns=['name', 'tradeType', 'ticker', 'strikePrice', 'optionType', 'date', 'price', 'timePlaced','traded'])
                tempPandy = tempPandy.append(tradeData, ignore_index=True)
                concatFrame = [pandy, tempPandy]
                pandy = pd.concat(concatFrame, sort=False)


                print('DataFrame:\n', pandy.tail(),'\n\n\n')
                pandy.to_csv('trade_data/pandy.csv', index = False)

            else:
                print('Bad message! Skipping')



client.run(config.TOKEN_AUTH, bot=False)




