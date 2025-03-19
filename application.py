import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))
from flask import Flask, render_template, request, redirect, url_for
from backend.db_handling import DbHandling as db_conn
from backend.database_control import DbControl as controls
from datetime import datetime

app = Flask(__name__, 
            template_folder='frontend/templates',  
            static_folder='frontend/static')       

DATABASE = "tasks_2rfh"

@app.route('/')
def index():
    sort_by = request.args.get('sort_by', 'id')
    order = request.args.get('order', 'asc')
    conn = db_conn.connect_to_db()
    cursor = conn.cursor()
    tasks = controls.get_all_tasks(cursor, sort_by, order)
    existing_titles = controls.get_all_existing_titles(cursor)
    existing_ids = controls.get_all_existing_ids(cursor)
    cursor.close()
    db_conn.disconnect_db(conn)
    return render_template('index.html', tasks=tasks, sort_by=sort_by, order=order, existing_ids=existing_ids, existing_titles=existing_titles)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['taskNameUpdate']
    description = request.form.get('taskDescription', " ")
    status = request.form['taskStatusAdd']

    current_date = datetime.now().strftime("[%d-%m-%Y] ")
    if description:
        description = f"{current_date} {description}"
    else:
        description = current_date

    conn = db_conn.connect_to_db()
    cursor = conn.cursor()
    controls.add_task(title, description, status, cursor)
    cursor.close()
    db_conn.disconnect_db(conn)
    
    return redirect(url_for('index'))

@app.route('/edit', methods=['POST'])
def edit_task():
    id = request.form['taskIdEdit']
    title = request.form['taskNameEdit']
    description = request.form.get('taskDescription', " ")

    current_date = datetime.now().strftime("[%d-%m-%Y] ")
    if description:
        description = f"{current_date} {description}"
    else:
        description = current_date

    conn = db_conn.connect_to_db()
    cursor = conn.cursor()
    controls.edit_task(id, title, description, cursor)
    cursor.close()
    db_conn.disconnect_db(conn)
    
    return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update_task():
    title = request.form['taskNameUpdate']
    status = request.form['taskStatusUpdate']

    conn = db_conn.connect_to_db()
    cursor = conn.cursor()
    controls.update_task(status, title, cursor)
    cursor.close()
    db_conn.disconnect_db(conn)
    
    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete_task():
    title = request.form['taskNameDelete']

    conn = db_conn.connect_to_db()
    cursor = conn.cursor()
    controls.delete_task(title, cursor)
    cursor.close()
    db_conn.disconnect_db(conn)
    
    return redirect(url_for('index'))

@staticmethod
def get_all_tasks(db_connection, sort_by='id', order='ASC'):
    valid_sort_columns = ['id', 'title', 'description', 'status']
    if sort_by not in valid_sort_columns:
        sort_by = 'id'
        
    query = f"SELECT * FROM {DATABASE} ORDER BY {sort_by} {order}"
    cursor = db_connection.cursor()
    cursor.execute(query)
    tasks = cursor.fetchall()
    cursor.close()
    return tasks

if __name__ == '__main__':
    app.run(port=5005, debug=True)
