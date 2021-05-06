import discord

client = discord.Client()

TOKEN_AUTH = 'MjMxNTAzMTc1MzgxODExMjAx.YEPafA.Ud2X2EDKYZexrkE54xJKk8sMOMs'

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    #if message.author == client.user:
    #    return
    print(message)

    print(message.content)
    print(message.attachments)
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(TOKEN_AUTH, bot=False)