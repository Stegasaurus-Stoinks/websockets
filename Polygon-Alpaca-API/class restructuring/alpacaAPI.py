#file to simplify the alpaca api into universal funtions inorder to create seperation and modularity

BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
ORDERS_URL = "{}/v2/orders".format(BASE_URL)
POSITIONS_URL = "{}/v2/positions/{}".format(BASE_URL, ticker)
HEADERS = {'APCA-API-KEY-ID': keystore.PAPER_API_KEY, 'APCA-API-SECRET-KEY': keystore.PAPER_SECRET_KEY}

api = tradeapi.REST(keystore.PAPER_API_KEY, keystore.PAPER_SECRET_KEY, base_url='https://paper-api.alpaca.markets') # or use ENV Vars shown below

def SimpleBuy():
    #place a simple market order with buy price
    print("BUY!")

def SimpleSell():
    #place a simple market order with sell price
    print("SELL!")

def LiquidateAll():
    #clear out all positions
    print("LIQUIDATE!")