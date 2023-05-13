import mysql.connector
from mysql.connector import errorcode, Error

class UserRegister:

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

    def __enter__(self):
        self.conn = mysql.connector.connect(**self.configuration)
        self.cursor = self.conn.cursor(prepared=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_trace) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def get_all_user(self):
        try:
            self.cursor.execute("SELECT * FROM user")
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result

    def get_all_username(self):
        try:
            self.cursor.execute("SELECT username FROM user")
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result

    def get_all_id_username(self):
        try:
            self.cursor.execute("SELECT id, username FROM user")
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result

    def get_user(self, username):
        try:
            self.cursor.execute("SELECT * FROM user WHERE  username=(%s)", (username,))
            result = self.cursor.fetchone()
        except mysql.connector.Error as err:
                print(err)
        return result

    def getUserById(self, id):
        try:
            self.cursor.execute("SELECT * FROM user WHERE  id=(%s)", (id,))
            result = self.cursor.fetchone()
        except mysql.connector.Error as err:
                print(err)
        return result

    

    def updateUser(self, username):
        try:
            sql1 = '''
            UPDATE 
                user
            SET 
                username = %s, password = %s
            WHERE
                id = %s
                '''
            self.cursor.execute(sql1, username)
        except mysql.connector.Error as err:
                print(err)

    def create_user(self, username, password):
        try:
            if not self.exist_user(username):
                insert_stmt = (
                        "INSERT INTO user (username, password_hash) "
                        "VALUES (%s, %s)"
                    )
                data = (username, password)
                self.cursor.execute(insert_stmt, data)
                return True
            else: return False
        except Error as e:
            print(e)
            return False
    
    def exist_user(self, username):
        try:
            select_stmt = f"SELECT EXISTS(SELECT 1 FROM user WHERE username = '{username}');"
            self.cursor.execute(select_stmt)
            exists = self.cursor.fetchall()
            exists = exists[0][0]
            if exists:
                return True
            else: return False
        except Error as e:
            print(e)

