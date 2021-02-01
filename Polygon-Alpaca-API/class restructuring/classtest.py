from algo import Algo
from ticker import Ticker

AAPL = Ticker("AAPL", "Stock")
AAPL.warmUp()

AAPLalgo1 = Algo(AAPL, "ThreeKings", 9, live = True)
AAPLalgo2 = Algo(AAPL, "MomentumEMA", 2, live = True)

AAPL.update()
AAPLalgo1.update()
AAPLalgo2.update()
