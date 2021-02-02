#file to simplify the alpaca api into universal funtions inorder to create seperation and modularity
import alpaca_trade_api as tradeapi
import keystore

BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
ORDERS_URL = "{}/v2/orders".format(BASE_URL)
POSITIONS_URL = "{}/v2/positions".format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID': keystore.PAPER_API_KEY, 'APCA-API-SECRET-KEY': keystore.PAPER_SECRET_KEY}

class TradeApi:

    def __init__(self):
        self.api = tradeapi.REST(keystore.PAPER_API_KEY, keystore.PAPER_SECRET_KEY, base_url='https://paper-api.alpaca.markets') # or use ENV Vars shown below


    def SimpleBuy(self, ticker, volume):
        #place a simple market order with buy price
        print("BUY!")

    def SimpleSell(self, ticker, volume):
        #place a simple market order with sell price
        print("SELL!")

    def LiquidateAll(self):
        #clear out all positions
        print("LIQUIDATE!")