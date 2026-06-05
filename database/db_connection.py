import mysql.connector


def get_connection():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Tanvee@1311",
        port=3306,
        database="billing_system"
    )