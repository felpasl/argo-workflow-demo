import os
import sys
import json
from pandas import json_normalize
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData

class InsertMessage:
    def __init__(self):
        self.p_user = os.getenv('POSTGRES_USER')
        self.p_password = os.getenv('POSTGRES_PASSWORD')
        self.p_host = os.getenv('POSTGRES_HOST')
        self.p_port = os.getenv('POSTGRES_PORT')
        self.p_db = os.getenv('POSTGRES_DB')
        self.conn_string = f"postgresql://{self.p_user}:{self.p_password}@{self.p_host}:{self.p_port}/{self.p_db}"
        
        self.engine = create_engine(self.conn_string)
        self.metadata = MetaData()
        self.conn = self.engine.connect()

    def create_table(self):
        messageTable = Table('messages', 
                             self.metadata,
                             Column('message', String))
        self.metadata.create_all(self.engine, checkfirst=True)

    def insert_message(self, message):
        
        print(message.to_sql('messages', con=self.engine, if_exists='replace',
          index=False))

    def close_connection(self):
        self.conn.commit()
        self.conn.close()

if __name__ == '__main__':
    insert_message = InsertMessage()
    insert_message.create_table()
    print(sys.argv[1])
    message = json_normalize(json.loads(sys.argv[1]))
    insert_message.insert_message(message)
    insert_message.close_connection()
