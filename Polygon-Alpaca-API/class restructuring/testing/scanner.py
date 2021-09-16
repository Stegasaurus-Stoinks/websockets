import pandas as pd

from finvizfinance.quote import finvizfinance
from finvizfinance.screener.overview import Overview



def scanner(num = 0, filter = {'Exchange':'NASDAQ','Sector':'Technology','Market Cap.':'+Mid (over $2bln)','20-Day High/Low':'New Low'}):
    foverview = Overview()
    filters_dict = {'Exchange':'NASDAQ','Sector':'Technology','Market Cap.':'+Mid (over $2bln)','20-Day High/Low':'New Low'}
    foverview.set_filter(filters_dict=filters_dict)
    df = foverview.ScreenerView()

    if num == 0:
        return(df)

    else:
        return(df.head(num))
    
    #stock = finvizfinance('tsla')
    #print(stock.TickerDescription())
    #print(stock.TickerFullInfo())
    #print(stock.TickerNews())


    #'Exchange', 'Index', 'Sector', 'Industry', 'Country', 
    #'Market Cap.', 'P/E', 'Forward P/E', 'PEG', 'P/S', 'P/B', 
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

    #https://finviz.com to find filters and stuff

print(scanner(10))
