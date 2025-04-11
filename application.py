import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))
from flask import Flask, render_template, request, redirect, url_for, jsonify
from backend.db_handling import DbHandling as db_conn
from backend.database_control import DbControl as controls
from datetime import datetime

app = Flask(__name__, 
            template_folder='frontend/templates',  
            static_folder='frontend/static')       

DATABASE = "tasman2nd"

@app.route('/', methods=['GET'])
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

@app.route('/api/tasks', methods=['GET'])
def api_get_tasks():
    sort_by = request.args.get('sort_by', 'id')
    order = request.args.get('order', 'asc')
    conn = db_conn.connect_to_db()
    cursor = conn.cursor()
    tasks = controls.get_all_tasks(cursor, sort_by, order)
    cursor.close()
    db_conn.disconnect_db(conn)
    return jsonify(tasks), 200

@app.route('/api/tasks', methods=['POST'])
def api_add_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description', " ")
    status = data.get('status')

    current_date = datetime.now().strftime("[%d-%m-%Y] ")
    if description:
        description = f"{current_date} {description}"
    else:
        description = current_date

    conn = db_conn.connect_to_db()
    cursor = conn.cursor()
    try:
        controls.add_task(title, description, status, cursor)
        conn.commit()
        response = {'message': 'Task added successfully'}
    except Exception as e:
        response
    finally:
        cursor.close()
        db_conn.disconnect_db(conn)
    return jsonify(response), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def api_edit_task(task_id):
    data = request.get_json()
    title = data.get('title')
    description = data.get('description', " ")

    current_date = datetime.now().strftime("[%d-%m-%Y] ")
    if description:
        description = f"{current_date} {description}"
    else:
        description = current_date

    conn = db_conn.connect_to_db()
    cursor = conn.cursor()
    try:
        controls.edit_task(task_id, title, description, cursor)
        conn.commit()
        response = {'message': 'Task updated successfully'}
    except Exception as e:
        response = {'error': str(e)}
    finally:
        cursor.close()
        db_conn.disconnect_db(conn)
    return jsonify(response), 200

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def api_update_task(task_id):
    data = request.get_json()
    status = data.get('status')

    conn = db_conn.connect_to_db()
    cursor = conn.cursor()
    try:
        controls.update_task(status, task_id, cursor)
        conn.commit()
        response = {'message': 'Task status updated successfully'}
    except Exception as e:
        response = {'error': str(e)}
    finally:
        cursor.close()
        db_conn.disconnect_db(conn)
    return jsonify(response), 200

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def api_delete_task(task_id):
    conn = db_conn.connect_to_db()
    cursor = conn.cursor()
    try:
        controls.delete_task(task_id, cursor)
        conn.commit()
        response = {'message': 'Task deleted successfully'}
    except Exception as e:
        response = {'error': str(e)}
    finally:
        cursor.close()
        db_conn.disconnect_db(conn)
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(port=5005, debug=False)
