from sseclient import SSEClient

message = SSEClient('https://cloud-sse.iexapis.com/stable/stocksUSNoUTP1Second?token=pk_536cdf66059a4846a9ce981fb1f19b38&symbols=spy')

for msg in message:
    outputMsg = msg.data
    outputJS = json.loads(outputMsg)
    #print( FilterName, outputJS[FilterName] )
    print(outputJS)
    for line in outputJS:
        print("Calculation Price: " + str(line['calculationPrice']) + " Close: " + str(line['close']))
        print("Last Trade Time " + str(line['lastTradeTime']) + " Latest Price: " + str(line['latestPrice']))