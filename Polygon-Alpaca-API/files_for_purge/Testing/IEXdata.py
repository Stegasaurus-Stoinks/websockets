import pyEX as p
import mplfinance as mpl
import requests
import pandas as pd
from sseclient import SSEClient

TOKEN = "pk_536cdf66059a4846a9ce981fb1f19b38"
SECRET_TOKEN = "sk_c0b9ebde0d734c61b35515fe66e6b5c1"

base_url = 'https://cloud.iexapis.com/v1'
sandbox_url = 'https://sandbox.iexapis.com/stable'

#curl --header 'Accept: text/event-stream' 

url = 'https://cloud-sse.iexapis.com/stable/stocksUSNoUTP1Minute?symbols=aapl&token=sk_c0b9ebde0d734c61b35515fe66e6b5c1'
url2 = 'https://cloud-sse.iexapis.com/stable/cryptoQuotes/?symbols/=btcusdt/&token=sk_c0b9ebde0d734c61b35515fe66e6b5c1'
url3 = 'https://cloud-sse.iexapis.com/stable/cryptoQuotes?symbols/=btcusdt/&token=sk_c0b9ebde0d734c61b35515fe66e6b5c1'
url4 = base_url + '/crypto/btcusdt/quote/?token=sk_c0b9ebde0d734c61b35515fe66e6b5c1'
url5 = 'https://cloud-sse.iexapis.com/stable/forex1Minute?symbols=USDCAD&token=sk_c0b9ebde0d734c61b35515fe66e6b5c1'
url6 = 'https://cloud-sse.iexapis.com/stable/cryptoquotes?token=sk_c0b9ebde0d734c61b35515fe66e6b5c1&symbols=btcusdt'

messages = SSEClient(url)
for msg in messages:
    print(msg)
#while(1):
    #r = requests.get(url5, headers={"Accept":"text/event-stream"})
    #print(r.status_code)
    #print(r.headers)
    #print(r._content)
    #print(r.json())
    #quit()

#resp = requests.get(base_url+'/stock/AAPL/chart'+'?token='+TOKEN)

#resp.raise_for_status()

#df=pd.DataFrame(resp.json())
#print(df)

#mpl.plot(data)

