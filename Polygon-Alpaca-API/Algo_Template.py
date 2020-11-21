import select, time
import psycopg2
import psycopg2.extensions
import config
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

#------Config Variables------
Live_Trading = True
notify_channel = "testyy"
ticker = "SPY"
#----------------------------

NewData = False
AM_candlesticks = []
Current_time = datetime(2020, 11, 18, 18, 11, 0)
Next_time = datetime(2020, 11, 18, 18, 11, 0)
End_time = datetime(2020, 11, 18, 18, 30, 0)

CONNECTION = "postgres://{}:{}@{}:{}/{}".format(config.TSDB_USERNAME, config.TSDB_AWS_PASSWORD, config.TSDB_AWS_HOST, config.TSDB_PORT, config.TSDB_DATABASE)
conn = psycopg2.connect(CONNECTION)
cur = conn.cursor()
cur.execute("LISTEN " + notify_channel)
#cur.execute("NOTIFY testyy, 'this connection works';")
conn.commit()


def AwaitNewData():
    global NewData
    if Live_Trading:
        while not NewData:
            #print("NewData is", NewData)
            if select.select([conn],[],[],10) == ([],[],[]):
                print("Waiting for notifications on channel " + notify_channel)
            else:
                conn.poll()
                while conn.notifies:
                    notify = conn.notifies.pop(0)
                    #print("Got NOTIFY, New Data Recieved!")
                    #print(notify.pid, notify.channel, notify.payload)
                    NewData = True

def QueryData(ticker):
    global Current_time

    if Live_Trading:
        data = QueryLast(ticker)
        if Current_time != data[0]:
            print("This is a new data point")
            print("{} opened @ {} at time {}".format(data[1],data[6],data[0]))
            Current_time = data[0]
            return(data)
        else:
            print("ERROR! This is the same time data as the last point, possible data collection error!")    


    else:
        #for backtesting
        print("pull backtesting data using specific time stamp")

def QueryLast(ticker):
    query = """
    SELECT *
    FROM stockamdata
    WHERE symbol = %s
    AND time = %s
    ORDER BY time
    DESC LIMIT %s;
    """
    data = (ticker, Next_time, 1)
    cur.execute(query, data)
    results = cur.fetchall()[0]
    conn.commit()
    return results

def UpdateDataArray(data):
    global AM_candlesticks
    if data != None:
        change = 0.00
        change = float(data[8])-float(data[6])
        print(change)
        AM_candlesticks.append({
                "dtime": data[0],
                "open": data[6],
                "high": data[7],
                "low": data[9],
                "close": data[8],
                "volume": data[2],
                "change": change
            })
        #print(len(AM_candlesticks))
        if len(AM_candlesticks) > 20:
            AM_candlesticks.pop(0)
            #print(len(AM_candlesticks))

def main():
    global NewData
    while True:
        AwaitNewData() 
        #Breaks out to the code below if a notify is recieved on the above defined "notify_channel"
        #------------Add code Below Here-------------

        print("Notify Recieved")
        UpdateDataArray(QueryData(ticker))   

        #------------Add code Above Here-------------
        #Reset the notification loop
        NewData=False

main()