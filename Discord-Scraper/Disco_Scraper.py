#local imports
import config
import disco_util as util

import discord
import asyncio

import re
from datetime import datetime
import pandas as pd
import os

nameList = ['testy', 'test', 'anotha test']
pandy = pd.DataFrame(columns=['name', 'tradeType', 'ticker', 'strikePrice', 'optionType', 'date', 'price', 'timePlaced', 'traded'])
cur_positions = pd.DataFrame(columns=['name', 'tradeType', 'ticker', 'strikePrice', 'optionType', 'date', 'price', 'timePlaced'])


#Primary parsey thing
async def parseAndStuff(author, message):
    global pandy

    #split string into array
    splitString = re.split("\s", message, 2)
    if len(splitString) < 3:
        return
    tradeType = splitString[0]
    ticker = splitString[1]
    otherStuff = splitString[2]


    #Get name variable
    name = util.getName(author)

    #get strike price
    strikePrice = util.getStrikePrice(otherStuff)
    if strikePrice == None:
        return

    #get option type
    optionType = util.getOptionType(strikePrice)

    #get date
    date = util.getDate(otherStuff)
    if date == None:
        return

    #get price
    price = util.getPrice(otherStuff)
    if price == None:
        return

    now = datetime.now()

    tempList = {'name': name, 'tradeType': tradeType, 'ticker': ticker, 'strikePrice': strikePrice, 'optionType': optionType, 'date': date, 'price': price, 'timePlaced':now}

    print(tempList)
    tempPandy = pd.DataFrame(columns=['name', 'tradeType', 'ticker', 'strikePrice', 'optionType', 'date', 'price', 'timePlaced'])
    tempPandy = tempPandy.append(tempList, ignore_index=True)
    concatFrame = [pandy, tempPandy]
    pandy = pd.concat(concatFrame, sort=False)

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
    indx = None
    #logic block for buy or sell
    if tradeType.lower() == 'stc':
        if cur_positions.empty:
            return
        #check if we already have a position from same author
        for i in range(len(cur_positions.name)):
            if cur_positions.name[i] == tradeName and cur_positions.ticker[i] == tradeTicker:
                #save index of name to call later
                indx = i
        #if we have a match, then sell and delete position from cur_positions. Could also hold record here for our buys ans sells.
        if indx != None:
            print('\nSold some '+ tradeTicker +' with '+ tradeName +'!\n')#########DO LE SELL HERE :D
            cur_positions = cur_positions.drop(indx)
            traded = True

    elif tradeType.lower() == 'bto':
        #if tradeName in nameList:
        print('\nBought some '+ tradeTicker +' with '+ tradeName +'!\n')##########DO LE BUY HERE :D
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
    if message.guild != None:
        if message.guild.name == config.GUILD_NAME and message.channel.id == config.CHANNEL_ID and str(message.author) != 'Xcapture#0190':
            print("from: "+ str(message.author) + ",\n" + str(message.content))
            tradeData = await parseAndStuff(str(message.author), str(message.content))

            if tradeData != None:
                #if not cur_positions.empty:
                traded = await tradeAndStuff(tradeData)
                tradeData.update({'traded': traded});
                print('TESTING TO SEE IF TRADED WAS ADDED');

                tempPandy = pd.DataFrame(columns=['name', 'tradeType', 'ticker', 'strikePrice', 'optionType', 'date', 'price', 'timePlaced','traded'])
                tempPandy = tempPandy.append(tradeData, ignore_index=True)
                concatFrame = [pandy, tempPandy]
                pandy = pd.concat(concatFrame, sort=False)


                print('DataFrame:\n', pandy.tail(),'\n\n\n')
                pandy.to_csv('trade_data/pandy.csv', index = False)

            else:
                print('Bad message! Skipping')



client.run(config.TOKEN_AUTH, bot=False)




