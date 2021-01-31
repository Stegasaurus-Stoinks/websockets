class Algo:
    
    #unique id so find trades that have been placed by this algo
    self.tradeID

    def __init__(self, ticker, ):
        self.ticker = ticker
        self.type = type
        self.risklevel = risklevel    

    def update(self):
        #This function will be run once the database recieves a new data point
        print("Run Update Loop")

    def queryData(self):
        #pull data from the database

    def checkData(self):
        #check to make sure the new point is actually differnt from the last

    def updateArray(self):
        #add new point to 




p1 = Algo("John", 36)

print(p1.name)
print(p1.age) 