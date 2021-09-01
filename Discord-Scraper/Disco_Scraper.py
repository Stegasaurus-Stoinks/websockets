#local imports 
import disco_func.config as config
import disco_func.disco_util as utily

#ibkr stuff
from IBKR.ibkrApi import ibkrApi as ibkr
from ib_insync import *

import PhoneMessage

import discord
import asyncio

import pandas as pd
import os
import math
#'Sweet_Louuu', 'Muse', 'Justinvred','ryan-7k','illproducer','slam','skepticule', 'Wags'

nameList = ['EvaPanda', 'Justinvred', 'wildape']
pandy = pd.DataFrame(columns=['name', 'tradeType', 'ticker', 'strikePrice', 'optionType', 'date', 'price', 'timePlaced', 'traded','notes'])
all_trades = pd.DataFrame(columns=['name', 'tradeType', 'ticker', 'strikePrice', 'optionType', 'date', 'price', 'timePlaced','notes'])

#phone message stuff (could be removed if i can figure out how to add more args to event)
def onOrderUpdate(trade):
    trade_data = all_trades.tail()
    PhoneMessage.manageOrderUpdate(trade, ib, trade_data)

try:
    ib = ibkr()
    ib.orderStatusEvent += onOrderUpdate
    ib.connect(host='127.0.0.1', port=7496, clientId=1)
    Trading = True
    
    try:
        mintickrule = ib.reqMarketRule(110)
        print(mintickrule)
        rulelowthresh = float(mintickrule[0][0])
        rulelowtick = float(mintickrule[0][1])
        rulehighthresh = float(mintickrule[1][0])
        rulehightick = float(mintickrule[1][1])
        
    
    except:
        rulelowthresh = float(0)
        rulelowtick = float(.05)
        rulehighthresh = float(3.00)
        rulehightick = float(0.1)

except:
    print("--------------------------------------------------------------------------------------------------------------------------------")
    print("Trading offline: There was a problem connecting to IB. Make sure Trader Workstation is open and try restarting the python script")
    print("--------------------------------------------------------------------------------------------------------------------------------")
    Trading = False





#Buy or sell and stuff. Takes recent trade information and checks to see if we need to buy or sell, and adds it to recent positions if so
async def tradeAndStuff(trade):
    global all_trades
    traded = False
    positions = ib.refresh()
    orders = ib.openOrders()

    tradeType = trade.get('tradeType').lower()
    tradeName = trade.get('name')
    tradeTicker = trade.get('ticker').upper()
    price = float(trade.get('price'))
    date = trade.get('date')
    dat = date.split('/')
    dateyear = '2021'
    datemonth = dat[0].zfill(2)
    dateday = dat[1].zfill(2)
    notes = trade.get('notes')
    
    date = dateyear+datemonth+dateday

    tradeRight = trade.get('optionType')
    strike = trade.get('strikePrice')
    strike = float(strike[:-1])

    indx = None
    #logic block for buy or sell
    if tradeType.lower() == 'stc':
        if not orders:
            pass
        else:
            for curTrade in ib.openTrades():
                    print(curTrade)
                    if curTrade.contract.symbol == tradeTicker and curTrade.contract.strike == strike and curTrade.contract.right == tradeRight:
                        orderid = str(curTrade.order.orderId)
                        print("checking if needs to be cancelled:",orderid)
                        if curTrade.orderStatus.remaining != 0: #check if the full order has been filled before trying to cancel
                            ib.cancelOrder(curTrade.order)   
                    


        if not positions:
            return traded

        #check if we have a matching position to sell
        success = False
        for i in positions:
            if i.contract.symbol == tradeTicker and i.contract.strike == strike and i.contract.right == tradeRight:
                success = True

        #if we have a match, then sell and delete position from all_trades. Could also hold record here for our buys ans sells.
        if success == True:

            sellPercent = utily.checkNotes(notes) #check notes for key words to decide exit percentage
            
            print('\nSold '+ str(sellPercent*100) +"% of "+ tradeTicker +' with '+ tradeName +'!\n')#########DO LE SELL HERE :D

            if Trading:
                for position in positions:
                    print(position.contract.symbol,tradeTicker,position.contract.strike,strike,position.contract.right,tradeRight)
                    #date of contract is ignored so that we dont trade agaisnt any other positions
                    if position.contract.symbol == tradeTicker and position.contract.strike == strike and position.contract.right == tradeRight:
                        ib.closePosition(position, percent=sellPercent)
                        print(position.contract.conId)
                        print(position.contract)


                print("-------------ORDERS------------")
                for curTrade in ib.openTrades():
                    print(curTrade)
                    if curTrade.contract.symbol == tradeTicker and curTrade.contract.strike == strike and curTrade.contract.right == tradeRight:
                        orderid = str(curTrade.order.orderId)
                        print("Order ID:",orderid)
                        if curTrade.orderStatus.remaining != 0: #check if the full order has been filled before trying to cancel
                            ib.cancelOrder(curTrade.order)   
            traded = True

            all_trades = all_trades.append(trade, ignore_index=True)
            print('saving current positions')
            all_trades.to_csv('trade_data/all_trades.csv', index = False)

    elif tradeType.lower() == 'bto':
        if tradeName in nameList:
            print('\nBought some '+ tradeTicker +' with '+ tradeName +'!\n')##########DO LE BUY HERE :D
            if Trading:

                #calculate risk based on price and keywords
                buyPercent = utily.checkNotes(notes)
                risk = buyPercent

                if risk == 0.0:
                    print("risky trade! Skipping.")
                    return

                if price <= 0.75:
                    risk = 0.75
                if price <= 0.50:
                    risk = 0.50

                
                #if notes != None:  ###############ADD KEYWORD RISK STUFF HERE

                #calculate quantity based on price
                quantity = math.floor(((config.ACCOUNT_SIZE*config.MAX_POSITION_SIZE)*risk)/(price*100))
                print(config.ACCOUNT_SIZE,config.MAX_POSITION_SIZE,risk,price,"quantity:",quantity)
                

                #calculate price
                wiggle = 0.03 #percentage wiggle on entry price

                if price > rulehighthresh: #rounding price to correct multiple based on trading rules
                    base = rulehightick
                else:
                    base = rulelowtick

                price = price+(price*wiggle)
                price = base * round(price/base)

                ib.openPosition(tradeTicker, strike, date, tradeRight, quantity, price = price)
                
            traded = True

            all_trades = all_trades.append(trade, ignore_index=True)
            print('saving current positions')
            all_trades.to_csv(allTradesFile, index = False)
    return traded








