import mysql.connector
from mysql.connector import errorcode, Error

class UserHasQuiz:

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

    def join_user_quiz(self):
        try:
            join_stmt = '''
                SELECT *
                FROM user
                INNER JOIN user_has_quiz
                ON user.id = user_has_quiz.user_id
                INNER JOIN quiz
                ON quiz.id = user_has_quiz.quiz_id;
            '''
            self.cursor.execute(join_stmt)
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result

    def join_user_quiz_with_id(self, user_id, quiz_id):
        try:
            join_stmt = '''
                SELECT *
                FROM user
                INNER JOIN user_has_quiz
                ON user.id = user_has_quiz.user_id
                INNER JOIN quiz
                ON quiz.id = user_has_quiz.quiz_id
                WHERE user.id=%s and quiz.id=%s;
            '''
            data = (user_id, quiz_id)
            self.cursor.execute(join_stmt, data)
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result

    def join_user_quiz_with_quiz_id(self, quiz_id):
        try:
            join_stmt = '''
                SELECT *
                FROM user
                INNER JOIN user_has_quiz
                ON user.id = user_has_quiz.user_id
                INNER JOIN quiz
                ON quiz.id = user_has_quiz.quiz_id
                WHERE quiz.id=%s;
            '''
            data = (quiz_id,)
            self.cursor.execute(join_stmt, data)
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result

    def get_user_quiz_id_by_quiz_id(self, quiz_id):
        try:
            join_stmt = '''
                SELECT user_id, quiz_id
                FROM user
                INNER JOIN user_has_quiz
                ON user.id = user_has_quiz.user_id
                INNER JOIN quiz
                ON quiz.id = user_has_quiz.quiz_id
                WHERE quiz.id=%s;
            '''
            data = (quiz_id,)
            self.cursor.execute(join_stmt, data)
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result

    def get_composite_id(self, user_id, quiz_id):
        try:
            self.cursor.execute("SELECT * FROM user_has_quiz WHERE user_id=(%s) and quiz_id=(%s)", (user_id, quiz_id))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result

    def get_composite_id_by_quiz_id(self, quiz_id):
        try:
            self.cursor.execute("SELECT * FROM user_has_quiz WHERE quiz_id=(%s)", (quiz_id,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result

    def get_user_id(self, user_id):
        try:
            self.cursor.execute("SELECT * FROM user_has_quiz WHERE user_id=(%s)", (user_id,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result

    def get_quiz_id(self, quiz_id):
        try:
            self.cursor.execute("SELECT * FROM user_has_quiz WHERE quiz_id=(%s)", (quiz_id,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result

    def delete_quiz_id(self,user_id, quiz_id):
        try:
            self.cursor.execute("DELETE FROM user_has_quiz WHERE user_id=(%s) AND quiz_id=(%s);", (user_id, quiz_id))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result