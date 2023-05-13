import mysql.connector
from mysql.connector import errorcode, Error

class AdminRegister:

    def __init__(self, host='localhost', user='root', password='test', database='quiz_web_app') -> None:

        # dbconfig = {'host': '127.0.0.1',
        #             'user': 'user',
        #             'password': 'test',
        #             'database': 'myDb', }

        dbconfig = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
        }

        self.configuration = dbconfig

    def __enter__(self) -> 'cursor':
        self.conn = mysql.connector.connect(**self.configuration)
        self.cursor = self.conn.cursor(prepared=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_trace) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def get_admin(self, username):
        try:
            self.cursor.execute("SELECT * FROM administrator WHERE username=(%s)", (username,))
            result = self.cursor.fetchone()
        except mysql.connector.Error as err:
                print(err)
        return result

    def get_password_hash(self, username, password_hash):
        try:
            self.cursor.execute("SELECT * FROM administrator WHERE username=(%s)", (username,))
            result = self.cursor.fetchone()
        except mysql.connector.Error as err:
                print(err)
        return result

    def get_admin_by_id(self, id):
        try:
            self.cursor.execute("SELECT * FROM administrator WHERE  id=(%s)", (id,))
            result = self.cursor.fetchone()
        except mysql.connector.Error as err:
                print(err)
        return result

    

    def updateAdmin(self, username):
        try:
            sql1 = '''
            UPDATE 
                administrator
            SET 
                username = %s, password = %s
            WHERE
                id = %s
                '''
            self.cursor.execute(sql1, username)
        except mysql.connector.Error as err:
                print(err)
    



    def create_admin(self, username, password, first_name, last_name):
        try:
            if not self.exist_admin(username):
                insert_stmt = (
                        "INSERT INTO administrator (username, password_hash, first_name, last_name) "
                        "VALUES (%s, %s, %s, %s)"
                    )
                data = (username, password, first_name, last_name)
                self.cursor.execute(insert_stmt, data)
                return True
            else: return False
        except Error as e:
            print(e)
            return False
    
    def exist_admin(self, username):
        try:
            select_stmt = f"SELECT EXISTS(SELECT 1 FROM administrator WHERE username = '{username}');"
            self.cursor.execute(select_stmt)
            exists = self.cursor.fetchall()
            exists = exists[0][0]
            if exists:
                return True
            else: return False
        except Error as e:
            print(e)