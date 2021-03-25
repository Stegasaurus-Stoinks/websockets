import discord
import asyncio
import config
import re
from datetime import datetime
import pandas as pd


pandy = pd.DataFrame(columns=['tradeType', 'ticker', 'strikePrice', 'optionType', 'date', 'price', 'timePlaced'])

async def parseAndStuff(author, message):

    global pandy

    #Getting name variable
    tempName = re.search("[#][0-9]+", author)
    name = author.rstrip(tempName.group())


    splitString = re.split("\s", message, 2)
    #print(splitString)

    tradeType = splitString[0]
    ticker = splitString[1]
    otherStuff = splitString[2]

    strikePrice = re.search("[$]*[0-9.]*[cCpP]", otherStuff)
    strikePrice = strikePrice.group()
    print("Strike Price = " + strikePrice)


    if strikePrice.startswith('$'):
        strikePrice = strikePrice[1:]

    if strikePrice.endswith('c') or strikePrice.endswith('C'):
        strikePrice = strikePrice[:-1]
        optionType = "C"
    elif strikePrice.endswith('p') or strikePrice.endswith('P'):
        strikePrice = strikePrice[:-1]
        optionType = "P"
    print(optionType)





    date = re.search("[0-9]+[/][0-9]+[0-9/]*", otherStuff)
    date = date.group()
    print("Date = " + date)

    price = re.search("[@][ ]*[0-9.]+[0-9.]+", otherStuff)
    price = price.group()
    print("price = " + price)

    now = datetime.now()

    tempList = {'tradeType': tradeType, 'ticker': ticker, 'strikePrice': strikePrice, 'optionType': optionType, 'date': date, 'price': price, 'timePlaced':now}

    print(tempList)
    pandy = pandy.append(tempList, ignore_index=True)

    
    print(pandy.tail())
    print("\n")






client = discord.Client()

@client.event
async def on_ready():
    print(await client.fetch_guild(723418405067161640))

@client.event
async def on_message(message):
    if message.guild != None:
        if message.guild.name == config.GUILD_NAME and message.channel.id == config.CHANNEL_ID:
            print("from: "+ str(message.author) + ",\n" + str(message.content))
            await parseAndStuff(str(message.author), str(message.content))

client.run(config.TOKEN_AUTH, bot=False)




