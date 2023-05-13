import mysql.connector

class QuizRegister:

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

    def join_quiz_with_answer(self):
        try:
            join_stmt = '''SELECT * from quiz JOIN answer ON quiz.id=answer.quiz_id;'''
            self.cursor.execute(join_stmt)
            quizes = self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
        return quizes


    def get_all_quiz(self):
        try:
            select_stmt = "SELECT * FROM quiz"
            self.cursor.execute(select_stmt)
            quizes = self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
        return quizes
    
    def get_all_quiz_as_list(self):
        try:
            select_stmt = "SELECT * FROM quiz"
            self.cursor.execute(select_stmt)
            quizes = self.cursor.fetchall()
            quizes = [list(row) for row in quizes]
        except mysql.connector.Error as err:
            print(err)
        return quizes

    def get_quiz_by_id(self, id):
        try:
            self.cursor.execute("SELECT * FROM quiz WHERE id=(%s)", (id,))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(err)

    def get_quiz_title_by_id(self, id):
        try:
            self.cursor.execute("SELECT title FROM quiz WHERE id=(%s)", (id,))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(err)


    def create_quiz(self, title, question, active, category, admin_id):
        try:
            insert_stmt = (
                "INSERT INTO quiz (title, question, active, category, administrator_id) "
                "VALUES (%s, %s, %s, %s, %s)"
            )
            data = (title, question, active, category, admin_id)
            self.cursor.execute(insert_stmt, data)
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(err)

    def set_active_by_id(self, active, id):
        try:
            sql1 = '''
            UPDATE 
                quiz
            SET 
                active = %s
            WHERE
                id = %s
            '''
            self.cursor.execute(sql1, (active, id))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(err)

    def update_quiz_by_id(self, id, title, question, active, category):
        try:
            sql1 = '''
            UPDATE 
                quiz
            SET 
                title = %s,
                question = %s,
                active = %s,
                category = %s
            WHERE
                id = %s
            '''
            self.cursor.execute(sql1, (title, question, active, category, id))
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)

    def update_quiz_question_by_id(self, id, question):
        try:
            sql1 = '''
            UPDATE 
                quiz
            SET 
                question = %s
            WHERE
                id = %s
            '''
            self.cursor.execute(sql1, (question, id))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(err)



    def delete_quiz_by_id(self, id):
        try:
            self.cursor.execute("DELETE FROM quiz WHERE id=(%s);", (id,))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(err)

    def get_length_all_quizes(self):
        try:
            self.cursor.execute("SELECT COUNT(*) as length FROM quiz;")
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(err)



