from pathlib import Path
import sqlite3

#DbHandling is responsible for opening and closing the database

class DbHandling:
    @staticmethod
    def connect_to_db():
        db_path = Path(r"C:\general_reps\exercise1_tts\backend\tasks.db")
        conn = sqlite3.connect(db_path)
        return conn

    @staticmethod
    def disconnect_db(connection):
        if connection:
            print("---Connection to database closed---")
        connection.close()
