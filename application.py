import datetime
import sys
import os
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))
from flask import Flask, render_template, request, redirect, url_for, jsonify, url_for, session, flash
from backend.user_auth import UserAuthentication as auth
from backend.db_handling import DbHandling as db_conn
from backend.database_control import DbControl as controls
from backend.database_control import Testing as testing
from backend.database_control import status_inputs as status_inputs
from datetime import datetime

load_dotenv()

app = Flask(__name__, 
            template_folder='frontend/templates',  
            static_folder='frontend/static') 
app.secret_key = 'SECRET_KEY'

@app.route ('/api/check_username', methods=['GET'])
def check_username():
    username = request.args.get('username')
    if not username:
        return jsonify({'exists': False})
    user = auth.get_user_by_username(username)
    return jsonify({'exists': user is not None})
    
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth.verify_user(username, password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm_password']
        if password != confirm:
            flash('Passwords do not match')
            return render_template('register.html')
        try:
            auth.create_user(username, password)
            session['username'] = username
            flash('Registration successful. You are now logged in.')
            return redirect(url_for('index'))
        except Exception as e:
            flash('Username already exists')
            return render_template('register.html')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/denied')
def denied():
    return render_template('denied.html')

@app.route('/', methods=['GET'])
@login_required
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
    username = session.get('username')
    return render_template('index.html', tasks=tasks, username=username, sort_by=sort_by, order=order, existing_ids=existing_ids, existing_titles=existing_titles)


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

    if status not in status_inputs:
        print("Invalid status, opeation can not be performed")

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
    if status not in status_inputs:
        print("Invalid status")

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

@app.route('/api/tasks/status', methods=['GET'])
def api_status():
    return jsonify({"status": "API is online"}), 200

@app.route('/api/tasks/single/<task_id>', methods=['GET'])
def api_get_single_task(task_id):
    if not task_id.isdigit():
        return jsonify("Task ID must be an integer."), 400
    
    task_id = int(task_id)
    conn = db_conn.connect_to_db()
    cursor = conn.cursor()
    single_task = testing.get_single_task_by_id(cursor, task_id)
    cursor.close()
    db_conn.disconnect_db(conn)
    
    if single_task:
        task = {
            "id": single_task[0],
            "title": single_task[1],
            "description": single_task[2],
            "status": single_task[3]
        }
        return jsonify(task), 200
    else:
        return jsonify("Task not found"), 404

@app.route('/api/tasks/all', methods=['GET'])
def api_get_all_tasks():
    sort_by = request.args.get('sort_by', 'id')
    order = request.args.get('order', 'asc')
    conn = db_conn.connect_to_db()
    cursor = conn.cursor()
    tasks = controls.get_all_tasks(cursor, sort_by, order)
    cursor.close()
    db_conn.disconnect_db(conn)
    return jsonify(tasks), 200

@app.route('/api/tasks/', methods=['POST'])
def api_add_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description', " ")
    status = data.get('status')

    if not title or title == "" or len(title) >= 50:
        return jsonify("Title is too long, 50 characters is allowed"), 400
    
    current_date = datetime.now().strftime("[%d-%m-%Y] ")

    if description:
        description = f"{current_date} {description}"
    else:
        description = current_date

    if len(description) > 267:
        return jsonify("Description is too long, 267 characters is allowed"), 400

    if status not in status_inputs:
        return jsonify("Invalid status, operation can not be performed"), 400

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

    conn = db_conn.connect_to_db()
    cursor = conn.cursor()
    all_ids = controls.get_all_existing_ids(cursor)

    if not isinstance(task_id, int):
        return jsonify("Task ID must be an integer"), 400
    if task_id < 0:
        return jsonify("Task ID cannot be a negative"), 400

    if task_id not in all_ids:
        cursor.close()
        db_conn.disconnect_db(conn)
        return jsonify("Task with given ID not found"), 404

    if not title or title == "" or len(title) >= 50:
        return jsonify("Title is too long, 50 characters is allowed"), 400

    current_date = datetime.now().strftime("[%d-%m-%Y] ")
    if description:
        description = f"{current_date} {description}"
    else:
        description = current_date
        
    if len(description) > 267:
        return jsonify("Description is too long, 267 characters is allowed"), 400

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

@app.route('/api/tasks/<string:title>', methods=['PUT'])
def api_update_task(title):
    data = request.get_json()
    status = data.get('status')
    conn = db_conn.connect_to_db()
    cursor = conn.cursor()
    try:
        if not title or title == "" or len(title) >= 50:
            return jsonify("Title is too long, 50 characters is allowed"), 400
        
        if title not in controls.get_all_existing_titles(cursor):
            return jsonify("Task with given title not found"), 404

        if status not in status_inputs:
            return jsonify({"error": "Invalid status, operation cannot be performed"}), 400

        controls.update_task(status, title, cursor)
        conn.commit()
        return jsonify({'message': 'Task status updated successfully'}), 200
    
    except Exception as e:
        return jsonify({'error': f'Could not update task: {str(e)}'}), 400
    
    finally:
        cursor.close()
        db_conn.disconnect_db(conn)

@app.route('/api/tasks/<string:title>', methods=['DELETE'])
def api_delete_task(title):
    conn = db_conn.connect_to_db()
    cursor = conn.cursor()
    try:
        if title not in controls.get_all_existing_titles(cursor):
            return jsonify("Task with given title not found"), 404
        controls.delete_task(title, cursor)
        conn.commit()
        response = {'message': 'Task deleted successfully'}
    except Exception as e:
        response = {'error': str(e)}
    finally:
        cursor.close()
        db_conn.disconnect_db(conn)
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5005, debug=True)
