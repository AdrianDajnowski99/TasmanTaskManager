import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from backend.db_handling import DbHandling as db_conn


class UserAuthentication:
    @staticmethod
    def create_user(username, password):
        conn = db_conn.connect_to_db()
        cursor = conn.cursor()
        password_hash = generate_password_hash(password)
        auth_query = f"INSERT INTO private.users (username, password_hash) VALUES (%s, %s)"
        cursor.execute(auth_query, (username, password_hash))
        conn.commit()
        cursor.close()
        db_conn.disconnect_db(conn)


    @staticmethod
    def get_user_by_username(username):
        conn = db_conn.connect_to_db()
        cursor = conn.cursor()
        auth_query = f"SELECT id, username, password_hash FROM private.users WHERE username = %s"
        cursor.execute(auth_query, (username,))
        user = cursor.fetchone()
        cursor.close()
        db_conn.disconnect_db(conn)
        return user
    
    @staticmethod
    def verify_user(username, password):
        user = UserAuthentication.get_user_by_username(username)
        if user and check_password_hash(user[2], password):
            return True
        return False
    


