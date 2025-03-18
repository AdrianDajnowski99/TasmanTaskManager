import atexit
import os
from db_handling import DbHandling as db_conn

database_name = "tasks"
invalid_input_output = "Invalid input. Please try again."

class TaskManager:

    @staticmethod
    def display_interface_message():
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path_interface = os.path.join(script_dir, "interface_message.txt")
        with open(file_path_interface, "r") as file:
            print(file.read())

    @staticmethod
    def display_errors_message():
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path_interface = os.path.join(script_dir, "error_message.txt")
        with open(file_path_interface, "r") as file:
            print(file.read())

    @staticmethod
    def add_task(db_connection):
        from database_control import DbControl
        cursor = db_connection.cursor()
        title = str(input("Enter your task title: "))
        add_description_choice = input("Do you want to add a description to your task? (Choose [Y] for YES or [N] for NO): ")

        if add_description_choice.upper() == "Y":
            description = str(input("Enter your task description: "))
        else:
            description = None
            print("Adding task description has been skipped.")

        while True:
            print("TIP: The input is case-insensitive. The program will normalize it.")
            task_status = input("DATABASE: Choose a status from the list: (To Do/In Progress/Done/ND)").strip()
            normalized = DbControl.normalize_status_input(task_status)

            if normalized:
                print(f"DATABASE NOTIFICATION: Input accepted and normalized to: {normalized}")
                task_title = DbControl.add_task(title, description, task_status, cursor)
                print(f"DATABASE NOTIFICATION: New task (named: {task_title}) was successfully added to the database.")
                break
            else:
                print(invalid_input_output)
        cursor.close()

    @staticmethod
    def show_tasks(db_connection):
        from database_control import DbControl
        cursor = db_connection.cursor()
        DbControl.show_tasks(cursor)
        cursor.close()



    @staticmethod
    def edit_task(db_connection):
        from database_control import DbControl
        cursor = db_connection.cursor()
        existing_ids = DbControl.get_all_existing_ids(cursor)
        task_id = int(input("DATABASE: Select an ID from the database: "))
        

        if task_id not in existing_ids:
            print("DATABASE ERROR: ID does not exist. Try again")
            cursor.close()
            return
        
        while True:
            title = str(input("Enter your task title: "))
            add_description_choice = input("Do you want to add a description to your task? (Choose [Y] for YES or [N] for NO): ")

            if add_description_choice.upper() == "Y":
                description = str(input("Enter your task description: "))
            else:
                description = None
                print("Adding task description has been skipped.")

            task_title = DbControl.edit_task(task_id, title, description, cursor)
            print(f"DATABASE NOTIFICATION: Task (id: {task_id}) has been successfully updated in database.")
            break
        cursor.close()



    @staticmethod
    def update_task(db_connection):
        from database_control import DbControl 
        cursor = db_connection.cursor()
        existing_titles = DbControl.get_all_existing_titles(cursor)
        task_title = str(input("DATABASE: Select a title from the database: "))

        if task_title not in existing_titles:
            print("DATABASE ERROR: Title does not exist. Try again.")
            cursor.close()
            return

        while True:
            print("TIP: The input is case-insensitive. The program will normalize it.")
            task_status = input("DATABASE: Choose a status from the list: (To Do/In Progress/Done/ND)").strip()
            normalized = DbControl.normalize_status_input(task_status)

            if normalized:
                print(f"DATABASE NOTIFICATION: Input accepted and normalized to: {normalized}")
                DbControl.update_task(task_status, task_title, cursor)
                break
            else:
                print(invalid_input_output)
        cursor.close()

    @staticmethod
    def delete_task(db_connection):
        from database_control import DbControl
        cursor = db_connection.cursor()
        existing_titles = DbControl.get_all_existing_titles(cursor)
        task_title = str(input("DATABASE: Select a title from the database: "))

        if task_title not in existing_titles:
            print("DATABASE ERROR: Title does not exist. Try again.")
            cursor.close()
            return

        DbControl.delete_task(task_title, cursor)
        print(f"DATABASE NOTIFICATION: Task '{task_title}' has been successfully deleted.")
        cursor.close()

    @staticmethod
    def tasker(conn):
        atexit.register(db_conn.disconnect_db, conn)
        print("_____________________________________________________________")
        TaskManager.display_interface_message()

        choice = input("Choose the preferred operation (1/2/3/4/9/O): ")

        if choice == '1':
            TaskManager.add_task(conn)
        elif choice == '2':
            TaskManager.show_tasks(conn)
        elif choice == '3':
            TaskManager.update_task(conn)
        elif choice == '4':
            TaskManager.delete_task(conn)
        elif choice == '5':
            TaskManager.edit_task(conn)
        elif choice == '9':
            TaskManager.show_errors_list()
        elif choice == "0":
            TaskManager.input_exit()
        else:
            print("Invalid input. Please try again.")

    @staticmethod
    def show_errors_list():
        TaskManager.display_errors_message()

    @staticmethod
    def input_exit():
        print("IN-TERMINAL INTERFACE NOTIFICATION: Quitting...")
        quit()

def get_existing_titles(conn):
    from database_control import DbControl 
    cursor = conn.cursor()
    existing_titles = DbControl.get_all_existing_titles(cursor)
    cursor.close()
    return existing_titles

def validate_task_title(task_title, existing_titles):
    if task_title not in existing_titles:
        print("DATABASE ERROR: ID does not exist. Try again")
        return False
    return True

def normalize_status_input():
    from database_control import DbControl 
    while True:
        print("TIP: The input is case-insensitive. Program will normalise it.")
        task_status = input("DATABASE: Choose status from the list: (To Do/In Progress/Done/ND)").strip()
        normalized = DbControl.normalize_status_input(task_status)
        if normalized:
            print(f"DATABASE NOTIFICATION: Input accepted and normalised to: {normalized}")
            return normalized
        else:
            print("Invalid input. Please try again.")
            