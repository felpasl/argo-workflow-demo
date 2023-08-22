import psycopg2
import os
import sys
import json

class InsertMessage:
    def __init__(self):
        self.p_user = os.getenv('POSTGRES_USER')
        self.p_password = os.getenv('POSTGRES_PASSWORD')
        self.p_host = os.getenv('POSTGRES_HOST')
        self.p_port = os.getenv('POSTGRES_PORT')
        self.p_db = os.getenv('POSTGRES_DB')
        self.conn_string = f"postgresql://{self.p_user}:{self.p_password}@{self.p_host}:{self.p_port}/{self.p_db}"
        self.conn = psycopg2.connect(self.conn_string)
        self.cursor = self.conn.cursor()

    def create_table(self):
        sql = "CREATE TABLE IF NOT EXISTS messages (message VARCHAR(255));"
        self.cursor.execute(sql)
        print(self.cursor.statusmessage)

    def insert_message(self, message):
        sql = "INSERT INTO messages (message) VALUES (%(message)s);"
        param = {'message': message}
        self.cursor.execute(sql, param)
        print(self.cursor.statusmessage)

    def close_connection(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

if __name__ == '__main__':
    insert_message = InsertMessage()
    insert_message.create_table()
    message = json.loads(sys.argv[0])
    insert_message.insert_message(message)
    insert_message.close_connection()
