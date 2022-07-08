import pandas as pd

from finvizfinance.quote import finvizfinance
from finvizfinance.screener.overview import Overview



def scanner(num = 0, signal = '', filter = {'Exchange':'NASDAQ','Index':'S&P 500','Market Cap.':'+Large (over $10bln)','Average Volume':'Over 100K'}):
    foverview = Overview()
    foverview.set_filter(signal =signal, filters_dict=filter)
    df = foverview.ScreenerView()

    #print(df)
    try:
        if num == 0:
            return(df)

        else:
            return(df.head(num))

    except:
        print("No results or there was an Error")
    
    #stock = finvizfinance('tsla')
    #print(stock.TickerDescription())
    #print(stock.TickerFullInfo())
    #print(stock.TickerNews())

    #_____________Possible Filters_____________
    # 'Exchange', 'Index', 'Sector', 'Industry', 'Country', 
    # 'Market Cap.', 'P/E', 'Forward P/E', 'PEG', 'P/S', 'P/B', 
    # 'Price/Cash', 'Price/Free Cash Flow', 'EPS growththis year', 
    # 'EPS growthnext year', 'EPS growthpast 5 years', 'EPS growthnext 5 years', 
    # 'Sales growthpast 5 years', 'EPS growthqtr over qtr', 'Sales growthqtr over qtr', 
    # 'Dividend Yield', 'Return on Assets', 'Return on Equity', 'Return on Investment', 
    # 'Current Ratio', 'Quick Ratio', 'LT Debt/Equity', 'Debt/Equity', 'Gross Margin', 
    # 'Operating Margin', 'Net Profit Margin', 'Payout Ratio', 'InsiderOwnership', 
    # 'InsiderTransactions', 'InstitutionalOwnership', 'InstitutionalTransactions', 
    # 'Float Short', 'Analyst Recom.', 'Option/Short', 'Earnings Date', 'Performance', 
    # 'Performance 2', 'Volatility', 'RSI (14)', 'Gap', '20-Day Simple Moving Average', 
    # '50-Day Simple Moving Average', '200-Day Simple Moving Average', 'Change', 
    # 'Change from Open', '20-Day High/Low', '50-Day High/Low', '52-Week High/Low', 
    # 'Pattern', 'Candlestick', 'Beta', 'Average True Range', 'Average Volume', 
    # 'Relative Volume', 'Current Volume', 'Price', 'Target Price', 'IPO Date', 
    # 'Shares Outstanding', 'Float'

    #___________Possible signal_____________ 
    # 'Top Gainers', 'Top Losers', 'New High', 'New Low', 'Most Volatile', 
    # 'Most Active', 'Unusual Volume', 'Overbought', 'Oversold', 'Downgrades',
    # 'Upgrades', 'Earnings Before', 'Earnings After', 'Recent Insider Buying', 
    # 'Recent Insider Selling', 'Major News', 'Horizontal S/R', 'TL Resistance', 
    # 'TL Support', 'Wedge Up', 'Wedge Down', 'Triangle Ascending', 'Triangle Descending', 
    # 'Wedge', 'Channel Up', 'Channel Down', 'Channel', 'Double Top', 'Double Bottom', 
    # 'Multiple Top', 'Multiple Bottom', 'Head & Shoulders', 'Head & Shoulders Inverse'

    #https://finviz.com to find filters and stuff

#scan_results = scanner(num = 0, signal = 'Most Active', filter={'Exchange':'NASDAQ','Index':'S&P 500','Market Cap.':'+Large (over $10bln)','Average Volume':'Over 100K'})

#print(scan_results)