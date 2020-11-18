from polygon import RESTClient
import config

def main():
    key = config.API_KEY

    # RESTClient can be used as a context manager to facilitate closing the underlying http session
    # https://requests.readthedocs.io/en/master/user/advanced/#session-objects
    with RESTClient(key) as client:
        resp = client.stocks_equities_daily_open_close("AAPL", "2020-10-16")
        resp2 = client.stocks_equities_snapshot_single_ticker("AAPL")
        response = client.stocks_equities_snapshot_gainers_losers("losers")
        #respo = client.stocks_equities_snapshot_all_tickers()


        print(resp2.status+"\n")
        print(resp2.ticker.ticker)
        print(resp2.ticker.todays_chang_eperc)
        print(resp2.ticker.day.close_price)
        print(f"On: {resp.from_} Apple opened at {resp.open} and closed at {resp.close}")
        #print(respo.status)
        #print(respo.tickers)
        print("bleh")
        if response.status == "OK":
            if len(response.tickers) > 0:
                #print(response.tickers[0])
                for ticker in response.tickers:
                    print(f" {ticker['ticker']} dropped {ticker['todaysChange']}$ which was {ticker['todaysChangePerc']}% updated @ {ticker['updated']}")
        
        else:
            print("error with polygon api call")


if __name__ == '__main__':
    main()