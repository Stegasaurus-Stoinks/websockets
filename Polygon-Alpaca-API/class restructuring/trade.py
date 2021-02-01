import alpacaAPI
class Trade:
    
    #unique id so find trades that have been placed by this algo

    def __init__(self, ID, openPrice, openTime):
        self.ID = ID
        self.openPrice = openPrice
        self.openTime = openTime
        self.openPostion()
        
    def openPostion(self):
        #call funtion to open order through api
        alpacaAPI.SimpleBuy()
        self.status = "Open"

    def closePostion(self, closePrice, closeTime):
        self.closePrice = closePrice
        self.closeTime = closeTime

        #call funtion to close order through api
        alpacaAPI.SimpleSell()
        self.status = "Closed"

    def getStatus(self):
        return(self.status)