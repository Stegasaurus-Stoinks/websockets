from algo import Algo
from ticker import Ticker
from database import Database

#------Config Variables------
Live_Trading = True
#----------------------------
DB = Database()

#test database query
#print(DB.QueryLast("AAPL",number = 10))
#test database notify
#DB.awaitNewData()

AAPL = Ticker("AAPL", "Stock")
AAPLalgo1 = Algo(AAPL, "ThreeKings", 9, live = True)
print(AAPLalgo1.getStatus())
print(AAPL.getStatus())
AAPL.warmUp()
print(AAPLalgo1.getStatus())
print(AAPL.getStatus())

#AAPLalgo2 = Algo(AAPL, "MomentumEMA", 2, live = True)

#AAPL.update()
#AAPLalgo1.update()
#AAPLalgo2.update()