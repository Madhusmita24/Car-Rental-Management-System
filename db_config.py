import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost", user="root", password="yourpassword", database="car_rental"
    )
