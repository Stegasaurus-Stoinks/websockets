import psycopg2
import psycopg2.extensions
import select

import config

class Database:

    def __init__(self, BackTest, notify_channel = "amdata"):
        self.notify_channel = notify_channel
        CONNECTION = "postgres://{}:{}@{}:{}/{}".format(config.TSDB_USERNAME, config.TSDB_AWS_PASSWORD, config.TSDB_AWS_HOST, config.TSDB_PORT, config.TSDB_DATABASE)
        self.conn = psycopg2.connect(CONNECTION)
        self.cur = self.conn.cursor()
        self.BackTest = BackTest

        self.setupNotify()

        

    def setupNotify(self):
        self.cur.execute("LISTEN " + self.notify_channel)
        #cur.execute("NOTIFY testyy, 'this connection works';")
        self.conn.commit()



    def sendQuery(self, query, data):
        self.cur.execute(query, data)
        results = self.cur.fetchall()
        self.conn.commit()
        return results



    def awaitNewData(self):

        self.NewData = False

        #loop here until conn.poll() recieves a non empty message
        while (self.NewData == False):
            #print("NewData is", self.NewData)
            if self.BackTest:
                self.NewData = True
                return()

            if select.select([self.conn],[],[],40) == ([],[],[]):
                print("Waiting for notifications on channel " + self.notify_channel)
            else:
                self.conn.poll()
                while self.conn.notifies:
                    self.notify = self.conn.notifies.pop(0)
                    print("Got NOTIFY, New Data Recieved!")
                    #print(notify.pid, notify.channel, notify.payload)
                    self.NewData = True



    def QueryLast(self, ticker, number = 1):
        query = """
        SELECT *
        FROM stockamdata
        WHERE symbol = %s
        ORDER BY time
        DESC LIMIT %s;
        """
        data = (ticker, number)
        
        results = self.sendQuery(query, data)
        return results

    def QuerySpecificData(self, ticker, Current_time, number = 1):
        query = """
        SELECT *
        FROM stockamdata
        WHERE symbol = %s
        AND time = %s
        ORDER BY time
        DESC LIMIT %s;
        """
        data = (ticker, Current_time, number)
        
        results = self.sendQuery(query, data)
        return results