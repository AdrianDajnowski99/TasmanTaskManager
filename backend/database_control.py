import datetime
import atexit
import psycopg2
from db_handling import DbHandling as db_conn
from error_mapper import ErrorMapper

conn = db_conn.connect_to_db()
database_name = "tasks_2rfh"

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
            cursor.execute(action_query, params)
            db_connection.commit()
        except psycopg2.Error as e:
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
        title_query_check = "SELECT title FROM tasks WHERE title LIKE %s"
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
        print("Existing tasks Titles:")
        for show_titles in titles:
            print(show_titles[0])
        return [show_titles[0] for show_titles in titles]

    @staticmethod
    def normalize_status_input(task_status):
        status_inputs = ["To Do", "In Progress", "Done", "ND"]
        task_status = task_status.strip().lower()
        for status in status_inputs:
            if task_status.lower() == status.lower():
                return status
        return None

    @staticmethod
    def add_task(title, description, task_status, cursor):
        task_id = DbControl.generate_unique_task_id()
        normalized_status = DbControl.normalize_status_input(task_status)
        task_title = DbControl.generate_unique_title(cursor, title)
        action_query = f"INSERT INTO {database_name} (id, title, description, status) VALUES (%s, %s, %s, %s)"
        SafeDatabaseExecutor.execute_errors_query(cursor.connection, action_query, (task_id, task_title, description, normalized_status))
        return task_title

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
    def update_task(task_status, task_title, cursor):
        normalized_status = DbControl.normalize_status_input(task_status)
        action_query = f"UPDATE {database_name} SET status = %s WHERE title = %s;"
        SafeDatabaseExecutor.execute_errors_query(cursor.connection, action_query, (normalized_status, task_title))
        cursor.connection.commit()
        print(f"DATABASE NOTIFICATION: Task (name: {task_title}) has been successfully updated in database")
        return "Task has been successfully updated in database"

    @staticmethod
    def delete_task(task_title, cursor):
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
