import select
import psycopg2
import psycopg2.extensions
import config

CONNECTION = "postgres://{}:{}@{}:{}/{}".format(config.TSDB_USERNAME, config.TSDB_AWS_PASSWORD, config.TSDB_AWS_HOST, config.TSDB_PORT, config.TSDB_DATABASE)
conn = psycopg2.connect(CONNECTION)
cur = conn.cursor()
cur.execute("LISTEN testyy")
#cur.execute("NOTIFY testyy, 'this connection works';")
conn.commit()
print("Waiting for notifications on channel 'test'")


while True:
    if select.select([conn],[],[],10) == ([],[],[]):
        print("Timeout")
    else:
        conn.poll()
        while conn.notifies:
            notify = conn.notifies.pop(0)
            print("Got NOTIFY:", notify.pid, notify.channel, notify.payload)