import discord
import asyncio

TOKEN_AUTH = "MTg5NjA0MTc4MTExMjM0MDUw.YEPoQQ.-kgEiLpyPGCzIeV58bxhPe_wQqo" # Retrieved from browser local storage

client = discord.Client()

@client.event
async def on_ready():
    print(await client.fetch_guild(723418405067161640))

@client.event
async def on_message(message):
    if message.guild != None:
        if message.guild.name == "Wall Street War - VIP":
            print("Channel: ", message.channel.name, "\n")
            print("from: "+ str(message.author) + ",\n" + str(message))
            print("\nmessage contents: ",str(message.content))
client.run(TOKEN_AUTH, bot=False)