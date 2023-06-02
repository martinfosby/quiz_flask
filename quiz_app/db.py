import mysql.connector
from mysql.connector import errorcode, Error

# MySQL database configuration

config = {

    'user': 'root',
    'password': 'test',
    'host': 'localhost',
    'database': 'quiz_web_app',
}

# Function to get a database connection

def db_get_connection():
    return mysql.connector.connect(**config)

# Function to query multiple rows from the database
def db_query_rows(sql, vars=None):
    try:
        conn = db_get_connection()
        cursor = conn.cursor(dictionary=True, prepared=True)
        cursor.execute(sql, vars)
        row = cursor.fetchall()
        cursor.close()
        conn.close()
        return row
    except Error as e:
        print(e)
        conn.rollback()


# Function to query a single row from the database
def db_query_single(sql, vars=None):
    try:
        conn = db_get_connection()
        cursor = conn.cursor(dictionary=True, prepared=True)
        cursor.execute(sql, vars)
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row
    except Error as e:
        print(e)
        conn.rollback()

# Function to execute a statement on the database
def db_exec(sql, *args, **kargs):
    try:
        conn = db_get_connection()
        cursor = conn.cursor(prepared=True)
        cursor.execute(sql, *args, **kargs)
        conn.commit()
        last_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return last_id
    except Error as e:
        print(e)
        conn.rollback()

# Function to execute a statement on the database
def db_exec_many(sql, vars=None):
    try:
        conn = db_get_connection()
        cursor = conn.cursor(prepared=True)
        cursor.executemany(sql, vars)
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        print(e)
        conn.rollback()