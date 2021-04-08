import discord
import asyncio
import config
import re
from datetime import datetime
import pandas as pd
import os

nameList = ['testy', 'test', 'anotha test']
pandy = pd.DataFrame(columns=['name', 'tradeType', 'ticker', 'strikePrice', 'optionType', 'date', 'price', 'timePlaced'])
cur_positions = pd.DataFrame(columns=['name', 'tradeType', 'ticker', 'strikePrice', 'optionType', 'date', 'price', 'timePlaced'])


#Primary parsey thing
async def parseAndStuff(author, message):
    global pandy

    #Get name variable
    tempName = re.search("[#][0-9]+", author)
    name = author.rstrip(tempName.group())
    print(name)
    #split string into array
    splitString = re.split("\s", message, 2)
    
    tradeType = splitString[0]
    ticker = splitString[1]
    otherStuff = splitString[2]

    #get strike price
    strikePrice = re.search("[$]*[0-9.]+[cCpP]", otherStuff)
    if strikePrice == None:
        return
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
    if date == None:
        return
    date = date.group()
    print("Date = " + date)

    #get price
    price = re.search("[@][ ]*[0-9.]+[0-9.]+", otherStuff)
    if price == None:
        return
    price = price.group()
    price = str.replace(price, '@', '')
    price = str.replace(price, ' ', '')
    print("price = " + price)


    now = datetime.now()

    tempList = {'name': name, 'tradeType': tradeType, 'ticker': ticker, 'strikePrice': strikePrice, 'optionType': optionType, 'date': date, 'price': price, 'timePlaced':now}

    print(tempList)
    pandy = pandy.append(tempList, ignore_index=True)

    #print(pandy.tail())
    print("\n")
    return tempList





#Buy or sell and stuff. Takes recent trade information and checks to see if we need to buy or sell, and adds it to recent positions if so
async def tradeAndStuff(trade):
    global cur_positions

    
    tradeType = trade.get('tradeType')
    tradeName = trade.get('name')
    tradeTicker = trade.get('ticker')
    
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
            cur_positions.drop(indx)
    elif tradeType.lower() == 'bto':
        #if tradeName in nameList:
        print('\nBought some '+ tradeTicker +' with '+ tradeName +'!\n')##########DO LE BUY HERE :D
        cur_positions.append(trade, ignore_index=True)
    print('saving current positions')
    cur_positions.to_csv('cur_positions.csv', index = False)




#Check if we need to load in data from previous days
fileExist = os.path.isfile('pandy.csv')
print('File exists: ', str(fileExist), '\n')
if fileExist:
    pandy = pd.read_csv('pandy.csv')

fileExist2 = os.path.isfile('cur_positions.csv')
print('File exists: ', str(fileExist2), '\n')
if fileExist2:
    cur_positions = pd.read_csv('cur_positions.csv')

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
            trade = await parseAndStuff(str(message.author), str(message.content))

            if trade != None:
                #if not cur_positions.empty:
                await tradeAndStuff(trade)
                
                
                print('DataFrame:\n', pandy.tail(),'\n\n\n')
                pandy.to_csv('pandy.csv', index = False)
            else:
                print('Bad message! Skipping')




client.run(config.TOKEN_AUTH, bot=False)




