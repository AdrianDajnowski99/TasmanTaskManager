from pathlib import Path
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
# DbHandling is responsible for opening and closing the database

class DbHandling:
    @staticmethod
    def connect_to_db():
        try:
            conn = psycopg2.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT")
            ) 
            return conn
        except Exception as e:
            print("Unable to connect to database")
            raise e

    @staticmethod
    def disconnect_db(connection):
        if connection:
            print("---Connection to database closed---")
            connection.close()
