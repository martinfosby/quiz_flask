import mysql.connector

# MySQL database configuration

config = {

    'user': 'user',
    'password': 'test',
    'host': 'localhost',
    'database': 'quiz_web_app',
}

# Function to get a database connection

def db_get_connection():
    return mysql.connector.connect(**config)

# Function to query multiple rows from the database

def db_query_rows(sql, vars=None):
    conn = db_get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, vars)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


# Function to query a single row from the database
def db_query_single(sql, vars=None):
    conn = db_get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, vars)
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row

# Function to execute a statement on the database
def db_exec(sql, vars=None):
    conn = db_get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, vars)
    conn.commit()
    cursor.close()
    conn.close()