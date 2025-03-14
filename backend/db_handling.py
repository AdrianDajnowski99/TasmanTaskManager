from pathlib import Path
import psycopg2

# DbHandling is responsible for opening and closing the database

class DbHandling:
    @staticmethod
    def connect_to_db():
        conn = psycopg2.connect(
            dbname="tasks_2rfh",
            user="adrian99",
            password="baHBJlnWjzhc7y0hcRyVi1xl4yKhKFnJ",
            host="dpg-cv85t4ogph6c739b0di0-a",
            port="5432"
        )
        return conn

    @staticmethod
    def disconnect_db(connection):
        if connection:
            print("---Connection to database closed---")
        connection.close()
