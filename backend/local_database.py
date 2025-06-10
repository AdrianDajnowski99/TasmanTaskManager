import sqlite3
import os
from pathlib import Path

class ConnectToLocalDb:
    DB_NAME = "local_tasman.db"

    @staticmethod
    def connect_to_db():
        db_path = Path(r"C:\general_reps\Exercise1_tts\backend\emergency_local_database\local_tasman.db")
        conn = sqlite3.connect(db_path)
        return conn
    
    @staticmethod
    def disconnect_db(connection):
        if connection:
            print("---Connection to database closed---")
        connection.close()

    @staticmethod
    def is_main_db_online(connection):
        try:
            from db_handling import DbHandling
            conn = DbHandling.connect_to_db()
            conn.close()
            return True
        except Exception:
            return False
        
    @staticmethod
    def get_connection():
        if ConnectToLocalDb.is_main_db_online():
            from db_handling import DbHandling
            return DbHandling.connect_to_db()
        else:
            return ConnectToLocalDb.connect_to_db()
