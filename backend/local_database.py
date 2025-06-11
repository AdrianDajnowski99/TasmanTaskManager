import sqlite3
import os
from pathlib import Path

class ConnectToLocalDb:
    DB_NAME = "local_tasman.db"

    @staticmethod
    def get_db_path():
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(script_dir, '..', 'data')
        os.makedirs(data_dir, exist_ok=True)
        return os.path.join(data_dir, ConnectToLocalDb.DB_NAME)

    @staticmethod
    def init_db():
        from database_control import database_name
        db_path = ConnectToLocalDb.get_db_path()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {database_name} (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description optional TEXT,
                status TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    @staticmethod
    def connect_to_db():
        db_path = ConnectToLocalDb.get_db_path()

        if not os.path.exists(db_path):
            ConnectToLocalDb.init_db()
        return sqlite3.connect(db_path)

    @staticmethod
    def disconnect_db(connection):
        if connection:
            connection.close()

    @staticmethod
    def is_online_db_available():
        try:
            from db_handling import DbHandling
            conn = DbHandling.connect_to_db()
            conn.close()
            return True
        except Exception:
            return False

    @staticmethod
    def get_db_connection():
        if ConnectToLocalDb.is_online_db_available():
            from db_handling import DbHandling
            return DbHandling.connect_to_db()
        else:
            return ConnectToLocalDb.connect_to_db()
        