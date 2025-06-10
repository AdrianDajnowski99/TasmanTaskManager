import datetime
import atexit
import psycopg2
import sqlite3
from db_handling import DbHandling as db_conn
from error_mapper import ErrorMapper
from local_database import ConnectToLocalDb as local_db

conn = db_conn.connect_to_db()
database_name = "tasman2nd"
status_inputs = ["To Do", "In Progress", "Done", "ND"]

class AppStart:
    @staticmethod
    def main():
        from user_actions import TaskManager as manager
        db_connection = db_conn.connect_to_db()
        atexit.register(db_conn.disconnect_db, db_connection)
        manager.tasker(db_connection)

class SafeDatabaseExecutor:
    @staticmethod
    def execute_errors_query(db_connection, action_query, params=None):
        try:
            cursor = db_connection.cursor()
            if isinstance(db_connection, sqlite3.Connection):
                action_query = action_query.replace('%s', '?')
            cursor.execute(action_query, params)
            db_connection.commit()
        except (psycopg2.Error, sqlite3.Error) as e:
            print(f"Error: {e}")
            print(ErrorMapper.get_error_message(e))
        except Exception as e:
            print(f"Unexpected error occurred: {e}")

class DbControl:
    @staticmethod
    def generate_unique_task_id():
        now = datetime.datetime.now()
        return now.strftime("%d%m%y%M%S%f")

    @staticmethod
    def generate_unique_title(cursor, given_title):

        if isinstance(cursor.connection, sqlite3.Connection):
            title_query_check = f"SELECT title FROM {database_name} WHERE title LIKE ?"
            cursor.execute(title_query_check, (f"{given_title}%",))
        else:
            title_query_check = f"SELECT title FROM {database_name} WHERE title LIKE %s"
            cursor.execute(title_query_check, (f"{given_title}%",))
            
        existing_titles = [row[0] for row in cursor.fetchall()]

        if given_title not in existing_titles:
            return given_title

        title_suffix = 1
        new_title = f"{given_title}_{title_suffix}"
        while new_title in existing_titles:
            title_suffix += 1
            new_title = f"{given_title}_{title_suffix}"
        return new_title

    @staticmethod
    def get_all_existing_titles(cursor):
        cursor.execute(f"SELECT title FROM {database_name} ORDER BY id")
        titles = cursor.fetchall()
        return [title[0] for title in titles]
    
    @staticmethod
    def get_all_existing_ids(cursor):
        cursor.execute(f"SELECT id FROM {database_name} ORDER BY id")
        ids = cursor.fetchall()
        #print("Existing tasks IDs:")
        for show_ids in ids:
            return [show_ids[0] for show_ids in ids]

    @staticmethod
    def normalize_status_input(task_status):
        task_status = task_status.strip().lower()
        for status in status_inputs:
            if task_status.lower() == status.lower():
                return status
        return None

    @staticmethod
    def add_task(title, description, task_status, cursor):
        try:
            task_id = DbControl.generate_unique_task_id()
            normalized_status = DbControl.normalize_status_input(task_status)
            task_title = DbControl.generate_unique_title(cursor, title)

            if isinstance(cursor.connection, sqlite3.Connection):
                action_query = f"INSERT INTO {database_name} (id, title, description, status) VALUES (?, ?, ?, ?)"
            else:
                action_query = f"INSERT INTO {database_name} (id, title, description, status) VALUES (%s, %s, %s, %s)"
                
            SafeDatabaseExecutor.execute_errors_query(cursor.connection, action_query, (task_id, task_title, description, normalized_status))
            
            return task_title
        except Exception as e:
            print(f"Error adding task: {e}")
            raise

    @staticmethod
    def show_tasks(cursor):
        print("DATABASE: Showing tasks in database:")
        cursor.execute(f'SELECT * FROM {database_name} ORDER BY id')
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print("No tasks to show")
        print("DATABASE: END")

    @staticmethod
    def edit_task(task_id, task_title, description, cursor):
        task_title = DbControl.generate_unique_title(cursor, task_title)

        if isinstance(cursor.connection, sqlite3.Connection):
            action_query = f"UPDATE {database_name} SET title = ?, description = ? WHERE id = ?;"
        else:
            action_query = f"UPDATE {database_name} SET title = %s, description = %s WHERE id = %s;"
            
        SafeDatabaseExecutor.execute_errors_query(cursor.connection, action_query, (task_title, description, task_id))
        cursor.connection.commit()
        print(f"DATABASE NOTIFICATION: Task (id: {task_id}) has been successfully updated in database")
        return "Task has been successfully updated in database"    
    
    @staticmethod
    def update_task(task_status, task_title, cursor):
        normalized_status = DbControl.normalize_status_input(task_status)

        if isinstance(cursor.connection, sqlite3.Connection):
            action_query = f"UPDATE {database_name} SET status = ? WHERE title = ?;"
        else:
            action_query = f"UPDATE {database_name} SET status = %s WHERE title = %s;"
            
        SafeDatabaseExecutor.execute_errors_query(cursor.connection, action_query, (normalized_status, task_title))
        cursor.connection.commit()
        print(f"DATABASE NOTIFICATION: Task (name: {task_title}) has been successfully updated in database")
        return "Task has been successfully updated in database"
    
    @staticmethod
    def delete_task(task_title, cursor):

        if isinstance(cursor.connection, sqlite3.Connection):
            action_query = f"DELETE FROM {database_name} WHERE title = ?;"
        else:
            action_query = f"DELETE FROM {database_name} WHERE title = %s;"
            
        SafeDatabaseExecutor.execute_errors_query(cursor.connection, action_query, (task_title,))
        cursor.connection.commit()
        print(f"DATABASE NOTIFICATION: Task (name: {task_title}) has been successfully deleted from the database")
        return "Task has been successfully removed from the database"

    @staticmethod
    def get_all_tasks(cursor, sort_by='id', order='ASC'):
        valid_sort_columns = ['id', 'title', 'description', 'status']
        if sort_by not in valid_sort_columns:
            sort_by = 'id'

        query = f"SELECT * FROM {database_name} ORDER BY {sort_by} {order}"
        cursor.execute(query)
        tasks = cursor.fetchall()
        return tasks

class Testing:
    @staticmethod
    def get_single_task_by_id(cursor, task_id):

        if isinstance(cursor.connection, sqlite3.Connection):
            single_task_query = f"SELECT * FROM {database_name} WHERE id = ?"
        else:
            single_task_query = f"SELECT * FROM {database_name} WHERE id = %s"
            
        cursor.execute(single_task_query, (task_id,))
        single_task = cursor.fetchone()
        return single_task