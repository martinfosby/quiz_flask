import mysql.connector

class MySQLTransaction:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def __enter__(self):
        self.cursor.execute("START TRANSACTION")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.cursor.execute("ROLLBACK")
        else:
            self.cursor.execute("COMMIT")
        self.cursor.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params)

    def executemany(self, sql, seq_params):
        self.cursor.executemany(sql, seq_params)
