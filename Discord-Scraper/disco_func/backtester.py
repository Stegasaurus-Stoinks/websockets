
import discord
from disco_util import parseAndStuff
import pandas as pd

TOKEN_AUTH = "MjMxNTAzMTc1MzgxODExMjAx.YEPafA.Ud2X2EDKYZexrkE54xJKk8sMOMs" # Retrieved from browser local storage
results = pd.DataFrame(columns=['name', 'tradeType', 'ticker', 'strikePrice', 'optionType', 'date', 'price', 'timePlaced', 'traded','notes'])


async def collectList(username):
    messageList = []
    channel = client.get_channel(821479719161561168)
    messages = await channel.history(limit=200).flatten()
    print("test")
    messages.reverse()
    for m in messages:
        if username in str(m.author):
            messageList.append(m)
            print(m.content)
        
    return messages

print("BLAHHHHH")

client = discord.Client()

@client.event
async def on_connect():
    #data variables:
    bto = 0
    stc = 0
    goodTrades = 0
    badTrades = 0
    totalTrades = 0
    percentMade = 0
    global results


    print("blehhhhh")
    print(await client.fetch_guild(723418405067161640))
    messages = await collectList("EvaPanda")

    for m in messages:
        #parse
        tradeData = await parseAndStuff(str(m.author), str(m.content))
        
        if tradeData != None:
            #variables
            tradeType = tradeData.get('tradeType').lower()
            ticker = tradeData.get('ticker')
            date = tradeData.get('date')
            strikePrice = tradeData.get('strikePrice')
            price = tradeData.get('price')
            



            #collect data
            if tradeType == "bto":
                bto += 1
            #compare against pd
            if tradeType == "stc":
                stc += 1
                temp = results.loc[(results['strikePrice'] == strikePrice) & (results['ticker'] == ticker) & (results['date'] == date)]
                if not temp.empty:
                    tempPrice = float(temp['price'].iloc[0])
                    tradeType = temp['tradeType'].iloc[0].lower()
                    if tradeType == "bto":
                        totalTrades += 1
                        print(temp)
                        percent = (float(price)/float(tempPrice)) - 1
                        if percent < 0:
                            badTrades += 1
                        else:
                            goodTrades += 1
                        


            tempResults = pd.DataFrame(columns=['name', 'tradeType', 'ticker', 'strikePrice', 'optionType', 'date', 'price', 'timePlaced','traded','notes'])
            tempResults = tempResults.append(tradeData, ignore_index=True)
            concatFrame = [results, tempResults]
            results = pd.concat(concatFrame, sort=False)


            #print('DataFramen', resulty.tail(),'nnn')
            results.to_csv('trade_data/results.csv', index = False)
    print("Buys: ",bto)
    print("Sells: ",stc)
    print("Good trades: ",goodTrades)
    print("Bad trades: ",badTrades)
    print("total trades: ",totalTrades)


client.run(TOKEN_AUTH, bot=False)