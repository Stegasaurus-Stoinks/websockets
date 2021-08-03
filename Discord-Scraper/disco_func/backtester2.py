import discord
from disco_util import parseAndStuff
import pandas as pd
import config

TOKEN_AUTH = "MjMxNTAzMTc1MzgxODExMjAx.YEPafA.Ud2X2EDKYZexrkE54xJKk8sMOMs" # Retrieved from browser local storage
results = pd.DataFrame(columns=['name', 'tradeType', 'ticker', 'strikePrice', 'optionType', 'date', 'price', 'timePlaced', 'traded','notes'])


async def collectList(username):
    messageList = []
    channel = client.get_channel(config.TEST_CHANNEL)
    messages = await channel.history(limit=500, after=config.CHANNEL_HISTORY).flatten()
    print("test")
    messages.reverse()
    for m in messages:
        if username in str(m.author):
            messageList.append(m)
            print(m.content)
        
    print(len(messages))
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
    incompleteTrades = 0
    percentMade = 0
    global results


    print("blehhhhh")
    print(await client.fetch_guild(723418405067161640))
    messages = await collectList(config.TEST_USERNAME)

    for m in messages:
        #parse
        tradeData = await parseAndStuff(str(m.author), str(m.content))
        
        if tradeData != None:        
            #add to pd
            tempResults = pd.DataFrame(columns=['name', 'tradeType', 'ticker', 'strikePrice', 'optionType', 'date', 'price', 'timePlaced','traded','notes'])
            tempResults = tempResults.append(tradeData, ignore_index=True)
            concatFrame = [results, tempResults]
            results = pd.concat(concatFrame, sort=False)

    #collect data
    for i in range(len(results)):
        entry = results.iloc[i]
        
        
        #variables
        tradeType = entry.get('tradeType').lower()
        ticker = entry.get('ticker')
        date = entry.get('date')
        strikePrice = entry.get('strikePrice')
        price = float(entry.get('price'))

        if tradeType == "bto":
            totalTrades += 1
            sellNum = 0
            bto += 1
            sellTrades = results.loc[(results['strikePrice'] == strikePrice) & (results['ticker'] == ticker) & (results['date'] == date) & ((results['tradeType'] == "STC"))]
            print(sellTrades)
            if not sellTrades.empty:
                #add sells together
                for i in range(len(sellTrades)):
                    sellNum += float(sellTrades['price'].iloc[i])
                #get average
                sellNum = sellNum/len(sellTrades)
                
                percent = (((sellNum/price)-1)*100)
                if percent <= 0:
                    badTrades += 1
                else:
                    goodTrades += 1 
                percentMade += percent
                print('price: ',price)
                print('sellNum: ',sellNum)
                print('curTradePercent',round(percent,2),"%")
                print('percentMade: ',round(percentMade,2),'%\n\n')
            else:
                incompleteTrades += 1
                print("\nINCOMPLETE TRADE\n",entry,"\n\n")
        #compare against pd
        if tradeType == "stc":
            stc += 1
        
        
    results.to_csv('trade_data/results.csv', index = False)
    print("Buys: ",bto)
    print("Sells: ",stc)
    print("Good trades: ",goodTrades)
    print("Bad trades: ",badTrades)
    print("total trades: ",totalTrades)
    print("incomplete trades: ",incompleteTrades)
    print("percent made: ",round(percentMade,2),"%")


client.run(TOKEN_AUTH, bot=False)