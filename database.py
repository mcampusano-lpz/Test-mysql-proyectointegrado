import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='RGbeauty',
            user='root',
            password='123456'
        )
        return connection
    except Error as e:
        print(f"Error conectando a MySQL: {e}")
        return None