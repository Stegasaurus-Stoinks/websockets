import smtplib
from ib_insync import *
import time
positionupdate=False

carriers = {
    'att':    '@mms.att.net',
    'tmobile':' @tmomail.net',
    'verizon':  '@vtext.com',
    'sprint':   '@page.nextel.com'
}

def send(message_text):

    fromaddr = 'pwilda100@gmail.com'
    toaddr = ['4804630030@tmomail.net']#,'4807346105@vtext.com']
    cc = ['test@gmail.com','wildakids@gmail.com']
    message_subject = 'TRADE UPDATE'

    message = ("From: %s \r\n" % fromaddr
    + "To: %s \r\n" % ",".join(toaddr)
    + "CC: %s\r\n" % ",".join(cc)
    + "Subject: %s\r\n" % message_subject
    + "\r\n" 
    + message_text)

    # Replace the number with your own, or consider using an argument\dict for multiple people.
	#to_number = '4804630030{}'.format(carriers['tmobile'])
    #to_number = 'wildakids@gmail.com'

    try:
        auth = ('pwilda100@gmail.com','legoswag1441')
        # Establish a secure session with gmail's outgoing SMTP server using your gmail account
        server = smtplib.SMTP( "smtp.gmail.com", 587 )
        server.starttls()
        #if things break uncomment line below to debug
        #server.set_debuglevel(1)
        server.login(auth[0], auth[1])
	    # Send text message through SMS gateway of destination number
        server.sendmail( auth[0], toaddr, message)
        server.quit()
        print("EMAIL SENT")

    except:
        print("Something went wrong...")



#send("we made billions")

open_order_cb = ''
order_status_cb = []
exec_details_cb = ""
position_cb = []


#events = ('connectedEvent', 'disconnectedEvent', 'updateEvent',
#'pendingTickersEvent', 'barUpdateEvent', 'newOrderEvent', 'orderModifyEvent',
#'cancelOrderEvent', 'openOrderEvent', 'orderStatusEvent', 'execDetailsEvent',
#'commissionReportEvent', 'updatePortfolioEvent', 'positionEvent',
#'accountValueEvent', 'accountSummaryEvent', 'pnlEvent', 'pnlSingleEvent',
#'scannerDataEvent', 'tickNewsEvent', 'newsBulletinEvent', 'errorEvent',
#'timeoutEvent')

def onUpdatepos(position_change):
    global positionupdate
    print("___________________UPDATED___________________")
    print(position_change)
    
    time.sleep(10)
    orders = ib.orders()
    print("ORDER 0")
    print(orders[0])
    for order in orders:
        print(order.action, order.filledQuantity)
        print(" ")

    

    #ib.sleep(1)
    #executions = ib.executions()
    #for execution in executions:
    #    print(execution)
    #    print(" ")
    #trades = ib.trades()
    #for trade in trades:
    #print(trades[0])
    

    message = "Position was changed: {} @ an Average Price of ${}".format(position_change.position, round(position_change.avgCost,2))
    print(message)
    #send(message)

def onUpdateport(portfolio):
    print("Portfolio update \n")

def onOrderUpdate(trade):
    print(trade)
    print("IS THIS WORKING????")

def connectConfirm():
    print("Connected!")

def reconnect():
    #this doesnt work for some dumb reason
    print("Reconnecting")
    while(not ib.isConnected()):
        ib.connect('127.0.0.1', 7496, clientId=1)
        time.sleep(10)
        print("retrying...")


ib = IB()

#ib.positionEvent += onUpdatepos
#ib.updatePortfolioEvent += onUpdateport
ib.orderStatusEvent += onOrderUpdate
ib.execDetailsEvent += onOrderUpdate
ib.newOrderEvent += onOrderUpdate
ib.positionEvent += onUpdateport
ib.connectedEvent += connectConfirm
ib.disconnectedEvent += reconnect


ib.connect('127.0.0.1', 7496, clientId=1)


openorders = ib.openOrders()
print(openorders)

nflx_contract = Stock('NFLX', 'SMART', 'USD')
nflx_order = MarketOrder('BUY', 200)
trade = ib.placeOrder(nflx_contract, nflx_order)

ib.run()



