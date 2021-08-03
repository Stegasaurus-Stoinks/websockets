import discord
from disco_util import parseAndStuff
import pandas as pd
import config

TOKEN_AUTH = "MjMxNTAzMTc1MzgxODExMjAx.YEPafA.Ud2X2EDKYZexrkE54xJKk8sMOMs" # Retrieved from browser local storage
results = pd.DataFrame(columns=['name', 'tradeType', 'ticker', 'strikePrice', 'optionType', 'date', 'price', 'timePlaced', 'traded','notes'])
messages = []

async def collectList(username):
    userMessages = []
    channel = client.get_channel(config.TEST_CHANNEL)
    messageList = await channel.history(limit=None, after=config.CHANNEL_HISTORY).flatten()
    for m in messageList:
        if username in str(m.author):
            userMessages.append(m)
            #print(m.content)
        
    print("total messages from",config.TEST_USERNAME,":",len(userMessages))
    return userMessages

def stringify(data):
    tradeType = data.get('tradeType')
    ticker = data.get('ticker')
    strikePrice = data.get('strikePrice')
    myString = (str(tradeType) + ' ' + str(ticker) + ' ' + str(strikePrice))
    return myString

def getNearMessages(data, messages):
    stringy = stringify(data)
    print(stringy)
    #search for message we want
    messageObject = [s for s in messages if stringy in s.content]
    print(messageObject)
    print(messageObject[0])
    #get index of message
    indexy = (messages.index(messageObject[0]))
    #print other messages
    for i in range(0,5):
        if indexy-i < 0:
            return
        print(i)
        print(messages[indexy-i].content)

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
            stringify(tradeData)
            tempResults = tempResults.append(tradeData, ignore_index=True)
            concatFrame = [results, tempResults]
            results = pd.concat(concatFrame, sort=False)

    #make tradeType lowercase
    results['tradeType'].str.lower()

    #collect data
    for i in range(len(results)):
        entry = results.iloc[i]
        
        
        #variables
        tradeType = entry.get('tradeType')
        ticker = entry.get('ticker')
        date = entry.get('date')
        strikePrice = entry.get('strikePrice')
        price = float(entry.get('price'))

        #if trade was a buy, check if it has any matching sells and fill in data accordingly
        if tradeType == "bto":
            totalTrades += 1
            sellNum = 0
            bto += 1
            sellTrades = results.loc[(results['strikePrice'] == strikePrice) & (results['ticker'] == ticker) & (results['date'] == date) & ((results['tradeType'] == "stc"))]
            
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

                if config.DETAILS:
                    print(sellTrades)
                    print('price: ',price)
                    print('sellNum: ',sellNum)
                    print('curTradePercent',round(percent,2),"%")
                    print('percentMade: ',round(percentMade,2),'%\n\n')
            #print incomplete trade stuff if it couldnt find any sells
            else:
                incompleteTrades += 1
                
                print("\nINCOMPLETE TRADE\n")
                # try:
                #     getNearMessages(entry,messages)
                # except:
                #     print("couldnt get nearby messages")
                # print('\n')


        #add sell count if it was a sell
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