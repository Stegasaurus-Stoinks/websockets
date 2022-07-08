from sseclient import SSEClient

messages = SSEClient('https://cloud-sse.iexapis.com/stable/stocksUSNoUTP1Second?token=pk_536cdf66059a4846a9ce981fb1f19b38&symbols=spy')

for msg in messages:
    temp = msg.__str__()
    temp = str(temp)
    
    print(temp.replace(",\"", '\n\"'))
