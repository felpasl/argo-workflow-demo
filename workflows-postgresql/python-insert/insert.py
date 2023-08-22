import psycopg2
import os
import sys

p_user = os.getenv('POSTGRES_USER')
p_password = os.getenv('POSTGRES_PASSWORD')
p_host = os.getenv('POSTGRES_HOST')
p_port = os.getenv('POSTGRES_PORT')
p_db = os.getenv('POSTGRES_DB')
conn_string = f"postgresql://{p_user}:{p_password}@{p_host}:{p_port}/{p_db}"
conn = psycopg2.connect(conn_string)
sql = "CREATE TABLE IF NOT EXISTS messages (message VARCHAR(255));"
cursor = conn.cursor()
cursor.execute(sql)
print(cursor.statusmessage)

sql = "INSERT INTO messages (message) VALUES (%(message)s);"
param = sys.argv[0]

cursor.execute(sql, param)
print(cursor.statusmessage)


conn.commit()
cursor.close()
conn.close()