#Check if we need to load in data from previous days
file = os.path.dirname(__file__)
pandyFile = os.path.join(file,'trade_data/pandy.csv')
fileExist = os.path.isfile(pandyFile)
print('File exists: ', str(fileExist), '\n')
if fileExist:
    pandy = pd.read_csv(pandyFile)

allTradesFile = os.path.join(file,'trade_data/all_trades.csv')
fileExist2 = os.path.isfile(allTradesFile)
print('File exists: ', str(fileExist2), '\n')
if fileExist2:
    all_trades = pd.read_csv(allTradesFile)

print('Current Positions:\n', all_trades, '\n')


#Client code from here onward
client = discord.Client()
print('pandy contents:\n', pandy, '\n')
@client.event
async def on_ready():
    print(await client.fetch_guild(723418405067161640), '\n')


#Primary method that activates on recieving message. Uses methods above to execute scraper logic
@client.event
async def on_message(message):
    global pandy
    #print("message recieved :", message.content, message)
    if message.guild != None:
        #print(message.guild.name,config.GUILD_NAME,message.channel.id,config.CHANNEL_ID,str(message.author),str(message.content))
        if ((message.guild.name == config.GUILD_NAME and message.channel.id == config.CHANNEL_ID) or
         (message.guild.name == config.GUILD_NAME2 and message.channel.id == config.CHANNEL_ID2 and str(message.author) != 'Xcapture#0190')):
            #print("from: "+ str(message.author) + ",\n" + str(message.content))
            tradeData = await utily.parseAndStuff(str(message.author), str(message.content))

            if tradeData != None:
                if tradeData.get('name') in nameList:
                    #if not all_trades.empty:
                    print("from: "+ str(message.author) + ",\n" + str(message.content))
                    print(tradeData)
                    
                    traded = await tradeAndStuff(tradeData)
                    tradeData.update({'traded': traded});

                    tempPandy = pd.DataFrame(columns=['name', 'tradeType', 'ticker', 'strikePrice', 'optionType', 'date', 'price', 'timePlaced','traded','notes'])
                    tempPandy = tempPandy.append(tradeData, ignore_index=True)
                    concatFrame = [pandy, tempPandy]
                    pandy = pd.concat(concatFrame, sort=False)


                    print('DataFrame:\n', pandy.tail(),'\n\n\n')
                    pandy.to_csv(pandyFile, index = False)

            else:
                print('Bad message! Skipping')



client.run(config.TOKEN_AUTH, bot=False)




