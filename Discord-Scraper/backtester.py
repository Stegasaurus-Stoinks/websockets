
import discord
import asyncio
#from Disco_Scraper import parseAndStuff
import pandas as pd

TOKEN_AUTH = "MTg5NjA0MTc4MTExMjM0MDUw.YEPoQQ.-kgEiLpyPGCzIeV58bxhPe_wQqo" # Retrieved from browser local storage
results = pd.DataFrame(columns=['name', 'tradeType', 'ticker', 'strikePrice', 'optionType', 'date', 'price', 'timePlaced', 'traded','notes'])


async def collectList(username):
    channel = client.get_channel(822972262008356964)
    messages = await channel.history(limit=5).flatten()
    print("test")
    messages.reverse()
    for i in messages:
        print(i.content)
    return messages

print("BLAHHHHH")

client = discord.Client()

@client.event
async def on_ready():
    print(await client.fetch_guild(723418405067161640))
    print(await collectList("bleh"))
    messages = await collectList("wildape")

    for m in messages:
        #parse
        #tradeData = await parseAndStuff(str(m.author), str(m.content))
        tradeData = "bleh"
        if tradeData != None:

            #compare against pd
            #results.loc[(results['column_name'] = A) & (results['column_name'] = B)]



            tempResults = pd.DataFrame(columns=['name', 'tradeType', 'ticker', 'strikePrice', 'optionType', 'date', 'price', 'timePlaced','traded','notes'])
            tempResults = tempResults.append(tradeData, ignore_index=True)
            concatFrame = [results, tempResults]
            resulty = pd.concat(concatFrame, sort=False)


            #print('DataFramen', resulty.tail(),'nnn')
            resulty.to_csv('trade_datapandy.csv', index = False)

client.run(TOKEN_AUTH, bot=False)
print(collectList("de"))