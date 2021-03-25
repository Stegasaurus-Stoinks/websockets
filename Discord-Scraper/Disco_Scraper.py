import discord
import asyncio
import config
import re
from datetime import datetime
import pandas as pd

nameList = ['testy', 'test', 'anotha test']
pandy = pd.DataFrame(columns=['name' 'tradeType', 'ticker', 'strikePrice', 'optionType', 'date', 'price', 'timePlaced'])
cur_positions = pd.DataFrame(columns=['name' 'tradeType', 'ticker', 'strikePrice', 'optionType', 'date', 'price', 'timePlaced'])


#Primary parsey thing
async def parseAndStuff(author, message):
    global pandy

    #Get name variable
    tempName = re.search("[#][0-9]+", author)
    name = author.rstrip(tempName.group())

    #split string into array
    splitString = re.split("\s", message, 2)
    
    tradeType = splitString[0]
    ticker = splitString[1]
    otherStuff = splitString[2]

    #get strike price
    strikePrice = re.search("[$]*[0-9.]*[cCpP]", otherStuff)
    strikePrice = strikePrice.group()
    strikePrice = str.replace(strikePrice, '@', '')
    print("Strike Price = " + strikePrice)
    
    if strikePrice.startswith('$'):
        strikePrice = strikePrice[1:]

    #get option type
    if strikePrice.endswith('c') or strikePrice.endswith('C'):
        strikePrice = strikePrice[:-1]
        optionType = "C"
    elif strikePrice.endswith('p') or strikePrice.endswith('P'):
        strikePrice = strikePrice[:-1]
        optionType = "P"
    print(optionType)


    #get date
    date = re.search("[0-9]+[/][0-9]+[0-9/]*", otherStuff)
    date = date.group()
    print("Date = " + date)

    #get price
    price = re.search("[@][ ]*[0-9.]+[0-9.]+", otherStuff)
    price = price.group()
    price = str.replace(price, '@', '')
    price = str.replace(price, ' ', '')
    print("price = " + price)


    now = datetime.now()

    tempList = {'name': name, 'tradeType': tradeType, 'ticker': ticker, 'strikePrice': strikePrice, 'optionType': optionType, 'date': date, 'price': price, 'timePlaced':now}

    print(tempList)
    pandy = pandy.append(tempList, ignore_index=True)

    print(pandy.tail())
    print("\n")
    return tempList





#Buy or sell and stuff
async def tradeAndStuff(trade):
    global cur_positions
    tradeType = trade.get('tradeType')
    tradeName = trade.get('name')
    tradeTicker = trade.get('ticker')
    
    #code block for if trade is sell
    if tradeType == 'STC':
        #check if we already have a position from same author
        for i in range(len(cur_positions.name)):
            if cur_positions.name[i] == tradeName and cur_positions.ticker[i] == tradeTicker:
                #save index of name
                indx = i
        #if we have a match, then sell and delete position from cur_positions. Could also hold record here for our buys ans sells.
        if indx != None:
            print('Bought some '+ tradeTicker +' with '+ tradeName +'!')#########DO LE SELL HERE :D
            cur_positions.drop(indx)
    elif tradeType == 'BTO':
        if tradeName in nameList:
            print('Bought some '+ tradeTicker +' with '+ tradeName +'!')##########DO LE BUY HERE :D









client = discord.Client()

@client.event
async def on_ready():
    print(await client.fetch_guild(723418405067161640))

@client.event
async def on_message(message):
    if message.guild != None:
        if message.guild.name == config.GUILD_NAME and message.channel.id == config.CHANNEL_ID:
            print("from: "+ str(message.author) + ",\n" + str(message.content))
            trade =  await parseAndStuff(str(message.author), str(message.content))
            await tradeAndStuff(trade)




client.run(config.TOKEN_AUTH, bot=False)




