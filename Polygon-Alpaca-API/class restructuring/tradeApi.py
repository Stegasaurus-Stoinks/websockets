#file to simplify the alpaca api into universal funtions inorder to create seperation and modularity
import alpaca_trade_api as tradeapi
import keystore
import json, requests

BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
ORDERS_URL = "{}/v2/orders".format(BASE_URL)
POSITIONS_URL = "{}/v2/positions".format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID': keystore.PAPER_API_KEY, 'APCA-API-SECRET-KEY': keystore.PAPER_SECRET_KEY}

class TradeApi:

    def __init__(self, Trading, LiveTrading):

        self.Trading = Trading

        if not LiveTrading:
            self.api = tradeapi.REST(keystore.PAPER_API_KEY, keystore.PAPER_SECRET_KEY, base_url='https://paper-api.alpaca.markets') # or use ENV Vars shown below


    def SimpleBuy(self, ticker, volume):
        if not self.Trading:
            print("SimpleBuy would have been executed, but you are not actually trading")
            return

        #place a simple market order with buy price
        data = {
            "symbol": ticker,
            "qty": volume,
            "side": "buy",
            "type": "market",
            "time_in_force": "gtc",
            "order_class": "simple",
        }

        r = requests.post(ORDERS_URL, json=data, headers=HEADERS)

        response = json.loads(r.content)

        print(response)
        print("PLACED BUY ORDER!")



    def SimpleSell(self, ticker, volume):
        """Place a simple market order with sell price"""
        data = {
            "symbol": ticker,
            "qty": volume,
            "side": "sell",
            "type": "market",
            "time_in_force": "gtc",
            "order_class": "simple",
        }

        r = requests.post(ORDERS_URL, json=data, headers=HEADERS)

        response = json.loads(r.content)

        print(response)
        print("PLACED SELL ORDER!")



    def BracketOrder(self, ticker, profit_price, loss_price, volume):

        data = {
            "symbol": ticker,
            "qty": volume,
            "side": "buy",
            "type": "market",
            "time_in_force": "gtc",
            "order_class": "bracket",
            "take_profit": {
                "limit_price": profit_price
            },
            "stop_loss": {
                "stop_price": loss_price
            }
        }

        r = requests.post(ORDERS_URL, json=data, headers=HEADERS)

        response = json.loads(r.content)

        print(response)



    def LiquidateAll(self):
        #clear out all positions
        print("LIQUIDATE!")