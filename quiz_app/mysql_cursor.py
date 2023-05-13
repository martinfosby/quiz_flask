import mysql.connector
from mysql.connector import Error

import logging
logger = logging.getLogger('app.log')

class MySqlCursor:
    def __init__(self, host='localhost', user='root', password='test', database='quiz_web_app'):
        dbconfig = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
        }
        self.configuration = dbconfig


    def __enter__(self):
        self.conn = mysql.connector.connect(**self.configuration)
        self.cursor = self.conn.cursor(prepared=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_trace):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def execute_select(self, stmt):
        try:
            self.cursor.execute(stmt)
            result = self.cursor.fetchall()
        except Error as err:
            print(err)
            logger.error(err)
        return result
            