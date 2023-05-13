import mysql.connector
from mysql.connector import errorcode, Error

class UserHasAnswer:

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



    def get_composite_id(self, user_id, answer_id):
        try:
            self.cursor.execute("SELECT * FROM user_has_answer WHERE user_id=(%s) and answer_id=(%s)", (user_id, answer_id))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result

    def join_users_answers(self):
        try:
            join_stmt = '''
                SELECT *
                FROM user
                INNER JOIN user_has_answer
                ON user.id = user_has_answer.user_id
                INNER JOIN answer
                ON answer.id = user_has_answer.answer_id;

            '''
            self.cursor.execute(join_stmt)
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result

    def join_users_answers_with_id(self, user_id, answer_id):
        try:
            join_stmt = '''
                SELECT *
                FROM user
                INNER JOIN user_has_answer
                ON user.id = user_has_answer.user_id
                INNER JOIN answer
                ON answer.id = user_has_answer.answer_id;
                WHERE user.id=%s and answer.id=%s;
            '''
            data = (user_id, answer_id)
            self.cursor.execute(join_stmt, data)
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result

    def get_composite_id_by_answer_id(self, answer_id):
        try:
            self.cursor.execute("SELECT * FROM user_has_answer WHERE answer_id=(%s)", (answer_id,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result

    def get_user_id(self, user_id):
        try:
            self.cursor.execute("SELECT * FROM user_has_answer WHERE user_id=(%s)", (user_id,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result

    def get_answer_id(self, answer_id):
        try:
            self.cursor.execute("SELECT * FROM user_has_answer WHERE answer_id=(%s)", (answer_id,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result

    def insert_into(self, user_id, answer_id):
        try:
            insert_stmt = '''
                INSERT INTO user_has_answer (user_id, answer_id) VALUES (%s, %s);
            '''
            data = (user_id, answer_id)
            self.cursor.execute(insert_stmt, data)
            result = self.cursor.fetchall()
            return True
        except mysql.connector.Error as err:
            print(err)
            return False
    
    def update_user_has_answer(self, user_id, answer_id):
        try:
            self.cursor.execute("UPDATE user_has_answer SET answer_id=(%s) WHERE user_id=(%s);", (answer_id, user_id))
            return True
        except mysql.connector.Error as err:
            print(err)
            return False

    def delete_user_has_answer(self,user_id, answer_id):
        try:
            self.cursor.execute("DELETE FROM user_has_answer WHERE user_id=(%s) AND answer_id=(%s);", (user_id, answer_id))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result