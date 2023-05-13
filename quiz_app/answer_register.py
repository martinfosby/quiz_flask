import mysql.connector

class AnswerRegister:

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

    def get_all_answers(self):
        try:
            select_stmt = "SELECT * FROM answer"
            self.cursor.execute(select_stmt)
            quizes = self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
        return quizes

    def get_answer_by_id(self, id):
        try:
            self.cursor.execute("SELECT * FROM answer WHERE id=(%s)", (id,))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(err)

    def get_answer_by_answer(self, answer):
        try:
            self.cursor.execute("SELECT * FROM answer WHERE answer=(%s)", (answer,))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(err)

    def get_answer_by_quiz_id(self, quiz_id):
        try:
            self.cursor.execute("SELECT * FROM answer WHERE quiz_id=(%s)", (quiz_id,))
            answers = self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
        return answers

    def get_answer_dict_by_quiz_id(self, quiz_id):
        try:
            # configure the cursor to return a list of dictionaries
            self.cursor = self.conn.cursor(dictionary=True)
            self.cursor.execute("SELECT * FROM answer WHERE quiz_id=(%s)", (quiz_id,))
            answers = self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
        finally:
            self.cursor = self.conn.cursor()

        return answers

    def get_answer_correct_dict_by_quiz_id(self, quiz_id):
        try:
            # configure the cursor to return a list of dictionaries
            self.cursor = self.conn.cursor(dictionary=True)
            self.cursor.execute("SELECT answer, correct FROM answer WHERE quiz_id=(%s)", (quiz_id,))
            answers = self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
        finally:
            self.cursor = self.conn.cursor()

        return answers

    def create_answer_for_quiz(self, answer, correct, quiz_id):
        try:
            insert_stmt = (
                "INSERT INTO answer (answer, correct, quiz_id) "
                "VALUES (%s, %s, %s)"
            )
            data = (answer, correct, quiz_id)
            self.cursor.execute(insert_stmt, data)
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(err)



    
    def update_answer_by_id(self, id, answer, correct, quiz_id):
        try:
            sql1 = '''
            UPDATE 
                answer
            SET 
                answer = %s,
                correct = %s
            WHERE
                id = %s AND quiz_id = %s;
            '''
            self.cursor.execute(sql1, (answer, correct, id, quiz_id))
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)

    def delete_answer_by_id(self, id):
        try:
            self.cursor.execute("DELETE FROM answer WHERE quiz_id=(%s)", (id,))
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
