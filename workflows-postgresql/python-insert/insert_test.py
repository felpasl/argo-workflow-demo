import os
import sys
import json
from pandas import json_normalize

class InsertMessage:
    
    def create_table(self):
        sql = "CREATE TABLE IF NOT EXISTS messages (message VARCHAR(255));"
        print(sql)

    def insert_message(self, message):
        sql = "INSERT INTO messages (message) VALUES (%(message)s);"
        print (sql)
        print (message)

if __name__ == '__main__':
    insert_message = InsertMessage()
    insert_message.create_table()
    print(sys.argv[1])
    message = json_normalize(json.loads(sys.argv[1]))
    insert_message.insert_message(message)
