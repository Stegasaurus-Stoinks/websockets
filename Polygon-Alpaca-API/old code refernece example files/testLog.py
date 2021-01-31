import psycopg2
import psycopg2.extensions
from datetime import datetime, timedelta
import config

#########################For testing trades table###########################################################



myTime = datetime.now()
myTime2 = datetime(2020, 11, 18, 18, 11, 0)

def formatTime(timey):
    year = timey.year
    month = timey.month
    day = timey.day
    hour = timey.hour
    minute = timey.minute
    second = timey.second

    temp = "{}-{}-{} {}:{}:{}".format(year, month , day, hour, minute, second)
    return temp

entrytime = formatTime(myTime)
exittime = formatTime(myTime2)
algo = "tester"
entryprice = 54.2
exitprice = 12.4
symbol = "blah"
tradetype = "testy"
volume = 1234
id = 1234


CONNECTION = "postgres://{}:{}@{}:{}/{}".format(config.TSDB_USERNAME, config.TSDB_AWS_PASSWORD, config.TSDB_AWS_HOST, config.TSDB_PORT, config.TSDB_DATABASE)
conn = psycopg2.connect(CONNECTION)
cur = conn.cursor()




def log_order():
    data_send = """
    INSERT INTO trades(entrytime, exittime, algo, entryprice, exitprice, symbol, tradetype, volume, id) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    data = (entrytime, exittime, algo, entryprice, exitprice, symbol, tradetype, volume, id)
    try:
        cur.execute(data_send, data)
        print("order data logged")

    except (Exception, psycopg2.Error) as error:
            print(error.pgerror)
                
    conn.commit() 






log_order()