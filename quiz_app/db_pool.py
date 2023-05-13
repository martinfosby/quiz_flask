# db_pool.py

import mysql.connector.pooling

# Create a connection pool
connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name='my_pool',
    pool_size=5,
    host='localhost',
    database='quiz_web_app',
    user='root',
    password='test'
)

# Get a connection from the pool
def get_connection():
    return connection_pool.get_connection()

# Release the connection back to the pool
def release_connection(connection):
    connection_pool.release_connection(connection)
